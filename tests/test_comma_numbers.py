"""
Unit tests for numbers followed by commas.
"""
import unittest
from trnorm import normalize
from trnorm.num_to_text import NumberToTextConverter, convert_numbers_to_words_wrapper
from trnorm.legacy_normalizer import turkish_lower


class TestCommaNumbers(unittest.TestCase):
    """Test cases for numbers followed by commas."""

    def test_numbers_with_commas(self):
        """Test that numbers followed by commas are properly converted to text."""
        test_cases = [
            ("13, 14 ve 15", "on üç, on dört ve on beş"),
            ("1, 2, 3 sayıları", "bir, iki, üç sayıları"),
            ("Sınavda 5, 8, 13, 21 sorularını çözemedim.", 
             "sınavda beş, sekiz, on üç, yirmi bir sorularını çözemedim."),
            ("Yıl 1923, 29 Ekim'de", "yıl bin dokuz yüz yirmi üç, yirmi dokuz ekim'de"),
            ('"13, 14 ve 15 Eylül günleri', '"on üç, on dört ve on beş eylül günleri'),
            ('General Jukov, o günleri günlüğüne şu şekilde aktardı; "13, 14 ve 15 Eylül günleri',
             'general jukov, o günleri günlüğüne şu şekilde aktardı; "on üç, on dört ve on beş eylül günleri')
        ]

        # Create a list of converters for normalization
        converters = [
            convert_numbers_to_words_wrapper,
            turkish_lower
        ]

        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = normalize(input_text, converters)
                self.assertEqual(result, expected_output)

    def test_direct_conversion(self):
        """Test direct conversion using the NumberToTextConverter."""
        converter = NumberToTextConverter()
        test_cases = [
            ("13,", "on üç,"),
            ("13, 14", "on üç, on dört"),
            ("1, 2, 3", "bir, iki, üç"),
            ("100, 200, 300", "yüz, iki yüz, üç yüz")
        ]

        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = converter.convert_numbers_to_words(input_text)
                self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
