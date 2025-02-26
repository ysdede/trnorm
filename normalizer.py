"""
https://tdk.gov.tr/icerik/yazim-kurallari/sayilarin-yazilisi/
https://www.dragoman.ist/tr/turkcede-sayilarin-yazilisi/

Sayıların Yazılışı  23 Ocak 2019    Kategori: Yazım Kuralları

1. Sayılar harflerle de yazılabilir: bin yıldan beri, on dört gün, haftanın beşinci günü, üç ayda bir, yüz soru, iki hafta sonra, üçüncü sınıf vb.
Buna karşılık saat, para tutarı, ölçü, istatistik verilere ilişkin sayılarda rakam kullanılır:
        17.30’da, 11.00’de, 1.500.000 lira, 25 kilogram, 150 kilometre, 15 metre kumaş, 1.250.000 kişi vb.
Saatler ve dakikalar metin içinde yazıyla da yazılabilir:
        saat dokuzu beş geçe, saat yediye çeyrek kala, saat sekizi on dakika üç saniye geçe, mesela saat onda vb.
Dört veya daha çok basamaklı sayıların kolay okunabilmesi amacıyla içinde geçen bin, milyon, milyar ve trilyon sözleri harfle yazılabilir:
        1 milyar 500 milyon kişi, 3 bin 255 kalem, 8 trilyon 412 milyar vb.

2. Birden fazla kelimeden oluşan sayılar ayrı yazılır: iki yüz, üç yüz altmış beş, bin iki yüz elli bir vb.

3. Para ile ilgili işlemlerle senet, çek vb. ticari belgelerde geçen sayılar bitişik yazılır: 650,35 (altıyüzelliTL,otuzbeşkr.)

4. Yüzde ve binde işaretleri yazılırken sayılarla işaret arasında boşluk bırakılmaz: %25, ‰50 vb.

5. Adları sayılardan oluşan iskambil oyunları bitişik yazılır: altmışaltı, ellibir, yirmibir vb.

6. Romen rakamları tarihî olaylarda, yüzyıllarda, hükümdar adlarında, tarihlerde ayların yazılışında, kitap ve dergi ciltlerinde,
kitapların asıl bölümlerinden önceki sayfaların numaralandırılmasında, maddelerin sıralandırılmasında kullanılır:
        II. Dünya Savaşı; XX. yüzyıl; III. Selim, XIV. Louis, II. Wilhelm, V. Karl, VIII. Edward; 1.XI.1928; I. Cilt; I)… II) … vb.

7. Dört veya daha çok basamaklı sayılar sondan sayılmak üzere üçlü gruplara ayrılarak yazılır ve aralarına nokta konur:
        4.567, 326.197, 49.750.812, 28.434.250.310.500 vb.

8. Sayılarda kesirler virgülle ayrılır: 15,2 (15 tam, onda 2); 5,26 (5 tam, yüzde 26) vb.

9. Sıra sayıları yazıyla ve rakamla gösterilebilir. Rakamla gösterilmesi durumunda ya rakamdan sonra bir nokta konur ya da rakamdan sonra
kesme işareti konularak derece gösteren ek yazılır: 15., 56., XX.; 15’inci, 56’ncı, XX’nci vb.
UYARI: Sıra sayıları ekle gösterildiklerinde rakamdan sonra sadece kesme işareti ve ek yazılır, ayrıca nokta konmaz: 8.’inci değil 8’inci, 2.’nci değil 2’nci vb.

10. Üleştirme sayıları rakamla değil yazıyla belirtilir: 2’şer değil ikişer, 9’ar değil dokuzar, 100’er değil yüzer vb.

11. Bayağı kesirlere getirilecek ekler alttaki sayı esas alınarak yazılır: 4/8’i (dört bölü sekizi), 1/2’si (bir bölü ikisi) vb.

12. Bir zorunluluk olmadıkça cümle rakamla başlamaz.

"""

import re
import regex
import random
from asrtk.variables import abbreviations_dict
from asrtk.variables import unit_translations
from asrtk.variables import punctuation_dict
from asrtk.ordinals import normalize_ordinals
from asrtk.core.text import (
    turkish_capitalize,
    turkish_upper,
    turkish_lower,
    is_turkish_upper
)
from asrtk.variables import special_cases

def detect_decimal_separator(s: str) -> str:
    pattern = r"(\d+)(\.|,)(\d+)"
    match = re.search(pattern, s)

    if match:
        return match.group(2)  # Group 2 is the separator
    return None


