# HMS Monitoring Components Usage Guide

This guide provides instructions for using the three integrated monitoring components:
1. TMUX Integration
2. Supervisor Component
3. Knowledge Registry

## Prerequisites

- Rust and Cargo installed (see https://rustup.rs/)
- TMUX installed
  - macOS: `brew install tmux`
  - Ubuntu/Debian: `apt install tmux`
  - Fedora/RHEL: `dnf install tmux`

## Building the Components

Run the build script to compile all components:

```bash
./scripts/build_monitoring_components.sh
```

This will build the individual components and the integrated example.

## Running the Integrated Example

The integrated example demonstrates all three components working together:

```bash
cd examples
cargo run --bin integrated_monitoring_system
```

This will:
1. Create a TMUX session with visualization panes
2. Start the Supervisor component
3. Initialize the Knowledge Registry
4. Register sample components and healing strategies
5. Simulate component activity and health changes

Press Enter to exit the example when you're done.

## Standalone Component Usage

### TMUX Integration

```rust
use tmux_integration::{TmuxSessionManager, TmuxConfig, VisualizationController};

// Create a TMUX session manager
let config = TmuxConfig {
    base_dir: ".".to_string(),
    default_layout: "tiled".to_string(),
    auto_reconnect: true,
    auto_create: true,
    ..Default::default()
};

let session_manager = TmuxSessionManager::new("my-session", Some(config))?;

// Create a visualization controller
let visualization = VisualizationController::new(Arc::new(RwLock::new(session_manager)), 1000);

// Create the base layout
visualization.create_base_layout()?;

// Update component status
visualization.update_component_status(ComponentStatus {
    id: "my-component".to_string(),
    status: HealthStatus::Healthy,
    metrics: HashMap::new(),
    last_update: SystemTime::now(),
});

// Add agent activity
visualization.add_agent_activity(AgentActivity {
    agent_id: "my-agent".to_string(),
    activity_type: ActivityType::Completed,
    description: "Task completed".to_string(),
    timestamp: SystemTime::now(),
    result: Some(ActivityResult::Success("Operation successful".to_string())),
});
```

### Supervisor Component

```rust
use supervisor::{
    ComponentRegistry, ComponentRegistration, ComponentHealth,
    SupervisorAgent, SystemMonitor, RecoveryCoordinator
};

// Create a component registry
let registry = Arc::new(ComponentRegistry::new(100));

// Register a component
let registration = ComponentRegistration {
    id: "my-component".to_string(),
    component_type: ComponentType::Custom(1),
    version: "1.0.0".to_string(),
    dependencies: vec![],
    registration_time: SystemTime::now(),
    last_heartbeat: SystemTime::now(),
    health: ComponentHealth::Healthy,
    self_healing_capabilities: SelfHealingCapabilities::default(),
};

registry.register_component(registration)?;

// Create a recovery coordinator
let recovery = Arc::new(RecoveryCoordinator::new(registry.clone()));

// Create a system monitor
let monitor = Arc::new(SystemMonitor::new(
    registry.clone(),
    Duration::from_secs(5),
    recovery.clone(),
));

// Add a policy
let policy = HealingPolicy {
    id: "high-cpu-policy".to_string(),
    component_type: ComponentType::Custom(0),
    conditions: vec![
        PolicyCondition::MetricThreshold(
            "cpu_usage".to_string(),
            90.0,
            ThresholdComparison::GreaterThan,
        ),
    ],
    actions: vec![
        SupervisorAction::RestartComponent("${component_id}".to_string()),
    ],
    priority: 10,
    cooldown: Duration::from_secs(300),
    last_applied: None,
};

monitor.add_policy(policy)?;

// Create a supervisor agent
let agent = SupervisorAgent::new(
    "supervisor-01",
    registry.clone(),
    monitor,
    recovery,
);

// Start the supervisor
agent.start()?;
```

### Knowledge Registry

```rust
use knowledge_registry::{
    KnowledgeRegistry, KnowledgeSchema, KnowledgeId, KnowledgeValue, KnowledgeItem,
    KnowledgeQuery, StrategyEvaluator, LearningSystem
};

// Create a knowledge registry
let registry = Arc::new(KnowledgeRegistry::new());

// Create a schema
let schema = Arc::new(KnowledgeSchema::new());

// Add a knowledge item
let id = KnowledgeId::new("hms", "config", "settings", 1);
let mut value_map = HashMap::new();
value_map.insert("debug".to_string(), KnowledgeValue::Boolean(true));
value_map.insert("log_level".to_string(), KnowledgeValue::String("info".to_string()));

let item = KnowledgeItem::new(
    id,
    KnowledgeValue::Map(value_map),
    None,
);

registry.add_item(item)?;

// Query knowledge items
let query = KnowledgeQuery::new()
    .namespace("hms")
    .knowledge_type("config");
    
let items = registry.query(&query);

// Create strategy evaluator
let evaluator = Arc::new(StrategyEvaluator::new(registry.clone(), schema.clone()));

// Create learning system
let learning = Arc::new(LearningSystem::new(registry.clone(), evaluator.clone()));
```

## Component Integration

The three components are designed to work together seamlessly:

1. **TMUX Integration with Supervisor**:
   - Visualizes component health status from the Supervisor
   - Displays agent activities and recovery actions
   - Shows real-time metrics for all components

2. **Supervisor with Knowledge Registry**:
   - Uses healing strategies stored in the Knowledge Registry
   - Communicates with the Learning System to improve strategies
   - Stores component metrics in the Knowledge Registry

3. **Knowledge Registry with TMUX Integration**:
   - Provides strategy visualization templates
   - Stores visualization preferences and layouts
   - Enables knowledge-driven monitoring configurations

## Common Use Cases

### System Health Monitoring

```rust
// Register for component health changes
registry.subscribe(move |event| {
    if let RegistryEvent::ComponentHealthChanged(component_id, old_health, new_health) = event {
        println!("Component {} health changed from {:?} to {:?}", 
                component_id, old_health, new_health);
                
        // Update visualization
        let status = ComponentStatus {
            id: component_id,
            status: convert_health_status(new_health),
            metrics: HashMap::new(),
            last_update: SystemTime::now(),
        };
        
        visualization.update_component_status(status);
    }
});
```

### Automated Recovery

```rust
// Register recovery action handlers
recovery.register_action_handler("restart", |action, component_id| {
    println!("Restarting component {}", component_id);
    
    // Perform restart logic here
    
    // Add activity to visualization
    visualization.add_agent_activity(AgentActivity {
        agent_id: "supervisor".to_string(),
        activity_type: ActivityType::Completed,
        description: format!("Restarted component {}", component_id),
        timestamp: SystemTime::now(),
        result: Some(ActivityResult::Success("Restart successful".to_string())),
    });
    
    Ok(())
});
```

### Learning from Recovery Actions

```rust
// Record feedback for healing strategies
learning.record_feedback(StrategyFeedback {
    strategy_id: KnowledgeId::new("hms", "healing_strategy", "restart", 1),
    component_id: "component-01".to_string(),
    success: true,
    execution_time: Duration::from_millis(250),
    metrics: HashMap::from([
        ("response_time_after".to_string(), 45.0),
        ("error_rate_after".to_string(), 0.2),
    ]),
    timestamp: SystemTime::now(),
});

// Evolve strategies based on feedback
let evolved_strategy_id = learning.evolve_strategy(&strategy_id)?;
```

## Advanced Features

### Custom Visualization Layouts

You can create custom visualization layouts for specific monitoring scenarios:

```rust
// Create a performance monitoring layout
visualization.create_window("performance")?;
visualization.split_window("performance", "cpu", SplitDirection::Horizontal)?;
visualization.split_window("performance", "memory", SplitDirection::Horizontal)?;
visualization.split_window("performance", "network", SplitDirection::Vertical)?;
visualization.set_layout("performance", "main-vertical")?;
```

### Custom Healing Policies

Create specialized healing policies for different component types:

```rust
// Database component policy
let db_policy = HealingPolicy {
    id: "database-connection-pool".to_string(),
    component_type: ComponentType::Custom(42), // Database type
    conditions: vec![
        PolicyCondition::MetricThreshold(
            "connection_errors".to_string(),
            10.0,
            ThresholdComparison::GreaterThan,
        ),
    ],
    actions: vec![
        SupervisorAction::Custom(
            "reset_connection_pool".to_string(),
            HashMap::from([
                ("pool_size".to_string(), "20".to_string()),
                ("timeout".to_string(), "5000".to_string()),
            ]),
        ),
    ],
    priority: 5,
    cooldown: Duration::from_secs(60),
    last_applied: None,
};

monitor.add_policy(db_policy)?;
```

### Schema Validation for Knowledge Items

Use schemas to validate knowledge items:

```rust
// Register a schema
let mut fields = HashMap::new();
fields.insert("name".to_string(), FieldDefinition {
    name: "name".to_string(),
    field_type: FieldType::String,
    description: Some("Component name".to_string()),
    default: None,
});
fields.insert("version".to_string(), FieldDefinition {
    name: "version".to_string(),
    field_type: FieldType::String,
    description: Some("Component version".to_string()),
    default: None,
});

let schema_def = SchemaDefinition {
    name: "component_info".to_string(),
    version: 1,
    fields,
    required: ["name", "version"].iter().map(|s| s.to_string()).collect(),
};

schema.register_schema(schema_def)?;

// Validate a knowledge value
schema.validate("component_info", 1, &value)?;
```

## Troubleshooting

### TMUX Session Issues

If you encounter issues with TMUX sessions:

1. Ensure TMUX is installed and available in your PATH
2. Check if there are existing sessions with `tmux ls`
3. Kill conflicting sessions with `tmux kill-session -t session_name`
4. Try setting `kill_on_drop: true` in the TmuxConfig

### Supervisor Component Issues

If components are not being monitored correctly:

1. Verify that component registrations are completed
2. Check that heartbeats are being sent regularly
3. Ensure policies have correct conditions for your metrics
4. Review recovery action handlers for proper implementation

### Knowledge Registry Issues

If knowledge items are not being stored or retrieved:

1. Verify that item IDs are correctly formatted
2. Check schema validation if items are being rejected
3. Ensure queries have correct namespace and knowledge type
4. Check for expired items with TTL settings