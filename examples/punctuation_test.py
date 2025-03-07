"""
Example demonstrating the punctuation removal functionality.

This example shows how various types of punctuation marks are removed
from Turkish text using the remove_punctuation function.
"""

from trnorm.text_utils import remove_punctuation

# Test sentences with various punctuation marks
test_sentences = [
    # Standard punctuation
    "Merhaba, dünya! Nasılsın?",
    "Bu bir test cümlesidir; noktalama işaretlerini test ediyoruz.",
    "Yarın (Pazartesi) toplantımız var.",
    
    # Quotes and apostrophes
    "Ali'nin kitabı \"Yaz Günü\" çok güzel.",
    "İstanbul'un tarihi yerleri çok etkileyici.",
    "Bu 'özel' bir durum.",
    
    # Special characters and dashes
    "Ankara—İstanbul arası 450 km'dir.",
    "1990–2000 yılları arasında yaşanan olaylar…",
    "A–B–C sırasıyla ilerleyin.",
    
    # Various apostrophe types
    "Ali'nin Ali'nin Ali`nin Ali´nin Aliʹnin Aliʻnin Aliʼnin Aliʽnin Aliʿnin Aliˈnin",
    
    # Percentage and special symbols
    "Enflasyon %10 arttı.",
    "A+B=C formülü matematiksel bir ifadedir.",
    
    # Mixed punctuation
    "Prof. Dr. Ahmet Yılmaz'ın \"Türk Dili Tarihi\" adlı kitabı—ki bu kitap üniversitelerde ders kitabı olarak okutulmaktadır—çok değerli bilgiler içerir.",
]

# Process all test sentences
print("Punctuation Removal Test")
print("=" * 80)
print("{:<60} {:<60}".format("Original", "Processed"))
print("-" * 120)

for sentence in test_sentences:
    processed = remove_punctuation(sentence)
    print("{:<60} {:<60}".format(sentence, processed))

print("\nTest completed!")
