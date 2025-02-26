"""
Demo script for text_utils.py functionality.
This script demonstrates various Turkish text utilities.
"""

from trnorm.text_utils import (
    turkish_lower,
    turkish_upper,
    turkish_capitalize,
    is_turkish_upper,
    son_harf,
    sesli_ile_bitiyor,
    son_sesli_harf,
    son_sesli_harf_kalin,
    sapkasiz
)


def print_section(title):
    """Print a section title with decorative lines."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def demo_case_conversion():
    """Demonstrate Turkish case conversion functions."""
    print_section("Turkish Case Conversion")
    
    test_words = [
        "İstanbul", "ANKARA", "izmir", "ığdır", "IĞDIR",
        "Çanakkale", "ŞANLIURFA", "öğrenci", "ÖĞRENCİ"
    ]
    
    print("Original\t\tLowercase\t\tUppercase\t\tCapitalized")
    print("-" * 60)
    
    for word in test_words:
        lowercase = turkish_lower(word)
        uppercase = turkish_upper(word)
        capitalized = turkish_capitalize(lowercase)
        
        print(f"{word:<16}\t{lowercase:<16}\t{uppercase:<16}\t{capitalized:<16}")


def demo_is_turkish_upper():
    """Demonstrate is_turkish_upper function."""
    print_section("Turkish Uppercase Check")
    
    test_words = [
        "İSTANBUL", "Ankara", "izmir", "IĞDIR", "ÖĞRENCİ",
        "ÇANAKKALE", "şanlıurfa", "İstanbul", ""
    ]
    
    print("Word\t\t\tIs Uppercase?")
    print("-" * 40)
    
    for word in test_words:
        is_upper = is_turkish_upper(word)
        print(f"{word:<20}\t{is_upper}")


def demo_vowel_functions():
    """Demonstrate vowel-related functions."""
    print_section("Vowel-Related Functions")
    
    test_words = [
        "kitap", "kalem", "araba", "öğrenci",
        "İstanbul", "Ankara", "köprü", "kağıt"
    ]
    
    print("Word\t\tLast Letter\tEnds with Vowel?\tLast Vowel\tHas Back Vowel?")
    print("-" * 80)
    
    for word in test_words:
        last_letter = son_harf(word)
        ends_with_vowel = sesli_ile_bitiyor(word)
        last_vowel = son_sesli_harf(word) or "None"
        
        try:
            is_back_vowel = son_sesli_harf_kalin(word)
        except AttributeError:
            is_back_vowel = "N/A"
        
        print(f"{word:<12}\t{last_letter:<8}\t{ends_with_vowel!s:<16}\t{last_vowel:<8}\t{is_back_vowel!s}")


def demo_sapkasiz():
    """Demonstrate sapkasiz function."""
    print_section("Remove Accents (Sapkasiz)")
    
    test_words = [
        "kâğıt", "Âdem", "îman", "Îman", "hûr", "Hûr",
        "Âlî Bâbâ", "kâtip", "Îstanbul"
    ]
    
    print("Original\t\tWithout Accents")
    print("-" * 40)
    
    for word in test_words:
        without_accents = sapkasiz(word)
        print(f"{word:<20}\t{without_accents}")


def main():
    """Run all demos."""
    print("\nTurkish Text Utilities Demo")
    print("==========================\n")
    
    demo_case_conversion()
    demo_is_turkish_upper()
    demo_vowel_functions()
    demo_sapkasiz()
    
    print("\nDemo completed.\n")


if __name__ == "__main__":
    main()
