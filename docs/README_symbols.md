# Symbol Conversion Module

The `symbols` module in the `trnorm` package provides functionality for converting special symbols in Turkish text to their text representations. This is particularly useful for text normalization in natural language processing applications.

## Features

- Convert percent symbols (`%`) to their Turkish text representation ("yüzde")
- Convert currency symbols (`$`, `€`, `£`, `₺`, etc.) to their Turkish text representation
- Handle symbols both before and after numbers
- Support for apostrophes in Turkish text (e.g., `%50'si`, `$100'e`)
- Extensible design allowing for easy addition of new symbol mappings

## Usage

### Basic Usage

```python
from trnorm import convert_symbols

# Convert percent symbols
text = "Rezerv oranım gene %10. Yani rezerv olarak 90 altın ayıracağım."
normalized = convert_symbols(text)
# Result: "Rezerv oranım gene yüzde 10. Yani rezerv olarak 90 altın ayıracağım."

# Convert currency symbols (before numbers)
text = "$50 değerindeki ürün"
normalized = convert_symbols(text)
# Result: "50 dolar değerindeki ürün"

# Convert currency symbols (after numbers)
text = "Fiyat: 75,5 €"
normalized = convert_symbols(text)
# Result: "Fiyat: 75,5 avro"

# Convert mixed symbols
text = "%10 indirimli ürün $50'ye satılıyor."
normalized = convert_symbols(text)
# Result: "yüzde 10 indirimli ürün 50 dolar'ye satılıyor."
```

### Adding Custom Symbol Mappings

You can add your own symbol mappings using the `add_symbol_mapping` function:

```python
from trnorm import add_symbol_mapping, convert_symbols

# Add a custom symbol mapping
add_symbol_mapping("@", "et", False)  # @ symbol -> "et" (before number)

# Test the custom mapping
text = "Twitter hesabım @username değil @50 kullanıcısıdır."
normalized = convert_symbols(text)
# Result: "Twitter hesabım @username değil et 50 kullanıcısıdır."
```

### Creating a Custom Converter

For more advanced use cases, you can create your own `SymbolConverter` instance:

```python
from trnorm import SymbolConverter

# Create a custom converter without loading default mappings
converter = SymbolConverter(load_defaults=False)

# Add custom mappings
converter.add_symbol_mapping("@", "et", False)
converter.add_symbol_mapping("#", "numara", False)

# Convert text using the custom converter
text = "@50 ve #20"
normalized = converter.convert_all_symbols(text)
# Result: "et 50 ve numara 20"
```

## Symbol Mappings

The default symbol mappings are defined in the `symbol_mappings.py` module. The current mappings include:

### Percent Symbol
- `%` → "yüzde" (text appears before the number)

### Currency Symbols
- `$` → "dolar" (text appears after the number)
- `€` → "avro" (text appears after the number)
- `£` → "sterlin" (text appears after the number)
- `₺` → "lira" (text appears after the number)
- And many more currency symbols

## Extending Symbol Mappings

You can extend the symbol mappings in two ways:

### 1. At Runtime

```python
from trnorm import add_symbol_mapping

# Add a new symbol mapping
add_symbol_mapping("§", "paragraf", False)  # § symbol -> "paragraf" (before number)
```

### 2. By Modifying the `symbol_mappings.py` File

You can directly modify the `SYMBOL_MAPPINGS` dictionary in the `symbol_mappings.py` file:

```python
# Add to the SYMBOL_MAPPINGS dictionary
SYMBOL_MAPPINGS = {
    # Existing mappings...
    
    # New mapping
    "§": ("paragraf", False),
}
```

## Technical Details

The `SymbolConverter` class uses regular expressions to match symbols both before and after numbers. It handles special cases like apostrophes in Turkish text and preserves them in the output.

The `text_after` parameter in symbol mappings determines whether the text representation should appear before or after the number:
- If `text_after=True`, the text appears after the number (e.g., for currencies in Turkish)
- If `text_after=False`, the text appears before the number (e.g., for percent)

## Examples

See the `examples/demo_symbols.py` file for more examples of how to use the symbol conversion functionality.
