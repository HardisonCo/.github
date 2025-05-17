# HMS Supervisor Core Components

## 1. Introduction

This document outlines the core components of the HMS supervisor architecture based on a comprehensive analysis of existing specifications, implementation documents, and architecture diagrams. The supervisor architecture is designed to provide a cohesive coordination layer that orchestrates the various self-healing, optimization, and monitoring capabilities of the HMS ecosystem.

## 2. Supervisor Types and Hierarchy

The HMS supervisor architecture follows a hierarchical pattern with specialized supervisors for different domains and responsibilities:

### 2.1 Meta-Supervisor

The Meta-Supervisor is the top-level orchestration component that coordinates all other supervisors in the system. It serves as the entry point for system-wide operations and maintenance tasks.

**Responsibilities:**
- Orchestrate other supervisors
- Hot-load new supervisor playbooks
- Coordinate cross-domain activities
- Provide a unified interface to external systems
- Schedule and prioritize supervisor activities

### 2.2 Analysis Supervisor

The Analysis Supervisor is responsible for continuous monitoring, analysis, and reporting of system components.

**Responsibilities:**
- Monitor system components and collect metrics
- Analyze trends and detect anomalies
- Generate health reports
- Identify improvement opportunities
- Feed information to other supervisors

### 2.3 Improvement Supervisor

The Improvement Supervisor acts on insights from the Analysis Supervisor to implement improvements to the system.

**Responsibilities:**
- Queue refactor tasks
- Open and manage PRs
- Coordinate code improvement activities
- Verify improvement effectiveness
- Track technical debt and improvements

### 2.4 Runtime Supervisor

The Runtime Supervisor manages the day-to-day operation of the system, including health monitoring, recovery, and optimization.

**Responsibilities:**
- Monitor component health
- Detect and recover from failures
- Manage circuit breakers
- Coordinate distributed operations
- Interface with the GA-MAS system

### 2.5 Domain-Specific Supervisors

Several domain-specific supervisors handle specialized aspects of the system:

#### 2.5.1 GA-Supervisor (Genetic Algorithm)
- Manages the evolutionary optimization of the system
- Handles fitness functions and genome evolution
- Coordinates distributed evolution

#### 2.5.2 FFI-Supervisor (Foreign Function Interface)
- Manages cross-language communication
- Ensures type safety and memory correctness
- Coordinates versioned schema registry

#### 2.5.3 Prover-Supervisor (Economic Prover)
- Orchestrates mathematical proofs
- Verifies economic models
- Manages proof metrics

#### 2.5.4 CLI-Supervisor (Command Line Interface)
- Manages the user interface components
- Handles boot sequence visualization
- Coordinates plugin architecture

#### 2.5.5 Gov-Supervisor (Governance)
- Enforces policy and compliance
- Manages documentation and auditing
- Handles external review processes

## 3. Supervisor Architecture Components

### 3.1 Core Traits and Interfaces

#### 3.1.1 Supervisor Trait

```rust
pub trait Supervisor: Send + Sync {
    /// Returns the unique identifier for this supervisor
    fn id(&self) -> String;
    
    /// Returns the supervisor type
    fn supervisor_type(&self) -> SupervisorType;
    
    /// Initializes the supervisor
    fn initialize(&mut self) -> Result<(), SupervisorError>;
    
    /// Starts the supervisor's operations
    fn start(&mut self) -> Result<(), SupervisorError>;
    
    /// Stops the supervisor's operations
    fn stop(&mut self) -> Result<(), SupervisorError>;
    
    /// Processes a task assigned to this supervisor
    fn process_task(&self, task: SupervisorTask) -> Result<SupervisorTaskResult, SupervisorError>;
    
    /// Returns the supervisor's current health status
    fn health_status(&self) -> SupervisorHealthStatus;
    
    /// Returns the supervisor's metrics
    fn metrics(&self) -> HashMap<String, f64>;
    
    /// Handles a message from another supervisor
    fn handle_message(&self, message: SupervisorMessage) -> Result<(), SupervisorError>;
}
```

