# Genetic Engine Expansion Specification - Iteration 1

## 1. Introduction

This document provides detailed technical specifications for the feature expansion tasks scheduled for Iteration 1 of the HMS Genetic Engine evolution. The expansion focuses on four key areas:

1. Additional selection methods
2. Adaptive parameter tuning
3. Multi-objective optimization
4. Evolution visualization

These expansions will enhance the genetic engine's capabilities, making it more versatile for a wider range of optimization problems while maintaining high performance and usability.

## 2. Additional Selection Methods

### 2.1 Rank-Based Selection

**Description:**
Rank-based selection assigns selection probabilities based on the rank of individuals in the population rather than their absolute fitness values. This helps maintain selection pressure even when fitness values become very similar or differ by orders of magnitude.

**Features:**
- Linear and non-linear ranking options
- Configurable selection pressure
- Support for minimization and maximization problems
- Efficient implementation with O(n log n) complexity

**Implementation:**

```rust
/// Rank-based selection parameters
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RankSelectionParams {
    /// Selection pressure (1.0 to 2.0)
    pub selection_pressure: f64,
    /// Whether to use linear (true) or non-linear (false) ranking
    pub linear: bool,
}

impl Default for RankSelectionParams {
    fn default() -> Self {
        Self {
            selection_pressure: 1.5,
            linear: true,
        }
    }
}

/// Available selection methods
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum SelectionMethod {
    /// Tournament selection (select best of n random individuals)
    Tournament {
        /// Tournament size
        size: usize,
    },
    /// Roulette wheel selection (probability proportional to fitness)
    Roulette,
    /// Rank-based selection (probability based on rank, not fitness)
    Rank(RankSelectionParams),
    /// Stochastic Universal Sampling (SUS)
    StochasticUniversalSampling,
}

impl Default for SelectionMethod {
    fn default() -> Self {
        Self::Tournament { size: 3 }
    }
}

impl<G: Genome> Population<G> {
    // Implementation for rank-based selection
    fn rank_selection<'a>(&'a self, rng: &mut SmallRng, params: &RankSelectionParams) -> &'a Individual<G> {
        let pop_size = self.individuals.len();
        
        // Handle edge cases
        if pop_size <= 1 {
            return &self.individuals[0];
        }
        
        // Sort individuals by fitness
        let mut indices: Vec<usize> = (0..pop_size).collect();
        indices.sort_by(|&i, &j| {
            self.individuals[j].fitness.partial_cmp(&self.individuals[i].fitness)
                .unwrap_or(std::cmp::Ordering::Equal)
        });
        
        // Assign selection probability based on rank
        let mut rank_probabilities = vec![0.0; pop_size];
        let sp = params.selection_pressure;
        
        if params.linear {
            // Linear ranking
            // Probability(rank i) = (2-sp)/N + 2*(sp-1)*(N-i)/(N*(N-1))
            // where N is population size, i is rank (0 = best, N-1 = worst)
            for i in 0..pop_size {
                let rank = i as f64;
                let n = pop_size as f64;
                rank_probabilities[indices[i]] = (2.0 - sp) / n + 2.0 * (sp - 1.0) * (n - rank - 1.0) / (n * (n - 1.0));
            }
        } else {
            // Non-linear ranking
            // Probability(rank i) = q * (1-q)^i
            // where q is derived from selection pressure
            let q = 1.0 - (1.0 / sp);
            let mut sum = 0.0;
            
            for i in 0..pop_size {
                let p = q * (1.0 - q).powf(i as f64);
                rank_probabilities[indices[i]] = p;
                sum += p;
            }
            
            // Normalize probabilities
            for p in &mut rank_probabilities {
                *p /= sum;
            }
        }
        
        // Create cumulative distribution
        let mut cumulative = vec![0.0; pop_size];
        let mut sum = 0.0;
        
        for i in 0..pop_size {
            sum += rank_probabilities[i];
            cumulative[i] = sum;
        }
        
        // Ensure last value is exactly 1.0 to avoid floating point issues
        cumulative[pop_size - 1] = 1.0;
        
        // Select individual using a random value
        let r = rng.gen::<f64>();
        
        // Binary search for the selected individual
        match cumulative.binary_search_by(|&c| {
            c.partial_cmp(&r).unwrap_or(std::cmp::Ordering::Equal)
        }) {
            Ok(i) => &self.individuals[i],
            Err(i) => &self.individuals[i.saturating_sub(1)],
        }
    }
}
```

### 2.2 Stochastic Universal Sampling (SUS)

**Description:**
Stochastic Universal Sampling (SUS) is an improved version of roulette wheel selection that provides zero bias and minimum spread. It selects multiple individuals in a single pass, ensuring proportional representation and reducing the chances of selection error.

**Features:**
- Single-pass multiple selection
- Zero bias sampling
- Configurable sample size
- Efficient implementation with O(n) complexity

**Implementation:**

```rust
impl<G: Genome> Population<G> {
    // Implementation for stochastic universal sampling
    fn stochastic_universal_sampling<'a>(&'a self, rng: &mut SmallRng, num_selections: usize) -> Vec<&'a Individual<G>> {
        let pop_size = self.individuals.len();
        
        // Handle edge cases
        if pop_size <= 1 {
            return vec![&self.individuals[0]; num_selections.min(1)];
        }
        
        // Calculate total fitness
        let total_fitness = self.individuals.iter()
            .map(|ind| ind.fitness)
            .sum::<f64>();
            
        if total_fitness <= 0.0 {
            // Random selection if all fitnesses are zero or negative
            return (0..num_selections)
                .map(|_| &self.individuals[rng.gen_range(0..pop_size)])
                .collect();
        }
        
        // Calculate the selection step size
        let step_size = total_fitness / num_selections as f64;
        
        // Generate the first random point in [0, step_size)
        let start = rng.gen::<f64>() * step_size;
        
        // Create pointers for SUS
        let pointers: Vec<f64> = (0..num_selections)
            .map(|i| start + i as f64 * step_size)
            .collect();
            
        // Select individuals
        let mut selections = Vec::with_capacity(num_selections);
        let mut current_sum = 0.0;
        let mut pointer_idx = 0;
        
        for (idx, individual) in self.individuals.iter().enumerate() {
            current_sum += individual.fitness;
            
            // Check if we've crossed any pointers
            while pointer_idx < pointers.len() && pointers[pointer_idx] <= current_sum {
                selections.push(&self.individuals[idx]);
                pointer_idx += 1;
            }
            
            // If we've collected all selections, we're done
            if selections.len() >= num_selections {
                break;
            }
        }
        
        // In case of rounding errors, fill remaining selections
        while selections.len() < num_selections {
            selections.push(&self.individuals[pop_size - 1]);
        }
        
        selections
    }
    
    // Integrated selection method
    fn select<'a>(&'a self, method: &SelectionMethod, rng: &mut SmallRng) -> &'a Individual<G> {
        match method {
            SelectionMethod::Tournament { size } => {
                self.tournament_selection(rng, *size)
            },
            SelectionMethod::Roulette => {
                self.roulette_selection(rng)
            },
            SelectionMethod::Rank(params) => {
                self.rank_selection(rng, params)
            },
            SelectionMethod::StochasticUniversalSampling => {
                // For single selection, use the first result from SUS
                self.stochastic_universal_sampling(rng, 1)[0]
            },
        }
    }
    
    // Multiple selection method for batch selection
    fn select_multiple<'a>(&'a self, method: &SelectionMethod, rng: &mut SmallRng, count: usize) -> Vec<&'a Individual<G>> {
        match method {
            SelectionMethod::StochasticUniversalSampling => {
                self.stochastic_universal_sampling(rng, count)
            },
            // For other methods, perform multiple individual selections
            _ => (0..count)
                .map(|_| self.select(method, rng))
                .collect(),
        }
    }
}
```

## 3. Adaptive Parameter Tuning

### 3.1 Self-Adaptive Parameters

