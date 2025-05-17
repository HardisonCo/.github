# HMS Rust Implementation Plan

This document outlines a comprehensive strategy for implementing the HMS (Health Monitoring System) as described in the Unified Master Plan, with Rust as the primary language and strong FFI support for system components.

## 1. Rust-First Architecture Overview

### 1.1 Cargo Workspace Structure

```
/hms/
├── Cargo.toml                    # Workspace definition
├── crates/
│   ├── supervisor/               # Core orchestrator & control plane
│   ├── agent_core/               # Agent identity & lifecycle (HMS-AGT)
│   ├── agent_skills/             # Pluggable agent capabilities (HMS-AGX)
│   ├── communication/            # A2A protocol implementation
│   ├── verification/             # Compliance & verification pipeline
│   ├── self_healing/             # Autonomous recovery mechanisms
│   ├── genetic_engine/           # GA for theorem proving optimization
│   ├── data_store/               # Repository & knowledge base client
│   └── ffi/                      # FFI bindings (Python, Lean)
├── proto/                        # Protocol buffer definitions
└── docs/                         # Documentation
```

### 1.2 Core Technical Decisions

| Component | Technology Choice | Rationale |
|-----------|-------------------|-----------|
| Core Runtime | Tokio async | Industry standard for Rust async; excellent performance |
| Service Communication | gRPC (tonic) | Strong typing, bidirectional streams, language-agnostic |
| Event Bus | NATS | Lightweight, high-performance pub/sub |
| Serialization | Protocol Buffers | Compact binary format, excellent language support |
| Database | SQLx + Postgres | Type-safe SQL with async support |
| Vector Store | Qdrant client | Embedding storage for agent knowledge |
| FFI Strategy | PyO3 + cbindgen | Minimal overhead for Python & C bindings |
| UI Layer | Next.js + gRPC-Web | Separate from core for maintainability |

## 2. Phased Implementation Roadmap

### 2.1 Phase 1: Foundation (Weeks 1-6)

**Objective**: Establish the core Rust infrastructure and minimal agent system.

#### Week 1-2: Bootstrap
- Initialize Cargo workspace with empty crates
- Define protocol schemas (AgentTask, AgentEvent, SupervisorCommand)
- Implement basic Supervisor service with Tokio and tonic

```rust
// Example: Minimal Supervisor implementation in crates/supervisor/src/main.rs
use tokio::sync::mpsc;
use tonic::{transport::Server, Request, Response, Status};

pub mod proto {
    tonic::include_proto!("hms.supervisor");
}

#[derive(Default)]
pub struct SupervisorService {}

#[tonic::async_trait]
impl proto::supervisor_server::Supervisor for SupervisorService {
    async fn ping(
        &self,
        request: Request<proto::PingRequest>,
    ) -> Result<Response<proto::PingResponse>, Status> {
        println!("Got ping from: {:?}", request.remote_addr());
        
        let reply = proto::PingResponse {
            message: format!("Pong!"),
        };
        Ok(Response::new(reply))
    }
    
    async fn spawn_agent(
        &self,
        request: Request<proto::SpawnAgentRequest>,
    ) -> Result<Response<proto::SpawnAgentResponse>, Status> {
        let req = request.into_inner();
        println!("Spawning agent of type: {}", req.agent_type);
        
        // Placeholder implementation
        let reply = proto::SpawnAgentResponse {
            agent_id: format!("agent-{}", rand::random::<u64>()),
            status: proto::AgentStatus::Initializing as i32,
        };
        
        Ok(Response::new(reply))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let supervisor = SupervisorService::default();
    
    println!("Supervisor listening on {}", addr);
    
    Server::builder()
        .add_service(proto::supervisor_server::SupervisorServer::new(supervisor))
        .serve(addr)
        .await?;
    
    Ok(())
}
```

#### Week 3-4: Core Components
- Implement agent_core with identity and lifecycle management
- Build communication crate with A2A protocol client
- Create a simple serialization/deserialization layer for agent states

#### Week 5-6: Integration
- Connect Supervisor to agent_core for a basic spawn/ping/kill cycle
- Implement minimal data_store with SQLx for tracking agent state
- Create FFI bindings for a "hello world" Python agent

### 2.2 Phase 2: Agent System Development (Weeks 7-14)

**Objective**: Develop specialized agents and verification.

#### Week 7-8: Agent Skills
- Implement agent_skills trait system and plugin architecture
- Create first specialized agents (e.g., DecompositionAgent, StrategyAgent)

