# DeepSeek Batch Processing Script (v2) Documentation

## Overview
This script (`scripts/deepseek_batch_v2.py`) processes CSV files containing Automatic Speech Recognition (ASR) reference-prediction pairs through the DeepSeek Chat API (`deepseek-chat` model). It operates in batches for efficiency, utilizes a local SQLite cache to avoid redundant API calls, handles concurrent processing using multiple threads, and provides robust logging and error handling. The primary goal is to generate corrected reference texts based on detailed rules provided in prompt files.

## Key Features

### Core Functionality
- **Batch API Calls**: Submits multiple reference/prediction pairs (default: 10) in a single API request.
- **Detailed Correction Task**: Instructs the LLM (via `deepseek_prompt.md`) to perform alignment fixes, Turkish language corrections, localization, stopword preservation, and identify mismatched labels ("Hatalı etiketleme").
- **JSON Response Format**: Explicitly requests and parses JSON output from the API (`{"corrections": ["correction1", ...]}`) as defined in `deepseek_json_prompt.md`.
- **SQLite Caching**: Stores successful API results in a local database (`deepseek_cache_v2.db`) keyed by the unique input `hash` to prevent reprocessing. Cache lookups can be optionally skipped.
- **Concurrency Support**: Uses Python's `ThreadPoolExecutor` to process multiple batches in parallel across specified worker threads (default: 4), with thread-safe database access (using locks and WAL mode).

### Input/Output
- **Input CSV Requirements**:
  - Format: Comma-separated, UTF-8 encoding (assumed `quoting=csv.QUOTE_ALL`).
  - Required Columns: `reference` (original reference), `prediction` (ASR hypothesis), `hash` (unique identifier, must be pre-calculated). Rows missing these or with empty `prediction` are skipped.
- **Output CSV**:
  - Naming: `[input_filename]_corrected.csv` by default.
  - Contains all original input columns plus a new `correction` column holding the LLM's output.
- **Cache Database**: `scripts/deepseek_cache_v2.db` is created/updated in the script's directory.
- **Log Files**: Raw API prompts and responses are saved to timestamped files in the `scripts/deepseek_logs/` directory for debugging.

### Performance & Robustness
- **Token Management**: Uses a Hugging Face tokenizer (`scripts/deepseek_v3_tokenizer/`) to count input tokens against API limits (`MAX_API_INPUT_TOKEN_LIMIT`). Estimates output tokens to potentially set `max_tokens` API parameter.
- **Error Handling & Retries**: Implements retries with exponential backoff for transient API errors. Handles JSON parsing errors and mismatches between batch size and response length gracefully (skips affected batch).
- **Concurrency Configuration**: Configures SQLite for concurrent access using Write-Ahead Logging (WAL), increased cache size, and busy timeout.
- **Graceful Shutdown**: Responds to `Ctrl+C` (SIGINT) and `SIGTERM` signals to stop submitting new tasks and attempt to wait for running threads.
- **Progress Reporting**: Displays the percentage of rows completed during processing.

## Workflow

1.  **Initialization**:
    *   Parse command-line arguments.
    *   Load DeepSeek API key from `.env` file.
    *   Load Hugging Face tokenizer from `scripts/deepseek_v3_tokenizer/`.
    *   Initialize SQLite cache (`deepseek_cache_v2.db`) and configure it for concurrency (WAL mode).
    *   Load system prompts (`deepseek_prompt.md`, `deepseek_json_prompt.md`).
    *   Register signal handlers for graceful shutdown.
2.  **Input Processing**:
    *   Read input CSV specified by `--input`.
    *   Validate required columns (`reference`, `prediction`, `hash`) and skip invalid rows.
    *   Apply row limit if specified (`--limit`).
3.  **Batch Creation**:
    *   Group the valid input rows into batches of the specified size (`--batch_size`).