**Description:**
Self-adaptive parameters allow the genetic algorithm to adjust its own parameters during the run, potentially improving performance and convergence. This implementation encodes parameters like mutation rate and crossover rate within the genome itself, allowing them to evolve alongside the solution.

**Features:**
- Encoding of parameters within genomes
- Parameter inheritance and mutation
- Automatic adaptation to problem characteristics
- Support for multiple parameter types

**Implementation:**

```rust
/// Trait for self-adaptive genomes
pub trait SelfAdaptiveGenome: Genome {
    /// Get the mutation rate for this genome
    fn mutation_rate(&self) -> f64;
    
    /// Get the crossover rate for this genome
    fn crossover_rate(&self) -> f64;
    
    /// Set the mutation rate for this genome
    fn set_mutation_rate(&mut self, rate: f64);
    
    /// Set the crossover rate for this genome
    fn set_crossover_rate(&mut self, rate: f64);
    
    /// Mutate the adaptive parameters
    fn mutate_parameters(&mut self, rng: &mut SmallRng);
}

/// Wrapper for adding self-adaptation to any genome
#[derive(Clone, Debug)]
pub struct AdaptiveGenome<G: Genome> {
    /// The wrapped genome
    pub genome: G,
    /// Self-adaptive mutation rate
    pub mutation_rate: f64,
    /// Self-adaptive crossover rate
    pub crossover_rate: f64,
}

impl<G: Genome> AdaptiveGenome<G> {
    /// Create a new adaptive genome
    pub fn new(genome: G, mutation_rate: f64, crossover_rate: f64) -> Self {
        Self {
            genome,
            mutation_rate: mutation_rate.clamp(0.0, 1.0),
            crossover_rate: crossover_rate.clamp(0.0, 1.0),
        }
    }
    
    /// Create a new adaptive genome with default parameters
    pub fn with_defaults(genome: G) -> Self {
        Self {
            genome,
            mutation_rate: 0.1,
            crossover_rate: 0.7,
        }
    }
}

impl<G: Genome> Genome for AdaptiveGenome<G> {
    fn random(rng: &mut SmallRng) -> Self {
        Self {
            genome: G::random(rng),
            mutation_rate: rng.gen_range(0.05..0.2),
            crossover_rate: rng.gen_range(0.6..0.9),
        }
    }
    
    fn crossover(&self, other: &Self, rng: &mut SmallRng) -> (Self, Self) {
        let (child1_genome, child2_genome) = self.genome.crossover(&other.genome, rng);
        
        // Inherit parameters from parents with some probability
        let inherit_from_first = rng.gen_bool(0.5);
        
        let (child1_mutation, child2_mutation) = if inherit_from_first {
            (self.mutation_rate, other.mutation_rate)
        } else {
            (other.mutation_rate, self.mutation_rate)
        };
        
        let (child1_crossover, child2_crossover) = if inherit_from_first {
            (self.crossover_rate, other.crossover_rate)
        } else {
            (other.crossover_rate, self.crossover_rate)
        };
        
        (
            Self {
                genome: child1_genome,
                mutation_rate: child1_mutation,
                crossover_rate: child1_crossover,
            },
            Self {
                genome: child2_genome,
                mutation_rate: child2_mutation,
                crossover_rate: child2_crossover,
            },
        )
    }
    
    fn mutate(&mut self, rng: &mut SmallRng, _rate: f64) {
        // Use self-adaptive mutation rate
        self.genome.mutate(rng, self.mutation_rate);
        
        // Mutate the parameters themselves
        self.mutate_parameters(rng);
    }
}

impl<G: Genome> SelfAdaptiveGenome for AdaptiveGenome<G> {
    fn mutation_rate(&self) -> f64 {
        self.mutation_rate
    }
    
    fn crossover_rate(&self) -> f64 {
        self.crossover_rate
    }
    
    fn set_mutation_rate(&mut self, rate: f64) {
        self.mutation_rate = rate.clamp(0.0, 1.0);
    }
    
    fn set_crossover_rate(&mut self, rate: f64) {
        self.crossover_rate = rate.clamp(0.0, 1.0);
    }
    
    fn mutate_parameters(&mut self, rng: &mut SmallRng) {
        // Apply small Gaussian mutations to parameters
        const SIGMA: f64 = 0.1;
        
        // Mutate mutation rate
        if rng.gen_bool(0.2) {
            let delta = rng.gen_range(-SIGMA..SIGMA);
            self.mutation_rate = (self.mutation_rate + delta).clamp(0.01, 0.5);
        }
        
        // Mutate crossover rate
        if rng.gen_bool(0.2) {
            let delta = rng.gen_range(-SIGMA..SIGMA);
            self.crossover_rate = (self.crossover_rate + delta).clamp(0.1, 0.9);
        }
    }
}
```

### 3.2 Rule-Based Parameter Control

**Description:**
Rule-based parameter control uses predefined rules to adjust parameters based on the algorithm's progress. This implementation includes several control mechanisms such as the 1/5 success rule for mutation rate adjustment, diversity-based control, and time-based scheduling.

**Features:**
- 1/5 success rule for mutation rate control
- Diversity-based parameter adjustment
- Generation-based parameter schedules
- Fitness improvement rate monitoring

**Implementation:**

```rust
/// Parameter control strategies
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ParameterControl {
    /// Fixed parameters (no adaptation)
    Fixed,
    /// 1/5 success rule for mutation rate
    OneFifthRule {
        /// Adjustment factor
        adjustment_factor: f64,
        /// Window size for success rate calculation
        window_size: usize,
    },
    /// Diversity-based control
    DiversityBased {
        /// Diversity threshold for high diversity
        high_diversity: f64,
        /// Diversity threshold for low diversity
        low_diversity: f64,
        /// High diversity mutation rate
        high_diversity_mutation: f64,
        /// Low diversity mutation rate
        low_diversity_mutation: f64,
    },
    /// Time-based scheduling
    TimeBased {
        /// Initial mutation rate
        initial_mutation: f64,
        /// Final mutation rate
        final_mutation: f64,
        /// Initial crossover rate
        initial_crossover: f64,
        /// Final crossover rate
        final_crossover: f64,
    },
    /// Self-adaptation (parameters encoded in genomes)
    SelfAdaptation,
}

impl Default for ParameterControl {
    fn default() -> Self {
        Self::Fixed
    }
}

/// Parameter controller for genetic algorithms
pub struct ParameterController {
    /// Control strategy
    strategy: ParameterControl,
    /// Current mutation rate
    mutation_rate: f64,
    /// Current crossover rate
    crossover_rate: f64,
    /// Success history for 1/5 rule
    success_history: VecDeque<bool>,
    /// Generation counter
    generation: usize,
    /// Maximum generations (for time-based scheduling)
    max_generations: usize,
    /// Current population diversity
    diversity: f64,
}

impl ParameterController {
    /// Create a new parameter controller
    pub fn new(strategy: ParameterControl, initial_mutation: f64, initial_crossover: f64, max_generations: usize) -> Self {
        let window_size = match &strategy {
            ParameterControl::OneFifthRule { window_size, .. } => *window_size,
            _ => 10,
        };
        
        Self {
            strategy,
            mutation_rate: initial_mutation,
            crossover_rate: initial_crossover,
            success_history: VecDeque::with_capacity(window_size),
            generation: 0,
            max_generations,
            diversity: 0.5,
        }
    }
    
    /// Update parameters based on algorithm progress
    pub fn update(
        &mut self,
        success: bool,
        diversity: f64,
        best_fitness: f64,
        avg_fitness: f64,
    ) {
        self.diversity = diversity;
        self.generation += 1;
        
        match &self.strategy {
            ParameterControl::Fixed => {
                // No adaptation
            },
            ParameterControl::OneFifthRule { adjustment_factor, window_size } => {
                // Add success to history
                if self.success_history.len() >= *window_size {
                    self.success_history.pop_front();
                }
                self.success_history.push_back(success);
                
                // Calculate success rate
                let success_count = self.success_history.iter().filter(|&&s| s).count();
                let success_rate = success_count as f64 / self.success_history.len() as f64;
                
                // Apply 1/5 rule
                // If success rate > 1/5, increase mutation rate
                // If success rate < 1/5, decrease mutation rate
                if success_rate > 0.2 {
                    self.mutation_rate *= *adjustment_factor;
                } else if success_rate < 0.2 {
                    self.mutation_rate /= *adjustment_factor;
                }
                
                // Clamp mutation rate
                self.mutation_rate = self.mutation_rate.clamp(0.001, 0.5);
            },
            ParameterControl::DiversityBased { high_diversity, low_diversity, high_diversity_mutation, low_diversity_mutation } => {
                // Adjust mutation rate based on population diversity
                if diversity >= *high_diversity {
                    self.mutation_rate = *high_diversity_mutation;
                } else if diversity <= *low_diversity {
                    self.mutation_rate = *low_diversity_mutation;
                } else {
                    // Linear interpolation
                    let t = (diversity - *low_diversity) / (*high_diversity - *low_diversity);
                    self.mutation_rate = *low_diversity_mutation + t * (*high_diversity_mutation - *low_diversity_mutation);
                }
            },
            ParameterControl::TimeBased { initial_mutation, final_mutation, initial_crossover, final_crossover } => {
                // Linear scheduling based on generation
                let progress = (self.generation as f64) / (self.max_generations as f64);
                let t = progress.clamp(0.0, 1.0);
                
                self.mutation_rate = *initial_mutation + t * (*final_mutation - *initial_mutation);
                self.crossover_rate = *initial_crossover + t * (*final_crossover - *initial_crossover);
            },
            ParameterControl::SelfAdaptation => {
                // Parameters are encoded in genomes, nothing to do here
            },
        }
    }
    
    /// Get current mutation rate
    pub fn mutation_rate(&self) -> f64 {
        self.mutation_rate
    }
    
    /// Get current crossover rate
    pub fn crossover_rate(&self) -> f64 {
        self.crossover_rate
    }
    
    /// Get current generation
    pub fn generation(&self) -> usize {
        self.generation
    }
    
    /// Get current diversity
    pub fn diversity(&self) -> f64 {
        self.diversity
    }
}
```