```rust
// Example: Agent Skill trait in crates/agent_skills/src/lib.rs
use async_trait::async_trait;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SkillContext {
    pub agent_id: String,
    pub task_id: String,
    pub parameters: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SkillResult {
    pub success: bool,
    pub result: serde_json::Value,
    pub error_message: Option<String>,
}

#[async_trait]
pub trait AgentSkill: Send + Sync {
    // Unique identifier for the skill
    fn id(&self) -> &str;
    
    // Human-readable name
    fn name(&self) -> &str;
    
    // Description of what the skill does
    fn description(&self) -> &str;
    
    // Execute the skill with given context
    async fn execute(&self, ctx: SkillContext) -> SkillResult;
    
    // Check if the skill can handle the given context
    fn can_handle(&self, ctx: &SkillContext) -> bool;
}

// Example implementation
pub struct TheoremDecompositionSkill {
    id: String,
}

impl TheoremDecompositionSkill {
    pub fn new() -> Self {
        Self {
            id: "theorem_decomposition".to_string(),
        }
    }
}

#[async_trait]
impl AgentSkill for TheoremDecompositionSkill {
    fn id(&self) -> &str {
        &self.id
    }
    
    fn name(&self) -> &str {
        "Theorem Decomposition"
    }
    
    fn description(&self) -> &str {
        "Breaks complex theorems into smaller, more manageable sub-goals"
    }
    
    async fn execute(&self, ctx: SkillContext) -> SkillResult {
        // Implementation would go here
        // For now, a placeholder returning success
        SkillResult {
            success: true,
            result: serde_json::json!({
                "sub_goals": [
                    "subgoal_1",
                    "subgoal_2"
                ]
            }),
            error_message: None,
        }
    }
    
    fn can_handle(&self, ctx: &SkillContext) -> bool {
        // Check if the task parameters include a theorem
        ctx.parameters.get("theorem").is_some()
    }
}
```

#### Week 9-10: Verification Pipeline
- Implement verification crate with policy checking
- Create a Lean 4 client for verifying theorems
- Integrate with the Supervisor for pre/post-action verification

#### Week 11-14: FFI Integration
- Extend FFI layer to support Python ML frameworks
- Create Lean 4 bindings for theorem proving
- Implement serialization/deserialization of complex objects across FFI

### 2.3 Phase 3: Self-Healing & Genetic Algorithms (Weeks 15-22)

**Objective**: Add autonomy and learning capabilities.

#### Week 15-16: Monitoring Foundation
- Implement health checking and heartbeat mechanisms
- Create metrics collection system with Prometheus
- Build a diagnostic agent to detect failures

#### Week 17-18: Self-Healing
- Implement the self_healing crate with recovery strategies
- Add automatic restart/respawn logic to the Supervisor
- Create circuit breakers for cascading failure prevention

```rust
// Example: Self-healing module in crates/self_healing/src/lib.rs
use async_trait::async_trait;
use std::time::{Duration, Instant};
use tokio::sync::mpsc;

#[derive(Debug, Clone)]
pub enum HealthStatus {
    Healthy,
    Degraded { reason: String },
    Failed { reason: String },
}

#[derive(Debug, Clone)]
pub struct HealthReport {
    pub agent_id: String,
    pub status: HealthStatus,
    pub timestamp: Instant,
    pub metrics: serde_json::Value,
}

#[derive(Debug, Clone)]
pub enum RecoveryAction {
    Restart,
    Respawn { config_changes: serde_json::Value },
    Alert { message: String },
    Ignore,
}

#[async_trait]
pub trait HealthPolicy: Send + Sync {
    async fn evaluate(&self, report: &HealthReport) -> RecoveryAction;
}

pub struct StandardHealthPolicy {
    // Configuration parameters
    max_restart_attempts: usize,
    restart_cooldown: Duration,
    // State
    restart_history: std::collections::HashMap<String, Vec<Instant>>,
}

impl StandardHealthPolicy {
    pub fn new(max_restart_attempts: usize, restart_cooldown: Duration) -> Self {
        Self {
            max_restart_attempts,
            restart_cooldown,
            restart_history: std::collections::HashMap::new(),
        }
    }
    
    fn get_recent_restarts(&self, agent_id: &str) -> usize {
        let now = Instant::now();
        
        self.restart_history
            .get(agent_id)
            .map(|times| {
                times
                    .iter()
                    .filter(|t| now.duration_since(**t) < self.restart_cooldown)
                    .count()
            })
            .unwrap_or(0)
    }
}

#[async_trait]
impl HealthPolicy for StandardHealthPolicy {
    async fn evaluate(&self, report: &HealthReport) -> RecoveryAction {
        match &report.status {
            HealthStatus::Healthy => RecoveryAction::Ignore,
            
            HealthStatus::Degraded { reason } => {
                // Only restart if we haven't tried too many times
                let recent_restarts = self.get_recent_restarts(&report.agent_id);
                
                if recent_restarts < self.max_restart_attempts {
                    RecoveryAction::Restart
                } else {
                    RecoveryAction::Alert { 
                        message: format!(
                            "Agent {} is degraded ({}), but restart limit reached",
                            report.agent_id, reason
                        )
                    }
                }
            },
            
            HealthStatus::Failed { reason } => {
                let recent_restarts = self.get_recent_restarts(&report.agent_id);
                
                if recent_restarts < self.max_restart_attempts {
                    RecoveryAction::Respawn { 
                        config_changes: serde_json::json!({
                            "memory_limit": "increased",
                            "timeout": "increased"
                        })
                    }
                } else {
                    RecoveryAction::Alert { 
                        message: format!(
                            "Agent {} has failed ({}), and recovery attempts exhausted",
                            report.agent_id, reason
                        )
                    }
                }
            }
        }
    }
}
```

