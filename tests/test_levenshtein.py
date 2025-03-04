"""
Test script to compare different Levenshtein distance implementations and test batch processing.
"""
import sys
import os

# Add the parent directory to the path so we can import the trnorm package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from trnorm.metrics import levenshtein_distance, normalized_levenshtein_distance

# Original implementation for comparison
def original_levenshtein(str1, str2):
    """Original matrix-based implementation"""
    # Create a matrix of size (len(str1) + 1) x (len(str2) + 1)
    matrix = [[0 for _ in range(len(str2) + 1)] for _ in range(len(str1) + 1)]

    # Initialize first row and column
    for i in range(len(str1) + 1):
        matrix[i][0] = i
    for j in range(len(str2) + 1):
        matrix[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i-1] == str2[j-1]:
                matrix[i][j] = matrix[i-1][j-1]
            else:
                matrix[i][j] = min(
                    matrix[i-1][j] + 1,    # deletion
                    matrix[i][j-1] + 1,    # insertion
                    matrix[i-1][j-1] + 1   # substitution
                )

    return matrix[len(str1)][len(str2)]


def original_normalized_levenshtein(str1, str2):
    """Original normalized implementation"""
    # Get the raw Levenshtein distance
    distance = original_levenshtein(str1, str2)

    # Normalize by the length of the longer string
    max_length = max(len(str1), len(str2))

    # Avoid division by zero
    if max_length == 0:
        return 0.0 if len(str1) == len(str2) else 1.0

    return round(distance / max_length, 3)


# Test cases for strings
string_test_cases = [
    ("kitten", "sitting"),
    ("", ""),
    ("a", ""),
    ("", "a"),
    ("same", "same"),
    ("short", "verylongstring"),
    ("sunday", "saturday"),
    ("abc", "def"),
    ("lorem ipsum", "lorem ipsum dolor sit amet"),
    ("türkçe", "turkce"),
]

# Test string implementations
print("Testing Levenshtein distance with strings...")
print("-" * 70)
print(f"{'String 1':<20} {'String 2':<20} {'Current':<10} {'Original':<10} {'Same?':<6}")
print("-" * 70)

all_string_match = True
for s1, s2 in string_test_cases:
    current = levenshtein_distance(s1, s2)
    original = original_levenshtein(s1, s2)
    match = current == original
    if not match:
        all_string_match = False
    print(f"{s1[:20]:<20} {s2[:20]:<20} {current:<10} {original:<10} {match:<6}")

print("\nTesting Normalized Levenshtein distance with strings...")
print("-" * 70)
print(f"{'String 1':<20} {'String 2':<20} {'Current':<10} {'Original':<10} {'Same?':<6}")
print("-" * 70)

all_string_norm_match = True
for s1, s2 in string_test_cases:
    current = normalized_levenshtein_distance(s1, s2)
    original = original_normalized_levenshtein(s1, s2)
    match = current == original
    if not match:
        all_string_norm_match = False
    print(f"{s1[:20]:<20} {s2[:20]:<20} {current:<10} {original:<10} {match:<6}")

# Test batch processing
print("\nTesting batch processing for Levenshtein distance...")
print("-" * 70)

# Create lists of strings for batch processing
str1_list = [pair[0] for pair in string_test_cases]
str2_list = [pair[1] for pair in string_test_cases]

# Calculate batch results
batch_results = levenshtein_distance(str1_list, str2_list)
individual_results = [levenshtein_distance(s1, s2) for s1, s2 in string_test_cases]

print("Batch processing results:")
for i, (s1, s2, result) in enumerate(zip(str1_list, str2_list, batch_results)):
    print(f"{i+1}. '{s1[:10]}' vs '{s2[:10]}': {result}")

print("\nBatch results match individual results:", batch_results == individual_results)

# Test batch processing for normalized Levenshtein distance
print("\nTesting batch processing for Normalized Levenshtein distance...")
print("-" * 70)

# Calculate batch results
batch_norm_results = normalized_levenshtein_distance(str1_list, str2_list)
individual_norm_results = [normalized_levenshtein_distance(s1, s2) for s1, s2 in string_test_cases]

print("Batch processing results:")
for i, (s1, s2, result) in enumerate(zip(str1_list, str2_list, batch_norm_results)):
    print(f"{i+1}. '{s1[:10]}' vs '{s2[:10]}': {result}")

print("\nBatch results match individual results:", batch_norm_results == individual_norm_results)

# Test error handling
print("\nTesting error handling...")
print("-" * 70)

try:
    # Test with inputs of different types
    levenshtein_distance("string", ["list"])
    print("Error: Different input types not caught!")
except TypeError as e:
    print(f"Correctly caught TypeError: {e}")

try:
    # Test with lists of different lengths
    levenshtein_distance(["a", "b"], ["c"])
    print("Error: Different length lists not caught!")
except ValueError as e:
    print(f"Correctly caught ValueError: {e}")

print("\nSummary:")
print(f"String Levenshtein implementations match: {all_string_match}")
print(f"String Normalized Levenshtein implementations match: {all_string_norm_match}")
print(f"Batch processing works correctly: {batch_results == individual_results and batch_norm_results == individual_norm_results}")
