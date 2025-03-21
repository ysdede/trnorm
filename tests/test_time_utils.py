"""
Tests for the time normalization functionality.
"""

import unittest
from trnorm.time_utils import normalize_times
from trnorm.normalizer import normalize
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.legacy_normalizer import turkish_lower


class TestTimeNormalization(unittest.TestCase):
    """Test cases for time normalization functionality."""

    def test_normalize_times_standalone(self):
        """Test the normalize_times function with standalone time patterns."""
        test_cases = [
            ("22.00", "22"),  # Zero minutes should be omitted
            ("9:45", "9 45"),
            ("13.30", "13 buçuk"),
            ("7:30", "7 buçuk"),
            ("08.00", "08"),  # Zero minutes should be omitted
        ]
        
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = normalize_times(input_text)
                self.assertEqual(result, expected_output)

    def test_normalize_times_with_saat(self):
        """Test the normalize_times function with 'saat' prefix."""
        test_cases = [
            ("saat 22.00", "saat 22"),  # Zero minutes should be omitted
            ("saat 9:45", "saat 9 45"),
            ("saat 13.30", "saat 13 buçuk"),
            ("saat 7:30", "saat 7 buçuk"),
            ("saat 08.00", "saat 08"),  # Zero minutes should be omitted
        ]
        
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = normalize_times(input_text)
                self.assertEqual(result, expected_output)

    def test_normalize_times_in_sentences(self):
        """Test the normalize_times function with times in sentences."""
        test_cases = [
            (
                "Toplantı saat 14.30'da başlayacak.",
                "Toplantı saat 14 buçuk'da başlayacak."
            ),
            (
                "Uçak 22:15'te kalkacak ve 06:45'te inecek.",
                "Uçak 22 15'te kalkacak ve 06 45'te inecek."
            ),
            (
                "Ancak 13 Nisan 2024 akşamı saat 22.00 sularında, İran Devrim Muhafızları, İsrail'i hedef alarak devasa bir füze saldırısı başlattı.",
                "Ancak 13 Nisan 2024 akşamı saat 22 sularında, İran Devrim Muhafızları, İsrail'i hedef alarak devasa bir füze saldırısı başlattı."
            ),
            (
                "Toplantı saat 9.00'da başlayacak.",
                "Toplantı saat 9'da başlayacak."
            ),
        ]
        
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = normalize_times(input_text)
                self.assertEqual(result, expected_output)

    def test_full_normalization_pipeline(self):
        """Test time normalization within the full normalization pipeline."""
        test_cases = [
            (
                "Ancak 13 Nisan 2024 akşamı saat 22.00 sularında, İran Devrim Muhafızları, İsrail'i hedef alarak devasa bir füze saldırısı başlattı.",
                "ancak on üç nisan iki bin yirmi dört akşamı saat yirmi iki sularında, iran devrim muhafızları, israil'i hedef alarak devasa bir füze saldırısı başlattı."
            ),
            (
                "Toplantı saat 14.30'da başlayacak.",
                "toplantı saat on dört buçuk'da başlayacak."
            ),
            (
                "Uçak 22:15'te kalkacak ve 06:45'te inecek.",
                "uçak yirmi iki on beş'te kalkacak ve altı kırk beş'te inecek."
            ),
            (
                "Toplantı saat 9.00'da başlayacak.",
                "toplantı saat dokuz'da başlayacak."
            ),
        ]
        
        # Create a list of converters for full normalization
        converters = [
            normalize_times,
            convert_numbers_to_words_wrapper,
            turkish_lower
        ]
        
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = normalize(input_text, converters)
                self.assertEqual(result, expected_output)

    def test_non_time_periods(self):
        """Test that non-time periods are not affected."""
        test_cases = [
            ("1.000.000", "1.000.000"),  # Should remain unchanged by time normalization
            ("3.14159", "3.14159"),      # Should remain unchanged by time normalization
            ("2.500,75", "2.500,75"),    # Should remain unchanged by time normalization
        ]
        
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = normalize_times(input_text)
                self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