### 3.3 Adaptive Genetic Engine

**Description:**
The adaptive genetic engine integrates parameter control strategies into the core genetic algorithm, providing automatic adaptation during the evolution process.

**Features:**
- Integration with existing genetic engine
- Support for all parameter control strategies
- Monitoring of adaptation effectiveness
- Simple API for users

**Implementation:**

```rust
/// Adaptive genetic engine with parameter control
pub struct AdaptiveGeneticEngine<G, F>
where
    G: Genome,
    F: FitnessFunction<G>,
{
    /// Base genetic engine
    engine: GeneticEngine<G, F>,
    /// Parameter controller
    controller: ParameterController,
    /// Success history
    success_history: Vec<bool>,
    /// Whether to use self-adaptive parameters
    use_self_adaptation: bool,
}

impl<G, F> AdaptiveGeneticEngine<G, F>
where
    G: Genome,
    F: FitnessFunction<G>,
{
    /// Create a new adaptive genetic engine
    pub fn new(engine: GeneticEngine<G, F>, strategy: ParameterControl) -> Self {
        let params = &engine.params;
        let controller = ParameterController::new(
            strategy.clone(),
            params.mutation_rate,
            params.crossover_rate,
            params.max_generations,
        );
        
        let use_self_adaptation = matches!(strategy, ParameterControl::SelfAdaptation);
        
        Self {
            engine,
            controller,
            success_history: Vec::new(),
            use_self_adaptation,
        }
    }
    
    /// Evolve the population
    pub fn evolve(&mut self) -> Result<GeneticSolution<G>> {
        if self.use_self_adaptation {
            // For self-adaptation, we need to convert the initial genomes
            // This is a simplified example - in practice we'd need proper genome conversion
            self.convert_to_adaptive_genomes();
            
            // Use special evolution for self-adaptation
            self.evolve_self_adaptive()
        } else {
            // Use regular evolution with parameter control
            self.evolve_with_parameter_control()
        }
    }
    
    /// Evolve using parameter control
    fn evolve_with_parameter_control(&mut self) -> Result<GeneticSolution<G>> {
        // Initialize the population
        let mut population = self.engine.initialize_population();
        
        // Apply constraints to the initial population
        population = self.engine.apply_constraints(population);
        
        // Track the best solution found so far
        let mut best_solution = match population.best() {
            Some(best) => GeneticSolution {
                genome: best.genome.clone(),
                fitness: best.fitness,
                generation: population.generation,
            },
            None => return Err(anyhow::anyhow!("Failed to initialize population")),
        };
        
        // Calculate initial diversity
        let diversity = self.calculate_diversity(&population);
        
        // Initialize parameter controller
        self.controller.update(false, diversity, best_solution.fitness, population.average_fitness);
        
        // Track start time for timeout
        let start_time = Instant::now();
        let timeout = Duration::from_millis(self.engine.params.timeout_ms);
        
        // Main evolution loop
        for generation in 0..self.engine.params.max_generations {
            // Check for timeout
            if start_time.elapsed() > timeout {
                tracing::info!("Evolution timeout after {} generations", generation);
                break;
            }
            
            // Get current parameters from controller
            let mutation_rate = self.controller.mutation_rate();
            let crossover_rate = self.controller.crossover_rate();
            
            // Apply parameters to engine
            self.engine.params.mutation_rate = mutation_rate;
            self.engine.params.crossover_rate = crossover_rate;
            
            // Evolve one generation
            let prev_best_fitness = population.best_fitness;
            population = self.engine.evolve_generation(population);
            
            // Check for improvement
            let success = population.best_fitness > prev_best_fitness;
            self.success_history.push(success);
            
            // Calculate diversity
            let diversity = self.calculate_diversity(&population);
            
            // Update parameter controller
            self.controller.update(
                success,
                diversity,
                population.best_fitness,
                population.average_fitness,
            );
            
            // Update best solution if needed
            if let Some(best) = population.best() {
                if best.fitness > best_solution.fitness {
                    best_solution = GeneticSolution {
                        genome: best.genome.clone(),
                        fitness: best.fitness,
                        generation: population.generation,
                    };
                    
                    tracing::debug!(
                        fitness = best_solution.fitness, 
                        generation = best_solution.generation,
                        mutation_rate = mutation_rate,
                        crossover_rate = crossover_rate,
                        "New best solution found"
                    );
                }
                
                // Check for early stopping
                if best.fitness >= self.engine.params.fitness_threshold {
                    tracing::info!(
                        "Reached fitness threshold after {} generations", 
                        population.generation
                    );
                    break;
                }
            }
        }
        
        Ok(best_solution)
    }
    
    /// Calculate population diversity
    fn calculate_diversity<I: Genome>(&self, population: &Population<I>) -> f64 {
        // For demonstration purposes, a simple diversity measure
        // In practice, this would depend on the genome representation
        
        // For numeric genomes, we could use variance
        // For string genomes, we could use edit distance
        // For permutation genomes, we could use position variance
        
        // Placeholder implementation
        let best_fitness = population.best_fitness;
        let avg_fitness = population.average_fitness;
        
        // Simple diversity measure: normalized difference between best and average
        if best_fitness <= 0.0 {
            return 0.5; // Default diversity
        }
        
        let diversity = (best_fitness - avg_fitness) / best_fitness;
        diversity.clamp(0.0, 1.0)
    }
    
    // Additional methods for self-adaptation would go here
    // ...
}
```

## 4. Multi-Objective Optimization

### 4.1 Non-dominated Sorting Genetic Algorithm (NSGA-II)

