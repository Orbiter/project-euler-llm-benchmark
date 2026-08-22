"""
Reverse-proxy / load-balancer for OpenAI-API-compatible LLM endpoints.

Reads endpoints.json and routes to the least-loaded endpoint, failing over on errors.
Endpoints that fail are excluded from routing until a successful request heals them.

Usage: python proxy.py [--port PORT] [--config FILE]
"""

import os
import sys
import json
import base64
import time
import argparse
import threading
from pathlib import Path
from typing import Dict, Iterator, List, Optional

import requests
import urllib3
from flask import Flask, request, Response, jsonify, send_file

from llm_client import Endpoint, get_llm_url_stub


# ---------------------------------------------------------------------------
# Globals - populated at startup
# ---------------------------------------------------------------------------
_endpoints: List[Endpoint] = []
_active_counts: Dict[str, int] = {}           # url -> active request count
_total_counts:  Dict[str, int] = {}           # url -> cumulative successful responses
_error_states:  Dict[str, dict] = {}          # url -> {error, ts, msg}
_counters_lock = threading.Lock()                  # guards all dicts


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

TOOLING_EXPECTED_FUNCTION_NAME = "lightswitch"
FORMAT_EXPECTED_MOODS = {"surprised", "angry", "happy"}
REQUIRED_CAPABILITY_FIELDS = (
      "has_vision",
      "has_tooling",
      "has_thinking",
      "has_format",
)


def _normalize_message_text(message):
    if not message:
        return ""
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                text = part.get("text") or part.get("content")
                if isinstance(text, str):
                    parts.append(text)
        return " ".join(parts).strip()
    if isinstance(content, dict):
        text = content.get("text")
        if isinstance(text, str):
            return text.strip()
    return ""


def _normalize_mood(value):
    mood = value.strip().lower() if isinstance(value, str) else ""
    return mood if mood in FORMAT_EXPECTED_MOODS else ""


def test_vision(endpoint):
    print(f"Testing has_vision capabilities of model {endpoint.store_name}...")
    image_path = "llmtest/testimage.png"
    if not os.path.exists(image_path):
        raise Exception(f"Test image not found: {image_path}")
    with open(image_path, "rb") as img:
        b64 = base64.b64encode(img.read()).decode("utf-8")
    from llm_client import openai_api_chat
    answer, _, _, _, _ = openai_api_chat(endpoint, prompt="what is in the image", base64_image=b64)
    result = "42" in answer
    if result:
        print(f"Model {endpoint.store_name} is multimodal.")
    else:
        print(f"Model {endpoint.store_name} is not multimodal; it returned: {answer}")
    return result


def test_tooling(endpoint):
    print(f"Testing has_tooling capability for model {endpoint.store_name}...")
    from llm_client import openai_api_chat
    _, _, _, _, _, rj = openai_api_chat(
        endpoint,
        prompt="Switch on the light",
        system_message="You are a home assistant.",
        tools=[{
            "type": "function",
            "function": {
                "name": TOOLING_EXPECTED_FUNCTION_NAME,
                "description": "Switch the light on or off.",
                "parameters": {
                    "type": "object",
                    "properties": {"state": {"type": "string", "enum": ["on", "off"]}},
                    "required": ["state"],
                    "additionalProperties": False,
                },
            },
        }],
        stream=False,
        temperature=0.0,
        return_response_json=True,
    )
    message = rj.get("choices", [{}])[0].get("message", {})
    tool_calls = message.get("tool_calls") or []
    if not tool_calls:
        return False
    function = tool_calls[0].get("function", {})
    tool_name = function.get("name") or tool_calls[0].get("name") or ""
    print(f"Tool-calling test requested tool: {tool_name}")
    return tool_name == TOOLING_EXPECTED_FUNCTION_NAME


