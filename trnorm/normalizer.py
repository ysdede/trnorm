"""
Turkish Text Normalizer

This module provides a comprehensive normalizer that applies all normalization steps
in the correct order to Turkish text.

It combines all the normalization functionalities from the trnorm package:
- Number to text conversion
- Ordinal number normalization
- Roman numeral conversion
- Symbol conversion
- Turkish character handling
- Text utilities
- Dimension handling
- Unit abbreviation expansion
"""

from typing import List, Union, Optional

from trnorm.num_to_text import convert_numbers_to_words_wrapper, replace_multiplication_symbol_in_dimensions
from trnorm.ordinals import normalize_ordinals
from trnorm.roman_numerals import roman_to_arabic, find_roman_ordinals
from trnorm.symbols import convert_symbols, default_converter
from trnorm.legacy_normalizer import normalize_text, replace_hatted_characters
from trnorm.text_utils import turkish_lower, sapkasiz
from trnorm.dimension_utils import preprocess_dimensions, normalize_dimensions
from trnorm.unit_utils import normalize_units


class TurkishNormalizer:
    """
    A comprehensive normalizer for Turkish text.

    This class applies all normalization steps in the correct order to Turkish text.
    It can process both single strings and lists of strings.
    """

    def __init__(self, 
                 apply_number_conversion: bool = True,
                 apply_ordinal_normalization: bool = True,
                 apply_symbol_conversion: bool = True,
                 apply_multiplication_symbol: bool = True,
                 apply_unit_normalization: bool = True,
                 apply_legacy_normalization: bool = False,
                 lowercase: bool = True,
                 remove_hats: bool = True):
        """
        Initialize the Turkish normalizer with configuration options.

        Args:
            apply_number_conversion (bool): Whether to convert numbers to their text representation
            apply_ordinal_normalization (bool): Whether to normalize ordinals
            apply_symbol_conversion (bool): Whether to convert symbols to their text representation
            apply_multiplication_symbol (bool): Whether to replace multiplication symbol 'x' with 'çarpı'
            apply_unit_normalization (bool): Whether to expand unit abbreviations to full text
            apply_legacy_normalization (bool): Whether to apply legacy normalization (more aggressive)
            lowercase (bool): Whether to convert text to lowercase
            remove_hats (bool): Whether to remove circumflex (hat) from Turkish characters
        """
        self.apply_number_conversion = apply_number_conversion
        self.apply_ordinal_normalization = apply_ordinal_normalization
        self.apply_symbol_conversion = apply_symbol_conversion
        self.apply_multiplication_symbol = apply_multiplication_symbol
        self.apply_unit_normalization = apply_unit_normalization
        self.apply_legacy_normalization = apply_legacy_normalization
        self.lowercase = lowercase
        self.remove_hats = remove_hats

    def normalize(self, text: Union[str, List[str]]) -> Union[str, List[str]]:
        """
        Apply all normalization steps to the input text.

        This method applies the following normalization steps in order:
        1. Preprocess dimensions (add spaces between numbers and 'x')
        2. Symbol conversion (%, $, etc. to their text representation)
        3. Multiplication symbol replacement (3x4 -> 3 çarpı 4)
        4. Number to text conversion (123 -> yüz yirmi üç)
        5. Ordinal normalization (1. -> birinci)
        6. Unit abbreviation expansion (cm -> santimetre)
        7. Character normalization (lowercase, remove hats)
        8. Legacy normalization (if enabled)

        Args:
            text (Union[str, List[str]]): Input text or list of texts to normalize

        Returns:
            Union[str, List[str]]: Normalized text or list of normalized texts
        """
        # Handle list input
        if isinstance(text, list):
            return [self.normalize(item) for item in text]

        # Apply normalization steps in order
        result = text
        
        # 1. Preprocess dimensions to add spaces between numbers and 'x'
        result = preprocess_dimensions(result)

        # 2. Symbol conversion
        if self.apply_symbol_conversion:
            result = convert_symbols(result)
            
        # 3. Multiplication symbol replacement
        if self.apply_multiplication_symbol:
            # Use the new normalize_dimensions function instead of replace_multiplication_symbol_in_dimensions
            result = normalize_dimensions(result)

        # 4. Number to text conversion
        if self.apply_number_conversion:
            result = convert_numbers_to_words_wrapper(result)

        # 5. Ordinal normalization
        if self.apply_ordinal_normalization:
            result = normalize_ordinals(result)
            
        # 6. Unit abbreviation expansion
        if self.apply_unit_normalization:
            result = normalize_units(result)

        # 7. Character normalization
        if self.remove_hats:
            result = replace_hatted_characters(result)
        
        if self.lowercase:
            result = turkish_lower(result)

        # 8. Legacy normalization (more aggressive, removes punctuation)
        if self.apply_legacy_normalization:
            result = normalize_text(result)

        return result


