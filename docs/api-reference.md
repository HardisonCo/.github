# Economic Theorem Prover API Reference

This document provides comprehensive reference documentation for the Economic Theorem Prover API, allowing programmatic integration with other systems and applications.

## API Overview

The Economic Theorem Prover provides a REST API for proving economic theorems, managing proof strategies, and configuring system behavior. The API follows REST conventions and uses JSON for request and response bodies.

### Base URL

```
http://localhost:8000/api/v1
```

The default port is 8000, but this can be configured when starting the API server.

### Authentication

The API supports both API key authentication and JWT token-based authentication:

- API Key: Include your API key in the `X-API-Key` header
- JWT: Include the JWT token in the `Authorization` header as a Bearer token

For local development, authentication can be disabled with the `--no-auth` flag.

## Theorem Endpoints

### List Theorems

```
GET /theorems
```

Retrieves a list of all theorems in the repository.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `domain` | string | Filter by economic domain (e.g., "microeconomics") |
| `status` | string | Filter by proof status ("proven", "unproven", "in_progress") |
| `limit` | integer | Maximum number of results (default: 50) |
| `offset` | integer | Pagination offset (default: 0) |

**Response:**

```json
{
  "theorems": [
    {
      "id": "theorem-123",
      "name": "utility_maximization",
      "domain": "microeconomics",
      "status": "proven",
      "created_at": "2023-04-15T10:30:00Z",
      "proven_at": "2023-04-15T10:32:15Z",
      "proof_steps": 12
    },
    ...
  ],
  "total": 157,
  "limit": 50,
  "offset": 0
}
```

### Get Theorem

```
GET /theorems/{id}
```

Retrieves detailed information about a specific theorem.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | ID of the theorem to retrieve |

**Response:**

```json
{
  "id": "theorem-123",
  "name": "utility_maximization",
  "domain": "microeconomics",
  "status": "proven",
  "created_at": "2023-04-15T10:30:00Z",
  "proven_at": "2023-04-15T10:32:15Z",
  "source": "theorem utility_maximization {U : Utility} {B : Budget} {x : Bundle} (h : Maximizes U x B) : MRS U x = PriceRatio B := ...",
  "proof": {
    "steps": [
      {
        "tactic": "intro",
        "goal": "Maximizes U x B → MRS U x = PriceRatio B"
      },
      {
        "tactic": "apply first_order_condition",
        "goal": "First_Order_Condition U x B"
      },
      ...
    ],
    "time_ms": 320,
    "strategy_id": "strategy-456"
  },
  "dependencies": [
    "theorem-100",
    "theorem-101"
  ]
}
```

### Create Theorem

```
POST /theorems
```

Creates a new theorem.

**Request:**

```json
{
  "name": "law_of_demand",
  "domain": "microeconomics",
  "source": "theorem law_of_demand {p₁ p₂ : Price} {x₁ x₂ : Quantity} (h₁ : p₁ < p₂) (h₂ : OptimalDemand p₁ x₁) (h₃ : OptimalDemand p₂ x₂) : x₁ ≥ x₂ := ..."
}
```

**Response:**

```json
{
  "id": "theorem-124",
  "name": "law_of_demand",
  "domain": "microeconomics",
  "status": "unproven",
  "created_at": "2023-04-16T09:15:00Z",
  "source": "theorem law_of_demand {p₁ p₂ : Price} {x₁ x₂ : Quantity} (h₁ : p₁ < p₂) (h₂ : OptimalDemand p₁ x₁) (h₃ : OptimalDemand p₂ x₂) : x₁ ≥ x₂ := ..."
}
```

### Prove Theorem

```
POST /theorems/{id}/prove
```

Initiates a proof attempt for the specified theorem.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | ID of the theorem to prove |

**Request:**

```json
{
  "strategy_id": "strategy-456",
  "timeout": 30,
  "optimize": true,
  "options": {
    "max_proof_steps": 100,
    "auto_tactics": true
  }
}
```

**Response:**

```json
{
  "proof_job_id": "job-789",
  "theorem_id": "theorem-124",
  "status": "in_progress",
  "started_at": "2023-04-16T09:16:30Z",
  "estimated_completion_time": "2023-04-16T09:17:00Z"
}
```

### Get Proof Job Status

```
GET /proof-jobs/{id}
```

Checks the status of a proof job.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | ID of the proof job |

**Response:**

