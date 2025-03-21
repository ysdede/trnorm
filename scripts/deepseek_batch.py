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

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv('deepseek_api_key')
if not api_key:
    raise ValueError("deepseek_api_key not found in .env file")

# Use the API key when initializing the client
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

# Initialize SQLite cache
CACHE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deepseek_cache.db")

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
    batch_content = ""
    for item in batch:
        batch_content += f"{item['hash']}: {item['reference']}\n"
    batch_tokens = count_tokens(batch_content)
    
    # Estimate response tokens (roughly 25% of input tokens as a safety margin)
    # Each correction will be roughly similar in length to the original text
    estimated_response_tokens = int(batch_tokens * 1.25)
    
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

def call_deepseek(client, prompt, reference, prediction):
    """Individual API call for a single pair"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Referans: {reference}\nHipotez: {prediction}"}
        ],
        temperature=0.7,
        max_tokens=MAX_API_OUTPUT_TOKEN_LIMIT  # Set to maximum available output tokens
    )
    return response.choices[0].message.content

def batch_call_deepseek(client, prompt, batch):
    """Process multiple pairs in a single API call"""
    # Format the batch into a single message with hash identifiers
    batch_content = "\n\n".join([
        f"Pair {item['hash']}:\nReferans: {item['reference']}\nHipotez: {item['prediction']}"
        for item in batch
    ])
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Process these {len(batch)} pairs:\n{batch_content}"}
                ],
                temperature=0.7,
                max_tokens=MAX_API_OUTPUT_TOKEN_LIMIT  # Set to maximum available output tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"API error: {str(e)}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                raise

def parse_batch_response(response_text, batch):
    """Parse the API response and match with original hashes"""
    lines = response_text.split('\n')
    if lines[0] == "```json" and lines[-1] == "```":
        response_text = '\n'.join(lines[1:-1])
    try:
        corrections = json.loads(response_text, strict=False)
        if isinstance(corrections, list) and len(corrections) == len(batch):
            return {item['hash']: correction for item, correction in zip(batch, corrections)}
    except json.JSONDecodeError:
        print(f"Failed to parse JSON response: {response_text}")

    return None

def create_dynamic_batches(rows, prompt, max_batch_tokens):
    """Create batches based on token count instead of fixed batch size"""
    batches = []
    current_batch = []
    current_batch_tokens = 0
    
    # Set safety margins to ensure we stay well below the maximum token limits
    safe_input_token_limit = min(max_batch_tokens, MAX_API_INPUT_TOKEN_LIMIT * 0.8)  # 80% of max input tokens for safety
    safe_output_token_limit = MAX_API_OUTPUT_TOKEN_LIMIT * 0.8  # 80% of max output tokens for safety
    
    for row in rows:
        # Calculate tokens for this row
        row_tokens = count_tokens(f"{row['hash']}: {row['reference']}\n")
        estimated_response_tokens = int(row_tokens * 1.25)  # Estimate response tokens
        
        # Check if adding this row would exceed our safe limits
        new_batch_tokens = current_batch_tokens + row_tokens
        new_estimated_response = int(new_batch_tokens * 1.25)
        
        # Check both input and output limits
        input_limit_exceeded = (count_tokens(prompt) + new_batch_tokens) > safe_input_token_limit
        output_limit_exceeded = new_estimated_response > safe_output_token_limit
        
        # If either limit would be exceeded, start a new batch
        if (current_batch and (input_limit_exceeded or output_limit_exceeded)):
            batches.append(current_batch)
            current_batch = []
            current_batch_tokens = 0
        
        # Handle case where a single row exceeds limits
        if not current_batch and (input_limit_exceeded or output_limit_exceeded):
            print(f"Warning: Row with hash {row['hash']} exceeds safe token limits. Processing in a separate batch.")
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

new_row_template = {
    'hash': None,
    'wer': None,
    'cer': None,
    'cosSim': None,
    'reference': None,
    'corrected_reference': None,
    'prediction': None,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--output', help='Output CSV file (default: input_corrected.csv)')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of rows to process (0 for all)')
    parser.add_argument('--batch_size', type=int, default=5, help='Number of sentences to process in a batch')
    parser.add_argument('--max_batch_tokens', type=int, default=4096, 
                        help=f'Maximum token count for a batch (API limit is {MAX_API_INPUT_TOKEN_LIMIT})')
    parser.add_argument('--prompt', default='scripts/deepseek_prompt.md', help='Path to prompt file')
    parser.add_argument('--skip_cache', action='store_true', help='Skip using cache and force API calls')
    parser.add_argument('--token_based_batching', action='store_true', help='Use token count instead of fixed batch size')
    args = parser.parse_args()
    
    # Determine output file path
    if args.output:
        output_file = args.output
    else:
        input_path = Path(args.input)
        output_file = str(input_path.parent / f"{input_path.stem}_corrected{input_path.suffix}")
    
    # Read the input CSV file
    with open(args.input, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    
    # Limit rows if specified
    if args.limit > 0:
        rows = rows[:args.limit]
    
    # Read the base prompt and add JSON instructions for batch processing
    base_prompt = read_prompt(args.prompt)
    json_prompt = base_prompt + """