**Description:**
The Non-dominated Sorting Genetic Algorithm II (NSGA-II) is a popular algorithm for multi-objective optimization. It uses Pareto dominance and crowding distance to rank solutions, ensuring both convergence to the Pareto front and diversity of solutions.

**Features:**
- Pareto dominance ranking
- Crowding distance calculation
- Fast non-dominated sorting
- Elitist selection mechanism

**Implementation:**

```rust
/// Objective function for multi-objective optimization
pub trait ObjectiveFunction<G: Genome>: Send + Sync + 'static {
    /// Evaluate a genome for a specific objective
    fn evaluate(&self, genome: &G) -> f64;
    
    /// Whether this objective should be minimized
    fn is_minimizing(&self) -> bool;
    
    /// Get the name of this objective
    fn name(&self) -> &str;
}

/// Multi-objective fitness function
pub struct MultiObjectiveFitness<G: Genome> {
    /// Objective functions
    objectives: Vec<Box<dyn ObjectiveFunction<G>>>,
}

impl<G: Genome> MultiObjectiveFitness<G> {
    /// Create a new multi-objective fitness function
    pub fn new() -> Self {
        Self {
            objectives: Vec::new(),
        }
    }
    
    /// Add an objective function
    pub fn add_objective<O: ObjectiveFunction<G> + 'static>(&mut self, objective: O) -> &mut Self {
        self.objectives.push(Box::new(objective));
        self
    }
    
    /// Get the number of objectives
    pub fn num_objectives(&self) -> usize {
        self.objectives.len()
    }
    
    /// Evaluate a genome for all objectives
    pub fn evaluate_all(&self, genome: &G) -> Vec<f64> {
        self.objectives.iter()
            .map(|obj| obj.evaluate(genome))
            .collect()
    }
    
    /// Check if solution A dominates solution B
    pub fn dominates(&self, a_scores: &[f64], b_scores: &[f64]) -> bool {
        debug_assert_eq!(a_scores.len(), self.objectives.len());
        debug_assert_eq!(b_scores.len(), self.objectives.len());
        
        let mut a_better_somewhere = false;
        
        for (i, (a, b)) in a_scores.iter().zip(b_scores.iter()).enumerate() {
            let minimizing = self.objectives[i].is_minimizing();
            
            // For each objective, check if a is worse than b
            if (minimizing && a > b) || (!minimizing && a < b) {
                return false;
            }
            
            // Check if a is better than b for at least one objective
            if (minimizing && a < b) || (!minimizing && a > b) {
                a_better_somewhere = true;
            }
        }
        
        a_better_somewhere
    }
}

/// Individual for multi-objective optimization
#[derive(Clone)]
struct MultiObjectiveIndividual<G: Genome> {
    /// Genome
    genome: G,
    /// Objective scores
    scores: Vec<f64>,
    /// Rank (lower is better)
    rank: usize,
    /// Crowding distance (higher is better)
    crowding_distance: f64,
}

impl<G: Genome> MultiObjectiveIndividual<G> {
    /// Create a new multi-objective individual
    fn new(genome: G, scores: Vec<f64>) -> Self {
        Self {
            genome,
            scores,
            rank: 0,
            crowding_distance: 0.0,
        }
    }
    
    /// Check if this individual dominates another
    fn dominates(&self, other: &Self, fitness: &MultiObjectiveFitness<G>) -> bool {
        fitness.dominates(&self.scores, &other.scores)
    }
}

/// Non-dominated sorting algorithm for NSGA-II
struct NonDominatedSorting<G: Genome> {
    /// Fitness function
    fitness: MultiObjectiveFitness<G>,
}

impl<G: Genome> NonDominatedSorting<G> {
    /// Create a new non-dominated sorting algorithm
    fn new(fitness: MultiObjectiveFitness<G>) -> Self {
        Self { fitness }
    }
    
    /// Perform fast non-dominated sorting on a population
    fn sort(&self, population: &mut Vec<MultiObjectiveIndividual<G>>) -> Vec<Vec<usize>> {
        let n = population.len();
        
        // Initialize domination counters and dominated sets
        let mut domination_count = vec![0; n];
        let mut dominated_by: Vec<Vec<usize>> = vec![Vec::new(); n];
        
        // Calculate domination relationships
        for i in 0..n {
            for j in (i+1)..n {
                if population[i].dominates(&population[j], &self.fitness) {
                    dominated_by[i].push(j);
                    domination_count[j] += 1;
                } else if population[j].dominates(&population[i], &self.fitness) {
                    dominated_by[j].push(i);
                    domination_count[i] += 1;
                }
            }
        }
        
        // Build fronts
        let mut fronts: Vec<Vec<usize>> = Vec::new();
        let mut current_front = Vec::new();
        
        // First front: all individuals with domination count of 0
        for i in 0..n {
            if domination_count[i] == 0 {
                population[i].rank = 0;
                current_front.push(i);
            }
        }
        
        fronts.push(current_front);
        
        // Build remaining fronts
        let mut front_index = 0;
        while !fronts[front_index].is_empty() {
            let mut next_front = Vec::new();
            
            for &i in &fronts[front_index] {
                for &j in &dominated_by[i] {
                    domination_count[j] -= 1;
                    if domination_count[j] == 0 {
                        population[j].rank = front_index + 1;
                        next_front.push(j);
                    }
                }
            }
            
            front_index += 1;
            fronts.push(next_front);
        }
        
        // Remove the last empty front
        fronts.pop();
        
        fronts
    }
    
    /// Calculate crowding distance for individuals in each front
    fn calculate_crowding_distance(&self, population: &mut Vec<MultiObjectiveIndividual<G>>, fronts: &[Vec<usize>]) {
        let num_objectives = self.fitness.num_objectives();
        
        // Reset all crowding distances
        for individual in population.iter_mut() {
            individual.crowding_distance = 0.0;
        }
        
        // Calculate crowding distance for each front
        for front in fronts {
            let front_size = front.len();
            
            // Skip fronts with fewer than 2 individuals
            if front_size <= 1 {
                if front_size == 1 {
                    population[front[0]].crowding_distance = f64::INFINITY;
                }
                continue;
            }
            
            // Calculate crowding distance for each objective
            for obj_idx in 0..num_objectives {
                // Sort individuals in the front by the current objective
                let mut sorted_front = front.clone();
                sorted_front.sort_by(|&a, &b| {
                    let a_score = population[a].scores[obj_idx];
                    let b_score = population[b].scores[obj_idx];
                    a_score.partial_cmp(&b_score).unwrap_or(std::cmp::Ordering::Equal)
                });
                
                // Set boundary points to infinity
                population[sorted_front[0]].crowding_distance = f64::INFINITY;
                population[sorted_front[front_size - 1]].crowding_distance = f64::INFINITY;
                
                // Calculate crowding distance for intermediate points
                let obj_min = population[sorted_front[0]].scores[obj_idx];
                let obj_max = population[sorted_front[front_size - 1]].scores[obj_idx];
                let scale = (obj_max - obj_min).max(1e-10); // Avoid division by zero
                
                for i in 1..(front_size - 1) {
                    let prev_score = population[sorted_front[i-1]].scores[obj_idx];
                    let next_score = population[sorted_front[i+1]].scores[obj_idx];
                    
                    // Add normalized distance to crowding distance
                    population[sorted_front[i]].crowding_distance +=
                        (next_score - prev_score) / scale;
                }
            }
        }
    }
}

/// NSGA-II algorithm for multi-objective optimization
pub struct NsgaII<G: Genome> {
    /// Fitness function
    fitness: MultiObjectiveFitness<G>,
    /// Genetic parameters
    params: GeneticParameters,
    /// Non-dominated sorting algorithm
    sorter: NonDominatedSorting<G>,
    /// Initial genomes
    initial_genomes: Vec<G>,
    /// Random number generator
    rng: SmallRng,
}

impl<G: Genome> NsgaII<G> {
    /// Create a new NSGA-II algorithm
    pub fn new(fitness: MultiObjectiveFitness<G>, params: GeneticParameters) -> Self {
        let sorter = NonDominatedSorting::new(fitness.clone());
        
        Self {
            fitness,
            params,
            sorter,
            initial_genomes: Vec::new(),
            rng: SmallRng::from_entropy(),
        }
    }
    
    /// Add an initial genome
    pub fn add_initial_genome(&mut self, genome: G) -> &mut Self {
        self.initial_genomes.push(genome);
        self
    }
    
    /// Run the NSGA-II algorithm
    pub fn run(&mut self) -> Result<Vec<GeneticSolution<G>>> {
        // Initialize population
        let mut population = self.initialize_population();
        
        // Track start time for timeout
        let start_time = Instant::now();
        let timeout = Duration::from_millis(self.params.timeout_ms);
        
        // Main evolution loop
        for generation in 0..self.params.max_generations {
            // Check for timeout
            if start_time.elapsed() > timeout {
                tracing::info!("Evolution timeout after {} generations", generation);
                break;
            }
            
            // Create offspring population through selection, crossover, and mutation
            let offspring = self.create_offspring(&population);
            
            // Combine parent and offspring populations
            let mut combined = population;
            combined.extend(offspring);
            
            // Perform non-dominated sorting
            let fronts = self.sorter.sort(&mut combined);
            
            // Calculate crowding distance
            self.sorter.calculate_crowding_distance(&mut combined, &fronts);
            
            // Select next generation based on rank and crowding distance
            let next_generation = self.select_next_generation(combined, fronts);
            
            // Update population
            population = next_generation;
        }
        
        // Extract Pareto front
        let mut pareto_front = Vec::new();
        
        // Sort population by rank and crowding distance
        let mut sorted_population = population.clone();
        sorted_population.sort_by(|a, b| {
            let rank_cmp = a.rank.cmp(&b.rank);
            if rank_cmp != std::cmp::Ordering::Equal {
                return rank_cmp;
            }
            
            // If ranks are equal, sort by crowding distance (descending)
            b.crowding_distance.partial_cmp(&a.crowding_distance)
                .unwrap_or(std::cmp::Ordering::Equal)
        });
        
        // Extract individuals in the first front (rank 0)
        for individual in sorted_population {
            if individual.rank == 0 {
                pareto_front.push(GeneticSolution {
                    genome: individual.genome,
                    fitness: individual.scores[0], // Use first objective as primary fitness
                    generation: self.params.max_generations,
                });
            }
        }
        
        Ok(pareto_front)
    }
    
    /// Initialize the population
    fn initialize_population(&mut self) -> Vec<MultiObjectiveIndividual<G>> {
        let mut population = Vec::with_capacity(self.params.population_size);
        
        // Use initial genomes
        for genome in &self.initial_genomes {
            let scores = self.fitness.evaluate_all(genome);
            population.push(MultiObjectiveIndividual::new(genome.clone(), scores));
        }
        
        // Generate random genomes to fill the population
        while population.len() < self.params.population_size {
            let genome = G::random(&mut self.rng);
            let scores = self.fitness.evaluate_all(&genome);
            population.push(MultiObjectiveIndividual::new(genome, scores));
        }
        
        population
    }
    
    /// Create offspring through selection, crossover, and mutation
    fn create_offspring(&mut self, population: &[MultiObjectiveIndividual<G>]) -> Vec<MultiObjectiveIndividual<G>> {
        let mut offspring = Vec::with_capacity(population.len());
        
        while offspring.len() < population.len() {
            // Tournament selection
            let parent1 = self.tournament_selection(population);
            let parent2 = self.tournament_selection(population);
            
            // Crossover
            let (mut child1, mut child2) = if self.rng.gen::<f64>() < self.params.crossover_rate {
                parent1.genome.crossover(&parent2.genome, &mut self.rng)
            } else {
                (parent1.genome.clone(), parent2.genome.clone())
            };
            
            // Mutation
            child1.mutate(&mut self.rng, self.params.mutation_rate);
            child2.mutate(&mut self.rng, self.params.mutation_rate);
            
            // Evaluate offspring
            let scores1 = self.fitness.evaluate_all(&child1);
            let scores2 = self.fitness.evaluate_all(&child2);
            
            // Add to offspring population
            offspring.push(MultiObjectiveIndividual::new(child1, scores1));
            
            if offspring.len() < population.len() {
                offspring.push(MultiObjectiveIndividual::new(child2, scores2));
            }
        }
        
        offspring
    }
    
    /// Select the next generation based on rank and crowding distance
    fn select_next_generation(
        &self,
        mut combined: Vec<MultiObjectiveIndividual<G>>,
        fronts: Vec<Vec<usize>>,
    ) -> Vec<MultiObjectiveIndividual<G>> {
        let mut next_generation = Vec::with_capacity(self.params.population_size);
        let mut front_idx = 0;
        
        // Add individuals from each front until we reach the population size
        while next_generation.len() + fronts[front_idx].len() <= self.params.population_size {
            // Add all individuals from the current front
            for &idx in &fronts[front_idx] {
                next_generation.push(combined[idx].clone());
            }
            
            front_idx += 1;
            
            // If we've used all fronts, break
            if front_idx >= fronts.len() {
                break;
            }
        }
        
        // If we need more individuals to fill the population
        if next_generation.len() < self.params.population_size {
            // Sort the current front by crowding distance (descending)
            let mut last_front = Vec::new();
            for &idx in &fronts[front_idx] {
                last_front.push(combined[idx].clone());
            }
            
            last_front.sort_by(|a, b| {
                b.crowding_distance.partial_cmp(&a.crowding_distance)
                    .unwrap_or(std::cmp::Ordering::Equal)
            });
            
            // Add individuals from the last front until we reach the population size
            let remaining = self.params.population_size - next_generation.len();
            for i in 0..remaining {
                next_generation.push(last_front[i].clone());
            }
        }
        
        next_generation
    }
    
    /// Tournament selection based on rank and crowding distance
    fn tournament_selection(&mut self, population: &[MultiObjectiveIndividual<G>]) -> &MultiObjectiveIndividual<G> {
        // Select tournament_size individuals randomly
        let size = self.params.tournament_size.min(population.len());
        let mut best_idx = self.rng.gen_range(0..population.len());
        
        for _ in 1..size {
            let idx = self.rng.gen_range(0..population.len());
            
            // Compare individuals based on rank and crowding distance
            if population[idx].rank < population[best_idx].rank ||
                (population[idx].rank == population[best_idx].rank &&
                 population[idx].crowding_distance > population[best_idx].crowding_distance) {
                best_idx = idx;
            }
        }
        
        &population[best_idx]
    }
}
```

