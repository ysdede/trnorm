"""
Example script demonstrating time normalization in Turkish text.

This script shows how the time normalization feature works with various
time formats and in different contexts.
"""

from trnorm import normalize
from trnorm.time_utils import normalize_times


def main():
    """
    Demonstrate time normalization with various examples.
    """
    print("Turkish Time Normalization Examples")
    print("==================================")
    print()

    # Example 1: Basic time normalization
    print("Example 1: Basic time normalization")
    examples = [
        "saat 22.00",  # Zero minutes - will be omitted
        "saat 9:45",
        "13.30",
        "7:15",
        "08.00"        # Zero minutes - will be omitted
    ]
    
    for example in examples:
        print(f"Original: {example}")
        normalized = normalize_times(example)
        print(f"After time normalization: {normalized}")
        fully_normalized = normalize(example)
        print(f"Fully normalized: {fully_normalized}")
        print()
    
    # Example 2: Times in sentences
    print("Example 2: Times in sentences")
    examples = [
        "Toplantı saat 14.30'da başlayacak.",
        "Uçak 22:15'te kalkacak ve 06:45'te inecek.",
        "Ancak 13 Nisan 2024 akşamı saat 22.00 sularında, İran Devrim Muhafızları, İsrail'i hedef alarak devasa bir füze saldırısı başlattı.",
        "Toplantı saat 9.00'da başlayacak."  # Zero minutes - will be omitted
    ]
    
    for example in examples:
        print(f"Original: {example}")
        normalized = normalize_times(example)
        print(f"After time normalization: {normalized}")
        fully_normalized = normalize(example)
        print(f"Fully normalized: {fully_normalized}")
        print()
    
    # Example 3: Comparing with and without time normalization
    print("Example 3: Comparing with and without time normalization")
    example = "Ancak 13 Nisan 2024 akşamı saat 22.00 sularında, İran Devrim Muhafızları, İsrail'i hedef alarak devasa bir füze saldırısı başlattı."
    
    print(f"Original: {example}")
    
    # Without time normalization (will interpret 22.00 as a decimal number)
    without_time_norm = normalize(example, apply_time_normalization=False)
    print(f"Without time normalization: {without_time_norm}")
    
    # With time normalization (will correctly handle 22.00 as a time)
    with_time_norm = normalize(example)
    print(f"With time normalization: {with_time_norm}")
    print()
    
    # Example 4: Half-hour expressions
    print("Example 4: Half-hour expressions")
    examples = [
        "saat 13.30'da",
        "7:30'da",
        "Toplantı 14.30'da başlayacak."
    ]
    
    for example in examples:
        print(f"Original: {example}")
        normalized = normalize(example)
        print(f"Normalized: {normalized}")
        print()
    
    # Example 5: Zero minutes (new behavior)
    print("Example 5: Zero minutes (omitted)")
    examples = [
        "saat 10.00",
        "15:00",
        "Toplantı 9.00'da başlayacak.",
        "Saat 18.00 itibariyle tüm hazırlıklar tamamlanmış olacak."
    ]
    
    for example in examples:
        print(f"Original: {example}")
        normalized = normalize_times(example)
        print(f"After time normalization: {normalized}")
        fully_normalized = normalize(example)
        print(f"Fully normalized: {fully_normalized}")
        print()


if __name__ == "__main__":
    main()
