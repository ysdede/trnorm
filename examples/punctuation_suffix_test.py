"""
Test the improved suffix handling with punctuation.

This script demonstrates how the context-aware normalization handles
Turkish suffixes in text with various punctuation marks.
"""

from trnorm import normalize
from trnorm.suffix_handler import context_aware_merge_suffixes, _count_suffixes
from trnorm.metrics import wer, cer

# Test cases with Turkish suffixes and punctuation
test_cases = [
    # Case 1: Suffixes with commas
    {
        "ref": "Toros ile, Ahmet ile, ve Ali ile gittiler.",
        "hyp": "Toros ile, Ahmet ile, ve Ali ile geldiler."
    },
    # Case 2: Suffixes with question marks
    {
        "ref": "Hava güzel ise? Pikniğe gidelim mi?",
        "hyp": "Hava güzel ise? Parka gidelim mi?"
    },
    # Case 3: Suffixes with semicolons
    {
        "ref": "Çocuk iken; çok yaramazdı; şimdi büyüdü.",
        "hyp": "Çocuk iken; çok uslu duruyordu; şimdi büyüdü."
    },
    # Case 4: Mixed punctuation
    {
        "ref": "Toros ile gitti, hava güzel ise pikniğe gidelim; değil ise evde kalalım!",
        "hyp": "Toros ile geldi, hava güzel ise parka gidelim; değil ise evde kalalım!"
    }
]

print("=" * 80)
print("PUNCTUATION HANDLING IN CONTEXT-AWARE SUFFIX NORMALIZATION")
print("=" * 80)

for i, case in enumerate(test_cases, 1):
    ref = case["ref"]
    hyp = case["hyp"]
    
    # Count suffixes in both texts
    ref_suffixes = _count_suffixes(ref)
    hyp_suffixes = _count_suffixes(hyp)
    
    print(f"\nCase {i}:")
    print("-" * 80)
    print(f"Reference: {ref}")
    print(f"Hypothesis: {hyp}")
    print("-" * 40)
    print("Suffix counts:")
    print(f"Reference: {ref_suffixes}")
    print(f"Hypothesis: {hyp_suffixes}")
    print(f"Suffixes match: {ref_suffixes == hyp_suffixes}")
    print("-" * 40)
    
    # Standard normalization (without context)
    ref_norm_standard = normalize(ref)
    hyp_norm_standard = normalize(hyp)
    
    # Context-aware normalization
    ref_norm_context = normalize(ref, context_text=hyp)
    hyp_norm_context = normalize(hyp, context_text=ref)
    
    print(f"Standard Normalized Reference: {ref_norm_standard}")
    print(f"Standard Normalized Hypothesis: {hyp_norm_standard}")
    print("-" * 40)
    print(f"Context-Aware Normalized Reference: {ref_norm_context}")
    print(f"Context-Aware Normalized Hypothesis: {hyp_norm_context}")
    
    # Calculate WER/CER
    standard_wer = wer(ref_norm_standard, hyp_norm_standard)
    standard_cer = cer(ref_norm_standard, hyp_norm_standard)
    context_wer = wer(ref_norm_context, hyp_norm_context)
    context_cer = cer(ref_norm_context, hyp_norm_context)
    
    print("-" * 40)
    print(f"Standard WER: {standard_wer:.4f}, CER: {standard_cer:.4f}")
    print(f"Context-Aware WER: {context_wer:.4f}, CER: {context_cer:.4f}")
    print(f"Improvement - WER: {standard_wer - context_wer:.4f}, CER: {standard_cer - context_cer:.4f}")

print("\n" + "=" * 80)
print("Test completed!")
print("=" * 80)
