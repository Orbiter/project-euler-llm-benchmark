#!/usr/bin/env python3

import json
import sys
from pathlib import Path

from language_config import LANGUAGE_WEIGHTS, TOTAL_LANGUAGE_WEIGHT


def weighted_score(metrics: dict, suffix: str) -> float | None:
    total = 0.0
    for lang, weight in LANGUAGE_WEIGHTS.items():
        key = f"{lang}-{suffix}"
        value = metrics.get(key)
        if value is None:
            return None
        total += value * weight
    return total / TOTAL_LANGUAGE_WEIGHT


def main() -> int:
    benchmark_path = Path(__file__).with_name("benchmark.json")

    try:
        raw = benchmark_path.read_text()
    except OSError as exc:
        print(f"Failed to read {benchmark_path}: {exc}", file=sys.stderr)
        return 1

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"Failed to parse JSON from {benchmark_path}: {exc}", file=sys.stderr)
        return 1

    ratios = 0.0
    rcount = 0

    for name, metrics in data.items():
        bench_100 = weighted_score(metrics, "100")
        bench_200 = weighted_score(metrics, "200")
        if bench_100 is None or bench_200 is None: continue
        if bench_100 < 4 or bench_200 < 4 : continue # skip small numbers, the quotients are too noisy
        print(f"{name}: 100={bench_100:.2f}, 200={bench_200:.2f}, ratio={bench_200/bench_100:.6f}")
        ratios += (bench_200 / bench_100)
        rcount += 1

    if not ratios:
        javascript_pairs = sum(
            "javascript-100" in metrics and "javascript-200" in metrics
            for metrics in data.values()
        )
        print("No LLM has complete five-language 100 and 200 benchmark data.")
        if javascript_pairs == 0:
            print("JavaScript 100/200 calibration data is not available yet.")
        return 0

    comparison_factor = ratios / rcount
    print(f"Comparison factor: {comparison_factor:.6f}; that means: bench_200 = bench_100 * {comparison_factor:.6f}")
    print(f"Models included: {rcount}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