### 4.2. Multi-Objective Metrics and Visualization

**Description:**
Multi-objective metrics and visualization tools help evaluate the quality of Pareto fronts and visualize the trade-offs between objectives.

**Features:**
- Hypervolume indicator
- Inverted generational distance
- Pareto front visualization
- Parallel coordinate plots

**Implementation:**

```rust
/// Multi-objective metrics for evaluating Pareto fronts
pub struct MultiObjectiveMetrics {
    /// Reference point for hypervolume calculation
    reference_point: Vec<f64>,
    /// Whether each objective is minimized
    is_minimizing: Vec<bool>,
}

impl MultiObjectiveMetrics {
    /// Create a new multi-objective metrics calculator
    pub fn new(reference_point: Vec<f64>, is_minimizing: Vec<bool>) -> Self {
        assert_eq!(reference_point.len(), is_minimizing.len(),
            "Reference point and minimization flags must have the same length");
            
        Self {
            reference_point,
            is_minimizing,
        }
    }
    
    /// Calculate hypervolume indicator for a Pareto front
    pub fn hypervolume(&self, pareto_front: &[Vec<f64>]) -> f64 {
        if pareto_front.is_empty() {
            return 0.0;
        }
        
        let dim = self.reference_point.len();
        if dim <= 1 {
            return 0.0;
        }
        
        // Normalize objective values
        let normalized = self.normalize_objectives(pareto_front);
        
        // Use a simplified hypervolume calculation for 2D
        if dim == 2 {
            self.hypervolume_2d(&normalized)
        } else {
            // For higher dimensions, use a more complex algorithm (not implemented here)
            // This would typically use the hypervolume by slicing objectives (HSO) algorithm
            // or similar methods
            0.0
        }
    }
    
    /// Calculate hypervolume for 2D Pareto fronts
    fn hypervolume_2d(&self, pareto_front: &[Vec<f64>]) -> f64 {
        if pareto_front.is_empty() {
            return 0.0;
        }
        
        // Sort points by first objective
        let mut sorted = pareto_front.to_vec();
        sorted.sort_by(|a, b| {
            a[0].partial_cmp(&b[0]).unwrap_or(std::cmp::Ordering::Equal)
        });
        
        // Calculate area
        let mut hypervolume = 0.0;
        let mut prev_x = sorted[0][0];
        let mut prev_y = sorted[0][1];
        
        for point in &sorted[1..] {
            let x = point[0];
            let y = point[1];
            
            // Add rectangular area
            hypervolume += (x - prev_x) * prev_y;
            
            prev_x = x;
            prev_y = y.max(prev_y);
        }
        
        // Add final rectangle
        hypervolume += (1.0 - prev_x) * prev_y;
        
        hypervolume
    }
    
    /// Normalize objective values to [0,1] range
    fn normalize_objectives(&self, pareto_front: &[Vec<f64>]) -> Vec<Vec<f64>> {
        let dim = self.reference_point.len();
        
        // Find min and max values for each objective
        let mut min_vals = vec![f64::INFINITY; dim];
        let mut max_vals = vec![f64::NEG_INFINITY; dim];
        
        for point in pareto_front {
            for i in 0..dim {
                min_vals[i] = min_vals[i].min(point[i]);
                max_vals[i] = max_vals[i].max(point[i]);
            }
        }
        
        // Normalize points
        let mut normalized = Vec::with_capacity(pareto_front.len());
        
        for point in pareto_front {
            let mut norm_point = Vec::with_capacity(dim);
            
            for i in 0..dim {
                let range = (max_vals[i] - min_vals[i]).max(1e-10);
                let value = if self.is_minimizing[i] {
                    // For minimization: invert so that smaller values are better
                    1.0 - (point[i] - min_vals[i]) / range
                } else {
                    // For maximization: larger values are better
                    (point[i] - min_vals[i]) / range
                };
                
                norm_point.push(value);
            }
            
            normalized.push(norm_point);
        }
        
        normalized
    }
    
    /// Calculate inverted generational distance
    pub fn inverted_generational_distance(&self, pareto_front: &[Vec<f64>], reference_front: &[Vec<f64>]) -> f64 {
        if pareto_front.is_empty() || reference_front.is_empty() {
            return f64::INFINITY;
        }
        
        let mut sum_distances = 0.0;
        
        for ref_point in reference_front {
            // Find minimum distance to any point in the Pareto front
            let min_distance = pareto_front.iter()
                .map(|point| self.euclidean_distance(point, ref_point))
                .fold(f64::INFINITY, f64::min);
                
            sum_distances += min_distance.powi(2);
        }
        
        let igd = (sum_distances / reference_front.len() as f64).sqrt();
        igd
    }
    
    /// Calculate Euclidean distance between two points
    fn euclidean_distance(&self, a: &[f64], b: &[f64]) -> f64 {
        assert_eq!(a.len(), b.len(), "Points must have the same dimension");
        
        let sum_squared = a.iter().zip(b.iter())
            .map(|(a_i, b_i)| (a_i - b_i).powi(2))
            .sum::<f64>();
            
        sum_squared.sqrt()
    }
}

#[cfg(feature = "visualization")]
pub mod visualization {
    use super::*;
    use plotters::prelude::*;
    
    /// Visualize a 2D Pareto front
    pub fn plot_pareto_front_2d(
        pareto_front: &[Vec<f64>],
        output_path: &str,
        title: &str,
        x_label: &str,
        y_label: &str,
    ) -> Result<(), Box<dyn std::error::Error>> {
        let root = BitMapBackend::new(output_path, (800, 600)).into_drawing_area();
        root.fill(&WHITE)?;
        
        // Find min and max values
        let mut min_x = f64::INFINITY;
        let mut max_x = f64::NEG_INFINITY;
        let mut min_y = f64::INFINITY;
        let mut max_y = f64::NEG_INFINITY;
        
        for point in pareto_front {
            min_x = min_x.min(point[0]);
            max_x = max_x.max(point[0]);
            min_y = min_y.min(point[1]);
            max_y = max_y.max(point[1]);
        }
        
        // Add some margin
        let x_margin = (max_x - min_x) * 0.1;
        let y_margin = (max_y - min_y) * 0.1;
        
        // Create chart
        let mut chart = ChartBuilder::on(&root)
            .caption(title, ("sans-serif", 30).into_font())
            .margin(5)
            .x_label_area_size(30)
            .y_label_area_size(40)
            .build_cartesian_2d(
                (min_x - x_margin)..(max_x + x_margin),
                (min_y - y_margin)..(max_y + y_margin)
            )?;
            
        chart.configure_mesh()
            .x_desc(x_label)
            .y_desc(y_label)
            .axis_desc_style(("sans-serif", 15))
            .draw()?;
            
        // Plot Pareto front points
        chart.draw_series(
            pareto_front.iter().map(|point| {
                Circle::new((point[0], point[1]), 3, BLUE.filled())
            })
        )?;
        
        // Draw line connecting points in order
        let mut sorted = pareto_front.to_vec();
        sorted.sort_by(|a, b| {
            a[0].partial_cmp(&b[0]).unwrap_or(std::cmp::Ordering::Equal)
        });
        
        chart.draw_series(LineSeries::new(
            sorted.iter().map(|point| (point[0], point[1])),
            &RED,
        ))?;
        
        root.present()?;
        
        Ok(())
    }
    
    /// Create a parallel coordinate plot for multi-objective solutions
    pub fn plot_parallel_coordinates(
        pareto_front: &[Vec<f64>],
        output_path: &str,
        title: &str,
        objective_names: &[&str],
    ) -> Result<(), Box<dyn std::error::Error>> {
        let root = BitMapBackend::new(output_path, (800, 600)).into_drawing_area();
        root.fill(&WHITE)?;
        
        let num_objectives = objective_names.len();
        
        // Find min and max values for each objective
        let mut min_vals = vec![f64::INFINITY; num_objectives];
        let mut max_vals = vec![f64::NEG_INFINITY; num_objectives];
        
        for point in pareto_front {
            for i in 0..num_objectives {
                min_vals[i] = min_vals[i].min(point[i]);
                max_vals[i] = max_vals[i].max(point[i]);
            }
        }
        
        // Create chart
        let mut chart = ChartBuilder::on(&root)
            .caption(title, ("sans-serif", 30).into_font())
            .margin(5)
            .x_label_area_size(30)
            .y_label_area_size(40)
            .build_cartesian_2d(
                0..(num_objectives as i32 - 1),
                0f64..1f64
            )?;
            
        chart.configure_mesh()
            .disable_x_mesh()
            .disable_y_mesh()
            .x_labels(num_objectives)
            .x_label_formatter(&|x| {
                objective_names[*x as usize].to_string()
            })
            .draw()?;
            
        // Draw each solution as a line
        for point in pareto_front {
            let normalized: Vec<(i32, f64)> = point.iter().enumerate()
                .map(|(i, &val)| {
                    let range = (max_vals[i] - min_vals[i]).max(1e-10);
                    let norm_val = (val - min_vals[i]) / range;
                    (i as i32, norm_val)
                })
                .collect();
                
            chart.draw_series(LineSeries::new(
                normalized,
                &HSLColor(
                    rand::random::<f64>(), // Random hue
                    0.8, // High saturation
                    0.5, // Medium lightness
                ).mix(0.6), // 60% opacity
            ))?;
        }
        
        root.present()?;
        
        Ok(())
    }
}
```

