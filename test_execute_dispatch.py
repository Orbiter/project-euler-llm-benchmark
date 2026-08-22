import unittest
from unittest.mock import MagicMock, mock_open, patch

import execute


class JavaScriptDispatcherTests(unittest.TestCase):
    def test_javascript_extension_round_trip(self):
        self.assertEqual(execute.get_extension("javascript"), "js")
        self.assertEqual(execute.get_language_from_extension("js"), "javascript")

    def test_tool_result_uses_canonical_key_order(self):
        self.assertEqual(
            execute.get_series_name("javascript", 200, tool_mode=True),
            "javascript-200-tool",
        )

    def test_javascript_file_uses_javascript_runner(self):
        with patch(
            "builtins.open", mock_open(read_data="console.log(6 * 7);")
        ), patch("execute.execute_javascript_code", return_value="42") as run_js:
            output = execute.execute_solution(
                "solutions/model/javascript/0001.js", {"solution": "42"}
            )

        self.assertEqual(output, "42")
        run_js.assert_called_once_with("console.log(6 * 7);")

    @patch("execute.multiprocessing.cpu_count", return_value=64)
    @patch("execute.os.path.exists", return_value=True)
    @patch(
        "execute.os.listdir",
        return_value=[f"{number:04d}.js" for number in range(1, 11)],
    )
    @patch("execute.ThreadPoolExecutor")
    def test_javascript_workers_are_capped(
        self, executor_class, _listdir, _exists, _cpu_count
    ):
        executor = MagicMock()
        executor.map.return_value = []
        executor_class.return_value.__enter__.return_value = executor

        execute.process_solutions("model", "javascript", 10, {})

        executor_class.assert_called_once_with(
            max_workers=execute.JAVASCRIPT_MAX_WORKERS
        )


if __name__ == "__main__":
    unittest.main()
