"""
Unit tests for the dimension utilities.
"""

import unittest
import sys
import os

# Add the parent directory to the path to import the trnorm package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm.dimension_utils import preprocess_dimensions, normalize_dimensions
from trnorm.unit_utils import normalize_units
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.legacy_normalizer import turkish_lower
from trnorm import normalize


class TestDimensionUtils(unittest.TestCase):
    """Test the dimension utilities."""

    def test_preprocess_dimensions(self):
        """Test the preprocess_dimensions function."""
        test_cases = [
            # Basic cases
            ("2x3", "2 x 3"),
            ("2x3x4", "2 x 3 x 4"),
            ("5x10x15", "5 x 10 x 15"),
            
            # With units
            ("2x3cm", "2 x 3 cm"),
            ("120x180cm", "120 x 180 cm"),
            ("2x3metre", "2 x 3 metre"),
            ("5kg", "5 kg"),
            ("10mm", "10 mm"),
            
            # Mixed cases
            ("Masa 75x120x90cm", "Masa 75 x 120 x 90 cm"),
            
            # Regular 'x' in text (not dimensions)
            ("matematikte bilinmeyene x denmesinin sebebi", "matematikte bilinmeyene x denmesinin sebebi"),
            ("x ve y eksenleri", "x ve y eksenleri"),
        ]
        
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(preprocess_dimensions(input_text), expected_output)

    def test_normalize_dimensions(self):
        """Test the normalize_dimensions function."""
        test_cases = [
            # Basic cases
            ("2x3", "2 çarpı 3"),
            ("2 x 3", "2 çarpı 3"),
            ("2x3x4", "2 çarpı 3 çarpı 4"),
            
            # With units
            ("2x3cm", "2 çarpı 3 cm"),
            ("120x180cm", "120 çarpı 180 cm"),
            
            # Mixed cases
            ("Masa 75x120cm", "Masa 75 çarpı 120 cm"),
            
            # Regular 'x' in text (not dimensions)
            ("matematikte bilinmeyene x denmesinin sebebi", "matematikte bilinmeyene x denmesinin sebebi"),
        ]
        
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(normalize_dimensions(input_text), expected_output)
                
    def test_normalize_units(self):
        """Test the normalize_units function."""
        test_cases = [
            # Basic unit cases with space
            ("5 cm", "5 santimetre"),
            ("10 kg", "10 kilogram"),
            ("20 mm", "20 milimetre"),
            ("1 m", "1 metre"),
            
            # Units without space
            ("5cm", "5 santimetre"),
            ("10kg", "10 kilogram"),
            ("20mm", "20 milimetre"),
            ("1m", "1 metre"),
            
            # Units with periods (with space) - match current behavior
            ("5 cm.", "5 santimetre."),
            ("10 kg.", "10 kilogram."),
            
            # Units with periods (without space) - match current behavior
            ("5cm.", "5 santimetre."),
            ("10kg.", "10 kilogram."),
            
            # Multiple units in text (with space)
            ("Masa 75 cm yüksekliğinde ve 120 cm genişliğindedir.", 
             "Masa 75 santimetre yüksekliğinde ve 120 santimetre genişliğindedir."),
            
            # Multiple units in text (without space)
            ("Masa 75cm yüksekliğinde ve 120cm genişliğindedir.", 
             "Masa 75 santimetre yüksekliğinde ve 120 santimetre genişliğindedir."),
            
            # Mixed spacing
            ("Masa 75cm yüksekliğinde ve 120 cm genişliğindedir.", 
             "Masa 75 santimetre yüksekliğinde ve 120 santimetre genişliğindedir."),
             
            # Units with periods in sentences - match current behavior
            ("Ağırlığı 5 kg. ve uzunluğu 10 m.", 
             "Ağırlığı 5 kilogram. ve uzunluğu 10 metre."),
            ("Ağırlığı 5kg. ve uzunluğu 10m.", 
             "Ağırlığı 5 kilogram. ve uzunluğu 10 metre."),
            
            # Mixed with dimensions
            ("Oda 2 çarpı 3 m boyutlarındadır.", "Oda 2 çarpı 3 metre boyutlarındadır."),
            ("Oda 2 çarpı 3m boyutlarındadır.", "Oda 2 çarpı 3 metre boyutlarındadır."),
        ]
        
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(normalize_units(input_text), expected_output)

    def test_normalizer_integration(self):
        """Test the integration with the normalizer."""
        test_cases = [
            # Basic dimensions
            ("2x3", "iki çarpı üç"),
            ("2x3x4", "iki çarpı üç çarpı dört"),
            
            # Dimensions with units (with space)
            ("2x3 cm", "iki çarpı üç santimetre"),
            ("120x180 cm", "yüz yirmi çarpı yüz seksen santimetre"),
            
            # Dimensions with units (without space)
            ("2x3cm", "iki çarpı üç santimetre"),
            ("120x180cm", "yüz yirmi çarpı yüz seksen santimetre"),
            
            # Dimensions in sentences
            ("Odanın boyutları 2x3 metre.", "odanın boyutları iki çarpı üç metre."),
            ("Halının boyutu 120x180cm.", "halının boyutu yüz yirmi çarpı yüz seksen santimetre."),
            
            # Regular 'x' in text (not dimensions)
            ("matematikte bilinmeyene x denmesinin sebebi", "matematikte bilinmeyene x denmesinin sebebi"),
            
            # Units without dimensions (with space) - match current behavior
            ("Masa 75 cm yüksekliğindedir.", "masa yetmiş beş santimetre yüksekliğindedir."),
            ("Ağırlığı 5 kg.", "ağırlığı beş kilogram."),
            
            # Units without dimensions (without space) - match current behavior
            ("Masa 75cm yüksekliğinde.", "masa yetmiş beş santimetre yüksekliğinde."),
            ("Ağırlığı 5kg.", "ağırlığı beş kilogram."),
            
            # Mixed units with periods - match current behavior
            ("Ağırlığı 5 kg. ve uzunluğu 10 m.", "ağırlığı beş kilogram. ve uzunluğu on metre."),
        ]
        
        # Create a list of converters for full normalization
        converters = [
            preprocess_dimensions,
            normalize_dimensions,
            normalize_units,
            convert_numbers_to_words_wrapper,
            turkish_lower
        ]
        
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = normalize(input_text, converters)
                self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