def test_thinking(endpoint):
    print(f"Testing has_thinking capability for model {endpoint.store_name}...")
    from llm_client import openai_api_chat
    _, _, _, _, _, rj = openai_api_chat(
        endpoint,
        prompt="Think step by step and answer: what is 17 plus 25?",
        system_message="You are a helpful assistant.",
        temperature=0.1,
        max_tokens=512,
        think=True,
        stream=False,
        return_response_json=True,
    )
    for choice in rj.get("choices", []):
        message = choice.get("message", {})
        text = _normalize_message_text(message)
        if "<thinking>" in text or "</thinking>" in text:
            return True
        reasoning = choice.get("reasoning")
        if isinstance(reasoning, str) and reasoning.strip():
            return True
        if isinstance(message.get("reasoning"), str) and message.get("reasoning").strip():
            return True
    return False


def test_format(endpoint):
    print(f"Testing has_format capability for model {endpoint.store_name}...")
    from llm_client import openai_api_chat
    test_cases = [
        ("I hate programming", "angry"),
        ("I love programming", "happy"),
        ("Wait, that worked perfectly?", "surprised"),
    ]
    for input_text, expected_mood in test_cases:
        _, _, _, _, _, rj = openai_api_chat(
            endpoint,
            prompt=input_text,
            system_message="You are a mood classifier. Identify the mood of the request.",
            temperature=0.1,
            max_tokens=128,
            stream=False,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "strict": True,
                    "schema": {
                        "title": "Classifier",
                        "type": "object",
                        "properties": {"mood": {"type": "string", "enum": sorted(FORMAT_EXPECTED_MOODS)}},
                        "required": ["mood"],
                    },
                },
            },
            return_response_json=True,
        )
        message = rj.get("choices", [{}])[0].get("message", {})
        mood = _normalize_mood((message.get("parsed") or {}).get("mood"))
        if not mood:
            rc = message.get("content")
            if isinstance(rc, dict):
                mood = _normalize_mood(rc.get("mood"))
        if not mood:
            text = _normalize_message_text(message)
            if text:
                try:
                    mood = _normalize_mood((json.loads(text) or {}).get("mood"))
                except json.JSONDecodeError:
                    mood = ""
        if mood != expected_mood:
            return False
    return True


def _build_target(endpoint: Endpoint, target_path: str) -> str:
    """Combine endpoint base URL with API path."""
    return get_llm_url_stub(endpoint) + target_path


def _increment_count(url: str) -> None:
    """Thread-safe increment of active-request counter."""
    with _counters_lock:
        active = _active_counts.get(url, 0)
        _active_counts[url] = active + 1


def _decrement_count(url: str) -> None:
    """Thread-safe decrement of active-request counter."""
    with _counters_lock:
        curr = _active_counts.get(url, 0)
        if curr > 0:
            _active_counts[url] = curr - 1


def _bump_total_count(url: str) -> None:
    """Increment cumulative successful-response counter."""
    with _counters_lock:
        total = _total_counts.get(url, 0)
        _total_counts[url] = total + 1


def _rewrite_model(data: bytes, model_name: str) -> bytes:
    """Parse JSON body and overwrite the 'model' field."""
    body = json.loads(data)
    body["model"] = model_name
    return json.dumps(body).encode("utf-8")


def _mark_error(url: str, msg: str) -> None:
    """Mark endpoint as failed; subsequent routing will skip it."""
    with _counters_lock:
        _error_states[url] = {"error": True, "ts": time.time(), "msg": msg[:200]}


def _clear_error(url: str) -> None:
    """Clear the error flag after success (auto-recovery)."""
    with _counters_lock:
        if url in _error_states and _error_states[url].get("error"):
            _error_states[url] = {"error": False, "ts": time.time(), "msg": ""}


def _pick_next_available() -> Optional[Endpoint]:
    """Return endpoint with fewest active requests; skip error-flagged ones."""
    if not _endpoints:
        return None
    with _counters_lock:
        candidates = [ep for ep in _endpoints
                      if not _error_states.get(ep.url, {}).get("error", False)]
    if not candidates:
        return None                # every endpoint unhealthy
    return min(candidates, key=lambda ep: _active_counts.get(ep.url, 0))


