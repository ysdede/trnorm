from ordinals import normalize_ordinals

# Sample text with various ordinal formats
sample_text = """
1. sınıf öğrencileri
2'nci katta oturuyorlar
3üncü sırada bekleyin
4. ve 5'inci arasında bir yerde
10uncu yıl marşı
21. yüzyılda yaşıyoruz
42'inci paralel
"""

# Normalize the text
normalized_text = normalize_ordinals(sample_text)

# Print the original and normalized text side by side
print("Original Text:")
print("-" * 40)
print(sample_text)
print("\nNormalized Text:")
print("-" * 40)
print(normalized_text)
