"""
Example script demonstrating the apostrophe handling functionality.
"""
from trnorm import normalize
from trnorm.metrics import wer, cer

print("Turkish Apostrophe Handling Examples")
print("====================================\n")

print("Example 1: Basic apostrophe handling")
examples = [
    "8'i almadım",
    "Kitap'ı okudum",
    "Ahmet'in arabası",
    "İstanbul'da yaşıyorum",
    "GoPro 7'yi kullanıyorum"
]

for example in examples:
    print(f"Original: {example}")
    standard = normalize(example)
    with_apostrophe = normalize(example, apply_apostrophe_handling=True)
    print(f"Standard normalization: {standard}")
    print(f"With apostrophe handling: {with_apostrophe}")
    print()

print("Example 2: Apostrophes in sentences")
examples = [
    "GoPro Osmo Action'dan daha çok sevdiğim GoPro 7 bu sırada, 8'i almadım.",
    "Türkiye'nin 81 ili vardır, 34'ü İstanbul'dur.",
    "Kitap'ı okudum ve çok beğendim, 5'i de alacağım.",
    "Ahmet'in arabası kırmızı, Ali'ninki ise mavi."
]

for example in examples:
    print(f"Original: {example}")
    standard = normalize(example)
    with_apostrophe = normalize(example, apply_apostrophe_handling=True)
    print(f"Standard normalization: {standard}")
    print(f"With apostrophe handling: {with_apostrophe}")
    print()

print("Example 3: Impact on WER calculation")
ref = "GoPro Osmo Action'dan daha çok sevdiğim GoPro 7 bu sırada, 8'i almadım, niye almadım?"
hyp = "GoPro. Osmo Action'dan daha çok sevdiğim. GoPro 7 bu sırada. 8'i almadım. Niye almadım?"

print(f"Reference: {ref}")
print(f"Hypothesis: {hyp}")

# Standard normalization
std_norm_ref = normalize(ref)
std_norm_hyp = normalize(hyp)
std_wer = wer(std_norm_ref, std_norm_hyp)
std_cer = cer(std_norm_ref, std_norm_hyp)

print(f"\nStandard normalization WER: {std_wer:.4f} ({std_wer*100:.2f}%)")
print(f"Standard normalization CER: {std_cer:.4f} ({std_cer*100:.2f}%)")

# With apostrophe handling
apo_norm_ref = normalize(ref, apply_apostrophe_handling=True)
apo_norm_hyp = normalize(hyp, apply_apostrophe_handling=True)
apo_wer = wer(apo_norm_ref, apo_norm_hyp)
apo_cer = cer(apo_norm_ref, apo_norm_hyp)

print(f"\nWith apostrophe handling WER: {apo_wer:.4f} ({apo_wer*100:.2f}%)")
print(f"With apostrophe handling CER: {apo_cer:.4f} ({apo_cer*100:.2f}%)")

print("\nNormalized Reference (standard):")
print(std_norm_ref)
print("\nNormalized Hypothesis (standard):")
print(std_norm_hyp)

print("\nNormalized Reference (with apostrophe handling):")
print(apo_norm_ref)
print("\nNormalized Hypothesis (with apostrophe handling):")
print(apo_norm_hyp)
