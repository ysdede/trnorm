"""
Turkish text normalization tools for natural language processing.

This package provides tools for normalizing Turkish text, including:
- Converting numbers to their text representation
- Converting ordinal numbers to their text representation
- Converting Roman numerals to Arabic numbers and normalizing Roman ordinals
- Converting special symbols (like %) to their text representation
- Adding Turkish suffixes to words (ile, ise, iken)
- Various text utility functions for Turkish language processing
- Metrics for text similarity (WER, CER, Levenshtein distance)
- Legacy normalizer for backward compatibility
- Comprehensive normalizer that applies all normalization steps in order
- Utilities for handling dimensions and multiplication symbols
- Flexible transformer-based approach for customizable text normalization
"""

__version__ = "0.1.0"

from .num_to_text import NumberToTextConverter, convert_numbers_to_words_wrapper
from .ordinals import normalize_ordinals
from .roman_numerals import roman_to_arabic, is_roman_numeral, find_roman_ordinals
from .symbols import SymbolConverter, convert_symbols, default_converter, add_symbol_mapping
from .symbol_mappings import get_all_mappings, get_mapping, add_mapping
from .metrics import wer, cer, levenshtein_distance
from .legacy_normalizer import normalize_text, replace_hatted_characters, turkish_lower as legacy_turkish_lower
from .text_utils import (
    turkish_lower,
    turkish_upper,
    turkish_capitalize,
    is_turkish_upper,
    son_harf,
    sesli_ile_bitiyor,
    son_sesli_harf,
    son_sesli_harf_kalin,
    sapkasiz,
    ekle,
)
from .normalizer import TurkishNormalizer, normalize, default_normalizer
from .dimension_utils import preprocess_dimensions, normalize_dimensions
from .unit_utils import normalize_units
from .transformer import (
    Transformer,
    TransformerPipeline,
    transform,
    get_available_transformers,
    create_custom_transformer,
    register_transformer,
    AVAILABLE_TRANSFORMERS,
    DEFAULT_TRANSFORMER_PIPELINE,
)

__all__ = [
    "NumberToTextConverter",
    "convert_numbers_to_words_wrapper",
    "normalize_ordinals",
    "roman_to_arabic",
    "is_roman_numeral",
    "find_roman_ordinals",
    "SymbolConverter",
    "convert_symbols",
    "default_converter",
    "add_symbol_mapping",
    "get_all_mappings",
    "get_mapping",
    "add_mapping",
    "wer",
    "cer",
    "levenshtein_distance",
    "normalize_text",
    "replace_hatted_characters",
    "legacy_turkish_lower",
    "turkish_lower",
    "turkish_upper",
    "turkish_capitalize",
    "is_turkish_upper",
    "son_harf",
    "sesli_ile_bitiyor",
    "son_sesli_harf",
    "son_sesli_harf_kalin",
    "sapkasiz",
    "ekle",
    "TurkishNormalizer",
    "normalize",
    "default_normalizer",
    "preprocess_dimensions",
    "normalize_dimensions",
    "normalize_units",
    "Transformer",
    "TransformerPipeline",
    "transform",
    "get_available_transformers",
    "create_custom_transformer",
    "register_transformer",
    "AVAILABLE_TRANSFORMERS",
    "DEFAULT_TRANSFORMER_PIPELINE",
]
