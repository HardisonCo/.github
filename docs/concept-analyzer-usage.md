# HMS Concept Analyzer Usage Guide

This document provides instructions on how to use the HMS Concept Analyzer tool to extract high-level abstractions from repositories, identify relationships between them, and detect gaps in the ecosystem.

## Table of Contents

1. [Overview](#overview)
2. [Building the Tool](#building-the-tool)
3. [Analyzing a Single Repository](#analyzing-a-single-repository)
4. [Batch Analysis](#batch-analysis)
5. [Gap Detection](#gap-detection)
6. [Integration with HMS-DEV](#integration-with-hms-dev)
7. [Advanced Configuration](#advanced-configuration)

## Overview

The HMS Concept Analyzer is a tool designed to:

1. Extract high-level abstractions (concepts) from code repositories
2. Identify relationships between these abstractions
3. Build a unified concept registry across multiple repositories 
4. Detect gaps in functionality across the ecosystem
5. Facilitate finding external open-source solutions to fill those gaps

The tool is implemented in Rust for performance and reliability, with concurrent processing capabilities for analyzing large repositories efficiently.

## Building the Tool

To build the concept analyzer from source:

```bash
# Navigate to the project directory
cd /path/to/hms-concept-analyzer

# Build the project
cargo build --release

# The executable will be available at
# target/release/concept-analyzer
```

## Analyzing a Single Repository

To analyze a single repository:

```bash
# Basic usage
./target/release/concept-analyzer analyze /path/to/repository [project_name]

# Example
./target/release/concept-analyzer analyze ./SYSTEM-COMPONENTS/HMS-DEV HMS-DEV
```

This will:
1. Collect and analyze all code files in the repository
2. Identify abstractions and their relationships
3. Save the results to the `concept_analysis` directory
4. Update the unified concept registry
5. Perform gap analysis

The output files include:
- `concept_analysis/{project_name}_analysis.json` - The analysis results
- `concept_analysis/concept_registry.json` - The updated registry
- `concept_analysis/{project_name}_gaps.json` - Identified gaps

## Batch Analysis

For analyzing multiple repositories at once:

```bash
# Create a batch configuration file (see example below)
# Then run:
./target/release/concept-analyzer batch /path/to/batch_config.json
```

Example batch configuration file (`batch_config.json`):

```json
{
  "repos": [
    {
      "path": "SYSTEM-COMPONENTS/HMS-DEV",
      "name": "HMS-DEV"
    },
    {
      "path": "SYSTEM-COMPONENTS/HMS-CDF",
      "name": "HMS-CDF"
    },
    {
      "path": "codex-rs",
      "name": "codex-rs"
    }
  ],
  "include_patterns": [
    "**/*.rs",
    "**/*.md",
    "**/*.ts",
    "**/*.js",
    "**/*.py",
    "**/*.json"
  ],
  "exclude_patterns": [
    "**/target/**",
    "**/node_modules/**",
    "**/.git/**",
    "**/dist/**"
  ],
  "concurrency": 4
}
```

Batch analysis processes multiple repositories in parallel (using the specified concurrency level) and combines all results into a single concept registry.

## Gap Detection

To run gap detection on an existing concept registry:

```bash
./target/release/concept-analyzer detect-gaps /path/to/concept_registry.json
```

This will analyze the registry for:
- Concepts implemented in only one repository but used by many
- Missing or incomplete functionality
- Opportunities for creating shared libraries

The results are saved to `ecosystem_gaps.json`.

## Integration with HMS-DEV

The Concept Analyzer is designed to integrate with the HMS-DEV environment, particularly with the MAC (Multi-Agent Collaboration) system. To use it in this context:

1. The HMS-DEV instance can initiate the concept analysis process
2. MAC can coordinate the analysis across multiple repositories
3. When gaps are detected, flow-tools can be used to search for OSS solutions
4. Once candidate solutions are found, they can be analyzed and integrated

Example integration workflow:

```
HMS-DEV → initiates analysis → Concept Analyzer → detects gaps
                                       ↓
                                 flow-tools → searches for solutions
                                       ↓
                                     MAC → evaluates and integrates solutions
```

## Advanced Configuration

### Custom Concept Extraction

The concept extraction process can be customized by modifying the LLM prompts in the source code:

- `IdentifyAbstractions::create_extraction_prompt` - Controls how abstractions are identified
- `RelationshipAnalyzer::create_relationship_prompt` - Controls how relationships are analyzed

### Performance Tuning

For large repositories, you can adjust:

- The concurrency level in batch mode
- Include/exclude patterns to focus on specific file types
- The number of abstractions to extract per repository (max_abstraction_num)

### Extending the System

The modular architecture makes it easy to extend the system:

1. Creating new gap detection algorithms in `ConceptRegistry::detect_gaps`
2. Adding new repository search capabilities
3. Enhancing the concept merging algorithm for better deduplication
4. Implementing visualization tools for the concept registry

---

## Future Enhancements

Future versions of the Concept Analyzer will include:

1. Enhanced LLM integration for more accurate concept extraction
2. Interactive visualizations of the concept map
3. Automated repository cloning and integration
4. Continuous monitoring of concept evolution over time
5. Integration with CI/CD systems for automated updates