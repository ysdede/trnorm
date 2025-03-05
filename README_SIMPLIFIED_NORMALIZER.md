# Simplified Turkish Text Normalizer

This document explains the simplified approach to Turkish text normalization that has been implemented in the `trnorm` package.

## Overview

The previous implementation of the Turkish normalizer was bloated with many optional parameters and a complex class structure. The new implementation provides a simpler, more flexible approach using the transformer-based architecture that was already available in the package.

## Key Changes

1. Removed the `TurkishNormalizer` class with its many optional parameters
2. Simplified the `normalize()` function to use the transformer-based approach
3. Added helper functions to make the API more user-friendly
4. Updated examples to demonstrate the new approach

## How to Use

### Basic Usage

```python
from trnorm import normalize

# Use default normalizers
normalized_text = normalize("Bugün 15. kattaki 3 toplantıya katıldım.")
# Result: "bugün on beşinci kattaki üç toplantıya katıldım."

# Use custom normalizers
normalized_text = normalize("Dün 3x4 metre halı aldım.", 
                           transformers=["normalize_dimensions", "convert_numbers"])
# Result: "Dün üç çarpı dört metre halı aldım."
```

### Available Normalizers

You can get a list of all available normalizers with their descriptions:

```python
from trnorm import get_available_normalizers

normalizers = get_available_normalizers()
for name, description in normalizers.items():
    print(f"{name}: {description}")
```

Available normalizers include:
- `preprocess_dimensions`: Add spaces between numbers and multiplication symbols
- `convert_symbols`: Convert symbols (%, $, etc.) to their text representation
- `normalize_dimensions`: Replace multiplication symbol 'x' with 'çarpı' in dimensions
- `convert_numbers`: Convert numbers to their text representation
- `normalize_ordinals`: Convert ordinal numbers (1., 2., etc.) to their text representation
- `normalize_units`: Convert unit abbreviations (cm, kg, etc.) to their full text
- `lowercase`: Convert text to lowercase using Turkish-specific rules
- `remove_hats`: Remove circumflex (hat) from Turkish characters
- `legacy_normalize`: Apply legacy normalization (more aggressive, removes punctuation)

### Creating a Reusable Pipeline

If you need to apply the same normalization steps to multiple texts, you can create a reusable pipeline:

```python
from trnorm import create_normalizer_pipeline

# Create a pipeline with custom normalizers
pipeline = create_normalizer_pipeline([
    "preprocess_dimensions",
    "normalize_dimensions",
    "convert_numbers",
    "normalize_units",
    "lowercase"
])

# Apply the pipeline to multiple texts
texts = [
    "Odanın boyutları 2x3x4 metre.",
    "Halının boyutu 120x180cm."
]

for text in texts:
    normalized = pipeline.apply(text)
    print(normalized)
```

## Examples

See the following example files for more detailed usage:
- `examples/simple_normalizer_example.py`: Basic usage of the simplified normalizer
- `examples/transformer_example.py`: More advanced usage with custom transformers

## Migration from the Old API

If you were using the old API with optional parameters like:

```python
normalize(text, apply_legacy_normalization=True, apply_apostrophe_handling=True)
```

You should now use the transformer-based approach:

```python
normalize(text, transformers=["legacy_normalize"])
```

The available transformers correspond to the previous optional parameters:
- `apply_number_conversion` → `"convert_numbers"`
- `apply_ordinal_normalization` → `"normalize_ordinals"`
- `apply_symbol_conversion` → `"convert_symbols"`
- `apply_multiplication_symbol` → `"normalize_dimensions"`
- `apply_unit_normalization` → `"normalize_units"`
- `apply_legacy_normalization` → `"legacy_normalize"`
- `lowercase` → `"lowercase"`
- `remove_hats` → `"remove_hats"`

## Benefits of the New Approach

1. **Simplicity**: The API is much simpler and easier to understand
2. **Flexibility**: You can easily customize which normalizers to apply and in what order
3. **Extensibility**: You can create and register custom normalizers
4. **Reusability**: You can create reusable pipelines for specific normalization tasks
5. **Consistency**: The normalizer now uses the same transformer-based approach that was already available in the package
