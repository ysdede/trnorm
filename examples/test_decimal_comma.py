"""
Test script to verify the handling of decimal numbers with trailing commas.
"""

import sys
import os

# Add the parent directory to the path to import trnorm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm.num_to_text import NumberToTextConverter

def test_decimal_numbers():
    """Test various decimal number formats with trailing commas."""
    converter = NumberToTextConverter()
    
    test_cases = [
        # Test case from the issue
        ("her tarafa 29,54, eklersek son hızın dikey bileşenine ulaşmış olacağız.", 
         "her tarafa yirmi dokuz virgül elli dört, eklersek son hızın dikey bileşenine ulaşmış olacağız."),
        
        # Additional test cases
        ("Hızı 12,5, olarak ölçtük.", 
         "Hızı on iki virgül beş, olarak ölçtük."),
        
        ("Sıcaklık 36,6, olarak ölçüldü.", 
         "Sıcaklık otuz altı virgül altı, olarak ölçüldü."),
        
        # Test with multiple decimal numbers
        ("Ölçümler 10,5, ve 20,3, olarak kaydedildi.", 
         "Ölçümler on virgül beş, ve yirmi virgül üç, olarak kaydedildi."),
        
        # Test with comma at the end of a sentence
        ("Enflasyon oranı 8,75,", 
         "Enflasyon oranı sekiz virgül yetmiş beş,"),
        
        # Test with period+space
        ("Saat 14.30 gibi geleceğim.", 
         "Saat on dört. otuz gibi geleceğim."),
        
        # Test with comma+space
        ("Ölçümler 10, 20 ve 30 olarak kaydedildi.", 
         "Ölçümler on, yirmi ve otuz olarak kaydedildi."),
    ]
    
    for i, (input_text, expected_output) in enumerate(test_cases):
        result = converter.convert_numbers_to_words(input_text)
        print(f"Test {i+1}:")
        print(f"Input:    {input_text}")
        print(f"Expected: {expected_output}")
        print(f"Result:   {result}")
        print(f"{'✓ PASS' if result == expected_output else '✗ FAIL'}")
        print()

if __name__ == "__main__":
    test_decimal_numbers()
