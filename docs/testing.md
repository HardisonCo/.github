# HMS-DOC Testing Documentation

This document provides information about the testing framework for the HMS-DOC project.

## Overview

The HMS-DOC project includes a comprehensive testing suite that covers:

1. **Unit Tests** - Testing individual components and functions
2. **Integration Tests** - Testing interactions between components
3. **Shell Script Tests** - Testing shell scripts for batch processing and automation

## Test Directory Structure

```
/tests/               # Original test directory
  __init__.py                         # Package initialization
  test_chain_of_recursive_thought.py  # Basic tests for CRT implementation
  test_chain_of_recursive_thought_enhanced.py  # Extended tests for CRT
  test_agency_config.py               # Tests for agency configuration system
  test_batch_integration.sh           # Shell tests for batch integration
  test_parallel_processing.sh         # Shell tests for parallel processing

/test/                # Enhanced test directory 
  __init__.py                         # Package initialization
  test_agency_issue_enhancement.py    # Tests for agency issue enhancement
  test_pipeline_integration.py        # Tests for pipeline integration
  test_complete_workflow.py           # End-to-end workflow tests
  run_enhancement_tests.py            # Test runner for enhancement features
  spec_agency_issue_enhancement.md    # Test specifications
```

## Running Tests

### Running All Tests

To run the complete test suite:

```bash
./run_all_tests.sh
```

This will run all Python unit tests, shell script tests, and integration tests, and provide a summary of results.

### Running Individual Test Files

To run a specific Python test file:

```bash
# With pytest (recommended)
python -m pytest tests/test_agency_config.py -v

# With unittest
python -m unittest tests/test_agency_config.py
```

To run a specific shell test:

```bash
./tests/test_batch_integration.sh
```

## Test Coverage

The testing suite covers the following key areas:

### Chain of Recursive Thoughts (CRT) Framework

- Basic functionality of `generate_crt_use_case`
- Extraction of patterns, perspectives, and agent models
- Handling of empty or incomplete LLM responses
- Mermaid diagram generation and formatting
- Command-line argument processing

### Agency Configuration System

- Loading and validating configuration
- Agency type and field definitions
- File path management
- ID and domain generation
- Agency data validation

### Batch Integration

- Script execution
- Output file generation
- Dependency checks
- Error handling
- Logging functionality

### Parallel Processing

- Concurrent job management
- Job throttling and limits
- Agency data processing
- Result reporting

## Adding New Tests

When adding new features, please follow these guidelines for creating tests:

1. Create a new test file in the `/tests` directory named `test_[component].py` or `test_[component].sh`
2. Use the existing test files as templates
3. For Python tests, use unittest or pytest
4. For shell tests, use the provided logging and test organization functions
5. Ensure proper cleanup after tests (especially for shell tests)

## Running Agency Issue Enhancement Tests

To run tests specifically for the Agency Issue Enhancement features:

```bash
# Run all enhancement tests
./test/run_enhancement_tests.py

# Run specific enhancement test modules
python -m pytest test/test_agency_issue_enhancement.py -v
python -m pytest test/test_pipeline_integration.py -v
python -m pytest test/test_complete_workflow.py -v

# Run the complete enhancement test workflow (shell wrapper)
./test_enhancement.sh
```

The Agency Issue Enhancement tests cover:

1. **Web Search Integration** - Finding real-world issues for agencies
2. **Use Case Enhancement** - Improving use cases with discovered issues
3. **Document Integration** - Adding enhanced content to documentation
4. **Fallback Mechanisms** - Handling API failures gracefully
5. **End-to-End Processing** - Complete workflow from search to document update

## Continuous Integration

The test suite is designed to be run as part of a continuous integration pipeline. The `run_all_tests.sh` script produces structured output and exit codes suitable for CI environments.

## Testing Standards

1. **Isolation**: Tests should run independently and not depend on the state from previous tests
2. **Coverage**: Aim for at least 80% code coverage
3. **Mocking**: Use mocks for external dependencies (like LLM calls)
4. **Assertions**: Use specific, meaningful assertions
5. **Documentation**: Each test should have a clear docstring explaining what it tests