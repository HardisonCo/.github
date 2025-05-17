# HMS Agency Tutorials Implementation Plan

This document outlines the comprehensive plan for implementing the HMS agency tutorial system, which will demonstrate how each HMS component supports various federal, state, and international agencies.

## Overview

The implementation plan covers approximately 1500 combinations of agencies and HMS system components (52 federal agencies × ~30 HMS components, plus state agencies and international health systems). This document outlines the strategy for scripting and tracking the progress of this large-scale documentation effort.

## Implementation Strategy

### 1. Agency Data Preparation

- Convert agency data from JS format to structured JSON
- Validate and enhance agency metadata (type, full name, abbreviation)
- Organize agencies by type (federal, state, international)
- Integrate international health systems data (22 major systems)
- Incorporate public health departments from global sources
- Add US state-level agencies using location data
- Store in `agencies.json` for programmatic access

### 2. Directory Structure Creation

- Create timestamped directories for agency documentation
- Establish consistent directory hierarchy:
  ```
  docs/HMS-NFO-AGENCY-{timestamp}/
  ├── agency1/
  │   ├── HMS-API/
  │   ├── HMS-GOV/
  │   └── ...
  ├── agency2/
  │   ├── HMS-API/
  │   └── ...
  └── index.md
  ```
- Create symbolic links to the latest version
- Generate index files for easy navigation
- Organize by agency type (federal, state, international)

### 3. Tutorial Generation

- Use LLM-based generation for component-specific tutorials
- Follow geographic prioritization: US Federal → US State → International
- Template structure for each tutorial:
  - Component Overview
  - Agency Context
  - Integration Points
  - Use Cases
  - Implementation Roadmap
  - Visual Diagrams (Mermaid system architecture and process flow)
  - Benefits and Value Proposition
  - Governance Considerations
- Parallelize generation where possible
- Implement retry mechanisms for API failures

### 4. Progress Tracking

- Develop script to analyze directory structure
- Count existing tutorials by component and agency
- Calculate completion percentages
- Generate visual reports showing progress
- Track by agency type (federal, state, international)
- Identify top-performing components and agencies
- Generate visualizations for stakeholder reporting

## Geographic Coverage

### US Federal Agencies
- Complete coverage of all 52 federal agencies
- Priority implementation of core components (HMS-API, HMS-GOV, HMS-MFE)
- Full component coverage for selected high-priority agencies

### US State Agencies
- Focus on state health departments for all 50 states
- Leverage geographic location data from HMS-NFO
- Adapt federal templates to state-specific requirements
- Prioritize high-population states first

### International Health Systems
- Coverage of 22 major global health systems (NHS, Medicare, etc.)
- Integration with international public health departments
- Regional coverage across all major continents
- Support for diverse healthcare system models:
  - Single-payer systems (UK, Canada)
  - Universal multi-payer systems (Germany, France)
  - Universal insurance coverage (Japan, Israel)
  - Mixed public-private systems (Australia)
  - Emerging national systems (Brazil, India)

## Timeline and Milestones

1. **Foundation Setup** (Complete)
   - Agency data conversion
   - Directory structure script
   - Symbolic link management

2. **Federal Agency Coverage** (In Progress)
   - Generate tutorials for core components (HMS-API, HMS-GOV, HMS-MFE)
   - Expand to secondary components
   - Enhance with mermaid diagrams

3. **State Agency Expansion** (Underway)
   - Prepare state agency data from location files
   - Follow federal agency template
   - Adapt to state-specific use cases

4. **International Agency Addition** (Started)
   - Integrate world health systems data
   - Process global public health departments
   - Adapt to international requirements
   - Consider regional healthcare models

## Execution Plan

### Scripts

1. `convert_agencies_data.py` - Converts agency data to JSON
2. `create_agency_structure.py` - Creates directory structure with international and state data
3. `generate_component_tutorials.py` - Generates component tutorials with mermaid diagrams
4. `check_tutorial_progress.py` - Tracks and visualizes progress
5. `generate_complete_agency_tutorials.sh` - Master orchestration script
6. `run_tutorial_progress.sh` - Progress tracking wrapper
7. `create_links.sh` - Manages symbolic links for documentation directories

### Orchestration

The master script `generate_complete_agency_tutorials.sh` orchestrates the entire process:

1. Prepare agency data
2. Create directory structure
3. Generate tutorials
4. Create index files
5. Update symlinks
6. Check and report progress

## Progress Monitoring

The progress tracking system (`check_tutorial_progress.py`) provides:

1. Overall completion percentage
2. Component-by-component breakdown
3. Agency type distribution
4. Visual charts for stakeholder reporting
5. Identification of coverage gaps

## Next Steps

1. Execute the full agency tutorial generation
2. Monitor progress and focus on coverage gaps
3. Enhance tutorials with additional diagrams
4. Expand state and international agency coverage
5. Create a web interface for easier navigation
6. Develop specialized tutorials for healthcare-specific components (HMS-UHC, HMS-EHR)