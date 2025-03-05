from trnorm import normalize

# Test with the specific example
text = "Ancak 13 Nisan 2024 akşamı saat 22.00 sularında, İran Devrim Muhafızları, İsrail'i hedef alarak devasa bir füze saldırısı başlattı."
print("Original text:")
print(text)
print("\nNormalized text (with time normalization):")
print(normalize(text))
print("\nNormalized text (without time normalization):")
print(normalize(text, apply_time_normalization=False))
