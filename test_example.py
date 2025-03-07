from trnorm import normalize
from trnorm.time_utils import normalize_times
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.legacy_normalizer import turkish_lower

# Test with the specific example
text = "Ancak 13 Nisan 2024 akşamı saat 22.00 sularında, İran Devrim Muhafızları, İsrail'i hedef alarak devasa bir füze saldırısı başlattı."
print("Original text:")
print(text)

# With time normalization
with_time_converters = [
    normalize_times,
    convert_numbers_to_words_wrapper,
    turkish_lower
]
print("\nNormalized text (with time normalization):")
print(normalize(text, with_time_converters))

# Without time normalization
without_time_converters = [
    convert_numbers_to_words_wrapper,
    turkish_lower
]
print("\nNormalized text (without time normalization):")
print(normalize(text, without_time_converters))
