# Trade Balance FFI Integration

This document describes the Foreign Function Interface (FFI) integration for the Trade Balance system, which enables the Win-Win Calculation Framework to be used from multiple programming languages.

## Overview

The Trade Balance Core is a pure Rust implementation of the Win-Win Calculation Framework, which provides a way to analyze and optimize deals between multiple entities to ensure that all parties receive positive value (a "win-win" outcome).

The FFI integration extends this functionality to other programming languages, with complete bindings for:

1. C and C++ applications via a C API
2. Python applications via the `hms_core` Python module

## Implementation Components

The FFI integration consists of the following components:

### 1. Rust Implementation (`trade_balance_core` crate)

The core implementation in pure Rust, which provides:
- Data structures for entity profiles, value components, and analysis results
- Entity-specific value translation for different entity types (Government, Corporate, NGO, Civilian)
- Win-Win calculation and deal analysis
- Value distribution optimization
- Deal improvement suggestions

### 2. FFI Bindings (`hms-ffi` crate)

The FFI layer that exposes the Rust functionality to other languages:
- C API functions for use in C/C++ applications
- Python bindings using PyO3
- Serialization of complex data structures using JSON
- Error handling and memory safety

### 3. C Header Files

Generated C header files for use in C/C++ applications:
- `/include/hms_trade_balance.h` - Main header file for the Trade Balance API
- `/include/hms_ffi.h` - Auto-generated header with all HMS FFI functions

### 4. Python Module

The `hms_core` Python module, which includes:
- Python functions for all Trade Balance operations
- JSON serialization/deserialization for data exchange
- Python-friendly error handling

### 5. Examples

Example code showing how to use the FFI bindings:
- `/examples/trade_balance_core_demo.rs` - Rust example
- `/examples/trade_balance_python_demo.py` - Python example
- `/examples/trade_balance_c_demo.c` - C example

## API Overview

### C API

The C API provides functions for:

1. `hms_trade_balance_analyze_win_win` - Analyze a deal for win-win status
2. `hms_trade_balance_optimize_distribution` - Optimize value distribution to ensure win-win
3. `hms_trade_balance_calculate_entity_value` - Calculate the value for a single entity
4. `hms_trade_balance_create_entity_profile` - Create an entity profile
5. `hms_trade_balance_create_value_component` - Create a value component
6. `hms_trade_balance_run_example_analysis` - Run an example analysis

### Python API

The Python API provides functions with the same functionality, but with Python-friendly interfaces:

1. `trade_balance_analyze_win_win_py` - Analyze a deal for win-win status
2. `trade_balance_optimize_distribution_py` - Optimize value distribution
3. `trade_balance_calculate_entity_value_py` - Calculate entity value
4. `trade_balance_create_entity_profile_py` - Create an entity profile
5. `trade_balance_create_value_component_py` - Create a value component
6. `trade_balance_run_example_analysis_py` - Run an example analysis

## Data Exchange

Since the Trade Balance system deals with complex data structures, the FFI integration uses JSON for data exchange:

1. Input data (entity profiles, value components, etc.) is serialized as JSON strings
2. Output data (analysis results, optimized components, etc.) is returned as JSON strings or Python dictionaries
3. Helper functions are provided to create and manipulate the required data structures

This approach provides a clean interface across language boundaries while maintaining the full expressiveness of the data model.

## Usage

### C/C++ Usage

```c
#include "hms_trade_balance.h"
#include <stdio.h>

int main() {
    char result_buffer[8192];
    
    // Analyze a deal
    int status = hms_trade_balance_analyze_win_win(
        entity_profiles_json,
        value_components_json,
        result_buffer,
        sizeof(result_buffer)
    );
    
    if (status == HMS_SUCCESS) {
        printf("Analysis result: %s\n", result_buffer);
    }
    
    return 0;
}
```

### Python Usage

```python
import hms_core
import json

# Create entity profiles and value components
entity_profiles = { ... }
value_components = { ... }

# Analyze the deal
analysis_result = hms_core.trade_balance_analyze_win_win_py(
    json.dumps(entity_profiles),
    json.dumps(value_components)
)

# Check if win-win
print(f"Is win-win: {analysis_result['is_win_win']}")
```

## Documentation

Detailed documentation is available in:

- `/core/crates/trade_balance_core/README.md` - Overview and Rust API
- `/include/hms_trade_balance.h` - C API documentation
- `/include/hms_trade_balance_py.md` - Python API documentation
- `/examples/` - Example code for each language

## Future Extensions

The FFI integration could be extended to support:
- Additional programming languages (Java, Ruby, etc.)
- WebAssembly for browser-based applications
- Streaming API for large-scale data analysis
- Asynchronous processing for long-running calculations