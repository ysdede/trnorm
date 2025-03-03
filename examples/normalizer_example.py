"""
Example usage of the TurkishNormalizer class.

This script demonstrates how to use the TurkishNormalizer class to normalize Turkish text.
"""

import sys
import os

# Add the parent directory to the path to import the trnorm package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm import normalize, TurkishNormalizer

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

# Additional examples for dimension handling
dimension_examples = [
    "Odanın boyutları 2x3x4 metre.",
    "Halının boyutu 120x180cm.",
    "Masa 75x120x90cm ebatlarında.",
    "2x3metre halı",
    "5x10x15 boyutlarında kutu",
    "10x20 ebatlarında fotoğraf",
    "3x4x5x6 boyutlu hiperkutu"
]

# Examples for unit normalization
unit_examples = [
    "Masanın yüksekliği 75 cm.",
    "Ağırlığı 5 kg.",
    "Sıcaklık 25 °C.",
    "Uzunluğu 10 m, genişliği 5 m.",
    "Araba 120 km/h hızla gidiyor.",
    "Oda 20 m² büyüklüğünde.",
    "Su 100 °C'de kaynar.",
    "Laptop 1.5 kg ağırlığında ve 35 cm genişliğinde."
]

# List to store normalized results
normalized_results = []

print("Original texts:")
for i, text in enumerate(example_texts, 1):
    print(f"{i}. {text}")

print("\n" + "-" * 50 + "\n")

# Using the default normalizer
print("Using default normalizer:")
for i, text in enumerate(example_texts, 1):
    normalized = normalize(text)
    normalized_results.append(normalized)
    print(f"{i}. {normalized}")

print("\n" + "-" * 50 + "\n")

# Using a custom normalizer (no lowercase, no hat removal)
print("Using custom normalizer (no lowercase, no hat removal):")
custom_normalizer = TurkishNormalizer(lowercase=False, remove_hats=False)
for i, text in enumerate(example_texts, 1):
    normalized = custom_normalizer.normalize(text)
    print(f"{i}. {normalized}")

print("\n" + "-" * 50 + "\n")

# Using the convenience function with custom parameters
print("Using convenience function with custom parameters (legacy normalization):")
for i, text in enumerate(example_texts, 1):
    normalized = normalize(text, apply_legacy_normalization=True)
    print(f"{i}. {normalized}")

print("\n" + "-" * 50 + "\n")

# Processing a list of texts at once
print("Processing a list of texts at once:")
batch_normalized = normalize(example_texts)
for i, normalized in enumerate(batch_normalized, 1):
    print(f"{i}. {normalized}")

# Example of selective normalization
print("\n" + "-" * 50 + "\n")
print("Selective normalization (only numbers to text):")
numbers_only = TurkishNormalizer(
    apply_number_conversion=True,
    apply_ordinal_normalization=False,
    apply_symbol_conversion=False,
    apply_multiplication_symbol=False,
    lowercase=False,
    remove_hats=False
)
for i, text in enumerate(example_texts, 1):
    normalized = numbers_only.normalize(text)
    print(f"{i}. {normalized}")

# Showcase dimension handling
print("\n" + "-" * 50 + "\n")
print("Dimension handling examples:")
for i, text in enumerate(dimension_examples, 1):
    normalized = normalize(text)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")

# Showcase unit normalization
print("\n" + "-" * 50 + "\n")
print("Unit normalization examples:")
for i, text in enumerate(unit_examples, 1):
    normalized = normalize(text)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")

# Comparing with and without unit normalization
print("\n" + "-" * 50 + "\n")
print("Comparing with and without unit normalization:")
for i, text in enumerate(unit_examples[:4], 1):
    # With unit normalization (default)
    with_units = normalize(text)
    
    # Without unit normalization
    without_units = normalize(text, apply_unit_normalization=False)
    
    print(f"{i}. Original: {text}")
    print(f"   With unit norm: {with_units}")
    print(f"   Without unit norm: {without_units}")
    print("")

# Comparing old and new dimension handling
print("\n" + "-" * 50 + "\n")
print("Comparing old and new dimension handling:")

# Import the old function for comparison
from trnorm.num_to_text import replace_multiplication_symbol_in_dimensions

complex_dimensions = [
    "2x3x4metre",
    "120x180cm",
    "5x10x15x20",
    "3x4cm x 5x6cm"
]

for i, text in enumerate(complex_dimensions, 1):
    # Old method
    old_result = replace_multiplication_symbol_in_dimensions(text)
    
    # New method
    new_result = normalize(text)
    
    print(f"{i}. Original: {text}")
    print(f"   Old method: {old_result}")
    print(f"   New method: {new_result}")
    print("")
