import sys
import os

# Add the parent directory to the path to import the trnorm package
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm import normalize
from trnorm.dimension_utils import preprocess_dimensions, normalize_dimensions
from trnorm.unit_utils import normalize_units
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.ordinals import normalize_ordinals
from trnorm.symbols import convert_symbols, add_symbol_mapping
from trnorm.symbols import SymbolConverter, get_all_mappings
from trnorm.apostrophe_handler import remove_apostrophes
from trnorm.text_utils import (
    turkish_lower,
    turkish_upper,
    turkish_capitalize,
    is_turkish_upper,
    sapkasiz,
)
from trnorm.time_utils import normalize_times
from trnorm.suffix_handler import merge_suffixes

my_pipeline = [
    normalize_times,
    normalize_ordinals,     # Moved before remove_apostrophes to preserve apostrophes in ordinals
    convert_symbols,
    convert_numbers_to_words_wrapper,
    merge_suffixes,         # Add suffix handler to merge Turkish suffixes
    remove_apostrophes,
    sapkasiz,
    preprocess_dimensions,
    normalize_dimensions,  # adds "çarpı" as a replacement to "x", but I'm not sure if we really need this.
    normalize_units,       # converts units like "cm" has been expanded to "santimetre",
                                # "kg" has been expanded to "kilogram"
                                # "°C" has been expanded to "santigrat derece"
    
    
]

def apply_normalizers(text):
    for norm in my_pipeline:
        text = norm(text)
    return text


example_texts = [
    "Turner'ın 'Köle Gemisi' isimli tablosuna bakıyoruz.",
    "Odanın boyutları 2x3x4 metre.",
    "Halının boyutu 120x180cm.",
    "Ağırlığı 5 kg. ve uzunluğu 10 metre.",
    "Sıcaklık 25 °C ve nem %60.",
    "Saat 14:30'da %25 indirimli ürünler satışa çıkacak.",
    "Ürün fiyatı 1.250,75 TL'dir.",
    "1. sınıfta 23 öğrenci var.",
    "Dün 3x4 metre halı aldım.",
    "II. Wilhelm, Almanya imparatoruydu.",
    "V. Karl, Kutsal Roma İmparatoru'ydu.",
    "1'inci sınıf 1inci kat",
    "2. Mahmud ya da II. Mahmud.",
    "1.000 ₺",
    "$500",
    "600 $",
    "kâğıt ve kalem",
    "Âdem ile Havva",
    "îmanın kimde",
    "Îman büyük harfle şapkalı",
    "hûr ne",
    "Yavru ile kâtip",
    "Python 2.7 - 2.4 ASA - Pi sayısı 3.14",
    "Bu kitap 1990'ların en iyi eserleri arasında.",
    "Toros ile hamile",
    "Hayat sana limon verdi ise limonata yap",
    "Hâl böyle iken böyle dedi adam."
]

# Test for just ordinals
print("\n\n--- Testing just ordinals ---")
ordinal_tests = [
    "1'inci sınıf 1inci kat",
    "2. Mahmud ya da II. Mahmud.",
    "1. sınıfta 23 öğrenci var.",
    "V. Karl, Kutsal Roma İmparatoru'ydu.",
]

# Test with just ordinals normalizer
for e in ordinal_tests:
    print(f"Original: {e}")
    print(f"Normalized: {normalize_ordinals(e)}")
    print()

# Full pipeline test
print("\n--- Testing full pipeline ---")
for e in example_texts:
    print(apply_normalizers(e))
