"""
Demonstration of context-aware normalization for Turkish text.

This script demonstrates how the context-aware normalization works,
particularly for handling Turkish suffixes in reference and hypothesis pairs.
"""

from trnorm import normalize

def print_comparison(title, ref, hyp, ref_norm, hyp_norm):
    """Print a formatted comparison of original and normalized text pairs."""
    print(f"\n{title}")
    print("-" * 80)
    print(f"Reference (original): {ref}")
    print(f"Hypothesis (original): {hyp}")
    print(f"Reference (normalized): {ref_norm}")
    print(f"Hypothesis (normalized): {hyp_norm}")
    print("-" * 80)

# Test cases with Turkish suffixes
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
    }
]

print("=" * 80)
print("CONTEXT-AWARE NORMALIZATION DEMO")
print("=" * 80)

for i, case in enumerate(test_cases, 1):
    ref = case["ref"]
    hyp = case["hyp"]
    
    # Standard normalization (without context)
    ref_norm_standard = normalize(ref)
    hyp_norm_standard = normalize(hyp)
    
    print_comparison(
        f"Case {i}: Standard Normalization (without context)",
        ref, hyp, ref_norm_standard, hyp_norm_standard
    )
    
    # Context-aware normalization
    ref_norm_context = normalize(ref, context_text=hyp)
    hyp_norm_context = normalize(hyp, context_text=ref)
    
    print_comparison(
        f"Case {i}: Context-Aware Normalization",
        ref, hyp, ref_norm_context, hyp_norm_context
    )
    
    print("\n" + "=" * 80)

# Additional test with a real ASR example
print("\nReal ASR Example:")
print("-" * 80)

ref = "Yavru ile kâtip masada oturuyordu"
hyp = "Yavru ile katip masada oturuyordu"

# Standard normalization
ref_norm_standard = normalize(ref)
hyp_norm_standard = normalize(hyp)

print_comparison(
    "Standard Normalization (without context)",
    ref, hyp, ref_norm_standard, hyp_norm_standard
)

# Context-aware normalization
ref_norm_context = normalize(ref, context_text=hyp)
hyp_norm_context = normalize(hyp, context_text=ref)

print_comparison(
    "Context-Aware Normalization",
    ref, hyp, ref_norm_context, hyp_norm_context
)

print("\n" + "=" * 80)
print("Demo completed!")
print("=" * 80)
