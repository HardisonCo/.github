# HMS Component Integration Guide

## 1. Overview

This guide documents how HMS components integrate with each other, with a focus on self-healing capabilities, TMUX integration, Supervisor component, Knowledge Registry, and MAC Framework. It provides practical guidance for component developers to ensure seamless integration across the HMS system.

## 2. Self-Healing Integration

### 2.1 Component Self-Healing Integration

Every HMS component should integrate with the self-healing system to ensure robustness and automatic recovery from failures. Here's how to integrate:

#### Step 1: Choose appropriate healing level

```rust
use crate::core::crates::self_healing::{
    HealingLevel, UnifiedHealingConfig, ImplementationConfig, HealingFactory
};

// For simple components
let level = HealingLevel::Basic;

// For important components
let level = HealingLevel::Advanced;

// For critical components
let level = HealingLevel::Full;
```

#### Step 2: Create configuration

```rust
let config = UnifiedHealingConfig {
    component_id: "my-component".to_string(),
    level,
    auto_healing_enabled: true,
    circuit_breaker_enabled: true,
    healing_timeout: 30,
    implementation_config: ImplementationConfig::Standalone(HashMap::new()),
};
```

#### Step 3: Create and initialize healing

```rust
// Create healing implementation
let mut healing = HealingFactory::create(config);

// Initialize (typically during component startup)
healing.initialize().await?;
```

#### Step 4: Integrate with component lifecycle

```rust
// During component health check
async fn check_health(&self) -> Result<HealthStatus> {
    // Check own health
    let component_health = self.internal_health_check();
    
    // Check self-healing health
    let healing_health = self.healing.check_health().await?;
    
    // Combine health status (use worse of the two)
    if component_health == HealthStatus::Healthy {
        Ok(healing_health)
    } else {
        Ok(component_health)
    }
}

// During component metrics reporting
async fn report_metrics(&self) {
    // Collect component metrics
    let cpu = self.get_cpu_usage();
    let memory = self.get_memory_usage();
    let response_time = self.get_avg_response_time();
    let errors = self.get_error_rate();
    let throughput = self.get_throughput();
    
    // Report to self-healing system
    let metrics = HealthMetrics {
        timestamp: SystemTime::now(),
        cpu_usage: cpu,
        memory_usage: memory,
        response_time,
        error_rate: errors,
        throughput,
        custom_metrics: HashMap::new(),
    };
    
    // Report metrics (implementation specific)
}

// During error handling
async fn handle_error(&self, error: &Error) {
    // Create issue from error
    let issue = Issue {
        id: Uuid::new_v4().to_string(),
        component: "my-component".to_string(),
        issue_type: error.type_name(),
        severity: map_severity(error.severity()),
        detected_at: SystemTime::now(),
        context: error.context(),
    };
    
    // Report issue (implementation specific)
    
    // Attempt healing if needed
    self.healing.heal().await?;
}
```

### 2.2 Cross-Component Healing Coordination

For issues that span multiple components, coordinate through the Supervisor:

```rust
// When detecting an issue that affects multiple components
async fn report_cross_component_issue(&self, issue: &Issue) {
    // Report to supervisor
    self.supervisor_client.report_issue(issue).await?;
    
    // Supervisor will coordinate healing across components
}
```

## 3. TMUX Integration

### 3.1 Component TMUX Integration

Components can integrate with TMUX for visualization and control using the TerminalInterface:

#### Step 1: Create terminal interface

```rust
use crate::core::mac::human_interface::terminal::{
    TerminalInterface, TerminalMode, TerminalLayout
};

// Create terminal interface
let terminal = TerminalInterface::new(
    "my-component",
    TerminalLayout::TwoByTwo,
    TerminalMode::Observe
);

// Initialize TMUX session
terminal.initialize().await?;
```

#### Step 2: Define panel layout

```rust
// Define panel layout
terminal.define_panel("metrics", 0, 0, "Component Metrics");
terminal.define_panel("logs", 0, 1, "Component Logs");
terminal.define_panel("status", 1, 0, "Health Status");
terminal.define_panel("actions", 1, 1, "Actions");
```

#### Step 3: Update panels with component information

