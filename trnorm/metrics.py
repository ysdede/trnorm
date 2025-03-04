"""
Metrics module for calculating text similarity metrics.

This module provides functions to calculate:
- Word Error Rate (WER)
- Character Error Rate (CER)
- Levenshtein Distance
- Normalized Levenshtein Distance

These metrics are commonly used to evaluate the performance of ASR (Automatic Speech Recognition)
and text normalization systems.
"""
from typing import Union, List, Sequence, TypeVar, Any, overload


def _calculate_levenshtein(s1: str, s2: str) -> int:
    """
    Internal function to calculate the Levenshtein distance between two strings.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        int: The Levenshtein distance between the two strings
    """
    # If s1 is shorter than s2, swap them to optimize the algorithm
    if len(s1) < len(s2):
        return _calculate_levenshtein(s2, s1)
    
    # If s2 is empty, the distance is just the length of s1
    if len(s2) == 0:
        return len(s1)
    
    # Initialize the previous row with values 0 to len(s2)
    previous_row = range(len(s2) + 1)
    
    # For each character in s1
    for i, c1 in enumerate(s1):
        # Initialize the current row with the current position
        current_row = [i + 1]
        
        # For each character in s2
        for j, c2 in enumerate(s2):
            # Calculate costs for insertions, deletions, and substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            # If characters are the same, no substitution cost; otherwise, add 1
            substitutions = previous_row[j] + (c1 != c2)
            
            # Take the minimum cost operation
            current_row.append(min(insertions, deletions, substitutions))
        
        # Update previous row for next iteration
        previous_row = current_row
    
    # The last element of the last row contains the Levenshtein distance
    return previous_row[-1]


def levenshtein_distance(s1: Union[str, List[str]], s2: Union[str, List[str]]) -> Union[int, List[int]]:
    """
    Calculate the Levenshtein distance between two strings or two lists of strings.
    
    The Levenshtein distance is a measure of the similarity between two strings.
    It is defined as the minimum number of single-character edits (insertions,
    deletions or substitutions) required to change one string into the other.
    
    This function can process:
    - Two strings: returns a single Levenshtein distance
    - Two lists of strings: returns a list of Levenshtein distances (batch processing)
    
    Args:
        s1: First string or list of strings
        s2: Second string or list of strings
        
    Returns:
        int or List[int]: The Levenshtein distance(s) between the input(s)
        
    Raises:
        TypeError: If inputs are not of the same type (both strings or both lists)
    """
    # Check if inputs are of the same type
    if type(s1) != type(s2):
        raise TypeError("Both inputs must be of the same type (both strings or both lists)")
    
    # If inputs are lists, process them in batch mode
    if isinstance(s1, list) and isinstance(s2, list):
        # If lists are of different lengths, raise an error
        if len(s1) != len(s2):
            raise ValueError("Input lists must have the same length for batch processing")
        
        # Process each pair of strings and return a list of results
        return [_calculate_levenshtein(str(item1), str(item2)) for item1, item2 in zip(s1, s2)]
    
    # If inputs are strings, calculate the Levenshtein distance directly
    elif isinstance(s1, str) and isinstance(s2, str):
        return _calculate_levenshtein(s1, s2)
    
    # If inputs are neither strings nor lists, raise an error
    else:
        raise TypeError("Inputs must be either strings or lists of strings")


def _calculate_normalized_levenshtein(s1: str, s2: str) -> float:
    """
    Internal function to calculate the normalized Levenshtein distance between two strings.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        float: Normalized distance between 0.0 (identical) and 1.0 (completely different)
    """
    # Get the raw Levenshtein distance
    distance = _calculate_levenshtein(s1, s2)

    # Normalize by the length of the longer string
    max_length = max(len(s1), len(s2))

    # Avoid division by zero
    if max_length == 0:
        return 0.0 if len(s1) == len(s2) else 1.0

    return round(distance / max_length, 3)


def normalized_levenshtein_distance(s1: Union[str, List[str]], s2: Union[str, List[str]]) -> Union[float, List[float]]:
    """
    Calculate the normalized Levenshtein distance between two strings or two lists of strings.
    Returns a value between 0.0 (identical) and 1.0 (completely different).
    
    This function can process:
    - Two strings: returns a single normalized Levenshtein distance
    - Two lists of strings: returns a list of normalized Levenshtein distances (batch processing)

    Args:
        s1: First string or list of strings
        s2: Second string or list of strings

    Returns:
        float or List[float]: Normalized distance(s) between 0.0 (identical) and 1.0 (completely different)
        
    Raises:
        TypeError: If inputs are not of the same type (both strings or both lists)
    """
    # Check if inputs are of the same type
    if type(s1) != type(s2):
        raise TypeError("Both inputs must be of the same type (both strings or both lists)")
    
    # If inputs are lists, process them in batch mode
    if isinstance(s1, list) and isinstance(s2, list):
        # If lists are of different lengths, raise an error
        if len(s1) != len(s2):
            raise ValueError("Input lists must have the same length for batch processing")
        
        # Process each pair of strings and return a list of results
        return [_calculate_normalized_levenshtein(str(item1), str(item2)) for item1, item2 in zip(s1, s2)]
    
    # If inputs are strings, calculate the normalized Levenshtein distance directly
    elif isinstance(s1, str) and isinstance(s2, str):
        return _calculate_normalized_levenshtein(s1, s2)
    
    # If inputs are neither strings nor lists, raise an error
    else:
        raise TypeError("Inputs must be either strings or lists of strings")


