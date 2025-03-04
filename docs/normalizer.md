# Turkish Text Normalizer

The `TurkishNormalizer` class provides a comprehensive solution for normalizing Turkish text by applying all available normalization steps in the correct order.

## Features

- Converts numbers to their text representation (123 → yüz yirmi üç)
- Normalizes ordinal numbers (1. → birinci)
- Converts Roman numerals to Arabic numbers
- Converts special symbols (%, $, etc.) to their text representation
- Intelligently handles multiplication symbols in dimensions (3x4 → 3 çarpı 4, 2x5x6x3 → 2 çarpı 5 çarpı 6 çarpı 3)
- Expands unit abbreviations to their full text (cm → santimetre, kg → kilogram)
- Handles Turkish character casing and diacritical marks
- Normalizes time expressions (e.g., "saat 22.00" → "saat yirmi iki")
- Provides both a class-based API and a simple function-based API
- Supports processing both single strings and lists of strings
- Allows customization of which normalization steps to apply
- Handles numbers followed by commas in lists and sequences
- Provides apostrophe handling for Turkish suffixes (e.g., "8'i" → "sekizi")

## Usage

### Basic Usage

```python
from trnorm import normalize

# Normalize a single string
text = "Bugün 15. kattaki 3 toplantıya katıldım."
normalized_text = normalize(text)
print(normalized_text)
# Output: "bugün on beşinci kattaki üç toplantıya katıldım."

# Normalize a list of strings
texts = [
    "Saat 14:30'da %25 indirimli ürünler satışa çıkacak.",
    "II. Dünya Savaşı 1939-1945 yılları arasında gerçekleşti."
]
normalized_texts = normalize(texts)
print(normalized_texts)
# Output: [
#   "saat on dört otuzda yüzde yirmi beş indirimli ürünler satışa çıkacak.",
#   "ikinci dünya savaşı bin dokuz yüz otuz dokuz bin dokuz yüz kırk beş yılları arasında gerçekleşti."
# ]
```

### Using the Class Directly

```python
from trnorm import TurkishNormalizer

# Create a custom normalizer
normalizer = TurkishNormalizer(
    apply_number_conversion=True,
    apply_ordinal_normalization=True,
    apply_symbol_conversion=True,
    apply_multiplication_symbol=True,
    apply_unit_normalization=True,
    apply_time_normalization=True,
    apply_legacy_normalization=False,
    lowercase=True,
    remove_hats=True
)

# Normalize text
text = "Ürün fiyatı 1.250,75 TL'dir."
normalized_text = normalizer.normalize(text)
print(normalized_text)
# Output: "ürün fiyatı bin iki yüz elli virgül yetmiş beş türk lirası'dir."
```

### Customizing Normalization Steps

```python
from trnorm import normalize

# Only convert numbers to text, keep case and diacritical marks
text = "Âlim insanlar 15 kitap okumuş."
normalized_text = normalize(
    text,
    apply_number_conversion=True,
    apply_ordinal_normalization=False,
    apply_symbol_conversion=False,
    apply_multiplication_symbol=False,
    apply_unit_normalization=False,
    apply_time_normalization=False,
    lowercase=False,
    remove_hats=False
)
print(normalized_text)
# Output: "Âlim insanlar on beş kitap okumuş."

# Apply legacy normalization (more aggressive, removes punctuation)
text = "Bugün 3x4 metre halı aldım."
normalized_text = normalize(text, apply_legacy_normalization=True)
print(normalized_text)
# Output: "bugün üç çarpı dört metre halı aldım"
```

### Handling Dimensions and Multiplication Symbols

```python
from trnorm import normalize

# Handle dimensions with merged multiplication symbols
text = "Odanın boyutları 2x3x4 metre."
normalized_text = normalize(text)
print(normalized_text)
# Output: "odanın boyutları iki çarpı üç çarpı dört metre."

# Handle dimensions with units
text = "Halının boyutu 120x180cm."
normalized_text = normalize(text)
print(normalized_text)
# Output: "halının boyutu yüz yirmi çarpı yüz seksen santimetre."
```

### Handling Unit Abbreviations

```python
from trnorm import normalize

# Convert unit abbreviations to full text
text = "Masanın yüksekliği 75 cm."
normalized_text = normalize(text)
print(normalized_text)
# Output: "masanın yüksekliği yetmiş beş santimetre."

# Multiple units in the same text
text = "Odanın boyutları 5 m x 4 m, yüksekliği 3 m."
normalized_text = normalize(text)
print(normalized_text)
# Output: "odanın boyutları beş metre çarpı dört metre, yüksekliği üç metre."

# Disable unit normalization
text = "Sıcaklık 25 °C."
normalized_text = normalize(text, apply_unit_normalization=False)
print(normalized_text)
# Output: "sıcaklık yirmi beş °c."
```