```json
{
  "id": "job-789",
  "theorem_id": "theorem-124",
  "status": "completed",
  "started_at": "2023-04-16T09:16:30Z",
  "completed_at": "2023-04-16T09:16:45Z",
  "result": {
    "success": true,
    "proof_steps": 23,
    "time_ms": 450,
    "strategy_id": "strategy-789"
  }
}
```

## Strategy Endpoints

### List Strategies

```
GET /strategies
```

Lists available proof strategies.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `domain` | string | Filter by economic domain |
| `limit` | integer | Maximum number of results (default: 50) |
| `offset` | integer | Pagination offset (default: 0) |

**Response:**

```json
{
  "strategies": [
    {
      "id": "strategy-456",
      "name": "microeconomics_utility_optimization",
      "domain": "microeconomics",
      "success_rate": 0.92,
      "average_proof_time_ms": 350,
      "created_at": "2023-03-10T14:20:00Z"
    },
    ...
  ],
  "total": 24,
  "limit": 50,
  "offset": 0
}
```

### Get Strategy

```
GET /strategies/{id}
```

Retrieves detailed information about a specific strategy.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | ID of the strategy to retrieve |

**Response:**

```json
{
  "id": "strategy-456",
  "name": "microeconomics_utility_optimization",
  "domain": "microeconomics",
  "description": "Optimized strategy for utility maximization problems",
  "created_at": "2023-03-10T14:20:00Z",
  "last_modified": "2023-04-01T09:45:00Z",
  "tactics": [
    {
      "name": "apply_first_order_condition",
      "parameters": {
        "auto_simplify": true
      },
      "weight": 0.8
    },
    {
      "name": "consumer_choice_tactic",
      "parameters": {},
      "weight": 0.6
    },
    ...
  ],
  "genetic_parameters": {
    "population_size": 50,
    "generations": 20,
    "mutation_rate": 0.1,
    "fitness_metric": "proof_speed"
  },
  "statistics": {
    "theorems_proven": 45,
    "success_rate": 0.92,
    "average_proof_time_ms": 350,
    "average_proof_steps": 15
  }
}
```

### Create Strategy

```
POST /strategies
```

Creates a new proof strategy.

**Request:**

```json
{
  "name": "game_theory_nash_equilibrium",
  "domain": "game_theory",
  "description": "Strategy for proving Nash equilibrium properties",
  "tactics": [
    {
      "name": "nash_equilibrium_tactic",
      "parameters": {
        "auto_simplify": true
      },
      "weight": 0.9
    },
    {
      "name": "best_response_analysis",
      "parameters": {},
      "weight": 0.7
    }
  ]
}
```

**Response:**

```json
{
  "id": "strategy-790",
  "name": "game_theory_nash_equilibrium",
  "domain": "game_theory",
  "description": "Strategy for proving Nash equilibrium properties",
  "created_at": "2023-04-16T10:00:00Z",
  "tactics": [
    {
      "name": "nash_equilibrium_tactic",
      "parameters": {
        "auto_simplify": true
      },
      "weight": 0.9
    },
    {
      "name": "best_response_analysis",
      "parameters": {},
      "weight": 0.7
    }
  ]
}
```

### Optimize Strategy

```
POST /strategies/{id}/optimize
```

Optimizes an existing strategy using genetic algorithms.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | ID of the strategy to optimize |

**Request:**

```json
{
  "population_size": 50,
  "generations": 20,
  "mutation_rate": 0.1,
  "crossover_rate": 0.7,
  "fitness_metric": "proof_speed",
  "training_theorems": [
    "theorem-123",
    "theorem-124"
  ]
}
```

**Response:**

```json
{
  "optimization_job_id": "opt-job-891",
  "strategy_id": "strategy-790",
  "status": "in_progress",
  "started_at": "2023-04-16T10:05:00Z",
  "estimated_completion_time": "2023-04-16T10:15:00Z"
}
```

## Genetic Algorithm Endpoints

### List Genetic Populations

```
GET /genetic/populations
```

Lists genetic algorithm populations.

**Response:**

```json
{
  "populations": [
    {
      "id": "pop-234",
      "domain": "microeconomics",
      "size": 50,
      "generations": 15,
      "current_generation": 10,
      "best_fitness": 0.88,
      "created_at": "2023-04-15T08:00:00Z"
    },
    ...
  ]
}
```

### Get Population Details

```
GET /genetic/populations/{id}
```

Retrieves details of a specific genetic population.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | ID of the population |

**Response:**

