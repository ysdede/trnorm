"""
Example usage of the transformer-based approach for Turkish text normalization.

This script demonstrates how to use the transformer-based approach to normalize Turkish text
with customizable transformer pipelines.
"""

import sys
import os

# Add the parent directory to the path to import the trnorm package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm import (
    transform,
    TransformerPipeline,
    get_available_transformers,
    create_custom_transformer,
    register_transformer,
    DEFAULT_TRANSFORMER_PIPELINE
)

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

# Print available transformers
print("Available transformers:")
for name, description in get_available_transformers().items():
    print(f"  - {name}: {description}")

print("\n" + "-" * 50 + "\n")

# Using the default transformer pipeline
print("Using default transformer pipeline:")
print(f"Default pipeline: {DEFAULT_TRANSFORMER_PIPELINE}")
for i, text in enumerate(example_texts[:3], 1):
    normalized = transform(text)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")
    print()

print("\n" + "-" * 50 + "\n")

# Using a custom transformer pipeline
print("Using custom transformer pipeline (only numbers and dimensions):")
custom_pipeline = ["preprocess_dimensions", "normalize_dimensions", "convert_numbers"]
for i, text in enumerate(mixed_examples[:2], 1):
    normalized = transform(text, transformers=custom_pipeline)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")
    print()

print("\n" + "-" * 50 + "\n")

# Creating a custom transformer pipeline with specific order
print("Creating a custom transformer pipeline with specific order:")
pipeline = TransformerPipeline([
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

# Creating and registering a custom transformer
print("Creating and registering a custom transformer:")

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

# Create and register the custom transformer
month_transformer = create_custom_transformer(
    name="replace_month_names",
    func=replace_turkish_month_names,
    description="Replace Turkish month names with their numeric representation"
)
register_transformer(month_transformer)

# Example text with month names
date_examples = [
    "5 Ocak 2023 tarihinde toplantı var.",
    "Nisan ayında tatile gideceğim.",
    "Ekim ve Kasım aylarında yağmur yağar."
]

# Create a pipeline with the custom transformer
custom_pipeline = TransformerPipeline([
    "replace_month_names",
    "convert_numbers",
    "lowercase"
])

for i, text in enumerate(date_examples, 1):
    normalized = custom_pipeline.apply(text)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")
    print()

print("\n" + "-" * 50 + "\n")

# Processing a list of texts at once
print("Processing a list of texts at once:")
batch_normalized = transform(example_texts)
for i, normalized in enumerate(batch_normalized, 1):
    print(f"{i}. {normalized}")

print("\n" + "-" * 50 + "\n")

# Comparing different transformer combinations
print("Comparing different transformer combinations:")

text = "Ürün boyutları 120x180cm ve fiyatı 1.250,75 TL'dir."
print(f"Original: {text}")

# Only dimension handling
dimension_only = transform(text, transformers=["preprocess_dimensions", "normalize_dimensions"])
print(f"Dimension only: {dimension_only}")

# Only number conversion
number_only = transform(text, transformers=["convert_numbers"])
print(f"Number only: {number_only}")

# Only unit normalization
unit_only = transform(text, transformers=["normalize_units"])
print(f"Unit only: {unit_only}")

# Full normalization
full_norm = transform(text)
print(f"Full normalization: {full_norm}")

# Custom order (different from default)
custom_order = transform(text, transformers=[
    "convert_numbers",
    "preprocess_dimensions",
    "normalize_dimensions",
    "normalize_units",
    "lowercase"
])
print(f"Custom order: {custom_order}")
