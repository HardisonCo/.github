# HMS Integrated TypeScript/Rust Implementation with FFI Layer

## 1. Architecture Overview

### 1.1 High-Level Design

The integrated TypeScript/Rust architecture for the HMS living organism approach follows a multi-layered design:

1. **Rust Core Layer** - Performance-critical components implemented in Rust
2. **FFI Bridge Layer** - Cross-language communication layer
3. **TypeScript Interface Layer** - User-facing and CLI components in TypeScript
4. **Agent Communication Layer** - Protocol for agent interaction across languages
5. **Evolution Layer** - GA implementation spanning both languages

This architecture enables a true living organism approach where agents can operate across language boundaries while maintaining the performance benefits of Rust and the flexibility of TypeScript.

### 1.2 Design Principles

The design is guided by the following principles:

1. **Language Appropriate Usage** - Use each language for its strengths
   - Rust for performance-critical components
   - TypeScript for user interfaces and scripting
   
2. **Seamless FFI** - Minimize the friction of cross-language calls
   - Automatic type conversion
   - Error propagation across language boundaries
   - Asynchronous support

3. **Agent Autonomy** - Each agent should function independently
   - Self-contained state
   - Independent decision making
   - Cross-language communication

4. **Evolutionary Design** - System that can evolve itself
   - Code generation across languages
   - Configuration evolution
   - Strategy adaptation

5. **Extensibility** - Easy extension to new components
   - Plugin architecture
   - Dynamic loading
   - Discoverable interfaces

## 2. Rust Core Layer

### 2.1 Components

The Rust core layer includes the following components:

1. **Health Monitoring Core** - High-performance monitoring engine
   ```rust
   pub struct HealthMonitorCore {
       metrics_store: Arc<RwLock<MetricsStore>>,
       anomaly_detector: Box<dyn AnomalyDetector + Send + Sync>,
       alert_manager: Box<dyn AlertManager + Send + Sync>,
       // ...
   }
   ```

2. **Genetic Algorithm Engine** - Evolutionary computation engine
   ```rust
   pub struct GeneticEngine {
       population: Vec<Chromosome>,
       selection_strategy: Box<dyn SelectionStrategy + Send + Sync>,
       crossover_operator: Box<dyn CrossoverOperator + Send + Sync>,
       mutation_operator: Box<dyn MutationOperator + Send + Sync>,
       // ...
   }
   ```

3. **Circuit Breaker Implementation** - Fast, low-overhead circuit breakers
   ```rust
   pub struct CircuitBreakerCore {
       state: Arc<RwLock<CircuitState>>,
       failure_counter: AtomicUsize,
       threshold: usize,
       reset_timeout: Duration,
       // ...
   }
   ```

4. **Recovery Strategies** - Efficient recovery implementations
   ```rust
   pub trait RecoveryStrategy: Send + Sync {
       fn recover(&self, context: &RecoveryContext) -> Result<RecoveryOutcome, RecoveryError>;
       fn estimated_cost(&self) -> RecoveryCost;
       // ...
   }
   ```

5. **Configuration Manager** - Configuration storage and validation
   ```rust
   pub struct ConfigurationManager {
       config_store: Arc<RwLock<ConfigStore>>,
       validators: HashMap<String, Box<dyn ConfigValidator + Send + Sync>>,
       change_history: VecDeque<ConfigChange>,
       // ...
   }
   ```

6. **Metrics Collector** - High-performance metrics collection
   ```rust
   pub struct MetricsCollector {
       metrics: Arc<DashMap<String, MetricValue>>,
       aggregators: HashMap<String, Box<dyn MetricAggregator + Send + Sync>>,
       // ...
   }
   ```

7. **Consensus Engine** - Distributed coordination implementation
   ```rust
   pub struct ConsensusEngine {
       node_id: NodeId,
       peers: Arc<RwLock<HashMap<NodeId, PeerState>>>,
       log: Arc<RwLock<ConsensusLog>>,
       state_machine: Arc<RwLock<Box<dyn StateMachine + Send + Sync>>>,
       // ...
   }
   ```

### 2.2 Agent Implementation

Each component is wrapped in an agent interface that provides autonomy:

