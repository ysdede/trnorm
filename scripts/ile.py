"""
This module provides functionality for adding the Turkish suffix "ile" (with) to words.

The suffix "ile" changes form based on vowel harmony and whether the word ends with a vowel:
- If the word ends with a consonant and the last vowel is back (a, ı, o, u): "la" is added
- If the word ends with a consonant and the last vowel is front (e, i, ö, ü): "le" is added
- If the word ends with a vowel and the last vowel is back (a, ı, o, u): "yla" is added
- If the word ends with a vowel and the last vowel is front (e, i, ö, ü): "yle" is added

Examples:
- Toros + ile = Torosla
- Ankara + ile = Ankarayla
- İstanbul + ile = İstanbulla
- Ali + ile = Aliyle
"""

from text_utils import ekle
from test_strings import ile_test_words, istisnalar_test_words


def ek_uret(kelime):
    """
    Add the Turkish suffix "ile" to a word, following Turkish vowel harmony rules.
    
    Args:
        kelime (str): The word to add the suffix to
        
    Returns:
        str: The word with the "ile" suffix added
    """
    return ekle(kelime, "ile")


# Run tests if this file is executed directly
if __name__ == "__main__":
    # Test regular words
    for kelime, beklenen in ile_test_words.items():
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

    with open("ile_ekli_kelimeler.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ekli_kelimeler))
