"""
Test script to verify the fix for the user's specific example.
"""
from trnorm import normalize
from trnorm.metrics import wer, cer

# The user's example
ref = "Ancak 13 Nisan 2024 akşamı saat 22.00 sularında, İran Devrim Muhafızları, İsrail'i hedef alarak devasa bir füze saldırısı başlattı."
hyp = "Ancak 13 Nisan 2024 akşamı saat 22 sularında İran devrim muhafızları İsrail'i hedef alarak devasa bir füze saldırısı başlattı."

print("Original Reference:")
print(ref)
print("\nOriginal Hypothesis:")
print(hyp)

# Test with the old behavior (simulated by disabling time normalization)
print("\n--- Without Time Normalization ---")
norm_ref_without = normalize(ref, apply_time_normalization=False)
norm_hyp_without = normalize(hyp, apply_time_normalization=False)

print("\nNormalized Reference (without time normalization):")
print(norm_ref_without)
print("\nNormalized Hypothesis (without time normalization):")
print(norm_hyp_without)

wer_score_without = wer(norm_ref_without, norm_hyp_without)
cer_score_without = cer(norm_ref_without, norm_hyp_without)
print(f"\nWER: {wer_score_without:.4f} ({wer_score_without*100:.2f}%)")
print(f"CER: {cer_score_without:.4f} ({cer_score_without*100:.2f}%)")

# Test with the new behavior
print("\n--- With Time Normalization (New Behavior) ---")
norm_ref_with = normalize(ref)
norm_hyp_with = normalize(hyp)

print("\nNormalized Reference (with time normalization):")
print(norm_ref_with)
print("\nNormalized Hypothesis (with time normalization):")
print(norm_hyp_with)

wer_score_with = wer(norm_ref_with, norm_hyp_with)
cer_score_with = cer(norm_ref_with, norm_hyp_with)
print(f"\nWER: {wer_score_with:.4f} ({wer_score_with*100:.2f}%)")
print(f"CER: {cer_score_with:.4f} ({cer_score_with*100:.2f}%)")

# Show the improvement
print("\n--- Improvement ---")
wer_improvement = wer_score_without - wer_score_with
cer_improvement = cer_score_without - cer_score_with
print(f"WER Improvement: {wer_improvement:.4f} ({wer_improvement*100:.2f}%)")
print(f"CER Improvement: {cer_improvement:.4f} ({cer_improvement*100:.2f}%)")
