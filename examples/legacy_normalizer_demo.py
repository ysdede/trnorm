"""
Demo for the legacy normalizer module.
This script demonstrates the usage of the legacy normalizer with various examples,
including the edge case handling for non-Turkish text.
"""

from trnorm.legacy_normalizer import normalize_text

def main():
    """Run the demo with various examples."""
    examples = [
        # Basic examples
        "Hello World",
        "Merhaba Dünya",
        "İstanbul",
        
        # Examples with special characters
        "Türkçe'de 'tırnak' işaretleri",
        'Türkçe"de "tırnak" işaretleri',
        
        # Examples with hatted characters
        "Kâğıt, Âdem, Îmân",
        
        # Non-Turkish characters (edge cases)
        "123",
        "!@#",
        "   ",
        "",
        
        # Mixed content
        "İstanbul'da 2023 yılında!",
        
        # Non-Latin script (edge case)
        "こんにちは世界",
        
        # Mixed scripts
        "Hello こんにちは İstanbul"
    ]
    
    print("Legacy Normalizer Demo")
    print("======================")
    
    for i, example in enumerate(examples, 1):
        normalized = normalize_text(example)
        print(f"\nExample {i}:")
        print(f"  Original: '{example}'")
        print(f"  Normalized: '{normalized}'")
        
    # List example
    list_example = ["Merhaba", "Dünya", "İstanbul'da", "123"]
    normalized_list = normalize_text(list_example)
    
    print("\nList Example:")
    print(f"  Original: {list_example}")
    print(f"  Normalized: {normalized_list}")

if __name__ == "__main__":
    main()
