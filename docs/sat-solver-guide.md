# SAT Solver for Economic Theorem Proving

This document provides a comprehensive guide to the SAT (Boolean Satisfiability) solver implementation for the HMS Economic Theorem Prover system. The solver is designed to verify economic theorems by encoding them as Boolean formulas and determining their satisfiability.

## Overview

The SAT solver provides an alternative approach to theorem proving, complementing the existing genetic algorithm approach and Lean integration. By encoding economic theorems as Boolean formulas in Conjunctive Normal Form (CNF), we can leverage efficient SAT solving techniques to verify or refute these theorems.

The solver implements the Davis-Putnam-Logemann-Loveland (DPLL) algorithm with modern optimizations, including:
- Unit propagation
- Pure literal elimination
- Variable selection heuristics (VSIDS)
- Phase saving
- Conflict-driven clause learning

## Architecture

The SAT solver is organized into the following components:

1. **Core Types (`types.rs`)**
   - Defines fundamental data structures like variables, literals, clauses, and formulas
   - Implements assignment representation and evaluation

2. **DPLL Solver (`dpll.rs`)**
   - Implements the main DPLL algorithm with optimizations
   - Handles search, backtracking, and conflict analysis

3. **Heuristics (`heuristics.rs`)**
   - Provides variable selection strategies like VSIDS
   - Implements phase selection strategies

4. **Utilities (`utils.rs`)**
   - Offers formula manipulation, parsing, and formatting utilities
   - Supports DIMACS format for formula I/O

5. **Encoder (`encoder.rs`)**
   - Translates economic theorems into CNF formulas
   - Provides encoding for bounded arithmetic operations
   - Implements specific encoders for WAR, DRP, and SPS theorems

6. **Integration (`integration.rs`)**
   - Connects the SAT solver with the verification pipeline
   - Implements verification interfaces for economic theorems

## Economic Theorem Encoding

The SAT solver supports encoding of the three main economic theorems from the Moneyball-Buffett Economic Model:

1. **WAR (Weighted Average Return)**
   - Formula: `WAR = (trade_balance / deficit) * 100`
   - Encoding: Ensures the theorem is valid by encoding arithmetic constraints

2. **DRP (Deficit Reduction Potential)**
   - Formula: `DRP = (sector_value / total_deficit) * weight_factor`
   - Encoding: Validates the deficit reduction calculation

3. **SPS (Sector Prioritization Score)**
   - Formula: `SPS = (sector_priority * sector_growth) / scaling_factor`
   - Encoding: Ensures correct sector prioritization calculation

## Usage Examples

### Basic SAT Solving

```rust
use hms_hardison::provers::sat_solver::{
    types::{Formula, Clause, Literal},
    dpll::DpllSolver,
};

// Create a formula
let mut formula = Formula::new();

// Add clauses (example: (x₁ ∨ x₂) ∧ (¬x₁ ∨ x₃))
let mut clause1 = Clause::new();
clause1.add_literal(Literal::positive(0)); // x₁
clause1.add_literal(Literal::positive(1)); // x₂

let mut clause2 = Clause::new();
clause2.add_literal(Literal::negative(0)); // ¬x₁
clause2.add_literal(Literal::positive(2)); // x₃

formula.add_clause(clause1);
formula.add_clause(clause2);

// Solve the formula
let mut solver = DpllSolver::new();
let result = solver.solve(formula);

// Process the result
match result {
    SatResult::Satisfiable(assignment) => {
        println!("Formula is satisfiable!");
        // Process assignment...
    },
    SatResult::Unsatisfiable => {
        println!("Formula is unsatisfiable!");
    },
    SatResult::Unknown => {
        println!("Solver could not determine satisfiability.");
    },
}
```

### Economic Theorem Verification

```rust
use hms_hardison::provers::sat_solver::{
    integration::{SatVerifier, TheoremType},
};
use hms_hardison::genetic_engine::representation::TheoremContext;

// Create a theorem context
let war_theorem = "WAR = (trade_balance / deficit) * 100";
let context = TheoremContext::new(
    "war_theorem",
    war_theorem,
    "Moneyball.Main",
    None,
);

// Create a SAT verifier
let verifier = SatVerifier::new(30000, 16);

// Verify the theorem
match verifier.verify(&context) {
    Ok(result) => {
        println!("Theorem verified successfully!");
        // Process result...
    },
    Err(err) => {
        println!("Verification failed: {}", err);
    },
}
```

## Formula Encoding Details

The SAT solver encodes arithmetic operations using a bit-vector representation with bounded integers. This approach allows us to encode:

1. **Integer Variables**
   - Each economic variable is encoded as a sequence of Boolean variables representing its bits
   - The bit width determines the range of representable integers

2. **Arithmetic Operations**
   - Addition: Full adder circuits encode binary addition
   - Multiplication: Encoded using repeated addition
   - Division: Encoded through multiplication constraints

3. **Comparison Operations**
   - Equality (=): Bit-by-bit comparison
   - Less than (<): Lexicographic comparison
   - Greater than (>): Encoded as less than with operands swapped

## Performance Considerations

The SAT solver's performance depends on several factors:

1. **Formula Size**
   - Number of variables and clauses
   - Bit width used for integer encoding

2. **Solver Configuration**
   - Timeout settings
   - Heuristic parameters
   - Conflict limit

3. **Encoding Efficiency**
   - Optimized encodings for specific operations
   - Simplified arithmetic constraints when possible

## Integration with Verification Pipeline

The SAT solver integrates with the existing verification pipeline through the `SatVerificationExt` trait, which extends `TheoremContext` with SAT verification capabilities. This allows seamless integration with the genetic engine and other verification methods.

To use the SAT solver in the verification pipeline:

1. Import the necessary modules
2. Create a `TheoremContext` for the theorem to verify
3. Use the `verify_with_sat` method to perform verification
4. Process the verification result

## Future Improvements

Planned improvements for the SAT solver include:

1. **More Efficient Encodings**
   - Specialized encodings for common economic operations
   - Support for floating-point arithmetic

2. **Advanced Solving Techniques**
   - Integration with external SAT solvers (MiniSAT, CryptoMiniSat)
   - Parallel solving for large formulas

3. **Extended Theorem Support**
   - Support for additional economic theorems
   - Encoding of more complex constraints

4. **Performance Optimizations**
   - Incremental solving for related theorems
   - Memory usage optimizations

## Conclusion

The SAT solver provides a powerful approach to economic theorem verification, complementing the existing methods in the HMS Economic Theorem Prover system. By encoding theorems as Boolean formulas and leveraging efficient solving techniques, we can automatically verify or refute economic theorems with formal guarantees.