#### 3.1.2 SupervisorTask

```rust
pub struct SupervisorTask {
    pub id: String,
    pub task_type: SupervisorTaskType,
    pub priority: TaskPriority,
    pub parameters: HashMap<String, Value>,
    pub dependencies: Vec<String>,
    pub timeout: Option<Duration>,
    pub created_at: DateTime<Utc>,
}
```

#### 3.1.3 SupervisorMessage

```rust
pub struct SupervisorMessage {
    pub id: String,
    pub source: String,
    pub destination: String,
    pub message_type: SupervisorMessageType,
    pub content: Value,
    pub timestamp: DateTime<Utc>,
    pub correlation_id: Option<String>,
    pub ttl: Option<Duration>,
}
```

### 3.2 Supervisor Coordinator

The Supervisor Coordinator manages the registration, discovery, and communication between supervisors.

```rust
pub struct SupervisorCoordinator {
    registered_supervisors: Arc<RwLock<HashMap<String, Box<dyn Supervisor>>>>,
    task_queue: Arc<TaskQueue>,
    message_broker: Arc<MessageBroker>,
    health_monitor: Arc<HealthMonitor>,
    configuration: SupervisorCoordinatorConfig,
}

impl SupervisorCoordinator {
    /// Creates a new SupervisorCoordinator
    pub fn new(config: SupervisorCoordinatorConfig) -> Self;
    
    /// Registers a supervisor with the coordinator
    pub fn register_supervisor<T: Supervisor + 'static>(&self, supervisor: T) -> Result<(), SupervisorError>;
    
    /// Retrieves a supervisor by ID
    pub fn get_supervisor(&self, id: &str) -> Option<Arc<Box<dyn Supervisor>>>;
    
    /// Assigns a task to a specific supervisor
    pub fn assign_task(&self, supervisor_id: &str, task: SupervisorTask) -> Result<String, SupervisorError>;
    
    /// Broadcasts a message to all supervisors
    pub fn broadcast_message(&self, message: SupervisorMessage) -> Result<(), SupervisorError>;
    
    /// Sends a message to a specific supervisor
    pub fn send_message(&self, supervisor_id: &str, message: SupervisorMessage) -> Result<(), SupervisorError>;
    
    /// Retrieves the health status of all supervisors
    pub fn health_status(&self) -> HashMap<String, SupervisorHealthStatus>;
    
    /// Starts all registered supervisors
    pub fn start_all(&self) -> Result<(), SupervisorError>;
    
    /// Stops all registered supervisors
    pub fn stop_all(&self) -> Result<(), SupervisorError>;
}
```

### 3.3 Task Queue

The Task Queue manages the prioritization and scheduling of supervisor tasks.

```rust
pub struct TaskQueue {
    high_priority: Arc<Mutex<VecDeque<SupervisorTask>>>,
    medium_priority: Arc<Mutex<VecDeque<SupervisorTask>>>,
    low_priority: Arc<Mutex<VecDeque<SupervisorTask>>>,
    task_registry: Arc<RwLock<HashMap<String, SupervisorTaskStatus>>>,
    task_results: Arc<RwLock<HashMap<String, SupervisorTaskResult>>>,
}

impl TaskQueue {
    /// Enqueues a task with the appropriate priority
    pub fn enqueue(&self, task: SupervisorTask) -> Result<(), QueueError>;
    
    /// Dequeues the next task to process
    pub fn dequeue(&self) -> Option<SupervisorTask>;
    
    /// Retrieves the status of a specific task
    pub fn task_status(&self, task_id: &str) -> Option<SupervisorTaskStatus>;
    
    /// Updates the status of a specific task
    pub fn update_status(&self, task_id: &str, status: SupervisorTaskStatus) -> Result<(), QueueError>;
    
    /// Records the result of a completed task
    pub fn record_result(&self, task_id: &str, result: SupervisorTaskResult) -> Result<(), QueueError>;
    
    /// Retrieves the result of a completed task
    pub fn get_result(&self, task_id: &str) -> Option<SupervisorTaskResult>;
}
```

