# HMS Documentation System Guide

This guide provides detailed instructions for working with the HMS Documentation System, including commands, tools, and workflows for generating and maintaining documentation.

## Directory Structure

The HMS documentation system uses the following directory hierarchy:

```
docs/
├── HMS-NFO-AGENCY-{timestamp}/  # Generated agency documentation
│   ├── agency1/                 # Federal, state, or international agency
│   │   ├── HMS-API/             # HMS component-specific documentation
│   │   │   └── index.md         # Component tutorial for agency1
│   │   ├── HMS-GOV/
│   │   └── ...
│   ├── agency2/
│   └── index.md                 # Agency documentation index
├── HMS-NFO-AGENCY-latest        # Symlink to latest agency documentation
└── ...
```

## Documentation Commands

### Environment Setup

```bash
# Install dependencies
./install_dependencies.sh

# Generate all documentation
./generate_comprehensive_docs.sh

# Track documentation progress
./run_tutorial_progress.sh
```

### Agency Management

```bash
# Update agencies data from all sources
./update_agencies.py

# Create agency directory structure
python create_agency_structure.py

# Create index files only
python create_agency_structure.py --indexes-only
```

### Component Tutorial Generation

```bash
# Generate tutorials for all agencies and components
python generate_component_tutorials.py --all

# Generate tutorials for a specific agency type
python generate_component_tutorials.py --type federal
python generate_component_tutorials.py --type state
python generate_component_tutorials.py --type international

# Generate tutorials for priority agencies only
python generate_component_tutorials.py --priority-only

# Generate tutorials for a specific agency
python generate_component_tutorials.py --agency state-ca-health

# Generate tutorials for a specific component
python generate_component_tutorials.py --component HMS-API
```

### Progress Tracking

```bash
# Generate progress visualization
python check_tutorial_progress.py

# Run the progress tracking script with environment
./run_tutorial_progress.sh
```

### Utilities

```bash
# Update symlinks to latest documentation
./create_links.sh

# Clean temporary files
./clean.sh
```

## Component Options

The HMS Documentation System supports the following components:

| Component | Description |
|-----------|-------------|
| HMS-API | Core backend API services |
| HMS-GOV | Administrative portal for governance |
| HMS-MFE | Micro-frontend components |
| HMS-MKT | Marketplace and service discovery |
| HMS-A2A | Agent-to-agent communication |
| HMS-ACT | Activity orchestration and workflow engine |
| HMS-CDF | Codified democracy foundation engine |
| HMS-ACH | Payment and financial transaction system |
| HMS-CUR | Currency and financial services |
| HMS-DEV | Development tools and pipelines |
| HMS-EHR | Electronic health records |
| HMS-EMR | Electronic medical records |
| HMS-ETL | Extract, transform, load data pipeline |
| HMS-MCP | Model context protocol |
| HMS-OPS | Operations and monitoring |
| HMS-SCM | Supply chain management |
| HMS-SME | Subject matter expertise system |
| HMS-UHC | Universal health connector |
| HMS-UTL | Utility services and shared libraries |

## Documentation Templates

Each component tutorial follows a standardized template with these sections:

1. **Overview** - Introduction to the component and agency context
2. **Integration Points** - Key integration points between the agency and component
3. **Use Cases** - Specific agency use cases for the component
4. **Implementation Roadmap** - Phased approach for implementing the component
5. **System Architecture** - Mermaid diagram showing component architecture
6. **Process Flow** - Mermaid diagram showing process flows
7. **Benefits and Value Proposition** - Key benefits for the agency
8. **Governance Considerations** - Governance and compliance aspects
9. **Economic Model Integration** - How the component utilizes the abundance-based economic model and participates in multi-party deals

## Agency Types and Organization

### Federal Agencies

Federal agencies are organized by their category (cabinet-level, independent, etc.) and include standard federal government agencies.

### State Agencies

State agencies currently focus on health departments for the top 10 most populous states:
- California
- New York
- Texas
- Florida
- Pennsylvania
- Illinois
- Ohio
- Georgia
- North Carolina
- Michigan

### International Health Systems

International health agencies focus on major health systems worldwide:
- United Kingdom (NHS)
- Canada (Medicare)
- Germany (GKV)
- France (Assurance Maladie)
- Japan (Kokumin Kenkō Hoken)
- Australia (Medicare)
- Brazil (SUS)
- Sweden (Healthcare System)
- Taiwan (NHI)
- South Korea (NHIS)

## Agency Issue Enhancement

The HMS Documentation System now includes a powerful Agency Issue Enhancement feature that enhances agency use cases with real-world issues and solutions:

```bash
# Run as part of the complete HMS Documentation Pipeline
python run_hms_doc_pipeline.py all

# Run just the enhancement and integration step
python run_hms_doc_pipeline.py enhance_integrate

# Process all predefined agencies
./batch_integrate_enhanced_use_cases.sh --all

# Process a specific agency
./batch_integrate_enhanced_use_cases.sh --agency ED "Department of Education" "distance learning challenges" education
```

The enhancement process:
1. Searches the web for real problems faced by the specified agency
2. Structures these issues into coherent problem statements
3. Enhances existing use cases with real-world context
4. Integrates the enhanced content into the agency documentation

For more details, see [Agency Issue Enhancement](docs/00_AGENCY_ISSUE_ENHANCEMENT.md).

## Recent Changes

### v2.1.0 (April 30, 2025)

- Added Agency Issue Enhancement System to improve real-world relevance
- Integrated enhancement with the HMS Documentation Pipeline
- Added comprehensive test suite for enhancement features
- Improved resilience to API failures with fallback mechanisms
- Enhanced documentation workflow to include real-world issues

### v2.0.0 (April 29, 2025)

- Added support for state health agencies
- Added support for international health systems
- Enhanced progress tracking with visualization
- Added priority-based documentation generation
- Improved directory structure organization
- Implemented comprehensive documentation generator script
- Integrated abundance-based economic model into all documentation

### v1.5.0 (April 28, 2025)

- Added visualization improvements with mermaid diagrams
- Enhanced the agency process flow diagrams
- Added comparison of legacy vs. AI-powered systems
- Improved API documentation integration

### v1.0.0 (April 27, 2025)

- Initial release with federal agency documentation
- Basic HMS component documentation
- Directory structure and script implementation
- Documentation generation workflow