### Handling Time Expressions

```python
from trnorm import normalize

# Normalize time expressions
text = "Saat 22.00'de toplantımız var."
normalized_text = normalize(text)
print(normalized_text)
# Output: "saat yirmi ikide toplantımız var."

# Normalize standalone times
text = "13.30'da görüşeceğiz."
normalized_text = normalize(text)
print(normalized_text)
# Output: "on üç buçukta görüşeceğiz."

# Normalize times with minutes
text = "Saat 10.15'te görüşelim."
normalized_text = normalize(text)
print(normalized_text)
# Output: "saat on on beşte görüşelim."
```

### Handling Number Lists and Sequences

```python
from trnorm import normalize

# Convert numbers in lists
text = "1, 2, 3 sayıları ardışıktır."
normalized_text = normalize(text)
print(normalized_text)
# Output: "bir, iki, üç sayıları ardışıktır."

# Handle numbers in date sequences
text = "Toplantımız 13, 14 ve 15 Mayıs tarihlerinde yapılacak."
normalized_text = normalize(text)
print(normalized_text)
# Output: "toplantımız on üç, on dört ve on beş mayıs tarihlerinde yapılacak."
```

### Apostrophe Handling in Turkish Suffixes

In Turkish, apostrophes are often used to separate suffixes from proper nouns or numbers. The normalizer can remove these apostrophes to create more natural text:

```python
from trnorm import normalize

# Enable apostrophe handling
text = "8'i almadım"
normalized_text = normalize(text, apply_apostrophe_handling=True)
print(normalized_text)
# Output: "sekizi almadım"

# More examples
text = "İstanbul'da yaşıyorum"
normalized_text = normalize(text, apply_apostrophe_handling=True)
print(normalized_text)
# Output: "istanbulda yaşıyorum"
```

## Normalization Order

The normalizer applies the following steps in order:

1. **Preprocess dimensions**: Add spaces between numbers and 'x' in dimension expressions
2. **Symbol conversion**: Convert symbols (%, $, etc.) to their text representation
3. **Multiplication symbol replacement**: Replace 'x' with 'çarpı' in dimension expressions
4. **Time expression normalization**: Convert time expressions (e.g., "saat 22.00") to their text form
5. **Number to text conversion**: Convert numbers to their text representation
6. **Ordinal normalization**: Convert ordinal numbers to their text representation
7. **Unit abbreviation expansion**: Convert unit abbreviations to their full text form
8. **Character normalization**: Apply lowercase and remove circumflex (hat) from Turkish characters
9. **Apostrophe handling**: Remove apostrophes in Turkish suffixes
10. **Legacy normalization**: Apply more aggressive normalization (if enabled)

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `apply_number_conversion` | bool | True | Whether to convert numbers to their text representation |
| `apply_ordinal_normalization` | bool | True | Whether to normalize ordinals |
| `apply_symbol_conversion` | bool | True | Whether to convert symbols to their text representation |
| `apply_multiplication_symbol` | bool | True | Whether to replace multiplication symbol 'x' with 'çarpı' |
| `apply_unit_normalization` | bool | True | Whether to expand unit abbreviations to full text |
| `apply_time_normalization` | bool | True | Whether to normalize time expressions |
| `apply_apostrophe_handling` | bool | False | Whether to remove apostrophes in Turkish suffixes |
| `apply_legacy_normalization` | bool | False | Whether to apply legacy normalization (more aggressive) |
| `lowercase` | bool | True | Whether to convert text to lowercase |
| `remove_hats` | bool | True | Whether to remove circumflex (hat) from Turkish characters |

## Time Normalization

The time normalization feature converts time expressions to their text form before applying number-to-text conversion. This ensures that time expressions are properly normalized and not misinterpreted as decimal numbers.

Examples:

- "saat 22.00" → "saat yirmi iki" (zero minutes are omitted)
- "13.30" → "on üç buçuk" (half hours are converted to "buçuk")
- "9:45" → "dokuz kırk beş"
- "18:00" → "on sekiz" (zero minutes are omitted)

The time normalization handles:

- Times with "saat" prefix (e.g., "saat 22.00", "saat 9:45")
- Standalone times (e.g., "22.00", "9:45")
- Special case for half hours (e.g., "13.30" → "on üç buçuk")
- Omitting zero minutes (e.g., "22.00" → "yirmi iki" instead of "yirmi iki sıfır")
