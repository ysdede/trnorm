# scripts/pick_best_scores.py

"""
Re-evaluates and filters ASR transcription results based on quality metrics.

This script reads an input CSV containing ASR 'prediction' texts and their
corresponding 'reference' ground truth. It recalculates Word Error Rate (WER)
and Character Error Rate (CER) using three different normalization strategies
from the `trnorm` library (non-context-aware, legacy, context-aware) and
determines the minimum ('best') WER and CER score for each entry.

Based on command-line specified thresholds, the script then filters these
results, retaining only those rows where EITHER the best WER is below its
threshold, OR the best CER is below its threshold, OR the pre-calculated
cosine similarity ('cosine_similarity' column from input) is above its
threshold.

The filtered subset, representing potentially higher-quality transcriptions,
is written to a new output CSV file.

Input Data Requirements:
    - CSV file format: Comma-separated, all fields quoted, UTF-8 encoding.
    - Path provided via the first command-line argument.
    - Required Input Columns:
        - 'reference': Original ground truth text.
        - 'prediction': ASR hypothesis text.
        - 'hash': Unique identifier.
        - 'cosine_similarity': Pre-calculated similarity score.

Output Data:
    - A new CSV file is created in the same directory as the input file.
    - The output filename is derived from the input filename by appending
      a suffix specified via the `--output_suffix` argument (default: '_picked').
    - The output file contains only the rows that passed the filtering criteria.
    - Output Columns:
        - "hash": Unique identifier from input.
        - "wer": The minimum WER calculated across the 3 normalization methods.
        - "cer": The minimum CER calculated across the 3 normalization methods.
        - "cosSim": Cosine similarity score from input.
        - "reference": Original reference text from input.
        - "prediction": Original ASR prediction text from input.
"""

import csv
import argparse
from pathlib import Path
from trnorm.metrics import wer as compute_wer, cer as compute_cer
from trnorm import normalize
from trnorm.legacy_normalizer import normalize_text as legacy_normalize

# Parse command line arguments
parser = argparse.ArgumentParser(description='Pick best quality rows from corrected transcription results')
parser.add_argument('input_file', type=str, help='Input CSV file path')
parser.add_argument('--wer_threshold', type=float, default=15.0, help='WER threshold for filtering (default: 15.0)')
parser.add_argument('--cer_threshold', type=float, default=20.0, help='CER threshold for filtering (default: 20.0)')
parser.add_argument('--cossim_threshold', type=float, default=97.0, help='Cosine similarity threshold for filtering (default: 97.0)')
parser.add_argument('--output_suffix', type=str, default='_picked', help='Suffix for output file (default: _picked)')
args = parser.parse_args()

# Use the provided input file
input_file = Path(args.input_file)

# Get the output directory and filename
log_root = input_file.parent
log_file = input_file.name

new_row_template = {
    'hash': None,
    'wer': None,
    'cer': None,
    'cosSim': None,
    'reference': None,
    'prediction': None,
}
# "wer","cer","levenshtein_distance","cosine_similarity","duration","inference_duration","reference","prediction","norm_reference","norm_prediction","hash"

# alternative reference inpuut
reference_column = 'reference'  # original reference
prediction_column = 'prediction'  # usual

new_rows = []
picked_rows = []
total_wer, total_cer = 0, 0
picked_total_wer, picked_total_cer = 0, 0

with open(input_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for idx, row in enumerate(reader):
        # Access columns by name, e.g., row['wer'], row['cer'], etc.
        wer_un = round(compute_wer(row[reference_column], row[prediction_column]) * 100, 2)
        cer_un = round(compute_cer(row[reference_column], row[prediction_column]) * 100, 2)

        wer_l = round(compute_wer(legacy_normalize(row[reference_column]), legacy_normalize(row[prediction_column])) * 100, 2)
        cer_l = round(compute_cer(legacy_normalize(row[reference_column]), legacy_normalize(row[prediction_column])) * 100, 2)
        
        reference_normalized = normalize(row[reference_column], context_text=row[prediction_column])
        prediction_normalized = normalize(row[prediction_column], context_text=row[reference_column])

        wer_trnorm = round(compute_wer(reference_normalized, prediction_normalized) * 100, 2)
        cer_trnorm = round(compute_cer(reference_normalized, prediction_normalized) * 100, 2)

        best_wer = min(wer_trnorm, wer_un, wer_l)
        best_cer = min(cer_trnorm, cer_un, cer_l)
        
        cos_sim = float(row['cosine_similarity'])

        print(f"Best wer: {best_wer}, best cer: {best_cer}, cos_sim: {cos_sim}, {wer_trnorm=}, {wer_un=}, {wer_l=} {'✨' if best_wer != wer_trnorm else ''}")

        new_row = new_row_template.copy()
        new_row['wer'] = best_wer
        new_row['cer'] = best_cer
        new_row['cosSim'] = cos_sim
        new_row['reference'] = row[reference_column]
        new_row['prediction'] = row[prediction_column]
        new_row['hash'] = row['hash']
        new_rows.append(new_row)

        total_wer += best_wer
        total_cer += best_cer
        
        # Check if the row meets the filtering criteria
        if best_wer < args.wer_threshold or best_cer < args.cer_threshold or cos_sim > args.cossim_threshold:
            picked_rows.append(new_row)
            picked_total_wer += best_wer
            picked_total_cer += best_cer

# Write picked rows to a new CSV file
output_file = Path(log_root, f"{log_file.split('.')[0]}{args.output_suffix}.csv")

print(f"Processed {len(new_rows)} rows")
print(f"Picked {len(picked_rows)} rows based on criteria:")
print(f"  - WER < {args.wer_threshold}")
print(f"  - CER < {args.cer_threshold}")
print(f"  - Cosine Similarity > {args.cossim_threshold}")

if picked_rows:
    print(f"Average WER of picked rows: {picked_total_wer / len(picked_rows)}")
    print(f"Average CER of picked rows: {picked_total_cer / len(picked_rows)}")
else:
    print("No rows matched the filtering criteria.")

print(f"Output file: {output_file}")

with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=new_row_template.keys())
    writer.writeheader()
    writer.writerows(picked_rows)
