"""
Module for handling special symbols in Turkish text normalization.

This module provides functions to convert special symbols like % (percent)
to their text representation in Turkish.
"""

import re
from trnorm.symbol_mappings import get_all_mappings, get_mapping, add_mapping


class SymbolConverter:
    """
    A class to convert special symbols to their text representation.
    
    This class can be extended to handle various symbols by adding new
    symbol-to-text mappings to the symbols_map dictionary.
    """
    
    def __init__(self, load_defaults=True):
        """
        Initialize the SymbolConverter with default symbol mappings.
        
        Args:
            load_defaults (bool): If True, load the default symbol mappings from symbol_mappings.py
        """
        # Dictionary mapping symbols to their text representation
        self.symbols_map = {}
        
        # Dictionary to track which symbols should have text placed after the number
        self.text_after_number = set()
        
        # Compile regex patterns for each symbol
        self.patterns = {}
        self.reverse_patterns = {}  # For symbols that appear after numbers (e.g., 500 $)
        
        # Load default mappings if requested
        if load_defaults:
            self.load_default_mappings()
    
    def load_default_mappings(self):
        """Load the default symbol mappings from symbol_mappings.py."""
        for symbol, (text_repr, text_after) in get_all_mappings().items():
            self.add_symbol_mapping(symbol, text_repr, text_after)
    
    def _compile_patterns(self, symbol):
        """
        Compile regex patterns for a symbol.
        
        Args:
            symbol (str): The symbol to compile patterns for
        """
        escaped_symbol = re.escape(symbol)
        
        # Pattern for symbol before number (e.g., $500)
        # Match: symbol + number + optional apostrophe with suffix
        self.patterns[symbol] = re.compile(
            rf'{escaped_symbol}(\d+(?:[.,]\d+)?)((\'[a-zA-ZçÇğĞıİöÖşŞüÜ]+)?)'
        )
        
        # Pattern for symbol after number (e.g., 500 $)
        # Match: number + optional apostrophe with suffix + symbol
        self.reverse_patterns[symbol] = re.compile(
            rf'(\d+(?:[.,]\d+)?)((\'[a-zA-ZçÇğĞıİöÖşŞüÜ]+)?)\s*{escaped_symbol}'
        )
    
    def add_symbol_mapping(self, symbol, text_representation, text_after=False):
        """
        Add a new symbol-to-text mapping.
        
        Args:
            symbol (str): The symbol to convert
            text_representation (str): The text representation of the symbol
            text_after (bool): If True, the text will be placed after the number
                               (e.g., for currencies in Turkish)
        """
        self.symbols_map[symbol] = text_representation
        if text_after:
            self.text_after_number.add(symbol)
            
        self._compile_patterns(symbol)
    
    def convert_symbol(self, text, symbol):
        """
        Convert a specific symbol in the text to its text representation.
        
        Args:
            text (str): The text to process
            symbol (str): The symbol to convert
            
        Returns:
            str: The processed text with the symbol converted to its text representation
        """
        if symbol not in self.symbols_map:
            return text
            
        text_repr = self.symbols_map[symbol]
        result = text
        
        # Handle symbol before number (e.g., $500)
        pattern = self.patterns[symbol]
        if symbol in self.text_after_number:
            # For currencies and other symbols that should have text after the number
            # Preserve any apostrophe and suffix
            result = pattern.sub(lambda m: m.group(1) + m.group(2) + ' ' + text_repr, result)
        else:
            # For symbols like percent that should have text before the number
            # Preserve any apostrophe and suffix
            result = pattern.sub(lambda m: text_repr + ' ' + m.group(1) + m.group(2), result)
        
        # Handle symbol after number (e.g., 500 $)
        reverse_pattern = self.reverse_patterns[symbol]
        # Preserve any apostrophe and suffix
        result = reverse_pattern.sub(lambda m: m.group(1) + m.group(2) + ' ' + text_repr, result)
        
        return result
    
    def convert_all_symbols(self, text):
        """
        Convert all known symbols in the text to their text representation.
        
        Args:
            text (str): The text to process
            
        Returns:
            str: The processed text with all known symbols converted to their text representation
        """
        result = text
        for symbol in self.symbols_map:
            result = self.convert_symbol(result, symbol)
        return result


# Create a default instance for easy import
default_converter = SymbolConverter()


def convert_symbols(text):
    """
    Convert all known symbols in the text to their text representation.
    
    This is a convenience function that uses the default SymbolConverter instance.
    
    Args:
        text (str): The text to process
        
    Returns:
        str: The processed text with all known symbols converted to their text representation
    """
    return default_converter.convert_all_symbols(text)


def add_symbol_mapping(symbol, text_representation, text_after=False):
    """
    Add a new symbol mapping to the default converter.
    
    This is a convenience function that adds a symbol mapping to the default
    SymbolConverter instance and also updates the symbol_mappings module.
    
    Args:
        symbol (str): The symbol to add
        text_representation (str): The text representation of the symbol
        text_after (bool): If True, the text will be placed after the number
                           (e.g., for currencies in Turkish)
    """
    default_converter.add_symbol_mapping(symbol, text_representation, text_after)
    # Also update the symbol_mappings module for persistence
    add_mapping(symbol, text_representation, text_after)
