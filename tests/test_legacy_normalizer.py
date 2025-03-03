"""
Tests for the legacy normalizer module.
"""

import pytest
from trnorm.legacy_normalizer import normalize_text, turkish_lower, replace_hatted_characters

def test_normalize_text_basic():
    """Test basic normalization functionality."""
    assert normalize_text("Hello World") == "hello world"
    assert normalize_text("Merhaba Dünya") == "merhaba dünya"
    assert normalize_text("İstanbul") == "istanbul"

def test_normalize_text_with_special_chars():
    """Test normalization with special characters."""
    assert normalize_text("Türkçe'de 'tırnak' işaretleri") == "türkçede tırnak işaretleri"
    assert normalize_text('Türkçe"de "tırnak" işaretleri') == "türkçede tırnak işaretleri"

def test_normalize_text_with_hatted_chars():
    """Test normalization with hatted characters."""
    # The hatted characters are replaced with their non-hatted equivalents
    assert normalize_text("Kâğıt, Âdem, Îmân") == "kağıt adem ıman"

def test_normalize_text_with_non_turkish_chars():
    """Test normalization with non-Turkish characters."""
    assert normalize_text("123") == "123"  # Original returned since normalized is empty
    assert normalize_text("!@#") == "!@#"  # Original returned since normalized is empty

def test_normalize_text_with_mixed_content():
    """Test normalization with mixed content."""
    assert normalize_text("İstanbul'da 2023 yılında!") == "istanbulda yılında"

def test_normalize_text_with_empty_string():
    """Test normalization with empty string."""
    assert normalize_text("") == ""

def test_normalize_text_with_only_spaces():
    """Test normalization with only spaces."""
    assert normalize_text("   ") == "   "  # Original returned since normalized is empty

def test_normalize_text_with_list():
    """Test normalization with a list of strings."""
    input_list = ["Merhaba", "Dünya", "İstanbul'da", "123"]
    expected = ["merhaba", "dünya", "istanbulda", "123"]
    assert normalize_text(input_list) == expected

def test_turkish_lower():
    """Test Turkish lowercase conversion."""
    assert turkish_lower("İIŞĞÜÖÇ") == "iışğüöç"
    # Turkish I (without dot) is lowercase of I (with dot)
    assert turkish_lower("ISTANBUL") == "ıstanbul"
    assert turkish_lower("İSTANBUL") == "istanbul"

def test_replace_hatted_characters():
    """Test replacing hatted characters."""
    assert replace_hatted_characters("Kâğıt") == "Kağıt"
    assert replace_hatted_characters("Âdem") == "Adem"
    assert replace_hatted_characters("Îmân") == "Iman"

def test_edge_case_non_latin_script():
    """Test edge case with non-Latin script."""
    japanese_text = "こんにちは世界"
    assert normalize_text(japanese_text) == japanese_text  # Should return original

def test_edge_case_mixed_scripts():
    """Test edge case with mixed scripts."""
    mixed_text = "Hello こんにちは İstanbul"
    # After normalization, only Latin Turkish chars remain, others are replaced with spaces
    assert normalize_text(mixed_text) == "hello istanbul"
