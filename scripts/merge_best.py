# scripts/merge_best.py
"""
Merges ASR results from multiple files, selecting the best entry per hash.

This script processes multiple CSV files containing Automatic Speech Recognition (ASR)
results. For each unique audio segment identifier ('hash'), it identifies the
entry (across all provided input files) that yields the lowest Word Error Rate (WER).

The WER used for comparison is the minimum value obtained from three different
calculations for each row:
1.  The pre-calculated WER from the input file (assumed to be context-aware trnorm).
2.  A recalculated WER using non-context-aware trnorm normalization.
3.  A recalculated WER using legacy trnorm normalization.

The script outputs a single consolidated CSV file containing only the best-performing
row for each unique hash, along with detailed metrics from that specific row
(including all three calculated/read WER/CER types) and the name of the source
file from which the best row was selected.

Input Data Requirements:
    - Multiple CSV files specified in the `log_files` list within the script.
    - Files located in the directory specified by `log_root`.
    - CSV format: Comma-separated, all fields quoted, UTF-8 encoding.
    - Required Input Columns per file:
        - "hash": Unique identifier for the audio segment.
        - "reference": Ground truth reference text.
        - "prediction": ASR hypothesis text.
        - "wer": Pre-calculated WER (assumed context-aware trnorm).
        - "cer": Pre-calculated CER (assumed context-aware trnorm).
        - "cosine_similarity": Pre-calculated similarity score.

Output Data:
    - A single CSV file named "merged_best_results.csv" located in `log_root`.
    - Contains one row per unique 'hash' found across all input files.
    - Each output row corresponds to the input row (from any file) that had the
      minimum WER ('best_wer') for that specific 'hash'.
    - Output Columns:
        - "hash": Unique identifier.
        - "wer": The minimum WER found for this hash (min of 3 methods).
        - "cer": The minimum CER found for this hash (min of 3 methods).
        - "cosSim": Cosine similarity from the selected best row.
        - "reference": Reference text from the selected best row.
        - "prediction": Prediction text from the selected best row.
        - "source_file": Filename of the input CSV containing the selected row.
        - "wer_un": Recalculated non-context-aware WER for the selected row.
        - "cer_un": Recalculated non-context-aware CER for the selected row.
        - "wer_l": Recalculated legacy WER for the selected row.
        - "cer_l": Recalculated legacy CER for the selected row.
        - "wer_trnorm": Original context-aware WER (from input) for the selected row.
        - "cer_trnorm": Original context-aware CER (from input) for the selected row.
"""

import csv
from pathlib import Path
from trnorm.metrics import wer as compute_wer, cer as compute_cer
from trnorm import normalize
from trnorm.legacy_normalizer import normalize_text as legacy_normalize

log_root = r"C:\Drive\hf_cache\relabel\khan"
log_files = [
    r"khanacademy-turkish--whisper-khanacademy-large-v3-turbo-tr-ct2--20250324134119.csv",
    r"khanacademy-turkish--ysdede-whisper-small-turkish-0--20250323154608.csv",
]  # predictions and scores files created by various asr models

input_files = [Path(log_root, log_file) for log_file in log_files]

new_row_template = {
    "hash": None,
    "wer": None,
    "cer": None,
    "cosSim": None,
    "reference": None,
    "prediction": None,
    "source_file": None,  # Added to track which file the row came from
    "wer_un": None,       # Added to store unnormalized WER
    "cer_un": None,       # Added to store unnormalized CER
    "wer_l": None,        # Added to store legacy normalized WER
    "cer_l": None,        # Added to store legacy normalized CER
    "wer_trnorm": None,   # Added to store trnorm normalized WER
    "cer_trnorm": None,   # Added to store trnorm normalized CER
}

# alternative reference input
reference_column = "reference"  # alternative reference
prediction_column = "prediction"  # usual

# Dictionary to store the best row for each hash
best_rows_by_hash = {}

# Process all input files
for input_file in input_files:
    print(f"Processing file: {input_file}")
    with open(input_file, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            # Skip if required columns are missing
            if not all(col in row for col in ["hash", "cosine_similarity", "wer", "cer", reference_column, prediction_column]):
                print(f"Skipping row {idx} in {input_file.name}: Missing required columns")
                continue
                
            # Calculate unnormalized and legacy metrics
            wer_un = round(
                compute_wer(row[reference_column], row[prediction_column]) * 100, 2
            )
            cer_un = round(
                compute_cer(row[reference_column], row[prediction_column]) * 100, 2
            )

            wer_l = round(
                compute_wer(
                    legacy_normalize(row[reference_column]),
                    legacy_normalize(row[prediction_column]),
                )
                * 100,
                2,
            )
            cer_l = round(
                compute_cer(
                    legacy_normalize(row[reference_column]),
                    legacy_normalize(row[prediction_column]),
                )
                * 100,
                2,
            )

            # Use existing trnorm WER and CER values from input file
            wer_trnorm = float(row["wer"])
            cer_trnorm = float(row["cer"])

            best_wer = min(wer_trnorm, wer_un, wer_l)
            best_cer = min(cer_trnorm, cer_un, cer_l)

            # Create a new row with all the calculated metrics
            new_row = new_row_template.copy()
            new_row["hash"] = row["hash"]
            new_row["wer"] = best_wer
            new_row["cer"] = best_cer
            new_row["cosSim"] = float(row["cosine_similarity"])
            new_row["reference"] = row[reference_column]
            new_row["prediction"] = row[prediction_column]
            new_row["source_file"] = input_file.name
            new_row["wer_un"] = wer_un
            new_row["cer_un"] = cer_un
            new_row["wer_l"] = wer_l
            new_row["cer_l"] = cer_l
            new_row["wer_trnorm"] = wer_trnorm
            new_row["cer_trnorm"] = cer_trnorm

            # Check if we already have a row with this hash
            if row["hash"] in best_rows_by_hash:
                # If the current row has a lower WER, replace the existing one
                if best_wer < best_rows_by_hash[row["hash"]]["wer"]:
                    print(f"Found better WER for hash {row['hash']}: {best_wer} vs {best_rows_by_hash[row['hash']]['wer']} (from {input_file.name})")
                    best_rows_by_hash[row["hash"]] = new_row
            else:
                # If this is the first time we see this hash, add it
                best_rows_by_hash[row["hash"]] = new_row

# Convert the dictionary to a list for output
new_rows = list(best_rows_by_hash.values())

# Calculate statistics
total_wer = sum(row["wer"] for row in new_rows)
total_cer = sum(row["cer"] for row in new_rows)

# Write the new rows to a new CSV file
output_file = Path(log_root, f"merged_best_results.csv")

print(f"Processed {len(new_rows)} unique rows from {len(input_files)} files")
print(f"Average WER: {total_wer / len(new_rows):.2f}")
print(f"Average CER: {total_cer / len(new_rows):.2f}")
print(f"Output file: {output_file}")

# Get file statistics
file_counts = {}
for row in new_rows:
    source_file = row["source_file"]
    if source_file in file_counts:
        file_counts[source_file] += 1
    else:
        file_counts[source_file] = 1

print("\nRows selected from each file:")
for file_name, count in file_counts.items():
    print(f"  {file_name}: {count} rows ({count/len(new_rows)*100:.1f}%)")

with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=new_row_template.keys())
    writer.writeheader()
    writer.writerows(new_rows)