```rust
// Update metrics panel
async fn update_metrics(&self) {
    let metrics = self.get_metrics();
    self.terminal.update_panel(
        "metrics", 
        format!("CPU: {}%\nMemory: {}MB\nErrors: {}%", 
                metrics.cpu, metrics.memory, metrics.errors)
    );
}

// Update logs panel
async fn log_message(&self, message: &str) {
    self.terminal.append_to_panel("logs", message);
}

// Update status panel
async fn update_status(&self) {
    let health = self.check_health().await?;
    let status = match health {
        HealthStatus::Healthy => "✅ Healthy",
        HealthStatus::Degraded(msg) => format!("⚠️ Degraded: {}", msg),
        HealthStatus::Critical(msg) => format!("🔴 Critical: {}", msg),
        HealthStatus::Failed(msg) => format!("❌ Failed: {}", msg),
    };
    self.terminal.update_panel("status", status);
}

// Update actions panel
async fn update_actions(&self) {
    let actions = self.get_available_actions();
    let actions_text = actions.join("\n");
    self.terminal.update_panel("actions", actions_text);
}
```

#### Step 4: Handle user input

```rust
// Set up input handler
terminal.set_input_handler(|input| {
    match input.trim() {
        "restart" => self.restart(),
        "status" => self.display_detailed_status(),
        "help" => self.display_help(),
        _ => self.unknown_command(input),
    }
});

// Start input handling
terminal.start_input_handling().await?;
```

### 3.2 Multi-Component TMUX Visualization

For visualizing multiple components in a single view:

```rust
// Create supervisor terminal interface
let supervisor_terminal = TerminalInterface::new(
    "supervisor",
    TerminalLayout::Custom(3, 3),
    TerminalMode::Observe
);

// Add component terminals as sub-panels
supervisor_terminal.add_component_panel("component1", 0, 0, 1, 1);
supervisor_terminal.add_component_panel("component2", 0, 1, 1, 1);
supervisor_terminal.add_component_panel("component3", 0, 2, 1, 1);

// Add overview panels
supervisor_terminal.define_panel("system-health", 1, 0, 1, 3, "System Health");
supervisor_terminal.define_panel("actions", 2, 0, 1, 3, "System Actions");

// Initialize all terminals
supervisor_terminal.initialize().await?;
```

## 4. Supervisor Integration

### 4.1 Component to Supervisor Integration

Components integrate with the Supervisor for system-wide coordination:

#### Step 1: Create supervisor client

```rust
use crate::core::supervisor::client::SupervisorClient;

// Create supervisor client
let supervisor = SupervisorClient::new("my-component");

// Connect to supervisor
supervisor.connect().await?;
```

#### Step 2: Register component

```rust
// Register component capabilities
let capabilities = ComponentCapabilities {
    can_restart: true,
    can_scale: false,
    can_failover: true,
    supported_recovery_actions: vec!["restart", "clear_cache", "reconnect"],
    healing_level: HealingLevel::Advanced,
};

supervisor.register_component("my-component", capabilities).await?;
```

#### Step 3: Report health and metrics

```rust
// Report health regularly
async fn report_health(&self) {
    let health = self.check_health().await?;
    self.supervisor.report_health(health).await?;
}

// Report metrics regularly
async fn report_metrics(&self) {
    let metrics = self.get_metrics();
    self.supervisor.report_metrics(metrics).await?;
}
```

#### Step 4: Handle supervisor commands

```rust
// Set up command handler
supervisor.set_command_handler(|command| {
    match command {
        SupervisorCommand::Restart => self.restart(),
        SupervisorCommand::ClearCache => self.clear_cache(),
        SupervisorCommand::UpdateConfig(config) => self.apply_config(config),
        SupervisorCommand::Shutdown => self.graceful_shutdown(),
        _ => Err(Error::UnsupportedCommand(command)),
    }
});

// Start command handling
supervisor.start_command_handling().await?;
```

### 4.2 Supervisor to Component Coordination

The Supervisor coordinates component activities:

```rust
// Supervisor coordinates healing across components
async fn coordinate_healing(&self, issue: &Issue) {
    // Determine affected components
    let affected = self.determine_affected_components(issue);
    
    // Plan recovery sequence
    let recovery_plan = self.plan_recovery(affected, issue);
    
    // Execute recovery actions in the right order
    for step in recovery_plan {
        match step {
            RecoveryStep::ComponentAction { component, action } => {
                self.send_command(component, action).await?;
            },
            RecoveryStep::WaitForHealth { component, timeout } => {
                self.wait_for_health(component, HealthStatus::Healthy, timeout).await?;
            },
            RecoveryStep::NotifyOperator(message) => {
                self.notify_operator(message).await?;
            }
        }
    }
}
```

