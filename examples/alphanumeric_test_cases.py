"""
Test cases for alphanumeric handling with the examples provided by the user.

This script demonstrates how the alphanumeric handling feature improves
WER/CER scores for sentences with alphanumeric abbreviations like B3, F1, etc.
"""

from trnorm import normalize
from trnorm.alphanumeric import normalize_alphanumeric
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.text_utils import turkish_lower, sapkasiz, remove_punctuation
from trnorm.metrics import wer, cer
from trnorm.legacy_normalizer import normalize_text as legacy_normalize

# Define the test cases from the user's examples
test_cases = [
    {
        "ref": "Kısa vadeli kredilerin notu ise F üç.",
        "hyp": "Kısa vadeli kredilerin notu ise F3."
    },
    {
        "ref": "B bir olan döviz kuru notu ise değişmedi.",
        "hyp": "B1 olan döviz kuru notu ise değişmedi."
    }
]

# Define two pipelines - one with alphanumeric handling and one without
pipeline_with_alphanumeric = [
    normalize_alphanumeric,  # Add alphanumeric handling
    convert_numbers_to_words_wrapper,
    sapkasiz,
    turkish_lower,
    remove_punctuation
]

pipeline_without_alphanumeric = [
    convert_numbers_to_words_wrapper,
    sapkasiz,
    turkish_lower,
    remove_punctuation
]

print("=" * 80)
print("ALPHANUMERIC HANDLING TEST CASES")
print("=" * 80)
print("\nComparing WER/CER scores with and without alphanumeric handling")
print("-" * 60)

for i, case in enumerate(test_cases, 1):
    ref = case["ref"]
    hyp = case["hyp"]
    
    print(f"\nTest Case {i}:")
    print(f"Reference: {ref}")
    print(f"Hypothesis: {hyp}")
    
    # Normalize with our pipeline including alphanumeric handling
    our_norm_ref = normalize(ref, pipeline_with_alphanumeric)
    our_norm_hyp = normalize(hyp, pipeline_with_alphanumeric)
    
    # Normalize with our pipeline without alphanumeric handling
    without_alpha_ref = normalize(ref, pipeline_without_alphanumeric)
    without_alpha_hyp = normalize(hyp, pipeline_without_alphanumeric)
    
    # Normalize with legacy normalizer
    legacy_norm_ref = legacy_normalize(ref)
    legacy_norm_hyp = legacy_normalize(hyp)
    
    # Calculate WER and CER for each approach
    our_wer = wer(our_norm_ref, our_norm_hyp)
    our_cer = cer(our_norm_ref, our_norm_hyp)
    
    without_alpha_wer = wer(without_alpha_ref, without_alpha_hyp)
    without_alpha_cer = cer(without_alpha_ref, without_alpha_hyp)
    
    legacy_wer = wer(legacy_norm_ref, legacy_norm_hyp)
    legacy_cer = cer(legacy_norm_ref, legacy_norm_hyp)
    
    print("\nScores (WER/CER):")
    print(f"With alphanumeric handling: {our_wer:.2f}/{our_cer:.3f}")
    print(f"Without alphanumeric handling: {without_alpha_wer:.2f}/{without_alpha_cer:.3f}")
    print(f"Legacy normalizer: {legacy_wer:.2f}/{legacy_cer:.3f}")
    
    print("\nNormalized outputs:")
    print(f"With alphanumeric handling:")
    print(f"  Ref: {our_norm_ref}")
    print(f"  Hyp: {our_norm_hyp}")
    
    print(f"Without alphanumeric handling:")
    print(f"  Ref: {without_alpha_ref}")
    print(f"  Hyp: {without_alpha_hyp}")
    
    print(f"Legacy normalizer:")
    print(f"  Ref: {legacy_norm_ref}")
    print(f"  Hyp: {legacy_norm_hyp}")

print("\n" + "=" * 80)
print("Test completed!")
print("=" * 80)