For batch processing, return corrections as a JSON array in order. Example:
["correction1", "correction2", ...]
"""
    
    print(f"Processing {len(rows)} rows")
    
    # Initialize cache if not skipping
    if not args.skip_cache:
        init_cache()
    
    corrected_rows = []
    
    if args.token_based_batching:
        batches = create_dynamic_batches(rows, json_prompt, args.max_batch_tokens)
        print(f"Created {len(batches)} dynamic batches")
    else:
        batches = [rows[i:i+args.batch_size] for i in range(0, len(rows), args.batch_size)]
        print(f"Created {len(batches)} fixed-size batches")
    
    for i, batch in enumerate(batches):
        batch_num = i+1
        total_batches = len(batches)
        print(f"Processing batch {batch_num}/{total_batches}")
        
        cached_corrections = {}
        batch_to_process = []
        
        # Check cache for each row in the batch
        if not args.skip_cache:
            for row in batch:
                if cached_correction := get_from_cache(row['hash'], row['reference'], row['prediction']):
                    cached_corrections[row['hash']] = cached_correction
                else:
                    batch_to_process.append(row)
        else:
            batch_to_process = batch
        
        # Process any rows not found in cache
        if batch_to_process:
            print(f"Making API call for {len(batch_to_process)} items not in cache")
            token_estimate = estimate_batch_tokens(json_prompt, batch_to_process)
            print("Token estimates:")
            print(f"  - Prompt: {token_estimate['prompt_tokens']} tokens")
            print(f"  - Batch content: {token_estimate['batch_tokens']} tokens")
            print(f"  - Estimated response: {token_estimate['estimated_response_tokens']} tokens")
            print(f"  - Total: {token_estimate['total_tokens']} tokens (API limit: {MAX_API_INPUT_TOKEN_LIMIT})")
            print(f"  - Input tokens: {token_estimate['input_tokens']} tokens")
            print(f"  - Exceeds input limit: {token_estimate['exceeds_input_limit']}")
            print(f"  - Exceeds output limit: {token_estimate['exceeds_output_limit']}")
            
            response = batch_call_deepseek(client, json_prompt, batch_to_process)
            new_corrections = parse_batch_response(response, batch_to_process)
            
            if new_corrections:
                # Add new corrections to cache and merge with cached results
                for idx, row in enumerate(batch_to_process):
                    hash_id = row['hash']
                    if hash_id in new_corrections:
                        correction = new_corrections[hash_id]
                        if not args.skip_cache:
                            add_to_cache(hash_id, row['reference'], row['prediction'], correction)
                        cached_corrections[hash_id] = correction
        
        # Create output rows
        for row in batch:
            corrected_row = new_row_template.copy()
            # Copy fields from input row
            corrected_row['hash'] = row['hash']
            corrected_row['reference'] = row['reference']
            corrected_row['prediction'] = row['prediction']
            
            # Copy metrics if they exist
            for field in ['wer', 'cer']:
                if field in row:
                    corrected_row[field] = row[field]
            
            # Handle cosine similarity field which might have different names
            if 'cosSim' in row:
                corrected_row['cosSim'] = row['cosSim']
            elif 'cosine_similarity' in row:
                corrected_row['cosSim'] = row['cosine_similarity']
            
            # Get correction
            hash_id = row['hash']
            corrected_reference = cached_corrections.get(hash_id, "-missing-correction-")
            corrected_row['corrected_reference'] = corrected_reference
            
            print(f"{hash_id}: {corrected_reference}")
            corrected_rows.append(corrected_row)
    
    # Write output CSV
    print(f"Writing {len(corrected_rows)} rows to {output_file}")
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(new_row_template.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(corrected_rows)
    
    print(f"Done! Output written to {output_file}")

if __name__ == "__main__":
    main()