```rust
pub struct RustAgent<T: AgentCore> {
    id: AgentId,
    core: T,
    health: Arc<RwLock<AgentHealth>>,
    message_bus: Arc<MessageBus>,
    config: Arc<RwLock<AgentConfig>>,
    state: Arc<RwLock<AgentState>>,
    evolution_context: Arc<RwLock<EvolutionContext>>,
    // ...
}

impl<T: AgentCore> Agent for RustAgent<T> {
    fn id(&self) -> AgentId;
    fn health(&self) -> AgentHealth;
    fn send_message(&self, target: AgentId, message: AgentMessage) -> Result<(), AgentError>;
    fn receive_message(&self, source: AgentId, message: AgentMessage) -> Result<(), AgentError>;
    fn evolve(&self, context: &EvolutionContext) -> Result<(), AgentError>;
    // ...
}
```

## 3. FFI Bridge Layer

### 3.1 Core FFI Design

The FFI layer uses Rust's foreign function interface capabilities and Node.js's N-API:

```rust
#[repr(C)]
pub struct FFIAgentHandle {
    id: u64,
    type_id: u32,
    // Other FFI-safe fields
}

#[no_mangle]
pub extern "C" fn hms_create_agent(agent_type: u32, config_ptr: *const u8, config_len: usize) -> FFIAgentHandle {
    // Implementation
}

#[no_mangle]
pub extern "C" fn hms_agent_send_message(
    agent: FFIAgentHandle, 
    target_id: u64, 
    message_ptr: *const u8, 
    message_len: usize
) -> i32 {
    // Implementation
}

// Additional FFI functions
```

### 3.2 TypeScript FFI Bindings

TypeScript bindings wrap the FFI functions in a more idiomatic interface:

```typescript
interface AgentOptions {
  id?: string;
  type: AgentType;
  config: Record<string, unknown>;
}

class RustAgentBinding {
  private handle: AgentHandle;
  private type: AgentType;
  private id: string;

  constructor(options: AgentOptions) {
    // Initialize using FFI
  }

  public async sendMessage(targetId: string, message: AgentMessage): Promise<void> {
    // Call FFI function
  }

  public async getHealth(): Promise<AgentHealth> {
    // Call FFI function
  }

  // Additional methods
}
```

### 3.3 Asynchronous Processing

To enable non-blocking calls across the FFI boundary:

```typescript
// TypeScript side
class AsyncRustAgent extends RustAgentBinding {
  public sendMessage(targetId: string, message: AgentMessage): Promise<void> {
    return new Promise((resolve, reject) => {
      // Register callback
      const callbackId = registerCallback((error, result) => {
        if (error) reject(error);
        else resolve(result);
      });
      
      // Call FFI with callback ID
      this.sendMessageAsync(targetId, message, callbackId);
    });
  }
}

// Rust side
#[no_mangle]
pub extern "C" fn hms_agent_send_message_async(
    agent: FFIAgentHandle, 
    target_id: u64, 
    message_ptr: *const u8, 
    message_len: usize,
    callback_id: u64
) {
    // Process asynchronously
    tokio::spawn(async move {
        // Call callback when done
        call_js_callback(callback_id, result);
    });
}
```

### 3.4 Memory Management

Careful memory management is essential for the FFI layer:

```rust
// Rust side
#[no_mangle]
pub extern "C" fn hms_free_string(ptr: *mut c_char) {
    if !ptr.is_null() {
        unsafe {
            let _ = CString::from_raw(ptr);
            // String is dropped here
        }
    }
}

// TypeScript side
function freeRustString(ptr: Buffer): void {
    if (ptr) {
        ffi.hms_free_string(ptr);
    }
}
```

### 3.5 Error Handling

Consistent error handling across language boundaries:

```rust
// Rust side
#[repr(C)]
pub struct FFIError {
    code: i32,
    message_ptr: *mut c_char,
}

#[no_mangle]
pub extern "C" fn hms_get_last_error() -> FFIError {
    // Return last error
}

// TypeScript side
class RustError extends Error {
  public code: number;
  
  constructor(code: number, message: string) {
    super(message);
    this.code = code;
  }
}

function checkLastError(): void {
  const error = ffi.hms_get_last_error();
  if (error.code !== 0) {
    const message = readRustString(error.message_ptr);
    freeRustString(error.message_ptr);
    throw new RustError(error.code, message);
  }
}
```

## 4. TypeScript Interface Layer

### 4.1 Agent Abstractions

TypeScript provides high-level agent abstractions:

