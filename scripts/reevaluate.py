# scripts/reevaluate.py

"""
# SCRIPT PURPOSE:
# Re-evaluate ASR transcription results by calculating alternative WER/CER metrics
# using different normalization methods (non-context-aware trnorm, legacy trnorm).
# This facilitates comparison with the original context-aware trnorm scores and aids
# in identifying high-quality transcriptions and potential mislabels.

# INPUT:
# - File path to a CSV containing ASR results.
# - Format: Comma-separated, all fields quoted, UTF-8 encoding.
# - Required Input Columns: "wer", "cer", "reference", "prediction", "hash"
#   (Note: Original "wer", "cer" were calculated using context-aware trnorm).

# PROCESSING:
# 1. Read the required columns ("wer", "cer", "reference", "prediction", "hash")
#    from the input CSV file.
# 2. Iterate through each row (transcription result).
# 3. For each row, recalculate WER and CER using:
#    a) trnorm WITHOUT context-aware normalization (results stored as wer_un, cer_un).
#    b) trnorm with LEGACY normalization (results stored as wer_l, cer_l).
# 4. Store the original data (wer, cer, reference, prediction, hash) along with
#    the newly calculated scores (wer_un, cer_un, wer_l, cer_l) in memory (e.g., a list of dictionaries).
# 5. After processing all rows, write the collected data to a new output CSV file.

# OUTPUT:
# - A new CSV file.
# - Columns:
#   - "wer": Original WER (context-aware trnorm).
#   - "cer": Original CER (context-aware trnorm).
#   - "wer_un": Recalculated WER (trnorm, non-context-aware).
#   - "cer_un": Recalculated CER (trnorm, non-context-aware).
#   - "wer_l": Recalculated WER (trnorm, legacy normalization).
#   - "cer_l": Recalculated CER (trnorm, legacy normalization).
#   - "reference": Original reference text.
#   - "prediction": Original prediction text.
#   - "hash": Original hash identifier.
"""

import csv
from pathlib import Path
from trnorm.metrics import wer as compute_wer, cer as compute_cer
from trnorm import normalize
from trnorm.legacy_normalizer import normalize_text as legacy_normalize

log_root = r"C:\Drive\hf_cache\ys0_large_v3_train_full"
log_file = r"ys-0--openai-whisper-large-v3-turbo--20250321192215_corrected.csv"  # corrected files are crated by llm api call to correct the references.
input_file = Path(log_root, log_file)

new_row_template = {
    'hash': None,
    'wer': None,
    'cer': None,
    'cosSim': None,
    'cps_ratio': None,
    'reference': None,
    'prediction': None,
    'duration': None,
}

reference_column = 'reference'  # usual
prediction_column = 'prediction'  # usual

new_rows = []
total_wer, total_cer = 0, 0

with open(input_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for idx, row in enumerate(reader):
        # Access columns by name, e.g., row['wer'], row['cer'], etc.
        wer_un = round(compute_wer(row[reference_column], row[prediction_column]) * 100, 2)
        cer_un = round(compute_cer(row[reference_column], row[prediction_column]) * 100, 2)
        wer_l = round(compute_wer(legacy_normalize(row[reference_column]), legacy_normalize(row[prediction_column])) * 100, 2)
        cer_l = round(compute_cer(legacy_normalize(row[reference_column]), legacy_normalize(row[prediction_column])) * 100, 2)

        wer_trnorm = float(row['wer'])
        cer_trnorm = float(row['cer'])

        best_wer = min(wer_trnorm, wer_un, wer_l)
        best_cer = min(cer_trnorm, cer_un, cer_l)

        # if best_wer > 22:
        #     continue

        duration = float(row['duration'])

        reference_cps = len(row['norm_reference']) / duration
        prediction_cps = len(row['norm_prediction']) / duration

        cps_ratio = abs(1 - (reference_cps / (prediction_cps + 1e-10))) * 100

        print(f"Best wer: {best_wer}, best cer: {best_cer}, {wer_trnorm=}, {wer_un=}, {wer_l=} {'✨' if best_wer != wer_trnorm else ''}")

        new_row = new_row_template.copy()
        new_row['wer'] = best_wer
        new_row['cer'] = best_cer
        new_row['cosSim'] = float(row['cosine_similarity'])
        new_row['reference'] = row[reference_column]
        new_row['prediction'] = row[prediction_column]
        new_row['hash'] = row['hash']
        new_row['duration'] = duration
        new_row['cps_ratio'] = round(cps_ratio, 2)
        new_rows.append(new_row)

        total_wer += best_wer
        total_cer += best_cer

# Write the new rows to a new CSV file
output_file = Path(log_root, f"{log_file.split('.')[0]}_reevaluated.csv")

print(f"Processed {len(new_rows)} rows")
print(f"Average WER: {total_wer / len(new_rows)}")
print(f"Average CER: {total_cer / len(new_rows)}")
print(f"Output file: {output_file}")

with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=new_row_template.keys())
    writer.writeheader()
    writer.writerows(new_rows)
