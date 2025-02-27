"""
Demo of symbol conversion functionality in the trnorm package.

This example demonstrates:
1. Converting percent symbols (%) to their text representation
2. Using the default symbol mappings for currencies
3. Adding custom symbol mappings
4. Converting multiple symbols in text
"""

from trnorm.symbols import SymbolConverter, convert_symbols, add_symbol_mapping
from trnorm.symbol_mappings import get_all_mappings


def demo_percent_conversion():
    """Demonstrate conversion of percent symbols."""
    print("\n=== Percent Symbol Conversion ===")
    
    examples = [
        "%50",
        "%10,5",
        "%99,9",
        "%22",
        "Rezerv oranım gene %10. Yani rezerv olarak 90 altın ayıracağım.",
        "Size %2 vereceğimize, 2 yıl vadeyle paranızı bizde tutacağınız için size %7 verelim.",
        "Bu çekirdek genlerimizin %99,9'unu içerir ve mitokondri'de de birkaç tane daha gen vardır.",
        "Herhangi bir zamanda vücuttaki tüm kanın yaklaşık %22'sini tutabilirler.",
        "Ve eğer daha yüksek, %7 ya da %8'den yüksekseniz, %7 ya da %8'den yüksek, yani eğer hemoglobin A1c seviyeniz sanki %9 ya da 10 ise, bu yüksek sayılır."
    ]
    
    for text in examples:
        normalized = convert_symbols(text)
        print(f"\nOriginal: {text}")
        print(f"Normalized: {normalized}")


def demo_currency_symbols():
    """Demonstrate using default currency symbol mappings."""
    print("\n=== Currency Symbol Conversion ===")
    print("In Turkish, currency names come after the number.")
    print("Currency symbols can appear before or after the number.")
    
    # Show available currency symbol mappings
    print("\nAvailable currency symbol mappings:")
    mappings = get_all_mappings()
    for symbol, (text, text_after) in mappings.items():
        if text_after:  # Only show currency symbols (text_after=True)
            print(f"  {symbol} -> {text}")
    
    # Examples with currency symbols before numbers
    print("\n--- Currency Symbols Before Numbers ---")
    examples_before = [
        "$50",
        "€60",
        "£100",
        "₺250",
        "$500 değerindeki ürün",
        "Fiyat: €75,5",
        "Toplam: £100,50"
    ]
    
    for text in examples_before:
        normalized = convert_symbols(text)
        print(f"\nOriginal: {text}")
        print(f"Normalized: {normalized}")
    
    # Examples with currency symbols after numbers
    print("\n--- Currency Symbols After Numbers ---")
    examples_after = [
        "50 $",
        "60 €",
        "100 £",
        "250 ₺",
        "500 $ değerindeki ürün",
        "Fiyat: 75,5 €",
        "Toplam: 100,50 £"
    ]
    
    for text in examples_after:
        normalized = convert_symbols(text)
        print(f"\nOriginal: {text}")
        print(f"Normalized: {normalized}")


def demo_custom_symbol_mapping():
    """Demonstrate adding a custom symbol mapping."""
    print("\n=== Custom Symbol Mapping ===")
    
    # Add a custom symbol mapping
    add_symbol_mapping("@", "et", False)  # @ symbol -> "et" (before number)
    
    examples = [
        "@50",
        "@10,5",
        "@99,9",
        "Email adresim @johndoe.",  # Should not be converted (no number)
        "Twitter hesabım @username değil @50 kullanıcısıdır."  # Only @50 should be converted
    ]
    
    for text in examples:
        normalized = convert_symbols(text)
        print(f"\nOriginal: {text}")
        print(f"Normalized: {normalized}")


def demo_mixed_symbols():
    """Demonstrate conversion of mixed symbols in text."""
    print("\n=== Mixed Symbol Conversion ===")
    print("Percent symbol text comes before the number, while currency text comes after.")
    
    examples = [
        # Currency symbols before numbers
        "%10 indirimli ürün $50'ye satılıyor.",
        "Fiyatlar: %10 indirim, $50, €75,5 ve £100.",
        "Dolar kurundaki %15'lik artış sonrası $100 şimdi €90 değerinde.",
        "$500 değerindeki ürün %20 indirimle satılıyor.",
        
        # Currency symbols after numbers
        "%10 indirimli ürün 50 $'ye satılıyor.",
        "Fiyatlar: %10 indirim, 50 $, 75,5 € ve 100 £.",
        "Dolar kurundaki %15'lik artış sonrası 100 $ şimdi 90 € değerinde.",
        "500 $ değerindeki ürün %20 indirimle satılıyor.",
        
        # Mixed position of currency symbols
        "Bazı ürünler $50, bazıları 60 € fiyatla satılıyor."
    ]
    
    for text in examples:
        normalized = convert_symbols(text)
        print(f"\nOriginal: {text}")
        print(f"Normalized: {normalized}")


def main():
    """Run all demonstrations."""
    print("=== Symbol Conversion Demo ===")
    print("This demo shows the symbol conversion functionality in the trnorm package.")
    
    demo_percent_conversion()
    demo_currency_symbols()
    demo_custom_symbol_mapping()
    demo_mixed_symbols()
    
    print("\nDemo completed!")


if __name__ == "__main__":
    main()
