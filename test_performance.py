import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import performance


class HardwareGuardTests(unittest.TestCase):
    @patch("performance._post_chat")
    @patch("performance.unload_all_ollama_models")
    @patch("performance.list_ollama_models")
    @patch("performance.platform.machine", return_value="x86_64")
    @patch("performance.platform.system", return_value="Linux")
    def test_main_terminates_before_request_on_wrong_hardware(
        self, _system, _machine, list_models, unload_models, post_chat
    ):
        result = performance.main(["--all"])

        self.assertEqual(result, 1)
        list_models.assert_not_called()
        unload_models.assert_not_called()
        post_chat.assert_not_called()

    @patch("performance._sysctl_value")
    @patch("performance.platform.machine", return_value="arm64")
    @patch("performance.platform.system", return_value="Darwin")
    def test_m1_ultra_mac_studio_is_accepted(self, _system, _machine, sysctl):
        sysctl.side_effect = ["Mac13,2", "Apple M1 Ultra"]

        self.assertEqual(
            performance.require_m1_mac_studio(),
            ("Mac13,2", "Apple M1 Ultra"),
        )

    @patch("performance._sysctl_value")
    @patch("performance.platform.machine", return_value="arm64")
    @patch("performance.platform.system", return_value="Darwin")
    def test_newer_mac_studio_is_rejected(self, _system, _machine, sysctl):
        sysctl.side_effect = ["Mac14,13", "Apple M2 Ultra"]

        with self.assertRaises(performance.PerformanceBenchmarkError):
            performance.require_m1_mac_studio()


