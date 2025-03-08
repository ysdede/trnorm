"""
We have the following ASR log:
tab seperated csv file with cols:
wer: WER metric
lev_dist: Levenshtein distance
sim: similarity score
r: reference text
p: prediction text
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
log_file = r"ysdede-khanacademy-turkish-ysdede-whisper-khanacademy-large-v3-turbo-tr.tsv"
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
CER_IDX = -1     # CER score (not available)
LEV_DIST_IDX = 1 # Levenshtein distance
SIM_IDX = 2      # Similarity score
DUR_IDX = 3      # Duration
TIME_IDX = 4     # Time
REF_IDX = 5      # Reference text
PRED_IDX = 6     # Prediction text

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
            average_wer = round((total_wer / count) * 100, 2)
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