```typescript
abstract class Agent {
  protected id: string;
  protected type: AgentType;
  protected messageHandlers: Map<string, MessageHandler>;
  protected healthStatus: AgentHealth;
  
  constructor(id: string, type: AgentType) {
    this.id = id;
    this.type = type;
    this.messageHandlers = new Map();
    this.healthStatus = { status: 'healthy' };
  }
  
  public abstract sendMessage(targetId: string, message: AgentMessage): Promise<void>;
  public abstract getHealth(): Promise<AgentHealth>;
  
  public registerMessageHandler(type: string, handler: MessageHandler): void {
    this.messageHandlers.set(type, handler);
  }
  
  // Additional methods
}

class TypeScriptAgent extends Agent {
  // Implementation using pure TypeScript
}

class RustBackedAgent extends Agent {
  private rustAgent: RustAgentBinding;
  
  constructor(id: string, type: AgentType, options: RustAgentOptions) {
    super(id, type);
    this.rustAgent = new RustAgentBinding({
      id,
      type,
      config: options.config
    });
  }
  
  public async sendMessage(targetId: string, message: AgentMessage): Promise<void> {
    return this.rustAgent.sendMessage(targetId, message);
  }
  
  // Additional implementations
}
```

### 4.2 CLI Interface

TypeScript implements the CLI interface:

```typescript
class HMS_CLI {
  private agents: Map<string, Agent>;
  private commandHandlers: Map<string, CommandHandler>;
  
  constructor() {
    this.agents = new Map();
    this.commandHandlers = new Map();
    this.registerDefaultCommands();
  }
  
  public registerCommand(name: string, handler: CommandHandler): void {
    this.commandHandlers.set(name, handler);
  }
  
  public async executeCommand(name: string, args: string[]): Promise<void> {
    const handler = this.commandHandlers.get(name);
    if (!handler) {
      throw new Error(`Unknown command: ${name}`);
    }
    
    await handler(args, this);
  }
  
  public createAgent(type: AgentType, options: AgentOptions): Agent {
    // Create appropriate agent type based on configuration
    let agent: Agent;
    
    if (options.useRustImplementation) {
      agent = new RustBackedAgent(options.id || uuidv4(), type, options);
    } else {
      agent = new TypeScriptAgent(options.id || uuidv4(), type, options);
    }
    
    this.agents.set(agent.id, agent);
    return agent;
  }
  
  // Additional methods
}
```

### 4.3 User Interface

TypeScript provides user interface components:

```typescript
class DashboardComponent {
  private cli: HMS_CLI;
  private domElement: HTMLElement;
  
  constructor(cli: HMS_CLI, elementId: string) {
    this.cli = cli;
    this.domElement = document.getElementById(elementId);
  }
  
  public async render(): Promise<void> {
    // Render dashboard
  }
  
  // Additional methods
}

class AgentVisualizer {
  private agent: Agent;
  private domElement: HTMLElement;
  
  constructor(agent: Agent, elementId: string) {
    this.agent = agent;
    this.domElement = document.getElementById(elementId);
  }
  
  public async render(): Promise<void> {
    // Render agent visualization
  }
  
  // Additional methods
}
```

## 5. Agent Communication Layer

### 5.1 Message Format

Messages between agents use a consistent format across languages:

```typescript
interface AgentMessage {
  id: string;
  type: string;
  payload: Record<string, unknown>;
  metadata: {
    timestamp: number;
    sender: string;
    priority: number;
    ttl?: number;
  };
}
```

### 5.2 Communication Protocols

The communication layer supports multiple protocols:

```typescript
interface CommunicationProtocol {
  sendMessage(targetId: string, message: AgentMessage): Promise<void>;
  registerHandler(handler: (message: AgentMessage) => Promise<void>): void;
}

class DirectCommunication implements CommunicationProtocol {
  // Implementation for in-process communication
}

class MessageBusCommunication implements CommunicationProtocol {
  // Implementation using a message bus
}

class DistributedCommunication implements CommunicationProtocol {
  // Implementation for cross-node communication
}
```

### 5.3 Service Discovery

Agents discover each other using a service registry:

```typescript
interface ServiceRegistry {
  registerAgent(agent: Agent): Promise<void>;
  unregisterAgent(agentId: string): Promise<void>;
  findAgent(agentId: string): Promise<Agent | null>;
  findAgentsByType(type: AgentType): Promise<Agent[]>;
}

class LocalServiceRegistry implements ServiceRegistry {
  // Implementation for local registry
}

class DistributedServiceRegistry implements ServiceRegistry {
  // Implementation for distributed registry
}
```

