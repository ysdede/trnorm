"""
Demo of Roman numeral functionality in the trnorm package.

This example demonstrates:
1. Converting Roman numerals to Arabic numbers
2. Checking if a string is a valid Roman numeral
3. Normalizing Roman ordinals in Turkish text
"""

from trnorm import roman_to_arabic, is_roman_numeral, normalize_ordinals


def demo_roman_to_arabic():
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


def demo_is_roman_numeral():
    """Demonstrate checking if a string is a valid Roman numeral."""
    print("\n=== Roman Numeral Validation ===")
    
    examples = [
        "I", "V", "X", "XIV", "MCMXCIX",  # Valid
        "IIII", "VV", "ABC", "123"        # Invalid
    ]
    
    print(f"{'String':<10} {'Valid?':<10}")
    print("-" * 20)
    
    for string in examples:
        valid = is_roman_numeral(string)
        print(f"{string:<10} {str(valid):<10}")


def demo_roman_ordinals():
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
    """Run all demonstrations."""
    print("=== Roman Numerals Demo ===")
    print("This demo shows the Roman numeral functionality in the trnorm package.")
    
    demo_roman_to_arabic()
    demo_is_roman_numeral()
    demo_roman_ordinals()
    
    print("\nDemo completed!")


if __name__ == "__main__":
    main()
