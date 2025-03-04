"""
Test script to verify the fix for the user's specific example with commas.
"""
from trnorm import normalize
from trnorm.metrics import wer, cer

# The user's example
ref = 'General Jukov, o günleri günlüğüne şu şekilde aktardı; "13, 14 ve 15 Eylül günleri, Stalingrad için çok zor günlerdi.'
hyp = 'General Yukov o günleri günlüğüne şu şekilde aktardı. 13, 14 ve 15 Eylül günleri Stalingrad için çok zor günlerdi.'

print("Original Reference:")
print(ref)
print("\nOriginal Hypothesis:")
print(hyp)

# Test with our fixed normalization
print("\n--- With Fixed Normalization ---")
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

# Format the output in the debugging data format the user mentioned
print("\n--- Debugging Data Format ---")
print(f"{wer_score*100:.2f}/- - {cer_score*100:.2f}/-")
print(ref)
print(hyp)
print(norm_ref)
print(norm_hyp)