class PerformanceCalculationTests(unittest.TestCase):
    def test_rate_uses_ollama_nanosecond_duration(self):
        data = {"eval_count": 75, "eval_duration": 826_062_839}

        self.assertAlmostEqual(
            performance._rate(data, "eval_count", "eval_duration"),
            90.792,
            places=3,
        )

    def test_benchmark_update_preserves_entry_and_adds_only_two_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "benchmark.json"
            path.write_text(
                json.dumps({"model-a": {"python-200": 12.5}}),
                encoding="utf-8",
            )

            performance.update_benchmark(path, "model-a", 91, 225)
            updated = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(
            updated,
            {
                "model-a": {
                    "python-200": 12.5,
                    "_output_tokens_per_second": 91,
                    "_prompt_tokens_per_second": 225,
                }
            },
        )
        self.assertIsInstance(updated["model-a"]["_output_tokens_per_second"], int)
        self.assertIsInstance(updated["model-a"]["_prompt_tokens_per_second"], int)

    def test_only_two_positive_integer_values_count_as_complete(self):
        self.assertTrue(
            performance.has_performance_values({
                "_output_tokens_per_second": 91,
                "_prompt_tokens_per_second": 225,
            })
        )
        self.assertFalse(
            performance.has_performance_values({
                "_output_tokens_per_second": 91,
            })
        )

    def test_existing_think_variants_are_both_selected(self):
        benchmark = {
            "model-a-think": {"python-200": 10},
            "model-a-no_think": {"python-200": 11},
        }

        self.assertEqual(
            performance.benchmark_store_names(benchmark, "model-a"),
            ["model-a-think", "model-a-no_think"],
        )

    def test_base_name_is_used_when_no_think_variant_exists(self):
        self.assertEqual(
            performance.benchmark_store_names({}, "new-model"),
            ["new-model"],
        )
        self.assertFalse(
            performance.has_performance_values({
                "_output_tokens_per_second": 91.5,
                "_prompt_tokens_per_second": 225,
            })
        )

    @patch("performance.measure_performance")
    @patch("performance.unload_all_ollama_models")
    @patch("performance.list_ollama_models")
    @patch("performance.require_m1_mac_studio")
    def test_all_skips_complete_models_and_benchmarks_the_rest(
        self, hardware, list_models, unload_models, measure
    ):
        hardware.return_value = ("Mac13,2", "Apple M1 Ultra")
        list_models.return_value = ["complete-model", "missing-model", "partial-model"]
        measure.side_effect = [(101, 201), (102, 202)]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "benchmark.json"
            path.write_text(
                json.dumps({
                    "complete-model": {
                        "_output_tokens_per_second": 90,
                        "_prompt_tokens_per_second": 190,
                    },
                    "partial-model-think": {"_output_tokens_per_second": 80},
                    "partial-model-no_think": {
                        "_output_tokens_per_second": 81,
                        "_prompt_tokens_per_second": 181,
                    },
                }),
                encoding="utf-8",
            )

            result = performance.main([
                "--all",
                "--runs", "1",
                "--benchmark", str(path),
            ])
            updated = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        self.assertEqual(
            [call.args[1] for call in measure.call_args_list],
            ["missing-model", "partial-model"],
        )
        self.assertEqual(unload_models.call_count, 2)
        self.assertEqual(
            updated["complete-model"],
            {
                "_output_tokens_per_second": 90,
                "_prompt_tokens_per_second": 190,
            },
        )
        self.assertEqual(updated["missing-model"]["_output_tokens_per_second"], 101)
        self.assertEqual(
            updated["partial-model-think"]["_prompt_tokens_per_second"],
            202,
        )
        self.assertEqual(
            updated["partial-model-no_think"]["_output_tokens_per_second"],
            102,
        )

    @patch("performance.requests.post")
    @patch("performance.list_running_ollama_models")
    @patch("performance.list_ollama_models")
    def test_pre_run_cleanup_unloads_every_active_model_and_verifies(
        self, list_models, list_running, post
    ):
        list_models.return_value = ["model-a", "model-b", "model-c"]
        list_running.side_effect = [["model-a", "model-c"], []]
        post.return_value = Mock()

        performance.unload_all_ollama_models("http://localhost:11434")

        self.assertEqual(list_models.call_count, 1)
        self.assertEqual(list_running.call_count, 2)
        self.assertEqual(post.call_count, 2)
        self.assertEqual(
            [call.kwargs["json"] for call in post.call_args_list],
            [
                {"model": "model-a", "keep_alive": 0, "stream": False},
                {"model": "model-c", "keep_alive": 0, "stream": False},
            ],
        )

    @patch("performance.requests.post")
    @patch("performance.time.sleep")
    @patch("performance.time.monotonic", side_effect=[0, 31])
    @patch("performance.list_running_ollama_models")
    @patch("performance.list_ollama_models", return_value=["model-a"])
    def test_pre_run_cleanup_fails_if_a_model_remains_active(
        self, _list_models, list_running, _monotonic, _sleep, post
    ):
        list_running.side_effect = [["model-a"], ["model-a"]]
        post.return_value = Mock()

        with self.assertRaisesRegex(
            performance.PerformanceBenchmarkError,
            "still reports active models",
        ):
            performance.unload_all_ollama_models("http://localhost:11434")

    @patch("performance.requests.Session")
    @patch("performance._post_chat")
    def test_measurement_returns_rounded_medians(self, post_chat, session_class):
        session_class.return_value.__enter__.return_value = Mock()
        post_chat.side_effect = [
            {},  # warm-up response is intentionally not included
            {
                "eval_count": 100,
                "eval_duration": 1_000_000_000,
                "prompt_eval_count": 5_000,
                "prompt_eval_duration": 2_000_000_000,
            },
            {
                "eval_count": 101,
                "eval_duration": 500_000_000,
                "prompt_eval_count": 5_000,
                "prompt_eval_duration": 1_000_000_000,
            },
            {
                "eval_count": 99,
                "eval_duration": 330_000_000,
                "prompt_eval_count": 5_000,
                "prompt_eval_duration": 500_000_000,
            },
        ]

        rates = performance.measure_performance(
            "http://localhost:11434",
            "test-model",
            runs=3,
            prompt_records=1,
            num_ctx=8_192,
            num_predict=100,
        )

        self.assertEqual(rates, (202, 5_000))


if __name__ == "__main__":
    unittest.main()
