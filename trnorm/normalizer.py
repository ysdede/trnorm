"""
Turkish Text Normalizer

This module provides a simple normalizer that applies a list of conversion functions
to Turkish text in sequence.
"""

from typing import List, Union, Callable, Optional, Any, Tuple

# Import all the functions needed for the default pipeline
from .dimension_utils import preprocess_dimensions, normalize_dimensions
from .unit_utils import normalize_units
from .num_to_text import convert_numbers_to_words_wrapper
from .ordinals import normalize_ordinals
from .symbols import convert_symbols
from .apostrophe_handler import remove_apostrophes
from .text_utils import turkish_lower, sapkasiz, remove_punctuation
from .time_utils import normalize_times
from .suffix_handler import merge_suffixes, context_aware_merge_suffixes
from .alphanumeric import normalize_alphanumeric

# Type definition for a conversion function
ConversionFunc = Callable[[str, Optional[Any]], str]

# Define the default pipeline
DEFAULT_PIPELINE = [
    normalize_times,
    normalize_alphanumeric,  # Add alphanumeric handling to separate patterns like F3, B1
    normalize_ordinals,
    convert_symbols,
    convert_numbers_to_words_wrapper,
    # merge_suffixes,
    context_aware_merge_suffixes,  # Use context-aware version instead of regular merge_suffixes
    remove_apostrophes,
    sapkasiz,
    preprocess_dimensions,
    normalize_dimensions,  # adds "çarpı" as a replacement to "x"
    normalize_units,       # converts units like "cm" to "santimetre", "kg" to "kilogram", etc.
    turkish_lower,
    sapkasiz,
    remove_punctuation     # Remove punctuation marks
]

def normalize(text: Union[str, List[str]], converters: Optional[List[ConversionFunc]] = None, 
              context_text: Optional[Union[str, List[str]]] = None) -> Union[str, List[str]]:
    """
    Normalize Turkish text using a list of conversion functions.
    
    This function applies the specified conversion functions to the input text in sequence.
    If no converters are specified, the DEFAULT_PIPELINE is used.
    
    Args:
        text (Union[str, List[str]]): Input text or list of texts to normalize
        converters (Optional[List[ConversionFunc]]): List of conversion functions to apply.
            If None, the DEFAULT_PIPELINE is used.
        context_text (Optional[Union[str, List[str]]]): Optional secondary text to provide context
            for context-aware converters (e.g., reference text when normalizing hypothesis)
            
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
        
        >>> # Using context-aware normalization for reference and hypothesis
        >>> ref = "Toros ile gitti"
        >>> hyp = "Toros ile geldi"
        >>> normalize(ref)  # Without context: "torosla gitti"
        >>> normalize(hyp)  # Without context: "torosla geldi"
        >>> # With context - may preserve "ile" if both have the same pattern
        >>> normalize(ref, context_text=hyp)  # With context: "toros ile gitti"
        >>> normalize(hyp, context_text=ref)  # With context: "toros ile geldi"
    """
    # Handle list input
    if isinstance(text, list):
        if context_text is not None and isinstance(context_text, list):
            # If both are lists, normalize each pair
            if len(text) == len(context_text):
                return [normalize(item, converters, ctx) 
                        for item, ctx in zip(text, context_text)]
            else:
                # If lengths don't match, ignore context
                return [normalize(item, converters) for item in text]
        else:
            # If only text is a list, normalize each item with the same context
            return [normalize(item, converters, context_text) for item in text]
    
    # If no converters are provided, use the default pipeline
    if converters is None:
        converters = DEFAULT_PIPELINE
    
    # Apply converters in sequence
    result = text
    for converter in converters:
        try:
            # Try to pass the context_text parameter if the converter supports it
            result = converter(result, context_text)
        except TypeError:
            # If the converter doesn't accept a second parameter, call it with just the text
            result = converter(result)
    
    return result
