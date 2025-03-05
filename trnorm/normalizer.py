"""
Turkish Text Normalizer

This module provides a simple normalizer that applies a list of conversion functions
to Turkish text in sequence.
"""

from typing import List, Union, Callable, Optional

# Type definition for a conversion function
ConversionFunc = Callable[[str], str]

def normalize(text: Union[str, List[str]], converters: Optional[List[ConversionFunc]] = None) -> Union[str, List[str]]:
    """
    Normalize Turkish text using a list of conversion functions.
    
    This function applies the specified conversion functions to the input text in sequence.
    If no converters are specified, an empty list is used (no conversion).
    
    Args:
        text (Union[str, List[str]]): Input text or list of texts to normalize
        converters (Optional[List[ConversionFunc]]): List of conversion functions to apply.
            If None, no conversion is applied.
            
    Returns:
        Union[str, List[str]]: Normalized text or list of normalized texts
        
    Examples:
        >>> from trnorm.num_to_text import convert_numbers_to_words_wrapper
        >>> from trnorm.legacy_normalizer import turkish_lower
        >>> normalize("Bugün 15 kişi geldi.", [convert_numbers_to_words_wrapper, turkish_lower])
        "bugün on beş kişi geldi."
    """
    # Handle list input
    if isinstance(text, list):
        return [normalize(item, converters) for item in text]
    
    # If no converters are provided, return the text as is
    if not converters:
        return text
    
    # Apply converters in sequence
    result = text
    for converter in converters:
        result = converter(result)
    
    return result
