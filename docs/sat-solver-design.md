# SAT Solver Design for Economic Theorem Proving

This document outlines the design of a SAT (Boolean Satisfiability) solver that will be integrated with the HMS Economic Theorem Prover system to enhance automated verification capabilities.

## 1. Overview

The SAT solver will provide an alternative verification method complementing the existing Lean integration and genetic algorithm approach. It will enable efficient verification of certain classes of economic theorems by encoding them as Boolean formulas and checking their satisfiability.

### Key Integration Points

1. **Verification Pipeline**: The SAT solver will be added as an optional verification backend in the existing pipeline.
2. **Theorem Encoding**: A translation layer will convert economic theorems to Boolean formulas.
3. **Result Integration**: SAT solving results will be converted back to the standard proof result format.
4. **Genetic Algorithm Enhancement**: SAT solver will provide guidance for the genetic algorithm to evolve better proofs.

## 2. Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                         HMS Economic Theorem Prover                     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                   ┌────────────────┴────────────────┐
                   │                                 │
    ┌──────────────▼─────────────┐      ┌────────────▼─────────────┐
    │  Theorem Representation    │      │  Verification Pipeline   │
    └──────────────┬─────────────┘      └────────────┬─────────────┘
                   │                                 │
    ┌──────────────▼─────────────┐      ┌────────────▼─────────────┐
    │  Formula Encoding Layer    │◄────►│  Verification Strategy    │
    └──────────────┬─────────────┘      └────────────┬─────────────┘
                   │                                 │
┌──────────────────▼─────────────────────────────────▼─────────────────┐
│                           Verification Methods                        │
│                                                                       │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐   │
│  │                 │    │                 │    │                 │   │
│  │  Lean Prover    │    │  SAT Solver     │    │  Genetic Alg.   │   │
│  │                 │    │                 │    │                 │   │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

## 3. SAT Solver Component Design

### 3.1 Core SAT Solver Module

The core SAT solver will be implemented using the DPLL (Davis–Putnam–Logemann–Loveland) algorithm with modern optimizations:

```rust
/// Represents a Boolean variable in a SAT formula
pub type Variable = u32;

/// Represents a literal (variable or its negation)
pub struct Literal {
    pub variable: Variable,
    pub polarity: bool,
}

/// Represents a clause (disjunction of literals)
pub type Clause = Vec<Literal>;

/// Represents a CNF formula (conjunction of clauses)
pub type Formula = Vec<Clause>;

/// Result of a SAT solving operation
pub enum SatResult {
    /// Formula is satisfiable with the given assignment
    Satisfiable(Assignment),
    /// Formula is not satisfiable
    Unsatisfiable,
    /// Solving timed out
    Timeout,
    /// Error occurred during solving
    Error(String),
}

/// A boolean assignment to variables
pub type Assignment = HashMap<Variable, bool>;

/// SAT solver interface
pub trait SatSolver {
    /// Solve the given formula
    fn solve(&self, formula: &Formula) -> SatResult;
    
    /// Check if the formula is satisfiable
    fn is_satisfiable(&self, formula: &Formula) -> bool;
    
    /// Find all satisfying assignments (for small formulas)
    fn all_solutions(&self, formula: &Formula, limit: usize) -> Vec<Assignment>;
}

/// DPLL-based SAT solver implementation
pub struct DpllSolver {
    /// Maximum number of conflicts before giving up
    pub max_conflicts: usize,
    /// Use unit propagation optimization
    pub use_unit_propagation: bool,
    /// Use pure literal elimination optimization
    pub use_pure_literal: bool,
    /// Variable selection heuristic
    pub var_selection: VariableSelectionStrategy,
    /// Activity-based heuristics
    pub variable_activities: HashMap<Variable, f64>,
}
```

### 3.2 Formula Encoding Layer

This layer will translate economic theorems and constraints into Boolean formulas:

```rust
/// Encoder for economic theorems
pub trait TheoremEncoder {
    /// Encode a theorem into a CNF formula
    fn encode_theorem(&self, theorem: &TheoremContext) -> Formula;
    
    /// Decode a SAT solution back to a theorem proof
    fn decode_solution(&self, 
                       theorem: &TheoremContext,
                       assignment: &Assignment) -> TacticChromosome;
                       
    /// Create constraints from the theorem context
    fn create_constraints(&self, theorem: &TheoremContext) -> Vec<Clause>;
}

/// Encoder for bounded integer arithmetic
pub struct BoundedArithmeticEncoder {
    /// Number of bits to use for integer representation
    pub bit_width: usize,
    /// Variable mapping
    pub variable_map: HashMap<String, Vec<Variable>>,
}

/// Encoder for economic model calculations
pub struct EconomicModelEncoder {
    /// Arithmetic encoder
    pub arithmetic_encoder: BoundedArithmeticEncoder,
    /// Precision for float operations
    pub float_precision: usize,
}
```

