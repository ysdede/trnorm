import re
from trnorm.text_utils import is_turkish_upper

# Compile regex patterns globally for efficiency
seq_pattern = re.compile(r'(\b\d+\.,?)\s+(?=\d+\.)')
# New patterns for various ordinal formats
ordinal_pattern = re.compile(r'\b(\d+)(?:\'(?:inci|[iı]nc[iı]|nci|uncu|üncü|inci|nci)|(?:inci|[iı]nc[iı]|nci|uncu|üncü|inci|nci))\b')
# Pattern for standalone ordinals with period (must be at the start of a line or end of a line or surrounded by spaces)
standalone_ordinal = re.compile(r'(?:^|\s)(\d+)\.(?:$|\s)')
# Pattern for ordinals or bullet points in context - capture the first letter of the next word to check casing
context_ordinal = re.compile(r'(\b\d+)\.\s+([A-Za-zÇçĞğİıÖöŞşÜü]\w*)')
# Pattern specifically for bullet points at the beginning of lines
bullet_point_pattern = re.compile(r'^\s*(\d+)\.\s+([A-Za-zÇçĞğİıÖöŞşÜü]\w*)')

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

# Convert a number to its text representation (without ordinal suffix)
def normalize_number(num):
    """
    Convert an integer to its text representation in Turkish.
    
    Args:
        num: The number to convert
        
    Returns:
        The text representation (without ordinal suffix)
    """
    if num == 0:
        return "sıfır"
    
    # Handle billions
    if num >= 1000000000:
        billions = num // 1000000000
        remainder = num % 1000000000
        
        if billions == 1:
            result = "bir milyar"
        else:
            result = f"{normalize_number(billions)} milyar"
        
        if remainder > 0:
            result += f" {normalize_number(remainder)}"
        
        return result
    
    # Handle millions
    if num >= 1000000:
        millions = num // 1000000
        remainder = num % 1000000
        
        if millions == 1:
            result = "bir milyon"
        else:
            result = f"{normalize_number(millions)} milyon"
        
        if remainder > 0:
            result += f" {normalize_number(remainder)}"
        
        return result
    
    # Handle thousands
    if num >= 1000:
        thousands = num // 1000
        remainder = num % 1000
        
        if thousands == 1:
            result = "bin"
        else:
            result = f"{normalize_number(thousands)} bin"
        
        if remainder > 0:
            result += f" {normalize_number(remainder)}"
        
        return result
    
    # Handle hundreds
    if num >= 100:
        hundreds_digit = num // 100
        remainder = num % 100
        
        if hundreds_digit == 1:
            result = "yüz"
        else:
            result = f"{ones[hundreds_digit]} yüz"
        
        if remainder > 0:
            result += f" {normalize_number(remainder)}"
        
        return result
    
    # Handle tens
    if num >= 10:
        tens_digit = num // 10
        remainder = num % 10
        
        result = tens[tens_digit]
        
        if remainder > 0:
            result += f" {ones[remainder]}"
        
        return result
    
    # Handle ones
    return ones[num]

# Convert numbers to their textual representation in Turkish
def num_to_text(n):
    """
    Convert a number to its ordinal text representation in Turkish.
    
    Args:
        n: The number to convert
        
    Returns:
        The ordinal text representation
    """
    # Check for special cases first
    if n in special_cases:
        return special_cases[n]
    
    # Convert the number to its text representation
    words = normalize_number(n)
    
    # Add ordinal suffix
    if words.endswith("bir"):
        return words[:-3] + "birinci"
    elif words.endswith("iki"):
        return words[:-3] + "ikinci"
    elif words.endswith("üç"):
        return words[:-2] + "üçüncü"
    elif words.endswith("dört"):
        return words[:-4] + "dördüncü"
    elif words.endswith("beş"):
        return words[:-3] + "beşinci"
    elif words.endswith("altı"):
        return words[:-4] + "altıncı"
    elif words.endswith("yedi"):
        return words[:-4] + "yedinci"
    elif words.endswith("sekiz"):
        return words[:-5] + "sekizinci"
    elif words.endswith("dokuz"):
        return words[:-5] + "dokuzuncu"
    elif words.endswith("on"):
        return words[:-2] + "onuncu"
    elif words.endswith("yirmi"):
        return words[:-5] + "yirminci"
    elif words.endswith("otuz"):
        return words[:-4] + "otuzuncu"
    elif words.endswith("kırk"):
        return words[:-4] + "kırkıncı"
    elif words.endswith("elli"):
        return words[:-4] + "ellinci"
    elif words.endswith("altmış"):
        return words[:-6] + "altmışıncı"
    elif words.endswith("yetmiş"):
        return words[:-6] + "yetmişinci"
    elif words.endswith("seksen"):
        return words[:-6] + "sekseninci"
    elif words.endswith("doksan"):
        return words[:-6] + "doksanıncı"
    elif words.endswith("yüz"):
        return words[:-3] + "yüzüncü"
    elif words.endswith("bin"):
        return words[:-3] + "bininci"
    elif words.endswith("milyon"):
        return words[:-6] + "milyonuncu"
    elif words.endswith("milyar"):
        return words[:-6] + "milyarıncı"
    
    # Default case (should not happen with our implementation)
    return words + "ıncı"

# Check if a string starts with an uppercase letter (using text_utils)
def is_uppercase_first(s):
    """Check if the first letter of a string is uppercase."""
    if not s:
        return False
    
    # Check if the first character is uppercase using text_utils
    return is_turkish_upper(s[0])

# Check if a line is a bullet point
def is_bullet_point(line):
    """
    Check if a line is a bullet point.
    
    A bullet point typically starts with a number followed by a period and a space,
    and then a word that starts with an uppercase letter.
    
    Args:
        line: The line to check
        
    Returns:
        True if the line is a bullet point, False otherwise
    """
    match = bullet_point_pattern.match(line)
    if match and is_uppercase_first(match.group(2)):
        return True
    
    return False

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
        num, word = m.group(1), m.group(2)
        
        # If the word starts with an uppercase letter, it's likely a bullet point
        # or the start of a sentence, so keep it as is
        if is_uppercase_first(word):
            return f"{num}. {word}"
        
        # Convert the number to its ordinal text form
        return f"{num_to_text(int(num))} {word}"
    
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

    # Process the text line by line to better handle bullet points
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        # Check if the line is a bullet point (starts with a number and period followed by an uppercase word)
        if is_bullet_point(line):
            # If it's a bullet point, keep it as is
            processed_lines.append(line)
        else:
            # Apply transformations in sequence to each line
            line = re.sub(seq_pattern, seq_repl, line)
            line = re.sub(context_ordinal, context_repl, line)
            line = re.sub(standalone_ordinal, standalone_repl, line)
            line = re.sub(ordinal_pattern, ordinal_repl, line)
            processed_lines.append(line)
    
    return '\n'.join(processed_lines)