```json
{
  "id": "pop-234",
  "domain": "microeconomics",
  "size": 50,
  "generations": 15,
  "current_generation": 10,
  "created_at": "2023-04-15T08:00:00Z",
  "genetic_parameters": {
    "mutation_rate": 0.1,
    "crossover_rate": 0.7,
    "selection_method": "tournament",
    "tournament_size": 5,
    "elitism_count": 2
  },
  "fitness_statistics": {
    "best_fitness": 0.88,
    "average_fitness": 0.65,
    "worst_fitness": 0.32,
    "fitness_variance": 0.04
  },
  "individuals": [
    {
      "id": "ind-1234",
      "fitness": 0.88,
      "tactics": [
        {"name": "intro", "weight": 0.9},
        {"name": "apply_first_order_condition", "weight": 0.8},
        {"name": "consumer_choice_tactic", "weight": 0.75}
      ]
    },
    ...
  ],
  "generation_history": [
    {
      "generation": 1,
      "best_fitness": 0.45,
      "average_fitness": 0.32
    },
    ...
    {
      "generation": 10,
      "best_fitness": 0.88,
      "average_fitness": 0.65
    }
  ]
}
```

### Create Genetic Population

```
POST /genetic/populations
```

Creates a new genetic algorithm population.

**Request:**

```json
{
  "domain": "game_theory",
  "size": 40,
  "generations": 20,
  "genetic_parameters": {
    "mutation_rate": 0.15,
    "crossover_rate": 0.8,
    "selection_method": "roulette",
    "elitism_count": 3
  },
  "training_theorems": [
    "theorem-150",
    "theorem-151",
    "theorem-152"
  ]
}
```

**Response:**

```json
{
  "id": "pop-235",
  "domain": "game_theory",
  "size": 40,
  "generations": 20,
  "current_generation": 0,
  "created_at": "2023-04-16T11:30:00Z",
  "genetic_parameters": {
    "mutation_rate": 0.15,
    "crossover_rate": 0.8,
    "selection_method": "roulette",
    "elitism_count": 3
  },
  "status": "initialized",
  "training_theorems": [
    "theorem-150",
    "theorem-151",
    "theorem-152"
  ]
}
```

### Run Genetic Evolution

```
POST /genetic/populations/{id}/evolve
```

Runs evolution for a genetic population.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | ID of the population |

**Request:**

```json
{
  "generations": 10,
  "parallel": true,
  "save_best_strategy": true
}
```

**Response:**

```json
{
  "evolution_job_id": "evo-job-456",
  "population_id": "pop-235",
  "generations": 10,
  "status": "in_progress",
  "started_at": "2023-04-16T11:35:00Z"
}
```

## Self-Healing Endpoints

### System Status

```
GET /self-healing/status
```

Retrieves the current status of the self-healing system.

**Response:**

```json
{
  "active": true,
  "mode": "supervised",
  "detection_interval": 30,
  "active_recoveries": 1,
  "pending_recoveries": 2,
  "pending_approvals": 1,
  "issues_in_quarantine": 3,
  "auto_healing_rate": 78.5,
  "total_recoveries_completed": 25,
  "total_recoveries_failed": 7,
  "total_anomalies_detected": 42,
  "timestamp": "2023-04-16T12:00:00Z"
}
```

### List Recovery Actions

```
GET /self-healing/recoveries
```

Lists recent recovery actions.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by status ("completed", "failed", "in_progress") |
| `limit` | integer | Maximum number of results (default: 50) |
| `offset` | integer | Pagination offset (default: 0) |

**Response:**

```json
{
  "recoveries": [
    {
      "id": "recovery-123",
      "issue_key": "proof_engine:performance",
      "component": "proof_engine",
      "strategy": "reconfiguration",
      "status": "completed",
      "severity": "medium",
      "started_at": "2023-04-16T11:45:00Z",
      "completed_at": "2023-04-16T11:45:30Z",
      "success": true
    },
    ...
  ],
  "total": 32,
  "limit": 50,
  "offset": 0
}
```

### Get Recovery Details

```
GET /self-healing/recoveries/{id}
```

Retrieves details about a specific recovery action.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | ID of the recovery action |

**Response:**

