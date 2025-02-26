import unittest

import sys
import os

# Add parent directory to path to allow imports from parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trnorm.num_to_text import NumberToTextConverter, convert_numbers_to_words_wrapper

class TestTurkishNumberConverter(unittest.TestCase):
    def setUp(self):
        self.converter = NumberToTextConverter()

    def test_basic_numbers(self):
        """Test basic numbers from 0-999"""
        test_cases = {
            "0": "sıfır",
            "5": "beş",
            "10": "on",
            "15": "on beş",
            "20": "yirmi",
            "42": "kırk iki",
            "100": "yüz",
            "101": "yüz bir",
            "200": "iki yüz",
            "345": "üç yüz kırk beş",
            "999": "dokuz yüz doksan dokuz"
        }
        for number, expected in test_cases.items():
            self.assertEqual(self.converter.convert_numbers_to_words(number), expected)

    def test_thousands(self):
        """Test numbers with thousands (1000-999999)"""
        test_cases = {
            "1000": "bin",
            "1001": "bin bir",
            "1100": "bin yüz",
            "1500": "bin beş yüz",
            "1999": "bin dokuz yüz doksan dokuz",
            "2000": "iki bin",
            "2001": "iki bin bir",
            "2345": "iki bin üç yüz kırk beş",
            "10000": "on bin",
            "20000": "yirmi bin",
            "100000": "yüz bin",
            "234567": "iki yüz otuz dört bin beş yüz altmış yedi"
        }
        for number, expected in test_cases.items():
            self.assertEqual(self.converter.convert_numbers_to_words(number), expected)

    def test_millions_and_above(self):
        """Test numbers in millions, billions and above"""
        test_cases = {
            "1000000": "bir milyon",
            "1000001": "bir milyon bir",
            "1000100": "bir milyon yüz",
            "2500000": "iki milyon beş yüz bin",
            "5000000": "beş milyon",  # This was the original issue case
            "10000000": "on milyon",
            "1000000000": "bir milyar",
            "1000000001": "bir milyar bir",
            "1234567890": "bir milyar iki yüz otuz dört milyon beş yüz altmış yedi bin sekiz yüz doksan"
        }
        for number, expected in test_cases.items():
            self.assertEqual(self.converter.convert_numbers_to_words(number), expected)

    def test_decimal_numbers(self):
        """Test decimal numbers with comma as separator"""
        test_cases = {
            "0,5": "sıfır virgül beş",
            "1,5": "bir virgül beş",
            "10,05": "on virgül sıfır beş",
            "100,75": "yüz virgül yetmiş beş",
            "1000,123": "bin virgül yüz yirmi üç",
            "1000000,99": "bir milyon virgül doksan dokuz"
        }
        for number, expected in test_cases.items():
            self.assertEqual(self.converter.convert_numbers_to_words(number), expected)

    def test_numbers_with_thousand_separators(self):
        """Test numbers with period as thousand separator"""
        test_cases = {
            "1.000": "bin",
            "10.000": "on bin",
            "100.000": "yüz bin",
            "1.000.000": "bir milyon",
            "1.234.567": "bir milyon iki yüz otuz dört bin beş yüz altmış yedi",
            "1.000.000.000": "bir milyar",
            "999.999.999": "dokuz yüz doksan dokuz milyon dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz"
        }
        for number, expected in test_cases.items():
            self.assertEqual(self.converter.convert_numbers_to_words(number), expected)

    def test_mixed_format_numbers(self):
        """Test numbers with both thousand separators and decimals"""
        test_cases = {
            "1.234,56": "bin iki yüz otuz dört virgül elli altı",
            "1.000.000,99": "bir milyon virgül doksan dokuz",
            "999.999,999": "dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz virgül dokuz yüz doksan dokuz"
        }
        for number, expected in test_cases.items():
            self.assertEqual(self.converter.convert_numbers_to_words(number), expected)

    def test_numbers_in_text(self):
        """Test numbers embedded in text"""
        test_cases = {
            "Fiyat: 1.234,56 TL": "Fiyat: bin iki yüz otuz dört virgül elli altı TL",
            "Toplam: 1.000.000 adet": "Toplam: bir milyon adet",
            "Mesafe: 5,5 km": "Mesafe: beş virgül beş km"
        }
        for text, expected in test_cases.items():
            self.assertEqual(self.converter.convert_numbers_to_words(text), expected)

    def test_dates_to_text(self):
        """Test dates to text conversion with various date separators (-, /, space, period) in ddmmyyyy format"""
        test_cases = {
            # Dates with hyphen separator
            "01-01-2023": "bir bir iki bin yirmi üç",
            "15-06-2023": "on beş altı iki bin yirmi üç",
            "31-12-2023": "otuz bir on iki iki bin yirmi üç",
            
            # Dates with slash separator
            "01/01/2023": "bir bir iki bin yirmi üç",
            "15/06/2023": "on beş altı iki bin yirmi üç",
            "31/12/2023": "otuz bir on iki iki bin yirmi üç",
            
            # Dates with period separator
            "01.01.2023": "bir bir iki bin yirmi üç",
            "15.06.2023": "on beş altı iki bin yirmi üç",
            "31.12.2023": "otuz bir on iki iki bin yirmi üç",
            
            # Dates with two-digit year
            "01-01-23": "bir bir yirmi üç",
            "15-06-23": "on beş altı yirmi üç",
            "31-12-23": "otuz bir on iki yirmi üç",
            
            # Dates with single-digit day/month
            "1-1-2023": "bir bir iki bin yirmi üç",
            "5-6-2023": "beş altı iki bin yirmi üç",
            "9-9-2023": "dokuz dokuz iki bin yirmi üç"
        }
        for date, expected in test_cases.items():
            self.assertEqual(self.converter.convert_numbers_to_words(date), expected)

if __name__ == '__main__':
    unittest.main()
