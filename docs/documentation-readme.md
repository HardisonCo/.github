# HMS Agency Documentation Management

This repository contains a comprehensive set of documentation for various government agencies at federal, state, and international levels, integrated with the Hierarchical Microservices System (HMS).

## Directory Structure

We have standardized the directory structure for all agency documentation as follows:

### US Federal Agencies
```
/path/to/docs/us/federal/[agency_id]/
  ├── index.md
  ├── 01_agency_information.md
  ├── 02_stakeholders.md
  ├── 03_legacy_challenges.md
  ├── 04_use_cases.md
  ├── 05_hms_integration.md
  └── 06_getting_started.md
```

### US State Agencies
```
/path/to/docs/us/state/[state_code]/[department]/
  ├── index.md
  ├── 01_agency_information.md
  ├── 02_stakeholders.md
  ├── 03_legacy_challenges.md
  ├── 04_use_cases.md
  ├── 05_hms_integration.md
  └── 06_getting_started.md
```

### International Agencies
```
/path/to/docs/international/[country_code]/[level]/[agency]/
  ├── index.md
  ├── 01_agency_information.md
  ├── 02_stakeholders.md
  ├── 03_legacy_challenges.md
  ├── 04_use_cases.md
  ├── 05_hms_integration.md
  └── 06_getting_started.md
```

## Documentation Status

The documentation now includes:
- 124 US federal agencies
- 251 US state agencies across 49 states
- 11 international agencies across 8 countries
- A total of 2,740 documentation files

## Utility Scripts

The following utility scripts are available to manage the documentation:

### fix_directory_structure.py

This script handles the reorganization of documents into the correct directory structure.

```bash
python3 fix_directory_structure.py
```

Key functionalities:
- Moves content from incorrect locations to the standardized directory structure
- Ensures all agencies have the standard 7-file documentation set
- Creates default content for missing files

### update_legacy_files.py

This script updates the legacy challenges documentation with detailed, agency-specific content.

```bash
# Update all files with default content
python3 update_legacy_files.py --all

# Update a specific file
python3 update_legacy_files.py --file /path/to/docs/us/state/XY/department/03_legacy_challenges.md

# Update a limited number of files
python3 update_legacy_files.py --all --limit 10
```

Key functionalities:
- Automatically detects agency type (transportation, health, environment, etc.)
- Generates tailored content based on agency type and state/country
- Includes realistic metrics and challenges specific to the agency type

### generate_directory_report.py

This script generates a comprehensive report on the documentation status.

```bash
python3 generate_directory_report.py
```

Key functionalities:
- Creates a JSON report with detailed statistics
- Generates a markdown report with formatted tables
- Identifies any incomplete documentation

## Content Structure

Each agency's documentation follows a standardized format:

1. **index.md** - Overview and navigation
2. **01_agency_information.md** - Core agency details and mission analysis
3. **02_stakeholders.md** - Stakeholder analysis with visualization
4. **03_legacy_challenges.md** - Current challenges and modernization opportunities
5. **04_use_cases.md** - Detailed use cases showing HMS integration
6. **05_hms_integration.md** - Technical architecture and component details
7. **06_getting_started.md** - User onboarding instructions

## Next Steps

1. Continue enhancing content for existing agencies
2. Expand international agency coverage
3. Add more detailed use cases showing cross-agency HMS integration
4. Integrate visualization diagrams in all documentation
5. Develop a web-based documentation portal

## Maintenance Guidelines

When adding new agency documentation:

1. Use the correct directory structure
2. Ensure all 7 required files are created
3. Follow content templates for consistency
4. Include agency-specific metrics and challenges
5. Highlight HMS integration points

## Running Reports

To check documentation completion status:

```bash
python3 generate_directory_report.py
```

This will create a report in the reports/ directory showing the status of all agency documentation.