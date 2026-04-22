from typing import Dict
from pathlib import Path
from argparse import ArgumentParser
from benchmark import read_benchmark, score_key, sort_benchmark

SECTION_HEADERS: Dict[int, str] = {
    200: "## Results for PE-Bench-200",
    100: "## Archived Outdated PE-Bench-100",
}

LANGUAGE_WEIGHTS: Dict[str, float] = {
    "python": 4.0,
    "java": 3.0,
    "rust": 2.0,
    "clojure": 1.0,
}
TOTAL_WEIGHT = sum(LANGUAGE_WEIGHTS.values())

class BenchmarkPublisher:
    """Generate the README table from the benchmark results."""

    def __init__(self, batch_size: int, readme_path: str | Path = "README.md") -> None:
        self.batch_size = batch_size
        self.readme_path = Path(readme_path)
        self.benchmark = read_benchmark()
        self.sorted_benchmark: dict = {}

    def publish(self) -> None:
        self.sorted_benchmark = sort_benchmark(self.benchmark, self.batch_size)
        readme_text = self.readme_path.read_text(encoding="utf-8")
        new_table = self._build_table()
        updated_readme, existing_table = self._replace_table(readme_text, new_table)
        print(new_table)
        self.readme_path.write_text(updated_readme, encoding="utf-8")

    @staticmethod
    def _safe_float(value: object) -> float | None:
        try:
            if value in (None, ""): return None
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _is_thinking(entry: dict) -> bool:
        value = entry.get("thinking", False)
        if isinstance(value, str):
            return value.strip().lower() == "true"
        return bool(value)

    def _section_header(self) -> str | None:
        return SECTION_HEADERS.get(self.batch_size)

    def _replace_table(self, readme_text: str, new_table: str) -> tuple[str, str]:
        lines = readme_text.splitlines(keepends=True)
        offsets: list[int] = [0]
        total = 0
        for line in lines:
            total += len(line)
            offsets.append(total)

        header_target = self._section_header()
        batch_token = f"PE-Bench-{self.batch_size}"

        in_section = False
        section_start_idx: int | None = None
        section_end_idx: int | None = None
        start_idx: int | None = None
        end_idx: int | None = None
        capture = False

        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("## "):
                if in_section and section_end_idx is None:
                    section_end_idx = idx

                matches_header = (
                    (header_target is not None and stripped == header_target)
                    or (header_target is None and batch_token in stripped)
                )
                in_section = matches_header
                if matches_header:
                    section_start_idx = idx
                capture = False
                continue

            if not in_section:
                continue

            if start_idx is None and (
                line.lstrip().startswith("### ") or line.lstrip().startswith("| Model")
            ):
                capture = True
                start_idx = idx

            if capture:
                if stripped == "" or line.lstrip().startswith("|") or line.lstrip().startswith("### "):
                    end_idx = idx + 1
                else:
                    capture = False

        if in_section and section_end_idx is None:
            section_end_idx = len(lines)

        if section_start_idx is None:
            raise ValueError(f"Could not locate section for batch size {self.batch_size}.")

        if start_idx is not None and end_idx is None:
            end_idx = len(lines)

        if start_idx is not None and end_idx is not None:
            start_char = offsets[start_idx]
            end_char = offsets[end_idx]
            existing_table = readme_text[start_char:end_char]
            updated_readme = readme_text[:start_char] + new_table + readme_text[end_char:]
            return updated_readme, existing_table

        insert_idx = section_end_idx if section_end_idx is not None else len(lines)
        insert_char = offsets[insert_idx]

        prefix = readme_text[:insert_char]
        if prefix and not prefix.endswith("\n"):
            prefix += "\n"
        suffix = readme_text[insert_char:]

        updated_readme = prefix + new_table + suffix
        return updated_readme, ""

    def _partition_by_thinking(self) -> tuple[dict, dict]:
        non_thinking: dict = {}
        thinking: dict = {}
        for model_name, entry in self.sorted_benchmark.items():
            (thinking if self._is_thinking(entry) else non_thinking)[model_name] = entry
        return non_thinking, thinking

    def _result_key(self, language: str, tool_mode: bool = False) -> str:
        if tool_mode:
            return f"{language}-{self.batch_size}-tool"
        return score_key(language, self.batch_size)

    def _has_results(self, entry: dict, tool_mode: bool = False) -> bool:
        return entry.get(self._result_key("python", tool_mode), "") not in (None, "")

    def _entry_score(self, entry: dict, tool_mode: bool = False) -> float:
        python_score = self._safe_float(entry.get(self._result_key("python", tool_mode)))
        if python_score is None:
            return 0.0

        combined_score = 0.0
        for language, weight in LANGUAGE_WEIGHTS.items():
            language_score = self._safe_float(entry.get(self._result_key(language, tool_mode)))
            if language_score is None:
                language_score = 0.0
            combined_score += weight * language_score
        return combined_score / TOTAL_WEIGHT

    def _sorted_entries(self, entries: dict, tool_mode: bool = False) -> dict:
        filtered_entries = {
            model_name: entry
            for model_name, entry in entries.items()
            if self._has_results(entry, tool_mode)
        }
        sorted_items = sorted(
            filtered_entries.items(),
            key=lambda item: self._entry_score(item[1], tool_mode),
            reverse=True,
        )
        return dict(sorted_items)

    def _build_table(self) -> str:
        max_model_name = max((len(name) for name in self.sorted_benchmark), default=len("Model"))

        if self.batch_size == 200:
            non_thinking, thinking = self._partition_by_thinking()
            groups = [
                ("### Non-Thinking", self._sorted_entries(non_thinking, tool_mode=False), False),
                ("### Thinking", self._sorted_entries(thinking, tool_mode=False), False),
                ("### Non-Thinking Tool Usage", self._sorted_entries(non_thinking, tool_mode=True), True),
                ("### Thinking Tool Usage", self._sorted_entries(thinking, tool_mode=True), True),
            ]
        else:
            groups = [(None, self._sorted_entries(self.sorted_benchmark, tool_mode=False), False)]

        tables: list[str] = []
        for heading, entries, tool_mode in groups:
            table_text = self._build_table_for_entries(entries, max_model_name, tool_mode=tool_mode)
            if heading:
                tables.append(f"{heading}\n{table_text}")
            else:
                tables.append(table_text)

        return "\n\n".join(tables).rstrip() + "\n\n"

    def _build_table_for_entries(self, entries: dict, max_model_name: int, tool_mode: bool = False) -> str:
        col_best = "Best<br/>Model<br/>for<br/>Size (GB)"
        col_bench_score = f"PE-{self.batch_size}-<br/>Score"
        col_memory_score = "Mem-<br/>Score"
        col_size = "Size<br/>*10^9 Params"
        col_quant = "Bits"
        col_context = "Context Length<br/>(K)"
        col_python = "Python"
        col_java = "Java"
        col_rust = "Rust"
        col_clojure = "Clojure"

        header = (
            f"| {'Model'.ljust(max_model_name)} | {col_best} | {col_bench_score} | {col_memory_score} | "
            f"{col_size} | {col_quant} | {col_context} | {col_python} | {col_java} | {col_rust} | {col_clojure} |"
        )
        alignment = (
            f"| :{'-' * (max_model_name - 1)} | {'-' * (len(col_best) - 1)}: | {'-' * (len(col_bench_score) - 1)}: | "
            f"{'-' * (len(col_memory_score) - 1)}: | {'-' * (len(col_size) - 1)}: | {'-' * (len(col_quant) - 1)}: | "
            f"{'-' * (len(col_context) - 1)}: | {'-' * (len(col_python) - 1)}: | {'-' * (len(col_java) - 1)}: | "
            f"{'-' * (len(col_rust) - 1)}: | {'-' * (len(col_clojure) - 1)}: |"
        )

        lines = [header, alignment]
        lowest_memory_amount = float("inf")

        python_key = self._result_key("python", tool_mode)
        for model_name, entry in entries.items():
            python_value = entry.get(python_key, "")
            if python_value in (None, ""): continue

            size_raw = entry.get("_parameter_size", "")
            quant_raw = entry.get("_quantization_level", "")
            context_raw = entry.get("_context_size", "")
            size_value = self._safe_float(size_raw)
            quant_value = self._safe_float(quant_raw)

            if size_value is None or size_value <= 0 or quant_value is None or quant_value <= 0:
                memory_amount = float("inf")
            else:
                if quant_value == 4:
                    memory_amount = size_value * 0.75
                elif quant_value == 8:
                    memory_amount = size_value * 1.1
                else:
                    memory_amount = size_value * 2.0
 
            bench_score_value = self._entry_score(entry, tool_mode)
            memory_score = (
                (100.0 * bench_score_value / memory_amount) if memory_amount not in (0.0, float("inf")) else None
            )

            best_model = False
            if memory_amount <= lowest_memory_amount:
                lowest_memory_amount = memory_amount
                best_model = True

            bench_python = self._stringify(python_value)
            bench_java = self._stringify(entry.get(self._result_key("java", tool_mode), ""))
            bench_rust = self._stringify(entry.get(self._result_key("rust", tool_mode), ""))
            bench_clojure = self._stringify(entry.get(self._result_key("clojure", tool_mode), ""))

            best_value = ""
            if best_model and memory_amount not in (float("inf"), 0.0):
                if memory_amount >= 100.0:
                    best_value = f"{memory_amount:.0f}"
                else:
                    best_value = f"{memory_amount:.2f}"

            bench_score_str = f"{bench_score_value:.2f}"
            memory_score_str = f"{memory_score:.0f}" if memory_score is not None else ""
            size_str = self._stringify(size_raw)
            quant_str = self._stringify(quant_raw)
            context_str = self._stringify(context_raw)

            line = "| " + model_name.ljust(max_model_name)
            line += " | " + f"{best_value:>8}"
            line += " | " + f"{bench_score_str:>6}"
            line += " | " + f"{memory_score_str:>6}"
            line += " | " + f"{size_str:>6}"
            line += " | " + f"{quant_str:>4}"
            line += " | " + f"{context_str:>4}"
            line += " | " + f"{bench_python:>4}"
            line += " | " + f"{bench_java:>4}"
            line += " | " + f"{bench_rust:>4}"
            line += " | " + f"{bench_clojure:>4}"
            line += " |"

            lines.append(line)

        return "\n".join(lines)

    @staticmethod
    def _stringify(value: object) -> str:
        if value in (None, ""):
            return ""
        return str(value)


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Publish benchmark results to the README table.")
    parser.add_argument(
        "--batch-size",
        type=int,
        nargs="*",
        default=[200, 100],
        help="Problem batch sizes to publish (e.g., 200 100). Defaults to updating both tables.",
    )
    parser.add_argument(
        "--readme",
        type=str,
        default="README.md",
        help="Path to the README file that contains the benchmark table.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    readme_path = args.readme
    batch_sizes = args.batch_size or [200, 100]

    for batch_size in batch_sizes:
        publisher = BenchmarkPublisher(batch_size, readme_path)
        publisher.publish()

if __name__ == "__main__":
    main()
