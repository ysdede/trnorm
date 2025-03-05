"""
Example script demonstrating the handling of numbers followed by commas.
"""
from trnorm import normalize

print("Turkish Number Sequence Normalization Examples")
print("=============================================\n")

print("Example 1: Basic number lists")
examples = [
    "1, 2, 3 sayıları ardışıktır.",
    "Toplantı 13, 14 ve 15 Mayıs tarihlerinde yapılacak.",
    "Sınavda 5, 8, 13, 21 sorularını çözemedim.",
    "Yıl 1923, 29 Ekim'de Cumhuriyet ilan edildi."
]

for example in examples:
    print(f"Original: {example}")
    normalized = normalize(example)
    print(f"Normalized: {normalized}")
    print()

print("Example 2: Numbers in quoted text")
examples = [
    'General Jukov, o günleri günlüğüne şu şekilde aktardı; "13, 14 ve 15 Eylül günleri, Stalingrad için çok zor günlerdi."',
    'Kitapta şöyle yazıyordu: "1, 2, 3... Haydi başlayalım!"',
    'Öğretmen, "23, 29, 31 ve 37 asal sayılardır," dedi.'
]

for example in examples:
    print(f"Original: {example}")
    normalized = normalize(example)
    print(f"Normalized: {normalized}")
    print()

print("Example 3: Comparing with and without normalization")
example = 'General Jukov, o günleri günlüğüne şu şekilde aktardı; "13, 14 ve 15 Eylül günleri, Stalingrad için çok zor günlerdi."'

print(f"Original: {example}")
print(f"With number normalization: {normalize(example)}")
print(f"Without number normalization: {normalize(example, apply_number_conversion=False)}")
print()

print("Example 4: Numbers with commas vs. decimal numbers")
examples = [
    "13, 14 ve 15 sayıları",  # Numbers with commas (list)
    "13,14 ve 15 sayıları",   # Decimal number and integer
]

for example in examples:
    print(f"Original: {example}")
    normalized = normalize(example)
    print(f"Normalized: {normalized}")
    print()