### 3.4 Message Broker

The Message Broker facilitates communication between supervisors.

```rust
pub struct MessageBroker {
    channels: Arc<RwLock<HashMap<String, mpsc::Sender<SupervisorMessage>>>>,
    subscribers: Arc<RwLock<HashMap<String, HashSet<String>>>>,
    message_history: Arc<RwLock<VecDeque<SupervisorMessage>>>,
    max_history_size: usize,
}

impl MessageBroker {
    /// Registers a channel for a supervisor
    pub fn register_channel(&self, supervisor_id: &str, channel: mpsc::Sender<SupervisorMessage>) -> Result<(), BrokerError>;
    
    /// Subscribes a supervisor to messages from another supervisor
    pub fn subscribe(&self, subscriber_id: &str, publisher_id: &str) -> Result<(), BrokerError>;
    
    /// Publishes a message to all subscribers
    pub fn publish(&self, message: SupervisorMessage) -> Result<Vec<String>, BrokerError>;
    
    /// Sends a direct message to a specific supervisor
    pub fn send_direct(&self, message: SupervisorMessage) -> Result<(), BrokerError>;
    
    /// Retrieves the message history for a specific supervisor
    pub fn get_history(&self, supervisor_id: &str) -> Vec<SupervisorMessage>;
    
    /// Clears the message history
    pub fn clear_history(&self) -> Result<(), BrokerError>;
}
```

## 4. Integration with HMS Components

### 4.1 Health Monitoring System Integration

Supervisors integrate with the Health Monitoring System to monitor component health and trigger recovery actions.

```rust
impl HealthStatusListener for SupervisorHealthListener {
    fn on_status_change(&self, old_result: Option<&HealthCheckResult>, new_result: &HealthCheckResult) {
        // Only react to unhealthy or critical statuses
        if new_result.status == HealthStatus::Unhealthy || new_result.status == HealthStatus::Critical {
            if old_result.map_or(true, |r| r.status != new_result.status) {
                // Create supervisor task for recovery
                let task = SupervisorTask {
                    id: Uuid::new_v4().to_string(),
                    task_type: SupervisorTaskType::Recovery,
                    priority: TaskPriority::High,
                    parameters: {
                        let mut params = HashMap::new();
                        params.insert("component_id".to_string(), Value::String(new_result.component_id.clone()));
                        params.insert("health_status".to_string(), Value::String(format!("{:?}", new_result.status)));
                        params.insert("message".to_string(), Value::String(new_result.message.clone()));
                        params
                    },
                    dependencies: Vec::new(),
                    timeout: Some(Duration::from_secs(30)),
                    created_at: Utc::now(),
                };
                
                // Assign task to Runtime Supervisor
                let runtime_supervisor_id = "runtime_supervisor";
                if let Err(e) = self.coordinator.assign_task(runtime_supervisor_id, task) {
                    error!("Failed to assign recovery task: {}", e);
                }
            }
        }
    }
}
```

### 4.2 Circuit Breaker Integration

Supervisors integrate with the Circuit Breaker pattern to prevent cascading failures.

