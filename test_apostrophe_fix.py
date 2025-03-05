"""
Test script to verify the apostrophe handling functionality.
"""
from trnorm import normalize
from trnorm.metrics import wer, cer

# The example text with the issue
ref = "GoPro Osmo Action'dan daha çok sevdiğim GoPro 7 bu sırada, 8'i almadım, niye almadım?"
hyp = "GoPro. Osmo Action'dan daha çok sevdiğim. GoPro 7 bu sırada. 8'i almadım. Niye almadım?"

print("Original Reference:")
print(ref)
print("\nOriginal Hypothesis:")
print(hyp)

# Test with the standard normalization
print("\n--- With Standard Normalization ---")
norm_ref = normalize(ref)
norm_hyp = normalize(hyp)

print("\nNormalized Reference:")
print(norm_ref)
print("\nNormalized Hypothesis:")
print(norm_hyp)

wer_score = wer(norm_ref, norm_hyp)
cer_score = cer(norm_ref, norm_hyp)
print(f"\nWER: {wer_score:.4f} ({wer_score*100:.2f}%)")
print(f"CER: {cer_score:.4f} ({cer_score*100:.2f}%)")

# Test with apostrophe handling enabled
print("\n--- With Apostrophe Handling Enabled ---")
apo_norm_ref = normalize(ref, apply_apostrophe_handling=True)
apo_norm_hyp = normalize(hyp, apply_apostrophe_handling=True)

print("\nApostrophe-Handled Reference:")
print(apo_norm_ref)
print("\nApostrophe-Handled Hypothesis:")
print(apo_norm_hyp)

apo_wer_score = wer(apo_norm_ref, apo_norm_hyp)
apo_cer_score = cer(apo_norm_ref, apo_norm_hyp)
print(f"\nApostrophe-Handled WER: {apo_wer_score:.4f} ({apo_wer_score*100:.2f}%)")
print(f"Apostrophe-Handled CER: {apo_cer_score:.4f} ({apo_cer_score*100:.2f}%)")

# Test specific apostrophe cases
print("\n--- Testing Specific Apostrophe Cases ---")
test_cases = [
    "8'i almadım",
    "Kitap'ı okudum",
    "Ahmet'in arabası",
    "İstanbul'da yaşıyorum",
    "GoPro 7'yi kullanıyorum"
]

for case in test_cases:
    print(f"\nOriginal: {case}")
    standard_norm = normalize(case)
    apo_norm = normalize(case, apply_apostrophe_handling=True)
    print(f"Standard normalization: {standard_norm}")
    print(f"With apostrophe handling: {apo_norm}")

# Format the output in the debugging data format
print("\n--- Debugging Data Format ---")
print(f"{wer_score*100:.2f}/{apo_wer_score*100:.2f} - {cer_score*100:.2f}/{apo_cer_score*100:.2f}")
print(ref)
print(hyp)
print(norm_ref)
print(norm_hyp)
print(apo_norm_ref)
print(apo_norm_hyp)
