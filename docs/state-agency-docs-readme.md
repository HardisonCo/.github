# State Agency Documentation Generator

This document provides instructions for generating documentation structures for US state agencies.

## Overview

The HMS-DOC project includes tools to:

1. Split the main `us.state.agencies.json` file into individual state files
2. Generate documentation structures for state agencies following the HMS component pattern
3. Verify that all agencies are properly included

## Available Scripts

The following scripts are available to help automate documentation generation:

### 1. Split State Agencies JSON

```bash
python3 split_state_agencies.py <input_json_file> <output_directory>
```

This script splits the main US state agencies JSON file into separate files for each state.

### 2. Verify State Split

```bash
python3 verify_state_split.py <original_json_file> <split_files_directory>
```

This script verifies that all states from the original file were extracted correctly.

### 3. Generate State Documentation

```bash
python3 generate_state_docs.py <state_json_file> <output_directory>
```

This script generates a documentation structure for a specific state's agencies.

### 4. All-in-One Processing Script

```bash
./process_state_agencies.sh
```

This script processes all states by:
1. Splitting the main JSON file
2. Verifying the split
3. Setting up documentation structure for Tennessee

### 5. Generate Documentation for a Specific State

```bash
./generate_state_agency_docs.sh <state_name>
```

Example:
```bash
./generate_state_agency_docs.sh california
```

This script generates documentation for a specific state's agencies.

## Documentation Structure

The generated documentation follows this structure:

```
state_code/                 # e.g., TN for Tennessee
├── README.md               # State overview
├── agency_label/           # e.g., TN_DOT
│   ├── README.md           # Agency overview
│   ├── HMS-A2A/            # HMS component directories
│   │   └── index.md
│   ├── HMS-ACH/
│   │   └── index.md
│   ├── ...
│   └── HMS-UTL/
│       └── index.md
├── another_agency/
│   └── ...
└── ...
```

## Next Steps

After generating the documentation structure:

1. Fill in the placeholder content in each `index.md` file with actual documentation
2. Update agency README files with specific information about each agency
3. Customize documentation based on agency-specific requirements
4. Add code samples, diagrams, and other supporting materials

## Troubleshooting

If you encounter issues:

1. Ensure the input JSON file is valid and follows the expected structure
2. Verify that output directories exist and are writable
3. Check for duplicate agency labels within the same state
4. Ensure Python 3.6+ is being used

For more information, refer to the HMS Documentation Guide.