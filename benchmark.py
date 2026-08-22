import os
import time
import json
import logging
import math
import statistics
from datetime import datetime, timezone
from typing import Dict

from language_config import BENCHMARK_LANGUAGES, LANGUAGE_WEIGHTS, REFERENCE_LANGUAGE

# Constants
BENCHMARK_FILE = 'benchmark.json'
BENCHMARK_FILE_STOP = 'benchmark.json.stop' # yes thats ugly
STOP_FILE_TIMEOUT = 60  # seconds
_BATCH_SIZES = [100, 200]
MIN_LANGUAGE_COEFFICIENT_SAMPLES = 1
_LANGUAGE_COEFFICIENTS_CACHE: Dict[tuple[int, bool], Dict[str, float]] = {}
_LANGUAGE_OBSERVED_COEFFICIENTS_CACHE: Dict[tuple[int, bool], Dict[str, float]] = {}
_LANGUAGE_COEFFICIENT_COUNTS_CACHE: Dict[tuple[int, bool], Dict[str, int]] = {}

# Configure logging
logging.basicConfig(level=logging.INFO)

def wait_for_stop_file():
    """Wait for the stop file to be removed or timeout."""
    while os.path.exists(BENCHMARK_FILE_STOP):
        stop_file_age = time.time() - os.path.getmtime(BENCHMARK_FILE_STOP)
        if stop_file_age > STOP_FILE_TIMEOUT:
            os.remove(BENCHMARK_FILE_STOP)
            logging.warning(f"Removed old {BENCHMARK_FILE_STOP} file.")
            break
        logging.info(f"Waiting for {BENCHMARK_FILE_STOP} to disappear...")
        time.sleep(1)

def read_benchmark() -> dict:
    """Read the benchmark data from the JSON file."""
    _LANGUAGE_COEFFICIENTS_CACHE.clear()
    _LANGUAGE_OBSERVED_COEFFICIENTS_CACHE.clear()
    _LANGUAGE_COEFFICIENT_COUNTS_CACHE.clear()
    wait_for_stop_file()
    try:
        with open(BENCHMARK_FILE, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        logging.error(f"{BENCHMARK_FILE} not found.")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON in {BENCHMARK_FILE}.")
        return {}

def current_timestamp_utc() -> str:
    """Return the current time in the benchmark's ISO 8601 UTC format."""
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )

def write_benchmark(benchmark: dict):
    """Write the benchmark data to the JSON file."""
    _LANGUAGE_COEFFICIENTS_CACHE.clear()
    _LANGUAGE_OBSERVED_COEFFICIENTS_CACHE.clear()
    _LANGUAGE_COEFFICIENT_COUNTS_CACHE.clear()
    try:
        with open(BENCHMARK_FILE_STOP, 'w', encoding='utf-8') as stop_file:
            stop_file.write("stop")
        with open(BENCHMARK_FILE, 'w', encoding='utf-8') as json_file:
            json.dump(benchmark, json_file, indent=4)
    except Exception as e:
        logging.error(f"Error writing to {BENCHMARK_FILE}: {e}")
    finally:
        if os.path.exists(BENCHMARK_FILE_STOP):
            os.remove(BENCHMARK_FILE_STOP)


def score_key(language: str, batch_size: int, tool_mode: bool = False) -> str:
    suffix = "-tool" if tool_mode else ""
    return f"{language}-{batch_size}{suffix}"
    
@staticmethod
def _safe_float(value: object) -> float | None:
    try:
        if value in (None, ""): return None
        return float(value)
    except (TypeError, ValueError):
        return None

