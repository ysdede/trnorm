"""
Mappings for symbol conversion in Turkish text normalization.

This module defines the mappings between symbols and their text representations
in Turkish. Users can modify this file to add new mappings or change existing ones.
"""

# Dictionary of symbol mappings
# Format: symbol: (text_representation, text_after)
# If text_after is True, the text will be placed after the number (e.g., for currencies)
# If text_after is False, the text will be placed before the number (e.g., for percent)
SYMBOL_MAPPINGS = {
    # Percent symbol
    "%": ("yüzde", False),
    
    # Currency symbols
    "$": ("dolar", True),
    "€": ("avro", True),
    "£": ("sterlin", True),
    "₺": ("lira", True),
    "¥": ("yen", True),
    "₽": ("ruble", True),
    "₹": ("rupi", True),
    "₩": ("won", True),
    "฿": ("baht", True),
    "₫": ("dong", True),
    "₴": ("grivna", True),
    "₲": ("guarani", True),
    "₱": ("peso", True),
    "₡": ("colon", True),
    "₦": ("naira", True),
    "₭": ("kip", True),
    
    # Add more symbols as needed
}

# Function to get all symbol mappings
def get_all_mappings():
    """
    Get all symbol mappings.
    
    Returns:
        dict: Dictionary of symbol mappings
    """
    return SYMBOL_MAPPINGS

# Function to get a specific symbol mapping
def get_mapping(symbol):
    """
    Get the mapping for a specific symbol.
    
    Args:
        symbol (str): The symbol to get the mapping for
        
    Returns:
        tuple: (text_representation, text_after) or None if the symbol is not found
    """
    return SYMBOL_MAPPINGS.get(symbol)

# Function to add a new symbol mapping
def add_mapping(symbol, text_representation, text_after=False):
    """
    Add a new symbol mapping.
    
    Args:
        symbol (str): The symbol to add
        text_representation (str): The text representation of the symbol
        text_after (bool): If True, the text will be placed after the number
                           (e.g., for currencies in Turkish)
    """
    SYMBOL_MAPPINGS[symbol] = (text_representation, text_after)
