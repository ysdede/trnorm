"""
Example of using the basic Turkish text normalizer.

This example demonstrates how to use the simplified normalizer approach
with direct function references.
"""

import sys
import os

# Add the parent directory to the path to import the trnorm package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm import normalize
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.ordinals import normalize_ordinals
from trnorm.symbols import convert_symbols
from trnorm.legacy_normalizer import normalize_text, replace_hatted_characters, turkish_lower
from trnorm.dimension_utils import preprocess_dimensions, normalize_dimensions
from trnorm.unit_utils import normalize_units

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

print("Basic normalizer examples:\n")

# 1. Using a single converter
print("1. Using a single converter (numbers to text):")
for i, text in enumerate(example_texts[:2], 1):
    normalized = normalize(text, [convert_numbers_to_words_wrapper])
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")
    print()

print("\n" + "-" * 50 + "\n")

# 2. Combining multiple converters
print("2. Combining multiple converters (dimensions, numbers, lowercase):")
converters = [
    preprocess_dimensions,
    normalize_dimensions,
    convert_numbers_to_words_wrapper,
    turkish_lower
]

for i, text in enumerate(mixed_examples[:2], 1):
    normalized = normalize(text, converters)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")
    print()

print("\n" + "-" * 50 + "\n")

# 3. Creating different converter sets for different tasks
print("3. Creating different converter sets for different tasks:")

# Number and symbol conversion only
number_symbol_converters = [
    convert_symbols,
    convert_numbers_to_words_wrapper
]

# Full text normalization
full_normalization_converters = [
    preprocess_dimensions,
    convert_symbols,
    normalize_dimensions,
    convert_numbers_to_words_wrapper,
    normalize_ordinals,
    normalize_units,
    replace_hatted_characters,
    turkish_lower
]

# Legacy normalization (aggressive)
legacy_converters = [
    normalize_text
]

text = "Ürün boyutları 120x180cm ve fiyatı 1.250,75 TL'dir."
print(f"Original: {text}")

# Apply different converter sets
number_symbol_result = normalize(text, number_symbol_converters)
print(f"Number and symbol conversion: {number_symbol_result}")

full_result = normalize(text, full_normalization_converters)
print(f"Full normalization: {full_result}")

legacy_result = normalize(text, legacy_converters)
print(f"Legacy normalization: {legacy_result}")

print("\n" + "-" * 50 + "\n")

# 4. Processing a list of texts at once
print("4. Processing a list of texts at once:")
batch_normalized = normalize(example_texts, full_normalization_converters)
for i, normalized in enumerate(batch_normalized, 1):
    print(f"{i}. {normalized}")

print("\n" + "-" * 50 + "\n")

# 5. Creating a custom converter function
print("5. Creating a custom converter function:")

def replace_turkish_month_names(text):
    """Replace Turkish month names with their numeric representation."""
    month_mapping = {
        "ocak": "1",
        "şubat": "2",
        "mart": "3",
        "nisan": "4",
        "mayıs": "5",
        "haziran": "6",
        "temmuz": "7",
        "ağustos": "8",
        "eylül": "9",
        "ekim": "10",
        "kasım": "11",
        "aralık": "12"
    }
    
    result = text
    for month, number in month_mapping.items():
        result = result.replace(month, number)
        result = result.replace(month.capitalize(), number)
    
    return result

# Example text with month names
date_examples = [
    "5 Ocak 2023 tarihinde toplantı var.",
    "Nisan ayında tatile gideceğim.",
    "Ekim ve Kasım aylarında yağmur yağar."
]

# Create a custom converter list with the month converter
custom_converters = [
    replace_turkish_month_names,
    convert_numbers_to_words_wrapper,
    turkish_lower
]

for i, text in enumerate(date_examples, 1):
    normalized = normalize(text, custom_converters)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")
    print()
