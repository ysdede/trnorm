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

if __name__ == "__main__":
    # Example usage
    from num_to_text import NumberToTextConverter
    converter = NumberToTextConverter()
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
