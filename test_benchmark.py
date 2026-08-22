import unittest

import benchmark


class MissingValueEstimationTests(unittest.TestCase):
    def setUp(self):
        benchmark._LANGUAGE_COEFFICIENTS_CACHE.clear()
        benchmark._LANGUAGE_OBSERVED_COEFFICIENTS_CACHE.clear()
        benchmark._LANGUAGE_COEFFICIENT_COUNTS_CACHE.clear()

    def tearDown(self):
        benchmark._LANGUAGE_COEFFICIENTS_CACHE.clear()
        benchmark._LANGUAGE_OBSERVED_COEFFICIENTS_CACHE.clear()
        benchmark._LANGUAGE_COEFFICIENT_COUNTS_CACHE.clear()

    def test_missing_javascript_uses_batch_specific_python_ratio(self):
        first = {"python-200": 100, "javascript-200": 80}
        second = {"python-200": 50, "javascript-200": 30}
        target = {
            "python-200": 40,
            "java-200": 0,
            "rust-200": 0,
            "clojure-200": 0,
        }
        data = {
            "first": first,
            "second": second,
            "third": {"python-200": 100, "javascript-200": 70},
            "fourth": {"python-200": 100, "javascript-200": 70},
            "fifth": {"python-200": 100, "javascript-200": 70},
            "target": target,
        }

        # Median JavaScript/Python ratio is 0.7,
        # so the missing JavaScript score is estimated as 0.7 * 40 = 28.
        expected = (5 * 40 + 4 * 28) / 15
        self.assertAlmostEqual(benchmark.bench_score(data, target, 200), expected)
        self.assertNotIn("javascript-200", target)

    def test_complete_score_uses_exact_five_language_weights(self):
        entry = {
            "python-200": 10,
            "javascript-200": 20,
            "java-200": 30,
            "rust-200": 40,
            "clojure-200": 50,
        }

        expected = (5 * 10 + 4 * 20 + 3 * 30 + 2 * 40 + 50) / 15
        self.assertAlmostEqual(
            benchmark.bench_score({"model": entry}, entry, 200), expected
        )

    def test_each_non_python_language_can_be_estimated(self):
        calibrator = {
            "python-100": 10,
            "javascript-100": 20,
            "java-100": 30,
            "rust-100": 40,
            "clojure-100": 50,
        }
        target = {"python-100": 2}
        data = {
            **{f"calibrator-{index}": calibrator for index in range(5)},
            "target": target,
        }

        expected = (5 * 2 + 4 * 4 + 3 * 6 + 2 * 8 + 1 * 10) / 15
        self.assertAlmostEqual(benchmark.bench_score(data, target, 100), expected)
        self.assertEqual(target, {"python-100": 2})

    def test_coefficient_median_resists_an_extreme_outlier(self):
        data = {
            **{
                f"normal-{index}": {
                    "python-200": 100,
                    "javascript-200": 75,
                }
                for index in range(4)
            },
            "outlier": {"python-200": 1, "javascript-200": 10_000},
        }
        target = {
            "python-200": 40,
            "java-200": 0,
            "rust-200": 0,
            "clojure-200": 0,
        }
        data["target"] = target

        # The outlier would make the arithmetic-mean coefficient about 2000.6.
        # The median remains 0.75, estimating JavaScript at 30.
        expected = (5 * 40 + 4 * 30) / 15
        self.assertAlmostEqual(benchmark.bench_score(data, target, 200), expected)
        summary = benchmark.language_coefficient_summary(data, 200)
        self.assertEqual(summary["javascript"]["coefficient"], 0.75)
        self.assertEqual(summary["javascript"]["samples"], 5)

    def test_non_finite_calibration_values_are_not_counted(self):
        data = {
            "valid": {"python-200": 100, "javascript-200": 75},
            "infinite-python": {
                "python-200": float("inf"),
                "javascript-200": 75,
            },
            "nan-language": {
                "python-200": 100,
                "javascript-200": float("nan"),
            },
        }

        summary = benchmark.language_coefficient_summary(data, 200)
        self.assertEqual(summary["javascript"]["observed_coefficient"], 0.75)
        self.assertEqual(summary["javascript"]["samples"], 1)

    def test_uncalibrated_language_is_excluded_instead_of_counted_as_zero(self):
        target = {
            "python-200": 10,
            "java-200": 10,
            "rust-200": 10,
            "clojure-200": 10,
        }

        self.assertEqual(benchmark.bench_score({"target": target}, target, 200), 10)
        summary = benchmark.language_coefficient_summary({"target": target}, 200)
        self.assertIsNone(summary["javascript"]["coefficient"])
        self.assertEqual(summary["javascript"]["samples"], 0)
        self.assertFalse(summary["javascript"]["ready"])

    def test_single_pair_coefficient_is_observed_and_used(self):
        calibrator = {"python-200": 10, "javascript-200": 0}
        target = {
            "python-200": 10,
            "java-200": 10,
            "rust-200": 10,
            "clojure-200": 10,
        }
        data = {"calibrator": calibrator, "target": target}

        self.assertAlmostEqual(benchmark.bench_score(data, target, 200), 110 / 15)
        summary = benchmark.language_coefficient_summary(data, 200)
        self.assertEqual(summary["javascript"]["coefficient"], 0.0)
        self.assertEqual(summary["javascript"]["observed_coefficient"], 0.0)
        self.assertEqual(summary["javascript"]["samples"], 1)
        self.assertEqual(summary["javascript"]["required_samples"], 1)
        self.assertTrue(summary["javascript"]["ready"])

    def test_coefficient_activates_at_required_sample_count(self):
        calibrator = {"python-200": 10, "javascript-200": 0}
        target = {
            "python-200": 10,
            "java-200": 10,
            "rust-200": 10,
            "clojure-200": 10,
        }
        data = {"calibrator": calibrator, "target": target}

        self.assertAlmostEqual(benchmark.bench_score(data, target, 200), 110 / 15)
        summary = benchmark.language_coefficient_summary(data, 200)
        self.assertEqual(summary["javascript"]["coefficient"], 0.0)
        self.assertEqual(summary["javascript"]["samples"], 1)
        self.assertTrue(summary["javascript"]["ready"])

    def test_tool_mode_uses_separate_coefficients(self):
        calibrator = {
            "python-200-tool": 100,
            "javascript-200-tool": 75,
        }
        target = {
            "python-200-tool": 40,
            "java-200-tool": 0,
            "rust-200-tool": 0,
            "clojure-200-tool": 0,
        }
        data = {
            **{f"calibrator-{index}": calibrator for index in range(5)},
            "target": target,
        }

        expected = (5 * 40 + 4 * 30) / 15
        self.assertAlmostEqual(
            benchmark.bench_score(data, target, 200, tool_mode=True), expected
        )
        summary = benchmark.language_coefficient_summary(data, 200, tool_mode=True)
        self.assertEqual(summary["javascript"]["coefficient"], 0.75)
        self.assertEqual(summary["javascript"]["samples"], 5)
        self.assertTrue(summary["javascript"]["ready"])


if __name__ == "__main__":
    unittest.main()
