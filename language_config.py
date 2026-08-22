"""Shared language configuration for the benchmark pipeline."""

from types import MappingProxyType
from typing import Final, Mapping


REFERENCE_LANGUAGE: Final = "python"

LANGUAGE_WEIGHTS: Final[Mapping[str, float]] = MappingProxyType({
    "python": 5.0,
    "javascript": 4.0,
    "java": 3.0,
    "rust": 2.0,
    "clojure": 1.0,
})
BENCHMARK_LANGUAGES: Final = tuple(LANGUAGE_WEIGHTS)
DEFAULT_LANGUAGES: Final = ",".join(BENCHMARK_LANGUAGES)
TOTAL_LANGUAGE_WEIGHT: Final = sum(LANGUAGE_WEIGHTS.values())

LANGUAGE_DISPLAY_NAMES: Final[Mapping[str, str]] = MappingProxyType({
    "python": "Python",
    "javascript": "JavaScript",
    "java": "Java",
    "rust": "Rust",
    "clojure": "Clojure",
})

# The extraction script historically accepts more languages than the benchmark runs.
LANGUAGE_EXTENSIONS: Final[Mapping[str, str]] = MappingProxyType({
    "c": "c",
    "r": "r",
    "go": "go",
    "c++": "cpp",
    "lua": "lua",
    "java": "java",
    "lisp": "lisp",
    "rust": "rs",
    "ruby": "rb",
    "perl": "pl",
    "python": "py",
    "prolog": "pl",
    "matlab": "matlab",
    "kotlin": "kt",
    "clojure": "clj",
    "fortran": "f",
    "javascript": "js",
})

_BENCHMARK_LANGUAGE_BY_EXTENSION: Final = {
    LANGUAGE_EXTENSIONS[language]: language for language in BENCHMARK_LANGUAGES
}


def get_extension(language: str) -> str:
    """Return the source-file extension for a supported language."""
    try:
        return LANGUAGE_EXTENSIONS[language]
    except KeyError as exc:
        raise ValueError(f"Unsupported language: {language}") from exc


def get_language_from_extension(extension: str) -> str:
    """Resolve a benchmark language from its source-file extension."""
    try:
        return _BENCHMARK_LANGUAGE_BY_EXTENSION[extension]
    except KeyError as exc:
        raise ValueError(f"Unsupported extension: {extension}") from exc
