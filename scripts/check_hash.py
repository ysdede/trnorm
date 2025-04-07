"""
Hash Checker for CSV files

This script reads a list of CSV files, checks for duplicate hashes,
and verifies if shortened hashes (first 5 + last 5 characters) would cause conflicts.
"""

import csv
import sys
import os
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple, Set


def read_csv_files(file_paths: List[Path]) -> List[dict]:
    """
    Read all CSV files and return a list of all rows.
    
    Args:
        file_paths: List of CSV file paths to read
        
    Returns:
        List of dictionaries containing all rows from all files
    """
    all_rows = []
    
    for file_path in file_paths:
        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if 'hash' in row and 'reference' in row:
                        all_rows.append(row)
                    else:
                        print(f"Warning: File {file_path} missing required 'hash' or 'reference' column")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
    
    return all_rows


def check_duplicates(rows: List[dict]) -> None:
    """
    Check for duplicate hashes in the CSV files.
    
    Args:
        rows: List of dictionaries containing CSV rows
    """
    hash_to_references = defaultdict(list)
    
    for row in rows:
        hash_value = row['hash']
        reference = row['reference']
        hash_to_references[hash_value].append(reference)
    
    expected_duplicates = 0
    unexpected_duplicates = 0
    
    for hash_value, references in hash_to_references.items():
        if len(references) > 1:
            # Check if all references are the same
            if len(set(references)) == 1:
                # All references are the same, this is expected
                expected_duplicates += 1
            else:
                # Different references with the same hash, this is unexpected
                unexpected_duplicates += 1
                print(f"Unexpected hash conflict found: {hash_value}")
                for i, ref in enumerate(references, 1):
                    print(f"  Reference {i}: {ref}")
    
    print(f"Found {expected_duplicates} expected duplicate hashes (same sentence, same hash).")
    
    if unexpected_duplicates == 0:
        print("No unexpected hash conflicts found (different sentences with same hash).")
    else:
        print(f"Found {unexpected_duplicates} unexpected hash conflicts (different sentences with same hash).")


def check_shortened_hash_conflicts(rows: List[dict], prefix_len=5, suffix_len=5) -> None:
    """
    Check if shortened hashes would cause conflicts.
    
    Args:
        rows: List of dictionaries containing CSV rows
        prefix_len: Number of characters to take from the beginning of the hash
        suffix_len: Number of characters to take from the end of the hash
    """
    # Map from shortened hash to (full hash, reference) pairs
    shortened_hash_to_data = defaultdict(list)
    
    for row in rows:
        full_hash = row['hash']
        reference = row['reference']
        shortened_hash = full_hash[:prefix_len] + full_hash[-suffix_len:]
        
        shortened_hash_to_data[shortened_hash].append((full_hash, reference))
    
    # Count conflicts
    expected_conflicts = 0
    unexpected_conflicts = 0
    
    # Track shortened hashes with conflicts for detailed reporting
    conflict_details = {}
    
    for shortened_hash, data_list in shortened_hash_to_data.items():
        if len(data_list) > 1:
            # Extract unique references
            unique_references = {ref for _, ref in data_list}
            
            if len(unique_references) == 1:
                # All references are the same, this is expected
                expected_conflicts += 1
            else:
                # Different references with the same shortened hash
                unexpected_conflicts += 1
                conflict_details[shortened_hash] = data_list
    
    print(f"Found {expected_conflicts} expected shortened hash conflicts (same sentence, different full hashes).")
    
    if unexpected_conflicts == 0:
        print("No unexpected shortened hash conflicts found (different sentences with same shortened hash).")
        print(f"✅ Using first {prefix_len} + last {suffix_len} characters is safe for shortening hashes.")
    else:
        print(f"Found {unexpected_conflicts} unexpected shortened hash conflicts (different sentences with same shortened hash):")
        print(f"❌ Using first {prefix_len} + last {suffix_len} characters is NOT safe for shortening hashes.")
        
        for shortened_hash, data_list in conflict_details.items():
            print(f"  Shortened hash conflict: {shortened_hash}")
            for i, (full_hash, reference) in enumerate(data_list, 1):
                print(f"    Full hash {i}: {full_hash}")
                print(f"    Reference {i}: {reference}")


def main():
    # Define input files
    input_root = r"C:\Drive\hf_cache\ys0_large_v3_train_full"
    input_csv_files = [
        "ys-0--openai-whisper-large-v3-turbo--20250321194154.csv",
        "ys-0--openai-whisper-large-v3-turbo--20250321193856.csv",
        "ys-0--openai-whisper-large-v3-turbo--20250321192215.csv",
    ]
    
    # Create full paths for input files
    file_paths = [Path(input_root, csv_file) for csv_file in input_csv_files]
    print(f"Reading {len(file_paths)} CSV files...")
    
    rows = read_csv_files(file_paths)
    print(f"Read {len(rows)} rows from all files.")
    
    print("\n=== Checking for Duplicate Hashes ===")
    check_duplicates(rows)
    
    print("\n=== Checking for Shortened Hash Conflicts (First 5 + Last 5) ===")
    check_shortened_hash_conflicts(rows, prefix_len=5, suffix_len=5)
    
    # Also check 4+4 for comparison
    print("\n=== Checking for Shortened Hash Conflicts (First 4 + Last 4) ===")
    check_shortened_hash_conflicts(rows, prefix_len=4, suffix_len=4)


if __name__ == "__main__":
    main()
