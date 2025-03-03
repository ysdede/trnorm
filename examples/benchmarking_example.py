"""
Example of how to use the transformer-based approach for benchmarking.

This script demonstrates how to use the transformer-based approach to normalize Turkish text
for benchmarking ASR systems.
"""

import sys
import os
import time
from typing import List, Dict, Any

# Add the parent directory to the path to import the trnorm package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trnorm import (
    transform,
    TransformerPipeline,
    get_available_transformers,
    create_custom_transformer,
    register_transformer,
    DEFAULT_TRANSFORMER_PIPELINE,
    wer,
    cer
)

# Example ASR benchmark data (reference, hypothesis pairs)
benchmark_data = [
    (
        "Bugün 15. kattaki 3 toplantıya katıldım.",
        "bugün on beşinci kattaki üç toplantıya katıldım"
    ),
    (
        "Saat 14:30'da %25 indirimli ürünler satışa çıkacak.",
        "saat on dört otuzda yüzde yirmi beş indirimli ürünler satışa çıkacak"
    ),
    (
        "II. Dünya Savaşı 1939-1945 yılları arasında gerçekleşti.",
        "ikinci dünya savaşı bin dokuz yüz otuz dokuz bin dokuz yüz kırk beş yılları arasında gerçekleşti"
    ),
    (
        "Ürün fiyatı 1.250,75 TL'dir.",
        "ürün fiyatı bin iki yüz elli virgül yetmiş beş türk lirası dır"
    ),
    (
        "Dün 3x4 metre halı aldım.",
        "dün üç çarpı dört metre halı aldım"
    ),
    (
        "Âlim insanlar bilgilerini paylaşır.",
        "alim insanlar bilgilerini paylaşır"
    ),
    (
        "Odanın boyutları 2x3x4 metre.",
        "odanın boyutları iki çarpı üç çarpı dört metre"
    ),
    (
        "Ağırlığı 5 kg. ve uzunluğu 10 metre.",
        "ağırlığı beş kilogram ve uzunluğu on metre"
    ),
]

def run_benchmark(data: List[tuple], pipeline: List[str] = None) -> Dict[str, Any]:
    """
    Run a benchmark on the given data using the specified transformer pipeline.
    
    Args:
        data: List of (reference, hypothesis) pairs
        pipeline: List of transformer names to use (or None for default)
        
    Returns:
        Dict with benchmark results (WER, CER, time)
    """
    start_time = time.time()
    
    # Create a transformer pipeline
    if pipeline is None:
        pipeline = DEFAULT_TRANSFORMER_PIPELINE
    
    # Process each pair
    normalized_pairs = []
    for reference, hypothesis in data:
        normalized_reference = transform(reference, transformers=pipeline)
        normalized_hypothesis = transform(hypothesis, transformers=pipeline)
        normalized_pairs.append((normalized_reference, normalized_hypothesis))
    
    # Calculate metrics
    total_wer = 0
    total_cer = 0
    
    for normalized_reference, normalized_hypothesis in normalized_pairs:
        total_wer += wer(normalized_reference, normalized_hypothesis)
        total_cer += cer(normalized_reference, normalized_hypothesis)
    
    avg_wer = total_wer / len(data) if data else 0
    avg_cer = total_cer / len(data) if data else 0
    
    end_time = time.time()
    
    return {
        "wer": avg_wer,
        "cer": avg_cer,
        "time": end_time - start_time,
        "normalized_pairs": normalized_pairs
    }

# Print available transformers
print("Available transformers:")
for name, description in get_available_transformers().items():
    print(f"  - {name}: {description}")

print("\n" + "-" * 50 + "\n")

# Run benchmark with different transformer pipelines
pipelines = {
    "Default": DEFAULT_TRANSFORMER_PIPELINE,
    "Minimal": ["lowercase"],
    "No Units": ["preprocess_dimensions", "convert_symbols", "normalize_dimensions", 
                "convert_numbers", "normalize_ordinals", "lowercase"],
    "No Dimensions": ["convert_symbols", "convert_numbers", "normalize_ordinals", 
                     "normalize_units", "lowercase"],
    "Custom Order": ["lowercase", "convert_numbers", "normalize_ordinals", 
                    "normalize_dimensions", "normalize_units"],
}

results = {}
for name, pipeline in pipelines.items():
    print(f"Running benchmark with {name} pipeline:")
    print(f"  Pipeline: {pipeline}")
    
    results[name] = run_benchmark(benchmark_data, pipeline)
    
    print(f"  WER: {results[name]['wer']:.4f}")
    print(f"  CER: {results[name]['cer']:.4f}")
    print(f"  Time: {results[name]['time']:.4f} seconds")
    
    # Show a few examples
    print("\n  Examples:")
    for i, ((ref, hyp), (norm_ref, norm_hyp)) in enumerate(zip(benchmark_data[:3], 
                                                             results[name]["normalized_pairs"][:3])):
        print(f"    Original Reference: {ref}")
        print(f"    Normalized Reference: {norm_ref}")
        print(f"    Original Hypothesis: {hyp}")
        print(f"    Normalized Hypothesis: {norm_hyp}")
        print(f"    WER: {wer(norm_ref, norm_hyp):.4f}")
        print()
    
    print("-" * 50 + "\n")

# Compare results
print("Benchmark Results Summary:")
print(f"{'Pipeline':<15} {'WER':<10} {'CER':<10} {'Time (s)':<10}")
print("-" * 45)
for name, result in results.items():
    print(f"{name:<15} {result['wer']:<10.4f} {result['cer']:<10.4f} {result['time']:<10.4f}")

# Create a custom transformer for benchmarking
print("\n" + "-" * 50 + "\n")
print("Creating a custom transformer for benchmarking:")

def remove_punctuation(text):
    """Remove all punctuation from text."""
    import re
    return re.sub(r'[^\w\s]', '', text)

# Create and register the custom transformer
punctuation_transformer = create_custom_transformer(
    name="remove_punctuation",
    func=remove_punctuation,
    description="Remove all punctuation from text"
)
register_transformer(punctuation_transformer)

# Create a custom pipeline with the new transformer
custom_pipeline = [
    "preprocess_dimensions",
    "convert_symbols",
    "normalize_dimensions",
    "convert_numbers",
    "normalize_ordinals",
    "normalize_units",
    "lowercase",
    "remove_punctuation"
]

print(f"Running benchmark with custom pipeline including punctuation removal:")
print(f"  Pipeline: {custom_pipeline}")

custom_results = run_benchmark(benchmark_data, custom_pipeline)

print(f"  WER: {custom_results['wer']:.4f}")
print(f"  CER: {custom_results['cer']:.4f}")
print(f"  Time: {custom_results['time']:.4f} seconds")

# Show a few examples
print("\n  Examples:")
for i, ((ref, hyp), (norm_ref, norm_hyp)) in enumerate(zip(benchmark_data[:3], 
                                                         custom_results["normalized_pairs"][:3])):
    print(f"    Original Reference: {ref}")
    print(f"    Normalized Reference: {norm_ref}")
    print(f"    Original Hypothesis: {hyp}")
    print(f"    Normalized Hypothesis: {norm_hyp}")
    print(f"    WER: {wer(norm_ref, norm_hyp):.4f}")
    print()

print("\nThis example demonstrates how to use the transformer-based approach for benchmarking ASR systems.")
print("You can create custom transformer pipelines to suit your specific benchmarking needs.")
print("The flexible architecture allows you to add, remove, or reorder transformers as needed.")
