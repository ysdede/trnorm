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

def detect_decimal_separator(s: str) -> str:
    pattern = r"(\d+)(\.|,)(\d+)"
    match = re.search(pattern, s)

    if match:
        return match.group(2)  # Group 2 is the separator
    return None


class NumberToTextConverter:
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
        
    def _convert_times_to_words(self, text, merge_words):
        """
        Convert time expressions to words before general number conversion.
        
        This method identifies time patterns like "saat 22.00" or "22:30" and 
        converts them appropriately to prevent misinterpretation as decimal numbers.
        
        Args:
            text (str): The input text containing time expressions
            merge_words (bool): Whether to merge words in the output
            
        Returns:
            str: The text with time expressions properly converted
        """
        # Pattern for times with "saat" prefix (e.g., "saat 22.00", "saat 9:45")
        saat_pattern = r'(\bsaat\s+)(\d{1,2})([\.:])(\d{2})\b'
        
        def replace_saat_time(match):
            saat_prefix = match.group(1)  # "saat "
            hours = match.group(2)
            separator = match.group(3)  # . or :
            minutes = match.group(4)
            
            # Convert hours and minutes to words
            hours_words = self._num_to_words(int(hours), 0, merge_words=merge_words)
            
            # Special case for half hours
            if minutes == "30":
                return f"{saat_prefix}{hours_words} buçuk"
            
            minutes_words = self._num_to_words(int(minutes), 0, merge_words=merge_words)
            return f"{saat_prefix}{hours_words} {minutes_words}"
        
        # Process times with "saat" prefix
        processed_text = re.sub(saat_pattern, replace_saat_time, text)
        
        # Pattern for standalone times that might be time expressions (e.g., "22.00", "9:45")
        time_pattern = r'\b(\d{1,2})([\.:])(\d{2})\b'
        
        def is_likely_time(hours, minutes):
            # Check if hours and minutes are valid time components
            h = int(hours)
            m = int(minutes)
            return 0 <= h <= 23 and 0 <= m <= 59 and len(minutes) == 2
        
        def replace_standalone_time(match):
            hours = match.group(1)
            separator = match.group(2)
            minutes = match.group(3)
            
            # Only convert if it looks like a valid time
            if is_likely_time(hours, minutes):
                hours_words = self._num_to_words(int(hours), 0, merge_words=merge_words)
                
                # Special case for half hours
                if minutes == "30":
                    return f"{hours_words} buçuk"
                
                minutes_words = self._num_to_words(int(minutes), 0, merge_words=merge_words)
                return f"{hours_words} {minutes_words}"
            
            # If it doesn't look like a time, return the original text
            return match.group(0)
        
        # Process standalone times
        return re.sub(time_pattern, replace_standalone_time, processed_text)

    def _is_ordinal_or_non_standard_number(self, word):
        """
        Check if a number is an ordinal (ends with period) or has a non-standard format 
        that should not be converted to text.
        
        Non-standard formats to skip (return True):
        - Numbers ending with a period: 2., 10., etc. (ordinals)
        - Numbers with period as decimal separator: 3.1, 10.5, 2.14, etc.
        - Numbers with incorrect thousand separator pattern: 1.0, 10.5, etc.
        
        Args:
            word (str): The word to check
            
        Returns:
            bool: True if it's an ordinal or non-standard number, False otherwise
        """
        # Skip if it's not a numeric string
        if not any(char.isdigit() for char in word):
            return False
            
        # Check for numbers ending with a period (ordinals)
        if re.match(r'^\d+\.$', word):
            return True
            
        # Check for numbers with period as decimal separator
        # This pattern matches numbers like 3.1, 10.5, 2.14, etc.
        # But we need to exclude properly formatted Turkish numbers with thousand separators
        if '.' in word and ',' not in word:
            # If it's a properly formatted Turkish number with thousand separators
            # like 1.000, 10.000, 100.000, 1.000.000, etc., don't skip it
            if re.match(r'^\d{1,3}(\.\d{3})+$', word):
                return False
                
            # If it has a period but doesn't match the thousand separator pattern,
            # it's likely a non-standard format (like 3.1, 10.5, etc.)
            return True
                
        return False

    def convert_numbers_to_words(self, input_text, num_dec_digits=6, decimal_seperator=",", merge_words=False):
        """
        Convert numeric strings into their Turkish text representation.

        This method converts numbers in the input text to their Turkish word equivalents.
        For example, "123" becomes "yüz yirmi üç".

        The method handles:
        - Regular numbers (e.g., "123" -> "yüz yirmi üç")
        - Decimal numbers (e.g., "12,5" -> "on iki virgül beş")
        - Numbers with apostrophes (e.g., "100'lerce" -> "yüz'lerce")
        - Numbers with divide symbols (e.g., "7/24" -> "yedi/yirmi dört")
        - Combinations of the above (e.g., "2/3'ü" -> "iki/üç'ü")
        - Time expressions (e.g., "saat 22.00" -> "saat yirmi iki sıfır sıfır")
        - Date expressions (e.g., "12.05.2023" -> "on iki beş iki bin yirmi üç")

        Args:
            input_text (str): The input text containing numbers to be converted.
            num_dec_digits (int, optional): Maximum number of decimal digits to convert. Defaults to 6.
            decimal_seperator (str, optional): The character used as decimal separator. Defaults to ",".
            merge_words (bool, optional): Whether to merge words in the output. Defaults to False.

        Returns:
            str: The input text with numbers converted to their Turkish word equivalents.
        """
        # First handle dates and times before general number conversion
        input_text = self._convert_dates_to_words(input_text, merge_words)
        input_text = self._convert_times_to_words(input_text, merge_words)
        
        # Special handling for numbers followed by commas and spaces (e.g., "13, ")
        # Replace with a special placeholder to preserve the pattern
        comma_space_placeholder = " |COMMA_SPACE| "
        input_text = re.sub(r'(\d+)(,\s+)', lambda m: self._int_to_words(int(m.group(1)), merge_words=merge_words) + comma_space_placeholder, input_text)
        
        input_text = input_text.replace(", ", " |$| ")
        input_text = input_text.replace("-", " ~ ")
        input_text = input_text.replace(":", ": ")  # Ensure space after colon
        
        # Handle divide symbol (/) in formats like 7/24 and 1/3
        # We'll convert the numbers on both sides while preserving the divide symbol
        divide_placeholder = " |DIVIDE| "
        
        # Process words that contain the divide symbol
        processed_text = []
        for word in input_text.split():
            if "/" in word and any(char.isnumeric() for char in word):
                # Check if it's a numeric format like 7/24 or 1/3
                parts = word.split("/")
                if len(parts) == 2 and all(part.strip() and any(char.isnumeric() for char in part) for part in parts):
                    # Replace / with the placeholder
                    processed_word = parts[0] + divide_placeholder + parts[1]
                    processed_text.append(processed_word)
                else:
                    processed_text.append(word)
            else:
                processed_text.append(word)
        
        input_text = " ".join(processed_text)
        self.decimal_seperator = decimal_seperator
        
        # Handle thousand separators (periods) and decimal separators
        words = []
        for word in input_text.split():
            # Special case for numbers with apostrophes and thousand separators
            if "'" in word and re.match(r'^\d{1,3}(\.\d{3})+\'', word):
                parts = word.split("'", 1)
                number_part = parts[0]
                suffix_part = "'" + parts[1] if len(parts) > 1 else ""
                
                try:
                    num = int(number_part.replace(".", ""))
                    converted_number = self._int_to_words(num, merge_words=merge_words)
                    words.append(converted_number + suffix_part)
                    continue
                except ValueError:
                    pass
            
            # Skip conversion if the number is an ordinal or has a non-standard format
            if self._is_ordinal_or_non_standard_number(word):
                words.append(word)
                continue
                
            # Check if the word contains an apostrophe with a number before it
            if "'" in word and any(char.isnumeric() for char in word.split("'")[0]):
                # Split by apostrophe
                parts = word.split("'", 1)  # Split only on the first apostrophe
                number_part = parts[0]
                suffix_part = "'" + parts[1] if len(parts) > 1 else ""
                
                # Skip conversion if the number part is an ordinal or has a non-standard format
                if self._is_ordinal_or_non_standard_number(number_part):
                    words.append(word)
                    continue
                
                converted_number = number_part
                if any(char.isnumeric() for char in number_part):
                    # Handle trailing comma
                    append_comma = False
                    if number_part.endswith(","):
                        number_part = number_part[:-1]
                        append_comma = True
                    
                    # Handle decimal and thousand separators
                    decimal_parts = number_part.split(",")
                    if len(decimal_parts) > 1:  # Has decimal part
                        integer_part = decimal_parts[0].replace(".", "")
                        decimal_part = decimal_parts[1]
                        try:
                            num = float(integer_part + "." + decimal_part)
                            converted_number = self._num_to_words(num, num_dec_digits, merge_words)
                        except ValueError:
                            pass
                    else:  # No decimal part
                        try:
                            num = int(number_part.replace(".", ""))
                            converted_number = self._int_to_words(num, merge_words=merge_words)
                        except ValueError:
                            pass
                    
                    if append_comma:
                        converted_number += ","
                words.append(converted_number + suffix_part)
            else:
                converted = word
                if any(char.isnumeric() for char in word):
                    # Handle trailing comma
                    append_comma = False
                    if word.endswith(","):
                        word = word[:-1]
                        append_comma = True
                    
                    # Handle decimal and thousand separators
                    decimal_parts = word.split(",")
                    if len(decimal_parts) > 1:  # Has decimal part
                        integer_part = decimal_parts[0].replace(".", "")
                        decimal_part = decimal_parts[1]
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
        
        # Replace the divide placeholder with the original divide symbol (/)
        result = result.replace(divide_placeholder, "/")
        
        # Restore the comma space placeholder
        result = result.replace(comma_space_placeholder, ", ")
        
        result = result.replace("  ", " ")  # Remove double spaces
        return result.strip()
        

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
    converter = NumberToTextConverter()
    return converter.convert_numbers_to_words(text)
