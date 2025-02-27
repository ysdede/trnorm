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

    def test_numbers_with_apostrophes(self):
        """Test numbers with apostrophes, which should convert the number part but preserve the suffix"""
        test_cases = {
            # Basic cases with different suffixes
            "1960'lı": "bin dokuz yüz altmış'lı",
            "67'ler": "altmış yedi'ler",
            "100'lerce": "yüz'lerce",
            "2000'li": "iki bin'li",
            "80'ler": "seksen'ler",
            "30'ar": "otuz'ar",
            "1990'ların": "bin dokuz yüz doksan'ların",
            "1000'den": "bin'den",
            "50'şer": "elli'şer",
            "200'ü": "iki yüz'ü",
            
            # Edge cases
            "0'dan": "sıfır'dan",
            "1.000'lik": "bin'lik",  # With thousand separator
            "1,5'lik": "bir virgül beş'lik",  # With decimal
            "1.234,56'lık": "bin iki yüz otuz dört virgül elli altı'lık",  # Complex number
            
            # Numbers with apostrophes in text
            "1960'lı yıllarda": "bin dokuz yüz altmış'lı yıllarda",
            "67'ler kuşağı": "altmış yedi'ler kuşağı",
            "100'lerce insan": "yüz'lerce insan",
            "Türkiye'de 80'ler müziği": "Türkiye'de seksen'ler müziği",
            "Sınıfta 30'ar kişilik": "Sınıfta otuz'ar kişilik",
            "Depremde 1000'den fazla": "Depremde bin'den fazla",
            "Toplantıya 200'ü aşkın": "Toplantıya iki yüz'ü aşkın",
            
            # Additional edge cases (focusing only on apostrophe handling, not ordinals)
            "42'ye kadar": "kırk iki'ye kadar",  # With dative case
            "100'e yakın": "yüz'e yakın",  # With dative case
            "15'i geçti": "on beş'i geçti",  # With accusative case
            "7'si geldi": "yedi'si geldi",  # With possessive
            
            # Multiple apostrophes in a sentence
            "1960'lı yılların 70'li dönemleri": "bin dokuz yüz altmış'lı yılların yetmiş'li dönemleri",
            "100'lerce insan 1000'lerce kitap okudu": "yüz'lerce insan bin'lerce kitap okudu",
            
            # Mixed with punctuation and special characters
            "1960'lı, 70'li ve 80'li yıllar": "bin dokuz yüz altmış'lı, yetmiş'li ve seksen'li yıllar",
            "2000'den önce, 1990'ların sonunda": "iki bin'den önce, bin dokuz yüz doksan'ların sonunda",
            "15'i, 20'si ve 25'i": "on beş'i, yirmi'si ve yirmi beş'i",
            
            # Complex sentences with multiple number formats (focusing only on apostrophe handling)
            "1960'lı yıllarda 2,5 milyon insan 100'lerce kitap okudu.": "bin dokuz yüz altmış'lı yıllarda iki virgül beş milyon insan yüz'lerce kitap okudu.",
            "Sınıfta 30'ar kişilik gruplar oluşturuldu.": "Sınıfta otuz'ar kişilik gruplar oluşturuldu.",
            "1990'ların başında 15.000'den fazla kişi katıldı.": "bin dokuz yüz doksan'ların başında on beş bin'den fazla kişi katıldı.",
            "2023'ün ilk 6 ayında 100'ü aşkın etkinlik düzenlendi.": "iki bin yirmi üç'ün ilk altı ayında yüz'ü aşkın etkinlik düzenlendi."
        }
        for text, expected in test_cases.items():
            self.assertEqual(self.converter.convert_numbers_to_words(text), expected)

    def test_divide_symbol_handling(self):
        """Test handling of divide symbols in numbers"""
        test_cases = {
            "7/24": "yedi/yirmi dört",
            "1/3": "bir/üç",
            "1/2": "bir/iki",
            "2/3": "iki/üç",
            "3/4": "üç/dört",
            "1/5": "bir/beş",
            "2/3'ü": "iki/üç'ü",
            "1/4'ü": "bir/dört'ü",
            "1/2'si": "bir/iki'si",
            "3/4'ünü": "üç/dört'ünü"
        }
        for number, expected in test_cases.items():
            self.assertEqual(self.converter.convert_numbers_to_words(number), expected)

if __name__ == '__main__':
    unittest.main()
