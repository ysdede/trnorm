"""
Unit tests for apostrophe handling in Turkish text normalization.
"""
import unittest
from trnorm import normalize
from trnorm.apostrophe_handler import remove_apostrophes
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.legacy_normalizer import turkish_lower


class TestApostropheHandling(unittest.TestCase):
    """Test cases for apostrophe handling in Turkish text."""

    def test_apostrophe_removal(self):
        """Test that apostrophes are properly removed."""
        test_cases = [
            ("8'i almadım", "8i almadım"),
            ("Kitap'ı okudum", "Kitapı okudum"),
            ("Ahmet'in arabası", "Ahmetin arabası"),
            ("İstanbul'da yaşıyorum", "İstanbulda yaşıyorum"),
            ("GoPro 7'yi kullanıyorum", "GoPro 7yi kullanıyorum"),
            ("'Merhaba' dedi", "Merhaba dedi"),
            ("O'nun kalemi", "Onun kalemi"),
            ("Türkiye'nin başkenti", "Türkiyenin başkenti")
        ]

        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = remove_apostrophes(input_text)
                self.assertEqual(result, expected_output)

    def test_normalization_with_apostrophe_handling(self):
        """Test normalization with apostrophe handling enabled."""
        test_cases = [
            ("8'i almadım", "sekizi almadım"),
            ("Kitap'ı okudum", "kitapı okudum"),
            ("Ahmet'in arabası", "ahmetin arabası"),
            ("İstanbul'da yaşıyorum", "istanbulda yaşıyorum"),
            ("GoPro 7'yi kullanıyorum", "gopro yediyi kullanıyorum"),
            ("O'nun 5'i var", "onun beşi var"),
            ("Türkiye'nin 81'i", "türkiyenin seksen biri")
        ]

        # Create a list of converters that includes apostrophe handling
        # Note: We need to convert numbers to words BEFORE removing apostrophes
        # to handle cases like "7'yi" -> "yedi'yi" -> "yediyi"
        converters = [
            convert_numbers_to_words_wrapper,
            remove_apostrophes,
            turkish_lower
        ]

        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = normalize(input_text, converters)
                self.assertEqual(result, expected_output)

    def test_normalization_without_apostrophe_handling(self):
        """Test normalization without apostrophe handling."""
        test_cases = [
            ("8'i almadım", "sekiz'i almadım"),
            ("Kitap'ı okudum", "kitap'ı okudum"),
            ("Ahmet'in arabası", "ahmet'in arabası"),
            ("İstanbul'da yaşıyorum", "istanbul'da yaşıyorum"),
            ("GoPro 7'yi kullanıyorum", "gopro yedi'yi kullanıyorum")
        ]

        # Create a list of converters without apostrophe handling
        converters = [
            convert_numbers_to_words_wrapper,
            turkish_lower
        ]

        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                result = normalize(input_text, converters)
                self.assertEqual(result, expected_output)

    def test_user_example(self):
        """Test the specific user example."""
        ref = "GoPro Osmo Action'dan daha çok sevdiğim GoPro 7 bu sırada, 8'i almadım, niye almadım?"
        expected = "gopro osmo actiondan daha çok sevdiğim gopro yedi bu sırada, sekizi almadım, niye almadım?"
        
        # Create a list of converters that includes apostrophe handling
        # Note: We need to convert numbers to words BEFORE removing apostrophes
        converters = [
            convert_numbers_to_words_wrapper,
            remove_apostrophes,
            turkish_lower
        ]
        
        result = normalize(ref, converters)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
