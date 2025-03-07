"""
Example demonstrating the use of the Turkish suffix handler.

This example shows how to use the suffix_handler module to process Turkish
suffixes in text, merging them with their preceding words according to
Turkish grammar rules.
"""

from trnorm.suffix_handler import merge_suffixes

# Define example sentences with various Turkish suffixes
examples = [
    # Examples with 'ile' suffix
    "Toros ile hamile",
    "Ankara ile İstanbul arasında yolculuk yaptık",
    "Ali ile Veli arkadaş oldular",
    "Kalem ile defter aldım",
    
    # Examples with 'ise' suffix
    "Hayat sana limon verdi ise limonata yap",
    "Ankara ise daha büyük bir şehir",
    "Ali ise yarın gelecek",
    "Çay ise daha sıcak içilir",
    
    # Examples with 'iken' suffix
    "Hâl böyle iken böyle dedi adam",
    "Ankara iken İstanbul'a taşındı",
    "Çocuk iken hayalleri vardı",
    "Öğrenci iken çalışıyordu",
    
    # Examples with multiple suffix types
    "Toros ile giderken yağmur yağdı ise şemsiye al",
    "Ali iken Veli ile tanıştı ise iyi oldu",
    "Çay ise içelim, kahve ile de olur iken vazgeçtim",
    
    # Examples with abbreviations and special cases
    "AB ile ilgili konular",
    "x ile y arasındaki ilişki",
    "Toros ile",
    "ile Toros",
]

# Process all examples
print("Turkish Suffix Handling Examples")
print("=" * 80)
print("{:<50} {:<50}".format("Original", "Processed"))
print("-" * 100)

for example in examples:
    processed = merge_suffixes(example)
    print("{:<50} {:<50}".format(example, processed))

print("\nProcessing a list of strings:")
print("=" * 80)

# Process a list of strings
input_list = [
    "Toros ile hamile",
    "Hayat sana limon verdi ise limonata yap",
    "Hâl böyle iken böyle dedi adam"
]

processed_list = merge_suffixes(input_list)

for original, processed in zip(input_list, processed_list):
    print("{:<50} {:<50}".format(original, processed))

print("\nExample completed!")
