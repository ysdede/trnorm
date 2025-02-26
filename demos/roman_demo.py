"""
Demo script for Roman numeral conversion and Roman ordinals normalization.

This script demonstrates:
1. Converting Roman numerals to Arabic numbers
2. Normalizing Roman ordinals in Turkish text
"""

import sys
import os

# Add the parent directory to the path to import trnorm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm.roman_numerals import roman_to_arabic, is_roman_numeral
from trnorm.ordinals import normalize_ordinals


def demonstrate_roman_to_arabic():
    """Demonstrate conversion of Roman numerals to Arabic numbers."""
    print("\n=== Roman to Arabic Conversion ===")
    examples = [
        "I", "IV", "V", "IX", "X", "XIV", "XIX", "XX", 
        "XL", "L", "XC", "C", "CD", "D", "CM", "M", 
        "MCMXCIX", "MMXXIV"
    ]
    
    print(f"{'Roman':<10} {'Arabic':<10}")
    print("-" * 20)
    
    for roman in examples:
        try:
            arabic = roman_to_arabic(roman)
            print(f"{roman:<10} {arabic:<10}")
        except ValueError as e:
            print(f"{roman:<10} Error: {e}")


def demonstrate_roman_ordinals():
    """Demonstrate normalization of Roman ordinals in Turkish text."""
    print("\n=== Roman Ordinals Normalization ===")
    examples = [
        "II. Dünya Savaşı başladı.",
        "XX. yüzyılda teknoloji hızla gelişti.",
        "III. Selim, Osmanlı padişahıydı.",
        "XIV. Louis, Fransa kralıydı.",
        "II. Wilhelm, Almanya imparatoruydu.",
        "V. Karl, Kutsal Roma İmparatoru'ydu.",
        "VIII. Edward, İngiltere kralıydı.",
        "I. Dünya Savaşı'ndan sonra II. Dünya Savaşı başladı.",
        "XIX. yüzyıldan XX. yüzyıla geçiş süreci.",
        "3. sınıf öğrencileri ve II. Dünya Savaşı hakkında 20. yüzyılın en önemli olaylarından biri olan V. büyük savaş."
    ]
    
    for text in examples:
        normalized = normalize_ordinals(text)
        print(f"\nOriginal: {text}")
        print(f"Normalized: {normalized}")


def main():
    """Main function to run the demonstrations."""
    print("=== Roman Numerals and Ordinals Demo ===")
    
    demonstrate_roman_to_arabic()
    demonstrate_roman_ordinals()
    
    print("\nDemo completed.")


if __name__ == "__main__":
    main()