```rust
impl CircuitBreakerListener for SupervisorCircuitListener {
    fn on_state_change(&self, breaker_id: &str, old_state: CircuitState, new_state: CircuitState) {
        // React to circuit state changes
        if new_state == CircuitState::Open && old_state != CircuitState::Open {
            // Create supervisor task for circuit handling
            let task = SupervisorTask {
                id: Uuid::new_v4().to_string(),
                task_type: SupervisorTaskType::CircuitBreaker,
                priority: TaskPriority::High,
                parameters: {
                    let mut params = HashMap::new();
                    params.insert("breaker_id".to_string(), Value::String(breaker_id.to_string()));
                    params.insert("old_state".to_string(), Value::String(format!("{:?}", old_state)));
                    params.insert("new_state".to_string(), Value::String(format!("{:?}", new_state)));
                    params
                },
                dependencies: Vec::new(),
                timeout: Some(Duration::from_secs(30)),
                created_at: Utc::now(),
            };
            
            // Assign task to Runtime Supervisor
            let runtime_supervisor_id = "runtime_supervisor";
            if let Err(e) = self.coordinator.assign_task(runtime_supervisor_id, task) {
                error!("Failed to assign circuit breaker task: {}", e);
            }
            
            // Broadcast message to all supervisors about circuit state change
            let message = SupervisorMessage {
                id: Uuid::new_v4().to_string(),
                source: "circuit_breaker_system".to_string(),
                destination: "*".to_string(), // Broadcast
                message_type: SupervisorMessageType::CircuitStateChange,
                content: serde_json::to_value(CircuitStateChangePayload {
                    breaker_id: breaker_id.to_string(),
                    old_state,
                    new_state,
                    timestamp: Utc::now(),
                }).unwrap_or_default(),
                timestamp: Utc::now(),
                correlation_id: None,
                ttl: None,
            };
            
            if let Err(e) = self.coordinator.broadcast_message(message) {
                error!("Failed to broadcast circuit state change message: {}", e);
            }
        }
    }
}
```

### 4.3 Genetic Algorithm Integration

Supervisors integrate with the Genetic Algorithm framework for system optimization.

```rust
impl SupervisorEvolutionListener for SupervisorGAListener {
    fn on_evolution_complete(&self, generation: usize, best_chromosome: &Chromosome, population: &[Chromosome]) {
        // Create supervisor task for applying optimized parameters
        let task = SupervisorTask {
            id: Uuid::new_v4().to_string(),
            task_type: SupervisorTaskType::ApplyOptimization,
            priority: TaskPriority::Medium,
            parameters: {
                let mut params = HashMap::new();
                params.insert("generation".to_string(), Value::Number(generation.into()));
                params.insert("best_chromosome".to_string(), serde_json::to_value(best_chromosome).unwrap_or_default());
                params.insert("fitness".to_string(), Value::Number(best_chromosome.fitness.into()));
                params
            },
            dependencies: Vec::new(),
            timeout: Some(Duration::from_secs(60)),
            created_at: Utc::now(),
        };
        
        // Assign task to appropriate supervisor
        let target_supervisor_id = match best_chromosome.optimization_target {
            OptimizationTarget::Performance => "runtime_supervisor",
            OptimizationTarget::ResourceUsage => "runtime_supervisor",
            OptimizationTarget::Reliability => "runtime_supervisor",
            OptimizationTarget::Security => "gov_supervisor",
            _ => "runtime_supervisor",
        };
        
        if let Err(e) = self.coordinator.assign_task(target_supervisor_id, task) {
            error!("Failed to assign optimization task: {}", e);
        }
    }
}
```

### 4.4 Recovery Manager Integration

Supervisors integrate with the Recovery Manager to handle recovery actions.

```rust
impl RecoveryListener for SupervisorRecoveryListener {
    fn on_recovery_initiated(&self, component_id: &str, strategy: RecoveryStrategy) {
        // Create supervisor message about recovery initiation
        let message = SupervisorMessage {
            id: Uuid::new_v4().to_string(),
            source: "recovery_manager".to_string(),
            destination: "runtime_supervisor".to_string(),
            message_type: SupervisorMessageType::RecoveryInitiated,
            content: serde_json::to_value(RecoveryInitiatedPayload {
                component_id: component_id.to_string(),
                strategy: format!("{:?}", strategy),
                timestamp: Utc::now(),
            }).unwrap_or_default(),
            timestamp: Utc::now(),
            correlation_id: None,
            ttl: None,
        };
        
        if let Err(e) = self.coordinator.send_message("runtime_supervisor", message) {
            error!("Failed to send recovery initiation message: {}", e);
        }
    }
    
    fn on_recovery_completed(&self, component_id: &str, result: RecoveryResult) {
        // Create supervisor message about recovery completion
        let message = SupervisorMessage {
            id: Uuid::new_v4().to_string(),
            source: "recovery_manager".to_string(),
            destination: "runtime_supervisor".to_string(),
            message_type: SupervisorMessageType::RecoveryCompleted,
            content: serde_json::to_value(RecoveryCompletedPayload {
                component_id: component_id.to_string(),
                success: result.success,
                message: result.message,
                duration: result.duration.as_millis() as u64,
                timestamp: Utc::now(),
            }).unwrap_or_default(),
            timestamp: Utc::now(),
            correlation_id: None,
            ttl: None,
        };
        
        if let Err(e) = self.coordinator.send_message("runtime_supervisor", message) {
            error!("Failed to send recovery completion message: {}", e);
        }
    }
}
```

