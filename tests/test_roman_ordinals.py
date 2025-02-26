"""
Tests for Roman numeral ordinal normalization.
"""

import unittest
from trnorm.roman_numerals import roman_to_arabic, is_roman_numeral
from trnorm.ordinals import normalize_ordinals


class TestRomanNumerals(unittest.TestCase):
    """Test cases for Roman numeral functions."""
    
    def test_is_roman_numeral(self):
        """Test the is_roman_numeral function."""
        valid_romans = ["I", "V", "X", "L", "C", "D", "M", "IV", "IX", "XIV", "MCMXCIX"]
        invalid_romans = ["A", "B", "Y", "Z", "IIII", "VV", "IXX", "ABC", "123"]
        
        for roman in valid_romans:
            self.assertTrue(is_roman_numeral(roman), f"{roman} should be a valid Roman numeral")
        
        for roman in invalid_romans:
            self.assertFalse(is_roman_numeral(roman), f"{roman} should not be a valid Roman numeral")
    
    def test_roman_to_arabic(self):
        """Test the roman_to_arabic function."""
        test_cases = [
            ("I", 1),
            ("II", 2),
            ("III", 3),
            ("IV", 4),
            ("V", 5),
            ("IX", 9),
            ("X", 10),
            ("XIV", 14),
            ("XIX", 19),
            ("XX", 20),
            ("XL", 40),
            ("L", 50),
            ("XC", 90),
            ("C", 100),
            ("CD", 400),
            ("D", 500),
            ("CM", 900),
            ("M", 1000),
            ("MCMXCIX", 1999),
            ("MMXXIV", 2024)
        ]
        
        for roman, expected in test_cases:
            self.assertEqual(roman_to_arabic(roman), expected, f"{roman} should convert to {expected}")
        
        # Test invalid Roman numerals
        with self.assertRaises(ValueError):
            roman_to_arabic("IIII")  # Not a standard Roman numeral
        
        with self.assertRaises(ValueError):
            roman_to_arabic("ABC")  # Not a Roman numeral at all


class TestRomanOrdinalNormalization(unittest.TestCase):
    """Test cases for Roman ordinal normalization."""
    
    def test_roman_ordinals_with_proper_nouns(self):
        """Test normalization of Roman ordinals followed by proper nouns."""
        test_cases = [
            ("II. Dünya Savaşı", "ikinci Dünya Savaşı"),
            ("XX. yüzyıl", "yirminci yüzyıl"),
            ("III. Selim", "üçüncü Selim"),
            ("XIV. Louis", "on dördüncü Louis"),
            ("II. Wilhelm", "ikinci Wilhelm"),
            ("V. Karl", "beşinci Karl"),
            ("VIII. Edward", "sekizinci Edward")
        ]
        
        for input_text, expected in test_cases:
            self.assertEqual(normalize_ordinals(input_text), expected, 
                             f"Failed to normalize: {input_text}")
    
    def test_mixed_ordinals(self):
        """Test normalization of text containing both Arabic and Roman ordinals."""
        input_text = "3. sınıf öğrencileri ve II. Dünya Savaşı hakkında 20. yüzyılın en önemli olaylarından biri olan V. büyük savaş."
        expected = "üçüncü sınıf öğrencileri ve ikinci Dünya Savaşı hakkında yirminci yüzyılın en önemli olaylarından biri olan beşinci büyük savaş."
        
        self.assertEqual(normalize_ordinals(input_text), expected)
    
    def test_roman_numerals_without_period(self):
        """Test that Roman numerals without a period are not normalized."""
        input_text = "Roma rakamları I, V, X, L, C, D ve M harflerinden oluşur."
        # Should remain unchanged
        self.assertEqual(normalize_ordinals(input_text), input_text)


if __name__ == "__main__":
    unittest.main()