class Normalizer:
    """
    - For more details about the algorithms and datasets, see `Readme <https://github.com/vngrs-ai/VNLP/blob/main/vnlp/normalizer/ReadMe.md>`_.
    """

    def __init__(self):
        self.decimal_seperator = None

    def _convert_dates_to_words(self, text, merge_words):
        # Regular expression to match dates
        date_pattern = r'\b(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})\b'
        # Function to replace dates with their word form
        def replace_with_words(match):
            day, month, year = match.groups()
            day_words = self._num_to_words(int(day), 0, merge_words=merge_words)
            month_words = self._num_to_words(int(month), 0, merge_words=merge_words)
            year_words = self._num_to_words(int(year), 0, merge_words=merge_words)
            return f"{day_words} {month_words} {year_words}"

        return re.sub(date_pattern, replace_with_words, text)

    def convert_numbers_to_words(self, input_text, num_dec_digits=6, decimal_seperator=",", merge_words=False):
        """
        Inherited from 'https://github.com/vngrs-ai/vnlp/blob/main/vnlp/normalizer/normalizer.py'

        Converts numbers to word form.

        Args:
            tokens:
                List of input tokens.
            num_dec_digits:
                Number of precision (decimal points) for floats.
            decimal_seperator:
                Decimal seperator character. Comma "," CAN NOT be "." for Turkish!

        Returns:
            List of converted tokens

        """
        input_text = self._convert_dates_to_words(input_text, merge_words)
        input_text = input_text.replace(", ", " |$| ")
        input_text = input_text.replace("-", " ~ ")
        input_text = input_text.replace(":", ": ")  # Ensure space after colon
        self.decimal_seperator = decimal_seperator
        
        # Handle thousand separators (periods) and decimal separators
        words = []
        for word in input_text.split():
            converted = word
            if any(char.isnumeric() for char in word):
                # Handle trailing comma
                append_comma = False
                if word.endswith(","):
                    word = word[:-1]
                    append_comma = True
                
                # Handle decimal and thousand separators
                parts = word.split(",")
                if len(parts) > 1:  # Has decimal part
                    integer_part = parts[0].replace(".", "")
                    decimal_part = parts[1]
                    try:
                        num = float(integer_part + "." + decimal_part)
                        converted = self._num_to_words(num, num_dec_digits, merge_words)
                    except ValueError:
                        pass
                else:  # No decimal part
                    try:
                        num = int(word.replace(".", ""))
                        converted = self._int_to_words(num, merge_words=merge_words)
                    except ValueError:
                        pass
                
                if append_comma:
                    converted += ","
            words.append(converted)

        result = " ".join(words)
        result = result.replace(" |$| ", ", ")
        result = result.replace(" ~ ", "-")
        result = result.replace("  ", " ")  # Remove double spaces
        return result.strip()


    def _is_token_valid_turkish(self, token):
        """
        Checks whether given token is valid according to Turkish.
        """
        valid_according_to_stemmer_analyzer = not (
            self._stemmer_analyzer.candidate_generator.get_analysis_candidates(token)[0][-1] == "Unknown"
        )
        valid_according_to_lexicon = token in self._words_lexicon
        return valid_according_to_stemmer_analyzer or valid_according_to_lexicon

    def _int_to_words(self, main_num, put_commas=False, merge_words=False):
        """
        This function is adapted from:
        https://github.com/Omerktn/Turkish-Lexical-Representation-of-Numbers/blob/master/src.py
        It had a few bugs with numbers like 1000 and 1010, which are resolved.
        """
        tp = [
            "yüz",
            "bin",
            "milyon",
            "milyar",
            "trilyon",
            "katrilyon",
            "kentilyon",
            "seksilyon",
            "septilyon",
            "oktilyon",
            "nonilyon",
            "desilyon",
            "undesilyon",
            "dodesilyon",
            "tredesilyon",
            "katordesilyon",
            "seksdesilyon",
            "septendesilyon",
            "oktodesilyon",
            "nove mdesilyon",
            "vigintilyon",
        ]

        dec = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
        ten = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]

        parts = []

        if main_num == 0:
            return "sıfır"

        # Handle billions
        if main_num >= 1000000000:
            billions = main_num // 1000000000
            remainder = main_num % 1000000000
            
            if billions == 1:
                parts.append("bir")
            else:
                parts.extend(self._int_to_words(billions, False, False).split())
            parts.append("milyar")
            
            if remainder > 0:
                parts.extend(self._int_to_words(remainder, False, False).split())
            
            result = " ".join(parts)
            return result.replace(" ", "") if merge_words else result

        # Handle millions
        if main_num >= 1000000:
            millions = main_num // 1000000
            remainder = main_num % 1000000
            
            if millions == 1:
                parts.append("bir")
            else:
                parts.extend(self._int_to_words(millions, False, False).split())
            parts.append("milyon")
            
            if remainder > 0:
                parts.extend(self._int_to_words(remainder, False, False).split())
            
            result = " ".join(parts)
            return result.replace(" ", "") if merge_words else result

        # Handle thousands
        if main_num >= 1000:
            thousands = main_num // 1000
            remainder = main_num % 1000
            
            if thousands == 1:
                parts.append("bin")
            else:
                parts.extend(self._int_to_words(thousands, False, False).split())
                parts.append("bin")
            
            if remainder > 0:
                parts.extend(self._int_to_words(remainder, False, False).split())
            
            result = " ".join(parts)
            return result.replace(" ", "") if merge_words else result

        # Handle hundreds
        if main_num >= 100:
            hundreds = main_num // 100
            remainder = main_num % 100
            
            if hundreds == 1:
                parts.append("yüz")
            else:
                parts.append(dec[hundreds])
                parts.append("yüz")
            
            if remainder > 0:
                parts.extend(self._int_to_words(remainder, False, False).split())
            
            result = " ".join(parts)
            return result.replace(" ", "") if merge_words else result

        # Handle tens
        if main_num >= 10:
            tens = main_num // 10
            remainder = main_num % 10
            
            parts.append(ten[tens])
            if remainder > 0:
                parts.append(dec[remainder])
            
            result = " ".join(parts)
            return result.replace(" ", "") if merge_words else result

        # Handle ones
        return dec[main_num]


    def _num_to_words(self, num, num_dec_digits, merge_words=False, alt_seperator=""):
        integer_part = int(num)
        decimal_part = round(num % 1, num_dec_digits)

        # if number is int (considering significant decimal digits)
        if decimal_part < 10**-num_dec_digits:
            return self._int_to_words(integer_part, merge_words)
        # if number is float
        else:
            str_decimal = "{:f}".format(round(num % 1, num_dec_digits))[2:]

            zeros_after_decimal = 0
            for char in str_decimal:
                if char == "0":
                    zeros_after_decimal += 1
                else:
                    break

            str_decimal_stripped_from_zeros = str_decimal.strip("0")  # strip gets rid of heading and trailing 0s in string form

            if str_decimal_stripped_from_zeros == "":
                decimal_part = 0
            else:
                decimal_part = int(str_decimal_stripped_from_zeros)

            parts = []
            parts.extend(self._int_to_words(integer_part, False).split())
            parts.append("virgül")
            if zeros_after_decimal > 0:
                parts.extend(["sıfır"] * zeros_after_decimal)
            parts.extend(self._int_to_words(decimal_part, False).split())

            result = " ".join(parts)
            return result.replace(" ", "") if merge_words else result