def _forward(endpoint: Endpoint, method: str, url_path: str,
             headers: dict, data: bytes, timeout: int = 1200) -> Response:
    """Send a single request and return Flask Response."""
    target = _build_target(endpoint, url_path)

    # Build upstream headers (preserve everything except host; inject auth if needed)
    upstream_headers = {k: v for k, v in headers.items()
                       if k.lower() not in ("host", "transfer-encoding")}
    if endpoint.key:
        upstream_headers["Authorization"] = "Bearer " + endpoint.key

    # Overwrite model name for chat/completions requests
    if url_path == "/v1/chat/completions" and endpoint.model_name:
        data = _rewrite_model(data, endpoint.model_name)

    # Determine whether caller wants streamed SSE response
    is_stream = "text/event-stream" in headers.get("Accept", "")

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        resp = requests.request(
            method,
            target,
            headers=upstream_headers,
            data=data,
            verify=False,
            timeout=(60, timeout),        # (connect, read)
            stream=is_stream,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        _decrement_count(endpoint.url)              # failed -> release counter
        _mark_error(endpoint.url, str(exc)[:200])   # mark endpoint unhealthy
        raise

    if not is_stream:
        _bump_total_count(endpoint.url)          # count successful completion
        _clear_error(endpoint.url)                # auto-recover on success
        _decrement_count(endpoint.url)            # release counter
        return Response(resp.content, status=resp.status_code,
                        headers=dict(resp.headers))

    # ---- streaming response (SSE) ----
    # Counter stays +1 while chunks stream; decrement once stream ends/aborts.
    def stream_generator() -> Iterator[bytes]:
        try:
            for chunk in resp.iter_content(chunk_size=None):
                yield chunk
        finally:
            _bump_total_count(endpoint.url)       # count successful completion
            _clear_error(endpoint.url)             # auto-recover on success
            _decrement_count(endpoint.url)         # release after last chunk / abort

    return Response(stream_generator(), status=resp.status_code,
                    content_type="text/event-stream",
                    headers={"Cache-Control": "no-cache"})


def _try_endpoints(method: str, url_path: str, headers: dict, data: bytes):
    """Try endpoints by fewest-active-request order until one succeeds."""
    used = set()                      # avoid re-trying the same endpoint
    errors = []

    while True:
        ep = _pick_next_available()
        if ep is None or ep.url in used:
            break                     # nothing left to try
        used.add(ep.url)

        try:
            _increment_count(ep.url)
            return _forward(ep, method, url_path, headers, data)
        except Exception as exc:
            _decrement_count(ep.url)              # error flag set in _forward
            errors.append(str(ep.url) + ": " + str(exc))

    # Every endpoint failed (or all are in error state)
    result = jsonify({"error": "\n".join(errors)})
    return result, 502


app = Flask(__name__)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/v1/chat/completions", methods=["GET", "POST"])
def chat_completions():
    """Transparent proxy for /v1/chat/completions."""
    return _try_endpoints(
        request.method,
        "/v1/chat/completions",
        dict(request.headers),
        request.get_data(),
    )


@app.route("/v1/models", methods=["GET"])
def list_models():
    """Return combined model list from endpoints.json."""
    seen = set()
    model_list = []
    for ep in _endpoints:
        mn = ep.model_name
        if mn not in seen:
            seen.add(mn)
            model_list.append({
                "id": mn,
                "object": "model",
                "owned_by": "proxy",
                "store_name": ep.store_name,
            })
    return jsonify({"object": "list", "data": model_list})


@app.route("/api/endpoints", methods=["GET"])
def api_endpoints():
    """JSON view of every endpoint with load and error state."""
    with _counters_lock:
        active_snapshot = dict(_active_counts)
        total_snapshot  = dict(_total_counts)
        error_snap      = {k: dict(v) for k, v in _error_states.items()}

    data = []
    for ep in _endpoints:
        esnap = error_snap.get(ep.url, {"error": False, "ts": 0.0, "msg": ""})
        data.append({
            "store_name":      ep.store_name,
            "model_name":       ep.model_name,
            "url":              ep.url,
            "active_requests":  active_snapshot.get(ep.url, 0),
            "total_requests":   total_snapshot.get(ep.url, 0),
                  "capabilities":       _capabilities.get(ep.url, {}),
               "key_set":          bool(ep.key),
            "error":            esnap["error"],
            "error_ts":         esnap["ts"],
            "error_msg":        esnap["msg"],
        })
    return jsonify(data)


@app.route("/")
def dashboard():
    """Serve the monitoring dashboard."""
    return send_file("static/index.html", mimetype="text/html")


# ---------------------------------------------------------------------------
# Startup & CLI
# ---------------------------------------------------------------------------

def load_endpoints(path: str) -> List[Endpoint]:
    """Load Endpoint list from a JSON file."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    endpoints = []
    for entry in (data if isinstance(data, list) else [data]):
        ep = Endpoint(
            store_name=entry.get("store_name", ""),
            model_name=entry.get("model_name", ""),
            key=entry.get("key", ""),
            url=entry.get("url", ""),
            _context_size=entry.get("_context_size"),
            _publication_date=entry.get("_publication_date"),
            _quantization_level=entry.get("_quantization_level"),
        )
        endpoints.append(ep)

    if not endpoints:
        raise ValueError("No endpoints found in " + path)

    print("[proxy] Loaded " + str(len(endpoints)) + " endpoint(s) from " + path)
    return endpoints

def _load_raw_entries(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data if isinstance(data, list) else [data]


def _save_entries(path, entries):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, indent=1)


def run_ability_tests(config_path):
    entries = _load_raw_entries(config_path)
    needs_save = False

    for entry in entries:
        if all(f in entry for f in REQUIRED_CAPABILITY_FIELDS):
            print(f"Skipping {entry['store_name']}: all capability fields present.")
            continue

        ep = Endpoint(
            store_name=entry.get("store_name", ""),
            model_name=entry.get("model_name", ""),
            key=entry.get("key", ""),
            url=entry.get("url", ""),
        )

        cap_tests = [
             ("has_vision",   lambda _e=ep: test_vision(_e)),
             ("has_tooling",  lambda _e=ep: test_tooling(_e)),
             ("has_thinking", lambda _e=ep: test_thinking(_e)),
             ("has_format",   lambda _e=ep: test_format(_e)),
        ]

        for cap_name, test_fn in cap_tests:
            if cap_name in entry:
                print(f"  {cap_name} cached: {entry[cap_name]}")
                continue
            try:
                result = bool(test_fn())
            except Exception as exc:
                _mark_error(ep.url, "ability-test (" + cap_name + "): " + str(exc))
                entry[cap_name] = False
                needs_save = True
                print(f"  {cap_name} for {ep.store_name} = false (unhealthy)")
                continue

            entry[cap_name] = result
            needs_save = True
            print(f"  {cap_name} for {ep.store_name} = {result}")

        effective_thinking = bool(entry.get("has_thinking", False))
        if entry.get("thinking") != effective_thinking:
            entry["thinking"] = effective_thinking
            needs_save = True

    if needs_save:
        _save_entries(config_path, entries)
        print(f"Wrote capability data to {config_path}")


def main():
    """OpenAI-API reverse proxy / load balancer."""
    parser = argparse.ArgumentParser(description="OpenAI-API reverse proxy / load balancer")
    parser.add_argument("--port", type=int, default=8000,
                        help="Port to listen on (default: 8000)")
    parser.add_argument("--config", default="endpoints.json",
                        help="Path to endpoints config file (default: endpoints.json)")
    parser.add_argument("--test-abilities", action="store_true",
                        help="Run ability tests for missing capability data")
    args = parser.parse_args()

    if args.test_abilities:
        run_ability_tests(args.config)
        return

    global _endpoints
    _endpoints = load_endpoints(args.config)

    for ep in _endpoints:
        print("   - " + ep.store_name + " (" + ep.model_name + ") -> " + get_llm_url_stub(ep))

    app.run(host="0.0.0.0", port=args.port, threaded=True)


if __name__ == "__main__":
    main()
