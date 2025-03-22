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
from concurrent.futures import ThreadPoolExecutor, as_completed
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
                temperature=1.0,
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
    
    # Set safety margins - only for input tokens since we want to use full max_batch_tokens for output
    safe_input_token_limit = MAX_API_INPUT_TOKEN_LIMIT * 0.8  # 80% of max input tokens for safety
    safe_output_token_limit = max_batch_tokens  # Use the full max_batch_tokens parameter
    
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
        
        # Get estimated response tokens using the same logic as estimate_batch_tokens
        row_response_tokens = max(count_tokens(row['reference']), count_tokens(row['prediction']))
        row_response_tokens = int(row_response_tokens * 1.2 * 1.1)  # JSON overhead * tolerance
        
        # Calculate new totals if we add this row
        new_batch_tokens = current_batch_tokens + row_tokens
        new_response_tokens = sum(
            max(count_tokens(r['reference']), count_tokens(r['prediction']))
            for r in current_batch + [row]
        )
        new_response_tokens = int(new_response_tokens * 1.2 * 1.1)  # JSON overhead * tolerance
        
        # Check both input and output limits
        input_limit_exceeded = (prompt_tokens + new_batch_tokens) > safe_input_token_limit
        output_limit_exceeded = new_response_tokens > safe_output_token_limit
        
        # If either limit would be exceeded, start a new batch
        if (current_batch and (input_limit_exceeded or output_limit_exceeded)):
            batches.append(current_batch)
            current_batch = []
            current_batch_tokens = 0
            new_response_tokens = row_response_tokens
        
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
        return None
    
    try:
        # Estimate tokens for this batch
        token_info = estimate_batch_tokens(json_prompt, batch)
        print(f"Batch size: {len(batch)}, Input tokens: {token_info['input_tokens']}, Estimated response tokens: {token_info['estimated_response_tokens']}")
        
        # Check if we exceed token limits
        if token_info['exceeds_input_limit']:
            print(f"Warning: Batch exceeds input token limit ({token_info['input_tokens']} tokens)")
            return None
        
        if token_info['exceeds_output_limit']:
            print(f"Warning: Batch may exceed output token limit ({token_info['estimated_response_tokens']} tokens)")
        
        # Check cache first
        cached_results = {}
        for item in batch:
            if cached := get_from_cache(item['hash'], item['reference'], item['prediction']):
                cached_results[item['hash']] = cached
        
        # If all items are cached, return early
        if len(cached_results) == len(batch):
            return [{**item, 'correction': cached_results[item['hash']]} for item in batch]
        
        # Filter out cached items from the batch
        uncached_batch = [item for item in batch if item['hash'] not in cached_results]
        
        # Make API call for uncached items
        if not (response := batch_call_deepseek(json_prompt, uncached_batch)):
            return None
        
        # Parse response and update cache
        if corrections := parse_batch_response(response, uncached_batch):
            # Add new corrections to cache
            for item in uncached_batch:
                if item['hash'] in corrections:
                    add_to_cache(item['hash'], item['reference'], item['prediction'], corrections[item['hash']])
            
            # Combine cached and new results
            results = []
            for item in batch:
                if correction := (cached_results.get(item['hash']) or corrections.get(item['hash'])):
                    results.append({**item, 'correction': correction})
            
            return results
        
    except Exception as e:
        print(f"Error processing batch: {str(e)}")
        return None

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
    
    # Limit max workers to avoid system overload
    args.workers = min(args.workers, 16)
    
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
    configure_sqlite_for_concurrency()
    
    # Read input CSV
    print("Reading input CSV...")
    rows = []
    with open(args.input, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            if args.limit > 0 and len(rows) >= args.limit:
                break
    
    total_rows = len(rows)
    print(f"Processing {total_rows} rows")
    
    # Filter out cached items first
    if not args.skip_cache:
        print("Checking cache for existing corrections...")
        uncached_rows = []
        cached_rows = []
        for i, row in enumerate(rows):
            if i % 1000 == 0:
                print(f"Checking cache: {i}/{total_rows} rows")
            cached_result = get_from_cache(row['hash'], row['reference'], row['prediction'])
            if cached_result:
                cached_rows.append({**row, 'correction': cached_result})
            else:
                uncached_rows.append(row)
        
        print(f"Found {len(cached_rows)} cached corrections, {len(uncached_rows)} rows need processing")
        rows = uncached_rows
    
    if not rows:
        print("All rows are already in cache. Writing output file...")
        with open(args.output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(cached_rows[0].keys()))
            writer.writeheader()
            writer.writerows(cached_rows)
        print("Output file written successfully")
        return
    
    # Load base prompt and JSON format prompt
    base_prompt_path = os.path.join(os.path.dirname(__file__), "deepseek_prompt.md")
    json_prompt_path = os.path.join(os.path.dirname(__file__), "deepseek_json_prompt.md")
    
    with open(base_prompt_path, 'r', encoding='utf-8') as f:
        base_prompt = f.read()
    
    with open(json_prompt_path, 'r', encoding='utf-8') as f:
        json_format = f.read()
    
    # Combine prompts
    full_prompt = base_prompt + "\n\n" + json_format
    
    # Create batches with progress reporting
    print("Creating batches...")
    if args.token_based_batching:
        batches = create_dynamic_batches(rows, full_prompt, args.max_batch_tokens)
        print(f"Created {len(batches)} dynamic batches based on token count")
    else:
        batches = [rows[i:i+args.batch_size] for i in range(0, len(rows), args.batch_size)]
        print(f"Created {len(batches)} fixed-size batches")
    
    # Process batches in parallel with reasonable thread count
    corrected_rows = []
    
    print(f"Processing batches with {args.workers} workers")
    print("Press Ctrl+C to gracefully stop processing...")
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submit all tasks with timeout
        future_to_batch = {
            executor.submit(process_batch, batch, full_prompt): batch 
            for batch in batches
        }
        
        try:
            for future in as_completed(future_to_batch, timeout=300):  # 5 minute timeout per batch
                batch = future_to_batch[future]
                try:
                    results = future.result(timeout=300)  # 5 minute timeout for getting results
                    if results:
                        corrected_rows.extend(results)
                except TimeoutError:
                    print(f"Timeout processing batch of {len(batch)} rows")
                except Exception as e:
                    print(f"Error processing batch: {str(e)}")
                
                if shutdown_flag.is_set():
                    break
                
                # Report progress
                print(f"Completed {len(corrected_rows)}/{total_rows} rows ({len(corrected_rows)/total_rows*100:.1f}%)")
        
        except TimeoutError:
            print("Processing timeout reached")
        except KeyboardInterrupt:
            print("\nShutdown requested. Waiting for running tasks to complete...")
            shutdown_flag.set()
            executor.shutdown(wait=True, cancel_futures=True)
    
    # Combine cached and new results
    if not args.skip_cache:
        corrected_rows.extend(cached_rows)
    
    # Write output file
    print(f"Writing {len(corrected_rows)} rows to {args.output}")
    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(corrected_rows[0].keys()))
        writer.writeheader()
        writer.writerows(corrected_rows)
    print("Output file written successfully")

if __name__ == "__main__":
    main()