```json
{
  "id": "recovery-123",
  "issue_key": "proof_engine:performance",
  "component": "proof_engine",
  "type": "performance",
  "strategy": "reconfiguration",
  "status": "completed",
  "severity": "medium",
  "priority": "high",
  "started_at": "2023-04-16T11:45:00Z",
  "completed_at": "2023-04-16T11:45:30Z",
  "success": true,
  "details": {
    "changes": {
      "thread_pool_size": {
        "old_value": 4,
        "new_value": 8,
        "success": true
      },
      "cache_size_mb": {
        "old_value": 256,
        "new_value": 512,
        "success": true
      }
    },
    "metrics_before": {
      "response_time_ms": 580,
      "cpu_usage": 0.85,
      "memory_usage": 0.72
    },
    "metrics_after": {
      "response_time_ms": 320,
      "cpu_usage": 0.65,
      "memory_usage": 0.68
    }
  }
}
```

### Approve Recovery

```
POST /self-healing/approvals/{id}/approve
```

Approves a pending recovery action.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | ID of the approval request |

**Response:**

```json
{
  "approval_id": "approval-456",
  "issue_key": "theorem_repository:connection",
  "status": "approved",
  "approved_at": "2023-04-16T12:15:00Z",
  "recovery_id": "recovery-124"
}
```

### Reject Recovery

```
POST /self-healing/approvals/{id}/reject
```

Rejects a pending recovery action.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | ID of the approval request |

**Request:**

```json
{
  "reason": "Scheduled maintenance is about to begin"
}
```

**Response:**

```json
{
  "approval_id": "approval-457",
  "issue_key": "genetic_optimizer:memory",
  "status": "rejected",
  "rejected_at": "2023-04-16T12:20:00Z",
  "reason": "Scheduled maintenance is about to begin"
}
```

### Update Self-Healing Configuration

```
PUT /self-healing/config
```

Updates the self-healing system configuration.

**Request:**

```json
{
  "mode": "automated",
  "detection_interval": 20,
  "max_concurrent_recoveries": 5,
  "quarantine_period": 1200
}
```

**Response:**

```json
{
  "mode": "automated",
  "detection_interval": 20,
  "max_concurrent_recoveries": 5,
  "quarantine_period": 1200,
  "updated_at": "2023-04-16T12:30:00Z"
}
```

## Metrics Endpoints

### List Metrics

```
GET /metrics
```

Lists available metrics.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `component` | string | Filter by component |
| `type` | string | Filter by metric type (counter, gauge, histogram, timer) |

**Response:**

```json
{
  "metrics": [
    {
      "name": "proof_engine.response_time",
      "type": "timer",
      "description": "Proof engine response time",
      "unit": "milliseconds"
    },
    {
      "name": "proof_engine.theorems_proven",
      "type": "counter",
      "description": "Number of theorems proven",
      "unit": "count"
    },
    ...
  ]
}
```

### Get Metric Values

```
GET /metrics/{name}/values
```

Retrieves values for a specific metric.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Name of the metric |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | string | Start time (ISO 8601 format) |
| `end` | string | End time (ISO 8601 format) |
| `step` | string | Time step (e.g., "1m", "5m", "1h") |

**Response:**

```json
{
  "name": "proof_engine.response_time",
  "type": "timer",
  "description": "Proof engine response time",
  "unit": "milliseconds",
  "start": "2023-04-16T00:00:00Z",
  "end": "2023-04-16T12:00:00Z",
  "step": "1h",
  "values": [
    {
      "timestamp": "2023-04-16T00:00:00Z",
      "value": 345.2,
      "count": 42
    },
    {
      "timestamp": "2023-04-16T01:00:00Z",
      "value": 352.7,
      "count": 38
    },
    ...
  ],
  "statistics": {
    "min": 310.5,
    "max": 580.3,
    "avg": 358.9,
    "p95": 495.2,
    "p99": 545.8
  }
}
```

## Error Responses

The API returns standard HTTP status codes and error objects for error conditions:

```json
{
  "error": {
    "code": "theorem_not_found",
    "message": "Theorem with ID 'theorem-999' not found",
    "status": 404,
    "details": {
      "requested_id": "theorem-999"
    }
  }
}
```

Common error codes:

| Code | Status | Description |
|------|--------|-------------|
| `invalid_request` | 400 | The request was invalid |
| `unauthorized` | 401 | Authentication is required |
| `forbidden` | 403 | The action is not allowed |
| `not_found` | 404 | The requested resource was not found |
| `conflict` | 409 | The request conflicts with current state |
| `internal_error` | 500 | An internal server error occurred |

## Webhook Notifications

The API can send webhook notifications for significant events.

### Configuring Webhooks

```
POST /webhooks
```

**Request:**

