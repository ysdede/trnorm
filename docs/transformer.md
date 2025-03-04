# Turkish Text Transformer

The `transformer` module provides a flexible, customizable approach to Turkish text normalization using a transformer pipeline. This approach allows you to specify which transformers to apply and in what order, giving you complete control over the normalization process.

## Key Features

- **Customizable Transformer Pipeline**: Choose which transformers to apply and in what order
- **Default Pipeline**: Pre-configured pipeline with the most common transformers in the recommended order
- **Custom Transformers**: Create and register your own transformers
- **Batch Processing**: Process both single strings and lists of strings
- **Simple API**: Easy-to-use functions for common use cases

## Available Transformers

The following transformers are available out of the box:

| Transformer Name | Description |
|------------------|-------------|
| `preprocess_dimensions` | Add spaces between numbers and multiplication symbols |
| `convert_symbols` | Convert symbols (%, $, etc.) to their text representation |
| `normalize_dimensions` | Replace multiplication symbol 'x' with 'çarpı' in dimensions |
| `convert_numbers` | Convert numbers to their text representation |
| `normalize_ordinals` | Convert ordinal numbers (1., 2., etc.) to their text representation |
| `normalize_units` | Convert unit abbreviations (cm, kg, etc.) to their full text |
| `lowercase` | Convert text to lowercase using Turkish-specific rules |
| `remove_hats` | Remove circumflex (hat) from Turkish characters |
| `legacy_normalize` | Apply legacy normalization (more aggressive, removes punctuation) |

## Default Transformer Pipeline

The default transformer pipeline applies the following transformers in order:

1. `preprocess_dimensions`
2. `convert_symbols`
3. `normalize_dimensions`
4. `convert_numbers`
5. `normalize_ordinals`
6. `normalize_units`
7. `remove_hats`
8. `lowercase`

This order ensures that all normalization steps work correctly together.

## Usage

### Basic Usage

```python
from trnorm import transform

# Normalize a single string using the default pipeline
text = "Bugün 15. kattaki 3 toplantıya katıldım."
normalized_text = transform(text)
print(normalized_text)
# Output: "bugün on beşinci kattaki üç toplantıya katıldım."

# Normalize a list of strings
texts = [
    "Saat 14:30'da %25 indirimli ürünler satışa çıkacak.",
    "II. Dünya Savaşı 1939-1945 yılları arasında gerçekleşti."
]
normalized_texts = transform(texts)
print(normalized_texts)
# Output: [
#   "saat on dört otuzda yüzde yirmi beş indirimli ürünler satışa çıkacak.",
#   "ikinci dünya savaşı bin dokuz yüz otuz dokuz bin dokuz yüz kırk beş yılları arasında gerçekleşti."
# ]
```

### Custom Transformer Pipeline

```python
from trnorm import transform

# Use a custom transformer pipeline
text = "Odanın boyutları 2x3x4 metre."
custom_pipeline = ["preprocess_dimensions", "normalize_dimensions", "convert_numbers"]
normalized_text = transform(text, transformers=custom_pipeline)
print(normalized_text)
# Output: "Odanın boyutları iki çarpı üç çarpı dört metre."
```

### Using the TransformerPipeline Class

```python
from trnorm import TransformerPipeline

# Create a custom transformer pipeline
pipeline = TransformerPipeline([
    "preprocess_dimensions",
    "normalize_dimensions",
    "convert_numbers",
    "normalize_units",
    "lowercase"
])

# Apply the pipeline to text
text = "Halının boyutu 120x180cm."
normalized_text = pipeline.apply(text)
print(normalized_text)
# Output: "halının boyutu yüz yirmi çarpı yüz seksen santimetre."
```

### Creating Custom Transformers

```python
from trnorm import create_custom_transformer, register_transformer, TransformerPipeline

# Define a custom transformer function
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

# Create and register the custom transformer
month_transformer = create_custom_transformer(
    name="replace_month_names",
    func=replace_turkish_month_names,
    description="Replace Turkish month names with their numeric representation"
)
register_transformer(month_transformer)

# Create a pipeline with the custom transformer
custom_pipeline = TransformerPipeline([
    "replace_month_names",
    "convert_numbers",
    "lowercase"
])

# Apply the pipeline
text = "5 Ocak 2023 tarihinde toplantı var."
normalized = custom_pipeline.apply(text)
print(normalized)
# Output: "beş bir iki bin yirmi üç tarihinde toplantı var."
```

### Getting Available Transformers

```python
from trnorm import get_available_transformers

# Get all available transformers and their descriptions
transformers = get_available_transformers()
for name, description in transformers.items():
    print(f"{name}: {description}")
```

