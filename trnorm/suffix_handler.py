"""
This module provides functionality for handling Turkish suffixes in text.

It can identify and process the following Turkish suffixes:
- "ile" (with): Changes based on vowel harmony and whether the word ends with a vowel
- "ise" (if): Changes based on vowel harmony and whether the word ends with a vowel
- "iken" (while/when): Changes based on whether the word ends with a vowel

The module can process a single string or a list of strings, identifying and
merging these suffixes with their preceding words according to Turkish grammar rules.

Examples:
- "Toros ile hamile" -> "Torosla hamile"
- "Hayat sana limon verdi ise limonata yap" -> "Hayat sana limon verdiyse limonata yap"
- "Hâl böyle iken böyle dedi adam." -> "Hâl böyleyken böyle dedi adam."
"""

import re
from typing import Union, List

from trnorm.text_utils import ekle


def merge_suffixes(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Process Turkish suffixes in text, merging them with their preceding words.
    
    This function identifies the Turkish suffixes "ile", "ise", and "iken" in text
    and merges them with their preceding words according to Turkish grammar rules.
    
    Args:
        text (Union[str, List[str]]): A string or list of strings to process
        
    Returns:
        Union[str, List[str]]: The processed text with suffixes merged
    """
    # Handle list input recursively
    if isinstance(text, list):
        return [merge_suffixes(item) for item in text]
    
    # Process each suffix type
    text = _process_suffix(text, "ile")
    text = _process_suffix(text, "ise")
    text = _process_suffix(text, "iken")
    
    return text


def _process_suffix(text: str, suffix: str) -> str:
    """
    Process a specific Turkish suffix in text.
    
    Args:
        text (str): The text to process
        suffix (str): The suffix to process ("ile", "ise", or "iken")
        
    Returns:
        str: The processed text with the specified suffix merged
    """
    # Split text into words
    words = text.split()
    
    # Find all occurrences of the suffix
    suffix_indices = [i for i, word in enumerate(words) if word.lower() == suffix]
    
    # Process each suffix occurrence
    for idx in reversed(suffix_indices):  # Process in reverse to avoid index shifting
        # Skip if suffix is at the beginning of text (no preceding word)
        if idx == 0:
            continue
        
        # Get the word before the suffix
        preceding_word = words[idx - 1]
        
        # Merge the suffix with the preceding word
        merged_word = ekle(preceding_word, suffix)
        
        # Replace the original word and suffix with the merged word
        words[idx - 1] = merged_word
        words.pop(idx)
    
    # Join words back into text
    return " ".join(words)
