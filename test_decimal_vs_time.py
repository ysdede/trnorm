from trnorm import normalize

# Test with a time that would be incorrectly interpreted as a decimal number
text = "Saat 22.00 sularında başlayacak."
print("Original text:")
print(text)

# First modify the NumberToTextConverter to see how it would interpret 22.00 without time normalization
# We'll do this by creating a custom normalizer with time normalization disabled
print("\nNormalized text (WITHOUT time normalization):")
result_without_time = normalize(text, apply_time_normalization=False)
print(result_without_time)

# Now with time normalization enabled (default)
print("\nNormalized text (WITH time normalization):")
result_with_time = normalize(text)
print(result_with_time)

# Test with other examples
examples = [
    "Saat 13.30'da görüşeceğiz.",
    "22.15'te başlayacak.",
    "Toplantı 9.45'te başlayacak."
]

print("\nAdditional examples:")
for example in examples:
    print(f"\nOriginal: {example}")
    without_time = normalize(example, apply_time_normalization=False)
    print(f"Without time normalization: {without_time}")
    with_time = normalize(example)
    print(f"With time normalization: {with_time}")
