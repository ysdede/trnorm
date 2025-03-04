"""
Script to analyze WER, CER, and Levenshtein distance for example sentences.
"""

from trnorm.metrics import wer, cer, levenshtein_distance

# Example sentences
reference = "gerçekler kazma kürek olunca kas gücü de olmayınca bir yerde yapamıyoruz galibaya geldi"
hypothesis = "gerçekler kazma kürek olunca kaz gücü de olmayınca bir yerde yapamıyoruz galiba ya geldi"

# Calculate metrics
wer_score = wer(reference, hypothesis)
cer_score = cer(reference, hypothesis)
lev_distance = levenshtein_distance(reference, hypothesis)

# Print results
print(f"Reference: {reference}")
print(f"Hypothesis: {hypothesis}")
print(f"WER: {wer_score:.4f} ({wer_score*100:.2f}%)")
print(f"CER: {cer_score:.4f} ({cer_score*100:.2f}%)")
print(f"Levenshtein Distance: {lev_distance}")

# Analyze word by word
ref_words = reference.split()
hyp_words = hypothesis.split()

print("\nWord-by-word analysis:")
print("-" * 60)
print(f"{'Reference':<20} {'Hypothesis':<20} {'Match':<10}")
print("-" * 60)

for i in range(max(len(ref_words), len(hyp_words))):
    ref_word = ref_words[i] if i < len(ref_words) else ""
    hyp_word = hyp_words[i] if i < len(hyp_words) else ""
    match = "✓" if ref_word == hyp_word else "✗"
    print(f"{ref_word:<20} {hyp_word:<20} {match:<10}")

# Detailed analysis of the WER calculation
print("\nDetailed WER calculation:")
print("-" * 60)

# Calculate edit operations
operations = []
i, j = 0, 0
while i < len(ref_words) and j < len(hyp_words):
    if ref_words[i] == hyp_words[j]:
        operations.append(f"Match: {ref_words[i]} = {hyp_words[j]}")
        i += 1
        j += 1
    else:
        # Simple heuristic to determine operation type
        if i + 1 < len(ref_words) and ref_words[i + 1] == hyp_words[j]:
            operations.append(f"Deletion: {ref_words[i]}")
            i += 1
        elif j + 1 < len(hyp_words) and ref_words[i] == hyp_words[j + 1]:
            operations.append(f"Insertion: {hyp_words[j]}")
            j += 1
        else:
            operations.append(f"Substitution: {ref_words[i]} → {hyp_words[j]}")
            i += 1
            j += 1

# Handle remaining words
while i < len(ref_words):
    operations.append(f"Deletion: {ref_words[i]}")
    i += 1
while j < len(hyp_words):
    operations.append(f"Insertion: {hyp_words[j]}")
    j += 1

for op in operations:
    print(op)

# Count operations
substitutions = sum(1 for op in operations if op.startswith("Substitution"))
deletions = sum(1 for op in operations if op.startswith("Deletion"))
insertions = sum(1 for op in operations if op.startswith("Insertion"))

print("\nOperation counts:")
print(f"Substitutions: {substitutions}")
print(f"Deletions: {deletions}")
print(f"Insertions: {insertions}")
print(f"Total operations: {substitutions + deletions + insertions}")
print(f"Reference word count: {len(ref_words)}")
print(f"Manual WER calculation: {(substitutions + deletions + insertions) / len(ref_words):.4f} ({(substitutions + deletions + insertions) / len(ref_words) * 100:.2f}%)")

# Tokenization analysis
print("\nTokenization analysis:")
print(f"Reference word count: {len(ref_words)}")
print(f"Reference words: {ref_words}")
print(f"Hypothesis word count: {len(hyp_words)}")
print(f"Hypothesis words: {hyp_words}")

# Check if "galibaya" vs "galiba ya" is causing the difference
if "galibaya" in ref_words and "galiba" in hyp_words and "ya" in hyp_words:
    galibaya_index = ref_words.index("galibaya")
    galiba_index = hyp_words.index("galiba")
    ya_index = hyp_words.index("ya")
    
    print("\nFound tokenization difference:")
    print(f"Reference has 'galibaya' at position {galibaya_index}")
    print(f"Hypothesis has 'galiba' at position {galiba_index} and 'ya' at position {ya_index}")
    
    if galiba_index + 1 == ya_index:
        print("'galiba' and 'ya' are adjacent in the hypothesis")
        print("This could explain the WER difference (1 deletion + 1 insertion instead of 1 substitution)")
