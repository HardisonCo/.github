# HMS Use Case Generator Specification

## Overview

The HMS Use Case Generator is a comprehensive system for generating and enhancing all possible combinations of use cases for government agencies, international bodies, state agencies, and cross-agency collaborations. It leverages the HMS-NFO data repository to provide context-aware enhancement and integrates with the HMS-DOC pipeline.

## Key Features

- **Comprehensive Combination Generation**: Creates use cases combining agencies, topics, sub-components, international entities, countries, states, and collaborations
- **Multi-threaded Processing**: Processes combinations in parallel using 100 threads by default
- **NFO Data Integration**: Gathers relevant data from HMS-NFO to enhance use cases
- **Pipeline Integration**: Integrates with HMS-DOC pipeline for documentation generation
- **Robust Error Handling**: Gracefully handles errors and continues processing

## System Components

### 1. Main Python Script: `generate_all_use_case_combinations.py`

This is the core script that:
- Generates all possible combinations of parameters
- Gathers NFO data for each combination
- Processes combinations in parallel using ThreadPoolExecutor
- Enhances use cases using the issue finder
- Integrates with the HMS-DOC pipeline

#### Key Functions:

- `generate_combination_list()`: Creates comprehensive list of parameter combinations
- `gather_nfo_data()`: Collects relevant data from HMS-NFO
- `enhance_use_case()`: Enhances a use case with real-world issues
- `integrate_enhanced_use_case()`: Integrates enhanced use cases into documentation
- `run_pipeline_integration()`: Integrates with HMS-DOC pipeline
- `process_combination()`: Processes a single combination in a thread
- `main()`: Orchestrates the entire process

### 2. Batch Script: `batch_generate_all_use_cases.sh`

This shell script:
- Provides a user-friendly interface for running the generator
- Handles environment setup and command-line arguments
- Activates the virtual environment
- Sets environment variables for NFO directory
- Runs the Python script with appropriate settings

### 3. Integration with HMS-DOC Pipeline

The system integrates with the existing HMS-DOC pipeline:
- Creates a configuration file for the pipeline
- Passes generated use cases to the pipeline
- Ensures documentation is updated with new use cases

## Command-Line Interface

### Python Script Arguments

```
usage: generate_all_use_case_combinations.py [-h] [-o OUTPUT] [-m MAX_COMBINATIONS] [-i] [-p] [-t THREADS] [-v]

Generate and enhance all possible use case combinations

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Directory to store enhanced use cases (default: enhanced_agency_use_cases)
  -m MAX_COMBINATIONS, --max-combinations MAX_COMBINATIONS
                        Maximum number of combinations to process (default: 100)
  -i, --integrate       Integrate enhanced use cases into the documentation (default: False)
  -p, --pipeline        Integrate with HMS-DOC pipeline (default: False)
  -t THREADS, --threads THREADS
                        Number of threads to use for parallel processing (default: 100)
  -v, --verbose         Enable verbose logging (default: False)
```

### Batch Script Arguments

```
Usage: ./batch_generate_all_use_cases.sh [OPTIONS]

Options:
  --max-combinations NUM   Number of combinations to process (default: 100)
  --threads NUM            Number of threads to use (default: 100)
  --output DIR             Output directory (default: enhanced_agency_use_cases)
  --nfo-dir DIR            HMS-NFO directory (default: /Users/arionhardison/Desktop/CodifyHQ/HMS-NFO)
  --integrate              Integrate use cases into documentation
  --pipeline               Integrate with HMS-DOC pipeline
  --agency-types LIST      Specific agency types to process (comma-separated)
  --topics LIST            Specific topics to process (comma-separated)
  --components LIST        Specific HMS components to include (comma-separated)
  --international          Include international agencies
  --state                  Include state-level agencies
  --cross-agency           Include cross-agency collaborations
  --verbose                Enable detailed logging
  --help                   Show this help message

Examples:
  # Generate all use case combinations with default settings
  ./batch_generate_all_use_cases.sh

  # Generate all combinations with specified maximum count
  ./batch_generate_all_use_cases.sh --max-combinations 200

  # Generate combinations with specific NFO data directory
  ./batch_generate_all_use_cases.sh --nfo-dir /path/to/hms-nfo

  # Generate combinations with more threads for parallel processing
  ./batch_generate_all_use_cases.sh --threads 50

  # Generate combinations and integrate with HMS-DOC pipeline
  ./batch_generate_all_use_cases.sh --pipeline

  # Generate combinations for specific agency types and topics
  ./batch_generate_all_use_cases.sh --agency-types education,healthcare --topics "distance learning,telemedicine"
```

## Parameter Combinations

The system generates combinations of the following parameters:

1. **Agency Codes**: Federal agencies from AGENCY_MAPPING
2. **Agency Types**: education, healthcare, finance, security, transportation, energy, agriculture, justice, general
3. **Topics**: Domain-specific topics from TOPICS dictionary
4. **State Variations**: Combinations with state agencies (e.g., "Michigan Department of Education")
5. **International Variations**: Combinations with international agencies (e.g., "Japan Health and Human Services")
6. **Cross-Agency Collaborations**: Combinations of multiple agencies
7. **Sub-Components**: Specific components within agencies
8. **Collaboration Types**: Various collaboration patterns between entities

## Integration with HMS-NFO

The system gathers data from HMS-NFO to enhance use cases:

1. **Agency Data**: Agency-specific information from agency directories
2. **Topic Data**: Domain knowledge related to the selected topic
3. **Documentation**: Existing documentation related to the agency and topic
4. **Sources**: References and sources for further information
5. **Real-World Issues**: Actual problems faced by agencies identified through web research
6. **Economic Context**: Industry-specific economic data, including trade statistics and market analysis
7. **Regulatory Framework**: Legal and policy constraints affecting the agency's operations
8. **Stakeholder Analysis**: Key stakeholders and their relationships with the agency

