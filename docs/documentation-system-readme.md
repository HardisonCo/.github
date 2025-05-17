# HMS Comprehensive Documentation System

This directory contains scripts and tools to generate comprehensive documentation for integrating HMS components with various entities:
- International healthcare systems
- US Federal agencies
- US State agencies

## Documentation Structure

The generated documentation follows this structure:

```
/reference  # Reference material used during generation (not published)
├── _dev/                    # Development process information
│   └── README.md            # HMS development process documentation
├── _legacy_docs/            # Legacy documentation for reference
│   └── README.md            # Information about legacy documentation structure
├── _ref_data/               # Reference data for documentation generation
│   ├── federal/             # Federal reference data
│   ├── international/       # International reference data
│   │   └── data_schema.md   # Data schema for international systems
│   └── state/               # State reference data
│       └── state_agencies.md# Reference data for state agencies
├── _use_case_templates/     # Templates for use case generation
│   ├── federal/             # Federal use case templates
│   │   └── agency_integration.md  # Template for federal agencies
│   ├── international/       # International use case templates
│   │   └── healthcare_integration.md  # Template for int'l healthcare systems
│   └── state/               # State use case templates
│       └── agency_integration.md  # Template for state agencies

/docs  # Published documentation
├── International/           # International healthcare systems
│   ├── py-health/           # Paraguay healthcare system (example)
│   │   ├── HMS-NFO/         # HMS-NFO component docs for Paraguay
│   │   │   ├── index.md     # Component overview
│   │   │   └── use_case.md  # Detailed use case
│   │   ├── HMS-EHR/         # HMS-EHR component docs
│   │   ├── ...              # Other HMS components
│   │   └── README.md        # Paraguay system overview
│   ├── uk/                  # UK healthcare system
│   ├── ca/                  # Canada healthcare system
│   └── ...                  # Other healthcare systems
├── USA/
│   ├── Federal/             # US Federal agencies
│   │   ├── hhs/             # Health and Human Services
│   │   ├── dhs/             # Homeland Security
│   │   └── ...              # Other federal agencies
│   └── State/               # US State agencies
│       ├── ca/              # California
│       │   ├── ca_health/   # California Department of Health
│       │   ├── ca_ed/       # California Department of Education
│       │   └── ...          # Other California agencies
│       └── ...              # Other states
└── index.md                 # Main documentation index
```

## Available Scripts

- `generate_all_docs.sh`: Main script that generates all documentation for all entity types
- `run_comprehensive_docs.sh`: Runner script that handles directory backups and user prompts
- `generate_py_health_docs.py`: Example script for generating Paraguay health system docs
- `run_py_health_docs.sh`: Example runner for Paraguay health system documentation

## Quick Start

To generate a complete set of documentation:

```
./run_comprehensive_docs.sh
```

This will:
1. Prompt to back up any existing documentation
2. Generate international, federal, and state documentation
3. Create indices and navigation structure
4. Establish symlinks for easy access

## Customization

### Adding New Entity Types

To add documentation for a new entity type:
1. Edit `generate_all_docs.sh`
2. Add a new section for your entity type
3. Create appropriate directory structure
4. Define entity-specific customization

### Modifying HMS Components

To change the HMS components covered in documentation:
1. Modify the component list in the `create_agency_structure()` function
2. Update component descriptions as needed

## Output

Generated documentation is placed in:
- `/Users/arionhardison/Desktop/CodifyHQ/docs`

Symlinks for quick access are created in:
- `/Users/arionhardison/Desktop/CodifyHQ/HMS-DOC/output/`

## Data Sources

Documentation is generated using:
- `international_health_agencies.json` for international systems
- `data/federal_agencies.json` for federal agencies (falls back to sample data)
- Sample data for state agencies (can be replaced with a data source)

## Dependencies

- Python 3
- Bash shell environment
- API keys in .env file for LLM-enhanced content (optional)

## Maintenance

As the HMS system evolves, update the documentation templates in `generate_all_docs.sh` to reflect new capabilities, components, and integration patterns.

---

Last updated: May 4, 2025