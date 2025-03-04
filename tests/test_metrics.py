#!/usr/bin/env python3
"""
Tests for the metrics module in trnorm package.
"""

import pytest
from trnorm.metrics import wer, cer, levenshtein_distance


def test_levenshtein_distance_strings():
    # Test with strings
    assert levenshtein_distance("kitten", "sitting") == 3
    assert levenshtein_distance("", "") == 0
    assert levenshtein_distance("abc", "") == 3
    assert levenshtein_distance("", "abc") == 3
    assert levenshtein_distance("abc", "abc") == 0
    assert levenshtein_distance("abc", "abd") == 1


def test_levenshtein_distance_lists():
    # Test with lists - the function now returns a list of individual distances
    assert levenshtein_distance(["a", "b", "c"], ["a", "b", "d"]) == [0, 0, 1]
    assert levenshtein_distance([], []) == []
    
    # These tests need to be updated as we now require lists to have the same length
    with pytest.raises(ValueError):
        levenshtein_distance(["a", "b", "c"], [])
    
    with pytest.raises(ValueError):
        levenshtein_distance([], ["a", "b", "c"])
    
    # Test with equal length lists
    assert levenshtein_distance(["a", "b", "c"], ["a", "b", "c"]) == [0, 0, 0]
    assert levenshtein_distance(["abc", "def"], ["abd", "def"]) == [1, 0]


def test_wer():
    # Test WER calculation
    assert wer("this is a test", "this is a test") == 0.0
    assert wer("this is a test", "this is test") == 0.25
    assert wer("this is a test", "this is a different test") == 0.25  # 1 substitution in 4 words
    assert wer("", "this is a test") == 1.0
    assert wer("this is a test", "") == 1.0


def test_cer():
    # Test CER calculation
    assert cer("this is a test", "this is a test") == 0.0
    assert cer("this is a test", "this is test") == 0.14285714285714285
    assert cer("this is a test", "this is a different test") == 0.7142857142857143  # 10 chars different out of 14
    assert cer("", "this is a test") == 1.0
    assert cer("this is a test", "") == 1.0


def test_turkish_examples():
    # Test with Turkish examples
    assert wer("bu bir test cümlesidir", "bu bir test cümlesi") == 0.25
    assert cer("otomatik konuşma tanıma", "otomotik konuşma tanımla") == 0.08695652173913043
    
    # Test with special Turkish characters
    assert levenshtein_distance("şöğüıçİ", "soguici") == 7  # Each Turkish character is different from its ASCII counterpart

    assert wer("Kafkas göçmenleriyse günlük tartışmalardan uzak.", "Kafkas göçmenleri ise günlük tartışmalardan uzak.") == 0.4
    assert cer("Kafkas göçmenleriyse günlük tartışmalardan uzak.", "Kafkas göçmenleri ise günlük tartışmalardan uzak.") == 0.041666666666666664