def _language_coefficients(
    benchmark: dict, batch_size: int, tool_mode: bool = False
) -> Dict[str, float]:
    """Compute coefficients from the median language-to-Python score ratio.

        This is required for models where JavaScript or another non-Python language has
        not been tested. The batch-specific median resists individual outliers.
    """
    cache_key = (batch_size, tool_mode)
    cached_coefficients = _LANGUAGE_COEFFICIENTS_CACHE.get(cache_key)
    if cached_coefficients is not None:
        return cached_coefficients
    ratios: Dict[str, list[float]] = {
        lang: [] for lang in BENCHMARK_LANGUAGES if lang != REFERENCE_LANGUAGE
    }
    python_key = score_key(REFERENCE_LANGUAGE, batch_size, tool_mode)

    for model_test in benchmark.values():
        python_score = _safe_float(model_test.get(python_key))
        if python_score is None or not math.isfinite(python_score) or python_score <= 0:
            continue

        for language in BENCHMARK_LANGUAGES:
            if language == REFERENCE_LANGUAGE: continue
            language_key = score_key(language, batch_size, tool_mode)
            language_score = _safe_float(model_test.get(language_key))
            if (
                language_score is None
                or not math.isfinite(language_score)
                or language_score < 0
            ):
                continue
            ratios[language].append(language_score / python_score)

    observed_coefficients = {
        language: statistics.median(values)
        for language, values in ratios.items()
        if values
    }
    counts = {language: len(values) for language, values in ratios.items()}
    this_coefficients = {
        language: coefficient
        for language, coefficient in observed_coefficients.items()
        if counts[language] >= MIN_LANGUAGE_COEFFICIENT_SAMPLES
    } # the python coefficient is always 1.0
    _LANGUAGE_COEFFICIENTS_CACHE[cache_key] = this_coefficients
    _LANGUAGE_OBSERVED_COEFFICIENTS_CACHE[cache_key] = observed_coefficients
    _LANGUAGE_COEFFICIENT_COUNTS_CACHE[cache_key] = counts
    insufficient = [
        f"{language} ({count}/{MIN_LANGUAGE_COEFFICIENT_SAMPLES})"
        for language, count in counts.items()
        if count < MIN_LANGUAGE_COEFFICIENT_SAMPLES
    ]
    if insufficient:
        logging.warning(
            "Insufficient Python calibration pairs for batch %s%s: %s. Missing "
            "scores for these languages will be excluded until calibration is ready.",
            batch_size,
            " tool mode" if tool_mode else "",
            ", ".join(insufficient),
        )
    return this_coefficients

def language_coefficient_summary(
    benchmark: dict, batch_size: int, tool_mode: bool = False
) -> dict:
    """Return each non-Python coefficient and its calibration sample count."""
    coefficients = _language_coefficients(benchmark, batch_size, tool_mode)
    cache_key = (batch_size, tool_mode)
    observed = _LANGUAGE_OBSERVED_COEFFICIENTS_CACHE[cache_key]
    counts = _LANGUAGE_COEFFICIENT_COUNTS_CACHE[cache_key]
    return {
        language: {
            "coefficient": coefficients.get(language),
            "observed_coefficient": observed.get(language),
            "samples": counts[language],
            "required_samples": MIN_LANGUAGE_COEFFICIENT_SAMPLES,
            "ready": language in coefficients,
        }
        for language in counts
    }

def _bench_score(
    model_test: dict,
    batch_size: int,
    coefficients: Dict[str, float],
    tool_mode: bool = False,
) -> float:
    """ Compute the bench score for a given model test result and a batch size.
        Missing non-Python values are estimated from their language coefficient and the
        model's Python score. The estimates are used only for scoring and are not stored.
    """
    python_score = _safe_float(
        model_test.get(score_key(REFERENCE_LANGUAGE, batch_size, tool_mode))
    )
    if python_score is None: return 0.0
    combined_score = 0.0
    combined_weight = 0.0
    for language, weight in LANGUAGE_WEIGHTS.items():
        if language == REFERENCE_LANGUAGE:
            score = python_score
        else:
            language_key = score_key(language, batch_size, tool_mode)
            language_score = _safe_float(model_test.get(language_key))
            if language_score is None:
                if language not in coefficients:
                    continue
                score = coefficients[language] * python_score
            else:
                score = language_score
        combined_score += weight * score
        combined_weight += weight

    return combined_score / combined_weight
    
def bench_score(
    benchmark: dict, model_test: dict, batch_size: int, tool_mode: bool = False
) -> float:
    """ this computes the bench score for a given model test result and a batch size."""
    coefficients = _language_coefficients(benchmark, batch_size, tool_mode)
    return _bench_score(model_test, batch_size, coefficients, tool_mode)

def bench_score_average(benchmark: dict, model_test: dict) -> int:
    """ Average the bench score over all batch sizes. While the score over the different batch sizes
        are not comparable, we still observed that some models performed better with older batch sizes
        and other with newer batch sizes. So we simply average the scores over all batch sizes to get
        a combined score.
    """
    score = 0.0
    d = 0.0
    for batch_size in _BATCH_SIZES:
        s = bench_score(benchmark, model_test, batch_size)
        if (s > 0.0):
            score += s
            d += 1.0
    return score / d if d > 0.0 else 0.0

def sort_benchmark(benchmark: dict, batch_size:int = None) -> dict:
    """ sort the benchmark with the highest points first, we can either select a specific batch size
        or without a given batch size we average over all batch sizes.
    """
    if batch_size is None or batch_size not in _BATCH_SIZES:
        sorted_benchmark = dict(sorted(benchmark.items(), key=lambda item: bench_score_average(benchmark, item[1]), reverse=True))
    else:
        sorted_benchmark = dict(sorted(benchmark.items(), key=lambda item: bench_score(benchmark, item[1], batch_size), reverse=True))
    return sorted_benchmark