def wer(reference: Union[str, List[str]], hypothesis: Union[str, List[str]]) -> Union[float, List[float]]:
    """
    Calculate the Word Error Rate (WER) between reference and hypothesis strings.
    
    WER is defined as the edit distance between the word sequences divided by
    the number of words in the reference.
    
    This function can process:
    - Two strings: returns a single WER
    - Two lists of strings: returns a list of WERs (batch processing)
    
    Args:
        reference: The reference text or list of reference texts
        hypothesis: The hypothesis text or list of hypothesis texts
        
    Returns:
        float or List[float]: The Word Error Rate(s)
        
    Raises:
        TypeError: If inputs are not of the same type (both strings or both lists)
    """
    # Check if inputs are of the same type
    if type(reference) != type(hypothesis):
        raise TypeError("Both inputs must be of the same type (both strings or both lists)")
    
    # If inputs are lists, process them in batch mode
    if isinstance(reference, list) and isinstance(hypothesis, list):
        # If lists are of different lengths, raise an error
        if len(reference) != len(hypothesis):
            raise ValueError("Input lists must have the same length for batch processing")
        
        # Process each pair of strings and return a list of results
        results = []
        for ref, hyp in zip(reference, hypothesis):
            ref_words = str(ref).split()
            hyp_words = str(hyp).split()
            
            if len(ref_words) == 0:
                results.append(1.0)
            else:
                # Calculate Levenshtein distance between word sequences and normalize by reference length
                distance = _calculate_levenshtein(ref_words, hyp_words)
                results.append(distance / len(ref_words))
        
        return results
    
    # If inputs are strings, calculate the WER directly
    elif isinstance(reference, str) and isinstance(hypothesis, str):
        ref_words = reference.split()
        hyp_words = hypothesis.split()
        
        if len(ref_words) == 0:
            return 1.0
        
        # Calculate Levenshtein distance between word sequences and normalize by reference length
        distance = _calculate_levenshtein(ref_words, hyp_words)
        return distance / len(ref_words)
    
    # If inputs are neither strings nor lists, raise an error
    else:
        raise TypeError("Inputs must be either strings or lists of strings")


def cer(reference: Union[str, List[str]], hypothesis: Union[str, List[str]]) -> Union[float, List[float]]:
    """
    Calculate the Character Error Rate (CER) between reference and hypothesis strings.
    
    CER is defined as the edit distance between the character sequences divided by
    the number of characters in the reference.
    
    Unlike normalized_levenshtein_distance which normalizes by the maximum length of both strings,
    CER normalizes by the length of the reference string only.
    
    This function can process:
    - Two strings: returns a single CER
    - Two lists of strings: returns a list of CERs (batch processing)
    
    Args:
        reference: The reference text or list of reference texts
        hypothesis: The hypothesis text or list of hypothesis texts
        
    Returns:
        float or List[float]: The Character Error Rate(s)
        
    Raises:
        TypeError: If inputs are not of the same type (both strings or both lists)
    """
    # Check if inputs are of the same type
    if type(reference) != type(hypothesis):
        raise TypeError("Both inputs must be of the same type (both strings or both lists)")
    
    # If inputs are lists, process them in batch mode
    if isinstance(reference, list) and isinstance(hypothesis, list):
        # If lists are of different lengths, raise an error
        if len(reference) != len(hypothesis):
            raise ValueError("Input lists must have the same length for batch processing")
        
        # Process each pair of strings and return a list of results
        results = []
        for ref, hyp in zip(reference, hypothesis):
            ref_str = str(ref)
            hyp_str = str(hyp)
            
            if len(ref_str) == 0:
                results.append(1.0)
            else:
                # Calculate Levenshtein distance between character sequences and normalize by reference length
                distance = _calculate_levenshtein(ref_str, hyp_str)
                results.append(distance / len(ref_str))
        
        return results
    
    # If inputs are strings, calculate the CER directly
    elif isinstance(reference, str) and isinstance(hypothesis, str):
        if len(reference) == 0:
            return 1.0
        
        # Calculate Levenshtein distance between character sequences and normalize by reference length
        distance = _calculate_levenshtein(reference, hypothesis)
        return distance / len(reference)
    
    # If inputs are neither strings nor lists, raise an error
    else:
        raise TypeError("Inputs must be either strings or lists of strings")