## 5. Knowledge Registry Integration

### 5.1 Component to Knowledge Registry Integration

Components integrate with the Knowledge Registry to share and access knowledge:

#### Step 1: Create knowledge client

```rust
use crate::core::knowledge::client::KnowledgeClient;

// Create knowledge client
let knowledge = KnowledgeClient::new("my-component");

// Connect to knowledge registry
knowledge.connect().await?;
```

#### Step 2: Query knowledge

```rust
// Query for known issues
async fn check_known_issues(&self, symptom: &str) -> Vec<Issue> {
    let query = KnowledgeQuery::new()
        .component("my-component")
        .tag("issue")
        .contains(symptom);
    
    let results = self.knowledge.query(query).await?;
    
    // Parse results into issues
    results.into_iter()
        .map(|result| parse_issue_from_knowledge(result))
        .collect()
}

// Query for recovery strategies
async fn get_recovery_strategies(&self, issue_type: &str) -> Vec<RecoveryStrategy> {
    let query = KnowledgeQuery::new()
        .tag("recovery-strategy")
        .related_to(issue_type);
    
    let results = self.knowledge.query(query).await?;
    
    // Parse results into strategies
    results.into_iter()
        .map(|result| parse_strategy_from_knowledge(result))
        .collect()
}
```

#### Step 3: Contribute knowledge

```rust
// Contribute successful recovery
async fn contribute_recovery_knowledge(&self, issue: &Issue, action: &HealingAction, successful: bool) {
    let knowledge_item = KnowledgeItem::new()
        .component("my-component")
        .tags(vec!["recovery", "healing"])
        .content(serde_json::to_string(&RecoveryRecord {
            issue: issue.clone(),
            strategy: "my-strategy".to_string(),
            successful,
            action: action.clone(),
            timestamp: SystemTime::now(),
            duration: Duration::from_secs(1),
        })?);
    
    self.knowledge.contribute(knowledge_item).await?;
}

// Contribute new issue pattern
async fn contribute_issue_pattern(&self, issue: &Issue, symptoms: Vec<String>) {
    let knowledge_item = KnowledgeItem::new()
        .component("my-component")
        .tags(vec!["issue", "pattern"])
        .content(serde_json::to_string(&IssuePattern {
            issue_type: issue.issue_type.clone(),
            symptoms,
            severity: issue.severity,
        })?);
    
    self.knowledge.contribute(knowledge_item).await?;
}
```

### 5.2 Knowledge-Driven Healing

Components can use shared knowledge to improve healing:

```rust
// Use knowledge-driven healing
async fn knowledge_driven_heal(&self, issue: &Issue) -> Result<HealingAction> {
    // Query known successful strategies for this issue type
    let query = KnowledgeQuery::new()
        .tag("recovery")
        .related_to(&issue.issue_type)
        .filter("successful = true")
        .sort("timestamp", "desc")
        .limit(5);
    
    let results = self.knowledge.query(query).await?;
    
    if !results.is_empty() {
        // Try the most recently successful strategy first
        let latest = &results[0];
        let record: RecoveryRecord = serde_json::from_str(&latest.content)?;
        
        // Apply the strategy
        // Implementation depends on action type
        
        // Return the action
        Ok(record.action)
    } else {
        // Fall back to default healing
        self.healing.heal().await
    }
}
```

## 6. MAC Framework Integration

### 6.1 Component to MAC Framework Integration

Components integrate with the MAC Framework for multi-agent coordination:

#### Step 1: Create MAC client

```rust
use crate::core::mac::client::MacClient;

// Create MAC client
let mac = MacClient::new("my-component");

// Connect to MAC framework
mac.connect().await?;
```

#### Step 2: Register agent capabilities

```rust
// Register agent capabilities
let agent_capabilities = AgentCapabilities {
    can_process: vec!["data-analysis", "user-requests"],
    requires: vec!["database-access", "storage"],
    provides: vec!["analysis-results", "user-responses"],
    healing_level: HealingLevel::Advanced,
};

mac.register_agent("my-component-agent", agent_capabilities).await?;
```

#### Step 3: Handle MAC tasks

