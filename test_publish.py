import unittest
from unittest.mock import patch

from publish import BenchmarkPublisher


def make_publisher(batch_size: int) -> BenchmarkPublisher:
    publisher = BenchmarkPublisher.__new__(BenchmarkPublisher)
    publisher.batch_size = batch_size
    publisher.benchmark = {}
    return publisher


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


class PerformanceScoreTests(unittest.TestCase):
    @patch(
        "publish.language_coefficient_summary",
        return_value={
            "javascript": {
                "coefficient": None,
                "observed_coefficient": None,
                "samples": 0,
                "required_samples": 1,
                "ready": False,
            }
        },
    )
    def test_publish_refuses_uncalibrated_javascript(self, _summary):
        publisher = make_publisher(200)

        with self.assertRaisesRegex(
            RuntimeError, r"JavaScript/Python calibration.*standard \(0/1\)"
        ):
            publisher.publish()

    def test_pe_200_published_table_ignores_tool_mode(self):
        publisher = make_publisher(200)
        entry = {
            "python-200": 10,
            "javascript-200": 10,
            "java-200": 10,
            "rust-200": 10,
            "clojure-200": 10,
        }
        publisher.benchmark = {"model-a": entry}
        publisher.sorted_benchmark = publisher.benchmark

        table = publisher._build_table()

        self.assertIn("### Non-Thinking", table)
        self.assertNotIn("Tool Usage", table)

    @patch("publish.bench_score", return_value=42.5)
    def test_regular_score_uses_benchmark_estimator(self, estimate):
        publisher = make_publisher(200)
        publisher.benchmark = {"model-a": {"python-200": 50}}
        entry = publisher.benchmark["model-a"]

        self.assertEqual(publisher._entry_score(entry), 42.5)
        estimate.assert_called_once_with(
            publisher.benchmark, entry, 200, tool_mode=False
        )

    @patch("publish.bench_score", return_value=41.5)
    def test_tool_score_uses_benchmark_estimator(self, estimate):
        publisher = make_publisher(200)
        publisher.benchmark = {"model-a": {"python-200-tool": 50}}
        entry = publisher.benchmark["model-a"]

        self.assertEqual(publisher._entry_score(entry, tool_mode=True), 41.5)
        estimate.assert_called_once_with(
            publisher.benchmark, entry, 200, tool_mode=True
        )

    def test_formula_uses_pe_output_and_one_percent_of_prompt_rate(self):
        publisher = make_publisher(200)
        entry = {
            "_output_tokens_per_second": 100,
            "_prompt_tokens_per_second": 1_665,
        }

        score = publisher._performance_score(entry, pe_score=100.0)

        self.assertAlmostEqual(score, 116.65)

    def test_performance_column_is_immediately_right_of_pe_200(self):
        publisher = make_publisher(200)
        entry = {
            "python-200": 100,
            "javascript-200": 100,
            "java-200": 100,
            "rust-200": 100,
            "clojure-200": 100,
            "_output_tokens_per_second": 100,
            "_prompt_tokens_per_second": 1_665,
        }

        table = publisher._build_table_for_entries(
            {"model-a": entry},
            max_model_name=len("model-a"),
        )
        header, _alignment, row = table.splitlines()
        header_cells = table_cells(header)
        row_cells = table_cells(row)

        pe_index = header_cells.index("PE-200-<br/>Score")
        javascript_index = header_cells.index("JavaScript")
        self.assertEqual(header_cells[pe_index + 1], "Performance-<br/>Score")
        self.assertEqual(row_cells[pe_index], "100.00")
        self.assertEqual(row_cells[pe_index + 1], "116.65")
        self.assertEqual(row_cells[javascript_index], "100")

    def test_missing_performance_measurement_produces_empty_cell(self):
        publisher = make_publisher(200)
        entry = {
            "python-200": 50,
            "javascript-200": 50,
            "java-200": 50,
            "rust-200": 50,
            "clojure-200": 50,
        }

        table = publisher._build_table_for_entries(
            {"model-a": entry},
            max_model_name=len("model-a"),
        )
        header, _alignment, row = table.splitlines()
        header_cells = table_cells(header)
        row_cells = table_cells(row)
        performance_index = header_cells.index("Performance-<br/>Score")

        self.assertEqual(row_cells[performance_index], "")

    def test_tool_table_contains_javascript_results(self):
        publisher = make_publisher(200)
        entry = {
            "python-200-tool": 25,
            "javascript-200-tool": 25,
            "java-200-tool": 25,
            "rust-200-tool": 25,
            "clojure-200-tool": 25,
        }
        publisher.benchmark = {"model-a": entry}

        table = publisher._build_table_for_entries(
            {"model-a": entry},
            max_model_name=len("model-a"),
            tool_mode=True,
        )
        header, _alignment, row = table.splitlines()
        header_cells = table_cells(header)
        row_cells = table_cells(row)
        javascript_index = header_cells.index("JavaScript")

        self.assertEqual(row_cells[javascript_index], "25")
        self.assertEqual(row_cells[header_cells.index("PE-200-<br/>Score")], "25.00")

    def test_archived_pe_100_table_has_no_performance_column(self):
        publisher = make_publisher(100)
        table = publisher._build_table_for_entries(
            {"model-a": {"python-100": 10}},
            max_model_name=len("model-a"),
        )

        header = table.splitlines()[0]
        self.assertNotIn("Performance-<br/>Score", header)


if __name__ == "__main__":
    unittest.main()
