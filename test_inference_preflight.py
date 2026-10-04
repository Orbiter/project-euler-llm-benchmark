import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import inference
from codeextraction import process_markdown_files
from execute import execute_solution
from llm_client import Endpoint, LLMIncompleteResponse, LLMRequestTimeout


class InferenceFailureOutputTests(unittest.TestCase):
    def test_failed_problems_write_markdown_and_can_be_extracted(self):
        endpoint = Endpoint("test-model", "test-model", "", "https://example.com/v1/chat/completions")
        failures = [
            (LLMRequestTimeout("Overall timeout"), "Overall timeout"),
            (LLMIncompleteResponse("Stream ended prematurely"), "Stream ended prematurely"),
            (RuntimeError("API error"), "API error"),
            (RuntimeError(), "RuntimeError"),
            (RuntimeError("API error 429\n```python\nprint(429)\n```"), "API error 429\n```python\nprint(429)\n```"),
        ]
        for error, message in failures:
            with self.subTest(error=message), tempfile.TemporaryDirectory() as temp_dir:
                original_dir = os.getcwd()
                try:
                    os.chdir(temp_dir)
                    problems = Path("problems")
                    problems.mkdir()
                    for number in ("0001", "0002"):
                        (problems / f"{number}.txt").write_text("Example problem", encoding="utf-8")
                    with patch.object(inference, "ensure_model_available", return_value=True), patch.object(
                        inference, "read_benchmark", return_value={}
                    ), patch("llm_client.openai_api_chat", side_effect=error) as chat:
                        inference.process_problem_files(
                            str(problems), "$$$PROBLEM$$$", [endpoint], "python"
                        )

                    self.assertEqual(chat.call_count, 4)
                    process_markdown_files("test-model", "python")
                    for number in ("0001", "0002"):
                        output = Path("solutions/test-model/python") / number
                        expected = f"# error\n{message}\n"
                        self.assertEqual(output.with_suffix(".md").read_text(encoding="utf-8"), expected)
                        self.assertEqual(output.with_suffix(".py").read_text(encoding="utf-8"), expected)
                        self.assertTrue(
                            execute_solution(str(output.with_suffix(".py")), {"solution": "429"}).startswith("Error:")
                        )
                finally:
                    os.chdir(original_dir)


class StandardInferencePreflightTests(unittest.TestCase):
    def test_javascript_preflight_runs_before_endpoint_setup(self):
        with patch.object(
            sys, "argv", ["inference.py", "--language", "javascript"]
        ), patch.object(
            inference,
            "ensure_javascript_runtime",
            side_effect=RuntimeError("Node.js preflight failed"),
        ) as preflight, patch.object(inference, "build_endpoints") as build_endpoints:
            with self.assertRaisesRegex(RuntimeError, "Node.js preflight failed"):
                inference.main()

        preflight.assert_called_once_with()
        build_endpoints.assert_not_called()

    def test_non_javascript_inference_skips_node_preflight(self):
        with patch.object(
            sys, "argv", ["inference.py", "--language", "python"]
        ), patch.object(inference, "ensure_javascript_runtime") as preflight, patch.object(
            inference,
            "build_endpoints",
            side_effect=RuntimeError("endpoint setup reached"),
        ):
            with self.assertRaisesRegex(RuntimeError, "endpoint setup reached"):
                inference.main()

        preflight.assert_not_called()


if __name__ == "__main__":
    unittest.main()