# Create a default normalizer instance for easy import
default_normalizer = TurkishNormalizer()


def normalize(text: Union[str, List[str]], 
              apply_number_conversion: Optional[bool] = None,
              apply_ordinal_normalization: Optional[bool] = None,
              apply_symbol_conversion: Optional[bool] = None,
              apply_multiplication_symbol: Optional[bool] = None,
              apply_unit_normalization: Optional[bool] = None,
              apply_legacy_normalization: Optional[bool] = None,
              lowercase: Optional[bool] = None,
              remove_hats: Optional[bool] = None) -> Union[str, List[str]]:
    """
    Normalize Turkish text using the default normalizer.

    This is a convenience function that uses the default TurkishNormalizer instance.
    Any parameters set to None will use the default normalizer's settings.

    Args:
        text (Union[str, List[str]]): Input text or list of texts to normalize
        apply_number_conversion (Optional[bool]): Whether to convert numbers to their text representation
        apply_ordinal_normalization (Optional[bool]): Whether to normalize ordinals
        apply_symbol_conversion (Optional[bool]): Whether to convert symbols to their text representation
        apply_multiplication_symbol (Optional[bool]): Whether to replace multiplication symbol 'x' with 'çarpı'
        apply_unit_normalization (Optional[bool]): Whether to expand unit abbreviations to full text
        apply_legacy_normalization (Optional[bool]): Whether to apply legacy normalization
        lowercase (Optional[bool]): Whether to convert text to lowercase
        remove_hats (Optional[bool]): Whether to remove circumflex (hat) from Turkish characters

    Returns:
        Union[str, List[str]]: Normalized text or list of normalized texts
    """
    # Create a custom normalizer if any parameters are specified
    if any(param is not None for param in [
        apply_number_conversion, apply_ordinal_normalization, 
        apply_symbol_conversion, apply_multiplication_symbol,
        apply_unit_normalization, apply_legacy_normalization, 
        lowercase, remove_hats
    ]):
        custom_normalizer = TurkishNormalizer(
            apply_ordinal_normalization=apply_ordinal_normalization if apply_ordinal_normalization is not None else default_normalizer.apply_ordinal_normalization,
            apply_multiplication_symbol=apply_multiplication_symbol if apply_multiplication_symbol is not None else default_normalizer.apply_multiplication_symbol,
            apply_unit_normalization=apply_unit_normalization if apply_unit_normalization is not None else default_normalizer.apply_unit_normalization,
            apply_number_conversion=apply_number_conversion if apply_number_conversion is not None else default_normalizer.apply_number_conversion,
            apply_symbol_conversion=apply_symbol_conversion if apply_symbol_conversion is not None else default_normalizer.apply_symbol_conversion,
            lowercase=lowercase if lowercase is not None else default_normalizer.lowercase,
            remove_hats=remove_hats if remove_hats is not None else default_normalizer.remove_hats,
            apply_legacy_normalization=apply_legacy_normalization if apply_legacy_normalization is not None else default_normalizer.apply_legacy_normalization,

        )
        return custom_normalizer.normalize(text)
    
    # Use the default normalizer
    return default_normalizer.normalize(text)