## 6. Evolution Layer

### 6.1 Genetic Algorithm Implementation

The GA spans both languages:

```typescript
// TypeScript
interface EvolutionConfig {
  populationSize: number;
  mutationRate: number;
  crossoverRate: number;
  selectionStrategy: SelectionStrategy;
  fitnessFunction: FitnessFunction;
}

class EvolutionController {
  private config: EvolutionConfig;
  private population: Chromosome[];
  private rustEngine: RustGABinding | null;
  
  constructor(config: EvolutionConfig, useRustEngine: boolean = true) {
    this.config = config;
    this.population = [];
    
    if (useRustEngine) {
      this.rustEngine = new RustGABinding(config);
    } else {
      this.rustEngine = null;
    }
  }
  
  public async evolve(generations: number): Promise<Chromosome> {
    if (this.rustEngine) {
      return this.rustEngine.evolve(generations);
    } else {
      // TypeScript implementation
    }
  }
  
  // Additional methods
}
```

### 6.2 Code Generation

The system can generate code for both languages:

```typescript
interface CodeGenerator {
  generateRustCode(model: AgentModel): string;
  generateTypeScriptCode(model: AgentModel): string;
}

class AgentCodeGenerator implements CodeGenerator {
  public generateRustCode(model: AgentModel): string {
    // Generate Rust code for agent
  }
  
  public generateTypeScriptCode(model: AgentModel): string {
    // Generate TypeScript code for agent
  }
}
```

### 6.3 Dynamic Loading

Both languages support dynamic loading of generated code:

```typescript
// TypeScript
class DynamicLoader {
  public async loadTypeScriptAgent(code: string): Promise<Agent> {
    // Dynamically load TypeScript agent
  }
  
  public async loadRustAgent(code: string): Promise<Agent> {
    // Compile and load Rust agent
  }
}
```

## 7. Integration Strategy

### 7.1 Language Boundary Decisions

The architecture defines clear boundaries between languages:

- **Rust** is used for:
  - Performance-critical components
  - Core algorithms (GA, consensus, metrics collection)
  - Data processing pipelines
  - Low-level system interactions

- **TypeScript** is used for:
  - CLI interface
  - User interfaces
  - High-level coordination
  - Scripting and automation
  - Dynamic code generation and loading

### 7.2 FFI Boundary Management

To manage the complexity of the FFI boundary:

1. **Minimize Crossings** - Limit the number of FFI calls by batching operations
2. **Standardize Interfaces** - Use consistent patterns for all FFI interfaces
3. **Optimize Data Transfer** - Use efficient serialization for large data transfers
4. **Handle Errors Consistently** - Propagate errors across the boundary with context
5. **Memory Safety** - Ensure proper cleanup of resources on both sides

### 7.3 Deployment Model

The system supports different deployment models:

1. **Single Process** - All components in one process with in-process communication
2. **Multi-Process** - Components spread across processes with IPC
3. **Distributed** - Components spread across nodes with network communication

## 8. Development and Testing Strategy

### 8.1 Development Workflow

The integrated development workflow:

1. Define agent interfaces in a language-neutral IDL
2. Generate FFI interfaces for both languages
3. Implement core functionality in Rust
4. Implement UI/CLI functionality in TypeScript
5. Build and test cross-language integration

### 8.2 Testing Approach

Testing covers all aspects of the integration:

1. **Unit Tests** - Test each component in isolation
2. **Integration Tests** - Test cross-language interactions
3. **Performance Tests** - Verify overhead of FFI layer
4. **Evolution Tests** - Test GA optimization across languages
5. **Chaos Tests** - Test system resilience in failure scenarios

## 9. Conclusion

The integrated TypeScript/Rust implementation with FFI layer provides a robust foundation for the HMS living organism approach. By leveraging the strengths of both languages and providing seamless cross-language communication, the architecture enables:

1. **True Agent Autonomy** - Agents function as independent cells regardless of implementation language
2. **Cross-Language Evolution** - GA optimization spans language boundaries
3. **High Performance** - Critical components in Rust for maximum performance
4. **User-Friendly Interfaces** - TypeScript for UI and CLI components
5. **Extensibility** - Easy extension to new components in either language

This design addresses the gaps identified in the analysis phase and provides a clear path to implementing the living organism approach in the HMS architecture.