## 5. Cross-Language Integration

The supervisor architecture spans both Rust and TypeScript, with FFI communication between them.

### 5.1 Rust Core Implementation

```rust
pub struct CoreSupervisor<T: SupervisorCore> {
    id: String,
    supervisor_type: SupervisorType,
    core: T,
    task_channel: mpsc::Receiver<SupervisorTask>,
    message_channel: mpsc::Receiver<SupervisorMessage>,
    response_channel: mpsc::Sender<SupervisorTaskResult>,
    status: Arc<RwLock<SupervisorStatus>>,
    health_check: Arc<HealthCheck>,
    metrics: Arc<RwLock<HashMap<String, f64>>>,
}

impl<T: SupervisorCore> Supervisor for CoreSupervisor<T> {
    // Implementation of Supervisor trait methods
}
```

### 5.2 TypeScript Interface

```typescript
export interface SupervisorOptions {
  id: string;
  type: SupervisorType;
  config: Record<string, unknown>;
}

export class Supervisor {
  private rustHandle: RustSupervisorHandle;
  private id: string;
  private type: SupervisorType;
  
  constructor(options: SupervisorOptions) {
    // Initialize using FFI
    this.id = options.id;
    this.type = options.type;
    this.rustHandle = ffi.create_supervisor(
      options.id,
      SupervisorType[options.type],
      JSON.stringify(options.config)
    );
  }
  
  public async initialize(): Promise<void> {
    return new Promise((resolve, reject) => {
      ffi.supervisor_initialize(this.rustHandle, (error) => {
        if (error) reject(new Error(error));
        else resolve();
      });
    });
  }
  
  public async start(): Promise<void> {
    return new Promise((resolve, reject) => {
      ffi.supervisor_start(this.rustHandle, (error) => {
        if (error) reject(new Error(error));
        else resolve();
      });
    });
  }
  
  public async stop(): Promise<void> {
    return new Promise((resolve, reject) => {
      ffi.supervisor_stop(this.rustHandle, (error) => {
        if (error) reject(new Error(error));
        else resolve();
      });
    });
  }
  
  public async processTask(task: SupervisorTask): Promise<SupervisorTaskResult> {
    return new Promise((resolve, reject) => {
      ffi.supervisor_process_task(
        this.rustHandle,
        JSON.stringify(task),
        (error, result) => {
          if (error) reject(new Error(error));
          else resolve(JSON.parse(result) as SupervisorTaskResult);
        }
      );
    });
  }
  
  public async getHealthStatus(): Promise<SupervisorHealthStatus> {
    return new Promise((resolve, reject) => {
      ffi.supervisor_health_status(this.rustHandle, (error, status) => {
        if (error) reject(new Error(error));
        else resolve(JSON.parse(status) as SupervisorHealthStatus);
      });
    });
  }
  
  public async getMetrics(): Promise<Record<string, number>> {
    return new Promise((resolve, reject) => {
      ffi.supervisor_metrics(this.rustHandle, (error, metrics) => {
        if (error) reject(new Error(error));
        else resolve(JSON.parse(metrics) as Record<string, number>);
      });
    });
  }
  
  public async sendMessage(message: SupervisorMessage): Promise<void> {
    return new Promise((resolve, reject) => {
      ffi.supervisor_send_message(
        this.rustHandle,
        JSON.stringify(message),
        (error) => {
          if (error) reject(new Error(error));
          else resolve();
        }
      );
    });
  }
}
```

