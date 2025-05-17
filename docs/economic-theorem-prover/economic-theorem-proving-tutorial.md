# Economic Theorem Proving Tutorial

This tutorial will guide you through using the Economic Theorem Proving system, from installation to creating and proving your first economic theorems.

## Introduction

The Economic Theorem Proving System combines formal verification with genetic algorithm optimization to provide a powerful platform for formalizing and proving economic theories. This tutorial assumes basic familiarity with economic concepts but no prior experience with formal theorem proving.

## Prerequisites

Before starting, ensure you have:

- Python 3.8 or higher
- Lean 4.0 or higher
- Git (for installation from source)
- Basic knowledge of economic theory

## Installation

### Step 1: Install the economic-theorem-prover package

Using pip:

```bash
pip install economic-theorem-prover
```

From source:

```bash
git clone https://github.com/hardisonco/economic-theorem-prover.git
cd economic-theorem-prover
pip install -e .
```

### Step 2: Verify installation

```bash
econ-theorem-prover --version
```

You should see output similar to:

```
Economic Theorem Prover v1.0.0
```

## Tutorial 1: Your First Economic Theorem

In this tutorial, we'll formalize and prove a simple utility maximization theorem.

### Step 1: Create a new project

```bash
econ-theorem-prover new utility_example
cd utility_example
```

This creates a new project with the necessary directory structure and configuration files.

### Step 2: Define your first theorem

Create a file named `basic_utility.lean` with the following content:

```lean
import EconomicTheorems.Microeconomics
import EconomicTheorems.Tactics

open MicroEcon
open EconTactic

/-- If a consumer maximizes utility subject to a budget constraint,
    then the marginal rate of substitution equals the price ratio. -/
theorem mrs_equals_price_ratio
  {U : Utility} {B : Budget} {x : Bundle} (h₁ : Differentiable U)
  (h₂ : Maximizes U x B) : MRS U x = PriceRatio B :=
begin
  -- Start the proof
  apply first_order_condition,
  -- Use the maximization hypothesis
  apply h₂,
  -- Apply differentiability
  apply h₁,
  -- Complete the proof
  done
end
```

This theorem states that when a consumer maximizes utility subject to a budget constraint, the marginal rate of substitution equals the price ratio - a fundamental result in microeconomics.

### Step 3: Prove the theorem

```bash
econ-theorem-prover prove basic_utility.lean
```

You should see output confirming the theorem has been proven:

```
Proving theorem: mrs_equals_price_ratio
Status: ✓ Proven
Time: 0.23s
Proof steps: 4
```

### Step 4: Visualize the proof

```bash
econ-theorem-prover export basic_utility.lean --format html
```

This creates an HTML file (`basic_utility.html`) with an interactive visualization of the proof steps.

## Tutorial 2: Genetic Optimization

Now, let's use genetic algorithms to optimize our proof strategy.

### Step 1: Create a more complex theorem

Create a file named `demand_functions.lean`:

```lean
import EconomicTheorems.Microeconomics
import EconomicTheorems.Tactics

open MicroEcon
open EconTactic

/-- For Cobb-Douglas utility with equal weights, 
    the demand functions are x = w/(2*px) and y = w/(2*py) -/
theorem cobb_douglas_equal_weight_demand
  {px py w : ℝ} (h_px : px > 0) (h_py : py > 0) (h_w : w > 0) :
  let U := λ (x y : ℝ), x^(1/2) * y^(1/2) in
  let B := λ (x y : ℝ), px * x + py * y ≤ w in
  let x_star := w / (2 * px) in
  let y_star := w / (2 * py) in
  Maximizes U (x_star, y_star) B :=
begin
  -- Define our variables
  intros U B x_star y_star,
  
  -- This proof is more complex and could benefit from optimization
  apply utility_maximization_lagrangian,
  field_simp [U, B, x_star, y_star],
  apply budget_binding,
  simp [B, x_star, y_star],
  field_simp,
  ring,
end
```

### Step 2: Run proof with genetic optimization

```bash
econ-theorem-prover optimize demand_functions.lean
```

You'll see the genetic algorithm evolving proof strategies over several generations:

```
Genetic Optimization for theorem: cobb_douglas_equal_weight_demand
Population size: 50
Generations: 20

Generation 1/20:
  Best fitness: 0.42
  Average fitness: 0.28
  Best strategy: [intros, apply utility_maximization_lagrangian, field_simp, apply budget_binding, simp, field_simp, ring]

...

Generation 20/20:
  Best fitness: 0.86
  Average fitness: 0.73
  Best strategy: [intros, apply direct_utility_maximization, auto]

Optimization complete!
Optimized proof:
```

The system discovers a more efficient proof strategy using the `direct_utility_maximization` tactic combined with `auto`.

### Step 3: Save the optimized strategy

```bash
econ-theorem-prover optimize demand_functions.lean --save-strategy cobb_douglas_strategy.json
```

### Step 4: Apply the optimized strategy to similar theorems

Create a new theorem in `general_demand.lean`:

```lean
import EconomicTheorems.Microeconomics
import EconomicTheorems.Tactics

open MicroEcon
open EconTactic

/-- For Cobb-Douglas utility with parameter α,
    the demand functions are x = α*w/px and y = (1-α)*w/py -/
theorem cobb_douglas_general_demand
  {α px py w : ℝ} (h_α : 0 < α ∧ α < 1)
  (h_px : px > 0) (h_py : py > 0) (h_w : w > 0) :
  let U := λ (x y : ℝ), x^α * y^(1-α) in
  let B := λ (x y : ℝ), px * x + py * y ≤ w in
  let x_star := α * w / px in
  let y_star := (1 - α) * w / py in
  Maximizes U (x_star, y_star) B :=
begin
  -- This is where we'll use our optimized strategy
  sorry
end
```

