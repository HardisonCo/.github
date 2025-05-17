# ADR-001: Rust ⇄ Python FFI Boundary Strategy

**Date:** {YYYY-MM-DD}
**Status:** Proposed
**Context:** HMS-A2A requires interaction between existing Python components (Genetic Theorem Prover, initial agent logic) and newly ported/created Rust core components (trade_balance_core, mac_core, graph_core, engines). We need a consistent and maintainable strategy for this Foreign Function Interface (FFI).

**Decision Drivers:**
*   **Performance:** Minimize overhead for frequent calls across the boundary.
*   **Developer Experience:** Ease of writing, building, testing, and debugging FFI code.
*   **Type Safety:** How well can types be mapped and checked between languages?
*   **Maintainability:** Long-term stability, community support, ease of upgrades.
*   **Build Complexity:** Integration with Cargo and Python build systems (setuptools/pip).

## Considered Options

### Option 1: PyO3 + Maturin (Recommended Baseline)

*   **Description:** Use the PyO3 library to create native Python extension modules directly from Rust code. Use Maturin as the build backend to compile Rust code into Python wheels.
*   **Pros:**
    *   Idiomatic Rust and Python integration.
    *   Excellent documentation and strong community support.
    *   Good type conversion support (including complex types, Python objects).
    *   Manages Python GIL automatically in many cases.
    *   Maturin simplifies building and distributing wheels.
    *   Handles async Rust code reasonably well (via `pyo3-asyncio`).
*   **Cons:**
    *   Requires Python interpreter context for calls *from* Rust *to* Python (can be managed).
    *   Builds can be slightly slower due to Rust compilation.
    *   Tightly couples Rust crates to specific Python versions/environments during build (though wheels are generally portable).

### Option 2: C FFI (`cbindgen` + Python `ctypes`/`cffi`)

*   **Description:** Expose Rust functions via a stable C ABI using `extern "C"` and generate C header files with `cbindgen`. Call these C functions from Python using the built-in `ctypes` module or the `cffi` library.
*   **Pros:**
    *   Language-agnostic C interface, potentially reusable by other languages.
    *   Completely decouples Rust compilation from Python environment.
    *   Potentially lowest call overhead for simple function calls (no Python object conversion).
*   **Cons:**
    *   Manual memory management and safety concerns at the C boundary.
    *   Poor support for complex data types (requires manual serialization/deserialization, e.g., via JSON or Protobuf over the C boundary).
    *   Error handling is cumbersome (typically integer return codes).
    *   More boilerplate code on both Rust and Python sides.
    *   Python tooling (`ctypes`/`cffi`) is less ergonomic than PyO3.

### Option 3: Full Rewrite (No FFI)

*   **Description:** Port *all* remaining Python code (Genetic Theorem Prover, agent logic stubs) to Rust. Eliminate the need for a language boundary.
*   **Pros:**
    *   Simplifies build system and codebase.
    *   Maximizes performance and type safety (pure Rust).
    *   Eliminates FFI maintenance burden.
*   **Cons:**
    *   Significantly higher upfront development effort and time.
    *   May require expertise not currently available (e.g., complex AI/ML algorithms in Rust).
    *   Delays delivery of integrated system.

## Decision

**Chosen Option:** Option 1: PyO3 + Maturin

**Rationale:**
*   Provides the best balance of developer experience, performance, and type safety for integrating Rust libraries as Python modules.
*   Maturin streamlines the build process significantly.
*   Handles the primary use cases well: calling Rust logic from Python tests/harnesses, and eventually calling the Python GTP from the Rust `genetic_engine` (using `pyo3::Python::with_gil`).
*   While a full rewrite (Option 3) is the long-term ideal, Option 1 provides an incremental path, allowing us to benefit from Rust performance sooner.
*   Option 2 (C FFI) introduces too much manual complexity and safety risk for the types of data exchange needed (e.g., structured deals, market states).

**Consequences:**
*   Build system will depend on both Cargo and Maturin/pip.
*   CI needs to handle Rust compilation and Python wheel building/testing.
*   Developers need familiarity with PyO3 patterns for exposing Rust code.
*   Need to manage Python environment for calls *from* Rust *to* Python.

## Next Steps
*   Confirm Maturin setup in relevant crates (`trade_balance_core`, `mac_core`, `graph_core_py`, `genetic_prover_interface`).
*   Establish patterns for data serialization (e.g., using `serde_pyobject` or JSON/Protobuf) across the boundary where needed.
*   Prototype the Rust `genetic_engine` calling the Python GTP via PyO3. 