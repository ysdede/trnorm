import re

# Compile regex patterns globally for efficiency
seq_pattern = re.compile(r'(\b\d+\.,?)\s+(?=\d+\.)')
# New patterns for various ordinal formats
ordinal_pattern = re.compile(r'\b(\d+)(?:\'(?:inci|[iı]nc[iı]|nci|uncu|üncü|inci|nci)|(?:inci|[iı]nc[iı]|nci|uncu|üncü|inci|nci))\b')
# Pattern for standalone ordinals with period (must be at the start of a line or end of a line or surrounded by spaces)
standalone_ordinal = re.compile(r'(?:^|\s)(\d+)\.(?:$|\s)')
# Pattern for ordinals in context
context_ordinal = re.compile(r'\b(\d+)\. (\w+)')

# Convert numbers to their textual representation in Turkish
def num_to_text(n):
    """
    Convert a number to its ordinal text representation in Turkish.
    
    Args:
        n: The number to convert
        
    Returns:
        The ordinal text representation
    """
    # Dictionary for basic ordinals
    ones = {
        0: "", 1: "bir", 2: "iki", 3: "üç", 4: "dört", 5: "beş",
        6: "altı", 7: "yedi", 8: "sekiz", 9: "dokuz"
    }
    
    tens = {
        1: "on", 2: "yirmi", 3: "otuz", 4: "kırk", 5: "elli",
        6: "altmış", 7: "yetmiş", 8: "seksen", 9: "doksan"
    }
    
    # Special cases for common ordinals
    special_cases = {
        1: "birinci", 2: "ikinci", 3: "üçüncü", 4: "dördüncü", 5: "beşinci",
        6: "altıncı", 7: "yedinci", 8: "sekizinci", 9: "dokuzuncu", 10: "onuncu",
        20: "yirminci", 30: "otuzuncu", 40: "kırkıncı", 50: "ellinci",
        60: "altmışıncı", 70: "yetmişinci", 80: "sekseninci", 90: "doksanıncı",
        100: "yüzüncü", 1000: "bininci"
    }
    
    if n in special_cases:
        return special_cases[n]
    
    # Handle numbers from 11-99
    if 11 <= n < 100:
        ten_digit = n // 10
        one_digit = n % 10
        
        if one_digit == 0:  # Numbers ending with 0
            return tens[ten_digit] + "ıncı"
        else:
            # For compound numbers, add the suffix to the last word
            if one_digit == 1:
                return tens[ten_digit] + " birinci"
            elif one_digit == 2:
                return tens[ten_digit] + " ikinci"
            elif one_digit == 3:
                return tens[ten_digit] + " üçüncü"
            elif one_digit == 4:
                return tens[ten_digit] + " dördüncü"
            elif one_digit == 5:
                return tens[ten_digit] + " beşinci"
            elif one_digit == 6:
                return tens[ten_digit] + " altıncı"
            elif one_digit == 7:
                return tens[ten_digit] + " yedinci"
            elif one_digit == 8:
                return tens[ten_digit] + " sekizinci"
            elif one_digit == 9:
                return tens[ten_digit] + " dokuzuncu"
    
    # Handle larger numbers (simplified approach)
    return special_cases.get(n, f"{n}.")

# Normalize text with compiled regex patterns
def normalize_ordinals(text):
    """
    Normalize ordinals in text to their textual representation.
    
    Args:
        text: The input text containing ordinals
        
    Returns:
        Text with normalized ordinals
    """
    def context_repl(m):
        num, keyword = int(m.group(1)), m.group(2)
        return f"{num_to_text(num)} {keyword}"
    
    def seq_repl(m):
        nums = list(map(int, re.findall(r'\d+', m.group(0))))
        return ', '.join(num_to_text(num) for num in nums) + ' '
    
    def ordinal_repl(m):
        num = int(m.group(1))
        return num_to_text(num)
    
    def standalone_repl(m):
        num = int(m.group(1))
        # Preserve the space before or after if it exists
        prefix = ' ' if m.group(0)[0] == ' ' else ''
        suffix = ' ' if m.group(0)[-1] == ' ' else ''
        return prefix + num_to_text(num) + suffix

    # Apply transformations in sequence
    text = re.sub(seq_pattern, seq_repl, text)
    text = re.sub(context_ordinal, context_repl, text)
    text = re.sub(standalone_ordinal, standalone_repl, text)
    text = re.sub(ordinal_pattern, ordinal_repl, text)
    
    return text
