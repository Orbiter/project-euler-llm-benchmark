import unittest

import benchmark_grid_draw as grid


class FiveLanguageGridTests(unittest.TestCase):
    def test_complete_models_require_javascript_results(self):
        ones = "1" * grid.COLUMNS
        complete = {
            f"{language}-200-test": ones
            for language in ("python", "javascript", "java", "rust", "clojure")
        }
        missing_javascript = {
            key: value
            for key, value in complete.items()
            if key != "javascript-200-test"
        }

        models = grid.collect_models_with_tests(
            {"complete": complete, "missing": missing_javascript}
        )

        self.assertEqual([name for name, _, _ in models], ["complete"])
        self.assertEqual(grid.count_solutions(models[0][1]), [5] * grid.COLUMNS)

    def test_five_is_the_highest_color_and_legend_level(self):
        self.assertEqual(grid.color_for_count(5), grid.COLORS[5])
        self.assertEqual(grid.color_for_count(100), grid.COLORS[5])
        self.assertEqual(grid.COLOR_KEY_ITEMS[-1], (5, "5 languages"))


if __name__ == "__main__":
    unittest.main()