```rust
// Set up task handler
mac.set_task_handler(|task| {
    match task.task_type {
        "analyze-data" => self.analyze_data(task.payload),
        "process-request" => self.process_request(task.payload),
        "generate-report" => self.generate_report(task.payload),
        _ => Err(Error::UnsupportedTask(task.task_type)),
    }
});

// Start task handling
mac.start_task_handling().await?;
```

#### Step 4: Coordinate with other agents

```rust
// Request task execution by another agent
async fn request_database_query(&self, query: &str) -> Result<QueryResult> {
    let task = MacTask {
        task_type: "execute-query".to_string(),
        payload: serde_json::to_string(&query)?,
        priority: TaskPriority::Normal,
        timeout: Duration::from_secs(30),
    };
    
    let result = self.mac.request_task("database-agent", task).await?;
    
    // Parse result
    let query_result: QueryResult = serde_json::from_str(&result)?;
    Ok(query_result)
}
```

### 6.2 MAC-Driven Healing

The MAC Framework can coordinate healing across agents:

```rust
// MAC coordinator handles healing
async fn coordinate_healing(&self, issue: &Issue) {
    // Determine affected agents
    let affected = self.determine_affected_agents(issue);
    
    // Create healing coordination task
    let task = MacTask {
        task_type: "coordinate-healing".to_string(),
        payload: serde_json::to_string(&HealingCoordination {
            issue: issue.clone(),
            affected_agents: affected,
            priority: map_severity_to_priority(issue.severity),
        })?,
        priority: TaskPriority::High,
        timeout: Duration::from_secs(120),
    };
    
    // Send to supervisor agent
    self.request_task("supervisor-agent", task).await?;
}
```

## 7. Complete Integration Example

This example shows how all components integrate together:

```rust
use crate::core::crates::self_healing::{
    SelfHealing, HealingLevel, UnifiedHealingConfig, ImplementationConfig, HealingFactory
};
use crate::core::mac::human_interface::terminal::{
    TerminalInterface, TerminalMode, TerminalLayout
};
use crate::core::supervisor::client::SupervisorClient;
use crate::core::knowledge::client::KnowledgeClient;
use crate::core::mac::client::MacClient;

/// Integrated HMS component with all integration points
struct HmsComponent {
    // Component identification
    id: String,
    
    // Integration clients
    healing: Box<dyn SelfHealing>,
    terminal: TerminalInterface,
    supervisor: SupervisorClient,
    knowledge: KnowledgeClient,
    mac: MacClient,
    
    // Component state
    state: RwLock<ComponentState>,
}

impl HmsComponent {
    /// Create a new HMS component
    async fn new(id: &str) -> Result<Self> {
        // Create self-healing
        let healing_config = UnifiedHealingConfig {
            component_id: id.to_string(),
            level: HealingLevel::Advanced,
            auto_healing_enabled: true,
            circuit_breaker_enabled: true,
            healing_timeout: 30,
            implementation_config: ImplementationConfig::Hybrid(HashMap::new()),
        };
        
        let healing = HealingFactory::create(healing_config);
        
        // Create terminal interface
        let terminal = TerminalInterface::new(
            id,
            TerminalLayout::TwoByTwo,
            TerminalMode::Observe
        );
        
        // Create supervisor client
        let supervisor = SupervisorClient::new(id);
        
        // Create knowledge client
        let knowledge = KnowledgeClient::new(id);
        
        // Create MAC client
        let mac = MacClient::new(id);
        
        // Create component
        let component = Self {
            id: id.to_string(),
            healing,
            terminal,
            supervisor,
            knowledge,
            mac,
            state: RwLock::new(ComponentState::default()),
        };
        
        // Initialize all systems
        component.initialize().await?;
        
        Ok(component)
    }
    
    /// Initialize all integration points
    async fn initialize(&self) -> Result<()> {
        // Initialize self-healing
        self.healing.initialize().await?;
        
        // Initialize terminal
        self.terminal.initialize().await?;
        self.setup_terminal_panels().await?;
        
        // Connect to supervisor
        self.supervisor.connect().await?;
        self.register_with_supervisor().await?;
        
        // Connect to knowledge registry
        self.knowledge.connect().await?;
        
        // Connect to MAC framework
        self.mac.connect().await?;
        self.register_with_mac().await?;
        
        // Set up handlers
        self.setup_terminal_input_handler().await?;
        self.setup_supervisor_command_handler().await?;
        self.setup_mac_task_handler().await?;
        
        // Start background tasks
        self.start_health_reporting().await?;
        self.start_metrics_reporting().await?;
        self.start_terminal_updating().await?;
        
        Ok(())
    }
    
    /// Check component health
    async fn check_health(&self) -> Result<HealthStatus> {
        // Check internal health
        let internal_health = self.check_internal_health();
        
        // Check self-healing health
        let healing_health = self.healing.check_health().await?;
        
        // Combine health statuses (return worse of the two)
        let combined_health = match (internal_health, healing_health) {
            (HealthStatus::Failed(msg), _) | (_, HealthStatus::Failed(msg)) => {
                HealthStatus::Failed(msg)
            },
            (HealthStatus::Critical(msg), _) | (_, HealthStatus::Critical(msg)) => {
                HealthStatus::Critical(msg)
            },
            (HealthStatus::Degraded(msg), _) | (_, HealthStatus::Degraded(msg)) => {
                HealthStatus::Degraded(msg)
            },
            _ => HealthStatus::Healthy,
        };
        
        Ok(combined_health)
    }
    
    /// Handle an error with integrated healing
    async fn handle_error(&self, error: &Error) -> Result<()> {
        // Log the error
        self.terminal.append_to_panel("logs", &format!("ERROR: {}", error));
        
        // Create an issue
        let issue = Issue {
            id: Uuid::new_v4().to_string(),
            component: self.id.clone(),
            issue_type: error.type_name(),
            severity: map_severity(error.severity()),
            detected_at: SystemTime::now(),
            context: error.context(),
        };
        
        // Check knowledge for known issues
        let known_strategies = self.query_known_strategies(&issue).await?;
        
        // Attempt healing
        let healing_action = if !known_strategies.is_empty() {
            // Try knowledge-based strategy first
            self.apply_known_strategy(&issue, &known_strategies[0]).await?
        } else {
            // Fall back to default healing
            self.healing.heal().await?
        };
        
        // Update terminal with action
        self.terminal.append_to_panel(
            "actions", 
            &format!("Applied: {:?}", healing_action)
        );
        
        // Report to supervisor if serious
        if issue.severity >= Severity::Error {
            self.supervisor.report_issue(&issue).await?;
        }
        
        // Contribute knowledge
        self.contribute_recovery_knowledge(&issue, &healing_action, true).await?;
        
        Ok(())
    }
}
```