### 5.3 FFI Bridge

```rust
#[no_mangle]
pub extern "C" fn create_supervisor(
    id_ptr: *const c_char,
    type_ptr: *const c_char,
    config_ptr: *const c_char,
) -> *mut c_void {
    let id = unsafe { CStr::from_ptr(id_ptr).to_string_lossy().into_owned() };
    let type_str = unsafe { CStr::from_ptr(type_ptr).to_string_lossy().into_owned() };
    let config_json = unsafe { CStr::from_ptr(config_ptr).to_string_lossy().into_owned() };
    
    let supervisor_type = match type_str.as_str() {
        "Meta" => SupervisorType::Meta,
        "Analysis" => SupervisorType::Analysis,
        "Improvement" => SupervisorType::Improvement,
        "Runtime" => SupervisorType::Runtime,
        "GA" => SupervisorType::GA,
        "FFI" => SupervisorType::FFI,
        "Prover" => SupervisorType::Prover,
        "CLI" => SupervisorType::CLI,
        "Gov" => SupervisorType::Gov,
        _ => SupervisorType::Custom(type_str),
    };
    
    let config: HashMap<String, Value> = match serde_json::from_str(&config_json) {
        Ok(cfg) => cfg,
        Err(_) => HashMap::new(),
    };
    
    let supervisor = create_supervisor_instance(id, supervisor_type, config);
    
    Box::into_raw(Box::new(supervisor)) as *mut c_void
}

#[no_mangle]
pub extern "C" fn supervisor_initialize(handle: *mut c_void, callback: extern "C" fn(*const c_char)) {
    let supervisor = unsafe { &mut *(handle as *mut Box<dyn Supervisor>) };
    
    match supervisor.initialize() {
        Ok(_) => callback(std::ptr::null()),
        Err(e) => {
            let error_str = CString::new(e.to_string()).unwrap_or_default();
            callback(error_str.as_ptr());
        }
    }
}

// Additional FFI functions for other Supervisor methods
```

## 6. Supervisor Task Examples

### 6.1 Analysis Tasks

```yaml
id: "analyze_system_health"
task_type: "Analysis"
priority: "Medium"
parameters:
  components: ["all"]
  metrics: ["cpu", "memory", "response_time", "error_rate"]
  time_range_minutes: 60
  generate_report: true
dependencies: []
timeout: 300000  # 5 minutes
```

### 6.2 Recovery Tasks

```yaml
id: "recover_failed_component"
task_type: "Recovery"
priority: "High"
parameters:
  component_id: "api_service"
  failure_reason: "Connection timeout"
  max_retries: 3
  backoff_strategy: "exponential"
dependencies: []
timeout: 60000  # 1 minute
```

### 6.3 Optimization Tasks

```yaml
id: "optimize_performance_parameters"
task_type: "Optimization"
priority: "Medium"
parameters:
  target: "performance"
  components: ["db_service", "api_service"]
  max_generations: 10
  population_size: 20
  evaluation_criteria: ["throughput", "latency"]
dependencies: []
timeout: 600000  # 10 minutes
```

### 6.4 Governance Tasks

```yaml
id: "policy_compliance_check"
task_type: "Governance"
priority: "Low"
parameters:
  policy_type: "security"
  components: ["all"]
  generate_report: true
  alert_on_violation: true
dependencies: []
timeout: 300000  # 5 minutes
```

## 7. Conclusion

The supervisor architecture provides a comprehensive framework for orchestrating the HMS ecosystem. It enables coordinated self-healing, optimization, and governance through a hierarchical structure of specialized supervisors. The architecture is designed to be extensible, allowing new supervisor types to be added as the system evolves.

The core components defined in this document serve as the foundation for implementing the supervisor architecture in both Rust and TypeScript, with seamless integration via FFI. By following this design, the HMS system can achieve true autonomy and adaptive behavior, functioning as a living organism that continuously monitors, heals, and improves itself.