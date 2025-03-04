"""
Test script to verify time normalization with zero minutes.
"""
from trnorm import normalize

# Test cases with zero minutes
test_cases = [
    "Ancak 13 Nisan 2024 akşamı saat 22.00 sularında, İran Devrim Muhafızları, İsrail'i hedef alarak devasa bir füze saldırısı başlattı.",
    "Toplantı saat 9.00'da başlayacak.",
    "Saat 14.00 itibariyle tüm hazırlıklar tamamlanmış olacak.",
    "Uçak 18:00'de kalkacak.",
    "07.00'de kalkıp işe gidiyorum.",
    "Saat 22.30'da buluşalım.",  # Half hour case
    "Saat 10.15'te görüşelim."   # Regular minutes case
]

# Test with and without time normalization
for i, test in enumerate(test_cases):
    print(f"Test Case {i+1}:")
    print(f"Original: {test}")
    
    # With time normalization
    normalized = normalize(test)
    print(f"Normalized: {normalized}")
    
    print()  # Empty line for readability

# Test the specific example from the user
ref = "Ancak 13 Nisan 2024 akşamı saat 22.00 sularında, İran Devrim Muhafızları, İsrail'i hedef alarak devasa bir füze saldırısı başlattı."
hyp = "Ancak 13 Nisan 2024 akşamı saat 22 sularında İran devrim muhafızları İsrail'i hedef alarak devasa bir füze saldırısı başlattı."

print("User Example:")
print(f"Reference: {ref}")
print(f"Hypothesis: {hyp}")

norm_ref = normalize(ref)
norm_hyp = normalize(hyp)

print(f"Normalized Reference: {norm_ref}")
print(f"Normalized Hypothesis: {norm_hyp}")

# Calculate WER
from trnorm.metrics import wer, cer

wer_score = wer(norm_ref, norm_hyp)
cer_score = cer(norm_ref, norm_hyp)

print(f"\nWER: {wer_score:.4f} ({wer_score*100:.2f}%)")
print(f"CER: {cer_score:.4f} ({cer_score*100:.2f}%)")
