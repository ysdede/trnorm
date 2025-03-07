"""
Tests for the suffix_handler module.
"""

import unittest
from trnorm.suffix_handler import merge_suffixes


class TestSuffixHandler(unittest.TestCase):
    """Test cases for the suffix_handler module."""

    def test_ile_suffix(self):
        """Test merging of 'ile' suffix with preceding words."""
        test_cases = {
            "Toros ile hamile": "Torosla hamile",
            "Ankara ile İstanbul": "Ankarayla İstanbul",
            "Ali ile Veli": "Aliyle Veli",
            "Çay ile kahve": "Çayla kahve",
            "Kalem ile defter": "Kalemle defter",
            "AB ile ilgili": "AB ile ilgili",  # Abbreviations should remain separate
            "x ile y": "x ile y",  # Single letters should remain separate
            "Toros ile": "Torosla",  # Suffix at the end
            "ile Toros": "ile Toros",  # Suffix at the beginning (no change)
            "Toros ile İstanbul ile Ankara": "Torosla İstanbulla Ankara",  # Multiple occurrences
        }
        
        for input_text, expected_output in test_cases.items():
            self.assertEqual(merge_suffixes(input_text), expected_output)

    def test_ise_suffix(self):
        """Test merging of 'ise' suffix with preceding words."""
        test_cases = {
            "Hayat sana limon verdi ise limonata yap": "Hayat sana limon verdiyse limonata yap",
            "Ankara ise güzel": "Ankaraysa güzel",
            "Ali ise gelsin": "Aliyse gelsin",
            "Çay ise içelim": "Çaysa içelim",
            "Kalem ise alayım": "Kalemse alayım",
            "AB ise önemli": "AB ise önemli",  # Abbreviations should remain separate
            "x ise y": "x ise y",  # Single letters should remain separate
            "Toros ise": "Torossa",  # Suffix at the end
            "ise Toros": "ise Toros",  # Suffix at the beginning (no change)
            "Toros ise İstanbul ise Ankara": "Torossa İstanbulsa Ankara",  # Multiple occurrences
        }
        
        for input_text, expected_output in test_cases.items():
            self.assertEqual(merge_suffixes(input_text), expected_output)

    def test_iken_suffix(self):
        """Test merging of 'iken' suffix with preceding words."""
        test_cases = {
            "Hâl böyle iken böyle dedi adam": "Hâl böyleyken böyle dedi adam",
            "Ankara iken İstanbul'a taşındı": "Ankarayken İstanbul'a taşındı",
            "Ali iken Veli oldu": "Aliyken Veli oldu",
            "Çocuk iken hayalleri vardı": "Çocukken hayalleri vardı",
            "Öğrenci iken çalışıyordu": "Öğrenciyken çalışıyordu",
            "AB iken değişti": "AB iken değişti",  # Abbreviations should remain separate
            "x iken y": "x iken y",  # Single letters should remain separate
            "Toros iken": "Torosken",  # Suffix at the end
            "iken Toros": "iken Toros",  # Suffix at the beginning (no change)
            "Toros iken İstanbul iken Ankara": "Torosken İstanbulken Ankara",  # Multiple occurrences
        }
        
        for input_text, expected_output in test_cases.items():
            self.assertEqual(merge_suffixes(input_text), expected_output)

    def test_multiple_suffix_types(self):
        """Test handling of multiple suffix types in the same text."""
        test_cases = {
            "Toros ile giderken yağmur yağdı ise şemsiye al": "Torosla giderken yağmur yağdıysa şemsiye al",
            "Ali iken Veli ile tanıştı ise iyi oldu": "Aliyken Veliyle tanıştıysa iyi oldu",
            "Çay ise içelim, kahve ile de olur iken vazgeçtim": "Çaysa içelim, kahveyle de olurken vazgeçtim",
        }
        
        for input_text, expected_output in test_cases.items():
            self.assertEqual(merge_suffixes(input_text), expected_output)

    def test_list_input(self):
        """Test handling of list input."""
        input_list = [
            "Toros ile hamile",
            "Hayat sana limon verdi ise limonata yap",
            "Hâl böyle iken böyle dedi adam"
        ]
        
        expected_output = [
            "Torosla hamile",
            "Hayat sana limon verdiyse limonata yap",
            "Hâl böyleyken böyle dedi adam"
        ]
        
        self.assertEqual(merge_suffixes(input_list), expected_output)


if __name__ == "__main__":
    unittest.main()
