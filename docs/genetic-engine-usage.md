# Genetic Engine Usage Guide

## Overview

The Genetic Engine is a high-performance, flexible implementation of genetic algorithms for the HMS ecosystem. It provides both synchronous and asynchronous implementations, with support for parallel fitness evaluation using Rayon and tokio for async operations.

This guide covers:
1. Basic concepts and terminology
2. Core components and architecture
3. Using the generic engine
4. Working with text genomes
5. GitHub repository integration
6. Creating custom genome implementations
7. Performance optimizations
8. Examples and use cases

## Basic Concepts

### Genetic Algorithms

Genetic algorithms are optimization techniques inspired by natural evolution. They work by:

1. **Initialization**: Creating an initial population of potential solutions
2. **Evaluation**: Assessing each solution's fitness
3. **Selection**: Choosing the best solutions for reproduction
4. **Crossover**: Combining solutions to create offspring
5. **Mutation**: Introducing random variations
6. **Replacement**: Creating a new generation and repeating the process

### Key Terms

- **Genome**: A representation of a potential solution (equivalent to chromosomes in biology)
- **Population**: A collection of genomes being evolved
- **Fitness Function**: Evaluates how good a solution is, returning a score
- **Selection**: Method for choosing which solutions to reproduce
- **Crossover**: Combining parts of two solutions to create new ones
- **Mutation**: Small random changes to solutions to explore new possibilities
- **Elitism**: Preserving the best solutions unchanged across generations
- **Constraints**: Rules that solutions must satisfy

## Core Components

### Genome

The `Genome` trait represents a unit of genetic information:

```rust
pub trait Genome: Clone + Send + Sync + 'static {
    fn random(rng: &mut SmallRng) -> Self;
    fn crossover(&self, other: &Self, rng: &mut SmallRng) -> (Self, Self);
    fn mutate(&mut self, rng: &mut SmallRng, rate: f64);
}
```

### Fitness Functions

Two traits for evaluating genomes:

```rust
// Synchronous fitness function
pub trait FitnessFunction<G: Genome>: Send + Sync + 'static {
    fn fitness(&self, genome: &G) -> f64;
}

// Asynchronous fitness function
#[async_trait]
pub trait AsyncFitnessFunction<G: Genome>: Send + Sync + 'static {
    async fn fitness(&self, genome: &G) -> Result<f64>;
}
```

### Genetic Engines

Two main engine implementations:

1. `GeneticEngine<G, F>`: Synchronous engine for CPU-bound fitness functions
2. `AsyncGeneticEngine<G, F>`: Asynchronous engine for I/O-bound fitness functions

Both use a builder pattern for configuration:

```rust
let engine = GeneticEngine::builder()
    .with_population_size(50)
    .with_max_generations(100)
    .with_mutation_rate(0.1)
    .with_crossover_rate(0.7)
    .with_fitness_function(my_fitness_function)
    .build()?;
```

### Constraints

Constraints define rules that valid solutions must satisfy:

```rust
pub enum GeneticConstraint<G> {
    Custom {
        description: String,
        validator: Arc<dyn Fn(&G) -> bool + Send + Sync>,
    },
    // More constraint types can be added here
}
```

## Using the Generic Engine

### Creating a Basic Engine

```rust
use hms_concept_analyzer::{
    GeneticParameters, SelectionMethod,
    GeneticEngine, FitnessFunction, TextGenome
};

// Define a fitness function
struct MyFitness;

impl FitnessFunction<TextGenome> for MyFitness {
    fn fitness(&self, genome: &TextGenome) -> f64 {
        // Calculate fitness (example: count 'a's)
        let a_count = genome.text.chars().filter(|&c| c == 'a').count();
        a_count as f64 / genome.text.len().max(1) as f64
    }
}

// Create the engine
let params = GeneticParameters {
    population_size: 50,
    max_generations: 100,
    mutation_rate: 0.1,
    crossover_rate: 0.7,
    elite_count: 3,
    selection_method: SelectionMethod::Tournament,
    tournament_size: 3,
    timeout_ms: 60000,
    fitness_threshold: 0.9,
};

let fitness_function = MyFitness;
let mut engine = GeneticEngine::builder()
    .with_fitness_function(fitness_function)
    .build()?;

// Run evolution
let solution = engine.evolve()?;

println!("Best solution: {}", solution.genome.text);
println!("Fitness: {}", solution.fitness);
println!("Found in generation: {}", solution.generation);
```