Now apply the saved strategy:

```bash
econ-theorem-prover prove general_demand.lean --load-strategy cobb_douglas_strategy.json
```

## Tutorial 3: Working with Game Theory

Let's explore how to formalize game theory concepts.

### Step 1: Create a new game theory file

Create `prisoners_dilemma.lean`:

```lean
import EconomicTheorems.GameTheory
import EconomicTheorems.Tactics

open GameTheory
open EconTactic

/-- Define the Prisoner's Dilemma game -/
def prisoners_dilemma : Game := {
  players := 2,
  strategies := λ i, [Cooperate, Defect],
  payoffs := λ s,
    if s = [Cooperate, Cooperate] then [-1, -1]
    else if s = [Cooperate, Defect] then [-3, 0]
    else if s = [Defect, Cooperate] then [0, -3]
    else [-2, -2]
}

/-- In the Prisoner's Dilemma, (Defect, Defect) is a unique Nash Equilibrium -/
theorem pd_unique_nash_equilibrium :
  ∃! s, NashEquilibrium prisoners_dilemma s ∧ 
       s = [Defect, Defect] :=
begin
  apply unique_nash,
  iterate_strategy_profiles,
  iterate_best_responses,
  dominant_strategy_argument,
  done
end
```

### Step 2: Prove the game theory theorem

```bash
econ-theorem-prover prove prisoners_dilemma.lean
```

### Step 3: Analyze the Nash equilibrium

```bash
econ-theorem-prover analyze prisoners_dilemma.lean --property "nash_equilibrium"
```

This will output an analysis of the Nash equilibrium, showing why (Defect, Defect) is the unique equilibrium despite not being Pareto optimal.

## Tutorial 4: Mechanism Design

Let's explore mechanism design by formalizing and proving the incentive compatibility of the Vickrey auction.

### Step 1: Create a mechanism design theorem

Create `vickrey_auction.lean`:

```lean
import EconomicTheorems.MechanismDesign
import EconomicTheorems.Tactics

open MechanismDesign
open EconTactic

/-- Vickrey second-price auction is strategy-proof (truthful bidding is a dominant strategy) -/
theorem vickrey_auction_strategy_proof
  {n : ℕ} {v : ℕ → ℝ} {i : ℕ} (h_i : i < n) :
  let second_price_auction := VickreyAuction n in
  let truthful_bid := v i in
  DominantStrategy second_price_auction i (λ b, b = truthful_bid) :=
begin
  intros second_price_auction truthful_bid,
  
  apply direct_revelation_principle,
  
  cases em (wins_auction second_price_auction i truthful_bid),
  { 
    -- Case where agent i wins with truthful bid
    apply winning_case_analysis,
    apply payment_independence,
    done
  },
  {
    -- Case where agent i loses with truthful bid  
    apply losing_case_analysis,
    apply second_price_property,
    done
  }
end
```

### Step 2: Prove the mechanism design theorem

```bash
econ-theorem-prover prove vickrey_auction.lean
```

### Step 3: Test with different parameters

```bash
econ-theorem-prover parameterize vickrey_auction.lean --params "n=3, v=[10,7,5]"
```

This will analyze the theorem with specific parameter values, showing how the Vickrey auction works in a concrete example.

## Tutorial 5: Advanced Self-Healing Features

The Economic Theorem Proving System includes advanced self-healing features that automatically detect and resolve issues.

### Step 1: Enable the self-healing dashboard

```bash
econ-theorem-prover dashboard
```

This launches a web dashboard at http://localhost:8080 showing system health and metrics.

### Step 2: Configure self-healing behavior

Create or edit `self_healing_config.json`:

```json
{
  "enabled": true,
  "mode": "supervised",
  "detection_interval": 30,
  "dashboard_enabled": true,
  "dashboard_port": 8080
}
```

### Step 3: Run a resource-intensive proving session

```bash
# Run multiple complex proofs in parallel
econ-theorem-prover prove-batch complex_theorems.txt --parallel
```

The self-healing system will automatically:
1. Detect resource constraints
2. Adjust optimization parameters
3. Restart components if needed
4. Provide real-time updates on the dashboard

### Step 4: View recovery actions

On the dashboard, navigate to the "Self-Healing" tab to see:
- Detected anomalies
- Recovery actions taken
- System performance improvements
- Genetic optimization adjustments

## Conclusion

You've now learned the basics of the Economic Theorem Proving System:

1. Defining and proving simple economic theorems
2. Using genetic optimization to discover efficient proof strategies
3. Working with game theory concepts
4. Formalizing mechanism design properties
5. Utilizing the self-healing capabilities

Next steps:
- Explore the example theorems in the `examples/` directory
- Read the [User Guide](USER-GUIDE-ECONOMIC-THEOREM-PROVING.md) for more details
- Join the community forum to share your theorems and strategies

## Additional Resources

- [Economic Theorem Reference](ECONOMIC-THEOREM-REFERENCE.md): Library of common economic theorems
- [Tactics Catalog](TACTICS-CATALOG.md): Detailed documentation of available proof tactics
- [API Documentation](API-REFERENCE.md): Complete API reference for programmatic integration
- [Advanced Genetic Optimization](GENETIC-OPTIMIZATION-GUIDE.md): In-depth guide to customizing genetic algorithms