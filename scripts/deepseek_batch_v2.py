# scripts/deepseek_batch_v2.py

"""
Processes ASR reference/prediction pairs in batches using the DeepSeek API.

This script takes a CSV file containing Automatic Speech Recognition (ASR) results
(specifically 'reference', 'prediction', and 'hash' columns) and utilizes the
DeepSeek Chat API ('deepseek-chat' model) to generate corrected versions of the
'reference' text. It operates in batches for efficiency and leverages several
advanced features:

1.  **Batch API Calls:** Submits multiple reference/prediction pairs in a single
    API request to reduce overhead. The specific correction task for the LLM is
    defined in 'scripts/deepseek_prompt.md', covering alignment fixes (using the
    prediction as context), Turkish language/spelling/punctuation corrections,
    localization rules, stopword preservation, and identification of completely
    mismatched labels ("Hatalı etiketleme").
2.  **JSON Output Format:** Instructs the API (via 'scripts/deepseek_json_prompt.md')
    to return results for the batch in a structured JSON format:
    `{"corrections": ["correction_for_item1", "correction_for_item2", ...]}`.
    The script validates this structure and ensures the number of corrections
    matches the batch size to prevent data misalignment.
3.  **SQLite Caching:** Maintains a local SQLite database ('deepseek_cache_v2.db')
    to store successfully obtained corrections, keyed by the input row's 'hash'.
    This prevents redundant API calls for previously processed items, saving time
    and cost. The cache is configured for concurrent access (WAL mode).
4.  **Concurrency:** Uses a ThreadPoolExecutor to process multiple batches in
    parallel, significantly speeding up execution for large datasets. Database
    access is managed with locks for thread safety.
5.  **Token Management:** Employs a Hugging Face tokenizer ('deepseek_v3_tokenizer')
    to count input tokens before sending requests, ensuring they stay within the
    API's limits (MAX_API_INPUT_TOKEN_LIMIT). It also estimates potential output
    token usage to potentially adjust API call parameters (`max_tokens`).
6.  **Robust Logging & Error Handling:**
    - Logs the exact prompt sent to the API and the raw JSON response received
      to timestamped files within the 'deepseek_logs' directory for debugging.
    - Implements retries with exponential backoff for transient API errors.
    - Handles JSON parsing errors and mismatches in response lengths gracefully,
      typically by skipping the affected batch.
    - Supports graceful shutdown via SIGINT/SIGTERM signals.

The final output is a new CSV file containing all original columns plus the
LLM-generated 'correction' for each row, sourced either from the API call
during the run or retrieved from the cache.

Input Data Requirements:
    - Command-line arguments: --input (required), --output (optional),
      --batch_size (default 10), --limit (optional), --skip_cache (optional),
      --workers (default 4).
    - Input CSV format: Comma-separated (assuming all quoted), UTF-8 encoding.
    - Required Input Columns: 'reference', 'prediction', 'hash' (must be unique
      and pre-calculated).
    - File System:
        - Prompt file: 'scripts/deepseek_prompt.md' (defines correction rules).
        - JSON format prompt file: 'scripts/deepseek_json_prompt.md'.
        - Tokenizer files: Must exist in 'scripts/deepseek_v3_tokenizer/'.
    - Environment: A '.env' file with 'deepseek_api_key' variable.

Output Data:
    - Primary Output: A new CSV file (e.g., 'input_file_corrected.csv') in the
      same directory as the input, containing original columns plus the
      'correction' column.
    - Cache Database: 'scripts/deepseek_cache_v2.db' is created/updated.
    - Log Files: Raw prompt and response text files are stored in
      'scripts/deepseek_logs/'.
"""

import os
import csv
import json
import time
import sqlite3
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from openai import OpenAI
from transformers import AutoTokenizer
import signal
import datetime

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.environ.get("deepseek_api_key")
if not api_key:
    raise ValueError("API key not found. Please set the 'deepseek_api_key' environment variable.")

# Use the API key when initializing the client
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

