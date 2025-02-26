# TRNorm

Turkish text normalization tools for natural language processing.

## Overview

TRNorm is a comprehensive Python package designed for Turkish text normalization, providing tools to convert numbers, ordinals (including Roman numerals), and handle Turkish-specific text operations. It's built to support natural language processing tasks for Turkish text.

## Features

- **Number to Text Conversion**: Convert numeric values to their Turkish text representation
- **Ordinal Number Normalization**: Convert ordinal numbers (including Roman numerals) to their Turkish text representation
- **Roman Numeral Processing**: Convert Roman numerals to Arabic numbers and normalize Roman ordinals in text
- **Turkish Suffix Handling**: Add Turkish suffixes (ile, ise, iken) to words following vowel harmony rules
- **Text Utilities**: Various text utility functions for Turkish language processing

## Installation

```bash
pip install trnorm
```

## Usage

### Number to Text Conversion

```python
from trnorm import NumberToTextConverter, convert_numbers_to_words_wrapper

# Convert a single number
converter = NumberToTextConverter()
print(converter.convert("42"))  # "kırk iki"

# Convert numbers in a text
text = "Bugün 25 Nisan 2025 tarihinde 42 kişi katıldı."
normalized = convert_numbers_to_words_wrapper(text)
print(normalized)  # "Bugün yirmi beş Nisan iki bin yirmi beş tarihinde kırk iki kişi katıldı."
```

### Ordinal Number Normalization

```python
from trnorm import normalize_ordinals

# Arabic ordinals
text = "1. sırada 2'nci kişi ve 3'üncü grup"
normalized = normalize_ordinals(text)
print(normalized)  # "birinci sırada ikinci kişi ve üçüncü grup"

# Roman ordinals
text = "XX. yüzyılda II. Dünya Savaşı yaşandı."
normalized = normalize_ordinals(text)
print(normalized)  # "yirminci yüzyılda ikinci Dünya Savaşı yaşandı."
```

### Roman Numeral Processing

```python
from trnorm import roman_to_arabic, is_roman_numeral

# Convert Roman numerals to Arabic numbers
print(roman_to_arabic("XIV"))  # 14
print(roman_to_arabic("MCMXCIX"))  # 1999

# Check if a string is a valid Roman numeral
print(is_roman_numeral("XIV"))  # True
print(is_roman_numeral("ABC"))  # False
```

### Turkish Suffix Handling

```python
from trnorm import ekle

# Add "ile" suffix (with)
print(ekle("Ankara", "ile"))  # "Ankarayla"
print(ekle("İstanbul", "ile"))  # "İstanbulla"

# Add "ise" suffix (if)
print(ekle("Ankara", "ise"))  # "Ankaraysa"
print(ekle("İstanbul", "ise"))  # "İstanbulsa"

# Add "iken" suffix (while/when)
print(ekle("çalışıyor", "iken"))  # "çalışıyorken"
print(ekle("evde", "iken"))  # "evdeyken"
```

### Text Utilities

```python
from trnorm import turkish_lower, turkish_upper, turkish_capitalize

print(turkish_lower("İSTANBUL"))  # "istanbul"
print(turkish_upper("istanbul"))  # "İSTANBUL"
print(turkish_capitalize("istanbul"))  # "İstanbul"
```

## Examples

The package includes several example scripts in the `examples` directory:

- `demo_ordinals.py`: Demonstrates ordinal number normalization
- `demo_iken.py`: Shows Turkish suffix handling
- `demo_text_utils.py`: Illustrates text utility functions

Additionally, there are more comprehensive demos in the `demos` directory:

- `roman_demo.py`: Demonstrates Roman numeral conversion and Roman ordinal normalization

## Development

### Running Tests

```bash
python -m unittest discover
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache License 2.0
