import csv
import argparse
import time
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import sqlite3
import hashlib
import transformers
from concurrent.futures import ThreadPoolExecutor
import threading
from transformers import AutoTokenizer
import signal

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.environ.get("deepseek_api_key")
if not api_key:
    raise ValueError("API key not found. Please set the 'deepseek_api_key' environment variable.")

# Use the API key when initializing the client
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

# Initialize SQLite cache
CACHE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deepseek_cache.db")

# Create a lock for SQLite connections
db_lock = threading.RLock()

# Initialize tokenizer
tokenizer_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deepseek_v3_tokenizer")
try:
    tokenizer = transformers.AutoTokenizer.from_pretrained(tokenizer_dir, trust_remote_code=True)
    print(f"Tokenizer loaded from {tokenizer_dir}")
except Exception as e:
    print(f"Error: Could not load tokenizer: {str(e)}")
    print(f"Please make sure the tokenizer files are available in {tokenizer_dir}")
    raise

# Maximum token limits for DeepSeek API (hard limits)
MAX_API_OUTPUT_TOKEN_LIMIT = 8192  # Maximum output tokens
MAX_API_INPUT_TOKEN_LIMIT = 65536  # Maximum input context tokens (64K)

def count_tokens(text):
    """Count the number of tokens in a text using DeepSeek tokenizer"""
    return len(tokenizer.encode(text))

def estimate_batch_tokens(prompt, batch):
    """Estimate the token count for a batch request"""
    # Count prompt tokens
    prompt_tokens = count_tokens(prompt)
    
    # Count batch content tokens
    batch_content = "\n\n".join([
        f"Pair {item['hash']}:\nReferans: {item['reference']}\nHipotez: {item['prediction']}"
        for item in batch
    ])
    batch_tokens = count_tokens(batch_content)
    
    # Estimate response tokens based on max length of reference/prediction
    # plus JSON formatting overhead (20%) and tolerance (10%)
    base_response_tokens = sum(
        max(count_tokens(item['reference']), count_tokens(item['prediction']))
        for item in batch
    )
    estimated_response_tokens = int(base_response_tokens * 1.2 * 1.1)  # JSON overhead * tolerance
    
    # Check if estimated response exceeds output limit
    if estimated_response_tokens > MAX_API_OUTPUT_TOKEN_LIMIT * 0.8:  # Using 80% of max as safety margin
        estimated_response_tokens = int(MAX_API_OUTPUT_TOKEN_LIMIT * 0.8)
    
    # Total tokens (input + output)
    total_tokens = prompt_tokens + batch_tokens + estimated_response_tokens
    
    return {
        "prompt_tokens": prompt_tokens,
        "batch_tokens": batch_tokens,
        "estimated_response_tokens": estimated_response_tokens,
        "total_tokens": total_tokens,
        "input_tokens": prompt_tokens + batch_tokens,
        "exceeds_input_limit": (prompt_tokens + batch_tokens) > MAX_API_INPUT_TOKEN_LIMIT,
        "exceeds_output_limit": estimated_response_tokens > MAX_API_OUTPUT_TOKEN_LIMIT
    }

