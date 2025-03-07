"""
Example of using the simplified Turkish text normalizer.

This example demonstrates how to use the new simplified normalizer approach
with customizable converters.
"""

import sys
import os

# Add the parent directory to the path to import the trnorm package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm import normalize
from trnorm.dimension_utils import preprocess_dimensions, normalize_dimensions
from trnorm.unit_utils import normalize_units
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.ordinals import normalize_ordinals
from trnorm.symbols import convert_symbols
from trnorm.legacy_normalizer import turkish_lower

# Example texts with various normalization needs
example_texts = [
    "Bugün 15. kattaki 3 toplantıya katıldım.",
    "Saat 14:30'da %25 indirimli ürünler satışa çıkacak.",
    "II. Dünya Savaşı 1939-1945 yılları arasında gerçekleşti.",
    "Ürün fiyatı 1.250,75 TL'dir.",
    "1. sınıfta 23 öğrenci var.",
    "Dün 3x4 metre halı aldım.",
    "Âlim insanlar bilgilerini paylaşır.",
]

# Examples for dimension and unit handling
mixed_examples = [
    "Odanın boyutları 2x3x4 metre.",
    "Halının boyutu 120x180cm.",
    "Ağırlığı 5 kg. ve uzunluğu 10 metre.",
    "Sıcaklık 25 °C ve nem %60.",
]

# Basic normalization example
print("Basic normalization example:")
basic_converters = [
    convert_numbers_to_words_wrapper,
    turkish_lower
]

for text in example_texts[:3]:
    print(f"\nOriginal: {text}")
    normalized = normalize(text, basic_converters)
    print(f"Normalized: {normalized}")

# Dimension and unit handling example
print("\nDimension and unit handling example:")
dimension_converters = [
    preprocess_dimensions,
    normalize_dimensions,
    normalize_units,
    convert_numbers_to_words_wrapper,
    turkish_lower
]

for text in mixed_examples[:2]:
    print(f"\nOriginal: {text}")
    normalized = normalize(text, dimension_converters)
    print(f"Normalized: {normalized}")

# Full normalization example
print("\nFull normalization example:")
full_converters = [
    preprocess_dimensions,
    normalize_dimensions,
    normalize_units,
    convert_numbers_to_words_wrapper,
    convert_symbols,
    normalize_ordinals,
    turkish_lower
]

for text in example_texts[3:]:
    print(f"\nOriginal: {text}")
    normalized = normalize(text, full_converters)
    print(f"Normalized: {normalized}")

# Batch processing example
print("\nBatch processing example:")
batch_normalized = normalize(example_texts, basic_converters)
for i, normalized in enumerate(batch_normalized, 1):
    print(f"{i}. {normalized}")

# Custom converter combinations
print("\nCustom converter combinations:")
text = "Ürün boyutları 120x180cm ve fiyatı 1.250,75 TL'dir."
print(f"\nOriginal: {text}")

# Only dimension handling
dimension_only = normalize(text, [preprocess_dimensions, normalize_dimensions])
print(f"Dimension only: {dimension_only}")

# Only number conversion
number_only = normalize(text, [convert_numbers_to_words_wrapper])
print(f"Number only: {number_only}")

# Only unit normalization
unit_only = normalize(text, [normalize_units])
print(f"Unit only: {unit_only}")

# Full normalization
full_norm = normalize(text, full_converters)
print(f"Full normalization: {full_norm}")