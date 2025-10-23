import os
import time
import json
import logging
from typing import Dict

# Constants
BENCHMARK_FILE = 'benchmark.json'
BENCHMARK_FILE_STOP = 'benchmark.json.stop' # yes thats ugly
STOP_FILE_TIMEOUT = 60  # seconds
_LANGUAGE_WEIGHTS: Dict[str, float] = {"python": 4.0, "java": 3.0, "rust": 2.0, "clojure": 1.0}
_LANGUAGES = list(_LANGUAGE_WEIGHTS.keys())
_TOTAL_WEIGHT = sum(_LANGUAGE_WEIGHTS.values())
_BATCH_SIZES = [100, 200]
_LANGUAGE_COEFFICIENTS_CACHE: Dict[int, Dict[str, float]] = {}

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

def write_benchmark(benchmark: dict):
    """Write the benchmark data to the JSON file."""
    _LANGUAGE_COEFFICIENTS_CACHE.clear()
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


def score_key(language: str, batch_size: int) -> str:
    return f"{language}-{batch_size}"
    
@staticmethod
def _safe_float(value: object) -> float | None:
    try:
        if value in (None, ""): return None
        return float(value)
    except (TypeError, ValueError):
        return None

def _language_coefficients(benchmark: dict, batch_size: int) -> Dict[str, float]:
    """ Compute the coefficients for each language based on the average ratio to python.
        This is required for all models where not all languages are tested. We then simply
        use the average ratio to python as the coefficient. This must be computed once for
        each batch size.
    """
    cached_coefficients = _LANGUAGE_COEFFICIENTS_CACHE.get(batch_size)
    if cached_coefficients is not None:
        return cached_coefficients
    totals: Dict[str, float] = {lang: 0.0 for lang in _LANGUAGES if lang != "python"}
    counts: Dict[str, int] = {lang: 0 for lang in _LANGUAGES if lang != "python"}
    python_key = score_key("python", batch_size)

    for model_test in benchmark.values():
        python_score = _safe_float(model_test.get(python_key))
        if python_score is None or python_score <= 0:
            continue

        for language in _LANGUAGES:
            if language == "python": continue
            language_key = score_key(language, batch_size)
            language_score = _safe_float(model_test.get(language_key))
            if language_score is None: continue
            totals[language] += language_score / python_score # must be 1 for python
            counts[language] += 1

    this_coefficients = {
        language: (totals[language] / counts[language]) if counts[language] else 0.0
        for language in totals
    } # the python coefficient is always 1.0
    _LANGUAGE_COEFFICIENTS_CACHE[batch_size] = this_coefficients
    return this_coefficients

def _bench_score(model_test: dict, batch_size: int, coefficients: Dict[str, float]) -> float:
    """ Compute the bench score for a given model test result and a batch size.
        In case that values are missing, we use the coefficients to estimate the missing values.
    """
    python_score = _safe_float(model_test.get(score_key("python", batch_size)))
    if python_score is None: return 0.0
    combined_score = 0.0
    for language, weight in _LANGUAGE_WEIGHTS.items():
        if language == "python":
            score = python_score
        else:
            language_key = score_key(language, batch_size)
            language_score = _safe_float(model_test.get(language_key))
            if language_score is None:
                score = coefficients.get(language, 0.0) * python_score
            else:
                score = language_score
        combined_score += weight * score

    return combined_score / _TOTAL_WEIGHT
    
def bench_score(benchmark: dict, model_test: dict, batch_size:int) -> int:
    """ this computes the bench score for a given model test result and a batch size."""
    coefficients = _language_coefficients(benchmark, batch_size)
    return _bench_score(model_test, batch_size, coefficients)

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