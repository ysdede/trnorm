"""
Demo script for ordinals normalization.
This script demonstrates the normalization of Turkish ordinals in various formats.
"""

from trnorm.ordinals import normalize_ordinals


def main():
    """Run the demo."""
    # Original text with various ordinal formats
    original_text = """
# Ordinals with lowercase letters (should be converted):
1. sınıf öğrencileri
2'nci katta oturuyorlar
3üncü sırada bekleyin
4. ve 5'inci arasında bir yerde
10uncu yıl marşı
21. yüzyılda yaşıyoruz
42'inci paralel

# Bullet points with uppercase letters (should be preserved):
1. Sabah kahvaltısı
2. Yürüyüş
3. Öğle yemeği
4. İş toplantısı

# Mixed examples:
1. birinci madde açıklaması (lowercase b - should be converted)
2. İkinci madde (capital İ - should be preserved)
3. üçüncü madde (lowercase ü - should be converted)

# Big numbers:
99. günde
103. sırada
2000. saniye
19857. aday
"""

    # Normalize the text
    normalized_text = normalize_ordinals(original_text)

    # Print the original and normalized text
    print("Original Text:")
    print("------------------------------------------------------------")
    print(original_text)
    print("\nNormalized Text:")
    print("------------------------------------------------------------")
    print(normalized_text)


if __name__ == "__main__":
    main()