## Comparison with TurkishNormalizer

The transformer-based approach provides more flexibility than the `TurkishNormalizer` class:

1. **Customizable Order**: With `TransformerPipeline`, you can specify the exact order of transformations.
2. **Selective Application**: You can choose exactly which transformers to apply.
3. **Extensibility**: You can easily create and register custom transformers.
4. **Clarity**: The pipeline approach makes it clear which transformations are being applied.

However, `TurkishNormalizer` provides a simpler interface for common use cases. Choose the approach that best fits your needs:

- Use `TurkishNormalizer` for simple, predefined normalization with boolean flags.
- Use `TransformerPipeline` for complete control over the normalization process.

## Integration with Benchmarking Code

When integrating with benchmarking code, you can create a custom pipeline that matches your specific requirements:

```python
from trnorm import TransformerPipeline

# Create a pipeline for your benchmarking needs
benchmark_pipeline = TransformerPipeline([
    "preprocess_dimensions",
    "normalize_dimensions",
    "convert_numbers",
    "normalize_ordinals",
    "normalize_units",
    "lowercase"
])

# Process your benchmark data
benchmark_results = []
for reference, hypothesis in benchmark_data:
    normalized_reference = benchmark_pipeline.apply(reference)
    normalized_hypothesis = benchmark_pipeline.apply(hypothesis)
    # Calculate metrics using normalized texts
    # ...
    benchmark_results.append(result)
```

This approach allows you to easily customize the normalization process for your specific benchmarking requirements.

## Transformer Module

### Overview

The transformer module provides a flexible approach to Turkish text normalization using a pipeline of transformers. Each transformer performs a specific normalization step, and users can customize which transformers to apply and in what order.

### Key Features

- **Customizable Pipelines**: Create pipelines with specific transformers and ordering
- **Default Pipeline**: Recommended set of transformers in optimal order
- **Extensible**: Easily add custom transformers
- **Efficient**: Process both single strings and lists of strings

### Available Transformers

| Transformer Name | Description |
|------------------|-------------|
| `preprocess_dimensions` | Add spaces between numbers and multiplication symbols |
| `convert_symbols` | Convert symbols (%, $, etc.) to their text representation |
| `normalize_dimensions` | Replace multiplication symbol 'x' with 'çarpı' in dimensions |
| `convert_numbers` | Convert numbers to their text representation |
| `normalize_ordinals` | Convert ordinal numbers (1., 2., etc.) to their text representation |
| `normalize_units` | Convert unit abbreviations (cm, kg, etc.) to their full text |
| `lowercase` | Convert text to lowercase using Turkish-specific rules |
| `remove_hats` | Remove circumflex (hat) from Turkish characters |
| `legacy_normalize` | Apply legacy normalization (more aggressive, removes punctuation) |

### Usage Examples

### Default Pipeline
```python
from trnorm import TransformerPipeline

pipeline = TransformerPipeline()
normalized_text = pipeline.apply("Bugün 15. kattaki 3 toplantıya katıldım.")
```

### Custom Pipeline
```python
custom_pipeline = TransformerPipeline([
    'convert_numbers',
    'normalize_ordinals',
    'lowercase'
])
```

### Creating Custom Transformers
```python
from trnorm import create_custom_transformer, register_transformer

def my_custom_transformer(text):
    # Custom transformation logic
    return transformed_text

custom_transformer = create_custom_transformer(
    name='my_transformer',
    func=my_custom_transformer,
    description='My custom text transformation'
)
register_transformer(custom_transformer)
```

### Benchmarking

The transformer approach is particularly useful for ASR benchmarking, allowing researchers to:

- Test different normalization strategies
- Measure the impact of specific transformers on WER/CER
- Create custom pipelines tailored to specific datasets

See `benchmarking_example.py` for a complete example.

### Best Practices

1. Use the default pipeline as a starting point
2. Test different transformer combinations to optimize for your specific use case
3. Create custom transformers for domain-specific normalization needs
4. Document any custom pipelines for reproducibility

### API Reference

### TransformerPipeline
```python
class TransformerPipeline:
    def __init__(self, transformers: Optional[List[str]] = None):
        """Initialize with list of transformer names"""

    def apply(self, text: Union[str, List[str]]) -> Union[str, List[str]]:
        """Apply all transformers in sequence"""
```

### Transformer
```python
class Transformer:
    def __init__(self, name: str, func: TransformerFunc, description: str, **kwargs):
        """Initialize a transformer"""

    def __call__(self, text: str) -> str:
        """Apply the transformation"""
