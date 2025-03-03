"""
Utilities for handling dimensions and multiplication symbols in Turkish text.

This module provides functions to handle dimensions and multiplication symbols
in Turkish text, particularly for ASR normalization.
"""

import re
from trnorm.unit_utils import unit_translations

def preprocess_dimensions(text):
    """
    Preprocess text to add spaces between numbers and multiplication symbols.
    
    This function detects numbers and multiplication symbols that are merged together
    and adds spaces between them to ensure proper normalization.
    
    Args:
        text (str): The input text containing potentially merged dimensions
        
    Returns:
        str: Text with spaces added between numbers and multiplication symbols
    """
    processed_text = text
    
    # Add spaces between numbers and 'x' (for dimensions like 2x3)
    processed_text = re.sub(r'(\d+)([xX])(\d+)', r'\1 \2 \3', processed_text)
    
    # Add spaces between numbers and units
    # Create a pattern that matches any unit (with optional period)
    unit_pattern = '|'.join([re.escape(unit) + r'\.?' for unit in unit_translations.keys()])
    processed_text = re.sub(r'(\d+)(' + unit_pattern + r')', r'\1 \2', processed_text)
    
    # Handle multi-dimensional cases (like 2x3x4)
    # Apply the pattern repeatedly until no more changes
    previous_text = ""
    while previous_text != processed_text:
        previous_text = processed_text
        processed_text = re.sub(r'(\d+)([xX])(\d+)', r'\1 \2 \3', processed_text)
    
    return processed_text


def normalize_dimensions(text):
    """
    Normalize dimensions in text by replacing multiplication symbols with 'çarpı'.
    
    This function handles various dimension formats including multiple dimensions
    like 2x5x6x3 and dimensions with units like 3x4cm.
    
    Args:
        text (str): The input text containing dimensional expressions
        
    Returns:
        str: The text with multiplication symbols replaced by 'çarpı'
    """
    # First, preprocess to ensure spaces between numbers and 'x'
    text = preprocess_dimensions(text)
    
    # Replace 'x' with 'çarpı' when it's between numbers (dimensions)
    pattern = r'(\d+(?:\.\d+)?(?:\s*(?:' + '|'.join([re.escape(unit) for unit in unit_translations.keys()]) + r'))?)\s+([xX])\s+(\d+(?:\.\d+)?)'
    
    # Replace all occurrences of the pattern
    while re.search(pattern, text):
        def replacement(match):
            """Replace 'x' with 'çarpı' between numbers."""
            num1, x_symbol, num2 = match.groups()
            return f"{num1.strip()} çarpı {num2.strip()}"
        
        # Replace one occurrence at a time to handle chains like 2 x 3 x 4
        text = re.sub(pattern, replacement, text, count=1)
    
    # Clean up any double spaces
    return re.sub(r'\s+', ' ', text).strip()
