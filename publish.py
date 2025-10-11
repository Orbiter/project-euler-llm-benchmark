from typing import Dict
from pathlib import Path
from argparse import ArgumentParser
from benchmark import read_benchmark

LANGUAGE_WEIGHTS: Dict[str, float] = {
    "python": 4.0,
    "java": 3.0,
    "rust": 2.0,
    "clojure": 1.0,
}

SECTION_HEADERS: Dict[int, str] = {
    200: "## Results for PE-Bench-200",
    100: "## Archived Outdated PE-Bench-100",
}

class BenchmarkPublisher:
    """Generate the README table from the benchmark results."""

    def __init__(self, batch_size: int, readme_path: str | Path = "README.md") -> None:
        self.batch_size = batch_size
        self.readme_path = Path(readme_path)
        self.languages = list(LANGUAGE_WEIGHTS.keys())
        self.total_weight = sum(LANGUAGE_WEIGHTS.values())
        self.benchmark = read_benchmark()
        self.sorted_benchmark: Dict[str, Dict[str, object]] = {}

    def publish(self) -> None:
        coefficients = self._compute_language_coefficients()
        self._apply_combined_scores(coefficients)
        self.sorted_benchmark = dict(
            sorted(
                self.benchmark.items(),
                key=lambda item: float(item[1].get("_bench_score", 0.0)),
                reverse=True,
            )
        )

        readme_text = self.readme_path.read_text(encoding="utf-8")
        new_table = self._build_table()
        updated_readme, existing_table = self._replace_table(readme_text, new_table)

        if existing_table:
            print(existing_table)
        print(new_table)

        self.readme_path.write_text(updated_readme, encoding="utf-8")

    def _score_key(self, language: str) -> str:
        return f"{language}-{self.batch_size}"

    @staticmethod
    def _safe_float(value: object) -> float | None:
        try:
            if value in (None, ""):
                return None
            return float(value)
        except (TypeError, ValueError):
            return None

    def _compute_language_coefficients(self) -> Dict[str, float]:
        totals: Dict[str, float] = {lang: 0.0 for lang in self.languages if lang != "python"}
        counts: Dict[str, int] = {lang: 0 for lang in self.languages if lang != "python"}
        python_key = self._score_key("python")

        for entry in self.benchmark.values():
            python_score = self._safe_float(entry.get(python_key))
            if python_score is None or python_score <= 0:
                continue

            for language in self.languages:
                if language == "python":
                    continue
                language_key = self._score_key(language)
                language_score = self._safe_float(entry.get(language_key))
                if language_score is None:
                    continue
                totals[language] += language_score / python_score
                counts[language] += 1

        return {
            language: (totals[language] / counts[language]) if counts[language] else 0.0
            for language in totals
        }

    def _apply_combined_scores(self, coefficients: Dict[str, float]) -> None:
        python_key = self._score_key("python")

        for entry in self.benchmark.values():
            python_score = self._safe_float(entry.get(python_key))
            if python_score is None:
                entry["_bench_score"] = 0.0
                continue

            combined_score = 0.0
            for language, weight in LANGUAGE_WEIGHTS.items():
                score = self._resolve_language_score(language, entry, python_score, coefficients)
                combined_score += weight * score

            entry["_bench_score"] = combined_score / self.total_weight

    def _resolve_language_score(
        self,
        language: str,
        entry: Dict[str, object],
        python_score: float,
        coefficients: Dict[str, float],
    ) -> float:
        if language == "python":
            return python_score

        language_key = self._score_key(language)
        language_score = self._safe_float(entry.get(language_key))
        if language_score is not None:
            return language_score

        return coefficients.get(language, 0.0) * python_score

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

            if start_idx is None and line.lstrip().startswith("| Model"):
                capture = True
                start_idx = idx

            if capture:
                if stripped == "" or line.lstrip().startswith("|"):
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

    def _build_table(self) -> str:
        python_key = self._score_key("python")
        max_model_name = max((len(name) for name in self.sorted_benchmark), default=len("Model"))

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

        for model_name, entry in self.sorted_benchmark.items():
            size_raw = entry.get("_parameter_size", "")
            quant_raw = entry.get("_quantization_level", "")
            context_raw = entry.get("_context_size", "")

            size_value = self._safe_float(size_raw)
            quant_value = self._safe_float(quant_raw)
            python_value = entry.get(python_key, "")

            memory_amount = (
                (size_value * quant_value / 8.0)
                if size_value is not None and size_value > 0 and quant_value is not None and quant_value > 0
                else float("inf")
            )
            bench_score = float(entry.get("_bench_score", 0.0))
            memory_score = (
                (100.0 * bench_score / memory_amount) if memory_amount not in (0.0, float("inf")) else None
            )

            best_model = False
            if memory_amount <= lowest_memory_amount:
                lowest_memory_amount = memory_amount
                best_model = True

            if python_value in (None, ""):
                continue

            bench_python = self._stringify(entry.get(python_key, ""))
            bench_java = self._stringify(entry.get(self._score_key("java"), ""))
            bench_rust = self._stringify(entry.get(self._score_key("rust"), ""))
            bench_clojure = self._stringify(entry.get(self._score_key("clojure"), ""))

            best_value = ""
            if best_model and memory_amount not in (float("inf"), 0.0):
                if memory_amount >= 100.0:
                    best_value = f"{memory_amount:.0f}"
                else:
                    best_value = f"{memory_amount:.2f}"

            bench_score_str = f"{bench_score:.2f}"
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

        return "\n".join(lines) + "\n\n"

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
        publisher = BenchmarkPublisher(batch_size=batch_size, readme_path=readme_path)
        publisher.publish()


if __name__ == "__main__":
    main()
