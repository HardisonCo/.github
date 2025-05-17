# Economic Theorem Prover Development Guide

This document outlines the development process and architecture of the Economic Theorem Prover project.

## Architecture Overview

The Economic Theorem Prover system is composed of several integrated components:

1. **HMS Supervisor (Rust)**: Orchestrates the entire system, manages agent lifecycle
2. **HMS AGT (Rust)**: Agent core implementation for genetic algorithms
3. **HMS FFI (Rust/Python)**: Foreign Function Interface for interoperability
4. **Theorem Repository (Python)**: Manages economic theorems and metadata
5. **Proof Engine (Python)**: Processes theorem proving requests
6. **Genetic Agents (Python)**: Self-evolving agents that optimize proof strategies
7. **Self-Healing (Python)**: Monitors and recovers from system failures
8. **Lean Formalization (Lean 4)**: Formal theorem definitions and some proofs

## Development Environment Setup

1. Install prerequisites:
   - Rust (via rustup)
   - Python 3.10+
   - Lean 4 (via elan)
   - Protocol Buffers compiler

2. Run the setup script:
   ```bash
   chmod +x setup_dev_env.sh
   ./setup_dev_env.sh
   ```

3. Activate the Python virtual environment:
   ```bash
   source venv/bin/activate
   ```

## Development Workflow

### Adding New Economic Theorems

1. Create a new Lean file in `src/lean/economic_theorems/EconomicTheorems/`
2. Formalize the theorem following the patterns in `Basic.lean`
3. Register the theorem in the Theorem Repository

### Implementing Genetic Agents

1. Define agent traits in `src/python/genetic_agents/traits.py`
2. Implement evolution strategies in `src/python/genetic_agents/evolution.py`
3. Connect to the proof engine via the defined protocols

### Testing

- Rust tests: `cd src/rust && cargo test`
- Python tests: `cd src/python && pytest`
- Integration tests: `cd tests/integration && pytest`

## Protocol Buffer Generation

Protocol buffers are used for A2A communication. After modifying `.proto` files:

1. For Python:
   ```bash
   python -m grpc_tools.protoc -I=src/proto --python_out=src/python/proto --grpc_python_out=src/python/proto src/proto/theorem_prover.proto
   ```

2. For Rust, the build.rs files will handle generation automatically.

## Continuous Integration

The project uses GitHub Actions for CI. Workflows include:
- Running tests across all components
- Linting and formatting checks
- Building Docker containers for deployment

## DeepSeek-Prover-V2 Integration

The DeepSeek integration handles:
1. Preparing theorems for DeepSeek-Prover-V2
2. Interpreting and validating proof results
3. Integrating with the genetic optimization system

## Self-Healing System

The self-healing components monitor system health and implement recovery strategies:
1. Detecting component failures
2. Implementing fallback strategies
3. Logging and alerting mechanisms
4. Automatic recovery procedures