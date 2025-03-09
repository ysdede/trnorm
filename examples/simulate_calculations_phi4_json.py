"""
We now read from a JSON file with the following structure:
{
    "all_generated_texts": ["prediction1", "prediction2", ...],
    "all_labels": ["reference1", "reference2", ...],
    "wer": 0.0957283866575902,
    "cer": 0.026012004576156968
}
"""

import json
import sys
from pathlib import Path
from trnorm.metrics import (
    wer,
    cer,
    normalized_levenshtein_distance
)
from trnorm import normalize

log_root = r"C:\Drive\hf_cache"
log_file = r"ysdede-tr-med-audio--ysdede-Phi-4-mm-inst-asr-turkish-unf--eval_after.json"  # Updated to use a JSON file
input_file = Path(log_root, log_file)

# Initialize counters
total_wer = 0
total_cer = 0
count = 0

our_total_wer = 0
our_total_cer = 0
our_total_lev_dist = 0

perfect_predictions = 0

try:
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
        # Extract data from JSON
        predictions = data.get("all_generated_texts", [])
        references = data.get("all_labels", [])
        original_wer = data.get("wer")
        original_cer = data.get("cer")
        
        # Ensure we have matching references and predictions
        if len(predictions) != len(references):
            print(f"Warning: Number of predictions ({len(predictions)}) doesn't match references ({len(references)})")
            count = min(len(predictions), len(references))
        else:
            count = len(predictions)
        
        # Process each reference-prediction pair
        for i in range(count):
            ref_text = references[i]
            pred_text = predictions[i]
            
            # Use context-aware normalization for better WER/CER calculations
            normalized_ref = normalize(ref_text, context_text=pred_text)
            normalized_hyp = normalize(pred_text, context_text=ref_text)
            
            our_wer_score = wer(normalized_ref, normalized_hyp)
            our_cer_score = cer(normalized_ref, normalized_hyp)
            our_lev_dist_score = normalized_levenshtein_distance(normalized_ref, normalized_hyp)
            
            our_total_wer += our_wer_score
            our_total_cer += our_cer_score
            our_total_lev_dist += our_lev_dist_score

            if our_wer_score == 0 or our_cer_score == 0:
                perfect_predictions += 1

            # Print cases where our WER is significantly different from the original
            # (Since we don't have per-item WER in the JSON, we'll just print some samples)
            if our_wer_score > 0.70:  # Print first 5 and any with high WER
                print(f"Sample {i+1} - Our WER: {our_wer_score * 100:.2f}%, Our CER: {our_cer_score * 100:.2f}%")
                print(f"Reference: {ref_text}")
                print(f"Prediction: {pred_text}")
                print(f"Normalized Reference: {normalized_ref}")
                print(f"Normalized Hypothesis: {normalized_hyp}")
                print("*" * 50)
    
    # Print summary statistics
    if count > 0:
        # Original metrics (if available)
        if original_wer is not None:
            print(f"Original WER: {original_wer * 100:.2f}%")
        
        if original_cer is not None:
            print(f"Original CER: {original_cer * 100:.2f}%")
        
        print(f"Processed {count} valid pairs")
        print("=" * 50)
        
        # Our metrics
        our_average_wer = round((our_total_wer / count) * 100, 2)
        our_average_cer = round((our_total_cer / count) * 100, 2)
        our_average_lev_dist = round(our_total_lev_dist / count, 3)
        
        print(f"Our WER: {our_average_wer}%")
        print(f"Our CER: {our_average_cer}%")
        print(f"Our Levenshtein Distance: {our_average_lev_dist}")
        print(f"Total predictions: {len(predictions)}, perfect predictions: {perfect_predictions}")
    else:
        print("No valid pairs processed.")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
