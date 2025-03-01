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
from trnorm.metrics import wer, cer, levenshtein_distance

log_root = r"C:\Drive\hf_cache"
log_file = r"ysdede-yeni-split-0-deepdml-faster-whisper-large-v3-turbo-ct2.tsv"
input_file = Path(log_root, log_file)

lines = []
total_wer = 0
total_lev_dist = 0
total_sim = 0
count = 0

our_total_wer = 0
our_total_cer = 0

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

            our_total_wer += wer(row_data["r"], row_data["p"])
            our_total_cer += cer(row_data["r"], row_data["p"])

        except Exception as e:
            print(f"Error processing row: {row[:100]}... Error: {e}")
            continue  # Continue instead of exiting to process other rows

if count > 0:
    average_wer = total_wer / count
    average_lev_dist = total_lev_dist / count * 100
    average_sim = total_sim / count * 100
    print(f"Average WER: {average_wer:.2f}%")
    print(f"Average Levenshtein Distance: {average_lev_dist:.2f}")
    print(f"Average Similarity: {average_sim:.2f}")
    print(f"Processed {count} valid rows out of {len(rows)} total rows")
    print(50 * "=")

    print(f"Our WER: {our_total_wer / count:.2f}%")
    print(f"Our CER: {our_total_cer / count:.2f}%")
    
else:
    print("No valid rows were processed.")
