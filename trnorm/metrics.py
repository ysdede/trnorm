"""
Metrics module for calculating text similarity metrics.

This module provides functions to calculate:
- Word Error Rate (WER)
- Character Error Rate (CER)
- Levenshtein Distance

These metrics are commonly used to evaluate the performance of ASR (Automatic Speech Recognition)
and text normalization systems.
"""


def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two sequences.
    
    The Levenshtein distance is a measure of the similarity between two strings.
    It is defined as the minimum number of single-character edits (insertions,
    deletions or substitutions) required to change one string into the other.
    
    Args:
        s1: First sequence (string or list)
        s2: Second sequence (string or list)
        
    Returns:
        int: The Levenshtein distance between the two sequences
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def wer(reference, hypothesis):
    """
    Calculate the Word Error Rate (WER) between reference and hypothesis strings.
    
    WER is defined as the edit distance between the word sequences divided by
    the number of words in the reference.
    
    Args:
        reference (str): The reference text
        hypothesis (str): The hypothesis text
        
    Returns:
        float: The Word Error Rate
    """
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    
    if len(ref_words) == 0:
        return 1.0
    
    return levenshtein_distance(ref_words, hyp_words) / len(ref_words)


def cer(reference, hypothesis):
    """
    Calculate the Character Error Rate (CER) between reference and hypothesis strings.
    
    CER is defined as the edit distance between the character sequences divided by
    the number of characters in the reference.
    
    Args:
        reference (str): The reference text
        hypothesis (str): The hypothesis text
        
    Returns:
        float: The Character Error Rate
    """
    if len(reference) == 0:
        return 1.0
    
    return levenshtein_distance(reference, hypothesis) / len(reference)
