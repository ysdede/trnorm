"""
Demonstration of alphanumeric pattern handling in the Turkish text normalization pipeline.

This example shows how to use the normalize_alphanumeric function to separate
alphanumeric patterns (letter+number) with a space, allowing for proper text
normalization in the pipeline.
"""

from trnorm.alphanumeric import normalize_alphanumeric
from trnorm import normalize
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.text_utils import turkish_lower

# Example texts with alphanumeric patterns
example_texts = [
    "Kısa vadeli kredilerin notu ise F3.",
    "B1 olan döviz kuru notu ise değişmedi.",
    "F16 savaş uçakları tatbikata katıldı.",
    "A400M nakliye uçağı Türk Hava Kuvvetleri'ne teslim edildi.",
    "Hastaya B12 vitamini verildi.",
    "C4 patlayıcısı imha edildi.",
    "Öğrenciler A1 seviyesinden başlayarak dil öğreniyor."
]

print("=" * 80)
print("ALPHANUMERIC PATTERN HANDLING DEMO")
print("=" * 80)

# Demonstrate standalone normalize_alphanumeric function
print("\n1. Using normalize_alphanumeric function directly:")
print("-" * 50)

for text in example_texts:
    print(f"\nOriginal: {text}")
    
    # Default behavior (separation enabled)
    separated = normalize_alphanumeric(text)
    print(f"Separated: {separated}")
    
    # With separation disabled
    not_separated = normalize_alphanumeric(text, separate=False)
    print(f"Not separated: {not_separated}")

# Demonstrate in a normalization pipeline
print("\n\n2. Using in a normalization pipeline:")
print("-" * 50)

# Define two pipelines - one with alphanumeric separation and one without
pipeline_with_separation = [
    normalize_alphanumeric,  # Default: separation enabled
    convert_numbers_to_words_wrapper,
    turkish_lower
]

pipeline_without_separation = [
    lambda text: normalize_alphanumeric(text, separate=False),  # Disable separation
    convert_numbers_to_words_wrapper,
    turkish_lower
]

for text in example_texts[:4]:  # Use just a few examples for brevity
    print(f"\nOriginal: {text}")
    
    # Apply pipeline with separation
    result_with_separation = normalize(text, pipeline_with_separation)
    print(f"With separation: {result_with_separation}")
    
    # Apply pipeline without separation
    result_without_separation = normalize(text, pipeline_without_separation)
    print(f"Without separation: {result_without_separation}")

# Show the specific examples from the user's request
print("\n\n3. User's specific examples:")
print("-" * 50)

user_examples = [
    "Kısa vadeli kredilerin notu ise F3.",
    "B1 olan döviz kuru notu ise değişmedi."
]

pipeline = [
    normalize_alphanumeric,
    convert_numbers_to_words_wrapper,
    turkish_lower
]

for text in user_examples:
    print(f"\nOriginal: {text}")
    
    # Apply the pipeline
    result = normalize(text, pipeline)
    print(f"Normalized: {result}")
    
    # Show the intermediate step after alphanumeric separation
    separated = normalize_alphanumeric(text)
    print(f"After separation: {separated}")
    
    # Show the intermediate step after number conversion
    after_number_conversion = convert_numbers_to_words_wrapper(separated)
    print(f"After number conversion: {after_number_conversion}")

print("\n" + "=" * 80)
print("Demo completed!")
print("=" * 80)
