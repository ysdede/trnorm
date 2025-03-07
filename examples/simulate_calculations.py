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

import csv
from pathlib import Path
from trnorm.metrics import wer, cer, levenshtein_distance, normalized_levenshtein_distance
from trnorm import normalize

log_root = r"C:\Drive\hf_cache"
log_file = r"ysdede-commonvoice_17_tr_fixed-deepdml-faster-whisper-large-v3-turbo-ct2.tsv"
input_file = Path(log_root, log_file)

# Initialize counters
total_wer = 0
total_lev_dist = 0
total_sim = 0
count = 0

our_total_wer = 0
our_total_cer = 0
our_total_lev_dist = 0

# Required fields for processing
required_fields = ['r', 'p']  # Reference and prediction are essential

try:
    with open(input_file, "r", encoding="utf-8") as f:
        # Read as CSV with tab delimiter
        reader = csv.reader(f, delimiter='\t')
        
        # Get header row
        header = next(reader)
        
        # Create field index mapping
        field_indices = {}
        for i, field in enumerate(header):
            field_indices[field.strip().lower()] = i
        
        # Check if required fields exist
        missing_fields = [field for field in required_fields if field not in field_indices]
        if missing_fields:
            raise ValueError(f"Missing required fields in TSV: {missing_fields}")
        
        # Process each row
        for row in reader:
            try:
                # Skip empty rows
                if not row:
                    continue
                
                # Extract reference and prediction (required fields)
                ref_text = row[field_indices['r']]
                pred_text = row[field_indices['p']]
                
                # Extract other fields if they exist
                row_data = {
                    'r': ref_text,
                    'p': pred_text
                }
                
                # Try to get numeric fields if they exist
                for field in ['wer', 'cer', 'lev_dist', 'sim']:
                    if field in field_indices and field_indices[field] < len(row):
                        try:
                            row_data[field] = float(row[field_indices[field]])
                        except (ValueError, TypeError):
                            row_data[field] = None
                
                # If we have the original WER, add it to the total
                if 'wer' in row_data and row_data['wer'] is not None:
                    total_wer += row_data['wer']
                
                # If we have the original Levenshtein distance, add it to the total
                if 'lev_dist' in row_data and row_data['lev_dist'] is not None:
                    total_lev_dist += row_data['lev_dist']
                
                # If we have the original similarity score, add it to the total
                if 'sim' in row_data and row_data['sim'] is not None:
                    total_sim += row_data['sim']
                
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
                print(f"Error processing row: {row[:3]}... Error: {e}")
                continue
    
    # Print summary statistics
    if count > 0:
        # Original metrics (if available)
        if total_wer > 0:
            average_wer = round((total_wer / count), 2)
            print(f"Original Average WER: {average_wer:.2f}%")
        
        if total_lev_dist > 0:
            average_lev_dist = round(total_lev_dist / count, 2)
            print(f"Original Average Levenshtein Distance: {average_lev_dist:.2f}")
        
        if total_sim > 0:
            average_sim = round(total_sim / count, 2)
            print(f"Original Average Similarity: {average_sim:.2f}")
        
        print(f"Processed {count} valid rows")
        print(50 * "=")
        
        # Our metrics
        our_avg_wer = (our_total_wer / count) * 100
        our_avg_cer = (our_total_cer / count) * 100
        our_avg_lev_dist = our_total_lev_dist / count
        print(f"Our WER: {our_avg_wer:.2f}%")
        print(f"Our CER: {our_avg_cer:.2f}%")
        print(f"Our Levenshtein Distance: {our_avg_lev_dist:.3f}")
    else:
        print("No valid rows were processed.")

except Exception as e:
    print(f"Error processing file: {e}")