## 5. Visualization Components

### 5.1 Evolution Progress Visualization

**Description:**
Evolution progress visualization allows users to monitor the genetic algorithm's performance in real-time and analyze the results after completion.

**Features:**
- Fitness trend visualization
- Population diversity visualization
- Parameter adaptation visualization
- Generation-by-generation animation

**Implementation:**

```rust
#[cfg(feature = "visualization")]
pub mod evolution_visualization {
    use super::*;
    use plotters::prelude::*;
    use std::path::Path;
    
    /// Evolution statistics for visualization
    #[derive(Clone, Debug, Serialize, Deserialize)]
    pub struct EvolutionStats {
        /// Generation number
        pub generation: usize,
        /// Best fitness
        pub best_fitness: f64,
        /// Average fitness
        pub average_fitness: f64,
        /// Worst fitness
        pub worst_fitness: f64,
        /// Population diversity
        pub diversity: f64,
        /// Mutation rate
        pub mutation_rate: f64,
        /// Crossover rate
        pub crossover_rate: f64,
        /// Time stamp
        pub timestamp: f64,
        /// Additional metrics
        pub metrics: HashMap<String, f64>,
    }
    
    /// Evolution visualization manager
    pub struct EvolutionVisualizer {
        /// Evolution statistics
        stats: Vec<EvolutionStats>,
        /// Output directory
        output_dir: String,
        /// Start time
        start_time: Instant,
    }
    
    impl EvolutionVisualizer {
        /// Create a new evolution visualizer
        pub fn new(output_dir: &str) -> Result<Self, Box<dyn std::error::Error>> {
            // Create output directory if it doesn't exist
            std::fs::create_dir_all(output_dir)?;
            
            Ok(Self {
                stats: Vec::new(),
                output_dir: output_dir.to_string(),
                start_time: Instant::now(),
            })
        }
        
        /// Record evolution statistics for the current generation
        pub fn record_stats(
            &mut self,
            generation: usize,
            best_fitness: f64,
            average_fitness: f64,
            worst_fitness: f64,
            diversity: f64,
            mutation_rate: f64,
            crossover_rate: f64,
            metrics: HashMap<String, f64>,
        ) {
            let stats = EvolutionStats {
                generation,
                best_fitness,
                average_fitness,
                worst_fitness,
                diversity,
                mutation_rate,
                crossover_rate,
                timestamp: self.start_time.elapsed().as_secs_f64(),
                metrics,
            };
            
            self.stats.push(stats);
        }
        
        /// Plot fitness trends
        pub fn plot_fitness_trends(&self) -> Result<String, Box<dyn std::error::Error>> {
            let output_path = format!("{}/fitness_trends.png", self.output_dir);
            let root = BitMapBackend::new(&output_path, (800, 600)).into_drawing_area();
            root.fill(&WHITE)?;
            
            let min_fitness = self.stats.iter()
                .map(|stats| stats.worst_fitness)
                .fold(f64::INFINITY, f64::min);
                
            let max_fitness = self.stats.iter()
                .map(|stats| stats.best_fitness)
                .fold(f64::NEG_INFINITY, f64::max);
                
            let max_generation = self.stats.last()
                .map(|stats| stats.generation)
                .unwrap_or(0);
                
            // Create chart
            let mut chart = ChartBuilder::on(&root)
                .caption("Fitness Evolution", ("sans-serif", 30).into_font())
                .margin(5)
                .x_label_area_size(30)
                .y_label_area_size(40)
                .build_cartesian_2d(
                    0..(max_generation + 1),
                    (min_fitness - 0.1)..(max_fitness + 0.1)
                )?;
                
            chart.configure_mesh()
                .x_desc("Generation")
                .y_desc("Fitness")
                .axis_desc_style(("sans-serif", 15))
                .draw()?;
                
            // Plot best fitness
            chart.draw_series(LineSeries::new(
                self.stats.iter().map(|stats| (stats.generation, stats.best_fitness)),
                &RED,
            ))?
            .label("Best Fitness")
            .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RED));
            
            // Plot average fitness
            chart.draw_series(LineSeries::new(
                self.stats.iter().map(|stats| (stats.generation, stats.average_fitness)),
                &BLUE,
            ))?
            .label("Average Fitness")
            .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &BLUE));
            
            // Plot worst fitness
            chart.draw_series(LineSeries::new(
                self.stats.iter().map(|stats| (stats.generation, stats.worst_fitness)),
                &GREEN,
            ))?
            .label("Worst Fitness")
            .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &GREEN));
            
            chart.configure_series_labels()
                .background_style(&WHITE.mix(0.8))
                .border_style(&BLACK)
                .draw()?;
                
            root.present()?;
            
            Ok(output_path)
        }
        
        /// Plot diversity trend
        pub fn plot_diversity_trend(&self) -> Result<String, Box<dyn std::error::Error>> {
            let output_path = format!("{}/diversity_trend.png", self.output_dir);
            let root = BitMapBackend::new(&output_path, (800, 600)).into_drawing_area();
            root.fill(&WHITE)?;
            
            let max_generation = self.stats.last()
                .map(|stats| stats.generation)
                .unwrap_or(0);
                
            // Create chart
            let mut chart = ChartBuilder::on(&root)
                .caption("Population Diversity", ("sans-serif", 30).into_font())
                .margin(5)
                .x_label_area_size(30)
                .y_label_area_size(40)
                .build_cartesian_2d(
                    0..(max_generation + 1),
                    0.0..1.0
                )?;
                
            chart.configure_mesh()
                .x_desc("Generation")
                .y_desc("Diversity")
                .axis_desc_style(("sans-serif", 15))
                .draw()?;
                
            // Plot diversity
            chart.draw_series(LineSeries::new(
                self.stats.iter().map(|stats| (stats.generation, stats.diversity)),
                &BLUE,
            ))?;
            
            root.present()?;
            
            Ok(output_path)
        }
        
        /// Plot parameter adaptation
        pub fn plot_parameter_adaptation(&self) -> Result<String, Box<dyn std::error::Error>> {
            let output_path = format!("{}/parameter_adaptation.png", self.output_dir);
            let root = BitMapBackend::new(&output_path, (800, 600)).into_drawing_area();
            root.fill(&WHITE)?;
            
            let max_generation = self.stats.last()
                .map(|stats| stats.generation)
                .unwrap_or(0);
                
            // Create chart
            let mut chart = ChartBuilder::on(&root)
                .caption("Parameter Adaptation", ("sans-serif", 30).into_font())
                .margin(5)
                .x_label_area_size(30)
                .y_label_area_size(40)
                .build_cartesian_2d(
                    0..(max_generation + 1),
                    0.0..1.0
                )?;
                
            chart.configure_mesh()
                .x_desc("Generation")
                .y_desc("Parameter Value")
                .axis_desc_style(("sans-serif", 15))
                .draw()?;
                
            // Plot mutation rate
            chart.draw_series(LineSeries::new(
                self.stats.iter().map(|stats| (stats.generation, stats.mutation_rate)),
                &RED,
            ))?
            .label("Mutation Rate")
            .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RED));
            
            // Plot crossover rate
            chart.draw_series(LineSeries::new(
                self.stats.iter().map(|stats| (stats.generation, stats.crossover_rate)),
                &BLUE,
            ))?
            .label("Crossover Rate")
            .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &BLUE));
            
            chart.configure_series_labels()
                .background_style(&WHITE.mix(0.8))
                .border_style(&BLACK)
                .draw()?;
                
            root.present()?;
            
            Ok(output_path)
        }
        
        /// Generate evolution visualization report
        pub fn generate_report(&self) -> Result<String, Box<dyn std::error::Error>> {
            let report_path = format!("{}/evolution_report.html", self.output_dir);
            
            // Generate fitness trends plot
            let fitness_path = self.plot_fitness_trends()?;
            let diversity_path = self.plot_diversity_trend()?;
            let parameters_path = self.plot_parameter_adaptation()?;
            
            // Generate animated GIF (if enabled)
            #[cfg(feature = "animation")]
            let animation_path = self.generate_animation()?;
            
            // Create HTML report
            let mut html = String::new();
            html.push_str("<!DOCTYPE html>\n");
            html.push_str("<html>\n");
            html.push_str("<head>\n");
            html.push_str("  <title>Evolution Visualization Report</title>\n");
            html.push_str("  <style>\n");
            html.push_str("    body { font-family: Arial, sans-serif; margin: 20px; }\n");
            html.push_str("    h1 { color: #333; }\n");
            html.push_str("    .plot { margin: 20px 0; }\n");
            html.push_str("    .plot img { max-width: 100%; }\n");
            html.push_str("    .stats { margin: 20px 0; }\n");
            html.push_str("    table { border-collapse: collapse; width: 100%; }\n");
            html.push_str("    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n");
            html.push_str("    th { background-color: #f2f2f2; }\n");
            html.push_str("    tr:nth-child(even) { background-color: #f9f9f9; }\n");
            html.push_str("  </style>\n");
            html.push_str("</head>\n");
            html.push_str("<body>\n");
            html.push_str("  <h1>Evolution Visualization Report</h1>\n");
            
            // Add fitness trends plot
            html.push_str("  <div class=\"plot\">\n");
            html.push_str("    <h2>Fitness Trends</h2>\n");
            html.push_str(&format!("    <img src=\"{}\" alt=\"Fitness Trends\" />\n",
                Path::new(&fitness_path).file_name().unwrap().to_string_lossy()));
            html.push_str("  </div>\n");
            
            // Add diversity trend plot
            html.push_str("  <div class=\"plot\">\n");
            html.push_str("    <h2>Population Diversity</h2>\n");
            html.push_str(&format!("    <img src=\"{}\" alt=\"Diversity Trend\" />\n",
                Path::new(&diversity_path).file_name().unwrap().to_string_lossy()));
            html.push_str("  </div>\n");
            
            // Add parameter adaptation plot
            html.push_str("  <div class=\"plot\">\n");
            html.push_str("    <h2>Parameter Adaptation</h2>\n");
            html.push_str(&format!("    <img src=\"{}\" alt=\"Parameter Adaptation\" />\n",
                Path::new(&parameters_path).file_name().unwrap().to_string_lossy()));
            html.push_str("  </div>\n");
            
            // Add animation if available
            #[cfg(feature = "animation")]
            {
                html.push_str("  <div class=\"plot\">\n");
                html.push_str("    <h2>Evolution Animation</h2>\n");
                html.push_str(&format!("    <img src=\"{}\" alt=\"Evolution Animation\" />\n",
                    Path::new(&animation_path).file_name().unwrap().to_string_lossy()));
                html.push_str("  </div>\n");
            }
            
            // Add statistics table
            html.push_str("  <div class=\"stats\">\n");
            html.push_str("    <h2>Evolution Statistics</h2>\n");
            html.push_str("    <table>\n");
            html.push_str("      <tr>\n");
            html.push_str("        <th>Generation</th>\n");
            html.push_str("        <th>Best Fitness</th>\n");
            html.push_str("        <th>Average Fitness</th>\n");
            html.push_str("        <th>Worst Fitness</th>\n");
            html.push_str("        <th>Diversity</th>\n");
            html.push_str("        <th>Mutation Rate</th>\n");
            html.push_str("        <th>Crossover Rate</th>\n");
            html.push_str("      </tr>\n");
            
            // Add rows for each generation
            for stats in &self.stats {
                html.push_str("      <tr>\n");
                html.push_str(&format!("        <td>{}</td>\n", stats.generation));
                html.push_str(&format!("        <td>{:.4}</td>\n", stats.best_fitness));
                html.push_str(&format!("        <td>{:.4}</td>\n", stats.average_fitness));
                html.push_str(&format!("        <td>{:.4}</td>\n", stats.worst_fitness));
                html.push_str(&format!("        <td>{:.4}</td>\n", stats.diversity));
                html.push_str(&format!("        <td>{:.4}</td>\n", stats.mutation_rate));
                html.push_str(&format!("        <td>{:.4}</td>\n", stats.crossover_rate));
                html.push_str("      </tr>\n");
            }
            
            html.push_str("    </table>\n");
            html.push_str("  </div>\n");
            
            html.push_str("</body>\n");
            html.push_str("</html>\n");
            
            // Write HTML report
            std::fs::write(&report_path, html)?;
            
            Ok(report_path)
        }
        
        /// Export evolution statistics to JSON
        pub fn export_stats(&self) -> Result<String, Box<dyn std::error::Error>> {
            let stats_path = format!("{}/evolution_stats.json", self.output_dir);
            let json = serde_json::to_string_pretty(&self.stats)?;
            std::fs::write(&stats_path, json)?;
            Ok(stats_path)
        }
        
        #[cfg(feature = "animation")]
        fn generate_animation(&self) -> Result<String, Box<dyn std::error::Error>> {
            // Animation implementation would go here
            // This would typically create a series of frames and combine them into a GIF
            Ok(String::new())
        }
    }
}
```

