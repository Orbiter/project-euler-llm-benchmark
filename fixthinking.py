#!/usr/bin/env python3

import argparse
import json
import os
import stat
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_BENCHMARK_PATH = SCRIPT_DIR / "benchmark.json"
DEFAULT_SOLUTIONS_PATH = SCRIPT_DIR / "solutions"

START_DATE = date(2026, 3, 1)
END_DATE = date(2026, 7, 19)
OLD_SUFFIX = "-no_think"
NEW_SUFFIX = "-think"


@dataclass(frozen=True)
class Change:
    old_name: str
    new_name: str
    timestamp: str
    source_directory: Path
    destination_directory: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Rename affected -no_think benchmark records and test directories "
            "to -think for the configured inclusive UTC date range."
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
        help="validate and show all changes without modifying files",
    )
    return parser.parse_args()


def timestamp_date_utc(value: object, model_name: str) -> date:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{model_name}: missing timestamp")

    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise ValueError(
            f"{model_name}: invalid ISO 8601 timestamp {value!r}"
        ) from error

    if parsed.tzinfo is None:
        raise ValueError(f"{model_name}: timestamp has no timezone: {value!r}")
    return parsed.astimezone(timezone.utc).date()


def model_directory(solutions_path: Path, model_name: str) -> Path:
    solutions_root = solutions_path.resolve()
    candidate = (solutions_root / model_name).resolve()
    try:
        candidate.relative_to(solutions_root)
    except ValueError as error:
        raise ValueError(
            f"Model name resolves outside the solutions directory: {model_name!r}"
        ) from error
    return candidate


def collect_changes(benchmark: dict, solutions_path: Path) -> list[Change]:
    changes: list[Change] = []
    timestamp_errors: list[str] = []

    for model_name, record in benchmark.items():
        if not isinstance(record, dict):
            continue
        if "thinking" in record and record["thinking"] is not False:
            continue
        if not model_name.endswith(OLD_SUFFIX):
            continue

        source_directory = model_directory(solutions_path, model_name)

        try:
            record_date = timestamp_date_utc(record.get("timestamp"), model_name)
        except ValueError as error:
            if not source_directory.is_dir():
                continue
            timestamp_errors.append(str(error))
            continue

        if not START_DATE <= record_date <= END_DATE:
            continue

        new_name = model_name[: -len(OLD_SUFFIX)] + NEW_SUFFIX
        destination_directory = model_directory(solutions_path, new_name)
        if new_name in benchmark or destination_directory.exists():
            continue

        changes.append(
            Change(
                old_name=model_name,
                new_name=new_name,
                timestamp=record["timestamp"],
                source_directory=source_directory,
                destination_directory=destination_directory,
            )
        )

    if timestamp_errors:
        details = "\n".join(f"  {error}" for error in timestamp_errors)
        raise ValueError(
            "Cannot determine whether all potential records are in the date "
            f"range. Reconstruct their timestamps first:\n{details}"
        )

    return changes


def validate_changes(benchmark: dict, changes: list[Change]) -> None:
    errors: list[str] = []

    for change in changes:
        if change.new_name in benchmark:
            errors.append(
                f"benchmark record already exists: {change.new_name}"
            )
        if change.destination_directory.exists():
            errors.append(
                f"destination test directory already exists: "
                f"{change.destination_directory}"
            )

    if errors:
        details = "\n".join(f"  {error}" for error in errors)
        raise RuntimeError(f"Preflight validation failed:\n{details}")


def updated_benchmark(benchmark: dict, changes: list[Change]) -> dict:
    changes_by_name = {change.old_name: change for change in changes}
    updated: dict = {}

    for model_name, record in benchmark.items():
        change = changes_by_name.get(model_name)
        if change is None:
            updated[model_name] = record
            continue

        updated_record = dict(record)
        updated_record["thinking"] = True
        updated[change.new_name] = updated_record

    if len(updated) != len(benchmark):
        raise RuntimeError("The number of benchmark records changed unexpectedly.")
    return updated


def write_json_atomically(path: Path, data: dict) -> None:
    original_mode = stat.S_IMODE(path.stat().st_mode)
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

        os.chmod(temporary_path, original_mode)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def rollback_directories(renamed: list[Change]) -> None:
    rollback_errors: list[str] = []
    for change in reversed(renamed):
        try:
            change.destination_directory.rename(change.source_directory)
        except OSError as error:
            rollback_errors.append(
                f"{change.destination_directory} -> "
                f"{change.source_directory}: {error}"
            )

    if rollback_errors:
        details = "\n".join(f"  {error}" for error in rollback_errors)
        raise RuntimeError(f"Directory rollback failed:\n{details}")


def apply_changes(
    benchmark_path: Path, benchmark: dict, changes: list[Change]
) -> None:
    new_benchmark = updated_benchmark(benchmark, changes)
    renamed: list[Change] = []

    try:
        for change in changes:
            if change.source_directory.is_dir():
                change.source_directory.rename(change.destination_directory)
                renamed.append(change)
        write_json_atomically(benchmark_path, new_benchmark)
    except BaseException:
        rollback_directories(renamed)
        raise


def print_changes(changes: list[Change]) -> None:
    for change in changes:
        print(
            f"{change.timestamp}: {change.old_name} -> {change.new_name}"
        )
        print(
            f"  {change.source_directory} -> "
            f"{change.destination_directory}"
        )


def main() -> int:
    args = parse_args()
    benchmark_path = args.benchmark.resolve()
    solutions_path = args.solutions.resolve()

    with benchmark_path.open("r", encoding="utf-8") as benchmark_file:
        benchmark = json.load(benchmark_file)
    if not isinstance(benchmark, dict):
        raise ValueError(f"{benchmark_path} must contain a JSON object.")

    changes = collect_changes(benchmark, solutions_path)
    validate_changes(benchmark, changes)

    print(
        f"Found {len(changes)} records from {START_DATE.isoformat()} through "
        f"{END_DATE.isoformat()} (inclusive) to update."
    )
    print_changes(changes)

    if args.dry_run:
        print("Dry run complete; no files were changed.")
        return 0

    if not changes:
        print("No files were changed.")
        return 0

    apply_changes(benchmark_path, benchmark, changes)
    print(f"Updated {len(changes)} records and test directories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
