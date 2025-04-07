# scripts/reevaluate_corrected.py

"""
Re-evaluates ASR predictions against LLM-corrected references.

This script reads a CSV file containing ASR predictions and corresponding
reference transcriptions that have been corrected by a Language Model (LLM).
It aims to provide a refined quality assessment by calculating WER and CER
using the LLM correction as the ground truth and comparing results from
three different normalization techniques provided by the `trnorm` library:
1.  Non-context-aware normalization (via direct compute_wer/cer calls).
2.  Legacy normalization (`legacy_normalize`).
3.  Context-aware normalization (`normalize`).

For each transcription pair (LLM correction vs. ASR prediction), the script
calculates WER and CER using all three methods and then selects the minimum
(best) score obtained for both WER and CER.

The final output is a new CSV file containing these best scores, along with
the LLM correction (as the 'reference'), the original prediction, the hash,
and the cosine similarity. This output facilitates filtering for high-quality
transcriptions based on the improved LLM references and diverse metric calculations.

Input Data Requirements:
    - CSV file format: Comma-separated, all fields quoted, UTF-8 encoding.
    - Source file path configured via `log_root` and `log_file` variables.
    - Required Input Columns:
        - 'correction': Text corrected by an LLM (used as reference).
        - 'prediction': Original ASR hypothesis text.
        - 'hash': Unique identifier.
        - 'cosine_similarity': Pre-calculated similarity score.

Output Data:
    - A new CSV file is created in `log_root` with "_reevaluated" appended
      to the original filename (before the extension).
    - Output Columns:
        - "hash": Unique identifier from input.
        - "wer": The minimum WER calculated across the 3 normalization methods.
        - "cer": The minimum CER calculated across the 3 normalization methods.
        - "cosSim": Cosine similarity score from input.
        - "reference": The LLM-corrected text (from input 'correction' column).
        - "prediction": The original ASR prediction text from input.
"""

import csv
from pathlib import Path
from trnorm.metrics import wer as compute_wer, cer as compute_cer
from trnorm import normalize
from trnorm.legacy_normalizer import normalize_text as legacy_normalize

log_root = r"C:\Drive\hf_cache\ys0_large_v3_train_full"
# log_file = r"ys-0--openai-whisper-large-v3-turbo--20250321192215_corrected.csv"  # corrected files are crated by llm api call to correct the references.
# log_file = r"ys-0--openai-whisper-large-v3-turbo--20250321193856_corrected.csv"  # corrected files are crated by llm api call to correct the references.
log_file = r"ys-0--openai-whisper-large-v3-turbo--20250321194154_corrected.csv"  # corrected files are crated by llm api call to correct the references.

input_file = Path(log_root, log_file)

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
reference_column = 'correction'  # alternative reference
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
        
        reference_normalized = normalize(row[reference_column], context_text=row[prediction_column])
        prediction_normalized = normalize(row[prediction_column], context_text=row[reference_column])

        wer_trnorm = round(compute_wer(reference_normalized, prediction_normalized) * 100, 2)
        cer_trnorm = round(compute_cer(reference_normalized, prediction_normalized) * 100, 2)

        best_wer = min(wer_trnorm, wer_un, wer_l)
        best_cer = min(cer_trnorm, cer_un, cer_l)

        # if best_wer > 22:
        #     continue

        print(f"Best wer: {best_wer}, best cer: {best_cer}, {wer_trnorm=}, {wer_un=}, {wer_l=} {'✨' if best_wer != wer_trnorm else ''}")

        new_row = new_row_template.copy()
        new_row['wer'] = best_wer
        new_row['cer'] = best_cer
        new_row['cosSim'] = float(row['cosine_similarity'])
        new_row['reference'] = row[reference_column]
        new_row['prediction'] = row[prediction_column]
        new_row['hash'] = row['hash']
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
