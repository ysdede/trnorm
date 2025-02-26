import unittest
from ordinals import normalize_ordinals

class TestOrdinalNormalization(unittest.TestCase):
    def test_basic_ordinals(self):
        """Test basic ordinal formats"""
        test_cases = {
            "1.": "birinci",
            "2.": "ikinci",
            "3.": "üçüncü",
            "10.": "onuncu",
            "20.": "yirminci",
        }
        for input_text, expected in test_cases.items():
            self.assertEqual(normalize_ordinals(input_text), expected)
    
    def test_apostrophe_ordinals(self):
        """Test ordinals with apostrophe"""
        test_cases = {
            "1'inci": "birinci",
            "2'nci": "ikinci",
            "3'üncü": "üçüncü",
            "4'üncü": "dördüncü",
            "5'inci": "beşinci",
        }
        for input_text, expected in test_cases.items():
            self.assertEqual(normalize_ordinals(input_text), expected)
    
    def test_attached_ordinals(self):
        """Test ordinals without apostrophe"""
        test_cases = {
            "1inci": "birinci",
            "2nci": "ikinci",
            "3üncü": "üçüncü",
            "10uncu": "onuncu",
            "20inci": "yirminci",
        }
        for input_text, expected in test_cases.items():
            self.assertEqual(normalize_ordinals(input_text), expected)
    
    def test_mixed_text(self):
        """Test ordinals in mixed text"""
        test_cases = {
            "Bu 1. sınıf": "Bu birinci sınıf",
            "1'inci katta": "birinci katta",
            "2nci ve 3. sırada": "ikinci ve üçüncü sırada",
            "5'inci, 6. ve 7nci sırada": "beşinci, altıncı ve yedinci sırada",
        }
        for input_text, expected in test_cases.items():
            self.assertEqual(normalize_ordinals(input_text), expected)
    
    def test_larger_numbers(self):
        """Test larger ordinal numbers"""
        test_cases = {
            "11.": "on birinci",
            "21.": "yirmi birinci",
            "42.": "kırk ikinci",
            "99.": "doksan dokuzuncu",
            "100.": "yüzüncü",
        }
        for input_text, expected in test_cases.items():
            self.assertEqual(normalize_ordinals(input_text), expected)

    def test_bullet_points(self):
        """Test bullet points with uppercase first letters are preserved."""
        test_cases = {
            "1. Sabah kahvaltısı": "1. Sabah kahvaltısı",
            "2. Yürüyüş": "2. Yürüyüş",
            "3. Öğle yemeği": "3. Öğle yemeği",
            "4. İş toplantısı": "4. İş toplantısı",
            "1. birinci madde (lowercase b - should be converted)": "birinci birinci madde (lowercase b - should be converted)",
            "2. İkinci madde (capital İ - should be preserved)": "2. İkinci madde (capital İ - should be preserved)",
            "3. üçüncü madde (lowercase ü - should be converted)": "üçüncü üçüncü madde (lowercase ü - should be converted)",
        }
        
        for input_text, expected_output in test_cases.items():
            self.assertEqual(normalize_ordinals(input_text), expected_output)

    def test_big_numbers(self):
        """Test big numbers are converted correctly."""
        test_cases = {
            "99. günde": "doksan dokuzuncu günde",
            "103. sırada": "yüz üçüncü sırada",
            "2000. saniye": "iki bininci saniye",
            "19857. aday": "on dokuz bin sekiz yüz elli yedinci aday",
            "1000000. kişi": "bir milyonuncu kişi",
            "1000000000. atom": "bir milyarıncı atom",
        }
        
        for input_text, expected_output in test_cases.items():
            self.assertEqual(normalize_ordinals(input_text), expected_output)

if __name__ == '__main__':
    unittest.main()