#### Week 19-22: Genetic Algorithm Engine
- Implement the genetic_engine crate with population management
- Create fitness functions for theorem proving
- Build a mutation engine for agent parameters

### 2.4 Phase 4: Advanced Learning (Weeks 23-30)

**Objective**: Integrate RL and enhance genetic algorithms.

#### Week 23-24: Knowledge Base
- Extend data_store with vector embeddings
- Implement knowledge sharing across agents
- Create search and retrieval mechanisms

#### Week 25-28: RL Integration
- Implement interfaces with RL libraries via FFI
- Create the hybrid GA-RL optimization engine
- Develop reward functions for theorem proving

#### Week 29-30: Swarm Capabilities
- Implement collaborative proof strategies
- Create the shared memory space for agent cooperation
- Optimize for parallel theorem solving

### 2.5 Phase 5: Production Readiness (Weeks 31-40)

**Objective**: Harden the system for production use.

#### Week 31-34: Security & Compliance
- Add authentication and authorization
- Implement secure serialization and deserialization
- Create audit logging and compliance checks

#### Week 35-37: DevOps Integration
- Dockerize all components
- Create Kubernetes deployment manifests
- Implement CI/CD pipelines

#### Week 38-40: Scalability & UI
- Optimize for horizontal scaling
- Create admin UI for system management
- Implement advanced HITL controls

## 3. FFI Strategy

### 3.1 Python Integration (PyO3)

The primary FFI integration with Python will use PyO3, maintaining these principles:

1. **Zero-Copy When Possible**: Use PyO3's zero-copy features for large data transfers.
2. **GIL Management**: All Python operations release the GIL when not needed.
3. **Error Handling**: Proper propagation of errors between languages.
4. **Type Safety**: Using PyO3's type checking to ensure correctness.

Example Python module implementation:

```rust
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn spawn_agent(agent_type: &str, parameters: Option<PyObject>) -> PyResult<String> {
    // Convert Python parameters to Rust
    let params = match parameters {
        Some(p) => Python::with_gil(|py| {
            p.extract::<HashMap<String, PyObject>>(py)?
                .into_iter()
                .map(|(k, v)| {
                    let value = v.extract::<String>(py)?;
                    Ok((k, value))
                })
                .collect::<PyResult<HashMap<String, String>>>()
        })?,
        None => HashMap::new(),
    };

    // Call Rust supervisor (simplified)
    let agent_id = format!("agent-{}", rand::random::<u64>());
    
    Ok(agent_id)
}

#[pymodule]
fn hms_supervisor(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(spawn_agent, m)?)?;
    Ok(())
}
```

### 3.2 Lean 4 Integration

For Lean 4 integration, we'll use a combination of direct process execution and potentially the Lean 4 server protocol:

1. **Process-Based**: For simpler interactions, spawn Lean as a subprocess.
2. **Server Protocol**: For more complex scenarios, connect to the Lean server.
3. **Cache Management**: Intelligent caching of Lean environment to avoid costly re-initialization.

Example implementation:

