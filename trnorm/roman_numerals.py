"""
Module for handling Roman numerals in Turkish text normalization.

This module provides functions to convert Roman numerals to Arabic numbers
and identify Roman numerals in text.
"""

import re

# Dictionary mapping Roman numeral symbols to their values
ROMAN_VALUES = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}

# Regular expression pattern to match valid Roman numerals
# This pattern enforces standard Roman numeral rules:
# - I, X, C, M can be repeated up to 3 times
# - V, L, D cannot be repeated
# - Subtractive combinations are limited to specific pairs (IV, IX, XL, XC, CD, CM)
ROMAN_PATTERN = re.compile(r'^(?=[IVXLCDM])M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')

# Pattern to match Roman numerals followed by a period in text
# This is used to identify potential ordinal Roman numerals
ROMAN_ORDINAL_PATTERN = re.compile(r'\b([IVXLCDM]+)\.\s+([A-Za-zÇçĞğİıÖöŞşÜü]\w*)')


def is_roman_numeral(s):
    """
    Check if a string is a valid Roman numeral.
    
    Args:
        s (str): The string to check
        
    Returns:
        bool: True if the string is a valid Roman numeral, False otherwise
    """
    return bool(ROMAN_PATTERN.match(s.upper()))


def roman_to_arabic(roman):
    """
    Convert a Roman numeral to its Arabic (integer) equivalent.
    
    Args:
        roman (str): The Roman numeral to convert
        
    Returns:
        int: The Arabic number equivalent
        
    Raises:
        ValueError: If the input is not a valid Roman numeral
    """
    if not is_roman_numeral(roman):
        raise ValueError(f"Invalid Roman numeral: {roman}")
    
    roman = roman.upper()
    result = 0
    prev_value = 0
    
    # Process from right to left
    for char in reversed(roman):
        value = ROMAN_VALUES[char]
        # If the current value is less than the previous value, subtract it
        if value < prev_value:
            result -= value
        # Otherwise, add it
        else:
            result += value
        prev_value = value
    
    return result


def find_roman_ordinals(text):
    """
    Find all Roman ordinals in text (Roman numerals followed by a period).
    
    Args:
        text (str): The text to search
        
    Returns:
        list: A list of tuples containing (roman_numeral, start_position, end_position)
    """
    matches = []
    for match in ROMAN_ORDINAL_PATTERN.finditer(text):
        roman = match.group(1)
        if is_roman_numeral(roman):
            matches.append((roman, match.start(1), match.end(1)))
    return matches
