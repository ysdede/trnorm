"""
This module provides functionality for adding the Turkish conditional suffix "ise" (if) to words.

The suffix "ise" changes form based on vowel harmony and whether the word ends with a vowel:
- If the word ends with a consonant and the last vowel is back (a, ı, o, u): "sa" is added
- If the word ends with a consonant and the last vowel is front (e, i, ö, ü): "se" is added
- If the word ends with a vowel and the last vowel is back (a, ı, o, u): "ysa" is added
- If the word ends with a vowel and the last vowel is front (e, i, ö, ü): "yse" is added

Examples:
- Toros + ise = Torossa
- Ankara + ise = Ankaraysa
- İstanbul + ise = İstanbulsa
- Ali + ise = Aliyse
"""

from text_utils import ekle
from test_strings import ise_test_words, istisnalar_test_words


def ek_uret(kelime):
    """
    Add the Turkish conditional suffix "ise" to a word, following Turkish vowel harmony rules.
    
    Args:
        kelime (str): The word to add the suffix to
        
    Returns:
        str: The word with the "ise" suffix added
    """
    return ekle(kelime, "ise")


# Run tests if this file is executed directly
if __name__ == "__main__":
    # Test regular words
    for kelime, beklenen in ise_test_words.items():
        result = ek_uret(kelime)
        print(f"{kelime:<16} {beklenen:<16} --> {result:<16}")
        assert result == beklenen

    sozluk_tsv = "TDK_Sozluk-Turkish.tsv"

    import csv

    with open(sozluk_tsv, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        sozluk = list(reader)
        kelimeler = [satir[0].strip() for satir in sozluk]

    set_kelimeler = set(kelimeler)
    print(f"Len kelimeler: {len(kelimeler)}, len set kelimeler: {len(set_kelimeler)}")

    ekli_kelimeler = []

    for kelime in set_kelimeler:
        try:
            print(f"{kelime:<16} --> {ek_uret(kelime):<16}")
            ekli_kelimeler.append(ek_uret(kelime))
        except Exception as e:
            print(f"{kelime:<16} --> {e}")
            exit(1)

    with open("ise_ekli_kelimeler.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ekli_kelimeler))
