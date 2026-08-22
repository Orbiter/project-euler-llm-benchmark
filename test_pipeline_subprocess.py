import subprocess
import sys
import unittest
from unittest.mock import call, patch

import test as pipeline


class PipelineSubprocessTests(unittest.TestCase):
    @patch("test.subprocess.run")
    def test_standard_pipeline_runs_all_steps_as_checked_argument_lists(self, run):
        pipeline.test(
            "https://api.example/v1",
            "",
            "model with spaces",
            "javascript",
            overwrite_existing=True,
            overwrite_failed=True,
            max_problem_number=200,
            think=True,
        )

        common = ["--model", "model with spaces", "--think"]
        self.assertEqual(
            run.call_args_list,
            [
                call(
                    [
                        sys.executable,
                        pipeline._base_dir + "/inference.py",
                        "--language",
                        "javascript",
                        "--api_base",
                        "https://api.example/v1",
                        *common,
                        "--n200",
                        "--overwrite_existing",
                        "--overwrite_failed",
                    ],
                    check=True,
                ),
                call(
                    [
                        sys.executable,
                        pipeline._base_dir + "/codeextraction.py",
                        "--language",
                        "javascript",
                        *common,
                    ],
                    check=True,
                ),
                call(
                    [
                        sys.executable,
                        pipeline._base_dir + "/execute.py",
                        "--language",
                        "javascript",
                        *common,
                    ],
                    check=True,
                ),
            ],
        )

    @patch(
        "test.subprocess.run",
        side_effect=subprocess.CalledProcessError(7, ["inference.py"]),
    )
    def test_failed_inference_aborts_the_remaining_pipeline(self, run):
        with self.assertRaises(subprocess.CalledProcessError) as raised:
            pipeline.test(
                "http://localhost:11434",
                "",
                "model",
                "javascript",
                overwrite_existing=False,
                overwrite_failed=False,
            )

        self.assertEqual(raised.exception.returncode, 7)
        self.assertEqual(run.call_count, 1)

    @patch("test.subprocess.run")
    def test_tool_pipeline_runs_only_tool_inference(self, run):
        pipeline.test(
            "http://localhost:11434",
            "endpoint-name",
            "ignored-model",
            "javascript",
            overwrite_existing=False,
            overwrite_failed=False,
            tool_mode=True,
            endpoint_store_name="published-name",
            endpoint_model_name="provider/model",
        )

        self.assertEqual(run.call_count, 1)
        command = run.call_args.args[0]
        self.assertTrue(command[1].endswith("inference-with-tools.py"))
        self.assertIn("endpoint-name", command)
        self.assertIn("published-name", command)
        self.assertIn("provider/model", command)
        self.assertTrue(run.call_args.kwargs["check"])


if __name__ == "__main__":
    unittest.main()
