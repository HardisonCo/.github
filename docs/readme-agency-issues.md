# Enhancing Agency Use Cases with Real-World Issues

This document describes the system for enhancing HMS agency use cases with real-world issues and solutions, creating more relevant and impactful documentation.

## Overview

The Agency Issue Finder and Use Case Enhancement system uses web search and LLM-based analysis to:

1. Identify real-world issues faced by government agencies
2. Structure these issues into coherent problem statements
3. Generate comprehensive solutions using HMS components
4. Enhance existing use cases with real-world context
5. Integrate the enhanced use cases into agency documentation

## Key Components

### 1. Agency Issue Finder

The `agency_issue_finder.py` module searches the web for real problems faced by government agencies and generates structured data about these issues. It then creates comprehensive documentation showing how HMS components can solve these problems.

Key features:
- Web search for agency-specific issues
- Structured analysis of common problems
- Generation of solutions using HMS components
- Economic model integration
- Implementation guide creation

### 2. Use Case Enhancement

The `enhance_agency_use_cases_with_issues.py` module takes existing use cases and enhances them with real-world issues:

Key features:
- Finds existing use cases in the documentation
- Extracts key details from use cases
- Merges existing use cases with real-world issues
- Preserves the structure and flow of original use cases
- Enhances problem statements, stakeholder analysis, and solution components

### 3. Integration with Agency Documentation

The `integrate_enhanced_use_cases.py` module integrates enhanced use cases into the existing agency documentation structure:

Key features:
- Finds the latest agency documentation directory
- Backs up original use case files
- Adds a "Real-World Issues and Solutions" section
- Creates links to full enhanced use cases
- Preserves the rest of the documentation structure

## Usage Instructions

### Basic Usage

To enhance a single agency use case with real-world issues and integrate it:

```bash
./batch_integrate_enhanced_use_cases.sh --agency ED "Department of Education" "distance learning challenges" education
```

To process all predefined agencies:

```bash
./batch_integrate_enhanced_use_cases.sh --all
```

### Pipeline Integration

This functionality is fully integrated with the HMS Documentation Pipeline. You can run it as part of the pipeline:

```bash
python run_hms_doc_pipeline.py enhance_integrate
```

Or as part of the full pipeline:

```bash
python run_hms_doc_pipeline.py all
```

The pipeline will:
1. Run the agency issue finder to identify real-world problems
2. Enhance existing use cases with these real-world issues
3. Integrate the enhanced use cases into the documentation
4. Generate tutorials that leverage the enhanced use cases

### Advanced Usage

For more control over the enhancement process, you can run the individual scripts:

1. Enhance a use case with real-world issues:

```bash
python enhance_agency_use_cases_with_issues.py -a ED -n "Department of Education" -i "distance learning challenges" -t education
```

2. Integrate an enhanced use case:

```bash
python integrate_enhanced_use_cases.py -a ED -e enhanced_agency_use_cases
```

## Directory Structure

```
HMS-DOC/
├── agency_issue_finder.py                   # Core issue finding module
├── enhance_agency_use_cases_with_issues.py  # Use case enhancement module
├── enhance_use_cases_with_issues.sh         # Enhancement script
├── integrate_enhanced_use_cases.py          # Integration module
├── batch_integrate_enhanced_use_cases.sh    # Complete batch process
├── enhanced_agency_use_cases/               # Directory for enhanced use cases
├── custom_agency_use_cases/                 # Original use cases
└── docs/HMS-NFO-AGENCY-*/                   # Agency documentation
```

## Workflow

1. **Issue Identification**: Searches the web for real problems faced by the specified agency
2. **Issue Structuring**: Analyzes and structures the issues into a coherent format
3. **Solution Generation**: Develops solutions using HMS components that address the issues
4. **Use Case Enhancement**: Merges the issues and solutions with existing use cases
5. **Documentation Integration**: Integrates the enhanced use cases into the agency documentation

## Example

For the Department of Education (ED):

1. Identify real issues related to "distance learning challenges"
2. Structure these issues by stakeholders, limitations, and political factors
3. Generate HMS solutions using appropriate components
4. Enhance the existing ED use case with these real-world issues
5. Integrate the enhanced use case into the ED documentation

## Notes

- The enhancement process preserves the original use case structure
- The process adds real-world context and specific issues
- The integration creates a new section in the documentation
- All original documentation is backed up before modification

For more details, see the comments in the individual scripts.