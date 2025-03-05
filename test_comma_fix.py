"""
Test script to verify the fix for numbers followed by commas.
"""
from trnorm import normalize
from trnorm.metrics import wer, cer

# The example text with the issue
ref = 'General Jukov, o günleri günlüğüne şu şekilde aktardı; "13, 14 ve 15 Eylül günleri, Stalingrad için çok zor günlerdi.'
hyp = 'General Yukov o günleri günlüğüne şu şekilde aktardı. 13, 14 ve 15 Eylül günleri Stalingrad için çok zor günlerdi.'

print("Original Reference:")
print(ref)
print("\nOriginal Hypothesis:")
print(hyp)

# Test with the fixed normalization
norm_ref = normalize(ref)
norm_hyp = normalize(hyp)

print("\nNormalized Reference:")
print(norm_ref)
print("\nNormalized Hypothesis:")
print(norm_hyp)

# Calculate WER and CER
wer_score = wer(norm_ref, norm_hyp)
cer_score = cer(norm_ref, norm_hyp)
print(f"\nWER: {wer_score:.4f} ({wer_score*100:.2f}%)")
print(f"CER: {cer_score:.4f} ({cer_score*100:.2f}%)")

# Test additional examples with numbers followed by commas
examples = [
    "1, 2, 3 sayıları ardışıktır.",
    "Toplantı 13, 14 ve 15 Mayıs tarihlerinde yapılacak.",
    "Sınavda 5, 8, 13, 21 sorularını çözemedim.",
    "Yıl 1923, 29 Ekim'de Cumhuriyet ilan edildi."
]

print("\n--- Additional Examples ---")
for example in examples:
    print(f"\nOriginal: {example}")
    normalized = normalize(example)
    print(f"Normalized: {normalized}")

# Test the specific case that was problematic
specific = '"13, 14 ve 15 Eylül günleri'
print(f"\n\nSpecific test case: {specific}")
normalized = normalize(specific)
print(f"Normalized: {normalized}")

# Direct test of the number converter
from trnorm.num_to_text import NumberToTextConverter
converter = NumberToTextConverter()
test = "13, 14 ve 15"
print(f"\nDirect conversion test: {test}")
result = converter.convert_numbers_to_words(test)
print(f"Result: {result}")
