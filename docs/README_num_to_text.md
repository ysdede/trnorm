# Number to Text Converter for Turkish (num_to_text)

The `num_to_text` module provides functionality for converting numeric expressions in Turkish text to their word equivalents. This module is part of the `trnorm` package for Turkish text normalization.

## Features

- Converts numeric digits to their Turkish word equivalents
- Handles decimal numbers with configurable decimal separator
- Processes numbers embedded within text
- Supports thousands separators in numeric expressions
- Handles numbers with apostrophes (e.g., "67'ler", "100'lerce")

## Usage

```python
from trnorm.num_to_text import NumberToTextConverter

# Initialize the converter
converter = NumberToTextConverter()

# Basic number conversion
result = converter.convert_numbers_to_words("5 elma")  # "beş elma"

# Decimal number conversion
result = converter.convert_numbers_to_words("3,14 pi sayısı")  # "üç virgül on dört pi sayısı"

# Numbers with apostrophes
result = converter.convert_numbers_to_words("1960'lı yıllar")  # "bin dokuz yüz altmış'lı yıllar"
result = converter.convert_numbers_to_words("100'lerce insan")  # "yüz'lerce insan"

# Complex examples
result = converter.convert_numbers_to_words("1990'ların başında 15.000'den fazla kişi katıldı.")
# "bin dokuz yüz doksan'ların başında on beş bin'den fazla kişi katıldı."
```

## Apostrophe Handling

The module has special handling for numbers with apostrophes, which are common in Turkish:

- "67'ler" → "altmış yedi'ler" (The 67's / Generation 67)
- "1960'lı" → "bin dokuz yüz altmış'lı" (The 1960s)
- "100'lerce" → "yüz'lerce" (Hundreds of)
- "1000'den" → "bin'den" (More than a thousand)

The implementation splits tokens at apostrophes, converts the number part to text, and preserves the suffix after the apostrophe.

## Configuration Options

The `convert_numbers_to_words` method accepts several parameters:

- `input_text`: The text containing numbers to convert
- `num_dec_digits`: Maximum number of decimal digits to process (default: 6)
- `decimal_seperator`: Character used as decimal separator (default: ",")
- `merge_words`: Whether to merge the resulting words (default: False)

## Demo

A demo script is available at `examples/demo_num_to_text.py` that showcases the functionality of this module.

## Testing

The module includes comprehensive test cases in `tests/test_num_to_text.py`, including tests for numbers with apostrophes and other edge cases.
