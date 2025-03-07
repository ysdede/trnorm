"""
Turkish Text Normalizer

This module provides a simple normalizer that applies a list of conversion functions
to Turkish text in sequence.
"""

from typing import List, Union, Callable, Optional

# Import all the functions needed for the default pipeline
from .dimension_utils import preprocess_dimensions, normalize_dimensions
from .unit_utils import normalize_units
from .num_to_text import convert_numbers_to_words_wrapper
from .ordinals import normalize_ordinals
from .symbols import convert_symbols
from .apostrophe_handler import remove_apostrophes
from .text_utils import turkish_lower, sapkasiz, remove_punctuation
from .time_utils import normalize_times
from .suffix_handler import merge_suffixes
from .alphanumeric import normalize_alphanumeric

# Type definition for a conversion function
ConversionFunc = Callable[[str], str]

# Define the default pipeline
DEFAULT_PIPELINE = [
    normalize_times,
    normalize_alphanumeric,  # Add alphanumeric handling to separate patterns like F3, B1
    normalize_ordinals,
    convert_symbols,
    convert_numbers_to_words_wrapper,
    merge_suffixes,         # Add suffix handler to merge Turkish suffixes
    remove_apostrophes,
    sapkasiz,
    preprocess_dimensions,
    normalize_dimensions,  # adds "çarpı" as a replacement to "x"
    normalize_units,       # converts units like "cm" to "santimetre", "kg" to "kilogram", etc.
    turkish_lower,
    sapkasiz,
    remove_punctuation     # Remove punctuation marks
]

def normalize(text: Union[str, List[str]], converters: Optional[List[ConversionFunc]] = None) -> Union[str, List[str]]:
    """
    Normalize Turkish text using a list of conversion functions.
    
    This function applies the specified conversion functions to the input text in sequence.
    If no converters are specified, the DEFAULT_PIPELINE is used.
    
    Args:
        text (Union[str, List[str]]): Input text or list of texts to normalize
        converters (Optional[List[ConversionFunc]]): List of conversion functions to apply.
            If None, the DEFAULT_PIPELINE is used.
            
    Returns:
        Union[str, List[str]]: Normalized text or list of normalized texts
        
    Examples:
        >>> from trnorm import normalize
        >>> # Using the default pipeline
        >>> normalize("Bugün 15 kişi geldi.")
        "bugün on beş kişi geldi"
        
        >>> # Using a custom pipeline
        >>> from trnorm.num_to_text import convert_numbers_to_words_wrapper
        >>> from trnorm.text_utils import turkish_lower
        >>> normalize("Bugün 15 kişi geldi.", [convert_numbers_to_words_wrapper, turkish_lower])
        "bugün on beş kişi geldi"
    """
    # Handle list input
    if isinstance(text, list):
        return [normalize(item, converters) for item in text]
    
    # If no converters are provided, use the default pipeline
    if converters is None:
        converters = DEFAULT_PIPELINE
    
    # Apply converters in sequence
    result = text
    for converter in converters:
        result = converter(result)
    
    return result
