"""
Demo script for the legacy normalizer.
This script demonstrates how to use the legacy normalizer for Turkish text.
"""

from trnorm.legacy_normalizer import normalize_text, replace_hatted_characters

# Example 1: Basic normalization with hatted characters
text1 = "âîôû Çok iyi ve nazik biriydi. Prusya'daki ilk karşılaşmamızda onu konuşturmayı başarmıştım. Bana o yaz North Cape'de bulunduğunu ve Nijni Novgorod panayırına gitmeyi çok istediğini anlatmıştı.,;)([-*])"
print("Original text:")
print(text1)
print("\nNormalized text:")
print(normalize_text(text1))
print("\nOnly hatted characters replaced:")
print(replace_hatted_characters(text1))

# Example 2: Handling quotes
print("\n--- Handling quotes ---")
text2 = "Turner'ın 'Köle Gemisi' isimli tablosuna bakıyoruz."
text3 = "Turner'ın Köle Gemisi isimli tablosuna bakıyoruz."
print("With quotes:", normalize_text(text2))
print("Without quotes:", normalize_text(text3))

# Example 3: Processing a list of texts
print("\n--- Processing a list of texts ---")
list_text = [
    """Turner"ın "Köle Gemisi"isimli tablosuna bakıyoruz.""",
    """Turner"ın Köle Gemisi isimli tablosuna bakıyoruz.""",
    "Turner'ın (Köle Gemisi) isimli tablosuna bakıyoruz.",
    "Turner'ın Köle Gemisi isimli tablosuna bakıyoruz."
]
print("Original list:")
for item in list_text:
    print(f"  - {item}")
print("\nNormalized list:")
normalized_list = normalize_text(list_text)
for item in normalized_list:
    print(f"  - {item}")