def tts_normalize(text):
    """
    Preprocess text for TTS synthesis by normalizing numbers, units, and symbols.

    Args:
        text (str): The input text to be normalized.
        unit_translations (dict): A dictionary mapping abbreviations to their full forms.

    Returns:
        str: The normalized text.

    """
    spelled_out_numbers = ["bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]

    # Define a regex pattern that matches abbreviations preceded by numbers/spelled-out numbers
    pattern = r'(\d+(?:\.\d+)?)\s*(' + '|'.join(re.escape(unit) for unit in unit_translations.keys()) + r')\b'
    text = text.replace("°", " ° ").replace("  ", " ")

    def replace_abbr(match):
        """Replace matched abbreviation with its full form."""
        number, unit = match.groups()
        unit = unit.lower()

        if any(number.startswith(word) for word in spelled_out_numbers) or number.isdigit() or '.' in number:
            replacement = f"{number} {unit_translations[unit]}"
        else:
            replacement = match.group(0)

        return replacement

    # Replace all occurrences of abbreviations with their full form
    normalized_text = re.sub(pattern, replace_abbr, text)

    normalized_text = normalized_text.replace("(+)", " pozitif ").replace("(-)", " negatif ").replace("+", " artı ").replace("  ", " ").strip()  # TODO translation'a taşı.

    if normalized_text.endswith("."):
        # Noktadan önceki karakteri kontrol et
        if not re.search(r'\d\.$', normalized_text):
            # Noktadan önce sayı yoksa, noktayı virgülle değiştir
            normalized_text = normalized_text[:-1] + ","

    # Ensure the text ends with a comma, unless it ends with a question mark or period
    if normalized_text[-1] not in ["?", ","]:
        normalized_text += ","

    return normalized_text


def dio_normalizer(text):
    """
    Preprocess text by replacing abbreviations with their full forms.

    Args:
        text (str): The input text to be normalized.
        abbreviations_dict (dict): A dictionary mapping abbreviations to their full forms.

    Returns:
        str: The normalized text.

    """

    # apply all special cases as key, value replace to text
    for key, value in special_cases.items():
        text = text.replace(key, value)

    # Sort abbreviations by length to match longer ones first
    sorted_abbr = sorted(abbreviations_dict.keys(), key=len, reverse=True)

    # Create a regular expression pattern that matches any abbreviation as a whole word
    pattern = r'\b(?:' + '|'.join(re.escape(abbr) for abbr in sorted_abbr) + r')\b'

    def replace_abbr(match):
        """Replace matched abbreviation with its full form."""
        word = match.group(0)
        # Get the first long form from the dictionary
        replacement = abbreviations_dict.get(word, [word])[0]
        return replacement

    # Replace all occurrences of any abbreviation with their full form
    normalized_text = re.sub(pattern, replace_abbr, text)

    return normalized_text


def replace_multiplication_symbol_in_dimensions(text):
    """
    Replace the multiplication symbol 'x' used in mathematical dimensions with a more descriptive term.

    Args:
        text (str): The input text containing dimensional expressions.

    Returns:
        str: The text with the multiplication symbol 'x' replaced by a descriptive term in dimensional expressions.

    """
    # Define a regex pattern that matches 'x' between numbers (with optional decimal parts and optional units)
    pattern = r'(\d+(?:\.\d+)?\s*(?:cm|mm)?)(\s*x\s*)(\d+(?:\.\d+)?\s*(?:cm|mm)?)(?:(\s*x\s*)(\d+(?:\.\d+)?\s*(?:cm|mm)?))?'

    def replacement(match):
        """Construct the replacement string with a descriptive term."""
        number1, x1, number2, x2, number3 = match.groups()
        replacement = f"{number1.strip()} çarpı {number2.strip()}"
        if x2 and number3:
            replacement += f" çarpı {number3.strip()}"
        return replacement

    # Replace all occurrences of 'x' between numbers with a descriptive term
    return re.sub(pattern, replacement, text).replace("  ", " ").strip()


def convert_numbers_to_words_wrapper(text):
    normalizer = Normalizer()
    return normalizer.convert_numbers_to_words(text)


def apply_normalizers(text, normalizers=[turkish_capitalize, replace_multiplication_symbol_in_dimensions, dio_normalizer, tts_normalize, normalize_ordinals, convert_numbers_to_words_wrapper]):
    """
    Apply a sequence of normalization functions to a given text.

    🚨 Note: The `fill_dates` normalizer is applied first to ensure reproducibility
    when generating random dates, as the text hash is used as a random seed.

    Args:
        text (str): The input text to be normalized.
        normalizers (list): A list of normalization functions to be applied
            to the text in the given order.

    Returns:
        str: The normalized text with double spaces replaced by single spaces.
    """
    for normalizer in normalizers:
        text = normalizer(text)
    return text.replace("  ", " ")


def normalize_dictation(text):
    med_stopwords = ["nokta.", "paragraf", "bitti"]

    stopwords_sorted = sorted(med_stopwords, key=len, reverse=True)

    def remove_stopword(match):
        return ''

    normalized_text = regex.sub(r'[\n\t\[\]\{\}]', ' ', text)
    normalized_text = regex.sub(r'\s+', ' ', normalized_text).strip()

    for stopword in stopwords_sorted:
        # Adjusting the pattern to optionally include following punctuation like '.', ',', etc.
        pattern = r'\b' + regex.escape(stopword) + r'\b[.,]?'
        normalized_text = regex.sub(pattern, remove_stopword, normalized_text, flags=regex.IGNORECASE | regex.UNICODE)

    normalized_text = regex.sub(r'\s+', ' ', normalized_text).strip()

    # Handle edge cases for punctuation
    normalized_text = regex.sub(r'\.\s+\.', '.', normalized_text)  # Replace '. .' with '.'
    normalized_text = regex.sub(r'\s+\.', '.', normalized_text)  # Ensure no space before '.'

    return normalized_text


if __name__ == "__main__":
    # Example usage
    converter = Normalizer()
    # print(converter.convert_numbers_to_words('"123", "456,789", "0.12"'))
    # print(converter.convert_numbers_to_words("Her yıl Mart ayının 13. günü Pi günü olarak kutlanır. 3.14"))
    # print(converter.convert_numbers_to_words("9876.43 ve 3,14 aynı cümlede."))
    # print("*" * 50)

    # print(converter.convert_numbers_to_words("Küsuratlı bazı sayılar, 175.5 try."))
    # print(converter.convert_numbers_to_words("Virgülle ayrılmış bazı sayılar, 1,5 x 2,6, 3,2 x 6,8 milimetre."))
    print(converter.convert_numbers_to_words("1,5 gün önce."))
    # print(converter.convert_numbers_to_words("yaklaşık 4,5-5 cm'ye kadar"))
    print(converter.convert_numbers_to_words("Binler ayracı ile ayrılmış Türkçe sayılar: 5000000 lira"))
    print(converter.convert_numbers_to_words("3. gün"))
    print(converter.convert_numbers_to_words("09.05.2021 günü"))
