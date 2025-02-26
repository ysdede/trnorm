"""
Turkish text normalization tools for natural language processing.

This package provides tools for normalizing Turkish text, including:
- Converting numbers to their text representation
- Converting ordinal numbers to their text representation
- Adding Turkish suffixes to words (ile, ise, iken)
- Various text utility functions for Turkish language processing
"""

__version__ = "0.1.0"

from .num_to_text import NumberToTextConverter, convert_numbers_to_words_wrapper
from .ordinals import normalize_ordinals
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

__all__ = [
    "NumberToTextConverter",
    "convert_numbers_to_words_wrapper",
    "normalize_ordinals",
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
]