## 6. Implementation Plan

### 6.1 Phase 1: Selection Methods (Weeks 1-2)
- Implement rank-based selection
- Add stochastic universal sampling
- Update selection interface to support all methods
- Create benchmarks and tests for selection methods

### 6.2 Phase 2: Adaptive Parameter Tuning (Weeks 2-3)
- Implement self-adaptive parameter encoding
- Add rule-based parameter control
- Integrate adaptive mechanisms with genetic engine
- Create visualization tools for parameter adaptation

### 6.3 Phase 3: Multi-Objective Optimization (Weeks 3-5)
- Implement NSGA-II algorithm
- Add Pareto front extraction and analysis
- Create multi-objective metrics
- Develop visualization tools for Pareto fronts

### 6.4 Phase 4: Visualization Components (Weeks 5-6)
- Implement evolution progress visualization
- Add population diversity visualization
- Create parameter adaptation visualization
- Develop evolution animation capabilities

## 7. Acceptance Criteria

### 7.1 Selection Methods
- All selection methods correctly implemented
- Selection bias and spread within acceptable limits
- Performance overhead less than 10% compared to tournament selection
- Comprehensive tests for all selection methods

### 7.2 Adaptive Parameter Tuning
- Self-adaptive parameters correctly encoded in genomes
- Rule-based control applies parameter adjustments as expected
- Performance improvement of at least 15% for test problems compared to fixed parameters
- Visualization tools for parameter adaptation

### 7.3 Multi-Objective Optimization
- NSGA-II correctly identifies Pareto-optimal solutions
- Hypervolume indicator and other metrics correctly calculated
- Performance comparable to state-of-the-art implementations
- Visualization tools for Pareto fronts

### 7.4 Visualization Components
- Evolution progress visualization with multiple metrics
- Population diversity visualization
- Parameter adaptation visualization
- Generation-by-generation animation capabilities

## 8. Conclusion

This expansion specification outlines a comprehensive plan for enhancing the HMS Genetic Engine in Iteration 1 with additional selection methods, adaptive parameter tuning, multi-objective optimization, and visualization components. These enhancements will make the genetic engine more versatile, powerful, and user-friendly for a wide range of optimization problems.

The implementations are designed to be efficient, maintainable, and extensible, with comprehensive documentation and testing to ensure reliability and ease of use. The modular design allows users to mix and match features as needed for their specific applications, while the visualization tools provide valuable insights into the evolution process.