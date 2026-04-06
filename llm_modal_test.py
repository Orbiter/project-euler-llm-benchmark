import base64
import json
import os

from llm_client import Endpoint, openai_api_chat


TOOLING_EXPECTED_FUNCTION_NAME = "lightswitch"
FORMAT_EXPECTED_MOODS = {"surprised", "angry", "happy"}


def _normalize_message_text(message: dict) -> str:
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


def _normalize_mood(value) -> str:
    mood = value.strip().lower() if isinstance(value, str) else ""
    return mood if mood in FORMAT_EXPECTED_MOODS else ""


def test_vision(endpoint: Endpoint) -> bool:
    return test_vision_with_flags(endpoint)


def test_vision_with_flags(endpoint: Endpoint, think: bool = False, no_think: bool = False) -> bool:
    image_path = "llmtest/testimage.png"
    if not os.path.exists(image_path):
        raise Exception(f"Test image not found: {image_path}")

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    try:
        print(f"Testing multimodal capabilities of model {endpoint.store_name}...")
        answer, total_tokens, token_per_second, usage_summary, duration_seconds = openai_api_chat(
            endpoint,
            prompt="what is in the image",
            base64_image=base64_image,
            think=think,
            no_think=no_think,
        )
        result = "42" in answer
        if result:
            print(f"Model {endpoint.store_name} is multimodal.")
        else:
            print(
                f"Model {endpoint.store_name} is not multimodal; it returned the following answer: {answer}"
            )
        return result
    except Exception as e:
        print(f"Model {endpoint.store_name} is not multimodal; it created an error: {e}")
        return False


def test_tooling(endpoint: Endpoint, think: bool = False, no_think: bool = False) -> bool:
    print(f"Testing tool-calling capability for model {endpoint.store_name}...")
    try:
        answer, total_tokens, token_per_second, usage_summary, duration_seconds, response_json = openai_api_chat(
            endpoint,
            prompt="Switch on the light",
            system_message="You are a home assistant.",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": TOOLING_EXPECTED_FUNCTION_NAME,
                        "description": "Switch the light on or off.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "state": {"type": "string", "enum": ["on", "off"]},
                            },
                            "required": ["state"],
                            "additionalProperties": False,
                        },
                    },
                }
            ],
            stream=False,
            temperature=0.0,
            think=think,
            no_think=no_think,
            return_response_json=True,
        )
        message = response_json.get("choices", [{}])[0].get("message", {})
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            print(f"Tool-calling test returned no tool calls for {endpoint.store_name}.")
            return False
        function = tool_calls[0].get("function", {})
        tool_name = function.get("name") or tool_calls[0].get("name") or ""
        print(f"Tool-calling test requested tool: {tool_name}")
        return tool_name == TOOLING_EXPECTED_FUNCTION_NAME
    except Exception as e:
        print(f"Tool-calling test failed for {endpoint.store_name}: {e}")
        return False


def test_thinking(endpoint: Endpoint, think: bool = False, no_think: bool = False) -> bool:
    print(f"Testing thinking capability for model {endpoint.store_name}...")
    try:
        answer, total_tokens, token_per_second, usage_summary, duration_seconds, response_json = openai_api_chat(
            endpoint,
            prompt="Think step by step and answer: what is 17 plus 25?",
            system_message="You are a helpful assistant.",
            temperature=0.1,
            max_tokens=512,
            stream=False,
            think=think,
            no_think=no_think,
            return_response_json=True,
        )
        for choice in response_json.get("choices", []):
            message = choice.get("message", {})
            text = _normalize_message_text(message)
            if "<think>" in text or "</think>" in text:
                return True
            reasoning = choice.get("reasoning")
            if isinstance(reasoning, str) and reasoning.strip():
                return True
            if isinstance(message.get("reasoning"), str) and message.get("reasoning").strip():
                return True
        return False
    except Exception as e:
        print(f"Thinking test failed for {endpoint.store_name}: {e}")
        return False


def test_format(endpoint: Endpoint, think: bool = False, no_think: bool = False) -> bool:
    print(f"Testing structured-format capability for model {endpoint.store_name}...")
    test_cases = [
        ("I hate programming", "angry"),
        ("I love programming", "happy"),
        ("Wait, that worked perfectly?", "surprised"),
    ]
    for input_text, expected_mood in test_cases:
        try:
            answer, total_tokens, token_per_second, usage_summary, duration_seconds, response_json = openai_api_chat(
                endpoint,
                prompt=input_text,
                system_message="You are a mood classifier. Identify the mood of the request.",
                temperature=0.1,
                max_tokens=128,
                stream=False,
                think=think,
                no_think=no_think,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "strict": True,
                        "schema": {
                            "title": "Classifier",
                            "type": "object",
                            "properties": {
                                "mood": {"type": "string", "enum": sorted(FORMAT_EXPECTED_MOODS)}
                            },
                            "required": ["mood"],
                        },
                    },
                },
                return_response_json=True,
            )
            message = response_json.get("choices", [{}])[0].get("message", {})
            mood = _normalize_mood((message.get("parsed") or {}).get("mood"))
            if not mood:
                content = message.get("content")
                if isinstance(content, dict):
                    mood = _normalize_mood(content.get("mood"))
            if not mood:
                text = _normalize_message_text(message)
                if text:
                    try:
                        mood = _normalize_mood((json.loads(text) or {}).get("mood"))
                    except json.JSONDecodeError:
                        mood = ""
            if mood != expected_mood:
                return False
        except Exception as e:
            print(f"Structured-format test failed for {endpoint.store_name}: {e}")
            return False
    return True


def ensure_model_capabilities(
    entry: dict,
    endpoint: Endpoint,
    think: bool = False,
    no_think: bool = False,
) -> tuple[dict, bool]:
    updated_entry = dict(entry)
    changed = False
    capability_tests = [
        ("has_vision", lambda: test_vision_with_flags(endpoint, think=think, no_think=no_think)),
        ("has_tooling", lambda: test_tooling(endpoint, think=think, no_think=no_think)),
        ("has_thinking", lambda: test_thinking(endpoint, think=True, no_think=False)),
        ("has_format", lambda: test_format(endpoint, think=think, no_think=no_think)),
    ]

    for capability_name, capability_test in capability_tests:
        if capability_name in updated_entry:
            print(f"{capability_name.capitalize()} capability cached for {endpoint.store_name}: {updated_entry[capability_name]}")
            continue

        print(f"Testing {capability_name} capability for {endpoint.store_name}...")
        updated_entry[capability_name] = bool(capability_test())
        changed = True
        print(f"{capability_name.capitalize()} capability for {endpoint.store_name}: {updated_entry[capability_name]}")

    effective_thinking = bool(updated_entry.get("has_thinking", False) and not no_think)
    if updated_entry.get("thinking") != effective_thinking:
        updated_entry["thinking"] = effective_thinking
        changed = True

    return updated_entry, changed
