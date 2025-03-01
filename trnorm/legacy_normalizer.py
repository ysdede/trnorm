"""
Legacy text normalizer for Turkish text.
This module provides backward compatibility with the previous normalizer implementation.
"""

import re

# Turkish character mappings
turkish_upper_chars = {"ı": "I", "i": "İ", "ş": "Ş", "ğ": "Ğ", "ü": "Ü", "ö": "Ö", "ç": "Ç"}
turkish_lower_chars = {v: k for k, v in turkish_upper_chars.items()}

# Turkish hatted characters mapping
turkish_hatted_chars = {
    "â": "a",
    "Â": "A",
    "î": "i",
    "Î": "I",
    "û": "u",
    "Û": "U",
    "ô": "o",
    "Ô": "O"
}

def replace_hatted_characters(s):
    """Replace Turkish characters with circumflex (hat) with their non-hatted equivalents."""
    for k, v in turkish_hatted_chars.items():
        s = s.replace(k, v)
    return s

def turkish_lower(s):
    """Convert a string to lowercase, handling Turkish-specific uppercase to lowercase mappings."""
    return "".join(turkish_lower_chars.get(c, c.lower()) for c in s)

def normalize_text(text):
    """
    Handle Turkish specific characters, use helper functions defined earlier.
    Accepts both strings and lists of strings.
    
    Args:
        text: A string or list of strings to normalize
        
    Returns:
        Normalized text with Turkish characters handled properly
    """
    if isinstance(text, list):
        return [normalize_text(item) for item in text]
    else:
        text = text.replace(" '", " ").replace("' ", " ").replace("'", "")
        text = text.replace(' "', ' ').replace('" ', ' ').replace('"', '')
        text = replace_hatted_characters(text)
        text = turkish_lower(text)
        text = re.sub(r'[^a-zçğıöşü]', ' ', text).replace("  ", " ")
        return text.strip()
