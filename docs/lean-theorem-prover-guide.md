# Lean Theorem Prover Integration Guide

This guide provides detailed information on working with the Lean 4 theorem prover integration in the HMS Economic Theorem Prover system.

## Table of Contents
1. [Overview](#overview)
2. [Setting Up the Environment](#setting-up-the-environment)
3. [Understanding Moneyball.lean](#understanding-moneyballlean)
4. [Working with TheoremContext and Lean](#working-with-theoremcontext-and-lean)
5. [Creating and Verifying Theorem Proofs](#creating-and-verifying-theorem-proofs)
6. [Integrating with Genetic Algorithms](#integrating-with-genetic-algorithms)
7. [Python FFI Interface](#python-ffi-interface)
8. [Troubleshooting](#troubleshooting)
9. [Further Development (v0.3)](#further-development-v03)

## Overview

The HMS Economic Theorem Prover system integrates with Lean 4 to provide formal verification for economic theorems derived from the Moneyball-Buffett model. This integration allows for:

- Formal specification of economic models and calculations
- Rigorous verification of economic properties
- Evolution of proof strategies using genetic algorithms
- Integration with the HMS dashboard for visualization

The integration follows a four-phase approach:
1. **Core Data Structures** - Economic model representations in Lean
2. **Theorem Stubs** - Formal theorem statements with proof outlines
3. **Integrated Domain Logic** - Cross-domain constraints and relationships
4. **Verification Strategy** - Decision between executable verification and specification focus

## Setting Up the Environment

### Prerequisites

- Lean 4 installed via elan
- Rust toolchain (2021 edition or later)
- Python 3.8+ (for FFI interface)

### Installation Steps

1. Install Lean 4 if you haven't already:
   ```bash
   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
   ```

2. Build the Rust project:
   ```bash
   cargo build
   ```

3. Run the Lean integration demo:
   ```bash
   ./run_lean_economic_demo.sh
   ```

### Directory Structure

- `lean_libs/` - Contains the Lean library files
- `src/economic_engine/theorem_prover.rs` - Core theorem prover integration
- `src/genetic_engine/deepseek.rs` - DeepSeek-Prover integration with Lean
- `examples/lean_economic_theorem_demo.rs` - Demo showing Lean integration

## Understanding Moneyball.lean

The `Moneyball.lean` file defines the economic models and theorems in Lean 4. Key components include:

### Core Data Structures

```lean
structure TradeAnalysisInput where
  sector_weights : Finmap Sector Float
  agreement_impacts : Finmap Sector Float
  deficit_reduction_potentials : Finmap Sector Float
  weights_sum_one : ∑ s ∈ sector_weights.keys, 
                   FinmapHelpers.lookup_d sector_weights s 0 = 1.0
  weights_positive : ∀ s ∈ sector_weights.keys,
                    FinmapHelpers.lookup_d sector_weights s 0 > 0
  impacts_bounded : ∀ s ∈ agreement_impacts.keys,
                  -100 ≤ FinmapHelpers.lookup_d agreement_impacts s 0 ∧ 
                   FinmapHelpers.lookup_d agreement_impacts s 0 ≤ 100
  potentials_nonneg : ∀ s ∈ deficit_reduction_potentials.keys,
                     FinmapHelpers.lookup_d deficit_reduction_potentials s 0 ≥ 0
```

### Core Calculations

```lean
def war_score (input : TradeAnalysisInput) : Float :=
  let sectors := input.sector_weights.keys
  sectors.fold
    (fun acc s => 
      let weight := FinmapHelpers.lookup_d input.sector_weights s 0
      let impact := FinmapHelpers.lookup_d input.agreement_impacts s 0
      let potential := FinmapHelpers.lookup_d input.deficit_reduction_potentials s 0
      acc + weight * impact * potential)
    0
```

### Theorem Declarations

```lean
theorem war_score_bounds (input : TradeAnalysisInput) : 
  -100 ≤ war_score input ∧ war_score input ≤ 100 := sorry
```

## Working with TheoremContext and Lean

The `TheoremContext` struct provides the interface between Rust and Lean. To create a context for Lean verification:

```rust
let context = TheoremContext::new_lean(
    "war_score_bounds",
    "-100 ≤ war_score input ∧ war_score input ≤ 100",
    "Moneyball",
    "/path/to/lean_libs"
);
```

Key fields specific to Lean integration:

- `lean_module` - The Lean module containing the theorem (e.g., "Moneyball")
- `lean_lib_path` - Path to the directory containing Lean libraries
- `imports` - List of Lean imports needed for the proof
- `custom_tactics` - Lean tactics available for proving the theorem

## Creating and Verifying Theorem Proofs

To create and verify a proof with Lean:

```rust
// Create a proof using tactics
let gene = TacticGene::new(
    ProofTactic::Sequence(vec![
        Box::new(ProofTactic::Simplify),
        Box::new(ProofTactic::Custom("linarith".to_string(), vec![])),
    ])
);
let chromosome = TacticChromosome::new(vec![gene]);

// Verify the proof using the prover
let prover = DeepSeekProver::new(deepseek_config);
let result = prover.verify(&context, &chromosome).await?;

// Check the result
if result.success {
    println!("Proof verified successfully!");
} else {
    println!("Proof verification failed:");
    for error in &result.errors {
        println!("Error: {}", error);
    }
}
```

## Integrating with Genetic Algorithms

The genetic algorithm engine can evolve proof strategies for economic theorems:

```rust
// Create fitness function
let fitness = Arc::new(EconomicTheoremFitness::new(
    prover.clone(),
    theorem_statement,
));

// Create genetic algorithm components
let selection = Arc::new(TournamentSelection::new(3));
let crossover = Arc::new(SinglePointCrossover);
let mutation = Arc::new(TacticMutation::new(Arc::new(context.clone())));

// Create genetic engine
let mut engine = GeneticEngine::new(
    genetic_config,
    fitness,
    selection,
    crossover,
    mutation,
);

// Initialize and run evolution
engine.initialize(&context).await?;
let stats = engine.run_evolution().await?;

// Get best proof
if let Some(best) = engine.get_best_individual() {
    println!("Best proof found with fitness: {}", best.fitness);
    println!("Proof: {}", best.chromosome.to_lean_code());
}
```

## Python FFI Interface

The Python FFI interface provides a way to access the theorem prover from Python:

```python
from moneyball_theorem_helper import TheoremProverFFI

async def main():
    # Create prover
    prover = TheoremProverFFI(
        lean_executable_path="lean",
        lean_lib_path="./lean_libs"
    )
    
    # Submit theorem proving task
    task_id = await prover.submit_theorem(
        "war_score_bounds",
        "-100 ≤ war_score input ∧ war_score input ≤ 100",
        "Moneyball"
    )
    
    # Wait for result
    result = await prover.wait_for_theorem_proof(task_id)
    print(f"Theorem proving result: {result}")
```

## Troubleshooting

### Common Issues

1. **Lean Executable Not Found**
   
   Make sure Lean is installed and in your PATH. You can verify by running:
   ```bash
   lean --version
   ```

2. **Theorem Verification Fails**
   
   Check the error messages for syntax issues. Common problems include:
   - Incorrect Lean syntax in theorem statements
   - Missing imports in the Lean file
   - Invalid tactics in the proof attempt

3. **Genetic Algorithm Not Converging**
   
   If the genetic algorithm doesn't find good proofs:
   - Increase the population size and generation count
   - Adjust mutation and crossover rates
   - Add more custom tactics to the TheoremContext

### Debugging

To enable verbose logging for Lean verification:

```rust
let mut config = DeepSeekConfig::default();
config.verbosity = 3;
let prover = DeepSeekProver::new(config);
```

To save intermediate Lean files for inspection:

```rust
// In DeepSeekClient::verify_with_lean
let file_path = self.create_temp_file(&lean_code).await?;
println!("Lean file saved at: {}", file_path);
```

## Further Development (v0.3)

Based on the verification strategy decision in Phase 4, future development will focus on:

### Option A: Executable Verification

- Replace constraints with subtypes (`{x // P x}`) for runtime verification
- Add test generation for boundary cases
- Integrate with property-based testing frameworks

### Option B: Pure Specification

- Focus on comprehensive proofs of key economic theorems
- Enhance the theorem library with additional lemmas
- Create a more sophisticated proof library

In either case, the v0.3 development will include:

1. Replacing `sorry` placeholders with complete proofs
2. Enhancing the genetic algorithm to learn from successful proofs
3. Building a proof database for reuse across theorems
4. Integrating with the self-healing system for automatic proof recovery

Refer to the HMS_MASTER_PLAN_v0.6.md for the detailed roadmap and timelines.