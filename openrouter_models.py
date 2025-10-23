
import os
import re
import json
import logging
import requests
import argparse
from dataclasses import dataclass
from collections import defaultdict
from benchmark import read_benchmark, write_benchmark
from typing import Dict, Iterable, List, Optional, Sequence, Set

MODEL_SOURCE_URL = "https://openrouter.ai/api/frontend/models"
MODEL_CACHE_FILE = "openrouter_models.json"

_STOP_TOKENS = {
    "hf",
    "co",
    "gguf",
    "km",
    "it",
    "b",
    "m",
    "t",
    "v",
    "model",
    "models",
    "adapter",
    "adaptername",
    "openrouter",
    "standard",
    "preview",
}

_QUANTIZATION_REGEXPS = [
    re.compile(r"q(\d{1,2})", re.IGNORECASE),
    re.compile(r"(\d{1,2})\s*bit", re.IGNORECASE),
    re.compile(r"int(\d{1,2})", re.IGNORECASE),
    re.compile(r"fp(\d{1,2})", re.IGNORECASE),
]

_PARAMETER_SIZE_REGEX = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>[btm])\b", re.IGNORECASE
)

@dataclass
class MatchResult:
    benchmark_name: str
    entry_slug: Optional[str]
    hf_slug: Optional[str]
    entry_id: Optional[int]
    score: float
    reason: str

@dataclass
class ModelDetails:
    context_size: Optional[int]
    parameter_size: Optional[float]
    quantization_level: Optional[int]
    match: Optional[MatchResult]

