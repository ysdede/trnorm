"""
Configuration file for pytest.

This file is automatically loaded by pytest and can be used to define fixtures,
hooks, and other test configuration.
"""

import sys
import os

# Add the parent directory to the Python path to allow importing modules from the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
