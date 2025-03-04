from trnorm import normalize
from trnorm.num_to_text import NumberToTextConverter, convert_numbers_to_words_wrapper
from trnorm.time_utils import normalize_times
from trnorm.legacy_normalizer import turkish_lower

# Test with examples that might be misinterpreted due to thousands separators
examples = [
    "Saat 22.00 sularında başlayacak.",
    "Bu ürün 1.000 TL.",
    "Şirketin değeri 2.000.000 dolar.",
    "Saat 9.30'da buluşalım.",
    "Sıcaklık 36.5 derece.",
    "Bu kitap 22.50 TL."
]

# Create a converter instance to directly test the number conversion
converter = NumberToTextConverter()

print("Testing with direct number conversion:")
print("=====================================")
for example in examples:
    print(f"\nOriginal: {example}")
    # Use the converter directly to see how it interprets the numbers
    converted = converter.convert_numbers_to_words(example)
    print(f"Direct conversion: {converted}")
    
print("\n\nTesting with full normalization:")
print("===============================")

# Define converter lists for different normalization approaches
without_time_converters = [
    convert_numbers_to_words_wrapper,
    turkish_lower
]

with_time_converters = [
    normalize_times,
    convert_numbers_to_words_wrapper,
    turkish_lower
]

for example in examples:
    print(f"\nOriginal: {example}")
    # Test with time normalization disabled
    without_time = normalize(example, without_time_converters)
    print(f"Without time normalization: {without_time}")
    # Test with time normalization enabled
    with_time = normalize(example, with_time_converters)
    print(f"With time normalization: {with_time}")