### Using Constraints

```rust
use hms_concept_analyzer::{text_constraints, TextGenome};

// Add constraints to the engine
let mut engine = GeneticEngine::builder()
    .with_fitness_function(fitness_function)
    .with_constraint(text_constraints::min_length(10))
    .with_constraint(text_constraints::must_contain("hello"))
    .with_constraint(text_constraints::must_not_contain("error"))
    .with_constraint(text_constraints::matches_regex("^[a-z]+$")?)
    .build()?;
```

### Parallel Fitness Evaluation

```rust
// Uses Rayon for parallel fitness evaluation
let solution = engine.evolve_parallel()?;
```

## Working with Text Genomes

The `TextGenome` is a simple implementation provided for text-based solutions:

```rust
let genome = TextGenome { text: "hello world".to_string() };

// Create a random text genome
let random_genome = TextGenome::random(&mut SmallRng::from_entropy());

// Crossover two genomes
let (child1, child2) = genome.crossover(&random_genome, &mut SmallRng::from_entropy());

// Mutate a genome
let mut mutated = genome.clone();
mutated.mutate(&mut SmallRng::from_entropy(), 0.5);
```

## GitHub Repository Integration

### Finding Optimal Repositories

```rust
use hms_concept_analyzer::{
    RepositorySelectionEngine, RepositorySolutionProcessor,
    concept_registry::{GapInfo, GapType},
    repository_constraints,
};

// Define a gap
let gap = GapInfo {
    gap_type: GapType::MissingFunctionality,
    concept_id: "visualization".to_string(),
    description: "Missing visualization capabilities for concept maps".to_string(),
    suggestion: "Find a library for interactive graph visualization".to_string(),
};

// Required features
let required_features = vec![
    "visualization".to_string(),
    "interactive".to_string(),
    "graph".to_string(),
];

// Create clients
let github_client = GithubClient::new().await?;
let llm_client = OpenAIClient::new()?;

// Create the repository selection engine
let mut engine = RepositorySelectionEngine::new(
    gap.clone(),
    required_features,
    github_client,
    llm_client,
    None, // Use default parameters
).await?;

// Add constraints
engine.add_constraint(repository_constraints::has_language(
    vec!["rust", "javascript", "typescript"]
));
engine.add_constraint(repository_constraints::min_stars(10));

// Initialize population from GitHub search
engine.initialize_population().await?;

// Evolve to find the best solution
let solution = engine.evolve().await?;

// Generate a detailed report
let processor = RepositorySolutionProcessor::new(registry);
let report = processor.generate_report(&solution, &gap);
```

## Creating Custom Genome Implementations

### Implementing the Genome Trait

```rust
use rand::rngs::SmallRng;
use serde::{Serialize, Deserialize};
use hms_concept_analyzer::Genome;

#[derive(Clone, Debug, Serialize, Deserialize)]
struct MyCustomGenome {
    values: Vec<f64>,
}

impl Genome for MyCustomGenome {
    fn random(rng: &mut SmallRng) -> Self {
        let mut values = Vec::with_capacity(10);
        for _ in 0..10 {
            values.push(rng.gen_range(0.0..1.0));
        }
        Self { values }
    }
    
    fn crossover(&self, other: &Self, rng: &mut SmallRng) -> (Self, Self) {
        // Single-point crossover
        let point = rng.gen_range(0..self.values.len());
        
        let mut child1_values = Vec::new();
        let mut child2_values = Vec::new();
        
        for i in 0..self.values.len() {
            if i < point {
                child1_values.push(self.values[i]);
                child2_values.push(other.values[i]);
            } else {
                child1_values.push(other.values[i]);
                child2_values.push(self.values[i]);
            }
        }
        
        (
            Self { values: child1_values },
            Self { values: child2_values },
        )
    }
    
    fn mutate(&mut self, rng: &mut SmallRng, rate: f64) {
        for value in &mut self.values {
            if rng.gen::<f64>() < rate {
                // Add a small random value
                *value += rng.gen_range(-0.1..0.1);
                // Ensure it stays in range
                *value = value.min(1.0).max(0.0);
            }
        }
    }
}
```

