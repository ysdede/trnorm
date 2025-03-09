"""
Test script for Roman ordinals conversion with the new optional parameter.
"""

from trnorm.ordinals import normalize_ordinals
from trnorm.roman_numerals import find_roman_ordinals

# Test sentences with Roman ordinals
test_sentences = [
    "V. Karl, Kutsal Roma İmparatoru'ydu.",
    "II. Dünya Savaşı 1939'da başladı.",
    "XVI. Louis Fransa kralıydı.",
    "III. Selim Osmanlı padişahıydı.",
    "I. Dünya Savaşı ve II. Dünya Savaşı arasında 21 yıl vardı."
]

print("Roman Ordinals Conversion Test")
print("=" * 80)
print("{:<50} {:<50}".format("Original", "With Roman Ordinals Disabled (Default)"))
print("-" * 100)

for sentence in test_sentences:
    # Test with default parameter (Roman ordinals disabled)
    processed_default = normalize_ordinals(sentence)
    print("{:<50} {:<50}".format(sentence, processed_default))

print("\n")
print("{:<50} {:<50}".format("Original", "With Roman Ordinals Enabled"))
print("-" * 100)

for sentence in test_sentences:
    # Test with Roman ordinals enabled
    processed_enabled = normalize_ordinals(sentence, convert_roman_ordinals=True)
    print("{:<50} {:<50}".format(sentence, processed_enabled))

print("\nTest completed!")