The HMS-NFO data is leveraged in several ways:
- **Pre-generation Analysis**: Assesses existing data to determine most relevant combinations
- **Issue Selection**: Identifies the most impactful real-world issues based on NFO data
- **Context Enrichment**: Adds domain-specific context to enhance use case relevance
- **Solution Targeting**: Ensures proposed HMS solutions target actual agency needs
- **Cross-referencing**: Links related use cases across agencies and components

## Enhancement Process

Each use case is enhanced using the following process:

1. **Parameter Generation**:
   - Generate comprehensive combination parameters
   - Evaluate combination relevance using HMS-NFO data
   - Filter out combinations with minimal real-world applicability

2. **Data Gathering**:
   - Retrieve agency-specific data from HMS-NFO
   - Gather domain knowledge from NFO repositories
   - Collect real-world issues through API-based web research
   - Analyze economic data related to the agency domain
   - Evaluate political and regulatory constraints

3. **Issue Structuring**:
   - Format discovered issues into structured problem statements
   - Categorize issues by stakeholders, severity, and timeline
   - Identify related issues across agencies for cross-integration
   - Map issues to specific HMS components for solution development

4. **Content Enhancement**:
   - Create initial use case structure with identified issues
   - Develop solution narratives using HMS components
   - Apply the abundance-based economic model to show value creation
   - Include implementation steps tailored to agency constraints
   - Add real-world metrics and KPIs for measuring success

5. **Documentation Integration**:
   - Integrate the enhanced use case into appropriate documentation paths
   - Create cross-references across related document sections
   - Apply consistent formatting and terminology
   - Generate navigational links to related resources
   - Update indexes and tables of contents

6. **Pipeline Integration**:
   - Update the HMS-DOC pipeline with new content
   - Trigger tutorial generation using enhanced content
   - Update symlinks to latest documentation versions
   - Generate component integration documentation
   - Create test files for verifying documentation accuracy

## Parallel Processing

The system uses ThreadPoolExecutor to process combinations in parallel:

1. Creates a pool of worker threads (default: 100)
2. Submits each combination as a task to the pool
3. Uses thread-safe counters to track progress
4. Collects results as tasks complete
5. Logs progress at regular intervals

## Error Handling

The system includes robust error handling:

1. Each combination is processed independently
2. Errors in one combination don't affect others
3. All errors are logged with detailed information
4. The process continues even if some combinations fail
5. A summary of successes and failures is provided at the end

## Output

The system produces the following outputs:

1. **Enhanced Use Cases**: Markdown files with enhanced use cases
2. **NFO Data Files**: JSON files containing the gathered NFO data
3. **Summary File**: JSON file with statistics about the generation process
4. **Log File**: Detailed log of the entire process
5. **Pipeline Configuration**: Configuration file for the HMS-DOC pipeline

## Running the System

### Basic Usage - Complete Generation

To generate all use case combinations with default settings:

```bash
./batch_generate_all_use_cases.sh
```

This command will:
- Generate up to 100 use case combinations
- Process combinations using 100 parallel threads
- Store enhanced use cases in `enhanced_agency_use_cases/`
- Use the default HMS-NFO directory
- Log basic progress information

### Advanced Usage - Customizing Parameters

For more control over the generation process:

```bash
./batch_generate_all_use_cases.sh --max-combinations 200 --threads 50 --integrate --pipeline --nfo-dir /path/to/hms-nfo --agency-types education,healthcare
```

This command will:
- Generate up to 200 use case combinations
- Process combinations using 50 parallel threads
- Integrate enhanced use cases into the documentation
- Update the HMS-DOC pipeline with new content
- Use a custom HMS-NFO directory
- Only process education and healthcare agency types

### Focused Generation - Specific Topics and Components

To generate use cases for specific topics and HMS components:

```bash
./batch_generate_all_use_cases.sh --topics "distance learning,healthcare access" --components "HMS-A2A,HMS-NFO,HMS-CDF"
```

This command will:
- Focus only on the specified topics
- Include only the specified HMS components
- Use default settings for other parameters

### Pipeline Integration - Documentation Flow

To generate use cases and integrate them with the complete HMS-DOC pipeline:

```bash
./batch_generate_all_use_cases.sh --pipeline
```

This command will:
- Generate use cases with default settings
- Integrate them into the HMS-DOC pipeline
- Trigger tutorial generation
- Update symlinks to latest documentation
- Generate component integration documentation

## Dependencies

### Software Dependencies
- Python 3.6+
- Virtual environment with required packages (see requirements.txt)
- HMS-NFO repository (for NFO data access)
- HMS-DOC pipeline (for documentation integration)

### API Keys
The following API keys are required and must be set as environment variables:
- `OPENAI_API_KEY`: For OpenAI GPT models (required for issue discovery)
- `ANTHROPIC_API_KEY`: For Anthropic Claude models (required for content enhancement)
- `HMS_LLM_API_KEY`: For HMS internal LLM services (required for specialized processing)

Optional API keys:
- `GEMINI_API_KEY`: For Google Gemini models (optional fallback)

### Directory Structure
- `enhanced_agency_use_cases/`: Default output directory
- `logs/`: Directory for log files
- Environment variable `HMS_NFO_DIR`: Path to HMS-NFO repository (optional)

### Memory and CPU Requirements
- Recommended: 16GB+ RAM for full parallel processing
- Recommended: 8+ CPU cores for optimal performance
- Storage: 1GB+ free space for output files