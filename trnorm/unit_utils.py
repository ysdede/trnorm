"""
Utilities for handling unit abbreviations in Turkish text.

This module provides functions to convert unit abbreviations to their full text
representations in Turkish.
"""

import re

# TODO: 16.yy'da 

# Dictionary of unit translations
unit_translations = {
    "cc": "santilitre",
    "mm": "milimetre",
    "cm": "santimetre",
    "dm": "desimetre",
    "m": "metre",
    "km": "kilometre",
    "g": "gram",
    "kg": "kilogram",
    "ml": "mililitre",
    "in": "inç",
    "ft": "feet",
    "yd": "yard",
    "mg": "miligram",
    "oz": "ons",
    "lb": "pound",
    "st": "stone",
    "l": "litre",
    "dl": "desilitre",
    "cl": "santilitre",
    "gal": "galon",
    "pt": "pint",
    "fl oz": "sıvı ons",
    "sq mm": "milimetre kare",
    "sq cm": "santimetre kare",
    "sq m": "metre kare",
    "acre": "akre",
    "hectare": "hektar",
    "j": "jul",
    "kj": "kilojul",
    "cal": "kalori",
    "kcal": "kilokalori",
    "wh": "watt saat",
    "kwh": "kilowatt saat",
    "°": "derece",
    "°c": "santigrat derece",
    "°C": "santigrat derece",
    "c°": "santigrat derece",
    "C°": "santigrat derece",
    "°f": "derece fahrenheit",
    "k": "kelvin",
    "mph": "mil/saat",
    "km/h": "kilometre/saat",
    "km/s": "kilometre/saat",
    "km": "kilometre",
    "knot": "düğüm",
    "pa": "paskal",
    "kpa": "kilopaskal",
    "mpa": "megapaskal",
    "bar": "bar",
    "psi": "pound/inç kare",
    "mm3": "milimetre küp",
    "µm": "mikrometre",
    "mmHg": "milimetre civa"
}

def normalize_units(text):
    """
    Normalize unit abbreviations in text to their full text representations.
    
    This function replaces unit abbreviations (e.g., 'cm', 'kg') with their
    full text representations in Turkish (e.g., 'santimetre', 'kilogram').
    It handles both cases where units are preceded by a space (e.g., '5 cm')
    and where units are directly attached to numbers (e.g., '5cm').
    
    Note about periods: When a unit has a period at the end (e.g., 'kg.'), 
    the period is preserved in the output. This is because the period might be 
    a sentence-ending period rather than part of the abbreviation. Punctuation 
    handling is typically done in a separate normalization step.
    
    Args:
        text (str): The input text containing unit abbreviations
        
    Returns:
        str: The text with unit abbreviations replaced by their full text representations
    """
    # Create a regex pattern for all unit abbreviations
    # Sort by length (longest first) to avoid partial matches
    sorted_units = sorted(unit_translations.keys(), key=len, reverse=True)
    unit_pattern = '|'.join([re.escape(unit) for unit in sorted_units])
    
    # Pattern for units with or without spaces before them, and with or without periods after them
    # Group 1: Space or digit before the unit
    # Group 2: The unit itself
    # Group 3: Period (optional) followed by word boundary
    pattern = r'((?:\s+)|(?<=\d))(' + unit_pattern + r')(\.?)(\b)'
    
    def replace_unit(match):
        prefix = match.group(1)
        unit = match.group(2)
        has_period = match.group(3) == '.'
        suffix = match.group(4)
        
        # If the unit is in the dictionary, replace it with its full text representation
        if unit in unit_translations:
            # Add a space if the unit was directly attached to a number
            if prefix.strip() == '':
                prefix = ' '
            
            # Preserve the period in the replacement
            period = '.' if has_period else ''
            return prefix + unit_translations[unit] + period + suffix
        
        return match.group(0)
    
    # Apply the replacement
    return re.sub(pattern, replace_unit, text)
