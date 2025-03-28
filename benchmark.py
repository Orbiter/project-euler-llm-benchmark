import os
import time
import json
import logging

# Constants
BENCHMARK_FILE = 'benchmark.json'
BENCHMARK_FILE_STOP = 'benchmark.json.stop' # yes thats ugly
STOP_FILE_TIMEOUT = 60  # seconds

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

def read_benchmark():
    """Read the benchmark data from the JSON file."""
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

def write_benchmark(benchmark):
    """Write the benchmark data to the JSON file."""
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
