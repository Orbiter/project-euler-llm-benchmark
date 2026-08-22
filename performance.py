#!/usr/bin/env python3
"""Measure native Ollama prompt/decode throughput on an M1 Mac Studio.

The values reported here use Ollama's own token counts and nanosecond timing
fields.  They therefore match the rates printed by ``ollama run --verbose``
instead of estimating throughput from wall-clock request time.
"""

import argparse
import json
import platform
import random
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_BENCHMARK_PATH = SCRIPT_DIR / "benchmark.json"
M1_MAC_STUDIO_MODEL_IDS = frozenset({"Mac13,1", "Mac13,2"})
MIN_PROMPT_TOKENS = 4_000
REQUEST_TIMEOUT_SECONDS = 1_200
UNLOAD_TIMEOUT_SECONDS = 30
UNLOAD_POLL_INTERVAL_SECONDS = 0.25

_ADJECTIVES = (
    "amber", "balanced", "coastal", "distributed", "efficient", "granular",
    "harmonic", "iterative", "measured", "northern", "predictable",
    "resilient", "seasonal", "stable", "technical", "urban",
)
_TEAMS = (
    "analysis", "engineering", "logistics", "operations", "planning",
    "quality", "research", "safety", "support", "validation",
)
_VERBS = (
    "assembled", "catalogued", "compared", "inspected", "measured",
    "processed", "reviewed", "sampled", "tested", "verified",
)
_OBJECTS = (
    "archives", "batteries", "datasets", "instruments", "modules",
    "networks", "prototypes", "reports", "sensors", "workflows",
)
_LOCATIONS = (
    "coastal observatory", "eastern laboratory", "harbor facility",
    "mountain station", "northern workshop", "regional data center",
    "river terminal", "southern warehouse", "urban research campus",
)
_CONDITIONS = (
    "careful calibration", "moderate latency", "predictable demand",
    "reduced variance", "stable temperature", "strict quality controls",
    "sustained throughput", "well documented procedures",
)


class PerformanceBenchmarkError(RuntimeError):
    """Raised when the benchmark cannot produce a valid measurement."""


