"""
Tests for the symbols module.
"""

import unittest
from trnorm.symbols import SymbolConverter, convert_symbols


class TestSymbols(unittest.TestCase):
    """Test cases for the symbols module."""

    def test_percent_symbol_conversion(self):
        """Test conversion of percent symbol."""
        test_cases = [
            ("%50", "yüzde 50"),
            ("%10,5", "yüzde 10,5"),
            ("%99,9", "yüzde 99,9"),
            ("%22", "yüzde 22"),
            ("%7", "yüzde 7"),
            ("%8", "yüzde 8"),
            ("%9", "yüzde 9"),
            ("%10", "yüzde 10"),
        ]
        
        for input_text, expected_output in test_cases:
            self.assertEqual(convert_symbols(input_text), expected_output)
    
    def test_percent_symbol_in_sentences(self):
        """Test conversion of percent symbol in sentences."""
        test_cases = [
            (
                "Rezerv oranım gene %10. Yani rezerv olarak 90 altın ayıracağım.",
                "Rezerv oranım gene yüzde 10. Yani rezerv olarak 90 altın ayıracağım."
            ),
            (
                "Size %2 vereceğimize, 2 yıl vadeyle paranızı bizde tutacağınız için size %7 verelim.",
                "Size yüzde 2 vereceğimize, 2 yıl vadeyle paranızı bizde tutacağınız için size yüzde 7 verelim."
            ),
            (
                "Bu çekirdek genlerimizin %99,9'unu içerir ve mitokondri'de de birkaç tane daha gen vardır.",
                "Bu çekirdek genlerimizin yüzde 99,9'unu içerir ve mitokondri'de de birkaç tane daha gen vardır."
            ),
            (
                "Herhangi bir zamanda vücuttaki tüm kanın yaklaşık %22'sini tutabilirler.",
                "Herhangi bir zamanda vücuttaki tüm kanın yaklaşık yüzde 22'sini tutabilirler."
            ),
            (
                "Ve eğer daha yüksek, %7 ya da %8'den yüksekseniz, %7 ya da %8'den yüksek, yani eğer hemoglobin A1c seviyeniz sanki %9 ya da 10 ise, bu yüksek sayılır.",
                "Ve eğer daha yüksek, yüzde 7 ya da yüzde 8'den yüksekseniz, yüzde 7 ya da yüzde 8'den yüksek, yani eğer hemoglobin A1c seviyeniz sanki yüzde 9 ya da 10 ise, bu yüksek sayılır."
            ),
        ]
        
        for input_text, expected_output in test_cases:
            self.assertEqual(convert_symbols(input_text), expected_output)
    
    def test_currency_symbol_conversion(self):
        """Test conversion of currency symbols with text after the number."""
        # Test currency symbols before numbers
        test_cases_before = [
            ("$50", "50 dolar"),
            ("$10,5", "10,5 dolar"),
            ("$99,9'u", "99,9'u dolar"),
            ("€60", "60 avro"),
            ("€75,5", "75,5 avro"),
            ("£100", "100 sterlin"),
            ("%50 ve $25", "yüzde 50 ve 25 dolar"),
        ]
        
        for input_text, expected_output in test_cases_before:
            self.assertEqual(convert_symbols(input_text), expected_output)
            
        # Test currency symbols after numbers
        test_cases_after = [
            ("50 $", "50 dolar"),
            ("10,5 $", "10,5 dolar"),
            ("99,9'u $", "99,9'u dolar"),
            ("60 €", "60 avro"),
            ("75,5 €", "75,5 avro"),
            ("100 £", "100 sterlin"),
            ("%50 ve 25 $", "yüzde 50 ve 25 dolar"),
        ]
        
        for input_text, expected_output in test_cases_after:
            self.assertEqual(convert_symbols(input_text), expected_output)
    
    def test_mixed_symbols(self):
        """Test conversion of mixed symbols (before and after) in the same text."""
        test_cases = [
            (
                "Fiyatlar: %10 indirim, $50, €75,5 ve £100.",
                "Fiyatlar: yüzde 10 indirim, 50 dolar, 75,5 avro ve 100 sterlin."
            ),
            (
                "Dolar kurundaki %15'lik artış sonrası $100 şimdi €90 değerinde.",
                "Dolar kurundaki yüzde 15'lik artış sonrası 100 dolar şimdi 90 avro değerinde."
            ),
            (
                "$500 değerindeki ürün %20 indirimle satılıyor.",
                "500 dolar değerindeki ürün yüzde 20 indirimle satılıyor."
            ),
            (
                "Fiyatlar: %10 indirim, 50 $, 75,5 € ve 100 £.",
                "Fiyatlar: yüzde 10 indirim, 50 dolar, 75,5 avro ve 100 sterlin."
            ),
            (
                "Dolar kurundaki %15'lik artış sonrası 100 $ şimdi 90 € değerinde.",
                "Dolar kurundaki yüzde 15'lik artış sonrası 100 dolar şimdi 90 avro değerinde."
            ),
            (
                "500 $ değerindeki ürün %20 indirimle satılıyor.",
                "500 dolar değerindeki ürün yüzde 20 indirimle satılıyor."
            ),
            (
                "Bazı ürünler $50, bazıları 60 € fiyatla satılıyor.",
                "Bazı ürünler 50 dolar, bazıları 60 avro fiyatla satılıyor."
            ),
        ]
        
        for input_text, expected_output in test_cases:
            self.assertEqual(convert_symbols(input_text), expected_output)
    
    def test_custom_symbol_mapping(self):
        """Test adding a custom symbol mapping."""
        # Create a custom converter
        converter = SymbolConverter(load_defaults=False)
        
        # Add a custom symbol mapping
        converter.add_symbol_mapping("@", "et", False)  # @ symbol -> "et" (before number)
        
        test_cases = [
            ("@50", "et 50"),
            ("@10,5", "et 10,5"),
            ("@99,9", "et 99,9"),
            ("Email adresim @johndoe.", "Email adresim @johndoe."),  # Should not be converted (no number)
            ("Twitter hesabım @username değil @50 kullanıcısıdır.", "Twitter hesabım @username değil et 50 kullanıcısıdır.")  # Only @50 should be converted
        ]
        
        for input_text, expected_output in test_cases:
            self.assertEqual(converter.convert_all_symbols(input_text), expected_output)


if __name__ == "__main__":
    unittest.main()
