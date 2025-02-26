import unittest
import sys
import os

# Add parent directory to path to allow imports from parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from text_utils import (
    turkish_lower,
    turkish_upper,
    turkish_capitalize,
    is_turkish_upper,
    son_harf,
    sesli_ile_bitiyor,
    son_sesli_harf,
    son_sesli_harf_kalin,
    sapkasiz,
    kalin_sesliler,
    ince_sesliler,
    sesli_harfler,
    ekle
)


class TestTurkishTextUtils(unittest.TestCase):
    def test_constants(self):
        """Test the vowel constants."""
        # Test kalin_sesliler (back vowels)
        self.assertEqual(kalin_sesliler, "aıouûâ")
        
        # Test ince_sesliler (front vowels)
        self.assertEqual(ince_sesliler, "eiöüîêô")
        
        # Test sesli_harfler (all vowels)
        self.assertEqual(sesli_harfler, kalin_sesliler + ince_sesliler)
        
        # Verify all vowels are included
        all_vowels = set("aıoueiöüâîûêô")
        self.assertEqual(set(sesli_harfler), all_vowels)

    def test_turkish_lower(self):
        """Test turkish_lower function with various inputs."""
        # Test with uppercase Turkish characters
        self.assertEqual(turkish_lower("İŞĞÜÇÖI"), "işğüçöı")
        
        # Test with mixed case
        self.assertEqual(turkish_lower("İstanbul"), "istanbul")
        self.assertEqual(turkish_lower("ANKARA"), "ankara")
        
        # Test with accented characters
        self.assertEqual(turkish_lower("ÂÎÛ"), "âîû")
        
        # Test with empty string
        self.assertEqual(turkish_lower(""), "")
        
        # Test with non-Turkish characters
        self.assertEqual(turkish_lower("HELLO"), "hello")
        
        # Test with numbers and special characters
        self.assertEqual(turkish_lower("İSTANBUL123!"), "istanbul123!")

    def test_turkish_upper(self):
        """Test turkish_upper function with various inputs."""
        # Test with lowercase Turkish characters
        self.assertEqual(turkish_upper("işğüçöı"), "İŞĞÜÇÖI")
        
        # Test with mixed case
        self.assertEqual(turkish_upper("istanbul"), "İSTANBUL")
        self.assertEqual(turkish_upper("Ankara"), "ANKARA")
        
        # Test with accented characters
        self.assertEqual(turkish_upper("âîû"), "ÂÎÛ")
        
        # Test with empty string
        self.assertEqual(turkish_upper(""), "")
        
        # Test with non-Turkish characters
        self.assertEqual(turkish_upper("hello"), "HELLO")
        
        # Test with numbers and special characters
        self.assertEqual(turkish_upper("istanbul123!"), "İSTANBUL123!")
        
        # Test specific Turkish character pairs
        self.assertEqual(turkish_upper("i"), "İ")
        self.assertEqual(turkish_upper("ı"), "I")

    def test_turkish_capitalize(self):
        """Test turkish_capitalize function with various inputs."""
        # Test with lowercase Turkish characters
        self.assertEqual(turkish_capitalize("istanbul"), "İstanbul")
        self.assertEqual(turkish_capitalize("ırmak"), "Irmak")
        self.assertEqual(turkish_capitalize("şehir"), "Şehir")
        
        # Test with already capitalized words
        self.assertEqual(turkish_capitalize("İstanbul"), "İstanbul")
        self.assertEqual(turkish_capitalize("Ankara"), "Ankara")
        
        # Test with empty string
        self.assertEqual(turkish_capitalize(""), "")
        
        # Test with single character
        self.assertEqual(turkish_capitalize("i"), "İ")
        self.assertEqual(turkish_capitalize("ı"), "I")
        
        # Test with numbers and special characters at the beginning
        self.assertEqual(turkish_capitalize("123istanbul"), "123istanbul")
        self.assertEqual(turkish_capitalize("!istanbul"), "!istanbul")
        
        # Test with space at the beginning
        self.assertEqual(turkish_capitalize(" istanbul"), " istanbul")

    def test_is_turkish_upper(self):
        """Test is_turkish_upper function with various inputs."""
        # Test with uppercase Turkish words
        self.assertTrue(is_turkish_upper("İSTANBUL"))
        self.assertTrue(is_turkish_upper("ANKARA"))
        
        # Test with lowercase or mixed case
        self.assertFalse(is_turkish_upper("istanbul"))
        self.assertFalse(is_turkish_upper("İstanbul"))
        
        # Test with empty string
        self.assertTrue(is_turkish_upper(""))  # Empty string is considered uppercase
        
        # Test with single characters
        self.assertTrue(is_turkish_upper("İ"))
        self.assertFalse(is_turkish_upper("i"))
        
        # Test with numbers and special characters
        self.assertTrue(is_turkish_upper("İSTANBUL123!"))
        self.assertFalse(is_turkish_upper("İSTANBUL123!i"))

    def test_son_harf(self):
        """Test son_harf function with various inputs."""
        # Test with regular words
        self.assertEqual(son_harf("kitap"), "p")
        self.assertEqual(son_harf("İstanbul"), "l")
        
        # Test with single character
        self.assertEqual(son_harf("a"), "a")
        
        # Test with numbers and special characters
        self.assertEqual(son_harf("kitap123"), "3")
        self.assertEqual(son_harf("kitap!"), "!")
        
        # Test with empty string should raise an IndexError
        with self.assertRaises(IndexError):
            son_harf("")

    def test_sesli_ile_bitiyor(self):
        """Test sesli_ile_bitiyor function with various inputs."""
        # Test words ending with vowels
        self.assertTrue(sesli_ile_bitiyor("araba"))  # ends with 'a'
        self.assertTrue(sesli_ile_bitiyor("kapı"))   # ends with 'ı'
        self.assertTrue(sesli_ile_bitiyor("kedi"))   # ends with 'i'
        self.assertTrue(sesli_ile_bitiyor("kutu"))   # ends with 'u'
        self.assertTrue(sesli_ile_bitiyor("örtü"))   # ends with 'ü'
        self.assertTrue(sesli_ile_bitiyor("köprü"))  # ends with 'ü'
        
        # Test words ending with consonants
        self.assertFalse(sesli_ile_bitiyor("kitap"))  # ends with 'p'
        self.assertFalse(sesli_ile_bitiyor("kalem"))  # ends with 'm'
        self.assertFalse(sesli_ile_bitiyor("ağaç"))   # ends with 'ç'
        
        # Test with uppercase letters
        self.assertTrue(sesli_ile_bitiyor("ARABA"))   # ends with 'A'
        
        # Test with accented vowels
        self.assertTrue(sesli_ile_bitiyor("kâğıdâ"))  # ends with 'â'
        
        # Test with empty string should raise an IndexError
        with self.assertRaises(IndexError):
            sesli_ile_bitiyor("")

    def test_son_sesli_harf(self):
        """Test son_sesli_harf function with various inputs."""
        # Test finding the last vowel
        self.assertEqual(son_sesli_harf("kitap"), "a")
        self.assertEqual(son_sesli_harf("kalem"), "e")
        self.assertEqual(son_sesli_harf("İstanbul"), "u")
        self.assertEqual(son_sesli_harf("öğrenci"), "i")
        
        # Test with only consonants (should return None)
        self.assertIsNone(son_sesli_harf("krş"))
        
        # Test with empty string (should return None)
        self.assertIsNone(son_sesli_harf(""))
        
        # Test with uppercase letters
        self.assertEqual(son_sesli_harf("KALEM"), "e")
        
        # Test with accented vowels
        self.assertEqual(son_sesli_harf("kâğıt"), "ı")
        self.assertEqual(son_sesli_harf("îman"), "a")
        
        # Test with numbers and special characters
        self.assertEqual(son_sesli_harf("kitap123"), "a")
        self.assertEqual(son_sesli_harf("a!b@c#"), "a")

    def test_son_sesli_harf_kalin(self):
        """Test son_sesli_harf_kalin function with various inputs."""
        # Test words with back vowels as the last vowel
        self.assertTrue(son_sesli_harf_kalin("kitap"))  # last vowel is 'a'
        self.assertTrue(son_sesli_harf_kalin("okul"))   # last vowel is 'u'
        self.assertTrue(son_sesli_harf_kalin("kızıl"))  # last vowel is 'ı'
        
        # Test words with front vowels as the last vowel
        self.assertFalse(son_sesli_harf_kalin("ekmek"))  # last vowel is 'e'
        self.assertFalse(son_sesli_harf_kalin("üzüm"))   # last vowel is 'ü'
        self.assertFalse(son_sesli_harf_kalin("göl"))    # last vowel is 'ö'
        
        # Test with uppercase letters
        self.assertTrue(son_sesli_harf_kalin("KITAP"))   # last vowel is 'A'
        
        # Test with accented vowels
        self.assertTrue(son_sesli_harf_kalin("kâğıt"))   # last vowel is 'ı'
        self.assertTrue(son_sesli_harf_kalin("hûr"))     # last vowel is 'û'
        
        # Test with no vowels or empty string (should raise AttributeError)
        with self.assertRaises(AttributeError):
            son_sesli_harf_kalin("krş")
        with self.assertRaises(AttributeError):
            son_sesli_harf_kalin("")

    def test_sapkasiz(self):
        """Test sapkasiz function with various inputs."""
        # Test with accented characters
        self.assertEqual(sapkasiz("kâğıt"), "kağıt")
        self.assertEqual(sapkasiz("Âdem"), "Adem")
        self.assertEqual(sapkasiz("îman"), "iman")
        self.assertEqual(sapkasiz("Îman"), "İman")
        self.assertEqual(sapkasiz("hûr"), "hur")
        self.assertEqual(sapkasiz("Hûr"), "Hur")
        
        # Test with mixed accented and non-accented
        self.assertEqual(sapkasiz("kâtip"), "katip")
        self.assertEqual(sapkasiz("Îstanbul"), "İstanbul")
        
        # Test with no accented characters
        self.assertEqual(sapkasiz("kitap"), "kitap")
        self.assertEqual(sapkasiz("İstanbul"), "İstanbul")
        
        # Test with empty string
        self.assertEqual(sapkasiz(""), "")
        
        # Test with multiple accented characters
        self.assertEqual(sapkasiz("Âlî Bâbâ"), "Ali Baba")
        
        # Test with numbers and special characters
        self.assertEqual(sapkasiz("kâğıt123!"), "kağıt123!")

    def test_ekle_ile(self):
        """Test ekle function with 'ile' suffix."""
        from tests.test_strings import ile_test_words, istisnalar_test_words
        
        # Test regular words with 'ile'
        for kelime, beklenen in ile_test_words.items():
            self.assertEqual(ekle(kelime, "ile"), beklenen)
        
        # Test exception words with 'ile'
        for kelime, beklenen in istisnalar_test_words.items():
            self.assertEqual(ekle(kelime, "ile"), beklenen[0])

    def test_ekle_ise(self):
        """Test ekle function with 'ise' suffix."""
        from tests.test_strings import ise_test_words, istisnalar_test_words
        
        # Test regular words with 'ise'
        for kelime, beklenen in ise_test_words.items():
            self.assertEqual(ekle(kelime, "ise"), beklenen)
        
        # Test exception words with 'ise'
        for kelime, beklenen in istisnalar_test_words.items():
            self.assertEqual(ekle(kelime, "ise"), beklenen[1])
    
    def test_ekle_invalid(self):
        """Test ekle function with invalid inputs."""
        # Test with empty string
        self.assertEqual(ekle("", "ile"), "")
        
        # Test with invalid suffix
        with self.assertRaises(ValueError):
            ekle("test", "invalid")
        
        # Test with empty suffix
        with self.assertRaises(ValueError):
            ekle("test", "")

    def test_turkish_case_conversion_roundtrip(self):
        """Test that turkish_lower and turkish_upper work correctly in roundtrip."""
        test_words = [
            "İstanbul",
            "ANKARA",
            "izmir",
            "BURSA",
            "Çanakkale",
            "ŞANLIURFA",
            "ığdır",
            "IĞDIR"
        ]
        
        for word in test_words:
            # Test lowercase -> uppercase -> lowercase
            self.assertEqual(turkish_lower(turkish_upper(turkish_lower(word))), turkish_lower(word))
            
            # Test uppercase -> lowercase -> uppercase
            self.assertEqual(turkish_upper(turkish_lower(turkish_upper(word))), turkish_upper(word))


if __name__ == "__main__":
    unittest.main()
