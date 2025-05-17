# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Commands
- **Run main script**: `python main.py --dir <directory_path> [--output <output_dir>]`
- **Test utility**: `python -m utils.call_llm` (tests LLM connectivity)
- **Local directory testing**: `python -m utils.crawl_local_files` (tests file crawling)
- **Single LLM call test**: `python -c "from utils.call_llm import call_llm; print(call_llm('Write a hello world program'))"` 
- **Generate documentation**: `python generate_docs.py --agency <agency_name> --component <component_name>`
- **Update index files**: `python update_index_files.py`
- **Check documentation progress**: `python check_tutorial_progress.py`
- **Run all documentation**: `./run_comprehensive_docs.sh`

## Environment Setup
- Set `OPENAI_API_KEY` environment variable for OpenAI models
- Set `GEMINI_API_KEY` for fallback to Google Gemini models
- Create virtual env: `python -m venv venv && source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

## Code Style Guidelines
- **Imports**: Standard library first, then third-party, then local modules (grouped alphabetically)
- **Formatting**: Use 4 spaces for indentation, max line length of 100 characters
- **Types**: Use type hints where possible, especially for function parameters and return values
- **Naming**: Use snake_case for functions/variables, CamelCase for classes, follow PocketFlow patterns
- **Error Handling**: Use explicit exception types, implement fallbacks where possible (LLM calls)
- **Validation**: Validate inputs and outputs, especially when using LLM-generated content, including YAML
- **Batch Processing**: Use BatchNode for parallel processing, ensure retry mechanisms are configured
- **LLM Prompts**: Format as f-strings for readability, use clear instruction formatting

## Documentation Generation Process

### Documentation System Overview
The HMS documentation system generates comprehensive documentation for each component of the Health Management System (HMS) across different agencies and entities. The documentation includes architecture descriptions, integration guides, implementation details, and use cases.

### Agency Structure and Documentation Hierarchy

The HMS documentation follows a hierarchical structure for agencies:

1. **Federal Agencies**: Top-level agencies (HHS, CDC, FDA, etc.)
2. **Sub-Agencies**: Divisions or centers within a parent agency (e.g., FDA sub-agencies: CDER, CBER, CDRH, etc.)
3. **Components**: HMS components implemented for each agency or sub-agency (HMS-NFO, HMS-CDF, etc.)

#### Generating Documentation for Sub-Agencies

Sub-agency documentation is critical for accurate implementation guidance, as each sub-agency often has unique regulatory requirements, systems, and integration needs:

1. **Identify parent agency relationship**:
   ```bash
   python generate_agency_docs.py --agency FDA --sub-agency CDER --component NFO
   ```

2. **Generate complete sub-agency documentation set**:
   ```bash
   ./run_sub_agency_docs.sh FDA CDER
   ```
   This generates documentation for all HMS components for the specified sub-agency.

3. **Update sub-agency relationships**:
   ```bash
   python update_agency_structure.py --parent FDA --add-sub CDER,CBER,CDRH
   ```
   This updates the agency hierarchy and relationships in the documentation system.

### Restarting Documentation Generation
If documentation generation is interrupted or needs to be restarted:

1. **Check current progress**:
   ```bash
   python check_tutorial_progress.py
   ```
   This will show a report of completed and pending documentation tasks.

2. **Resume specific component documentation**:
   ```bash
   python generate_agency_docs.py --agency <agency_code> --component <component_code>
   ```
   Example: `python generate_agency_docs.py --agency HHS --component CDF`

   For sub-agencies:
   ```bash
   python generate_agency_docs.py --agency <parent_agency> --sub-agency <sub_agency_code> --component <component_code>
   ```
   Example: `python generate_agency_docs.py --agency FDA --sub-agency CDER --component NFO`

3. **Resume all documentation for an agency**:
   ```bash
   ./run_agency_docs.sh <agency_code>
   ```
   Example: `./run_agency_docs.sh HHS`

4. **Resume all documentation for a sub-agency**:
   ```bash
   ./run_sub_agency_docs.sh <parent_agency> <sub_agency>
   ```
   Example: `./run_sub_agency_docs.sh FDA CDER`

5. **Resume all documentation for a component across agencies**:
   ```bash
   ./run_all_component_tutorials.sh <component_code>
   ```
   Example: `./run_all_component_tutorials.sh NFO`

6. **Run comprehensive documentation generation**:
   ```bash
   ./run_comprehensive_docs.sh
   ```
   This will generate all missing documentation across all agencies, sub-agencies, and components.

### Tracking Documentation Progress

The documentation progress is tracked through several mechanisms:

1. **Progress Tracking File**: The system maintains a JSON file at `cache/documentation_progress.json` that tracks the completion status of each component for each agency.

2. **Progress Report Command**:
   ```bash
   python check_tutorial_progress.py --detailed
   ```
   This generates a comprehensive report of all documentation components, showing:
   - Completed components (✓)
   - In-progress components (⟳)
   - Not started components (✗)
   - Summary statistics by agency and component type

3. **Visual Progress Report**:
   ```
   python check_tutorial_progress.py --visual
   ```
   Generates a visual representation of documentation progress.

4. **Update Progress**:
   ```
   python update_progress.py --agency <code> --component <code> --status completed
   ```
   Valid status values: `not_started`, `in_progress`, `completed`, `error`

### Completing Documentation

To complete a full documentation cycle:

1. **Generate all documentation**:
   ```bash
   ./run_comprehensive_docs.sh
   ```

2. **Verify all components**:
   ```bash
   python check_tutorial_progress.py --detailed
   ```

3. **Fix any failed components**:
   ```bash
   python fix_tutorials.py --errors-only
   ```

4. **Update index files**:
   ```bash
   python update_index_files.py
   ```

5. **Update symlinks for latest documentation**:
   ```bash
   ./update_latest_symlinks.sh
   ```

6. **Generate main index**:
   ```bash
   python generate_main_index.py
   ```

7. **Validate all documentation**:
   ```bash
   python validate_docs.py
   ```

### Documentation Structure

The documentation is organized in the following hierarchical structure:

```
docs/
├── International/                 # International health systems
│   ├── intl-<country-code>/       # Country-specific folder
│   │   ├── HMS-A2A/               # Agent-to-Agent component
│   │   ├── HMS-ACH/               # Accountability and Care History component
│   │   └── ...                    # Other components
│   └── ...                        # Other countries
├── USA/                           # US health systems
│   ├── Federal/                   # Federal agencies
│   │   ├── <agency-code>/         # Agency-specific folder (e.g., FDA, HHS)
│   │   │   ├── HMS-A2A/           # Component documentation for main agency
│   │   │   ├── ...
│   │   │   └── <sub-agency>/      # Sub-agency folder (e.g., CDER, CBER)
│   │   │       ├── HMS-A2A/       # Component documentation for sub-agency
│   │   │       ├── HMS-NFO/       # Component-specific folder
│   │   │       │   ├── index.md              # Main component documentation
│   │   │       │   ├── integration.md        # Integration guide
│   │   │       │   ├── implementation.md     # Implementation details
│   │   │       │   ├── examples/             # Example code 
│   │   │       │   └── images/               # Diagrams and screenshots
│   │   │       └── ...
│   │   └── ...
│   └── State/                     # State agencies
│       ├── <state-code>/          # State-specific folder
│       │   ├── HMS-A2A/
│       │   └── ...
│       └── ...
└── index.md                       # Main documentation index
```

Each component folder contains:
- `index.md`: Main component documentation with:
  - Component overview
  - Agency/sub-agency-specific adaptations
  - Key use cases tailored to the agency/sub-agency
  - Prerequisites and environment setup
  - Configuration examples
  
- `integration.md`: Integration guide covering:
  - Agency/sub-agency system integrations
  - Data exchange formats and APIs
  - Authentication and security
  - Example integration code
  
- `implementation.md`: Implementation details including:
  - Installation instructions
  - Configuration steps
  - Custom adaptations for agency/sub-agency
  - Validation procedures
  - Troubleshooting guidance
  
- `examples/`: Example code, configuration files, and templates
  - Implementation examples
  - Integration code samples
  - Configuration templates
  
- `images/`: Visual documentation elements
  - Architecture diagrams
  - Process flows
  - Integration maps
  - Screenshots

### Component Status Tracking

For each component, the system tracks:

1. **Status**: Not started, in progress, completed, or error
2. **Completion Date**: When the component was fully documented
3. **Last Modified**: When the component was last updated
4. **Validation Status**: Whether the documentation passes validation checks
5. **Dependencies**: Other components that this component depends on
6. **Integration Status**: Status of integration documentation
7. **Use Cases**: Associated use cases and their completion status

### Error Recovery

If documentation generation fails:

1. **View error logs**:
   ```bash
   tail -n 100 logs/doc_generation_errors.log
   ```

2. **Retry failed components**:
   ```bash
   python fix_tutorials.py --errors-only
   ```

3. **Manual intervention**:
   If automated fixes fail, manually edit the component documentation:
   ```bash
   vim docs/<path>/<to>/<component>/index.md
   ```
   Then update the status:
   ```bash
   python update_progress.py --agency <code> --component <code> --status completed
   ```

4. **Verify fixes**:
   ```bash
   python check_tutorial_progress.py --detailed
   ```