"""
Tests for alphanumeric pattern handling.
"""

import unittest
from trnorm.alphanumeric import separate_alphanumeric, normalize_alphanumeric


class TestAlphanumeric(unittest.TestCase):
    """Test cases for alphanumeric pattern handling."""
    
    def test_separate_alphanumeric(self):
        """Test separating alphanumeric patterns."""
        test_cases = [
            # Single letter followed by a number
            ("F3", "F 3"),
            ("B1", "B 1"),
            ("A400", "A 400"),
            
            # Multiple letters followed by a number
            ("AB123", "AB 123"),
            ("CD45", "CD 45"),
            
            # Lowercase letters
            ("f16", "f 16"),
            ("b2", "b 2"),
            
            # Mixed case
            ("Fb17", "Fb 17"),
            
            # Multiple occurrences
            ("F3 ve B1 uçakları", "F 3 ve B 1 uçakları"),
            ("A1 sınıfı ve B2 vitamini", "A 1 sınıfı ve B 2 vitamini"),
            
            # Text with no alphanumeric patterns
            ("Normal text without patterns", "Normal text without patterns"),
            ("123 456", "123 456"),
            ("ABC DEF", "ABC DEF"),
            
            # Edge cases
            ("A1B2", "A 1B 2"),  # This is how the regex will handle it
            ("A1B2C3", "A 1B 2C 3"),
            
            # With punctuation
            ("F16.", "F 16."),
            ("B1,", "B 1,"),
            ("A400!", "A 400!"),
        ]
        
        for input_text, expected in test_cases:
            self.assertEqual(separate_alphanumeric(input_text), expected,
                            f"Failed to separate alphanumeric pattern in: {input_text}")
    
    def test_normalize_alphanumeric(self):
        """Test normalizing alphanumeric patterns with the separate parameter."""
        input_text = "F3 ve B1 uçakları A400 taşıyabilir."
        expected_separated = "F 3 ve B 1 uçakları A 400 taşıyabilir."
        
        # Test with separation enabled (default)
        self.assertEqual(normalize_alphanumeric(input_text), expected_separated,
                        "Failed to normalize with separation enabled")
        
        # Test with separation explicitly enabled
        self.assertEqual(normalize_alphanumeric(input_text, separate=True), expected_separated,
                        "Failed to normalize with separation explicitly enabled")
        
        # Test with separation disabled
        self.assertEqual(normalize_alphanumeric(input_text, separate=False), input_text,
                        "Failed to normalize with separation disabled")


if __name__ == "__main__":
    unittest.main()