def _sysctl_value(name: str) -> str:
    try:
        result = subprocess.run(
            ["sysctl", "-n", name],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise PerformanceBenchmarkError(f"Could not read {name} via sysctl.") from exc
    return result.stdout.strip()


def require_m1_mac_studio() -> tuple[str, str]:
    """Fail unless this process is running on an Apple M1 Mac Studio."""
    system = platform.system()
    architecture = platform.machine()
    if system != "Darwin" or architecture != "arm64":
        raise PerformanceBenchmarkError(
            "This benchmark may only run on an Apple Silicon Mac Studio M1 "
            f"(detected {system}/{architecture})."
        )

    model_id = _sysctl_value("hw.model")
    cpu_brand = _sysctl_value("machdep.cpu.brand_string")
    if model_id not in M1_MAC_STUDIO_MODEL_IDS or not cpu_brand.startswith("Apple M1"):
        raise PerformanceBenchmarkError(
            "This benchmark may only run on a Mac Studio with an Apple M1 chip "
            f"(detected model={model_id!r}, cpu={cpu_brand!r})."
        )
    return model_id, cpu_brand


def validate_local_api_base(api_base: str) -> str:
    """Return a normalized base URL and reject non-local Ollama servers."""
    parsed = urlparse(api_base)
    if parsed.scheme not in {"http", "https"}:
        raise PerformanceBenchmarkError("--api-base must use http or https.")
    if parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise PerformanceBenchmarkError(
            "--api-base must point to localhost so the measured server is the "
            "verified M1 Mac Studio."
        )
    if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
        raise PerformanceBenchmarkError(
            "--api-base must be a server base URL without a path, query, or fragment."
        )
    return api_base.rstrip("/")


def list_ollama_models(api_base: str) -> list[str]:
    """Return the unique model names reported by the local Ollama server."""
    url = f"{api_base}/api/tags"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        detail = ""
        if exc.response is not None:
            detail = f" Response: {exc.response.text[:500]}"
        raise PerformanceBenchmarkError(
            f"Could not list Ollama models at {url}.{detail}"
        ) from exc
    except ValueError as exc:
        raise PerformanceBenchmarkError(
            "Ollama returned invalid JSON while listing models."
        ) from exc

    raw_models = data.get("models") if isinstance(data, dict) else None
    if not isinstance(raw_models, list):
        raise PerformanceBenchmarkError(
            "Ollama's /api/tags response contains no model list."
        )

    models = {
        name
        for item in raw_models
        if isinstance(item, dict)
        for name in (item.get("name") or item.get("model"),)
        if isinstance(name, str) and name.strip()
    }
    return sorted(models, key=str.casefold)


def list_running_ollama_models(api_base: str) -> list[str]:
    """Return the model names currently loaded according to Ollama /api/ps."""
    url = f"{api_base}/api/ps"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        detail = ""
        if exc.response is not None:
            detail = f" Response: {exc.response.text[:500]}"
        raise PerformanceBenchmarkError(
            f"Could not list running Ollama models at {url}.{detail}"
        ) from exc
    except ValueError as exc:
        raise PerformanceBenchmarkError(
            "Ollama returned invalid JSON while listing running models."
        ) from exc

    raw_models = data.get("models") if isinstance(data, dict) else None
    if not isinstance(raw_models, list):
        raise PerformanceBenchmarkError(
            "Ollama's /api/ps response contains no model list."
        )

    models = {
        name
        for item in raw_models
        if isinstance(item, dict)
        for name in (item.get("name") or item.get("model"),)
        if isinstance(name, str) and name.strip()
    }
    return sorted(models, key=str.casefold)


def unload_all_ollama_models(api_base: str) -> None:
    """Unload every active Ollama model and verify that RAM is clear."""
    installed_models = list_ollama_models(api_base)
    running_models = list_running_ollama_models(api_base)
    print(
        f"Pre-run cleanup: {len(installed_models)} installed, "
        f"{len(running_models)} active Ollama model(s).",
        flush=True,
    )

    for model in running_models:
        print(f"Unloading active model {model}...", flush=True)
        url = f"{api_base}/api/generate"
        try:
            response = requests.post(
                url,
                json={"model": model, "keep_alive": 0, "stream": False},
                timeout=120,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            detail = ""
            if exc.response is not None:
                detail = f" Response: {exc.response.text[:500]}"
            raise PerformanceBenchmarkError(
                f"Could not unload Ollama model {model!r}.{detail}"
            ) from exc

    deadline = time.monotonic() + UNLOAD_TIMEOUT_SECONDS
    while True:
        remaining_models = list_running_ollama_models(api_base)
        if not remaining_models:
            break
        if time.monotonic() >= deadline:
            raise PerformanceBenchmarkError(
                "Ollama still reports active models after unload: "
                + ", ".join(remaining_models)
            )
        time.sleep(UNLOAD_POLL_INTERVAL_SECONDS)
    print("Pre-run cleanup complete: no Ollama model is active.", flush=True)


def build_long_prompt(run_number: int, record_count: int) -> str:
    """Build a long, deterministic prompt with a run-specific first token.

    Every measured run uses different content from the beginning. This avoids
    measuring a large prefix restored from Ollama's prompt cache.
    """
    rng = random.Random(91_337 + run_number)
    nonce = f"run-{run_number:04d}-{rng.getrandbits(64):016x}"
    lines = [
        nonce,
        "Read the complete synthetic operations log below. Retain its details ",
        "while reading; do not answer until the END OF LOG marker.",
        "",
    ]

    for record_number in range(1, record_count + 1):
        amount = rng.randint(120, 9_800)
        days = rng.randint(3, 180)
        lines.append(
            f"Record {record_number:04d}: During the {rng.choice(_ADJECTIVES)} "
            f"cycle, the {rng.choice(_TEAMS)} team {rng.choice(_VERBS)} "
            f"{amount} {rng.choice(_ADJECTIVES)} {rng.choice(_OBJECTS)} at the "
            f"{rng.choice(_LOCATIONS)}. The activity was associated with "
            f"{rng.choice(_CONDITIONS)} and scheduled for another review after "
            f"{days} days."
        )

    lines.extend((
        "",
        "END OF LOG",
        "Write a detailed report of at least 800 words. Discuss recurring operational "
        "patterns, possible bottlenecks, data-quality risks, capacity planning, and "
        "concrete recommendations. Use continuous prose and do not quote the log.",
    ))
    return "\n".join(lines)


def _post_chat(
    session: requests.Session,
    api_base: str,
    model: str,
    prompt: str,
    *,
    num_ctx: int,
    num_predict: int,
    seed: int,
) -> dict[str, Any]:
    url = f"{api_base}/api/chat"
    try:
        response = session.post(
            url,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "think": False,
                "keep_alive": "10m",
                "options": {
                    "temperature": 0,
                    "seed": seed,
                    "num_ctx": num_ctx,
                    "num_predict": num_predict,
                },
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        detail = ""
        if exc.response is not None:
            detail = f" Response: {exc.response.text[:500]}"
        raise PerformanceBenchmarkError(f"Ollama request to {url} failed.{detail}") from exc
    except ValueError as exc:
        raise PerformanceBenchmarkError("Ollama returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise PerformanceBenchmarkError("Ollama returned a non-object JSON response.")
    return data


def _rate(data: dict[str, Any], count_key: str, duration_key: str) -> float:
    count = data.get(count_key)
    duration = data.get(duration_key)
    if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
        raise PerformanceBenchmarkError(
            f"Ollama response has no positive integer {count_key!r}."
        )
    if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
        raise PerformanceBenchmarkError(
            f"Ollama response has no positive integer {duration_key!r}."
        )
    return count * 1_000_000_000 / duration


def measure_performance(
    api_base: str,
    model: str,
    *,
    runs: int,
    prompt_records: int,
    num_ctx: int,
    num_predict: int,
) -> tuple[int, int]:
    """Warm the model, measure several runs, and return rounded medians."""
    output_rates: list[float] = []
    prompt_rates: list[float] = []

    with requests.Session() as session:
        print(f"Warming up {model}...", flush=True)
        _post_chat(
            session,
            api_base,
            model,
            "Reply with the single word ready.",
            num_ctx=num_ctx,
            num_predict=8,
            seed=91_336,
        )

        for run_number in range(1, runs + 1):
            prompt = build_long_prompt(run_number, prompt_records)
            data = _post_chat(
                session,
                api_base,
                model,
                prompt,
                num_ctx=num_ctx,
                num_predict=num_predict,
                seed=91_337 + run_number,
            )

            prompt_count = data.get("prompt_eval_count")
            if not isinstance(prompt_count, int) or prompt_count < MIN_PROMPT_TOKENS:
                raise PerformanceBenchmarkError(
                    f"Run {run_number} evaluated only {prompt_count!r} prompt tokens; "
                    f"at least {MIN_PROMPT_TOKENS} are required. Increase "
                    "--prompt-records or --num-ctx."
                )

            output_rate = _rate(data, "eval_count", "eval_duration")
            prompt_rate = _rate(data, "prompt_eval_count", "prompt_eval_duration")
            output_rates.append(output_rate)
            prompt_rates.append(prompt_rate)
            print(
                f"Run {run_number}/{runs}: output={output_rate:.2f} tokens/s, "
                f"prompt={prompt_rate:.2f} tokens/s "
                f"({prompt_count} prompt tokens)",
                flush=True,
            )

    return round(statistics.median(output_rates)), round(statistics.median(prompt_rates))


def load_benchmark(benchmark_path: Path) -> dict[str, Any]:
    """Read and validate benchmark.json."""
    try:
        with benchmark_path.open("r", encoding="utf-8") as benchmark_file:
            benchmark = json.load(benchmark_file)
    except FileNotFoundError as exc:
        raise PerformanceBenchmarkError(f"Benchmark file not found: {benchmark_path}") from exc
    except json.JSONDecodeError as exc:
        raise PerformanceBenchmarkError(
            f"Benchmark file is not valid JSON: {benchmark_path}"
        ) from exc

    if not isinstance(benchmark, dict):
        raise PerformanceBenchmarkError("benchmark.json must contain a JSON object.")
    return benchmark


def has_performance_values(entry: Any) -> bool:
    """Return whether an entry already has both valid stored integer rates."""
    if not isinstance(entry, dict):
        return False
    values = (
        entry.get("_output_tokens_per_second"),
        entry.get("_prompt_tokens_per_second"),
    )
    return all(
        isinstance(value, int) and not isinstance(value, bool) and value > 0
        for value in values
    )


def benchmark_store_names(benchmark: dict[str, Any], model: str) -> list[str]:
    """Map one Ollama model to its existing think/no-think benchmark entries."""
    variant_names = [
        name
        for name in (f"{model}-think", f"{model}-no_think")
        if name in benchmark
    ]
    return variant_names or [model]


def update_benchmark_entries(
    benchmark_path: Path,
    store_names: list[str],
    output_tokens_per_second: int,
    prompt_tokens_per_second: int,
) -> None:
    """Update the two performance fields for one or more benchmark entries."""
    benchmark = load_benchmark(benchmark_path)
    for store_name in store_names:
        entry = benchmark.setdefault(store_name, {})
        if not isinstance(entry, dict):
            raise PerformanceBenchmarkError(
                f"Benchmark entry {store_name!r} must be a JSON object."
            )

        entry["_output_tokens_per_second"] = int(output_tokens_per_second)
        entry["_prompt_tokens_per_second"] = int(prompt_tokens_per_second)

    temporary_path = benchmark_path.with_name(f".{benchmark_path.name}.performance.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8") as benchmark_file:
            json.dump(benchmark, benchmark_file, indent=4)
            benchmark_file.write("\n")
        temporary_path.replace(benchmark_path)
    except OSError as exc:
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise PerformanceBenchmarkError(
            f"Could not update benchmark file: {benchmark_path}"
        ) from exc


def update_benchmark(
    benchmark_path: Path,
    store_name: str,
    output_tokens_per_second: int,
    prompt_tokens_per_second: int,
) -> None:
    """Update exactly the two performance fields for one benchmark entry."""
    update_benchmark_entries(
        benchmark_path,
        [store_name],
        output_tokens_per_second,
        prompt_tokens_per_second,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Measure native Ollama prompt/output throughput on an M1 Mac Studio "
            "and store the rounded median rates in benchmark.json."
        )
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--model", help="benchmark one Ollama model")
    selection.add_argument(
        "--all",
        action="store_true",
        help="benchmark all local Ollama models without stored performance values",
    )
    parser.add_argument(
        "--store-name",
        help="benchmark.json entry name (default: the Ollama model name)",
    )
    parser.add_argument(
        "--api-base",
        default="http://localhost:11434",
        help="local Ollama base URL (default: http://localhost:11434)",
    )
    parser.add_argument("--runs", type=int, default=5, help="measured runs (default: 5)")
    parser.add_argument(
        "--prompt-records",
        type=int,
        default=200,
        help="synthetic records in each long prompt (default: 200)",
    )
    parser.add_argument(
        "--num-ctx",
        type=int,
        default=16_384,
        help="Ollama context size used for the test (default: 16384)",
    )
    parser.add_argument(
        "--num-predict",
        type=int,
        default=512,
        help="maximum generated tokens per run (default: 512)",
    )
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=DEFAULT_BENCHMARK_PATH,
        help="benchmark JSON path (default: benchmark.json beside this script)",
    )
    return parser


def measure_and_store(
    *,
    api_base: str,
    model: str,
    store_names: list[str],
    benchmark_path: Path,
    runs: int,
    prompt_records: int,
    num_ctx: int,
    num_predict: int,
) -> tuple[int, int]:
    """Benchmark one model and immediately persist its two rates."""
    unload_all_ollama_models(api_base)
    output_rate, prompt_rate = measure_performance(
        api_base,
        model,
        runs=runs,
        prompt_records=prompt_records,
        num_ctx=num_ctx,
        num_predict=num_predict,
    )
    update_benchmark_entries(
        benchmark_path,
        store_names,
        output_rate,
        prompt_rate,
    )
    print(
        f"Stored {', '.join(store_names)}: "
        f"_output_tokens_per_second={output_rate}, "
        f"_prompt_tokens_per_second={prompt_rate}",
        flush=True,
    )
    return output_rate, prompt_rate


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        # This must remain before API validation, session creation, or warm-up.
        model_id, cpu_brand = require_m1_mac_studio()

        if args.runs < 1:
            raise PerformanceBenchmarkError("--runs must be at least 1.")
        if args.prompt_records < 1:
            raise PerformanceBenchmarkError("--prompt-records must be at least 1.")
        if args.num_ctx < MIN_PROMPT_TOKENS + args.num_predict:
            raise PerformanceBenchmarkError(
                f"--num-ctx must be at least {MIN_PROMPT_TOKENS + args.num_predict}."
            )
        if args.num_predict < 1:
            raise PerformanceBenchmarkError("--num-predict must be at least 1.")
        if args.all and args.store_name:
            raise PerformanceBenchmarkError("--store-name cannot be used with --all.")

        api_base = validate_local_api_base(args.api_base)
        benchmark_path = args.benchmark.resolve()
        print(f"Hardware verified: {model_id}, {cpu_brand}", flush=True)

        if args.all:
            models = list_ollama_models(api_base)
            benchmark = load_benchmark(benchmark_path)
            model_targets = {
                model: benchmark_store_names(benchmark, model)
                for model in models
            }
            pending_models = [
                model
                for model, store_names in model_targets.items()
                if not all(
                    has_performance_values(benchmark.get(store_name))
                    for store_name in store_names
                )
            ]
            pending_set = set(pending_models)

            print(f"Ollama models ({len(models)}):", flush=True)
            for model in models:
                target_text = ", ".join(model_targets[model])
                status = (
                    f"benchmark -> {target_text}"
                    if model in pending_set
                    else f"skip (already stored in {target_text})"
                )
                print(f"  {model}: {status}", flush=True)

            if not pending_models:
                print("All Ollama models already have performance values.", flush=True)
                return 0

            failures: list[tuple[str, str]] = []
            for position, model in enumerate(pending_models, start=1):
                print(
                    f"\nModel {position}/{len(pending_models)}: {model}",
                    flush=True,
                )
                try:
                    measure_and_store(
                        api_base=api_base,
                        model=model,
                        store_names=model_targets[model],
                        benchmark_path=benchmark_path,
                        runs=args.runs,
                        prompt_records=args.prompt_records,
                        num_ctx=args.num_ctx,
                        num_predict=args.num_predict,
                    )
                except PerformanceBenchmarkError as exc:
                    failures.append((model, str(exc)))
                    print(f"Skipping failed model {model}: {exc}", file=sys.stderr)

            if failures:
                print(
                    f"performance.py: {len(failures)} of {len(pending_models)} "
                    "model benchmarks failed:",
                    file=sys.stderr,
                )
                for model, message in failures:
                    print(f"  {model}: {message}", file=sys.stderr)
                return 1
            return 0

        if args.store_name:
            store_names = [args.store_name]
        else:
            benchmark = load_benchmark(benchmark_path)
            store_names = benchmark_store_names(benchmark, args.model)
        measure_and_store(
            api_base=api_base,
            model=args.model,
            store_names=store_names,
            benchmark_path=benchmark_path,
            runs=args.runs,
            prompt_records=args.prompt_records,
            num_ctx=args.num_ctx,
            num_predict=args.num_predict,
        )
    except PerformanceBenchmarkError as exc:
        print(f"performance.py: error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
