"""
Example of using the simplified Turkish text normalizer.

This example demonstrates how to use the new simplified normalizer approach
with customizable transformers.
"""

import sys
import os

# Add the parent directory to the path to import the trnorm package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm import normalize
from trnorm.legacy_normalizer import normalize_text, replace_hatted_characters, turkish_lower
from trnorm.dimension_utils import preprocess_dimensions, normalize_dimensions
from trnorm.unit_utils import normalize_units
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.ordinals import normalize_ordinals
from trnorm.symbols import convert_symbols

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

# Print available normalizers
print("Available normalizers:")
for name, description in get_available_normalizers().items():
    print(f"  - {name}: {description}")

print("\n" + "-" * 50 + "\n")

# Using the default normalizer
print("Using default normalizer:")
for i, text in enumerate(example_texts[:3], 1):
    normalized = normalize(text)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")
    print()

print("\n" + "-" * 50 + "\n")

# Using a custom list of transformers
print("Using custom transformers (only numbers and dimensions):")
custom_transformers = ["preprocess_dimensions", "normalize_dimensions", "convert_numbers"]
for i, text in enumerate(mixed_examples[:2], 1):
    normalized = normalize(text, transformers=custom_transformers)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")
    print()

print("\n" + "-" * 50 + "\n")

# Creating a reusable normalizer pipeline
print("Creating a reusable normalizer pipeline:")
pipeline = create_normalizer_pipeline([
    "preprocess_dimensions",
    "normalize_dimensions",
    "convert_numbers",
    "normalize_units",
    "lowercase"
])

for i, text in enumerate(mixed_examples, 1):
    normalized = pipeline.apply(text)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")
    print()

print("\n" + "-" * 50 + "\n")

# Using the legacy normalizer
print("Using legacy normalizer:")
legacy_transformers = ["legacy_normalize"]
text = "Bugün, 15. kattaki 3 toplantıya katıldım!"
normalized = normalize(text, transformers=legacy_transformers)
print(f"Original: {text}")
print(f"Normalized: {normalized}")

print("\n" + "-" * 50 + "\n")

# Processing a list of texts at once
print("Processing a list of texts at once:")
batch_normalized = normalize(example_texts)
for i, normalized in enumerate(batch_normalized, 1):
    print(f"{i}. {normalized}")

print("\n" + "-" * 50 + "\n")

# Comparing different transformer combinations
print("Comparing different transformer combinations:")

text = "Ürün boyutları 120x180cm ve fiyatı 1.250,75 TL'dir."
print(f"Original: {text}")

# Only dimension handling
dimension_only = normalize(text, transformers=["preprocess_dimensions", "normalize_dimensions"])
print(f"Dimension only: {dimension_only}")

# Only number conversion
number_only = normalize(text, transformers=["convert_numbers"])
print(f"Number only: {number_only}")

# Only unit normalization
unit_only = normalize(text, transformers=["normalize_units"])
print(f"Unit only: {unit_only}")

# Full normalization
full_norm = normalize(text)
print(f"Full normalization: {full_norm}")