```rust
// crates/verification/src/lean_client.rs
use std::path::Path;
use std::process::{Command, Output};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::process::Command as AsyncCommand;

pub struct LeanClient {
    lean_path: String,
    working_dir: String,
}

impl LeanClient {
    pub fn new(lean_path: String, working_dir: String) -> Self {
        Self {
            lean_path,
            working_dir,
        }
    }
    
    pub async fn verify_theorem(&self, theorem_file: &str) -> Result<bool, Box<dyn std::error::Error>> {
        let output = AsyncCommand::new(&self.lean_path)
            .arg(theorem_file)
            .current_dir(&self.working_dir)
            .output()
            .await?;
            
        let success = output.status.success();
        let stdout = String::from_utf8_lossy(&output.stdout);
        let stderr = String::from_utf8_lossy(&output.stderr);
        
        if !success {
            eprintln!("Lean verification failed: {}", stderr);
        }
        
        Ok(success)
    }
    
    pub async fn run_tactic(&self, theorem_file: &str, tactic: &str) -> Result<String, Box<dyn std::error::Error>> {
        // Implementation to run a specific tactic and get the resulting state
        todo!()
    }
}
```

### 3.3 C/C++ Integration (cbindgen)

For components needing C/C++ interop, we'll use cbindgen:

1. **ABI Stability**: Ensure a stable C ABI for all exported functions.
2. **Documentation**: Headers include Doxygen-style documentation.
3. **Error Handling**: C-friendly error reporting mechanisms.

Example header generation:

```rust
// crates/ffi/src/c_api.rs
use std::ffi::{CStr, CString};
use std::os::raw::{c_char, c_int};

#[no_mangle]
pub extern "C" fn hms_supervisor_init() -> c_int {
    // Initialize the supervisor
    1 // Success
}

#[no_mangle]
pub extern "C" fn hms_supervisor_spawn_agent(
    agent_type: *const c_char,
    agent_id_out: *mut c_char,
    agent_id_len: c_int
) -> c_int {
    let agent_type_str = unsafe {
        match CStr::from_ptr(agent_type).to_str() {
            Ok(s) => s,
            Err(_) => return -1, // Invalid UTF-8
        }
    };
    
    // Generate an agent ID (simplified)
    let agent_id = format!("agent-{}", rand::random::<u64>());
    
    // Copy to output buffer
    let c_agent_id = match CString::new(agent_id) {
        Ok(s) => s,
        Err(_) => return -2, // Allocation error
    };
    
    unsafe {
        std::ptr::copy_nonoverlapping(
            c_agent_id.as_ptr(),
            agent_id_out,
            agent_id_len as usize
        );
    }
    
    0 // Success
}
```

## 4. Testing Strategy

### 4.1 Unit Testing

Every crate will have comprehensive unit tests:

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_supervisor_ping() {
        let supervisor = SupervisorService::default();
        
        let request = Request::new(proto::PingRequest {});
        let response = supervisor.ping(request).await.unwrap();
        
        assert!(response.get_ref().message.contains("Pong"));
    }
    
    #[tokio::test]
    async fn test_agent_spawn() {
        let supervisor = SupervisorService::default();
        
        let request = Request::new(proto::SpawnAgentRequest {
            agent_type: "test_agent".to_string(),
            parameters: "{}".to_string(),
        });
        
        let response = supervisor.spawn_agent(request).await.unwrap();
        
        assert!(response.get_ref().agent_id.starts_with("agent-"));
        assert_eq!(response.get_ref().status, proto::AgentStatus::Initializing as i32);
    }
}
```

### 4.2 Integration Testing

End-to-end tests will validate complete workflows:

- Docker Compose for multi-service tests
- Mock FFI boundaries when needed
- Test agents that simulate various behaviors

### 4.3 Chaos Testing

Specific tests for the self-healing capabilities:

- Kill random agents mid-operation
- Inject latency or failures in communication
- Verify recovery and continued operation

## 5. Performance Optimization

### 5.1 Async Performance

- Tokio runtime tuned for workload
- Connection pooling for databases
- Batched operations where appropriate

### 5.2 FFI Optimization

- Minimize crossings via batching
- Strategic memory management and buffer reuse
- Caching frequently used data

## 6. Deliverables & Checkpoints

| Week | Checkpoint | Deliverable |
|------|------------|-------------|
| 2 | Bootstrap Complete | Functioning Supervisor that can ping |
| 6 | Foundation Complete | End-to-end agent spawn/task/kill cycle |
| 14 | Agent System Ready | Specialized agents with verification |
| 22 | Self-Healing Active | Automatic recovery from failure modes |
| 30 | Learning System Ready | GA-RL hybrid optimization working |
| 40 | Production Ready | Full system deployable to production |

## 7. References

- [Tokio](https://tokio.rs/) - Async runtime
- [tonic](https://github.com/hyperium/tonic) - gRPC framework
- [PyO3](https://pyo3.rs/) - Rust Python bindings
- [cbindgen](https://github.com/eqrion/cbindgen) - C binding generator
- [SQLx](https://github.com/launchbadge/sqlx) - SQL toolkit
- [Lean 4](https://leanprover.github.io/) - Theorem prover