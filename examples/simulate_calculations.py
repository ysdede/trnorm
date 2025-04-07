# examples/simulate_calculations.py

"""
Recalculates ASR metrics from a log file using trnorm context-aware normalization.

This script reads a specific ASR evaluation log file (expected to be tab-separated)
containing pre-calculated metrics like Word Error Rate (WER), Levenshtein Distance,
and Similarity Score, along with reference and prediction texts.

The primary goal is to re-evaluate the reference and prediction pairs using the
`trnorm` library, specifically applying its context-aware normalization (`trnorm.normalize`)
before calculating WER, Character Error Rate (CER), and normalized Levenshtein distance
(`trnorm.metrics.wer`, `trnorm.metrics.cer`, `trnorm.metrics.normalized_levenshtein_distance`).

It compares the newly calculated WER score with the original WER score read from the
log file for each row and prints detailed information for cases where the recalculated
WER is higher than the original. Finally, it calculates and prints the average scores
for both the original metrics (read from the file) and the metrics recalculated
using `trnorm`. This helps in comparing evaluation methodologies or validating the
`trnorm` calculations against existing logs.

Input Data Requirements:
    - File path configured via `log_root` and `log_file` variables.
    - File format: Tab-separated values (TSV), UTF-8 encoding.
    - Expected columns (Header is skipped, access by hardcoded index):
        - Index 0 (`WER_IDX`): Original WER score (float).
        - Index 2 (`LEV_DIST_IDX`): Original Levenshtein distance (float).
        - Index 3 (`SIM_IDX`): Original Similarity score (float).
        - Index 6 (`REF_IDX`): Reference transcription text (string).
        - Index 7 (`PRED_IDX`): Prediction (hypothesis) text (string).
        (Note: Other columns like duration, time might exist but are not used
         for recalculation, and CER is not expected in the input).

Output:
    - Prints to standard output.
    - For rows where recalculated WER > original WER: Prints comparison details
      (Original/Recalculated scores, Raw Texts, Normalized Texts).
    - At the end: Prints summary statistics:
        - Average Original WER, Levenshtein Distance, Similarity (if found).
        - Average Recalculated WER, CER, Levenshtein Distance using `trnorm`.
"""

import csv
import sys
from pathlib import Path
from trnorm.metrics import (
    wer,
    cer,
    normalized_levenshtein_distance
)
from trnorm import normalize

log_root = r"C:\Drive\hf_cache"
log_file = r"ymoslem-MediaSpeech-deepdml-faster-whisper-large-v3-turbo-ct2.tsv"
input_file = Path(log_root, log_file)

# Initialize counters
total_wer = 0
total_lev_dist = 0
total_sim = 0
count = 0

our_total_wer = 0
our_total_cer = 0
our_total_lev_dist = 0

# wer	lev_dist	sim	dur	time	r	p
# Hardcoded field indices for reliability
# These are the standard positions in our TSV files
WER_IDX = 0      # WER score
CER_IDX = 1     # CER score (not available)
LEV_DIST_IDX = 2 # Levenshtein distance
SIM_IDX = 3      # Similarity score
DUR_IDX = 4      # Duration
TIME_IDX = 5     # Time
REF_IDX = 6      # Reference text
PRED_IDX = 7     # Prediction text

try:
    with open(input_file, "r", encoding="utf-8") as f:
        # Skip header line
        next(f)
        
        # Process each line
        for line_num, line in enumerate(f, 1):
            try:
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Split by tab
                row = line.strip().split('\t')
                
                # Check if we have enough fields for reference and prediction
                if len(row) <= max(REF_IDX, PRED_IDX):
                    print(f"Warning: Line {line_num} has insufficient fields. Skipping.")
                    continue
                
                # Extract reference and prediction
                ref_text = row[REF_IDX]
                pred_text = row[PRED_IDX]
                
                # Extract other metrics if available
                row_data = {
                    'r': ref_text,
                    'p': pred_text
                }
                
                # Try to get WER if available
                if WER_IDX >= 0 and len(row) > WER_IDX:
                    try:
                        row_data['wer'] = float(row[WER_IDX])
                        total_wer += row_data['wer']
                    except (ValueError, TypeError):
                        row_data['wer'] = None
                
                # Try to get Levenshtein distance if available
                if LEV_DIST_IDX >= 0 and len(row) > LEV_DIST_IDX:
                    try:
                        row_data['lev_dist'] = float(row[LEV_DIST_IDX])
                        total_lev_dist += row_data['lev_dist']
                    except (ValueError, TypeError):
                        row_data['lev_dist'] = None
                
                # Try to get similarity score if available
                if SIM_IDX >= 0 and len(row) > SIM_IDX:
                    try:
                        row_data['sim'] = float(row[SIM_IDX])
                        total_sim += row_data['sim']
                    except (ValueError, TypeError):
                        row_data['sim'] = None
                
                count += 1
                
                # Use context-aware normalization for better WER/CER calculations
                normalized_ref = normalize(ref_text, context_text=pred_text)
                normalized_hyp = normalize(pred_text, context_text=ref_text)
                
                our_wer_score = wer(normalized_ref, normalized_hyp)
                our_cer_score = cer(normalized_ref, normalized_hyp)
                our_lev_dist_score = normalized_levenshtein_distance(normalized_ref, normalized_hyp)
                
                our_total_wer += our_wer_score
                our_total_cer += our_cer_score
                our_total_lev_dist += our_lev_dist_score
                
                # Print cases where our WER is higher than the original
                if 'wer' in row_data and row_data['wer'] is not None and round(our_wer_score * 100, 2) > row_data['wer']:
                    print(f"{our_wer_score * 100:.2f}/{row_data['wer']:.2f} - {our_lev_dist_score:.3f}/{row_data.get('lev_dist', 'N/A')}")
                    print(f"Reference: {ref_text}")
                    print(f"Prediction: {pred_text}")
                    print(f"Normalized Reference: {normalized_ref}")
                    print(f"Normalized Hypothesis: {normalized_hyp}")
                    print("*" * 50)
                
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
                continue
    
    # Print summary statistics
    if count > 0:
        # Original metrics (if available)
        if total_wer > 0:
            average_wer = round((total_wer / count), 2)
            print(f"Original Average WER: {average_wer}%")
        
        if total_lev_dist > 0:
            average_lev_dist = round(total_lev_dist / count, 2)
            print(f"Original Average Levenshtein Distance: {average_lev_dist}")
        
        if total_sim > 0:
            average_sim = round(total_sim / count, 2)
            print(f"Original Average Similarity: {average_sim}")
        
        print(f"Processed {count} valid rows")
        print("=" * 50)
        
        # Our metrics
        our_average_wer = round((our_total_wer / count) * 100, 2)
        our_average_cer = round((our_total_cer / count) * 100, 2)
        our_average_lev_dist = round(our_total_lev_dist / count, 3)
        
        print(f"Our WER: {our_average_wer}%")
        print(f"Our CER: {our_average_cer}%")
        print(f"Our Levenshtein Distance: {our_average_lev_dist}")
    else:
        print("No valid rows processed.")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
