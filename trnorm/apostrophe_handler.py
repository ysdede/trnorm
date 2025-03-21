"""
Module for handling apostrophes in Turkish text normalization.
"""

def remove_apostrophes(text):
    """
    Remove apostrophes from text while preserving word boundaries.
    This is particularly useful for Turkish suffixes that use apostrophes.
    
    Args:
        text (str): Input text with apostrophes
        
    Returns:
        str: Text with apostrophes removed
    """
    # Strip single/double quotes at the beginning and end
    text = text.strip('"').strip("'")

    # Handle apostrophes with spaces
    result = text.replace(" '", " ").replace("' ", " ")

    result = result.replace(' "', ' ').replace('" ', ' ')
    
    # Handle apostrophes without spaces (like in Turkish suffixes)
    result = result.replace("'", "")
    
    # Also handle quotes for consistency
    result = result.replace(' "', ' ').replace('" ', ' ').replace('"', '')
    
    return result
