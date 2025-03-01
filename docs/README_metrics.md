# Text Similarity Metrics

## Overview

The `metrics` module provides tools for evaluating text similarity, which is particularly useful for:

- Evaluating Automatic Speech Recognition (ASR) system performance
- Measuring the quality of text normalization
- Comparing different versions of Turkish text

## Available Metrics

### Levenshtein Distance

The Levenshtein distance is a measure of the similarity between two strings. It represents the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one string into another.

```python
from trnorm.metrics import levenshtein_distance

# Calculate distance between two strings
distance = levenshtein_distance("kitten", "sitting")  # Returns 3

# Can also be used with lists
distance = levenshtein_distance(["a", "b", "c"], ["a", "b", "d"])  # Returns 1
```

### Word Error Rate (WER)

WER is a common metric for evaluating speech recognition systems. It represents the percentage of words that were incorrectly recognized.

```python
from trnorm.metrics import wer

reference = "bu bir test cümlesidir"
hypothesis = "bu bir test cümlesi"

wer_score = wer(reference, hypothesis)  # Returns 0.25 (25%)
```

The WER is calculated as:

```
WER = (S + D + I) / N
```

Where:
- S is the number of substitutions
- D is the number of deletions
- I is the number of insertions
- N is the number of words in the reference

### Character Error Rate (CER)

CER is similar to WER but operates at the character level. It represents the percentage of characters that were incorrectly recognized.

```python
from trnorm.metrics import cer

reference = "otomatik konuşma tanıma"
hypothesis = "otomotik konuşma tanımla"

cer_score = cer(reference, hypothesis)  # Returns approximately 0.087 (8.7%)
```

The CER is calculated using the same formula as WER, but at the character level.

## Turkish-Specific Considerations

When working with Turkish text, these metrics take into account the unique characteristics of the Turkish language:

- Turkish has additional characters not found in English (ç, ğ, ı, ö, ş, ü)
- Case sensitivity is important for proper evaluation (I/ı and İ/i are distinct letters)
- Word boundaries may differ in Turkish compared to other languages

## Example Usage

### Basic Example

```python
from trnorm.metrics import wer, cer, levenshtein_distance

reference = "Türkçe metin normalizasyonu önemlidir"
hypothesis = "Türkçe metin normalizasyon önemli"

# Calculate metrics
wer_score = wer(reference, hypothesis)
cer_score = cer(reference, hypothesis)
lev_distance = levenshtein_distance(reference, hypothesis)

print(f"WER: {wer_score:.4f}")
print(f"CER: {cer_score:.4f}")
print(f"Levenshtein Distance: {lev_distance}")
```

### Processing ASR Logs

The package includes an example script for processing ASR log files:

```python
from trnorm.metrics import wer, cer

# For each line in an ASR log file
for line in asr_log:
    reference = line["reference_text"]
    hypothesis = line["asr_output"]
    
    # Calculate metrics
    wer_score = wer(reference, hypothesis)
    cer_score = cer(reference, hypothesis)
    
    # Process or store results
    print(f"WER: {wer_score:.4f}, CER: {cer_score:.4f}")
```

See the full example in `examples/process_asr_logs.py`.

## Integration with Other Modules

The metrics module can be used in conjunction with other trnorm modules:

```python
from trnorm.metrics import wer
from trnorm.num_to_text import convert_numbers_to_words_wrapper

# Original text with numbers
reference = "Bu 42 sayısı önemlidir"
# Text with normalized numbers
normalized = convert_numbers_to_words_wrapper(reference)
# ASR output
hypothesis = "bu kırk iki sayısı önemli"

# Calculate WER between original and ASR output
original_wer = wer(reference, hypothesis)
# Calculate WER between normalized and ASR output
normalized_wer = wer(normalized, hypothesis)

print(f"Original WER: {original_wer:.4f}")
print(f"Normalized WER: {normalized_wer:.4f}")
```

This demonstrates how normalization can improve ASR evaluation metrics by converting numbers to their text representation before comparison.
