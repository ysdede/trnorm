# Turkish Text Utilities

This module provides various utilities for working with Turkish text, including case conversion, vowel analysis, and accent removal.

## Features

### Case Conversion

- `turkish_lower(text)`: Converts text to lowercase, handling Turkish-specific characters (İ→i, I→ı, etc.)
- `turkish_upper(text)`: Converts text to uppercase, handling Turkish-specific characters (i→İ, ı→I, etc.)
- `turkish_capitalize(text)`: Capitalizes the first letter of text, handling Turkish-specific characters
- `is_turkish_upper(text)`: Checks if text is entirely uppercase according to Turkish rules

### Vowel Analysis

- `son_harf(text)`: Returns the last letter of a word
- `sesli_ile_bitiyor(text)`: Checks if a word ends with a vowel
- `son_sesli_harf(text)`: Returns the last vowel in a word
- `son_sesli_harf_kalin(text)`: Checks if the last vowel in a word is a back vowel (kalın sesli)

### Accent Removal

- `sapkasiz(text)`: Removes accents from Turkish text (â→a, î→i, û→u, etc.)

## Constants

- `kalin_sesliler`: Turkish back vowels (a, ı, o, u, û, â)
- `ince_sesliler`: Turkish front vowels (e, i, ö, ü, î, ê, ô)
- `sesli_harfler`: All Turkish vowels

## Usage

```python
from text_utils import turkish_lower, turkish_upper, turkish_capitalize, sapkasiz

# Case conversion
print(turkish_lower("İSTANBUL"))  # "istanbul"
print(turkish_upper("istanbul"))  # "İSTANBUL"
print(turkish_capitalize("istanbul"))  # "İstanbul"

# Accent removal
print(sapkasiz("kâğıt"))  # "kağıt"
```

## Examples

See `demo_text_utils.py` for comprehensive examples of all functions.

## Testing

Unit tests are available in `test_text_utils.py`. Run with:

```
python -m unittest test_text_utils.py
```
