"""
Utilities for handling time expressions in Turkish text.

This module provides functions to convert time expressions to their full text
representations in Turkish before applying number-to-text conversion.
"""

import re

def normalize_times(text):
    """
    Normalize time expressions in text to their text representations.
    
    This function identifies and converts time expressions in various formats:
    - Standard formats: "saat 22.00", "22:30", etc.
    - Special cases: converts "hh.30" to "hh buçuk" (half past hour)
    
    The function preserves the original structure of the text while ensuring that
    time expressions are properly normalized before number-to-text conversion.
    
    Args:
        text (str): The input text containing time expressions
        
    Returns:
        str: The text with time expressions converted to their text representations
    """
    # Pattern for times with "saat" prefix (e.g., "saat 22.00", "saat 9:45")
    # Group 1: "saat" prefix
    # Group 2: Hours
    # Group 3: Separator (. or :)
    # Group 4: Minutes
    saat_pattern = r'(\bsaat\s+)(\d{1,2})([\.:])(\d{2})\b'
    
    # Pattern for standalone times (e.g., "22.00", "9:45")
    # Group 1: Hours
    # Group 2: Separator (. or :)
    # Group 3: Minutes
    time_pattern = r'\b(\d{1,2})([\.:])(\d{2})\b'
    
    # Process times with "saat" prefix first
    def replace_saat_time(match):
        saat_prefix = match.group(1)  # "saat "
        hours = match.group(2)
        separator = match.group(3)  # . or :
        minutes = match.group(4)
        
        # Special case for half hours
        if minutes == "30":
            return f"{saat_prefix}{hours} buçuk"
        
        # For other times, preserve the format but mark it to prevent number-to-text conversion
        return f"{saat_prefix}{hours} {minutes}"
    
    # First process times with "saat" prefix
    processed_text = re.sub(saat_pattern, replace_saat_time, text)
    
    # Then process standalone times that might be time expressions
    # This is more complex as we need to determine if it's actually a time
    def is_likely_time(hours, minutes):
        # Check if hours and minutes are valid time components
        h = int(hours)
        m = int(minutes)
        return 0 <= h <= 23 and 0 <= m <= 59
    
    def replace_standalone_time(match):
        hours = match.group(1)
        separator = match.group(2)
        minutes = match.group(3)
        
        # Only convert if it looks like a valid time
        if is_likely_time(hours, minutes):
            # Special case for half hours
            if minutes == "30":
                return f"{hours} buçuk"
            
            # For other times, preserve the format but mark it to prevent number-to-text conversion
            return f"{hours} {minutes}"
        
        # If it doesn't look like a time, return the original text
        return match.group(0)
    
    # Process standalone times
    return re.sub(time_pattern, replace_standalone_time, processed_text)