def download_models(output_path: str = MODEL_CACHE_FILE, timeout: int = 30) -> Dict:
    """
    Download the OpenRouter model manifest to the local cache file.
    """
    logging.info("Downloading OpenRouter models to %s", output_path)
    response = requests.get(MODEL_SOURCE_URL, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    logging.info("Stored %d models in %s", len(data.get("data", [])), output_path)
    return data

def load_models(path: str = MODEL_CACHE_FILE) -> List[Dict]:
    """
    Load the cached OpenRouter models JSON file.
    """
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    models = payload.get("data", [])
    logging.debug("Loaded %d OpenRouter models from %s", len(models), path)
    return models

def _normalize_identifier(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())

def _tokenize(value: str) -> Set[str]:
    tokens: Set[str] = set()
    pieces = re.split(r"[^a-z0-9]+", value.lower())
    for piece in pieces:
        if not piece or piece in _STOP_TOKENS:
            continue
        if piece.isdigit():
            continue
        if re.fullmatch(r"v\d+", piece):
            continue
        tokens.add(piece)
        subtokens = re.findall(r"[a-z]+|\d+[a-z]*", piece)
        for sub in subtokens:
            if sub and sub not in _STOP_TOKENS:
                if sub.isdigit():
                    continue
                if re.fullmatch(r"v\d+", sub):
                    continue
                tokens.add(sub)
    return tokens

def _quantization_from_string(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    for regex in _QUANTIZATION_REGEXPS:
        match = regex.search(value)
        if match:
            number = match.group(1)
            try:
                return int(number)
            except ValueError:
                continue
    return None

def _parameter_size_from_strings(values: Sequence[str]) -> Optional[float]:
    best_value: Optional[float] = None
    for candidate in values:
        if not candidate:
            continue
        for match in _PARAMETER_SIZE_REGEX.finditer(candidate):
            value = float(match.group("value"))
            unit = match.group("unit").lower()
            if unit == "t":
                value *= 1000.0
            elif unit == "m":
                value /= 1000.0
            if best_value is None or value > best_value:
                best_value = value
    return best_value

def _to_k_units(raw_tokens: Optional[int]) -> Optional[int]:
    if not raw_tokens or raw_tokens <= 0:
        return None
    for divisor in (1000, 1024):
        if raw_tokens % divisor == 0:
            return raw_tokens // divisor
    return raw_tokens // 1000 if raw_tokens >= 1000 else raw_tokens

def _strip_quantization_suffix(name: str) -> str:
    without_suffix = re.sub(
        r"(:|-|/)?(q|fp|int)\d{1,2}[_\-a-z0-9]*$", "", name, flags=re.IGNORECASE
    )
    return without_suffix

def _benchmark_variants(name: str) -> Set[str]:
    name = name.strip()
    variants = {name, name.lower()}
    if name.lower().startswith("hf.co/"):
        trimmed = name[6:]
        variants.add(trimmed)
        variants.add(trimmed.split(":")[0])
    for sep in [":", "/"]:
        if sep in name:
            before, after = name.split(sep, 1)
            variants.add(before)
            variants.add(after)
            variants.add(f"{before}-{after}")
            variants.add(f"{before}/{after}")
    variants.add(name.replace(":", "-"))
    variants.add(name.replace(":", "/"))
    variants.add(_strip_quantization_suffix(name))
    return {variant for variant in variants if variant}

@dataclass
class _OpenRouterEntry:
    raw: Dict
    slug: Optional[str]
    hf_slug: Optional[str]
    aliases: Set[str]
    tokens: Set[str]

class OpenRouterIndex:
    def __init__(self, models: Iterable[Dict]):
        self.entries: List[_OpenRouterEntry] = []
        self._normalized_map: Dict[str, List[_OpenRouterEntry]] = defaultdict(list)
        for model in models:
            entry = self._create_entry(model)
            self.entries.append(entry)
            for alias in entry.aliases:
                normalized = _normalize_identifier(alias)
                if not normalized:
                    continue
                self._normalized_map[normalized].append(entry)

    def _create_entry(self, model: Dict) -> _OpenRouterEntry:
        aliases: Set[str] = set()
        slug = model.get("slug")
        hf_slug = model.get("hf_slug")
        aliases.update(
            filter(
                None,
                [
                    slug,
                    model.get("permaslug"),
                    hf_slug,
                    model.get("name"),
                    model.get("short_name"),
                ],
            )
        )

        endpoint = model.get("endpoint") or {}
        endpoint_model = endpoint.get("model") or {}
        aliases.update(
            filter(
                None,
                [
                    endpoint.get("model_variant_slug"),
                    endpoint.get("model_variant_permaslug"),
                    endpoint.get("provider_model_id"),
                    endpoint.get("name"),
                    endpoint_model.get("slug"),
                    endpoint_model.get("permaslug"),
                    endpoint_model.get("name"),
                ],
            )
        )

        tokens: Set[str] = set()
        for alias in aliases:
            tokens.update(_tokenize(alias))
        # Add group tokens for additional hints
        if model.get("group"):
            tokens.update(_tokenize(str(model["group"])))

        return _OpenRouterEntry(
            raw=model,
            slug=slug,
            hf_slug=hf_slug,
            aliases=aliases,
            tokens=tokens,
        )

    def match(self, benchmark_name: str) -> Optional[MatchResult]:
        direct_candidates = self._direct_match_candidates(benchmark_name)
        if len(direct_candidates) == 1:
            entry = next(iter(direct_candidates))
            return MatchResult(
                benchmark_name=benchmark_name,
                entry_slug=entry.slug,
                hf_slug=entry.hf_slug,
                entry_id=id(entry),
                score=10.0,
                reason="direct",
            )
        if len(direct_candidates) > 1:
            entry = self._best_token_match(benchmark_name, direct_candidates)
            if entry:
                return MatchResult(
                    benchmark_name=benchmark_name,
                    entry_slug=entry.slug,
                    hf_slug=entry.hf_slug,
                    entry_id=id(entry),
                    score=5.0,
                    reason="direct-ambiguous",
                )

        entry = self._best_token_match(benchmark_name, self.entries)
        if entry:
            bench_tokens = _tokenize(_strip_quantization_suffix(benchmark_name))
            common = bench_tokens & entry.tokens
            score = float(len(common))
            return MatchResult(
                benchmark_name=benchmark_name,
                entry_slug=entry.slug,
                hf_slug=entry.hf_slug,
                entry_id=id(entry),
                score=score,
                reason="fuzzy",
            )
        return None

    def _direct_match_candidates(
        self, benchmark_name: str
    ) -> List[_OpenRouterEntry]:
        variants = _benchmark_variants(benchmark_name)
        matches: Dict[str, _OpenRouterEntry] = {}
        for variant in variants:
            normalized = _normalize_identifier(variant)
            if not normalized:
                continue
            for entry in self._normalized_map.get(normalized, []):
                key = entry.slug or str(id(entry))
                if key not in matches:
                    matches[key] = entry
        return list(matches.values())

    def _best_token_match(
        self, benchmark_name: str, candidates: Iterable[_OpenRouterEntry]
    ) -> Optional[_OpenRouterEntry]:
        bench_tokens = _tokenize(_strip_quantization_suffix(benchmark_name))
        if not bench_tokens:
            return None
        best_entry: Optional[_OpenRouterEntry] = None
        best_score = 0.0
        for entry in candidates:
            common = bench_tokens & entry.tokens
            if not common or len(common) < 2:
                continue
            if not any(token and token[0].isalpha() for token in common):
                continue
            common_ratio = len(common) / max(len(bench_tokens), 1)
            if common_ratio < 0.5:
                continue
            numeric_bonus = sum(1 for token in common if any(char.isdigit() for char in token))
            score = len(common) + numeric_bonus
            if entry.hf_slug:
                hf_tokens = _tokenize(entry.hf_slug)
                score += 0.2 * len(bench_tokens & hf_tokens)
            if score > best_score:
                best_score = score
                best_entry = entry
        return best_entry

    def resolve_details(self, benchmark_name: str) -> ModelDetails:
        match = self.match(benchmark_name)
        if not match:
            return ModelDetails(None, None, None, None)
        entry = self._entry_by_slug(match.entry_slug, match.entry_id)
        if not entry:
            return ModelDetails(None, None, None, match)
        context_size = self._extract_context_size(entry.raw)
        parameter_size = self._extract_parameter_size(entry.raw)
        quantization_level = self._extract_quantization_level(entry.raw, benchmark_name)
        return ModelDetails(context_size, parameter_size, quantization_level, match)

    def _entry_by_slug(
        self, slug: Optional[str], entry_id: Optional[int]
    ) -> Optional[_OpenRouterEntry]:
        for entry in self.entries:
            if slug and entry.slug == slug:
                return entry
            if entry_id and id(entry) == entry_id:
                return entry
        return None

    @staticmethod
    def _extract_context_size(model: Dict) -> Optional[int]:
        candidates: List[int] = []
        for key in ("context_length", "max_prompt_tokens"):
            value = model.get(key)
            if isinstance(value, int):
                candidates.append(value)
        endpoint = model.get("endpoint") or {}
        for key in ("context_length", "max_prompt_tokens"):
            value = endpoint.get(key)
            if isinstance(value, int):
                candidates.append(value)
        endpoint_model = endpoint.get("model") or {}
        value = endpoint_model.get("context_length")
        if isinstance(value, int):
            candidates.append(value)
        return _to_k_units(max(candidates)) if candidates else None

    @staticmethod
    def _extract_parameter_size(model: Dict) -> Optional[float]:
        candidates: List[str] = []
        candidates.extend(
            filter(
                None,
                [
                    model.get("hf_slug"),
                    model.get("slug"),
                    model.get("name"),
                    model.get("short_name"),
                    model.get("group"),
                ],
            )
        )
        endpoint = model.get("endpoint") or {}
        endpoint_model = endpoint.get("model") or {}
        candidates.extend(
            filter(
                None,
                [
                    endpoint.get("name"),
                    endpoint.get("model_variant_slug"),
                    endpoint.get("model_variant_permaslug"),
                    endpoint_model.get("name"),
                    endpoint_model.get("slug"),
                ],
            )
        )
        return _parameter_size_from_strings(candidates)

    @staticmethod
    def _extract_quantization_level(
        model: Dict, benchmark_name: str
    ) -> Optional[int]:
        benchmark_lower = benchmark_name.lower()
        explicit = _quantization_from_string(benchmark_name)
        if explicit:
            return explicit
        quant_strings: List[str] = []
        for key in ("quantization", "variant", "group"):
            value = model.get(key)
            if isinstance(value, str):
                quant_strings.append(value)
        endpoint = model.get("endpoint") or {}
        for key in ("quantization", "provider_slug", "name"):
            value = endpoint.get(key)
            if isinstance(value, str):
                quant_strings.append(value)
        endpoint_model = endpoint.get("model") or {}
        if isinstance(endpoint_model.get("name"), str):
            quant_strings.append(endpoint_model["name"])

        for quant_string in quant_strings:
            quant = _quantization_from_string(quant_string)
            if quant:
                if "mlx" in benchmark_lower and quant >= 8:
                    return 4
                return quant

        if "mlx" in benchmark_lower:
            return 4

        return 4

def enrich_benchmark(
    index: OpenRouterIndex,
    model_names: Optional[Sequence[str]] = None,
    dry_run: bool = False,
) -> Dict[str, Dict[str, Optional[float]]]:
    """
    Populate missing benchmark metadata using OpenRouter models.

    Returns a dict containing the modifications per model for reporting.
    """
    benchmark = read_benchmark()
    if not benchmark:
        raise RuntimeError("No benchmark data available.")

    target_fields = ("_context_size", "_parameter_size", "_quantization_level")
    if model_names:
        missing_keys = [name for name in model_names if name not in benchmark]
        if missing_keys:
            raise KeyError(f"Model(s) not found in benchmark: {', '.join(missing_keys)}")
        candidate_items = ((name, benchmark[name]) for name in model_names)
    else:
        candidate_items = benchmark.items()

    modifications: Dict[str, Dict[str, Optional[float]]] = {}

    for name, data in candidate_items:
        missing = [
            field for field in target_fields if data.get(field) in (None, "", 0)
        ]
        if not missing:
            continue
        details = index.resolve_details(name)
        if not details.match:
            logging.debug("No OpenRouter match for %s", name)
            continue
        update_payload: Dict[str, Optional[float]] = {}
        if "_context_size" in missing and details.context_size:
            data["_context_size"] = details.context_size
            update_payload["_context_size"] = details.context_size
        if "_parameter_size" in missing and details.parameter_size:
            data["_parameter_size"] = details.parameter_size
            update_payload["_parameter_size"] = details.parameter_size
        if "_quantization_level" in missing and details.quantization_level:
            data["_quantization_level"] = details.quantization_level
            update_payload["_quantization_level"] = details.quantization_level

        if update_payload:
            modifications[name] = update_payload
            if details.match:
                logging.info(
                    "Matched %s -> %s (%s) with updates %s",
                    name,
                    details.match.entry_slug,
                    details.match.reason,
                    update_payload,
                )

    if modifications and not dry_run:
        write_benchmark(benchmark)
    elif modifications:
        logging.info("Dry run enabled, not writing benchmark.json")

    return modifications

def lookup_model(index: OpenRouterIndex, benchmark_name: str) -> ModelDetails:
    return index.resolve_details(benchmark_name)

def _configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="OpenRouter model utilities for Project Euler benchmark"
    )
    parser.add_argument(
        "--models-path",
        default=MODEL_CACHE_FILE,
        help="Path to the cached openrouter models JSON file",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable debug logging output"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    download_parser = subparsers.add_parser("download", help="Download OpenRouter model list")
    download_parser.add_argument(
        "--output",
        default=MODEL_CACHE_FILE,
        help="Destination file for the downloaded manifest",
    )

    lookup_parser = subparsers.add_parser(
        "lookup", help="Lookup details for a benchmark model"
    )
    lookup_parser.add_argument("model", help="Benchmark model name to resolve")

    enrich_parser = subparsers.add_parser(
        "enrich", help="Fill missing metadata in benchmark.json"
    )
    enrich_parser.add_argument(
        "--model",
        action="append",
        help="Specific benchmark model(s) to update (can be repeated)",
    )
    enrich_parser.add_argument(
        "--dry-run", action="store_true", help="Compute updates without writing files"
    )

    args = parser.parse_args(argv)
    _configure_logging(args.verbose)

    if args.command == "download":
        download_models(output_path=args.output)
        return 0

    models_path = args.models_path
    if not os.path.exists(models_path):
        raise FileNotFoundError(
            f"{models_path} does not exist. Please run the download command first."
        )
    models = load_models(models_path)
    index = OpenRouterIndex(models)

    if args.command == "lookup":
        details = lookup_model(index, args.model)
        if not details.match:
            logging.error("No match found for %s", args.model)
            return 1
        payload = {
            "match": {
                "benchmark_name": details.match.benchmark_name,
                "entry_slug": details.match.entry_slug,
                "hf_slug": details.match.hf_slug,
                "score": details.match.score,
                "reason": details.match.reason,
            },
            "_context_size": details.context_size,
            "_parameter_size": details.parameter_size,
            "_quantization_level": details.quantization_level,
        }
        print(json.dumps(payload, indent=2))
        return 0

    if args.command == "enrich":
        modifications = enrich_benchmark(
            index, model_names=args.model, dry_run=args.dry_run
        )
        print(json.dumps(modifications, indent=2))
        return 0

    parser.print_help()
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