```json
{
  "url": "https://example.com/economic-theorem-webhook",
  "events": [
    "theorem.proven",
    "theorem.disproven",
    "strategy.optimized",
    "recovery.completed"
  ],
  "secret": "your_webhook_secret"
}
```

**Response:**

```json
{
  "id": "webhook-123",
  "url": "https://example.com/economic-theorem-webhook",
  "events": [
    "theorem.proven",
    "theorem.disproven",
    "strategy.optimized",
    "recovery.completed"
  ],
  "created_at": "2023-04-16T13:00:00Z"
}
```

### Webhook Payload Structure

```json
{
  "id": "event-789",
  "type": "theorem.proven",
  "timestamp": "2023-04-16T14:30:00Z",
  "data": {
    "theorem_id": "theorem-124",
    "name": "law_of_demand",
    "domain": "microeconomics",
    "proof_steps": 23,
    "time_ms": 450,
    "strategy_id": "strategy-456"
  }
}
```

The webhook request includes an `X-Webhook-Signature` header with a HMAC-SHA256 signature of the payload using your webhook secret.

## Batch Operations

For bulk operations, the API provides batch endpoints:

### Batch Prove

```
POST /batch/prove
```

**Request:**

```json
{
  "theorem_ids": [
    "theorem-124",
    "theorem-125",
    "theorem-126"
  ],
  "strategy_id": "strategy-456",
  "timeout": 30,
  "parallel": true
}
```

**Response:**

```json
{
  "batch_id": "batch-123",
  "theorems": 3,
  "started_at": "2023-04-16T15:00:00Z",
  "status": "in_progress",
  "jobs": [
    {
      "theorem_id": "theorem-124",
      "proof_job_id": "job-789",
      "status": "in_progress"
    },
    {
      "theorem_id": "theorem-125",
      "proof_job_id": "job-790",
      "status": "in_progress"
    },
    {
      "theorem_id": "theorem-126",
      "proof_job_id": "job-791",
      "status": "in_progress"
    }
  ]
}
```

## Client Libraries

The Economic Theorem Prover provides client libraries for common programming languages:

### Python

```python
from economic_theorem_prover import Client

# Create client
client = Client(api_key="your_api_key")

# Prove a theorem
result = client.theorems.prove("theorem-124", optimize=True)

# Get proof details
proof = client.proof_jobs.get(result.proof_job_id)

# Check if successful
if proof.result.success:
    print(f"Theorem proven in {proof.result.time_ms}ms using {proof.result.proof_steps} steps")
else:
    print("Theorem could not be proven")
```

### JavaScript/TypeScript

```typescript
import { EconomicTheoremProver } from 'economic-theorem-prover';

// Create client
const client = new EconomicTheoremProver({
  apiKey: 'your_api_key'
});

// Prove a theorem
async function proveTheorem() {
  try {
    const result = await client.theorems.prove('theorem-124', {
      optimize: true
    });
    
    // Poll for result
    const proof = await client.proofJobs.waitForCompletion(result.proof_job_id);
    
    if (proof.result.success) {
      console.log(`Theorem proven in ${proof.result.time_ms}ms using ${proof.result.proof_steps} steps`);
    } else {
      console.log('Theorem could not be proven');
    }
  } catch (error) {
    console.error('Error proving theorem:', error);
  }
}

proveTheorem();
```

### Rust

```rust
use economic_theorem_prover::Client;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create client
    let client = Client::new("your_api_key");
    
    // Prove a theorem
    let result = client.theorems().prove("theorem-124", true).await?;
    
    // Wait for completion
    let proof = client.proof_jobs().wait_for_completion(&result.proof_job_id).await?;
    
    if proof.result.success {
        println!("Theorem proven in {}ms using {} steps", 
                 proof.result.time_ms, proof.result.proof_steps);
    } else {
        println!("Theorem could not be proven");
    }
    
    Ok(())
}
```

## API Versioning

The API uses a versioned URL scheme (`/api/v1`) to ensure compatibility as the API evolves. Breaking changes will only be introduced in new API versions.

When a new API version is released, the previous version will be supported for at least 12 months.

## Rate Limiting

The API implements rate limiting to ensure fair usage. Rate limits are applied per API key.

Rate limit headers are included in all API responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1681654800
```

If you exceed the rate limit, you'll receive a 429 Too Many Requests response.

## Conclusion

This API reference provides comprehensive documentation for programmatically interacting with the Economic Theorem Prover. For additional support, please contact support@economic-theorem-prover.org or visit our community forum.