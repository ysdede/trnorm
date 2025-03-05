"""
Test script to investigate the issue with numbers followed by commas.
"""
from trnorm import normalize

# The example text with the issue
text = 'General Jukov, o günleri günlüğüne şu şekilde aktardı; "13, 14 ve 15 Eylül günleri, Stalingrad için çok zor günlerdi.'

print("Original text:")
print(text)

# Test with normalization
normalized = normalize(text)
print("\nNormalized text:")
print(normalized)

# Test with each component separately
print("\nTesting each component separately:")

# 1. Preprocess dimensions
from trnorm.dimension_utils import preprocess_dimensions
result = preprocess_dimensions(text)
print("\n1. After preprocess_dimensions:")
print(result)

# 2. Symbol conversion
from trnorm.symbols import convert_symbols
result = convert_symbols(result)
print("\n2. After convert_symbols:")
print(result)

# 3. Multiplication symbol replacement
from trnorm.dimension_utils import normalize_dimensions
result = normalize_dimensions(result)
print("\n3. After normalize_dimensions:")
print(result)

# 4. Time expression normalization
from trnorm.time_utils import normalize_times
result = normalize_times(result)
print("\n4. After normalize_times:")
print(result)

# 5. Number to text conversion
from trnorm.num_to_text import convert_numbers_to_words_wrapper
result = convert_numbers_to_words_wrapper(result)
print("\n5. After convert_numbers_to_words_wrapper:")
print(result)

# 6. Ordinal normalization
from trnorm.ordinals import normalize_ordinals
result = normalize_ordinals(result)
print("\n6. After normalize_ordinals:")
print(result)

# 7. Unit abbreviation expansion
from trnorm.unit_utils import normalize_units
result = normalize_units(result)
print("\n7. After normalize_units:")
print(result)

# 8. Character normalization
from trnorm.legacy_normalizer import replace_hatted_characters
from trnorm.text_utils import turkish_lower
result = replace_hatted_characters(result)
result = turkish_lower(result)
print("\n8. After character normalization:")
print(result)

# Test with specific modifications to num_to_text
print("\nTesting with direct number conversion:")
from trnorm.num_to_text import NumberToTextConverter
converter = NumberToTextConverter()

# Test direct conversion of "13,"
test_text = "13,"
converted = converter.convert_numbers_to_words(test_text)
print(f"\nDirect conversion of '{test_text}': '{converted}'")

# Test direct conversion of "13, 14"
test_text = "13, 14"
converted = converter.convert_numbers_to_words(test_text)
print(f"Direct conversion of '{test_text}': '{converted}'")

# Test direct conversion with different spacing
test_text = "13,14"
converted = converter.convert_numbers_to_words(test_text)
print(f"Direct conversion of '{test_text}': '{converted}'")