## 8. Integration Points Quick Reference

| Component | Integration Points | Key Interfaces |
|-----------|-------------------|----------------|
| Self-Healing | - Component health<br>- Error handling<br>- Metrics reporting<br>- Configuration | `SelfHealing`<br>`HealingFactory`<br>`HealingLevel` |
| TMUX | - UI visualization<br>- User interaction<br>- Multi-panel display<br>- Status reporting | `TerminalInterface`<br>`TerminalMode`<br>`TerminalLayout` |
| Supervisor | - Component registration<br>- Health reporting<br>- Command handling<br>- System-wide coordination | `SupervisorClient`<br>`ComponentCapabilities`<br>`SupervisorCommand` |
| Knowledge Registry | - Knowledge queries<br>- Knowledge contribution<br>- Strategy discovery<br>- Issue pattern recognition | `KnowledgeClient`<br>`KnowledgeQuery`<br>`KnowledgeItem` |
| MAC Framework | - Agent registration<br>- Task handling<br>- Cross-agent coordination<br>- Distributed healing | `MacClient`<br>`AgentCapabilities`<br>`MacTask` |

## 9. Best Practices for Integration

1. **Order of Initialization**
   - Initialize self-healing first
   - Terminal interface second
   - Connect to supervisor, knowledge registry, and MAC framework after
   - Set up handlers last

2. **Health and Metrics Reporting**
   - Report health status every 5-10 seconds
   - Report detailed metrics every 30-60 seconds
   - Use appropriate severity levels for issues
   - Include context with issue reports

3. **Error Handling Flow**
   - Log errors first
   - Create structured issues from errors
   - Check knowledge registry for known strategies
   - Attempt self-healing
   - Report to supervisor if serious
   - Contribute recovery knowledge

4. **Configuration Management**
   - Use default configurations for development
   - Load configurations from environment for production
   - Accept configuration updates from supervisor
   - Validate all configuration changes before applying

5. **Resource Efficiency**
   - Use appropriate healing level for component criticality
   - Batch metrics reporting when possible
   - Use debouncing for frequent updates
   - Clean up resources during shutdown