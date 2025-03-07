from trnorm import normalize
from trnorm.time_utils import normalize_times
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.legacy_normalizer import turkish_lower

# Test with a time that would be incorrectly interpreted as a decimal number
text = "Saat 22.00 sularında başlayacak."
print("Original text:")
print(text)

# First modify the NumberToTextConverter to see how it would interpret 22.00 without time normalization
# We'll do this by creating a custom normalizer with time normalization disabled
print("\nNormalized text (WITHOUT time normalization):")
without_time_converters = [
    convert_numbers_to_words_wrapper,
    turkish_lower
]
result_without_time = normalize(text, without_time_converters)
print(result_without_time)

# Now with time normalization enabled
print("\nNormalized text (WITH time normalization):")
with_time_converters = [
    normalize_times,
    convert_numbers_to_words_wrapper,
    turkish_lower
]
result_with_time = normalize(text, with_time_converters)
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
    without_time = normalize(example, without_time_converters)
    print(f"Without time normalization: {without_time}")
    with_time = normalize(example, with_time_converters)
    print(f"With time normalization: {with_time}")
