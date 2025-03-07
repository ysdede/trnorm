"""
Alphanumeric pattern handling for Turkish text normalization.

This module provides functions to handle alphanumeric patterns like "F3", "B1", etc.,
by separating the letter and number components with a space to allow for proper
text normalization in the pipeline.
"""

import re


def separate_alphanumeric(text):
    """
    Separate alphanumeric patterns (letter+number) with a space.
    
    This function identifies patterns like "F3", "B1", "A400" and inserts a space
    between the letter and number components to allow for proper text normalization
    in the pipeline.
    
    Args:
        text (str): Input text containing alphanumeric patterns.
        
    Returns:
        str: Text with alphanumeric patterns separated by a space.
    """
    # Pattern to match a letter (or sequence of letters) followed by a number
    # Handles both uppercase and lowercase letters
    pattern = r'([a-zA-Z]+)(\d+)'
    
    # Replace with the same letter followed by a space and then the number
    result = re.sub(pattern, r'\1 \2', text)
    
    return result


def normalize_alphanumeric(text, separate=True):
    """
    Normalize alphanumeric patterns in text.
    
    Args:
        text (str): Input text containing alphanumeric patterns.
        separate (bool, optional): Whether to separate alphanumeric patterns.
            Defaults to True.
            
    Returns:
        str: Normalized text.
    """
    if not separate:
        return text
    
    return separate_alphanumeric(text)
