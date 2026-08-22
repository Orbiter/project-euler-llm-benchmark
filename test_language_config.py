import unittest

from language_config import (
    BENCHMARK_LANGUAGES,
    DEFAULT_LANGUAGES,
    LANGUAGE_DISPLAY_NAMES,
    LANGUAGE_WEIGHTS,
    TOTAL_LANGUAGE_WEIGHT,
    get_extension,
    get_language_from_extension,
)


class LanguageConfigTests(unittest.TestCase):
    def test_canonical_order_weights_and_defaults(self):
        self.assertEqual(
            BENCHMARK_LANGUAGES,
            ("python", "javascript", "java", "rust", "clojure"),
        )
        self.assertEqual(list(LANGUAGE_WEIGHTS.values()), [5.0, 4.0, 3.0, 2.0, 1.0])
        self.assertEqual(DEFAULT_LANGUAGES, "python,javascript,java,rust,clojure")
        self.assertEqual(TOTAL_LANGUAGE_WEIGHT, 15.0)

    def test_benchmark_extensions_round_trip(self):
        expected_extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "rust": "rs",
            "clojure": "clj",
        }
        for language, extension in expected_extensions.items():
            with self.subTest(language=language):
                self.assertEqual(get_extension(language), extension)
                self.assertEqual(get_language_from_extension(extension), language)

    def test_every_benchmark_language_has_a_display_name(self):
        self.assertEqual(set(LANGUAGE_DISPLAY_NAMES), set(BENCHMARK_LANGUAGES))

    def test_extraction_only_extensions_remain_supported(self):
        self.assertEqual(get_extension("c++"), "cpp")
        self.assertEqual(get_extension("fortran"), "f")

    def test_unknown_language_and_extension_fail_clearly(self):
        with self.assertRaisesRegex(ValueError, "Unsupported language"):
            get_extension("brainfuck")
        with self.assertRaisesRegex(ValueError, "Unsupported extension"):
            get_language_from_extension("cpp")


if __name__ == "__main__":
    unittest.main()