4.  **Parallel Batch Processing**:
    *   Use `ThreadPoolExecutor` with specified `--workers`.
    *   For each batch (run in a separate thread via `process_batch`):
        *   Check cache for each item's `hash` (unless `--skip_cache`).
        *   If items remain uncached:
            *   Construct the API request content.
            *   Check input token count against limits.
            *   Call the DeepSeek API (`batch_call_deepseek`) requesting JSON output, with retries.
            *   Log raw prompt and response to `deepseek_logs/`.
            *   Parse the JSON response (`parse_batch_response`).
            *   **Validate** that the number of corrections in the response matches the number of items sent in the API call for that batch. Skip batch on mismatch.
            *   Add successfully parsed new corrections to the SQLite cache (`add_to_cache`).
        *   Combine cached results and new API results for the batch.
    *   Collect results from all successfully processed batches.
5.  **Output Generation**:
    *   Combine results from all batches.
    *   Write the combined data (including original columns and the new `correction` column) to the output CSV file specified by `--output`.

## Command Line Arguments
```bash
usage: deepseek_batch_v2.py [-h] --input INPUT [--output OUTPUT] [--batch_size BATCH_SIZE] [--limit LIMIT] [--skip_cache] [--workers WORKERS]

Process CSV file with DeepSeek API in batches using caching and concurrency.

options:
  -h, --help            show this help message and exit
  --input INPUT         Path to the input CSV file. (required)
  --output OUTPUT       Path to the output CSV file (default: [input]_corrected.csv)
  --batch_size BATCH_SIZE
                        Number of items per API batch request. (default: 10)
  --limit LIMIT         Maximum number of valid rows to process from input (0 = process all). (default: 0)
  --skip_cache          Force API calls by skipping cache lookup. (default: False)
  --workers WORKERS     Number of parallel worker threads for processing batches. (default: 4)
```


## Critical Components & Notes

### Must Maintain
- **Input CSV Format**: Requires `reference`, `prediction`, `hash` columns. Assumes UTF-8, comma-separated, quoted fields.
- **Prompt Files**: Relies on `scripts/deepseek_prompt.md` and `scripts/deepseek_json_prompt.md` being present and correctly formatted.
- **Tokenizer**: Requires the tokenizer files in `scripts/deepseek_v3_tokenizer/`.
- **Cache Integrity**: The `hash` column is crucial for cache lookups; ensure input hashes are unique and stable.
- **JSON Validation**: The check matching the number of corrections in the response to the batch size is critical to prevent data misalignment.
- **Concurrency Safety**: SQLite configuration (WAL mode) and lock usage are essential for stability with multiple workers.
- **API Key**: Requires `deepseek_api_key` in a `.env` file accessible to the script.
- **Token Limits**: Adherence to `MAX_API_INPUT_TOKEN_LIMIT` prevents API errors.

### Potential Issues
- **API Rate Limits**: High worker counts or small batches might hit API rate limits (not explicitly handled beyond retries).
- **Tokenizer Mismatches**: Using a tokenizer different from the one DeepSeek uses internally could lead to inaccurate token counts.
- **Large Rows/Batches**: Very long reference/prediction texts could exceed token limits even with small batch sizes.
- **Invalid API Responses**: Non-JSON or malformed JSON responses (despite requesting JSON) will cause batches to fail.

## Version History

### v2.0 (This Version)
- **Batching**: Optimized for batch API calls expecting structured JSON responses.
- **Caching**: Implemented robust SQLite caching with concurrency support (WAL).
- **Concurrency**: Added multi-threading using `ThreadPoolExecutor`.
- **Token Counting**: Integrated Hugging Face tokenizer for input token validation.
- **Logging**: Added detailed logging for raw API prompts and responses.
- **Error Handling**: Improved validation of API responses (JSON structure, length match) and added graceful shutdown.
- **Dependencies**: Added `transformers` and `python-dotenv`.

### v1.0 (Implied Previous Version)
- Likely processed items individually or had less robust batching/caching/error handling.

