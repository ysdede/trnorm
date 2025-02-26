"""
Tests for Roman numeral to Arabic number conversion.
"""

import unittest
from trnorm.roman_numerals import roman_to_arabic, is_roman_numeral


class TestRomanToArabic(unittest.TestCase):
    """Test cases for Roman to Arabic conversion."""
    
    def test_single_symbols(self):
        """Test conversion of single Roman numeral symbols."""
        self.assertEqual(roman_to_arabic("I"), 1)
        self.assertEqual(roman_to_arabic("V"), 5)
        self.assertEqual(roman_to_arabic("X"), 10)
        self.assertEqual(roman_to_arabic("L"), 50)
        self.assertEqual(roman_to_arabic("C"), 100)
        self.assertEqual(roman_to_arabic("D"), 500)
        self.assertEqual(roman_to_arabic("M"), 1000)
    
    def test_additive_combinations(self):
        """Test conversion of Roman numerals using additive combinations."""
        self.assertEqual(roman_to_arabic("II"), 2)
        self.assertEqual(roman_to_arabic("III"), 3)
        self.assertEqual(roman_to_arabic("VI"), 6)
        self.assertEqual(roman_to_arabic("VII"), 7)
        self.assertEqual(roman_to_arabic("VIII"), 8)
        self.assertEqual(roman_to_arabic("XI"), 11)
        self.assertEqual(roman_to_arabic("XV"), 15)
        self.assertEqual(roman_to_arabic("XX"), 20)
        self.assertEqual(roman_to_arabic("XXX"), 30)
        self.assertEqual(roman_to_arabic("LX"), 60)
        self.assertEqual(roman_to_arabic("CC"), 200)
        self.assertEqual(roman_to_arabic("MM"), 2000)
    
    def test_subtractive_combinations(self):
        """Test conversion of Roman numerals using subtractive combinations."""
        self.assertEqual(roman_to_arabic("IV"), 4)
        self.assertEqual(roman_to_arabic("IX"), 9)
        self.assertEqual(roman_to_arabic("XL"), 40)
        self.assertEqual(roman_to_arabic("XC"), 90)
        self.assertEqual(roman_to_arabic("CD"), 400)
        self.assertEqual(roman_to_arabic("CM"), 900)
    
    def test_complex_numerals(self):
        """Test conversion of complex Roman numerals."""
        self.assertEqual(roman_to_arabic("XIV"), 14)
        self.assertEqual(roman_to_arabic("XIX"), 19)
        self.assertEqual(roman_to_arabic("XXIV"), 24)
        self.assertEqual(roman_to_arabic("XLII"), 42)
        self.assertEqual(roman_to_arabic("XCIX"), 99)
        self.assertEqual(roman_to_arabic("CDXLIV"), 444)
        self.assertEqual(roman_to_arabic("CMXCIX"), 999)
        self.assertEqual(roman_to_arabic("MCMXCIX"), 1999)
        self.assertEqual(roman_to_arabic("MMXXIV"), 2024)
    
    def test_case_insensitivity(self):
        """Test that Roman numeral conversion is case-insensitive."""
        self.assertEqual(roman_to_arabic("i"), 1)
        self.assertEqual(roman_to_arabic("iv"), 4)
        self.assertEqual(roman_to_arabic("xIv"), 14)
        self.assertEqual(roman_to_arabic("mcmxcix"), 1999)
    
    def test_invalid_numerals(self):
        """Test that invalid Roman numerals raise ValueError."""
        invalid_numerals = [
            "IIII",  # Not standard (should be IV)
            "VV",    # Invalid repetition
            "IXX",   # Invalid combination
            "ABC",   # Not Roman numerals
            "123",   # Not Roman numerals
            "",      # Empty string
            "MMMM"   # Too many repetitions of M
        ]
        
        for numeral in invalid_numerals:
            with self.assertRaises(ValueError, msg=f"Should raise ValueError for {numeral}"):
                roman_to_arabic(numeral)
    
    def test_is_roman_numeral(self):
        """Test the is_roman_numeral function."""
        valid_numerals = [
            "I", "V", "X", "L", "C", "D", "M",
            "IV", "IX", "XL", "XC", "CD", "CM",
            "III", "VII", "XXX", "CCC", "MMM",
            "XIV", "XXIV", "MCMXCIX", "MMXXIV"
        ]
        
        invalid_numerals = [
            "IIII", "VV", "IXX", "ABC", "123", "", "MMMM"
        ]
        
        for numeral in valid_numerals:
            self.assertTrue(is_roman_numeral(numeral), f"{numeral} should be a valid Roman numeral")
            self.assertTrue(is_roman_numeral(numeral.lower()), f"{numeral.lower()} should be a valid Roman numeral")
        
        for numeral in invalid_numerals:
            self.assertFalse(is_roman_numeral(numeral), f"{numeral} should not be a valid Roman numeral")


if __name__ == "__main__":
    unittest.main()
