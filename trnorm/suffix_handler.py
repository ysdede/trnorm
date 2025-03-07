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
from typing import Union, List, Optional, Dict

from trnorm.text_utils import ekle, turkish_lower


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


def context_aware_merge_suffixes(text: Union[str, List[str]], 
                                context_text: Optional[Union[str, List[str]]] = None) -> Union[str, List[str]]:
    """
    Context-aware version of merge_suffixes that compares suffixes in both texts.
    
    This function identifies the Turkish suffixes "ile", "ise", and "iken" in text
    and merges them with their preceding words according to Turkish grammar rules.
    If context_text is provided, it will skip merging suffixes if both texts have
    the same pattern of suffixes (same number and type).
    
    Args:
        text (Union[str, List[str]]): A string or list of strings to process
        context_text (Optional[Union[str, List[str]]]): Optional secondary text to compare
            suffix patterns with (e.g., reference text when normalizing hypothesis)
        
    Returns:
        Union[str, List[str]]: The processed text with suffixes merged (or preserved if matching context)
    """
    # Handle list input recursively
    if isinstance(text, list):
        if context_text is not None and isinstance(context_text, list):
            # If both are lists, process each pair
            if len(text) == len(context_text):
                return [context_aware_merge_suffixes(item, ctx) 
                        for item, ctx in zip(text, context_text)]
            else:
                # If lengths don't match, ignore context
                return [context_aware_merge_suffixes(item) for item in text]
        else:
            # If only text is a list, process each item with the same context
            return [context_aware_merge_suffixes(item, context_text) for item in text]
    
    # If no context is provided, fall back to regular merge_suffixes
    if context_text is None:
        return merge_suffixes(text)
    
    # Count suffixes in both texts
    text_suffixes = _count_suffixes(text)
    context_suffixes = _count_suffixes(context_text)
    
    # Compare suffix patterns
    if _suffixes_match(text_suffixes, context_suffixes):
        # If patterns match, preserve suffixes (don't merge)
        return text
    else:
        # If patterns don't match, proceed with regular merging
        return merge_suffixes(text)


def _count_suffixes(text: str) -> Dict[str, int]:
    """
    Count occurrences of each suffix type in the text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        Dict[str, int]: Dictionary with suffix types as keys and counts as values
    """
    suffixes = {"ile": 0, "ise": 0, "iken": 0}
    
    # Convert to lowercase using turkish_lower for proper handling of Turkish characters
    text = turkish_lower(text)
    
    # Split by whitespace and common punctuation
    # This regex splits on spaces, commas, semicolons, question marks, etc.
    words = re.split(r'[\s,.;:?!]+', text)
    
    # Filter out empty strings that might result from the split
    words = [word for word in words if word]
    
    for suffix in suffixes:
        suffixes[suffix] = words.count(suffix)
    
    return suffixes


def _suffixes_match(suffixes1: Dict[str, int], suffixes2: Dict[str, int]) -> bool:
    """
    Check if two suffix count dictionaries match.
    
    Args:
        suffixes1 (Dict[str, int]): First suffix count dictionary
        suffixes2 (Dict[str, int]): Second suffix count dictionary
        
    Returns:
        bool: True if both dictionaries have the same counts for all suffixes
    """
    for suffix, count in suffixes1.items():
        if count != suffixes2.get(suffix, 0):
            return False
    return True


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
