#!/usr/bin/env python3

import argparse
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_BENCHMARK_PATH = SCRIPT_DIR / "benchmark.json"
DEFAULT_SOLUTIONS_PATH = SCRIPT_DIR / "solutions"
TIMESTAMP_FIELD = "timestamp"

# Benchmark series are named e.g. python-200, python-200-test,
# python-200-tool or python-tool-200.  The latter form is produced by the
# current helper functions, while the former also occurs in existing data.
SERIES_KEY_PATTERN = re.compile(
    r"^(?P<language>[^-]+)-(?:tool-)?\d+(?:-tool)?(?:-test)?$"
)

# inference.py writes <problem>.md and <problem>.json, codeextraction.py writes
# <problem>.<language extension>, and inference-with-tools.py writes
# tool-<problem>.<language extension>. execute.py additionally writes
# solutions.json.
NUMBERED_TEST_FILE_PATTERN = re.compile(r"^(?:tool-)?\d+\.[^.]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct benchmark record timestamps from the newest test "
            "artifact belonging to each record."
        )
    )
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=DEFAULT_BENCHMARK_PATH,
        help="benchmark JSON to update (default: benchmark.json next to this script)",
    )
    parser.add_argument(
        "--solutions",
        type=Path,
        default=DEFAULT_SOLUTIONS_PATH,
        help="solutions directory (default: solutions next to this script)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="reconstruct and report timestamps without writing benchmark.json",
    )
    return parser.parse_args()


def languages_for_record(record: dict) -> list[str]:
    """Return languages in their first-occurrence order in the record."""
    languages: list[str] = []
    for key in record:
        match = SERIES_KEY_PATTERN.fullmatch(key)
        if not match:
            continue
        language = match.group("language")
        if language not in languages:
            languages.append(language)
    return languages


def is_test_artifact(filename: str) -> bool:
    return filename == "solutions.json" or bool(
        NUMBERED_TEST_FILE_PATTERN.fullmatch(filename)
    )


def newest_test_mtime(
    solutions_path: Path, model_name: str, languages: list[str]
) -> float | None:
    newest_mtime: float | None = None

    for language in languages:
        language_path = solutions_path / model_name / language
        try:
            entries = os.scandir(language_path)
        except (FileNotFoundError, NotADirectoryError):
            continue

        with entries:
            for entry in entries:
                if entry.name.startswith(".") or not is_test_artifact(entry.name):
                    continue
                try:
                    if not entry.is_file(follow_symlinks=True):
                        continue
                    mtime = entry.stat(follow_symlinks=True).st_mtime
                except FileNotFoundError:
                    # A concurrently running test may replace a file between
                    # scandir() and stat(); it will be picked up on a later run.
                    continue
                if newest_mtime is None or mtime > newest_mtime:
                    newest_mtime = mtime

    return newest_mtime


def iso_8601_utc(timestamp: float) -> str:
    return (
        datetime.fromtimestamp(timestamp, timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def reconstruct_timestamps(
    benchmark: dict, solutions_path: Path
) -> tuple[int, int, list[str]]:
    reconstructed = 0
    preserved = 0
    missing: list[str] = []

    # Assigning a value to an existing dict does not move it, and adding the
    # timestamp only appends a field inside the record.  The top-level record
    # order therefore remains unchanged.
    for model_name, record in benchmark.items():
        if not isinstance(record, dict):
            missing.append(model_name)
            continue

        # This script may be run on several machines that hold different
        # subsets of the test artifacts.  A timestamp reconstructed earlier is
        # authoritative and must never be replaced by a later run.
        if TIMESTAMP_FIELD in record:
            preserved += 1
            continue

        languages = languages_for_record(record)
        newest_mtime = newest_test_mtime(solutions_path, model_name, languages)
        if newest_mtime is None:
            missing.append(model_name)
            continue

        record[TIMESTAMP_FIELD] = iso_8601_utc(newest_mtime)
        reconstructed += 1

    return reconstructed, preserved, missing


def write_json_atomically(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(data, temporary_file, indent=4, ensure_ascii=False)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    args = parse_args()
    benchmark_path = args.benchmark.resolve()
    solutions_path = args.solutions.resolve()

    with benchmark_path.open("r", encoding="utf-8") as benchmark_file:
        benchmark = json.load(benchmark_file)
    if not isinstance(benchmark, dict):
        raise ValueError(f"{benchmark_path} must contain a JSON object.")

    original_order = list(benchmark)
    reconstructed, preserved, missing = reconstruct_timestamps(
        benchmark, solutions_path
    )
    if list(benchmark) != original_order:
        raise RuntimeError("The benchmark record order changed unexpectedly.")

    if not args.dry_run and reconstructed > 0:
        write_json_atomically(benchmark_path, benchmark)

    action = "Would update" if args.dry_run else "Updated"
    print(
        f"{action} {reconstructed} missing timestamps in "
        f"{benchmark_path.name}; preserved {preserved} existing timestamps."
    )
    if missing:
        print(
            f"No test artifact was found for {len(missing)} records; "
            "their timestamp was left unchanged:"
        )
        for model_name in missing:
            print(f"  {model_name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
