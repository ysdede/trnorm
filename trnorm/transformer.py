"""
Turkish Text Transformer

This module provides a flexible transformer-based approach to Turkish text normalization.
It allows users to specify which transformers to apply and in what order.
"""

from typing import List, Union, Callable, Optional, Dict, Any

from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.ordinals import normalize_ordinals
from trnorm.roman_numerals import roman_to_arabic, find_roman_ordinals
from trnorm.symbols import convert_symbols
from trnorm.legacy_normalizer import normalize_text, replace_hatted_characters
from trnorm.text_utils import turkish_lower, sapkasiz
from trnorm.dimension_utils import preprocess_dimensions, normalize_dimensions
from trnorm.unit_utils import normalize_units


# Type definition for a transformer function
TransformerFunc = Callable[[str], str]


class Transformer:
    """
    A class that represents a single text transformation step.
    
    Each transformer has a name, a function that performs the transformation,
    and optional parameters that can be passed to the function.
    """
    
    def __init__(self, name: str, func: TransformerFunc, description: str, **kwargs):
        """
        Initialize a transformer.
        
        Args:
            name (str): The name of the transformer
            func (TransformerFunc): The function that performs the transformation
            description (str): A brief description of what the transformer does
            **kwargs: Additional parameters to pass to the transformation function
        """
        self.name = name
        self.func = func
        self.description = description
        self.kwargs = kwargs
    
    def __call__(self, text: str) -> str:
        """
        Apply the transformation to the input text.
        
        Args:
            text (str): The input text to transform
            
        Returns:
            str: The transformed text
        """
        return self.func(text, **self.kwargs)
    
    def __repr__(self) -> str:
        """Return a string representation of the transformer."""
        return f"Transformer(name='{self.name}', description='{self.description}')"


# Define all available transformers
AVAILABLE_TRANSFORMERS: Dict[str, Transformer] = {
    "preprocess_dimensions": Transformer(
        name="preprocess_dimensions",
        func=preprocess_dimensions,
        description="Add spaces between numbers and multiplication symbols"
    ),
    "convert_symbols": Transformer(
        name="convert_symbols",
        func=convert_symbols,
        description="Convert symbols (%, $, etc.) to their text representation"
    ),
    "normalize_dimensions": Transformer(
        name="normalize_dimensions",
        func=normalize_dimensions,
        description="Replace multiplication symbol 'x' with 'çarpı' in dimensions"
    ),
    "convert_numbers": Transformer(
        name="convert_numbers",
        func=convert_numbers_to_words_wrapper,
        description="Convert numbers to their text representation"
    ),
    "normalize_ordinals": Transformer(
        name="normalize_ordinals",
        func=normalize_ordinals,
        description="Convert ordinal numbers (1., 2., etc.) to their text representation"
    ),
    "normalize_units": Transformer(
        name="normalize_units",
        func=normalize_units,
        description="Convert unit abbreviations (cm, kg, etc.) to their full text"
    ),
    "lowercase": Transformer(
        name="lowercase",
        func=turkish_lower,
        description="Convert text to lowercase using Turkish-specific rules"
    ),
    "remove_hats": Transformer(
        name="remove_hats",
        func=replace_hatted_characters,
        description="Remove circumflex (hat) from Turkish characters"
    ),
    "legacy_normalize": Transformer(
        name="legacy_normalize",
        func=normalize_text,
        description="Apply legacy normalization (more aggressive, removes punctuation)"
    )
}


# Default transformer pipeline
DEFAULT_TRANSFORMER_PIPELINE = [
    "preprocess_dimensions",
    "convert_symbols",
    "normalize_dimensions",
    "convert_numbers",
    "normalize_ordinals",
    "normalize_units",
    "remove_hats",
    "lowercase"
]


class TransformerPipeline:
    """
    A pipeline of transformers that can be applied to text in sequence.
    
    This class allows users to create a custom pipeline of transformers
    and apply them to text in a specific order.
    """
    
    def __init__(self, transformers: Optional[List[str]] = None):
        """
        Initialize a transformer pipeline.
        
        Args:
            transformers (Optional[List[str]]): A list of transformer names to include in the pipeline.
                If None, the default pipeline will be used.
        """
        if transformers is None:
            transformers = DEFAULT_TRANSFORMER_PIPELINE
        
        self.transformers = []
        for transformer_name in transformers:
            if transformer_name in AVAILABLE_TRANSFORMERS:
                self.transformers.append(AVAILABLE_TRANSFORMERS[transformer_name])
            else:
                raise ValueError(f"Unknown transformer: {transformer_name}")
    
    def apply(self, text: Union[str, List[str]]) -> Union[str, List[str]]:
        """
        Apply all transformers in the pipeline to the input text.
        
        Args:
            text (Union[str, List[str]]): The input text or list of texts to transform
            
        Returns:
            Union[str, List[str]]: The transformed text or list of transformed texts
        """
        # Handle list input
        if isinstance(text, list):
            return [self.apply(item) for item in text]
        
        # Apply transformers in sequence
        result = text
        for transformer in self.transformers:
            result = transformer(result)
        
        return result
    
    def __repr__(self) -> str:
        """Return a string representation of the transformer pipeline."""
        return f"TransformerPipeline(transformers={[t.name for t in self.transformers]})"


def transform(text: Union[str, List[str]], transformers: Optional[List[str]] = None) -> Union[str, List[str]]:
    """
    Transform text using a pipeline of transformers.
    
    This is a convenience function that creates a TransformerPipeline and applies it to the input text.
    
    Args:
        text (Union[str, List[str]]): The input text or list of texts to transform
        transformers (Optional[List[str]]): A list of transformer names to include in the pipeline.
            If None, the default pipeline will be used.
            
    Returns:
        Union[str, List[str]]: The transformed text or list of transformed texts
    """
    pipeline = TransformerPipeline(transformers)
    return pipeline.apply(text)


def get_available_transformers() -> Dict[str, str]:
    """
    Get a dictionary of all available transformers and their descriptions.
    
    Returns:
        Dict[str, str]: A dictionary mapping transformer names to their descriptions
    """
    return {name: transformer.description for name, transformer in AVAILABLE_TRANSFORMERS.items()}


def create_custom_transformer(name: str, func: TransformerFunc, description: str, **kwargs) -> Transformer:
    """
    Create a custom transformer that can be added to the pipeline.
    
    Args:
        name (str): The name of the transformer
        func (TransformerFunc): The function that performs the transformation
        description (str): A brief description of what the transformer does
        **kwargs: Additional parameters to pass to the transformation function
        
    Returns:
        Transformer: A new transformer instance
    """
    transformer = Transformer(name, func, description, **kwargs)
    return transformer


def register_transformer(transformer: Transformer) -> None:
    """
    Register a custom transformer so it can be used in transformer pipelines.
    
    Args:
        transformer (Transformer): The transformer to register
    """
    AVAILABLE_TRANSFORMERS[transformer.name] = transformer
