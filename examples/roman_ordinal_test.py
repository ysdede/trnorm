"""
Test the updated Roman ordinal conversion with limited range.

This script demonstrates how the modified Roman ordinal pattern
only converts Roman numerals up to 49 (XLIX) and ignores single
letter initials like 'D.' in names.
"""

from trnorm import normalize
from trnorm.ordinals import normalize_ordinals

# Test cases with various Roman numerals and initials
test_cases = [
    # Common Roman numerals that should be converted
    "I. Dünya Savaşı",
    "II. Selim",
    "III. Ahmet",
    "IV. Murat",
    "V. Charles",
    "VI. Edward",
    "X. Yüzyıl",
    "XV. Louis",
    "XX. Yüzyıl",
    "XXX. Olimpiyat Oyunları",
    "XL. Yıldönümü",
    "XLIX. Bölüm",
    
    # Higher Roman numerals that should NOT be converted (above 49)
    "L. Yıldönümü",
    "C. Yıldönümü",
    "D. Yıldönümü",
    "M. Yıldönümü",
    
    # Names with initials that should NOT be converted
    "Mehmet D. bu konuda ne düşünüyor?",
    "Ali B. ve Ayşe C. toplantıya katıldı.",
    "Prof. Dr. Ahmet K. konferans verdi.",
    "Mustafa K. Atatürk",
    "John F. Kennedy"
]

print("=" * 80)
print("ROMAN ORDINAL CONVERSION TEST WITH LIMITED RANGE")
print("=" * 80)
print()

for case in test_cases:
    # Test with standard normalization (includes all converters)
    normalized = normalize(case)
    
    # Test with only ordinal normalization
    ordinal_only = normalize_ordinals(case, convert_roman_ordinals=True)
    
    print(f"Original:      {case}")
    print(f"Normalized:    {normalized}")
    print(f"Ordinals Only: {ordinal_only}")
    print("-" * 80)

print()
print("Test completed!")
print("=" * 80)
