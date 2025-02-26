"""
Demo script for the "iken" suffix in Turkish.

This script demonstrates the use of the "iken" suffix with various Turkish words.
The "iken" suffix is a conditional suffix that means "while" or "when" in English.

Examples:
- başlayacak + iken = başlayacakken (while starting)
- çalışıyor + iken = çalışıyorken (while working)
- evde + iken = evdeyken (while at home)
"""

from text_utils import ekle

# Examples of words with "iken" suffix
examples = [
    "başlayacak",
    "çalışıyor",
    "durgun",
    "okur",
    "olgun",
    "uyur",
    "yazar",
    "geliyor",
    "gülmüş",
    "öğretmen",
    "evde",
    "okulda",
    "okumakta",
    "yolda",
    "Dy",
    "S",
    "x",
    "AB"
]

print("Turkish 'iken' Suffix Examples:")
print("------------------------------")
print(f"{'Word':<15} {'With iken':<15}")
print(f"{'-'*15} {'-'*15}")

for word in examples:
    with_iken = ekle(word, "iken")
    print(f"{word:<15} {with_iken:<15}")

print("\nExplanation:")
print("The 'iken' suffix in Turkish is used to express 'while' or 'when' in English.")
print("It follows these rules:")
print("1. For words ending with a consonant, 'ken' is added directly.")
print("2. For words ending with a vowel, 'yken' is added.")
print("3. For abbreviations or short words (≤ 3 letters), 'iken' is kept separate.")
