# TRNorm

Turkish text normalization tools for ASR (Automatic Speech Recognition) benchmarking and evaluation.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Overview

TRNorm is a specialized Python package designed for normalizing Turkish text in ASR evaluation contexts. It provides tools to standardize text representations of numbers, ordinals, and symbols to ensure fair comparison between ASR system outputs and reference transcriptions.

This package is specifically created for fairer ASR benchmarking, not as a comprehensive Turkish NLP solution. The primary goal is to normalize references and predictions to enable more accurate evaluation of ASR models and to mitigate errors from weakly labeled audio datasets.

## Features

- **Number to Text Conversion**: Convert numeric values to their Turkish text representation
- **Ordinal Number Normalization**: Convert ordinal numbers to their Turkish text representation
- **Roman Numeral Processing**: Convert Roman numerals to Arabic numbers and optionally normalize Roman ordinals in text
- **Symbol Conversion**: Convert special symbols (like %, €, $) to their text representation
- **Turkish Suffix Handling**: Add Turkish suffixes (ile, ise, iken) to words following vowel harmony rules
- **Text Utilities**: Various text utility functions for Turkish language processing
- **Metrics**: Text similarity metrics (WER, CER, Levenshtein distance)
- **Legacy Normalizer**: Backward compatibility with previous normalizer implementation

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

# Convert numbers with apostrophes
text = "1960'lı yıllarda 100'lerce insan katıldı."
normalized = convert_numbers_to_words_wrapper(text)
print(normalized)  # "bin dokuz yüz altmış'lı yıllarda yüz'lerce insan katıldı."

# Convert numbers with divide symbols
text = "7/24 hizmet veriyoruz ve işin 2/3'ü tamamlandı."
normalized = convert_numbers_to_words_wrapper(text)
print(normalized)  # "yedi/yirmi dört hizmet veriyoruz ve işin iki/üç'ü tamamlandı."
```

### Ordinal Number Normalization

```python
from trnorm import normalize_ordinals

# Arabic ordinals
text = "1. sırada 2'nci kişi ve 3'üncü grup"
normalized = normalize_ordinals(text)
print(normalized)  # "birinci sırada ikinci kişi ve üçüncü grup"

# Roman ordinals (disabled by default)
text = "XX. yüzyılda II. Dünya Savaşı yaşandı."
# Default behavior - Roman ordinals are not converted
normalized = normalize_ordinals(text)
print(normalized)  # "XX. yüzyılda II. Dünya Savaşı yaşandı."

# Enable Roman ordinals conversion
normalized = normalize_ordinals(text, convert_roman_ordinals=True)
print(normalized)  # "yirminci yüzyılda ikinci Dünya Savaşı yaşandı."
```

### Roman Numeral Processing

```python
from trnorm import roman_to_arabic, is_roman_numeral, find_roman_ordinals

# Convert Roman numerals to Arabic numbers
print(roman_to_arabic("XIV"))  # 14
print(roman_to_arabic("MCMXCIX"))  # 1999

# Check if a string is a valid Roman numeral
print(is_roman_numeral("XIV"))  # True
print(is_roman_numeral("ABC"))  # False

# Find Roman ordinals in text
text = "XX. yüzyılda II. Dünya Savaşı yaşandı."
ordinals = find_roman_ordinals(text)
print(ordinals)  # [('XX', 'yüzyılda', 0), ('II', 'Dünya', 12)]
```

### Symbol Conversion

```python
from trnorm import convert_symbols

# Convert symbols to text
text = "Ürün %20 indirimli ve fiyatı 50€."
normalized = convert_symbols(text)
print(normalized)  # "Ürün yüzde yirmi indirimli ve fiyatı elli avro."
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

### Metrics

```python
from trnorm import wer, cer, levenshtein_distance

reference = "bu bir test cümlesidir"
hypothesis = "bu bir deneme cümlesi"

print(wer(reference, hypothesis))  # Word Error Rate
print(cer(reference, hypothesis))  # Character Error Rate
print(levenshtein_distance(reference, hypothesis))  # Levenshtein Distance
```

### Legacy Normalizer

```python
from trnorm import normalize_text, replace_hatted_characters

# Basic normalization
text = "âîôû Çok iyi ve nazik biriydi. Prusya'daki ilk karşılaşmamızda onu konuşturmayı başarmıştım."
normalized = normalize_text(text)
print(normalized)  # "aiou çok iyi ve nazik biriydi prusyadaki ilk karşılaşmamızda onu konuşturmayı başarmıştım"

# Only replace hatted characters
text_with_hats = "âîôû Çok iyi"
print(replace_hatted_characters(text_with_hats))  # "aiou Çok iyi"

# Process a list of texts
texts = ["Turner'ın 'Köle Gemisi' isimli tablosuna bakıyoruz.", "Turner'ın Köle Gemisi isimli tablosuna bakıyoruz."]
normalized_texts = normalize_text(texts)
```

## Examples

The package includes several example scripts in the `examples` directory:

- `demo_ordinals.py`: Demonstrates ordinal number normalization
- `demo_iken.py`: Shows Turkish suffix handling
- `demo_text_utils.py`: Illustrates text utility functions
- `demo_num_to_text.py`: Shows number to text conversion
- `demo_metrics.py`: Demonstrates text similarity metrics
- `demo_legacy_normalizer.py`: Shows legacy normalizer functionality

## Development

### Running Tests

```bash
python -m unittest discover
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache License 2.0