### 3.3 Integration with Verification Pipeline

```rust
/// SAT verification job
pub struct SatVerificationJob {
    /// Original verification job
    pub base_job: VerificationJob,
    /// Encoded formula
    pub formula: Formula,
    /// Variable mapping for decoding
    pub variable_mapping: HashMap<String, Vec<Variable>>,
}

/// SAT verification provider
pub struct SatVerifier {
    /// SAT solver to use
    pub solver: Box<dyn SatSolver>,
    /// Encoder to use
    pub encoder: Box<dyn TheoremEncoder>,
    /// Timeout in milliseconds
    pub timeout_ms: u64,
}

impl TheoremProver for SatVerifier {
    async fn verify(&self, 
                   context: &TheoremContext, 
                   proof: &TacticChromosome) -> Result<ProofResult, String> {
        // Implementation details...
    }
    
    async fn generate(&self, 
                     context: &TheoremContext) -> Result<TacticChromosome, String> {
        // Implementation details...
    }
    
    async fn is_provable(&self, 
                        context: &TheoremContext) -> Result<bool, String> {
        // Implementation details...
    }
}
```

## 4. Theorem Encoding Strategies

### 4.1 Bounded Integer Arithmetic Encoding

For economic theorems involving bounds (like `war_score_bounds`), we'll use:

1. **Bit-vector Representation**: Encode integers as fixed-width bit vectors
2. **Comparison Circuits**: Implement less-than, greater-than, equality 
3. **Adder/Multiplier Circuits**: For arithmetic operations in economic formulas

### 4.2 Linear Constraints

For linear constraints like:
- `weights_sum_one`: Σ sector_weights = 1.0
- `potentials_nonneg`: ∀ s, deficit_reduction_potentials[s] ≥ 0

We'll use:
1. **Cardinality Constraints**: Efficient encoding of sum constraints
2. **Comparison Cascades**: For universally quantified constraints

### 4.3 Special Case: WAR Score Bounds

The theorem `war_score_bounds: -100 ≤ war_score(input) ∧ war_score(input) ≤ 100` requires:

1. Converting real arithmetic to bounded integer arithmetic
2. Encoding multiplications and summations
3. Encoding double-sided inequality

## 5. Implementation Plan

1. **Core SAT Solver**:
   - Implement basic DPLL
   - Add clause learning and watched literals
   - Add heuristics for variable selection
   - Add incremental solving capability

2. **Economic Theorem Encoding**:
   - Implement bounded arithmetic
   - Implement array/map encoding
   - Create specific encoders for WAR, DRP, SPS theorems

3. **Integration**:
   - Add SAT solver to verification pipeline
   - Create unified proof representation
   - Add proof extraction capability

4. **Optimizations**:
   - Simplify formulas before solving
   - Use domain-specific symmetry breaking
   - Implement structural sharing for subformulas

## 6. Evaluation Metrics

1. **Verification Speed**: Time to verify theorems compared to other methods
2. **Completeness**: Types of theorems that can be verified
3. **Memory Usage**: Peak memory consumption 
4. **Scalability**: Performance on larger economic models
5. **Integration Quality**: Smooth interaction with other components

## 7. Future Extensions

1. **SMT Integration**: Extend to Satisfiability Modulo Theories for richer formulas
2. **Quantifier Support**: Handle forall/exists in economic theorems
3. **Incremental Verification**: Reuse solver state across verification tasks
4. **Parallel Solving**: Distribute solving across multiple cores

## 8. Limitations

1. **Floating Point**: Limited precision for real numbers
2. **Non-linear Constraints**: Potential explosion in formula size
3. **Quantifiers**: Universal/existential quantifiers require special handling
4. **Formula Size**: Optimization theorems may lead to very large formulas

## 9. Verification Strategy Integration

The SAT solver will be integrated into the verification strategy module, which will decide which verification method to use for a given theorem:

1. Use **SAT** for: 
   - Bounded theorems (like `war_score_bounds`)
   - Constraint satisfaction problems

2. Use **Lean** for:
   - Complex arithmetic proofs
   - Inductive proofs
   - Theorems with quantifiers

3. Use **Genetic Algorithm** for:
   - When both SAT and Lean struggle
   - To optimize existing proofs
   - For complex combinations of theorems