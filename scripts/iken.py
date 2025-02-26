"""
This module provides functionality for adding the Turkish suffix "iken" (while/when) to words.

The suffix "iken" changes form based on whether the word ends with a vowel:
- If the word ends with a consonant: "ken" is added directly
- If the word ends with a vowel: "yken" is added
- For abbreviations or short words (≤ 3 letters): "iken" is kept separate

Examples:
- başlayacak + iken = başlayacakken (while starting)
- çalışıyor + iken = çalışıyorken (while working)
- evde + iken = evdeyken (while at home)
- AB + iken = AB iken (while AB)
"""

import sys
import os

# Add parent directory to path to allow imports from parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trnorm.text_utils import ekle
from trnorm.test_strings import iken_test_words


def ek_uret(kelime):
    """
    Add the Turkish suffix "iken" to a word, following Turkish grammar rules.
    
    Args:
        kelime (str): The word to add the suffix to
        
    Returns:
        str: The word with the "iken" suffix added
    """
    return ekle(kelime, "iken")


# Run script if executed directly
if __name__ == "__main__":
    # Test with examples from test_strings.py
    for kelime, beklenen in iken_test_words.items():
        result = ek_uret(kelime)
        print(f"{kelime:<16} {beklenen:<16} --> {result:<16}")
        assert result == beklenen

    sozluk_tsv = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/TDK_Sozluk-Turkish.tsv")

    import csv

    with open(sozluk_tsv, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)  # Skip header
        sozluk = list(reader)
        kelimeler = [satir[0].strip() for satir in sozluk if len(satir) > 0]

    set_kelimeler = set(kelimeler)
    print(f"Len kelimeler: {len(kelimeler)}, len set kelimeler: {len(set_kelimeler)}")

    ekli_kelimeler = []

    for kelime in set_kelimeler:
        try:
            result = ek_uret(kelime)
            print(f"{kelime:<16} --> {result:<16}")
            ekli_kelimeler.append(result)
        except Exception as e:
            print(f"{kelime:<16} --> {e}")
            exit(1)

    output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), r"data\iken_ekli_kelimeler.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(ekli_kelimeler))
    
    print(f"Saved {len(ekli_kelimeler)} words with 'iken' suffix to {output_file}")
