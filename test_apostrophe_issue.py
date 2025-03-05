"""
Test script to investigate the issue with apostrophes in text normalization.
"""
from trnorm import normalize
from trnorm.legacy_normalizer import normalize_text
from trnorm.metrics import wer, cer

# The example text with the issue
ref = "GoPro Osmo Action'dan daha çok sevdiğim GoPro 7 bu sırada, 8'i almadım, niye almadım?"
hyp = "GoPro. Osmo Action'dan daha çok sevdiğim. GoPro 7 bu sırada. 8'i almadım. Niye almadım?"

print("Original Reference:")
print(ref)
print("\nOriginal Hypothesis:")
print(hyp)

# Test with the current normalization
print("\n--- With Current Normalization ---")
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

# Test with legacy normalization
print("\n--- With Legacy Normalization ---")
legacy_norm_ref = normalize_text(ref)
legacy_norm_hyp = normalize_text(hyp)

print("\nLegacy Normalized Reference:")
print(legacy_norm_ref)
print("\nLegacy Normalized Hypothesis:")
print(legacy_norm_hyp)

legacy_wer_score = wer(legacy_norm_ref, legacy_norm_hyp)
legacy_cer_score = cer(legacy_norm_ref, legacy_norm_hyp)
print(f"\nLegacy WER: {legacy_wer_score:.4f} ({legacy_wer_score*100:.2f}%)")
print(f"Legacy CER: {legacy_cer_score:.4f} ({legacy_cer_score*100:.2f}%)")

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
    current_norm = normalize(case)
    legacy_norm = normalize_text(case)
    print(f"Current normalization: {current_norm}")
    print(f"Legacy normalization: {legacy_norm}")

# Test with custom apostrophe handling
print("\n--- Testing Custom Apostrophe Handling ---")

def custom_normalize(text):
    """Apply normalization with custom apostrophe handling."""
    # First convert numbers to text
    result = normalize(text)
    
    # Then handle apostrophes like in legacy normalizer
    result = result.replace(" '", " ").replace("' ", " ").replace("'", "")
    result = result.replace(' "', ' ').replace('" ', ' ').replace('"', '')
    
    return result

for case in test_cases:
    print(f"\nOriginal: {case}")
    custom_norm = custom_normalize(case)
    print(f"Custom normalization: {custom_norm}")

# Test the user's example with custom normalization
print("\n--- User Example with Custom Normalization ---")
custom_norm_ref = custom_normalize(ref)
custom_norm_hyp = custom_normalize(hyp)

print("\nCustom Normalized Reference:")
print(custom_norm_ref)
print("\nCustom Normalized Hypothesis:")
print(custom_norm_hyp)

custom_wer_score = wer(custom_norm_ref, custom_norm_hyp)
custom_cer_score = cer(custom_norm_ref, custom_norm_hyp)
print(f"\nCustom WER: {custom_wer_score:.4f} ({custom_wer_score*100:.2f}%)")
print(f"Custom CER: {custom_cer_score:.4f} ({custom_cer_score*100:.2f}%)")

# Format the output in the debugging data format
print("\n--- Debugging Data Format ---")
print(f"{wer_score*100:.2f}/{legacy_wer_score*100:.2f} - {cer_score*100:.2f}/{legacy_cer_score*100:.2f}")
print(ref)
print(hyp)
print(norm_ref)
print(norm_hyp)
