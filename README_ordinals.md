# Turkish Ordinals Normalization

This module provides functionality for normalizing Turkish ordinals in text. It converts numeric ordinals (e.g., "1.", "2'nci", "3üncü") to their textual representation (e.g., "birinci", "ikinci", "üçüncü") while preserving bullet points.

## Features

- Converts numeric ordinals to their textual representation in Turkish
- Preserves bullet points (lines starting with a number followed by a period and an uppercase word)
- Handles various ordinal formats:
  - With period: "1.", "2.", "3."
  - With apostrophe: "1'inci", "2'nci", "3'üncü"
  - Attached: "1inci", "2nci", "3üncü"
- Preserves capitalization of words following bullet points
- Handles sequences of ordinals: "1., 2. ve 3. sınıflar" → "birinci, ikinci ve üçüncü sınıflar"
- Supports big numbers (up to billions):
  - 99. → doksan dokuzuncu
  - 103. → yüz üçüncü
  - 2000. → iki bininci
  - 19857. → on dokuz bin sekiz yüz elli yedinci
  - 1000000. → bir milyonuncu
  - 1000000000. → bir milyarıncı

## Usage

```python
from ordinals import normalize_ordinals

# Example text with ordinals
text = """
1. sınıf öğrencileri
2'nci katta oturuyorlar
3üncü sırada bekleyin
4. ve 5'inci arasında bir yerde
103. sırada
2000. saniye

# Bullet points (preserved)
1. Sabah kahvaltısı
2. Yürüyüş
"""

# Normalize the text
normalized_text = normalize_ordinals(text)
print(normalized_text)
```

## Output

```
birinci sınıf öğrencileri
ikinci katta oturuyorlar
üçüncü sırada bekleyin
dördüncü ve beşinci arasında bir yerde
yüz üçüncü sırada
iki bininci saniye

# Bullet points (preserved)
1. Sabah kahvaltısı
2. Yürüyüş
```

## Implementation Details

The module uses regular expressions to detect and convert various ordinal formats. It processes the text line by line, checking if each line is a bullet point (starts with a number followed by a period and an uppercase word) and preserving it if it is.

The module uses the `text_utils` module for checking if a word starts with an uppercase letter, which is crucial for determining whether a line is a bullet point or not.

For big numbers, the module first converts the number to its text representation (e.g., "iki bin" for 2000) and then adds the appropriate ordinal suffix to the last word (e.g., "iki bininci" for 2000.).

## Dependencies

- `re` module for regular expressions
- `text_utils` module for checking if a word starts with an uppercase letter

## Testing

The module includes a comprehensive test suite that covers all the features and edge cases. You can run the tests using:

```bash
python -m unittest test_ordinals.py
```

## Demo

A demo script is provided to showcase the functionality of the module:

```bash
python demo_ordinals.py
```
