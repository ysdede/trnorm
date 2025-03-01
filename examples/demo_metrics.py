#!/usr/bin/env python3
"""
Demo script for the metrics module in trnorm package.

This script demonstrates how to use the metrics module to calculate:
- Word Error Rate (WER)
- Character Error Rate (CER)
- Levenshtein Distance

These metrics are commonly used to evaluate the performance of ASR (Automatic Speech Recognition)
and text normalization systems.
"""

from trnorm.metrics import wer, cer, levenshtein_distance


def main():
    # Example 1: Basic usage
    reference = "bu bir test cümlesidir"
    hypothesis = "bu bir test cümlesi"
    
    wer_score = wer(reference, hypothesis)
    cer_score = cer(reference, hypothesis)
    lev_distance = levenshtein_distance(reference, hypothesis)
    
    print("Example 1: Basic usage")
    print(f"Reference: '{reference}'")
    print(f"Hypothesis: '{hypothesis}'")
    print(f"WER: {wer_score:.4f}")
    print(f"CER: {cer_score:.4f}")
    print(f"Levenshtein Distance: {lev_distance}")
    print()
    
    # Example 2: Word substitution
    reference = "bu bir test cümlesidir"
    hypothesis = "bu bir deneme cümlesidir"
    
    wer_score = wer(reference, hypothesis)
    cer_score = cer(reference, hypothesis)
    lev_distance = levenshtein_distance(reference.split(), hypothesis.split())
    
    print("Example 2: Word substitution")
    print(f"Reference: '{reference}'")
    print(f"Hypothesis: '{hypothesis}'")
    print(f"WER: {wer_score:.4f}")
    print(f"CER: {cer_score:.4f}")
    print(f"Levenshtein Distance (words): {lev_distance}")
    print()
    
    # Example 3: Multiple errors
    reference = "otomatik konuşma tanıma sistemleri"
    hypothesis = "otomotik konuşma tanımla sistemleri"
    
    wer_score = wer(reference, hypothesis)
    cer_score = cer(reference, hypothesis)
    
    print("Example 3: Multiple errors")
    print(f"Reference: '{reference}'")
    print(f"Hypothesis: '{hypothesis}'")
    print(f"WER: {wer_score:.4f}")
    print(f"CER: {cer_score:.4f}")
    print()
    
    # Example 4: Empty reference
    reference = ""
    hypothesis = "bu bir test"
    
    wer_score = wer(reference, hypothesis)
    cer_score = cer(reference, hypothesis)
    
    print("Example 4: Empty reference")
    print(f"Reference: '{reference}'")
    print(f"Hypothesis: '{hypothesis}'")
    print(f"WER: {wer_score:.4f}")
    print(f"CER: {cer_score:.4f}")
    print()

    # Example 5: Real-world example
    reference = "Kafkas göçmenleriyse günlük tartışmalardan uzak."
    hypothesis = "Kafkas göçmenleri ise günlük tartışmalardan uzak."
    
    wer_score = wer(reference, hypothesis)
    cer_score = cer(reference, hypothesis)

    print("Example 5: Real-world example")
    print(f"Reference: '{reference}'")
    print(f"Hypothesis: '{hypothesis}'")
    print(f"WER: {wer_score}")
    print(f"CER: {cer_score}")
    print()

if __name__ == "__main__":
    main()
