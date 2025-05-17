# Agency Documentation Generation

This document provides guidance on generating documentation for government agencies using the extended PocketFlow system. The agency documentation feature allows you to create specialized documentation for federal, state, and international government agencies.

## Overview

The agency documentation generation system extends PocketFlow with specialized nodes and flows:

1. **AgencyContext Node**: Loads and processes agency-specific information
2. **AgencyTemplate Node**: Generates standardized agency documentation
3. **Agency Flow**: Custom PocketFlow configuration optimized for government agencies

## Available Data

Sample agency data is provided in the `research` directory:

- `federal_agencies.json`: U.S. federal agencies (HHS, DOD, ED, CIA, FCC, SBA)
- `state_agencies.json`: U.S. state agencies (CA, TX, NY, FL, WA)
- `international_agencies.json`: International agencies (WHO, UN, EU)
- `legislative_process.json`: Information about legislative processes

## Command Line Options

The main script supports the following agency-specific options:

```
Agency Options:
  --agency-id AGENCY_ID   Agency ID for specific agency documentation (e.g., 'hhs', 'ed', 'cia')
  --agency-type {federal,state,international}
                          Type of agency (federal, state, or international)
  --process-agency-data   Process agency data from JSON files before running flow
  --agency-data-dir AGENCY_DATA_DIR
                          Directory containing agency data JSON files
```

## Example Commands

### Process Agency Data Only

To process agency data from JSON files without running the full flow:

```bash
python process_agency_data.py --input-dir research --output-dir output --agency-type federal --generate-all
```

### Generate Documentation for a Specific Agency

```bash
python main.py --agency-id hhs --agency-type federal --process-agency-data --agency-data-dir research
```

This command:
1. Processes agency data from the `research` directory
2. Identifies HHS in the federal agency data
3. Configures the flow for HHS-specific documentation
4. Generates documentation using the agency-specific flow

### Generate Documentation for a State Agency

```bash
python main.py --agency-id state-ca-health --agency-type state --process-agency-data --agency-data-dir research
```

### Generate Documentation for an International Agency

```bash
python main.py --agency-id intl-who --agency-type international --process-agency-data --agency-data-dir research
```

### Process Local Directory with Agency Context

To analyze a local codebase with agency-specific context:

```bash
python main.py --dir /path/to/codebase --agency-id hhs --agency-type federal
```

### Complete Example with All Options

```bash
python main.py --dir /path/to/codebase --output-dir output --agency-id dod --agency-type federal --process-agency-data --agency-data-dir research --max-abstractions 15 --max-files 100 --no-cache --language english
```

## Agency Documentation Structure

Generated agency documentation includes:

1. **Agency Portals**: Government and civilian access portals
2. **Key Actors**: Government personnel and civilian partners
3. **Introduction**: Overview of the agency's mission
4. **Problem Statement**: Challenges the agency faces
5. **Stakeholders**: Government and civilian stakeholders
6. **Political Gridlock Factors**: Political challenges affecting the agency
7. **Value Opportunity**: Benefits of AI-assisted approaches
8. **HMS Solution**: Proposed solution architecture with AI agents
9. **Expected Outcomes**: Anticipated benefits of implementation

## Integration with Other Documentation

Agency documentation integrates with standard PocketFlow documentation:

1. The agency-specific flow extends the standard flow with agency context
2. Tutorial chapters reference agency missions and use cases
3. Code abstractions are described in the context of government applications
4. Architecture diagrams show agency-specific integrations

## Customizing Agency Templates

You can customize the agency documentation templates by modifying the `_generate_template` method in `agency_nodes.py`. The template supports:

- Custom agency portals and URLs
- Specialized government and civilian actors
- Agency-specific problem statements
- Tailored solution architectures