def init_cache():
    """Initialize the SQLite cache database"""
    with db_lock:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS corrections (
            hash TEXT PRIMARY KEY,
            reference TEXT,
            prediction TEXT,
            correction TEXT,
            timestamp TEXT
        )
        ''')
        conn.commit()
        conn.close()
        print(f"Cache initialized at {CACHE_DB_PATH}")

def get_from_cache(hash_id, reference=None, prediction=None):
    """Get a correction from cache by hash_id"""
    with db_lock:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT correction FROM corrections WHERE hash = ?", (hash_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print(f"Cache hit for {hash_id}")
            return result[0]
        return None

def add_to_cache(hash_id, reference, prediction, correction):
    """Add a correction to the cache"""
    with db_lock:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT OR REPLACE INTO corrections (hash, reference, prediction, correction, timestamp) VALUES (?, ?, ?, ?, ?)",
            (hash_id, reference, prediction, correction, timestamp)
        )
        conn.commit()
        conn.close()

def read_prompt(prompt_file):
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()

def call_deepseek(prompt, reference, prediction):
    """Individual API call for a single pair"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Referans: {reference}\nHipotez: {prediction}"}
        ],
        temperature=0.7,
        **({"max_tokens": MAX_API_OUTPUT_TOKEN_LIMIT} if len(reference) > 1000 else {})
    )
    return response.choices[0].message.content

def batch_call_deepseek(prompt, batch):
    """Call DeepSeek API for a batch of corrections"""
    # Format the batch into a single message with hash identifiers
    batch_content = "\n\n".join([
        f"Pair {item['hash']}:\nReferans: {item['reference']}\nHipotez: {item['prediction']}"
        for item in batch
    ])
    
    # Combine prompt and batch content
    full_prompt = f"{prompt}\n\n{batch_content}"
    
    # Count tokens to decide if we need to set max_tokens
    input_tokens = count_tokens(full_prompt)
    
    # Estimate output tokens (typically similar to reference length)
    total_ref_tokens = sum(count_tokens(item['reference']) for item in batch)
    estimated_output_tokens = int(total_ref_tokens * 1.2)  # Add 20% buffer
    
    print(f"Batch API call - Input tokens: {input_tokens}, Estimated output tokens: {estimated_output_tokens}")
    
    # Only specify max_tokens if we expect a large output
    kwargs = {}
    if estimated_output_tokens > 1000:  # Only set for larger expected outputs
        kwargs["max_tokens"] = min(estimated_output_tokens, MAX_API_OUTPUT_TOKEN_LIMIT)
    
    # Make the API call with retries
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"Making API call (attempt {attempt+1}/{max_retries})...")
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": batch_content}
                ],
                temperature=0.0,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API error: {str(e)}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
    
    print(f"Error calling DeepSeek API after {max_retries} attempts")
    return None

def parse_batch_response(response_text, batch):
    """Parse the API response and match with original hashes"""
    print(f"Raw API response length: {len(response_text) if response_text else 0} characters")
    
    if not response_text:
        print("Empty response from API")
        return {}
    
    # Check for markdown code blocks and remove them if present
    lines = response_text.split('\n')
    if lines and lines[0].strip().startswith('```') and lines[-1].strip().startswith('```'):
        print("Detected markdown code blocks, removing them")
        response_text = '\n'.join(lines[1:-1])
    
    try:
        # Try to parse as JSON
        corrections = json.loads(response_text)
        print("Successfully parsed response as JSON")
        
        if isinstance(corrections, list):
            # Map corrections to hashes
            return {row['hash']: corrections[i] for i, row in enumerate(batch) if i < len(corrections)}
        elif isinstance(corrections, dict):
            # If it's a dictionary with hash keys, use it directly
            return corrections
    except json.JSONDecodeError:
        print("Response is not valid JSON")
        return {}

def create_dynamic_batches(rows, prompt, max_batch_tokens):
    """Create batches based on token count instead of fixed batch size"""
    batches = []
    current_batch = []
    current_batch_tokens = 0
    
    # Set safety margins to ensure we stay well below the maximum token limits
    safe_input_token_limit = min(max_batch_tokens, MAX_API_INPUT_TOKEN_LIMIT * 0.8)  # 80% of max input tokens for safety
    safe_output_token_limit = MAX_API_OUTPUT_TOKEN_LIMIT * 0.8  # 80% of max output tokens for safety
    
    # Count prompt tokens once instead of repeatedly
    prompt_tokens = count_tokens(prompt)
    
    # Calculate how many tokens are available for the batch content
    available_tokens = safe_input_token_limit - prompt_tokens
    
    # Threshold for what's considered a "large" row (50% of available tokens)
    large_row_threshold = available_tokens * 0.5
    
    for row in rows:
        # Calculate tokens for this row
        row_text = f"Pair {row['hash']}:\nReferans: {row['reference']}\nHipotez: {row['prediction']}\n\n"
        row_tokens = count_tokens(row_text)
        estimated_response_tokens = int(row_tokens * 1.25)  # Estimate response tokens
        
        # Check if adding this row would exceed our safe limits
        new_batch_tokens = current_batch_tokens + row_tokens
        new_estimated_response = int(new_batch_tokens * 1.25)
        
        # Check both input and output limits
        input_limit_exceeded = (prompt_tokens + new_batch_tokens) > safe_input_token_limit
        output_limit_exceeded = new_estimated_response > safe_output_token_limit
        
        # If either limit would be exceeded, start a new batch
        if (current_batch and (input_limit_exceeded or output_limit_exceeded)):
            batches.append(current_batch)
            current_batch = []
            current_batch_tokens = 0
        
        # Handle case where a single row exceeds limits or is very large
        if not current_batch and (row_tokens > large_row_threshold):
            print(f"Warning: Row with hash {row['hash']} is very large ({row_tokens} tokens). Processing in a separate batch.")
            # Still add it to its own batch - the API will handle truncation if needed
            batches.append([row])
            continue
        
        # Add row to current batch
        current_batch.append(row)
        current_batch_tokens += row_tokens
    
    # Add the last batch if it's not empty
    if current_batch:
        batches.append(current_batch)
    
    return batches

# Global flag for graceful shutdown
shutdown_flag = threading.Event()

def signal_handler(signum, frame):
    """Handle interrupt signal"""
    print("\nShutdown requested. Waiting for running tasks to complete...")
    shutdown_flag.set()

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def process_batch(batch, json_prompt):
    """Process a single batch in a separate thread"""
    if shutdown_flag.is_set():
        print("Shutdown requested, skipping batch")
        return []
    
    # Check if any rows in the batch are already in the cache
    batch_to_process = []
    processed_rows = []
    
    for row in batch:
        if shutdown_flag.is_set():
            print("Shutdown requested, stopping batch processing")
            break
        
        # Create a new row based on the template
        processed_row = new_row_template.copy()
        
        # Copy fields from input row
        processed_row['hash'] = row['hash']
        processed_row['reference'] = row['reference']
        processed_row['prediction'] = row['prediction']
        
        # Copy metrics if they exist
        for field in ['wer', 'cer']:
            if field in row:
                processed_row[field] = row[field]
        
        # Handle cosine similarity field which might have different names
        if 'cosSim' in row:
            processed_row['cosSim'] = row['cosSim']
        elif 'cosine_similarity' in row:
            processed_row['cosSim'] = row['cosine_similarity']
        
        # Check cache with thread-safe access
        if cached_correction := get_from_cache(row["hash"], row["reference"], row["prediction"]):
            processed_row["corrected_reference"] = cached_correction
        else:
            batch_to_process.append(row)
            
        processed_rows.append(processed_row)
    
    if not batch_to_process or shutdown_flag.is_set():
        return processed_rows  # All rows were in cache or shutdown requested
    
    # Calculate token usage for this batch
    token_info = estimate_batch_tokens(json_prompt, batch_to_process)
    print(f"Batch size: {len(batch_to_process)}, Input tokens: {token_info['input_tokens']}, "
          f"Estimated response tokens: {token_info['estimated_response_tokens']}")
    
    # Call the API
    response = batch_call_deepseek(json_prompt, batch_to_process)
    if not response:
        print(f"Failed to get response for batch of {len(batch_to_process)} rows")
        # Mark uncorrected rows
        for row in processed_rows:
            if row["corrected_reference"] is None:
                row["corrected_reference"] = "-missing-correction-"
        return processed_rows
    
    # Parse the response
    corrections = parse_batch_response(response, batch_to_process)
    
    # Update processed rows with corrections and cache them
    for row in batch_to_process:
        hash_id = row["hash"]
        if hash_id in corrections:
            correction = corrections[hash_id]
            
            # Find the corresponding processed row
            for processed_row in processed_rows:
                if processed_row["hash"] == hash_id:
                    processed_row["corrected_reference"] = correction
                    break
            
            # Cache the correction with thread-safe access
            add_to_cache(hash_id, row["reference"], row["prediction"], correction)
    
    # Ensure all rows have a correction (even if it's just a placeholder)
    for row in processed_rows:
        if row["corrected_reference"] is None:
            row["corrected_reference"] = "-missing-correction-"
    
    return processed_rows

new_row_template = {
    'hash': None,
    'wer': None,
    'cer': None,
    'cosSim': None,
    'reference': None,
    'corrected_reference': None,
    'prediction': None,
}

def single_correction(reference, prediction, prompt_file=None):
    """Get a single correction without using the batch process"""
    if not prompt_file:
        prompt_file = os.path.join(os.path.dirname(__file__), "deepseek_prompt.md")
    
    prompt = read_prompt(prompt_file)
    
    # Count tokens to decide if we need to set max_tokens
    ref_tokens = count_tokens(reference)
    pred_tokens = count_tokens(prediction)
    prompt_tokens = count_tokens(prompt)
    
    # Estimate output tokens (typically similar to reference length)
    estimated_output_tokens = int(ref_tokens * 1.2)  # Add 20% buffer
    
    print(f"Input tokens: {prompt_tokens + ref_tokens + pred_tokens}, Estimated output tokens: {estimated_output_tokens}")
    
    # Only specify max_tokens if we expect a large output
    kwargs = {}
    if estimated_output_tokens > 1000:  # Only set for larger expected outputs
        kwargs["max_tokens"] = min(estimated_output_tokens, MAX_API_OUTPUT_TOKEN_LIMIT)
    
    try:
        return call_deepseek(prompt, reference, prediction)
    except Exception as e:
        print(f"Error calling DeepSeek API: {str(e)}")
        return None

def configure_sqlite_for_concurrency():
    """Configure SQLite for better concurrency"""
    with db_lock:
        conn = sqlite3.connect(CACHE_DB_PATH)
        conn.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging for better concurrency
        conn.execute("PRAGMA synchronous = NORMAL")  # Faster with reasonable safety
        conn.execute("PRAGMA cache_size = 10000")  # Larger cache for better performance
        conn.commit()
        conn.close()

def main():
    """Main function"""
    global tokenizer
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process CSV file with DeepSeek API')
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--output', help='Output CSV file (default: input_corrected.csv)')
    parser.add_argument('--batch_size', type=int, default=10, help='Batch size (default: 10)')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of rows to process (default: 0 = all)')
    parser.add_argument('--skip_cache', action='store_true', help='Skip cache lookup')
    parser.add_argument('--token_based_batching', action='store_true', help='Use token-based batching instead of fixed batch size')
    parser.add_argument('--max_batch_tokens', type=int, default=32000, help='Maximum tokens per batch for token-based batching (default: 32000)')
    parser.add_argument('--workers', type=int, default=4, help='Number of worker threads (default: 4)')
    args = parser.parse_args()
    
    # Set output file name if not provided
    if not args.output:
        input_path = Path(args.input)
        args.output = str(input_path.with_name(f"{input_path.stem}_corrected{input_path.suffix}"))
    
    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer_path = os.path.join(os.path.dirname(__file__), "deepseek_v3_tokenizer")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    
    # Initialize cache
    init_cache()
    
    # Read input CSV
    rows = []
    with open(args.input, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            if args.limit > 0 and len(rows) >= args.limit:
                break
    
    print(f"Processing {len(rows)} rows")
    
    # Load base prompt and JSON format prompt
    base_prompt_path = os.path.join(os.path.dirname(__file__), "deepseek_prompt.md")
    json_prompt_path = os.path.join(os.path.dirname(__file__), "deepseek_json_prompt.md")
    
    with open(base_prompt_path, 'r', encoding='utf-8') as f:
        base_prompt = f.read()
    
    with open(json_prompt_path, 'r', encoding='utf-8') as f:
        json_format = f.read()
    
    # Combine prompts
    full_prompt = base_prompt + "\n\n" + json_format
    
    # Create batches
    if args.token_based_batching:
        batches = create_dynamic_batches(rows, full_prompt, args.max_batch_tokens)
        print(f"Created {len(batches)} dynamic batches based on token count")
    else:
        batches = [rows[i:i+args.batch_size] for i in range(0, len(rows), args.batch_size)]
        print(f"Created {len(batches)} fixed-size batches")
    
    # Process batches in parallel
    corrected_rows = []
    
    print(f"Processing batches with {args.workers} workers")
    print("Press Ctrl+C to gracefully stop processing...")
    
    # Configure SQLite for better concurrency
    configure_sqlite_for_concurrency()
    
    try:
        # Create a thread pool and process batches in parallel
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            # Submit all batches to the executor
            futures = [executor.submit(process_batch, batch, full_prompt) for batch in batches]
            
            # Process results as they complete
            total_batches = len(futures)
            
            for i, future in enumerate(futures):
                if shutdown_flag.is_set():
                    # Cancel any pending futures
                    for f in futures[i:]:
                        f.cancel()
                    break
                
                try:
                    batch_results = future.result()
                    corrected_rows.extend(batch_results)
                    print(f"Completed {i+1}/{total_batches} batches ({(i+1)/total_batches:.1%})")
                except Exception as e:
                    print(f"Error processing batch: {str(e)}")
    except KeyboardInterrupt:
        print("\nInterrupt received, waiting for running tasks to complete...")
    finally:
        # Write output CSV with whatever results we have
        if corrected_rows:
            print(f"\nWriting {len(corrected_rows)} rows to {args.output}")
            with open(args.output, 'w', newline='', encoding='utf-8') as f:
                fieldnames = list(new_row_template.keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(corrected_rows)
            print("Output file written successfully")
        else:
            print("\nNo results to write")

if __name__ == "__main__":
    main()
