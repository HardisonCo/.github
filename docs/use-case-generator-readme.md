# HMS Use Case Generator

A powerful tool for generating and enhancing all possible combinations of agency use cases.

## Quick Start

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the generator with default settings (100 combinations, 100 threads)
./batch_generate_all_use_cases.sh

# Run with integration to documentation
./batch_generate_all_use_cases.sh --integrate

# Run with pipeline integration
./batch_generate_all_use_cases.sh --pipeline

# Run with custom settings
./batch_generate_all_use_cases.sh --max-combinations 200 --threads 50
```

## Features

- Generates combinations of agencies, topics, sub-components, states, countries, and collaborations
- Enhances use cases with real-world issues using the issue finder
- Integrates with HMS-NFO data for context-aware enhancement
- Processes combinations in parallel with multi-threading
- Integrates with HMS-DOC pipeline

## Command-Line Options

### Batch Script

```
Usage: ./batch_generate_all_use_cases.sh [OPTIONS]

Options:
  --max-combinations NUM   Number of combinations to process (default: 100)
  --threads NUM            Number of threads to use (default: 100)
  --output DIR             Output directory (default: enhanced_agency_use_cases)
  --nfo-dir DIR            HMS-NFO directory (default: /Users/arionhardison/Desktop/CodifyHQ/HMS-NFO)
  --integrate              Integrate use cases into documentation
  --pipeline               Integrate with HMS-DOC pipeline
  --help                   Show this help message
```

### Python Script

```
usage: generate_all_use_case_combinations.py [-h] [-o OUTPUT] [-m MAX_COMBINATIONS] [-i] [-p] [-t THREADS] [-v]

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Directory to store enhanced use cases
  -m MAX_COMBINATIONS, --max-combinations MAX_COMBINATIONS
                        Maximum number of combinations to process
  -i, --integrate       Integrate enhanced use cases into the documentation
  -p, --pipeline        Integrate with HMS-DOC pipeline
  -t THREADS, --threads THREADS
                        Number of threads to use for parallel processing
  -v, --verbose         Enable verbose logging
```

## Troubleshooting

If you encounter issues:

1. Check if the virtual environment is activated
2. Verify the HMS-NFO directory path is correct
3. Review the logs for detailed error messages
4. Try reducing the number of threads or combinations

## Common Examples

```bash
# Generate a small test batch
./batch_generate_all_use_cases.sh --max-combinations 10 --threads 5

# Full production run with pipeline integration
./batch_generate_all_use_cases.sh --max-combinations 300 --integrate --pipeline

# Generate use cases for a custom NFO directory
./batch_generate_all_use_cases.sh --nfo-dir /custom/path/to/hms-nfo

# Generate and save to a specific output directory
./batch_generate_all_use_cases.sh --output /path/to/output/directory
```

## Output

The generator produces:

- Enhanced use cases in markdown format
- NFO data files in JSON format
- Summary statistics in JSON format
- Detailed logs of the process

## Further Information

For complete documentation and specifications, see:

- `USE_CASE_GENERATOR_SPEC.md` - Detailed technical specification
- `enhance_agency_use_cases_with_issues.py` - Issue finder documentation
- `run_hms_doc_pipeline.py` - Pipeline integration documentation