# Economic Theorem Proving System User Guide

## Introduction

Welcome to the Economic Theorem Proving System, a cutting-edge platform that combines formal theorem proving with genetic algorithms to automatically prove and explore economic theorems. This system is designed for economists, researchers, and data scientists who want to formalize and verify economic theories with mathematical rigor.

This guide will help you get started with using the system, from basic theorem formulation to advanced genetic optimization of proof strategies.

## Table of Contents

1. [System Overview](#system-overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Formalizing Economic Theorems](#formalizing-economic-theorems)
5. [Running Proofs](#running-proofs)
6. [Genetic Optimization](#genetic-optimization)
7. [Self-Healing Features](#self-healing-features)
8. [Integration with Other Systems](#integration-with-other-systems)
9. [Troubleshooting](#troubleshooting)
10. [API Reference](#api-reference)

## System Overview

The Economic Theorem Proving System combines several cutting-edge technologies:

- **Lean 4 Theorem Prover**: A powerful formal verification tool used to express and prove mathematical theorems
- **Economic Domain-Specific Language**: Custom tactics and libraries for economic concepts
- **Genetic Algorithm Optimization**: Evolutionary algorithms that improve proof strategies over time
- **Self-Healing Architecture**: Automatic detection and recovery from system issues

Key capabilities:

- Formalize economic theories with mathematical precision
- Automatically prove or disprove economic theorems
- Discover optimal conditions for economic properties to hold
- Evolve and improve proof strategies through genetic algorithms
- Visualize proof steps and relationships between theorems
- Export formal proofs to various formats for publication

## Installation

### Prerequisites

- Python 3.8+
- Lean 4.0+
- Rust 1.50+
- Node.js 14+

### Using Package Manager

The recommended way to install is using the provided package manager:

```bash
pip install economic-theorem-prover
```

### From Source

For the latest development version:

```bash
git clone https://github.com/hardisonco/economic-theorem-prover.git
cd economic-theorem-prover
pip install -e .
```

### Verification

Verify your installation:

```bash
econ-theorem-prover --version
```

## Quick Start

This section will guide you through a basic workflow to quickly start proving economic theorems.

### Step 1: Create a New Project

```bash
econ-theorem-prover new my_economic_theories
cd my_economic_theories
```

### Step 2: Define a Simple Economic Theorem

Create a file named `utility_maximization.lean` with the following content:

```lean
import EconomicTheorems.Microeconomics
import EconomicTheorems.Tactics

open MicroEcon
open EconTactic

theorem basic_utility_maximization 
  {U : Utility} {B : Budget} {x : Consumption} :
  Maximizes U x B → FirstOrderConditions U x B :=
begin
  intro h_max,
  apply utility_maximization,
  assumption
end
```

### Step 3: Run the Proof

```bash
econ-theorem-prover prove utility_maximization.lean
```

You should see output confirming the theorem has been proven.

### Step 4: Run with Genetic Optimization

```bash
econ-theorem-prover prove utility_maximization.lean --optimize
```

This will use genetic algorithms to discover more efficient proof strategies.

## Formalizing Economic Theorems

This section explains how to formalize various economic concepts and theories in our system.

### Economic Domains

The system provides specialized tactics and libraries for different economic domains:

| Domain | Import Path | Description |
|--------|-------------|-------------|
| Microeconomics | `EconomicTheorems.Microeconomics` | Consumer choice, firm theory, market equilibrium |
| Macroeconomics | `EconomicTheorems.Macroeconomics` | Growth models, business cycles, monetary policy |
| Game Theory | `EconomicTheorems.GameTheory` | Strategic interactions, Nash equilibrium |
| Mechanism Design | `EconomicTheorems.MechanismDesign` | Auctions, matching, incentive compatibility |
| Welfare Economics | `EconomicTheorems.WelfareEconomics` | Social welfare, Pareto efficiency |

### Microeconomic Example

Here's a more detailed example for consumer choice theory:

```lean
import EconomicTheorems.Microeconomics
import EconomicTheorems.Tactics

open MicroEcon
open EconTactic

-- Define a utility function and budget constraint
def cobb_douglas (α : ℝ) (x y : ℝ) : ℝ := x^α * y^(1-α)

-- Theorem: Cobb-Douglas demand functions
theorem cobb_douglas_demand
  {α : ℝ} {p_x p_y w : ℝ} (h_α : 0 < α ∧ α < 1) 
  (h_p : p_x > 0 ∧ p_y > 0) (h_w : w > 0) :
  let x_star := α * w / p_x in
  let y_star := (1 - α) * w / p_y in
  Maximizes (λ x y, cobb_douglas α x y) 
            (x_star, y_star) 
            (λ x y, p_x * x + p_y * y ≤ w) :=
begin
  intros x_star y_star,
  apply consumer_choice,
  apply mrt_equals_mrs,
  simp [cobb_douglas],
  field_simp,
  ring
end
```

### Game Theory Example

Here's an example of formalizing a simple prisoner's dilemma game:

```lean
import EconomicTheorems.GameTheory
import EconomicTheorems.Tactics

open GameTheory
open EconTactic

def prisoners_dilemma : Game := {
  players := 2,
  strategies := λ i, [Cooperate, Defect],
  payoffs := λ s,
    if s = [Cooperate, Cooperate] then [-1, -1]
    else if s = [Cooperate, Defect] then [-3, 0]
    else if s = [Defect, Cooperate] then [0, -3]
    else [-2, -2]
}

theorem pd_has_unique_nash_equilibrium :
  let pd := prisoners_dilemma in
  ∃! s, NashEquilibrium pd s ∧ s = [Defect, Defect] :=
begin
  intro pd,
  apply nash_equilibrium,
  iterate_best_responses,
  dominant_strategy_argument
end
```

## Running Proofs

This section explains how to run proofs using the command-line interface and how to customize the proof process.

### Basic Proof Command

```bash
econ-theorem-prover prove <file.lean> [options]
```

### Common Options

| Option | Description |
|--------|-------------|
| `--timeout <seconds>` | Set a timeout for the proof attempt |
| `--optimize` | Use genetic optimization for proof strategy |
| `--verbose` | Show detailed proof steps |
| `--export <format>` | Export proof to specified format (pdf, html, json) |
| `--tactics <file>` | Use custom tactics from specified file |

### Proof Output

The system provides detailed information about the proof process:

```
Proving theorem: basic_utility_maximization
Status: ✓ Proven
Time: 0.32s
Proof steps: 12
Tactics used:
  - intro: 1
  - apply: 2
  - assumption: 1
```

### Batch Processing

To prove multiple theorems at once:

```bash
econ-theorem-prover prove-batch theorems_list.txt
```

where `theorems_list.txt` contains paths to Lean files, one per line.

## Genetic Optimization

This section explains how to use genetic algorithms to optimize proof strategies.

### Basic Optimization

```bash
econ-theorem-prover optimize <file.lean>
```

This command will:
1. Analyze your theorem
2. Generate a population of proof strategies
3. Evolve them over multiple generations
4. Apply the best strategy to prove your theorem

### Optimization Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--population-size` | Size of strategy population | 50 |
| `--generations` | Number of generations to evolve | 20 |
| `--mutation-rate` | Probability of mutation | 0.1 |
| `--crossover-rate` | Probability of crossover | 0.7 |
| `--fitness-metric` | Metric to optimize (speed, size, clarity) | speed |

### Viewing Optimization Progress

With the `--verbose` flag, you'll see the optimization process in real-time:

```
Generation 1/20:
  Best fitness: 0.45
  Average fitness: 0.32
  Best strategy: [intro, apply utility_maximization, assumption]

Generation 2/20:
  Best fitness: 0.61
  Average fitness: 0.38
  Best strategy: [intro, apply utility_maximization_direct, done]
  
...

Generation 20/20:
  Best fitness: 0.89
  Average fitness: 0.75
  Best strategy: [intro, rw utility_def, apply FOC_iff_maximizes, done]
```

### Saving and Loading Strategies

You can save optimized strategies for future use:

```bash
# Save the best strategy after optimization
econ-theorem-prover optimize <file.lean> --save-strategy my_strategy.json

# Use a saved strategy
econ-theorem-prover prove <file.lean> --load-strategy my_strategy.json
```

## Self-Healing Features

The Economic Theorem Proving System includes advanced self-healing capabilities to ensure reliable operation.

### Automatic Recovery

The system automatically:
- Detects anomalies in performance metrics
- Identifies and fixes common error patterns
- Restarts components that are unresponsive
- Adapts resource allocation based on workload

### Monitoring Dashboard

You can access the monitoring dashboard to view system health:

```bash
econ-theorem-prover dashboard
```

This launches a web dashboard on http://localhost:8080 showing:
- System health status
- Proof performance metrics
- Genetic algorithm optimization progress
- Recovery actions and outcomes

### Configuration

To configure self-healing behavior, edit `self_healing_config.json`:

```json
{
  "enabled": true,
  "mode": "supervised",
  "detection_interval": 30,
  "dashboard_enabled": true
}
```

Available modes:
- `manual`: Requires approval for all recovery actions
- `supervised`: Automatic for non-critical issues, requires approval for critical ones
- `automated`: Fully automatic recovery
- `learning`: Only monitors issues but doesn't take action

## Integration with Other Systems

### Exporting Proofs

You can export proven theorems to various formats:

```bash
econ-theorem-prover export <file.lean> --format <format>
```

Supported formats:
- `latex`: LaTeX document with formal proof
- `html`: Interactive HTML visualization
- `json`: Machine-readable proof data
- `graph`: Dependency graph of theorems

### API Integration

The system provides a REST API for integration with other applications:

```bash
econ-theorem-prover serve --port 8000
```

This starts a server with the following endpoints:
- `POST /api/prove`: Submit a theorem for proving
- `GET /api/theorems`: List all proven theorems
- `GET /api/theorems/{id}`: Get details of a specific theorem
- `POST /api/optimize`: Optimize a proof strategy

Example API usage:

```python
import requests

# Submit a theorem for proving
response = requests.post(
    "http://localhost:8000/api/prove",
    json={
        "theorem": "theorem example : 2 + 2 = 4 := by norm_num",
        "options": {"optimize": True}
    }
)

# Get the proof result
proof_id = response.json()["id"]
result = requests.get(f"http://localhost:8000/api/theorems/{proof_id}")
print(result.json())
```

## Troubleshooting

### Common Issues

| Problem | Possible Causes | Solution |
|---------|----------------|----------|
| Proof timeout | Complex theorem or inefficient strategy | Increase timeout with `--timeout` or use `--optimize` |
| "Tactic failed" error | Incorrect tactic application | Check theorem statement and proof structure |
| Memory exhaustion | Very large search space | Use `--memory-limit` flag or simplify theorem |
| "Unknown identifier" error | Missing import or typo | Verify imports and check identifier spelling |
| Self-healing disabled | Configuration issue | Check `self_healing_config.json` settings |

### Logs

View detailed logs to diagnose issues:

```bash
econ-theorem-prover logs --level debug
```

### Community Support

- GitHub Issues: [github.com/hardisonco/economic-theorem-prover/issues](https://github.com/hardisonco/economic-theorem-prover/issues)
- Community Forum: [forum.economic-theorem-prover.org](https://forum.economic-theorem-prover.org)
- Documentation: [docs.economic-theorem-prover.org](https://docs.economic-theorem-prover.org)

## API Reference

For detailed API documentation, please see the [API Reference Guide](API-REFERENCE.md).

## Appendix: Economic Theorem Examples

The system includes many example theorems from various economic domains:

| File | Description |
|------|-------------|
| `examples/utility_maximization.lean` | Basic consumer choice |
| `examples/welfare_theorems.lean` | First and second welfare theorems |
| `examples/nash_equilibrium.lean` | Nash equilibrium existence |
| `examples/mechanism_design.lean` | VCG mechanism incentive compatibility |
| `examples/growth_model.lean` | Solow growth model properties |

To run all examples:

```bash
econ-theorem-prover prove-examples
```