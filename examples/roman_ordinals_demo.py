"""
Demonstration of Roman ordinals conversion in the Turkish text normalization pipeline.

This example shows how to use the normalize_ordinals function with the new
convert_roman_ordinals parameter to control whether Roman ordinals are converted
to their text representation or left as is.
"""

from trnorm.ordinals import normalize_ordinals
from trnorm import normalize
from trnorm.text_utils import turkish_lower, sapkasiz, remove_punctuation
from trnorm.apostrophe_handler import remove_apostrophes

# Example texts with Roman and Arabic ordinals
example_texts = [
    "II. Dünya Savaşı 1939'da başladı.",
    "V. Karl, Kutsal Roma İmparatoru'ydu.",
    "III. Selim Osmanlı padişahıydı.",
    "XVI. Louis Fransa kralıydı.",
    "I. Dünya Savaşı ve II. Dünya Savaşı arasında 21 yıl vardı.",
    "3. sınıf öğrencileri ve II. Dünya Savaşı hakkında 20. yüzyılın en önemli olaylarından biri olan V. büyük savaş.",
    "Roma rakamları I, V, X, L, C, D ve M harflerinden oluşur."
]

print("=" * 80)
print("ROMAN ORDINALS CONVERSION DEMO")
print("=" * 80)

# Demonstrate standalone normalize_ordinals function
print("\n1. Using normalize_ordinals function directly:")
print("-" * 50)

for text in example_texts:
    print(f"\nOriginal: {text}")
    
    # Default behavior (Roman ordinals conversion disabled)
    default_result = normalize_ordinals(text)
    print(f"Default (Roman ordinals disabled): {default_result}")
    
    # With Roman ordinals conversion enabled
    roman_enabled_result = normalize_ordinals(text, convert_roman_ordinals=True)
    print(f"With Roman ordinals enabled: {roman_enabled_result}")

# Demonstrate in a full normalization pipeline
print("\n\n2. Using in a normalization pipeline:")
print("-" * 50)

# Define two pipelines - one with Roman ordinals conversion and one without
default_pipeline = [
    normalize_ordinals,  # Default: Roman ordinals conversion disabled
    remove_apostrophes,
    sapkasiz,
    turkish_lower,
    remove_punctuation
]

roman_enabled_pipeline = [
    lambda text: normalize_ordinals(text, convert_roman_ordinals=True),  # Enable Roman ordinals conversion
    remove_apostrophes,
    sapkasiz,
    turkish_lower,
    remove_punctuation
]

for text in example_texts[:3]:  # Use just a few examples for brevity
    print(f"\nOriginal: {text}")
    
    # Apply default pipeline
    default_result = normalize(text, default_pipeline)
    print(f"Default pipeline: {default_result}")
    
    # Apply pipeline with Roman ordinals conversion
    roman_enabled_result = normalize(text, roman_enabled_pipeline)
    print(f"Pipeline with Roman ordinals: {roman_enabled_result}")

print("\n" + "=" * 80)
print("Demo completed!")
print("=" * 80)