# Initialize SQLite cache
CACHE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deepseek_cache_v2.db")

# Create a lock for SQLite connections
db_lock = threading.RLock()

# Create logs directory for storing raw prompts and responses
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deepseek_logs")
os.makedirs(LOGS_DIR, exist_ok=True)

def save_to_log_file(content, prefix, batch_id=None):
    """Save content to a log file with timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_suffix = f"_batch{batch_id}" if batch_id is not None else ""
    filename = f"{prefix}_{timestamp}{batch_suffix}.txt"
    filepath = os.path.join(LOGS_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Saved {prefix} to {filepath}")
    return filepath

# Initialize tokenizer
tokenizer_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deepseek_v3_tokenizer")
try:
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
except Exception as e:
    print(f"Error loading tokenizer: {str(e)}")
    raise

# Flag for graceful shutdown
shutdown_flag = threading.Event()

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print("\nShutdown requested. Waiting for running tasks to complete...")
    shutdown_flag.set()

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Constants
MAX_API_OUTPUT_TOKEN_LIMIT = 8192  # Maximum output tokens
MAX_API_INPUT_TOKEN_LIMIT = 65536  # Maximum input context tokens (64K)

def count_tokens(text):
    """Count the number of tokens in a text using DeepSeek tokenizer"""
    return len(tokenizer.encode(text))

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

def configure_sqlite_for_concurrency():
    """Configure SQLite for better concurrency with multiple threads"""
    with db_lock:
        conn = sqlite3.connect(CACHE_DB_PATH)
        # Use Write-Ahead Logging for better concurrency
        conn.execute("PRAGMA journal_mode = WAL")
        # Balance between safety and performance
        conn.execute("PRAGMA synchronous = NORMAL")
        # Increase cache size for better performance
        conn.execute("PRAGMA cache_size = 10000")
        # Set busy timeout to wait instead of failing immediately
        conn.execute("PRAGMA busy_timeout = 5000")
        conn.commit()
        conn.close()
        print("SQLite configured for concurrent access")

def get_from_cache(hash_key, reference, prediction):
    """Get a correction from the cache"""
    with db_lock:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT correction FROM corrections WHERE hash = ?", (hash_key,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return None

def add_to_cache(hash_key, reference, prediction, correction):
    """Add a correction to the cache"""
    with db_lock:
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT OR REPLACE INTO corrections (hash, reference, prediction, correction, timestamp) VALUES (?, ?, ?, ?, ?)",
            (hash_key, reference, prediction, correction, timestamp)
        )
        conn.commit()
        conn.close()

def batch_call_deepseek(prompt, batch, batch_id=None):
    """Call DeepSeek API for a batch of corrections"""
    # Format the batch into a single message without hash identifiers
    batch_content = "\n\n".join([
        f"Referans: {item['reference']}\nHipotez: {item['prediction']}"
        for item in batch
    ])
    
    # Combine prompt and batch content
    full_prompt = f"{prompt}\n\n{batch_content}"
    
    # Save the prompt to a log file
    save_to_log_file(full_prompt, "prompt", batch_id)
    
    # Count tokens to decide if we need to set max_tokens
    input_tokens = count_tokens(full_prompt)
    
    # Estimate output tokens based on max(reference, prediction) plus JSON skeleton
    max_text_tokens = sum(
        max(count_tokens(item['reference']), count_tokens(item['prediction'])) 
        for item in batch
    )
    # Calculate JSON skeleton tokens (base JSON structure + batch size overhead)
    json_skeleton = '{"corrections":[' + ','.join(['""'] * len(batch)) + ']}'
    skeleton_tokens = count_tokens(json_skeleton)

    estimated_output_tokens = int((max_text_tokens + skeleton_tokens) * 1.02)
    
    print(f"Batch API call - Input tokens: {input_tokens}, Estimated output tokens: {estimated_output_tokens}")
    
    # Only specify max_tokens if we expect a large output
    kwargs = {}
    if estimated_output_tokens > 4000:  # Only set for larger expected outputs
        kwargs["max_tokens"] = MAX_API_OUTPUT_TOKEN_LIMIT
    elif estimated_output_tokens > 8192:
        print("Estimated output tokens exceed API limit. Skipping batch.")
        return None
    
    # Add response_format parameter for JSON output
    kwargs["response_format"] = {"type": "json_object"}
    
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
            response_content = response.choices[0].message.content
            
            # Save the response to a log file
            save_to_log_file(response_content, "response", batch_id)
            
            return response_content
        except Exception as e:
            print(f"API error: {str(e)}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
    
    print(f"Error calling DeepSeek API after {max_retries} attempts")
    return None

def parse_batch_response(response_text, batch):
    """Parse the API response and match with original references"""
    # print(f"Raw API response length: {len(response_text) if response_text else 0} characters")
    
    if not response_text:
        print("Empty response from API")
        return {}
    
    try:
        # Parse the JSON response
        json_data = json.loads(response_text)
        
        # Calculate response token count
        response_tokens = len(tokenizer.encode(response_text))
        print(f"Response token count: {response_tokens}")
        
        result = {}
        
        # Check if the response has a 'corrections' array
        if 'corrections' in json_data and isinstance(json_data['corrections'], list):
            corrections = json_data['corrections']
            
            # Skip the entire batch if number of corrections doesn't match number of inputs
            if len(corrections) != len(batch):
                print(f"Warning: Number of corrections ({len(corrections)}) doesn't match batch size ({len(batch)}). Skipping batch to prevent mismatches.")
                return {}
            
            # Match corrections with batch items by position
            for i, correction in enumerate(corrections):
                if i < len(batch):
                    # Store the correction with the hash as the key for database compatibility
                    result[batch[i]['hash']] = correction
        else:
            print("Warning: Response does not contain a 'corrections' array")
            return {}
        
        # Check for missing corrections
        if missing := [item['hash'] for item in batch if item['hash'] not in result]:
            print(f"Warning: Missing corrections for {len(missing)} items")
            
        return result
            
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {str(e)}")
        print("Response is not valid JSON")
        return {}

def process_batch(batch, json_prompt, batch_id=None):
    """Process a single batch in a separate thread"""
    if shutdown_flag.is_set():
        return None
    
    try:
        # Calculate token sizes
        batch_content = "\n\n".join([
            f"Referans: {item['reference']}\nHipotez: {item['prediction']}"
            for item in batch
        ])
        
        prompt_tokens = count_tokens(json_prompt)
        batch_tokens = count_tokens(batch_content)
        total_tokens = prompt_tokens + batch_tokens
        
        print(f"Batch {batch_id}: {len(batch)} items, Prompt tokens: {prompt_tokens}, Content tokens: {batch_tokens}, Total input tokens: {total_tokens}")
        
        # Check if we exceed token limits
        if total_tokens > MAX_API_INPUT_TOKEN_LIMIT:
            print(f"Warning: Batch {batch_id} exceeds input token limit ({total_tokens} tokens)")
            return None
        
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
        if not (response := batch_call_deepseek(json_prompt, uncached_batch, batch_id)):
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
        print(f"Error processing batch {batch_id}: {str(e)}")
        return None

def write_output_csv(output_path, rows):
    """Write rows to output CSV with standardized fieldnames"""
    fieldnames = ['wer', 'cer', 'cosine_similarity', 'reference', 'correction', 'prediction', 'hash']
    # Drop fields not in fieldnames
    filtered_rows = [{k: v for k, v in row.items() if k in fieldnames} for row in rows]
    print(f"Writing {len(filtered_rows)} rows to {output_path}")
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

def read_input_csv(file_path, limit=0):
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get('prediction', '').strip():
                continue
            rows.append(row)
            if limit > 0 and len(rows) >= limit:
                break
    return rows

def load_prompt_file(filename):
    """Load a prompt file from the scripts directory"""
    prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

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
    parser.add_argument('--workers', type=int, default=4, help='Number of worker threads (default: 4)')
    args = parser.parse_args()
    
    # Initialize cache
    init_cache()
    
    # Configure SQLite for concurrent access
    configure_sqlite_for_concurrency()
    
    # Set output file if not specified
    if not args.output:
        base_name = os.path.basename(args.input)
        name, ext = os.path.splitext(base_name)
        args.output = os.path.join(os.path.dirname(args.input), f"{name}_corrected{ext}")
    
    # Read input CSV
    print("Reading input CSV...")
    rows = read_input_csv(args.input, args.limit)
    print(f"Processing {len(rows)} rows")
    
    # Check cache for existing corrections
    print("Checking cache for existing corrections...")
    cached_rows = []
    rows_to_process = []
    
    if not args.skip_cache:
        for i, row in enumerate(rows):
            if i % 10 == 0:
                print(f"Checking cache: {i}/{len(rows)} rows")
            
            # Get the hash from the row (already calculated in input file)
            hash_key = row.get('hash')
            reference = row.get('reference', '').strip()
            prediction = row.get('prediction', '').strip()
            
            if not hash_key or not reference or not prediction:
                continue
            
            # Check if correction exists in cache
            if correction := get_from_cache(hash_key, reference, prediction):
                # Add correction to row
                row['correction'] = correction
                cached_rows.append(row)
            else:
                rows_to_process.append(row)
    else:
        # Skip cache lookup, process all rows
        for row in rows:
            # Get the hash from the row (already calculated in input file)
            hash_key = row.get('hash')
            reference = row.get('reference', '').strip()
            prediction = row.get('prediction', '').strip()
            
            if not hash_key or not reference or not prediction:
                continue
            
            rows_to_process.append(row)
    
    print(f"Found {len(cached_rows)} cached corrections, {len(rows_to_process)} rows need processing")
    
    if not rows_to_process:
        print("All rows are already in cache, writing output...")
        write_output_csv(args.output, cached_rows)
        print(f"Wrote {len(cached_rows)} rows to {args.output}")
        return
    
    json_prompt = load_prompt_file("deepseek_json_prompt.md")
    base_prompt = load_prompt_file("deepseek_prompt.md")

    full_prompt = f"{base_prompt}\n\n{json_prompt}"
    
    # Create fixed-size batches
    print(f"Creating batches with fixed size of {args.batch_size}...")
    batches = []
    current_batch = []
    
    for row in rows_to_process:
        current_batch.append(row)
        
        if len(current_batch) >= args.batch_size:
            batches.append(current_batch)
            current_batch = []
    
    # Add any remaining items as the last batch
    if current_batch:
        batches.append(current_batch)
    
    print(f"Created {len(batches)} fixed-size batches")
    
    # Process batches in parallel with reasonable thread count
    corrected_rows = []
    
    print(f"Processing batches with {args.workers} workers")
    print("Press Ctrl+C to gracefully stop processing...")
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submit all tasks with timeout
        future_to_batch = {
            executor.submit(process_batch, batch, full_prompt, batch_idx): batch 
            for batch_idx, batch in enumerate(batches)
        }
        
        try:
            # Process results as they complete
            completed = 0
            for future in future_to_batch:
                if shutdown_flag.is_set():
                    break
                
                try:
                    if results := future.result():
                        corrected_rows.extend(results)
                        completed += len(results)
                        print(f"Completed {completed}/{len(rows_to_process)} rows ({completed/len(rows_to_process)*100:.1f}%)")
                except Exception as e:
                    print(f"Error processing batch: {str(e)}")
        finally:
            # Shutdown executor if interrupted
            if shutdown_flag.is_set():
                executor.shutdown(wait=False)
    
    # Combine cached and new results
    all_rows = cached_rows + corrected_rows
    write_output_csv(args.output, all_rows)
    print(f"Done! Processed {len(corrected_rows)} rows, {len(cached_rows)} from cache")

if __name__ == "__main__":
    main()
