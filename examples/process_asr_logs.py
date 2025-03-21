"""
We have the following ASR log:
tab seperated csv file with cols:
wer: WER metric
lev_dist: Levenshtein distance
sim: Similarity score
dur: Input audio duration
time: Inference time
r: Reference ground-truth sentence
p: Predicted sentence

Sample:
wer     lev_dist	sim	    dur	    time	r	                                                p
40.00	0.042	    0.984	2.639	0.204	Kafkas göçmenleriyse günlük tartışmalardan uzak.	Kafkas göçmenleri ise günlük tartışmalardan uzak.

Import wer and cer from evaluate module and calculate raw wer and cer scores for each line.
We don't need duration and time for this task.
"""

from pathlib import Path
from trnorm.metrics import wer, cer, levenshtein_distance, normalized_levenshtein_distance
from trnorm import normalize
from trnorm.legacy_normalizer import normalize_text, replace_hatted_characters, turkish_lower
from trnorm.dimension_utils import preprocess_dimensions, normalize_dimensions
from trnorm.unit_utils import normalize_units
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.ordinals import normalize_ordinals
from trnorm.symbols import convert_symbols

log_root = r"C:\Drive\hf_cache"
# log_file = r"ysdede-yeni-split-0-deepdml-faster-whisper-large-v3-turbo-ct2.tsv"
log_file = r"erenfazlioglu-turkishvoicedataset-deepdml-faster-whisper-large-v3-turbo-ct2.tsv"
input_file = Path(log_root, log_file)

lines = []
total_wer = 0
total_lev_dist = 0
total_sim = 0
count = 0

our_total_wer = 0
our_total_cer = 0
our_total_lev_dist = 0

# Define the normalization functions we want to use
normalization_functions = [
    preprocess_dimensions,
    convert_symbols,
    normalize_dimensions,
    convert_numbers_to_words_wrapper,
    normalize_ordinals,
    normalize_units,
    replace_hatted_characters,
    turkish_lower,
    normalize_text  # Legacy normalization (more aggressive)
]

with open(input_file, "r", encoding="utf-8") as f:
    # Read the entire file as text
    content = f.read()
    
    # Split by newline characters
    rows = content.strip().split('\n')
    
    # Skip header
    header = rows[0]
    rows = rows[1:]
    
    for row in rows:
        try:
            # Split by tab character
            fields = row.split('\t')
            
            # Make sure we have at least 7 fields
            if len(fields) < 7:
                print(f"Skipping row with insufficient fields: {fields}")
                continue
                
            # Create a new row dictionary for each line
            row_data = {
                "wer": float(fields[0]),
                "lev_dist": float(fields[1]),
                "sim": float(fields[2]),
                "r": fields[5],
                "p": fields[6]
            }
            
            lines.append(row_data)

            total_wer += row_data["wer"]
            total_lev_dist += row_data["lev_dist"]
            total_sim += row_data["sim"]

            count += 1

            # Use the new simplified normalizer approach with direct function references
            ref = normalize(row_data["r"], normalization_functions)
            hyp = normalize(row_data["p"], normalization_functions)

            our_wer = wer(ref, hyp)
            our_cer = cer(ref, hyp)
            our_lev_dist = normalized_levenshtein_distance(ref, hyp)

            our_total_wer += our_wer
            our_total_cer += our_cer
            our_total_lev_dist += our_lev_dist
            
            if round(our_wer * 100, 2) > row_data['wer']:
                print(f"{our_wer * 100:.2f}/{row_data['wer']:.2f} - {our_lev_dist:.3f}/{row_data['lev_dist']:.3f}")
                print(f"{row_data['r']}\n{row_data['p']}")
                print(ref)
                print(hyp)
                print("*" * 50)

        except Exception as e:
            print(f"Error processing row: {row[:100]}... Error: {e}")
            continue  # Continue instead of exiting to process other rows

if count > 0:
    average_wer = round((total_wer / count), 2)
    average_lev_dist = round(total_lev_dist / count, 2)
    average_sim = round(total_sim / count, 2)
    print(f"Average WER: {average_wer:.2f}%")
    print(f"Average Levenshtein Distance: {average_lev_dist:.2f}")
    print(f"Average Similarity: {average_sim:.2f}")
    print(f"Processed {count} valid rows out of {len(rows)} total rows")
    print(50 * "=")

    our_avg_wer = (our_total_wer / count) * 100
    our_avg_cer = (our_total_cer / count) * 100
    our_lev_dist = our_total_lev_dist / count
    print(f"Our WER: {our_avg_wer:.2f}%")
    print(f"Our CER: {our_avg_cer:.2f}%")
    print(f"Our levenshtein distance: {our_lev_dist:.3f}")
else:
    print("No valid rows were processed.")
