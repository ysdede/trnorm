"""
Example demonstrating the handling of separator characters in the punctuation removal function.

This example shows how separator characters like hyphens and slashes are 
replaced with spaces instead of being removed.
"""

from trnorm.text_utils import remove_punctuation

# Test sentences with various separator characters
test_sentences = [
    # Hyphen as separator
    "İstanbul-Ankara arası 450 kilometre.",
    "2023-2024 eğitim-öğretim yılı başladı.",
    "Türk-İslam eserleri sergisi açıldı.",
    
    # Slash as separator
    "Kadın/Erkek eşitliği önemlidir.",
    "01/01/2023 tarihinde başlayacak.",
    "A/B testinin sonuçları açıklandı.",
    
    # Pipe as separator
    "Elma|Armut|Kiraz|Çilek",
    "Kategori|Alt Kategori|Ürün",
    
    # Mixed separators
    "İstanbul-Ankara/İzmir güzergahı",
    "Pazartesi-Salı/Çarşamba-Perşembe",
    "Yazılım/Donanım-Ağ/Güvenlik bölümleri",
    
    # Separators with other punctuation
    "İstanbul'dan-Ankara'ya yolculuk.",
    "Web 2.0/3.0 teknolojileri.",
    "A-B-C/D-E-F sıralaması."
]

# Process all test sentences
print("Separator Character Handling Test")
print("=" * 80)
print("{:<60} {:<60}".format("Original", "Processed"))
print("-" * 120)

for sentence in test_sentences:
    processed = remove_punctuation(sentence)
    print("{:<60} {:<60}".format(sentence, processed))

print("\nTest completed!")
