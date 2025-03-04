# Basic Turkish Text Normalizer

This document explains the simplified approach to Turkish text normalization that has been implemented in the `trnorm` package.

## Overview

The new implementation provides a simple, straightforward approach that allows you to manually import conversion functions and apply them iteratively to text. This approach is more robust and easier to understand than the previous complex architecture.

## Key Features

1. Simple function-based approach instead of complex class hierarchies
2. Direct control over which conversion functions to apply and in what order
3. Easy to extend with custom conversion functions
4. Support for both single strings and lists of strings

## How to Use

### Basic Usage

```python
from trnorm import normalize
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.legacy_normalizer import turkish_lower

# Apply a single conversion function
normalized_text = normalize("Bugün 15 kişi geldi.", [convert_numbers_to_words_wrapper])
# Result: "Bugün on beş kişi geldi."

# Apply multiple conversion functions in sequence
normalized_text = normalize("Bugün 15 kişi geldi.", [
    convert_numbers_to_words_wrapper,
    turkish_lower
])
# Result: "bugün on beş kişi geldi."
```

### Available Conversion Functions

The `trnorm` package provides many conversion functions that you can import and use:

```python
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.ordinals import normalize_ordinals
from trnorm.symbols import convert_symbols
from trnorm.legacy_normalizer import normalize_text, replace_hatted_characters, turkish_lower
from trnorm.dimension_utils import preprocess_dimensions, normalize_dimensions
from trnorm.unit_utils import normalize_units
```

### Creating Different Converter Sets for Different Tasks

You can create different lists of conversion functions for different normalization tasks:

```python
# Number and symbol conversion only
number_symbol_converters = [
    convert_symbols,
    convert_numbers_to_words_wrapper
]

# Full text normalization
full_normalization_converters = [
    preprocess_dimensions,
    convert_symbols,
    normalize_dimensions,
    convert_numbers_to_words_wrapper,
    normalize_ordinals,
    normalize_units,
    replace_hatted_characters,
    turkish_lower
]

# Legacy normalization (aggressive)
legacy_converters = [
    normalize_text
]

# Apply different converter sets to the same text
text = "Ürün boyutları 120x180cm ve fiyatı 1.250,75 TL'dir."

number_symbol_result = normalize(text, number_symbol_converters)
full_result = normalize(text, full_normalization_converters)
legacy_result = normalize(text, legacy_converters)
```

### Processing Lists of Texts

The `normalize` function can process both single strings and lists of strings:

```python
texts = [
    "Bugün 15. kattaki 3 toplantıya katıldım.",
    "Saat 14:30'da %25 indirimli ürünler satışa çıkacak."
]

normalized_texts = normalize(texts, full_normalization_converters)
```

### Creating Custom Conversion Functions

You can easily create your own conversion functions and add them to the normalization process:

```python
def replace_turkish_month_names(text):
    """Replace Turkish month names with their numeric representation."""
    month_mapping = {
        "ocak": "1",
        "şubat": "2",
        # ... other months
    }
    
    result = text
    for month, number in month_mapping.items():
        result = result.replace(month, number)
        result = result.replace(month.capitalize(), number)
    
    return result

# Add your custom function to the converter list
custom_converters = [
    replace_turkish_month_names,
    convert_numbers_to_words_wrapper,
    turkish_lower
]

normalized_text = normalize("5 Ocak 2023 tarihinde toplantı var.", custom_converters)
# Result: "beş bir iki bin yirmi üç tarihinde toplantı var."
```

## Examples

See the following example files for more detailed usage:
- `examples/basic_normalizer_example.py`: Comprehensive examples of the basic normalizer
- `examples/process_asr_logs.py`: Example of using the normalizer for ASR log processing

## Benefits of the New Approach

1. **Simplicity**: The API is much simpler and easier to understand
2. **Flexibility**: You have direct control over which conversion functions to apply and in what order
3. **Extensibility**: You can easily create and add custom conversion functions
4. **Transparency**: The normalization process is clear and explicit
5. **Robustness**: No complex architecture or dependencies to worry about
