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

# Pattern to match Roman numerals using only I, V, X (up to 39) followed by a period in text
# This is used to identify potential ordinal Roman numerals
# Limited to common use cases in Turkish text (typically up to 39/XXXIX)
# This prevents incorrect conversion of initials like "D." in names like "Mehmet D."
ROMAN_ORDINAL_PATTERN = re.compile(r'\b([IVX]+)\.\s+([A-Za-zÇçĞğİıÖöŞşÜü]\w*)')


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
        int: The Arabic numeral equivalent
        
    Raises:
        ValueError: If the input is not a valid Roman numeral
    """
    if not is_roman_numeral(roman):
        raise ValueError(f"Invalid Roman numeral: {roman}")
    
    result = 0
    prev_value = 0
    
    # Process the Roman numeral from right to left
    for char in reversed(roman.upper()):
        value = ROMAN_VALUES[char]
        
        # If the current value is less than the previous value,
        # it's a subtractive combination (like IV for 4)
        if value < prev_value:
            result -= value
        else:
            result += value
        
        prev_value = value
    
    return result


def find_roman_ordinals(text):
    """
    Find all Roman ordinals in a text.
    
    Args:
        text (str): The text to search for Roman ordinals
        
    Returns:
        list: A list of tuples containing (roman_numeral, word, position)
    """
    results = []
    for match in ROMAN_ORDINAL_PATTERN.finditer(text):
        roman = match.group(1)
        word = match.group(2)
        position = match.start()
        results.append((roman, word, position))
    
    return results
