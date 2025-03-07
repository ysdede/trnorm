"""
Compare WER/CER calculations with and without context-aware normalization.

This script demonstrates how context-aware normalization can improve
WER/CER calculations for ASR evaluation by preserving matching suffix patterns.
"""

from trnorm import normalize
from trnorm.metrics import wer, cer

# Test cases with Turkish suffixes that might affect WER/CER calculations
test_cases = [
    # Case 1: Both sentences have "ile" in the same position
    {
        "ref": "Toros ile gitti",
        "hyp": "Toros ile geldi"
    },
    # Case 2: Both sentences have "ise" in the same position
    {
        "ref": "Hava güzel ise pikniğe gidelim",
        "hyp": "Hava güzel ise parka gidelim"
    },
    # Case 3: Both sentences have "iken" in the same position
    {
        "ref": "Çocuk iken çok yaramazdı",
        "hyp": "Çocuk iken çok uslu duruyordu"
    },
    # Case 4: Different number of suffixes
    {
        "ref": "Toros ile gitti ve hava güzel ise pikniğe gidelim",
        "hyp": "Toros gitti ve hava güzel pikniğe gidelim"
    },
    # Case 5: Multiple instances of the same suffix
    {
        "ref": "Ali ile Veli ile gitti",
        "hyp": "Ali ile Veli ile geldi"
    },
    # Real ASR examples
    {
        "ref": "Yavru ile kâtip masada oturuyordu",
        "hyp": "Yavru ile katip masada oturuyordu"
    },
    {
        "ref": "Hayat sana limon verdi ise limonata yap",
        "hyp": "Hayat sana limon verdi ise limonat yap"
    }
]

print("=" * 80)
print("WER/CER COMPARISON: STANDARD VS CONTEXT-AWARE NORMALIZATION")
print("=" * 80)

total_standard_wer = 0
total_standard_cer = 0
total_context_wer = 0
total_context_cer = 0

for i, case in enumerate(test_cases, 1):
    ref = case["ref"]
    hyp = case["hyp"]
    
    # Standard normalization (without context)
    ref_norm_standard = normalize(ref)
    hyp_norm_standard = normalize(hyp)
    
    standard_wer = wer(ref_norm_standard, hyp_norm_standard)
    standard_cer = cer(ref_norm_standard, hyp_norm_standard)
    
    # Context-aware normalization
    ref_norm_context = normalize(ref, context_text=hyp)
    hyp_norm_context = normalize(hyp, context_text=ref)
    
    context_wer = wer(ref_norm_context, hyp_norm_context)
    context_cer = cer(ref_norm_context, hyp_norm_context)
    
    # Calculate improvement
    wer_improvement = standard_wer - context_wer
    cer_improvement = standard_cer - context_cer
    
    # Accumulate totals
    total_standard_wer += standard_wer
    total_standard_cer += standard_cer
    total_context_wer += context_wer
    total_context_cer += context_cer
    
    print(f"\nCase {i}:")
    print("-" * 80)
    print(f"Reference: {ref}")
    print(f"Hypothesis: {hyp}")
    print("-" * 40)
    print(f"Standard Normalized Reference: {ref_norm_standard}")
    print(f"Standard Normalized Hypothesis: {hyp_norm_standard}")
    print(f"Standard WER: {standard_wer:.4f}, CER: {standard_cer:.4f}")
    print("-" * 40)
    print(f"Context-Aware Normalized Reference: {ref_norm_context}")
    print(f"Context-Aware Normalized Hypothesis: {hyp_norm_context}")
    print(f"Context-Aware WER: {context_wer:.4f}, CER: {context_cer:.4f}")
    print("-" * 40)
    print(f"Improvement - WER: {wer_improvement:.4f}, CER: {cer_improvement:.4f}")
    
    if wer_improvement > 0 or cer_improvement > 0:
        print("✓ Context-aware normalization improved the scores!")
    else:
        print("- No improvement with context-aware normalization.")

# Calculate average improvements
avg_standard_wer = total_standard_wer / len(test_cases)
avg_standard_cer = total_standard_cer / len(test_cases)
avg_context_wer = total_context_wer / len(test_cases)
avg_context_cer = total_context_cer / len(test_cases)

wer_improvement = avg_standard_wer - avg_context_wer
cer_improvement = avg_standard_cer - avg_context_cer

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Average Standard WER: {avg_standard_wer:.4f}, CER: {avg_standard_cer:.4f}")
print(f"Average Context-Aware WER: {avg_context_wer:.4f}, CER: {avg_context_cer:.4f}")
print(f"Average Improvement - WER: {wer_improvement:.4f}, CER: {cer_improvement:.4f}")

if wer_improvement > 0 or cer_improvement > 0:
    print("\n✓ Context-aware normalization improved the overall scores!")
else:
    print("\n- No overall improvement with context-aware normalization.")

print("\n" + "=" * 80)
print("Test completed!")
print("=" * 80)
