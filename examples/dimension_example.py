"""
Example script demonstrating dimension and unit normalization in Turkish text.

This script shows how the trnorm package handles dimensions and unit abbreviations
in Turkish text.
"""

import sys
import os

# Add the parent directory to the path to import the trnorm package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm import normalize

# Example texts with dimensions and units
examples = [
    # Basic dimensions
    "2x3",
    "2x3x4",
    
    # Dimensions with units
    "2x3cm",
    "120x180cm",
    
    # Basic units
    "5kg",
    "10mm",
    
    # Units with spaces
    "5 kg",
    "10 mm",
    
    # Units with periods
    "5kg.",
    "10mm.",
    
    # Units with spaces and periods
    "5 kg.",
    "10 mm.",
    
    # Dimensions and units in sentences
    "Odanın boyutları 2x3 metre.",
    "Halının boyutu 120x180cm.",
    "Bu masanın ölçüleri 75x120x90cm.",
    
    # Regular 'x' in text (not dimensions)
    "matematikte bilinmeyene x denmesinin sebebi",
    "x ve y eksenleri",
    "Masa 2x3 metre ve x ekseni",
    
    # Units in sentences (with and without spaces)
    "Masa 75 cm yüksekliğindedir.",
    "Masa 75cm yüksekliğindedir.",
    "Ağırlığı 5 kg.",
    "Ağırlığı 5kg.",
    "Sıcaklık 25 °C.",
    "Sıcaklık 25°C.",
    "Uzunluğu 10 m, genişliği 5 m.",
    "Uzunluğu 10m, genişliği 5m.",
    
    # Multiple units with periods in the same sentence
    "Ağırlığı 5 kg. ve uzunluğu 10 metre.",
    "Ağırlığı 5kg. ve uzunluğu 10m."
]

print("Dimension and Unit Normalization Examples:")
print("=" * 50)

# Normalize and print each example
for example in examples:
    normalized = normalize(example)
    print(f"Original: {example}")
    print(f"Normalized: {normalized}")
    print("-" * 50)

# Show examples without unit normalization
print("\nWithout Unit Normalization:")
print("=" * 50)

examples_without_unit_norm = [
    "2x3cm",
    "Masa 75 cm yüksekliğindedir.",
    "Masa 75cm yüksekliğindedir.",
    "Ağırlığı 5 kg. ve uzunluğu 10 m."
]

for example in examples_without_unit_norm:
    normalized = normalize(example, apply_unit_normalization=False)
    print(f"Original: {example}")
    print(f"Normalized (no unit norm): {normalized}")
    print("-" * 50)