### Implementing Fitness Functions

```rust
// Synchronous fitness function
struct MyFitness;

impl FitnessFunction<MyCustomGenome> for MyFitness {
    fn fitness(&self, genome: &MyCustomGenome) -> f64 {
        // Simple example: sum of values
        genome.values.iter().sum()
    }
}

// Asynchronous fitness function
struct MyAsyncFitness {
    client: Arc<SomeExternalClient>,
}

#[async_trait]
impl AsyncFitnessFunction<MyCustomGenome> for MyAsyncFitness {
    async fn fitness(&self, genome: &MyCustomGenome) -> Result<f64> {
        // Call an external API to evaluate the genome
        let result = self.client.evaluate(genome.values.clone()).await?;
        Ok(result.score)
    }
}
```

## Performance Optimizations

The genetic engine includes several optimizations:

1. **SmallRng**: Uses a faster, thread-local RNG for better performance
2. **Parallel Fitness Evaluation**: Uses Rayon for CPU-bound fitness calculations
3. **Async/Await**: Supports I/O-bound fitness functions with tokio
4. **Efficient Selection**: Optimized tournament and roulette selection
5. **Early Stopping**: Terminates when fitness threshold is reached
6. **Convergence Detection**: Detects when fitness plateaus
7. **Timeout Protection**: Prevents runaway execution

To maximize performance:

- Use `evolve_parallel()` for CPU-bound fitness functions
- Use the async engine for I/O-bound fitness functions
- Set appropriate population size and generation count
- Use early stopping with a reasonable fitness threshold
- Choose the right selection method for your problem
- Consider caching fitness results for expensive calculations

## Examples and Use Cases

### Optimizing Configuration Parameters

```rust
#[derive(Clone, Debug, Serialize, Deserialize)]
struct ConfigGenome {
    batch_size: usize,
    learning_rate: f64,
    hidden_size: usize,
    dropout: f64,
}

impl Genome for ConfigGenome {
    // Implementation details...
}

// Fitness function evaluates model performance with these parameters
struct ModelPerformance;

impl FitnessFunction<ConfigGenome> for ModelPerformance {
    fn fitness(&self, genome: &ConfigGenome) -> f64 {
        // Train and evaluate a model with these parameters
        // Return validation accuracy or similar metric
    }
}
```

### Finding Optimal Text Templates

```rust
// Use TextGenome to find optimal text templates
// Example: generating SQL queries, configuration files, etc.

struct TemplatePerformance {
    test_data: Vec<TestCase>,
}

impl FitnessFunction<TextGenome> for TemplatePerformance {
    fn fitness(&self, genome: &TextGenome) -> f64 {
        // Evaluate the template against test cases
        let template = &genome.text;
        let success_count = self.test_data.iter()
            .filter(|test| test.evaluate(template))
            .count();
            
        success_count as f64 / self.test_data.len() as f64
    }
}
```

### Finding Optimal API Integrations

```rust
// Use RepositorySelectionEngine to find optimal libraries for integration
// Example: finding visualization libraries, database connectors, etc.

async fn find_optimal_api() -> Result<()> {
    let gap = GapInfo {
        gap_type: GapType::MissingFunctionality,
        concept_id: "database".to_string(),
        description: "Need a high-performance database connector".to_string(),
        suggestion: "Find a library for PostgreSQL integration".to_string(),
    };
    
    let required_features = vec![
        "postgresql".to_string(),
        "async".to_string(),
        "connection-pool".to_string(),
    ];
    
    let mut engine = RepositorySelectionEngine::new(
        gap.clone(),
        required_features,
        github_client,
        llm_client,
        None,
    ).await?;
    
    let solution = engine.evolve().await?;
    
    // Use the solution to integrate with your system
    Ok(())
}
```

## Conclusion

The Genetic Engine provides a powerful, flexible framework for evolutionary optimization in the HMS ecosystem. By abstracting the core algorithm while providing specialized implementations for common tasks, it enables efficient solution finding for a wide range of problems.

For more details, see:
- [Genetic Engine Architecture](genetic_engine_architecture.md)
- [API Documentation](../src/concept_analyzer/genetic_engine.rs)
- [GitHub Repository Integration](../src/concept_analyzer/genetic_github.rs)