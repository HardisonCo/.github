# Health Monitoring System Specification

## 1. Overview

The Health Monitoring System is a critical component of the HMS self-healing architecture. It continuously monitors the health of various system components, detects anomalies, and triggers appropriate recovery actions when issues are detected. This specification provides comprehensive implementation details, interface definitions, and integration plans for the Health Monitoring System.

## 2. Interface Definitions

### 2.1 Core Traits and Structures

```rust
/// Represents the result of a health check
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HealthCheckResult {
    /// Unique identifier for the component being checked
    pub component_id: String,
    /// Current status of the component
    pub status: HealthStatus,
    /// Detailed message about the health check result
    pub message: String,
    /// Timestamp when the check was performed
    pub timestamp: DateTime<Utc>,
    /// Additional metadata about the health check
    pub metadata: HashMap<String, Value>,
    /// Performance metrics collected during the check
    pub metrics: HashMap<String, f64>,
}

/// Represents the possible health statuses of a component
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum HealthStatus {
    /// Component is functioning normally
    Healthy,
    /// Component is functioning but with degraded performance
    Degraded,
    /// Component is functioning but approaching failure threshold
    Warning,
    /// Component has failed but may recover automatically
    Unhealthy,
    /// Component has failed and requires manual intervention
    Critical,
    /// Component status could not be determined
    Unknown,
}

/// Function type for health check implementations
pub type HealthCheckFn = Box<dyn Fn() -> HealthCheckResult + Send + Sync>;

/// Trait for components that can be health-checked
pub trait HealthCheckable {
    /// Returns the component's unique identifier
    fn component_id(&self) -> String;
    
    /// Performs a health check on the component
    fn check_health(&self) -> HealthCheckResult;
    
    /// Returns a list of dependencies for this component
    fn dependencies(&self) -> Vec<String> {
        Vec::new()
    }
}

/// Listener for health status changes
pub trait HealthStatusListener: Send + Sync {
    /// Called when a component's health status changes
    fn on_status_change(&self, old_result: Option<&HealthCheckResult>, new_result: &HealthCheckResult);
}
```

### 2.2 Health Monitor Interface

```rust
/// Main health monitoring system
pub struct HealthMonitor {
    health_checks: Arc<Mutex<HashMap<String, HealthCheckFn>>>,
    statuses: Arc<RwLock<HashMap<String, HealthCheckResult>>>,
    recovery_manager: Option<Arc<RecoveryManager>>,
    circuit_breakers: HashMap<String, Arc<Mutex<CircuitBreaker>>>,
    listeners: Arc<Mutex<Vec<Box<dyn HealthStatusListener>>>>,
    running: Arc<AtomicBool>,
    check_interval: Duration,
    health_history: Arc<Mutex<HashMap<String, VecDeque<HealthCheckResult>>>>,
    max_history_length: usize,
    dependency_graph: Arc<RwLock<DiGraph<String, ()>>>,
    node_indices: Arc<RwLock<HashMap<String, NodeIndex>>>,
}

impl HealthMonitor {
    /// Creates a new health monitoring system
    pub fn new(check_interval: Duration, max_history_length: usize) -> Self;
    
    /// Registers a health check function for a component
    pub fn register_check<F>(&self, component_id: &str, check: F) -> Result<(), Error>
    where
        F: Fn() -> HealthCheckResult + Send + Sync + 'static;
    
    /// Registers a component that implements HealthCheckable
    pub fn register_component<T: HealthCheckable + 'static>(&self, component: Arc<T>) -> Result<(), Error>;
    
    /// Sets the recovery manager for automatic recovery actions
    pub fn set_recovery_manager(&mut self, recovery_manager: Arc<RecoveryManager>);
    
    /// Registers a circuit breaker for a component
    pub fn register_circuit_breaker(&mut self, component_id: &str, circuit_breaker: Arc<Mutex<CircuitBreaker>>);
    
    /// Adds a health status listener
    pub fn add_listener<L: HealthStatusListener + 'static>(&self, listener: L);
    
    /// Starts the health monitoring background task
    pub fn start(&self) -> Result<(), Error>;
    
    /// Stops the health monitoring background task
    pub fn stop(&self) -> Result<(), Error>;
    
    /// Gets the current health status for a component
    pub fn get_status(&self, component_id: &str) -> Option<HealthCheckResult>;
    
    /// Gets the health status history for a component
    pub fn get_history(&self, component_id: &str) -> Option<Vec<HealthCheckResult>>;
    
    /// Triggers immediate health check for a component
    pub fn check_now(&self, component_id: &str) -> Result<HealthCheckResult, Error>;
    
    /// Returns list of all monitored components
    pub fn monitored_components(&self) -> Vec<String>;
    
    /// Returns a hierarchical representation of component dependencies
    pub fn dependency_tree(&self) -> HashMap<String, Vec<String>>;
    
    /// Analyzes trends in component health over time
    pub fn analyze_trends(&self, component_id: &str, window: Duration) -> Result<HealthTrend, Error>;
    
    /// Registers a dependency between components
    pub fn register_dependency(&self, dependent: &str, dependency: &str) -> Result<(), Error>;
}
```

### 2.3 Health Trend Analysis

```rust
/// Represents trend analysis of component health
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HealthTrend {
    pub component_id: String,
    pub start_time: DateTime<Utc>,
    pub end_time: DateTime<Utc>,
    pub status_counts: HashMap<HealthStatus, usize>,
    pub status_durations: HashMap<HealthStatus, Duration>,
    pub metric_trends: HashMap<String, MetricTrend>,
    pub stability_score: f64,
    pub prediction: Option<HealthPrediction>,
}

/// Represents trend analysis for a specific metric
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MetricTrend {
    pub name: String,
    pub min: f64,
    pub max: f64,
    pub mean: f64,
    pub median: f64,
    pub stddev: f64,
    pub trend_slope: f64,
    pub is_concerning: bool,
}

/// Represents a prediction of future health status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HealthPrediction {
    pub predicted_status: HealthStatus,
    pub confidence: f64,
    pub time_horizon: Duration,
    pub potential_issues: Vec<String>,
}
```

## 3. Implementation Details

### 3.1 Health Check Execution Model

The Health Monitor operates on a background thread that periodically executes registered health checks. This architecture ensures that health monitoring does not interfere with the normal operation of the system. The execution model follows these steps:

1. Upon starting, the Health Monitor spawns a background task using `tokio::spawn`.
2. The task loops at the specified check interval.
3. On each iteration, it executes all registered health checks in parallel using `futures::future::join_all`.
4. Results are collected and compared with previous statuses to detect changes.
5. Status changes trigger notifications to registered listeners.
6. If configured, the Circuit Breaker and Recovery Manager are notified of health status changes.

```rust
async fn run_checks(self: Arc<Self>) {
    let running = self.running.clone();
    while running.load(Ordering::SeqCst) {
        let component_ids = {
            let checks = self.health_checks.lock().await;
            checks.keys().cloned().collect::<Vec<_>>()
        };
        
        let futures: Vec<_> = component_ids.iter().map(|id| {
            let id = id.clone();
            let self_clone = self.clone();
            async move {
                self_clone.check_component(&id).await
            }
        }).collect();
        
        let results = futures::future::join_all(futures).await;
        
        for result in results {
            if let Ok((component_id, health_result)) = result {
                self.update_status(component_id, health_result).await;
            }
        }
        
        tokio::time::sleep(self.check_interval).await;
    }
}
```

### 3.2 Dependency Graph Management

The Health Monitor maintains a directed graph of component dependencies using the `petgraph` crate. This enables:

1. Topological sorting of components for ordered health checks
2. Root cause analysis when multiple components fail
3. Impact analysis to determine which components will be affected by a failure

```rust
fn build_dependency_graph(&self) -> DiGraph<String, ()> {
    let mut graph = DiGraph::<String, ()>::new();
    let mut node_indices = HashMap::new();
    
    // Add all components as nodes
    let components = self.monitored_components();
    for component in &components {
        let node_idx = graph.add_node(component.clone());
        node_indices.insert(component.clone(), node_idx);
    }
    
    // Add edges for dependencies
    for component in components {
        if let Some(deps) = self.component_dependencies(&component) {
            for dep in deps {
                if let (Some(&from), Some(&to)) = (node_indices.get(&component), node_indices.get(&dep)) {
                    graph.add_edge(from, to, ());
                }
            }
        }
    }
    
    graph
}
```

### 3.3 Health Status Detection Algorithms

The Health Monitor employs several algorithms to detect various types of health issues:

#### 3.3.1 Threshold-Based Detection

Simple threshold-based detection compares metric values against predefined thresholds.

```rust
fn check_thresholds(metrics: &HashMap<String, f64>, thresholds: &HashMap<String, (f64, f64)>) -> Vec<String> {
    let mut violations = Vec::new();
    
    for (metric_name, value) in metrics {
        if let Some((min, max)) = thresholds.get(metric_name) {
            if value < min {
                violations.push(format!("{} below minimum threshold: {} < {}", metric_name, value, min));
            } else if value > max {
                violations.push(format!("{} above maximum threshold: {} > {}", metric_name, value, max));
            }
        }
    }
    
    violations
}
```

#### 3.3.2 Statistical Anomaly Detection

More sophisticated detection uses statistical methods to identify anomalies in metric time series.

```rust
fn detect_anomalies(history: &VecDeque<HealthCheckResult>, sensitivity: f64) -> Vec<String> {
    let mut anomalies = Vec::new();
    
    // Extract time series for each metric
    let mut metric_series: HashMap<String, Vec<f64>> = HashMap::new();
    for result in history {
        for (metric, value) in &result.metrics {
            metric_series.entry(metric.clone())
                .or_insert_with(Vec::new)
                .push(*value);
        }
    }
    
    // Apply anomaly detection to each metric
    for (metric, series) in metric_series {
        if series.len() < 10 {
            continue; // Not enough data points
        }
        
        // Calculate mean and standard deviation
        let mean = series.iter().sum::<f64>() / series.len() as f64;
        let variance = series.iter()
            .map(|x| (x - mean).powi(2))
            .sum::<f64>() / series.len() as f64;
        let stddev = variance.sqrt();
        
        // Check if latest value is an anomaly
        if let Some(latest) = series.last() {
            let z_score = (latest - mean).abs() / stddev;
            if z_score > sensitivity {
                anomalies.push(format!("{} is anomalous (z-score: {:.2})", metric, z_score));
            }
        }
    }
    
    anomalies
}
```

#### 3.3.3 Trend Analysis

Trend analysis detects gradual degradation by analyzing the slope of metrics over time.

```rust
fn analyze_trend(series: &[(DateTime<Utc>, f64)]) -> Option<f64> {
    if series.len() < 3 {
        return None;
    }
    
    // Convert to relative time (seconds from start)
    let start_time = series[0].0;
    let x: Vec<f64> = series.iter()
        .map(|(t, _)| (*t - start_time).num_seconds() as f64)
        .collect();
    let y: Vec<f64> = series.iter().map(|(_, v)| *v).collect();
    
    // Calculate linear regression
    let n = x.len() as f64;
    let sum_x: f64 = x.iter().sum();
    let sum_y: f64 = y.iter().sum();
    let sum_xy: f64 = x.iter().zip(y.iter()).map(|(x, y)| x * y).sum();
    let sum_xx: f64 = x.iter().map(|x| x * x).sum();
    
    let slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x);
    
    Some(slope)
}
```

### 3.4 Health History Management

The Health Monitor maintains a history of health check results for each component, with the following considerations:

1. Memory efficiency: History is stored in a ring buffer (VecDeque) with a configurable maximum size
2. Thread safety: Access to history is protected by a mutex
3. Persistence: Optional periodic serialization to disk for long-term analysis

```rust
fn update_history(&self, component_id: &str, result: HealthCheckResult) {
    let mut history = self.health_history.lock().unwrap();
    
    let component_history = history.entry(component_id.to_string())
        .or_insert_with(VecDeque::new);
        
    if component_history.len() >= self.max_history_length {
        component_history.pop_front();
    }
    
    component_history.push_back(result);
}
```

## 4. HMS-Specific Health Checks

The following are specific health checks that will be implemented for HMS components:

### 4.1 Agent Health Checks

```rust
pub struct AgentHealthCheck {
    agent_id: String,
    timeout: Duration,
    agent_comm_channel: mpsc::Sender<AgentHealthRequest>,
    response_channel: mpsc::Receiver<AgentHealthResponse>,
}

impl HealthCheckable for AgentHealthCheck {
    fn component_id(&self) -> String {
        format!("agent:{}", self.agent_id)
    }
    
    fn check_health(&self) -> HealthCheckResult {
        // Send ping request to agent
        let request = AgentHealthRequest::Ping;
        match self.agent_comm_channel.try_send(request) {
            Ok(_) => {
                // Wait for response with timeout
                match tokio::time::timeout(self.timeout, self.response_channel.recv()).await {
                    Ok(Some(AgentHealthResponse::Pong(metrics))) => {
                        // Process agent metrics
                        let mut result = HealthCheckResult {
                            component_id: self.component_id(),
                            status: HealthStatus::Healthy,
                            message: "Agent responsive".to_string(),
                            timestamp: Utc::now(),
                            metadata: HashMap::new(),
                            metrics: metrics,
                        };
                        
                        // Check memory usage
                        if let Some(memory_usage) = metrics.get("memory_usage_mb") {
                            if *memory_usage > 500.0 {
                                result.status = HealthStatus::Warning;
                                result.message = format!("Agent memory usage high: {:.2} MB", memory_usage);
                            }
                        }
                        
                        // Check message queue length
                        if let Some(queue_length) = metrics.get("message_queue_length") {
                            if *queue_length > 100.0 {
                                result.status = HealthStatus::Degraded;
                                result.message = format!("Agent message queue backlog: {}", queue_length);
                            }
                        }
                        
                        result
                    },
                    _ => HealthCheckResult {
                        component_id: self.component_id(),
                        status: HealthStatus::Unhealthy,
                        message: "Agent not responding to ping".to_string(),
                        timestamp: Utc::now(),
                        metadata: HashMap::new(),
                        metrics: HashMap::new(),
                    }
                }
            },
            Err(_) => HealthCheckResult {
                component_id: self.component_id(),
                status: HealthStatus::Critical,
                message: "Cannot communicate with agent".to_string(),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        }
    }
    
    fn dependencies(&self) -> Vec<String> {
        vec!["system:agent_communication_bus".to_string()]
    }
}
```

### 4.2 API Service Health Checks

```rust
pub struct ApiServiceHealthCheck {
    service_url: String,
    client: reqwest::Client,
    auth_token: Option<String>,
    expected_status: StatusCode,
}

impl HealthCheckable for ApiServiceHealthCheck {
    fn component_id(&self) -> String {
        format!("api:{}", self.service_url)
    }
    
    fn check_health(&self) -> HealthCheckResult {
        let start_time = Instant::now();
        let mut request = self.client.get(&self.service_url);
        
        if let Some(token) = &self.auth_token {
            request = request.header("Authorization", format!("Bearer {}", token));
        }
        
        match request.send() {
            Ok(response) => {
                let status = response.status();
                let latency = start_time.elapsed().as_millis() as f64;
                
                let mut metrics = HashMap::new();
                metrics.insert("latency_ms".to_string(), latency);
                
                if status == self.expected_status {
                    HealthCheckResult {
                        component_id: self.component_id(),
                        status: if latency > 1000.0 { HealthStatus::Degraded } else { HealthStatus::Healthy },
                        message: format!("API responsive with status {}", status),
                        timestamp: Utc::now(),
                        metadata: HashMap::new(),
                        metrics,
                    }
                } else {
                    HealthCheckResult {
                        component_id: self.component_id(),
                        status: HealthStatus::Unhealthy,
                        message: format!("Unexpected status code: {} (expected {})", status, self.expected_status),
                        timestamp: Utc::now(),
                        metadata: HashMap::new(),
                        metrics,
                    }
                }
            },
            Err(e) => HealthCheckResult {
                component_id: self.component_id(),
                status: HealthStatus::Critical,
                message: format!("API request failed: {}", e),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        }
    }
    
    fn dependencies(&self) -> Vec<String> {
        vec!["network:external".to_string()]
    }
}
```

### 4.3 Database Health Checks

```rust
pub struct DatabaseHealthCheck<T: Database> {
    database: Arc<T>,
    query_timeout: Duration,
}

impl<T: Database> HealthCheckable for DatabaseHealthCheck<T> {
    fn component_id(&self) -> String {
        format!("database:{}", self.database.name())
    }
    
    fn check_health(&self) -> HealthCheckResult {
        let start_time = Instant::now();
        
        match tokio::time::timeout(self.query_timeout, self.database.ping()).await {
            Ok(Ok(_)) => {
                let latency = start_time.elapsed().as_millis() as f64;
                
                // Collect additional metrics
                let mut metrics = HashMap::new();
                metrics.insert("latency_ms".to_string(), latency);
                
                if let Ok(conn_metrics) = self.database.connection_metrics().await {
                    metrics.extend(conn_metrics);
                }
                
                // Determine status based on metrics
                let status = if latency > 500.0 || 
                              metrics.get("active_connections").map_or(0.0, |v| *v) > metrics.get("max_connections").map_or(100.0, |v| *v) * 0.9 {
                    HealthStatus::Degraded
                } else {
                    HealthStatus::Healthy
                };
                
                HealthCheckResult {
                    component_id: self.component_id(),
                    status,
                    message: "Database responsive".to_string(),
                    timestamp: Utc::now(),
                    metadata: HashMap::new(),
                    metrics,
                }
            },
            _ => HealthCheckResult {
                component_id: self.component_id(),
                status: HealthStatus::Critical,
                message: "Database not responding".to_string(),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        }
    }
    
    fn dependencies(&self) -> Vec<String> {
        vec!["network:internal".to_string()]
    }
}
```

### 4.4 Resource Usage Health Checks

```rust
pub struct SystemResourceCheck {
    hostname: String,
    cpu_threshold: f64,
    memory_threshold: f64,
    disk_threshold: f64,
}

impl HealthCheckable for SystemResourceCheck {
    fn component_id(&self) -> String {
        format!("system:{}", self.hostname)
    }
    
    fn check_health(&self) -> HealthCheckResult {
        let mut metrics = HashMap::new();
        let mut issues = Vec::new();
        
        // CPU usage
        let cpu_usage = sys_info::loadavg().map(|la| la.one).unwrap_or(0.0);
        metrics.insert("cpu_load_1m".to_string(), cpu_usage);
        
        if cpu_usage > self.cpu_threshold {
            issues.push(format!("CPU usage too high: {:.2}%", cpu_usage * 100.0));
        }
        
        // Memory usage
        if let Ok(mem_info) = sys_info::mem_info() {
            let total_kb = mem_info.total as f64;
            let free_kb = mem_info.free as f64;
            let used_percent = 100.0 * (1.0 - (free_kb / total_kb));
            
            metrics.insert("memory_total_kb".to_string(), total_kb);
            metrics.insert("memory_free_kb".to_string(), free_kb);
            metrics.insert("memory_used_percent".to_string(), used_percent);
            
            if used_percent > self.memory_threshold * 100.0 {
                issues.push(format!("Memory usage too high: {:.2}%", used_percent));
            }
        }
        
        // Disk usage
        if let Ok(disk_info) = sys_info::disk_info() {
            let total_kb = disk_info.total as f64;
            let free_kb = disk_info.free as f64;
            let used_percent = 100.0 * (1.0 - (free_kb / total_kb));
            
            metrics.insert("disk_total_kb".to_string(), total_kb);
            metrics.insert("disk_free_kb".to_string(), free_kb);
            metrics.insert("disk_used_percent".to_string(), used_percent);
            
            if used_percent > self.disk_threshold * 100.0 {
                issues.push(format!("Disk usage too high: {:.2}%", used_percent));
            }
        }
        
        // Determine overall status
        let status = if issues.is_empty() {
            HealthStatus::Healthy
        } else if issues.iter().any(|issue| issue.contains("too high")) {
            HealthStatus::Warning
        } else {
            HealthStatus::Degraded
        };
        
        HealthCheckResult {
            component_id: self.component_id(),
            status,
            message: if issues.is_empty() { 
                "System resources within normal parameters".to_string() 
            } else { 
                issues.join("; ") 
            },
            timestamp: Utc::now(),
            metadata: HashMap::new(),
            metrics,
        }
    }
}
```

## 5. Integration with Other Components

### 5.1 Integration with Recovery Manager

The Health Monitor integrates with the Recovery Manager to trigger automated recovery actions when health issues are detected:

```rust
impl HealthStatusListener for RecoveryManagerListener {
    fn on_status_change(&self, old_result: Option<&HealthCheckResult>, new_result: &HealthCheckResult) {
        // Only trigger recovery for transitions to unhealthy states
        if new_result.status == HealthStatus::Unhealthy || new_result.status == HealthStatus::Critical {
            if old_result.map_or(true, |r| r.status != new_result.status) {
                let component_id = new_result.component_id.clone();
                let recovery_manager = self.recovery_manager.clone();
                let new_result = new_result.clone();
                
                tokio::spawn(async move {
                    let recovery_strategy = match new_result.status {
                        HealthStatus::Unhealthy => RecoveryStrategy::Automatic,
                        HealthStatus::Critical => RecoveryStrategy::Escalated,
                        _ => return,
                    };
                    
                    recovery_manager.initiate_recovery(
                        &component_id,
                        recovery_strategy,
                        Some(new_result),
                    ).await;
                });
            }
        }
    }
}
```

### 5.2 Integration with Circuit Breaker

The Health Monitor updates circuit breakers when health status changes:

```rust
impl HealthStatusListener for CircuitBreakerListener {
    fn on_status_change(&self, _old_result: Option<&HealthCheckResult>, new_result: &HealthCheckResult) {
        let circuit_breakers = self.circuit_breakers.lock().unwrap();
        
        if let Some(breaker) = circuit_breakers.get(&new_result.component_id) {
            let mut breaker = breaker.lock().unwrap();
            
            match new_result.status {
                HealthStatus::Healthy => breaker.record_success(),
                HealthStatus::Degraded | HealthStatus::Warning => {
                    // No change to circuit breaker state
                },
                HealthStatus::Unhealthy | HealthStatus::Critical => breaker.record_failure(),
                HealthStatus::Unknown => {
                    // No reliable information, don't change state
                }
            }
        }
    }
}
```

### 5.3 Integration with Adaptive Configuration

The Health Monitor provides feedback to the Adaptive Configuration system for dynamic reconfiguration:

```rust
impl HealthStatusListener for AdaptiveConfigListener {
    fn on_status_change(&self, old_result: Option<&HealthCheckResult>, new_result: &HealthCheckResult) {
        // Only trigger configuration changes for persistent problems
        if old_result.map_or(false, |r| r.status != HealthStatus::Healthy && new_result.status != HealthStatus::Healthy) {
            let component_id = new_result.component_id.clone();
            let adaptive_config = self.adaptive_config.clone();
            let metrics = new_result.metrics.clone();
            
            tokio::spawn(async move {
                // First try the fast adaptation path
                if let Err(_) = adaptive_config.apply_predefined_adaptation(&component_id, &metrics).await {
                    // If that fails, trigger genetic algorithm optimization
                    adaptive_config.schedule_optimization(&component_id).await;
                }
            });
        }
    }
}
```

### 5.4 Integration with Metrics Collector

The Health Monitor publishes health metrics to the Metrics Collector:

```rust
impl HealthStatusListener for MetricsCollectorListener {
    fn on_status_change(&self, _old_result: Option<&HealthCheckResult>, new_result: &HealthCheckResult) {
        let metrics_collector = self.metrics_collector.clone();
        let component_id = new_result.component_id.clone();
        let status = new_result.status.clone();
        let timestamp = new_result.timestamp;
        let component_metrics = new_result.metrics.clone();
        
        tokio::spawn(async move {
            // Record component health status as a metric
            let status_value = match status {
                HealthStatus::Healthy => 1.0,
                HealthStatus::Degraded => 0.75,
                HealthStatus::Warning => 0.5,
                HealthStatus::Unhealthy => 0.25,
                HealthStatus::Critical => 0.0,
                HealthStatus::Unknown => -1.0,
            };
            
            let mut metrics = HashMap::new();
            metrics.insert(format!("{}.health_status", component_id), status_value);
            
            // Add component-specific metrics with component_id prefix
            for (metric_name, value) in component_metrics {
                metrics.insert(format!("{}.{}", component_id, metric_name), value);
            }
            
            metrics_collector.record_multiple(metrics, Some(timestamp)).await;
        });
    }
}
```

## 6. Testing Strategy

### 6.1 Unit Tests

Unit tests for the Health Monitoring System will focus on individual components and algorithms:

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_health_check_registration() {
        let monitor = HealthMonitor::new(Duration::from_secs(5), 100);
        
        // Test registering a valid health check
        let result = monitor.register_check("test_component", || {
            HealthCheckResult {
                component_id: "test_component".to_string(),
                status: HealthStatus::Healthy,
                message: "Test component is healthy".to_string(),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        });
        
        assert!(result.is_ok());
        assert_eq!(monitor.monitored_components().len(), 1);
        
        // Test duplicate registration
        let result = monitor.register_check("test_component", || {
            HealthCheckResult {
                component_id: "test_component".to_string(),
                status: HealthStatus::Healthy,
                message: "Test component is healthy".to_string(),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        });
        
        assert!(result.is_err());
    }
    
    #[tokio::test]
    async fn test_health_status_change_notification() {
        let monitor = HealthMonitor::new(Duration::from_secs(5), 100);
        
        // Create a mock listener
        struct MockListener {
            notifications: Arc<Mutex<Vec<(Option<HealthStatus>, HealthStatus)>>>,
        }
        
        impl HealthStatusListener for MockListener {
            fn on_status_change(&self, old_result: Option<&HealthCheckResult>, new_result: &HealthCheckResult) {
                let old_status = old_result.map(|r| r.status.clone());
                let mut notifications = self.notifications.lock().unwrap();
                notifications.push((old_status, new_result.status.clone()));
            }
        }
        
        let notifications = Arc::new(Mutex::new(Vec::new()));
        let listener = MockListener { notifications: notifications.clone() };
        
        monitor.add_listener(listener);
        
        // Register a component with changing health
        let mut health_status = Arc::new(Mutex::new(HealthStatus::Healthy));
        let health_status_clone = health_status.clone();
        
        monitor.register_check("test_component", move || {
            let status = health_status_clone.lock().unwrap().clone();
            HealthCheckResult {
                component_id: "test_component".to_string(),
                status,
                message: "Test status".to_string(),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        }).unwrap();
        
        // Initial check
        monitor.check_now("test_component").await.unwrap();
        
        // Change status
        {
            let mut status = health_status.lock().unwrap();
            *status = HealthStatus::Degraded;
        }
        
        // Check again
        monitor.check_now("test_component").await.unwrap();
        
        // Verify notification
        let notifications = notifications.lock().unwrap();
        assert_eq!(notifications.len(), 2);
        assert_eq!(notifications[0].1, HealthStatus::Healthy);
        assert_eq!(notifications[1].0, Some(HealthStatus::Healthy));
        assert_eq!(notifications[1].1, HealthStatus::Degraded);
    }
    
    #[tokio::test]
    async fn test_health_history() {
        let monitor = HealthMonitor::new(Duration::from_secs(5), 3); // Max history of 3
        
        monitor.register_check("test_component", || {
            HealthCheckResult {
                component_id: "test_component".to_string(),
                status: HealthStatus::Healthy,
                message: "Test component is healthy".to_string(),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        }).unwrap();
        
        // Run multiple checks
        for _ in 0..5 {
            monitor.check_now("test_component").await.unwrap();
        }
        
        // Verify history length is capped
        let history = monitor.get_history("test_component").unwrap();
        assert_eq!(history.len(), 3);
    }
    
    #[tokio::test]
    async fn test_anomaly_detection() {
        // Create synthetic time series with an anomaly
        let mut series = Vec::new();
        for i in 0..20 {
            let value = if i == 15 { 100.0 } else { 10.0 + (i as f64 * 0.1) };
            series.push(value);
        }
        
        let anomalies = detect_anomalies_in_series(&series, 3.0);
        assert_eq!(anomalies.len(), 1);
        assert!(anomalies[0].contains("anomalous"));
    }
}
```

### 6.2 Integration Tests

Integration tests will verify the Health Monitor's interactions with other components:

```rust
#[cfg(test)]
mod integration_tests {
    use super::*;
    
    #[tokio::test]
    async fn test_health_monitor_with_recovery_manager() {
        // Create test components
        let monitor = HealthMonitor::new(Duration::from_secs(1), 100);
        let recovery_manager = Arc::new(RecoveryManager::new(100));
        
        // Configure recovery manager with a test strategy
        recovery_manager.register_strategy("test_component", RecoveryStrategy::Automatic).await.unwrap();
        
        let recovery_count = Arc::new(AtomicUsize::new(0));
        let recovery_count_clone = recovery_count.clone();
        
        recovery_manager.register_handler("test_component", Box::new(move |_component_id, _context| {
            recovery_count_clone.fetch_add(1, Ordering::SeqCst);
            Ok(RecoveryResult {
                successful: true,
                message: "Test recovery performed".to_string(),
                timestamp: Utc::now(),
            })
        })).await.unwrap();
        
        // Link components
        monitor.set_recovery_manager(recovery_manager);
        
        // Register a failing component
        monitor.register_check("test_component", || {
            HealthCheckResult {
                component_id: "test_component".to_string(),
                status: HealthStatus::Unhealthy,
                message: "Test component is unhealthy".to_string(),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        }).unwrap();
        
        // Start monitoring
        monitor.start().await.unwrap();
        
        // Wait for recovery to be triggered
        tokio::time::sleep(Duration::from_secs(3)).await;
        
        // Verify recovery was attempted
        assert!(recovery_count.load(Ordering::SeqCst) > 0);
        
        // Clean up
        monitor.stop().await.unwrap();
    }
    
    #[tokio::test]
    async fn test_health_monitor_with_circuit_breaker() {
        // Create test components
        let monitor = HealthMonitor::new(Duration::from_secs(1), 100);
        let circuit_breaker = Arc::new(Mutex::new(CircuitBreaker::new(
            "test_component",
            2,
            2,
            Duration::from_secs(5),
        )));
        
        // Link components
        monitor.register_circuit_breaker("test_component", circuit_breaker.clone());
        
        // Register a component with changing health
        let mut health_status = Arc::new(Mutex::new(HealthStatus::Healthy));
        let health_status_clone = health_status.clone();
        
        monitor.register_check("test_component", move || {
            let status = health_status_clone.lock().unwrap().clone();
            HealthCheckResult {
                component_id: "test_component".to_string(),
                status,
                message: "Test status".to_string(),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        }).unwrap();
        
        // Start with initial check
        monitor.check_now("test_component").await.unwrap();
        
        // Verify initial state
        {
            let breaker = circuit_breaker.lock().unwrap();
            assert_eq!(breaker.state(), CircuitState::Closed);
        }
        
        // Change to unhealthy and check twice to trigger circuit breaker
        {
            let mut status = health_status.lock().unwrap();
            *status = HealthStatus::Unhealthy;
        }
        
        monitor.check_now("test_component").await.unwrap();
        monitor.check_now("test_component").await.unwrap();
        
        // Verify circuit breaker opened
        {
            let breaker = circuit_breaker.lock().unwrap();
            assert_eq!(breaker.state(), CircuitState::Open);
        }
        
        // Change back to healthy
        {
            let mut status = health_status.lock().unwrap();
            *status = HealthStatus::Healthy;
        }
        
        // Wait for reset timeout
        tokio::time::sleep(Duration::from_secs(5)).await;
        
        // Check again to allow half-open state
        monitor.check_now("test_component").await.unwrap();
        
        // Verify half-open state
        {
            let breaker = circuit_breaker.lock().unwrap();
            assert_eq!(breaker.state(), CircuitState::HalfOpen);
        }
        
        // Check again to close the circuit
        monitor.check_now("test_component").await.unwrap();
        
        // Verify closed state
        {
            let breaker = circuit_breaker.lock().unwrap();
            assert_eq!(breaker.state(), CircuitState::Closed);
        }
    }
}
```

### 6.3 Performance Tests

Performance tests will verify the Health Monitor's efficiency under load:

```rust
#[cfg(test)]
mod performance_tests {
    use super::*;
    
    #[tokio::test]
    #[ignore] // Run only during performance testing
    async fn test_health_monitor_high_component_count() {
        let monitor = HealthMonitor::new(Duration::from_secs(5), 10);
        
        // Register a large number of components
        const NUM_COMPONENTS: usize = 1000;
        
        let start = Instant::now();
        
        for i in 0..NUM_COMPONENTS {
            let component_id = format!("test_component_{}", i);
            monitor.register_check(&component_id, move || {
                HealthCheckResult {
                    component_id: component_id.clone(),
                    status: HealthStatus::Healthy,
                    message: "Test component is healthy".to_string(),
                    timestamp: Utc::now(),
                    metadata: HashMap::new(),
                    metrics: HashMap::new(),
                }
            }).unwrap();
        }
        
        let registration_time = start.elapsed();
        println!("Registered {} components in {:?}", NUM_COMPONENTS, registration_time);
        
        // Test parallel health checking
        let start = Instant::now();
        monitor.start().await.unwrap();
        
        // Wait for one complete cycle
        tokio::time::sleep(Duration::from_secs(6)).await;
        
        monitor.stop().await.unwrap();
        
        // Verify all components were checked
        let components = monitor.monitored_components();
        assert_eq!(components.len(), NUM_COMPONENTS);
        
        for i in 0..NUM_COMPONENTS {
            let component_id = format!("test_component_{}", i);
            assert!(monitor.get_status(&component_id).is_some());
        }
    }
    
    #[tokio::test]
    #[ignore] // Run only during performance testing
    async fn test_health_monitor_dependency_analysis() {
        let monitor = HealthMonitor::new(Duration::from_secs(5), 10);
        
        // Create a complex dependency graph
        const NUM_COMPONENTS: usize = 100;
        
        // Register components
        for i in 0..NUM_COMPONENTS {
            let component_id = format!("component_{}", i);
            monitor.register_check(&component_id, move || {
                HealthCheckResult {
                    component_id: component_id.clone(),
                    status: HealthStatus::Healthy,
                    message: "Test component is healthy".to_string(),
                    timestamp: Utc::now(),
                    metadata: HashMap::new(),
                    metrics: HashMap::new(),
                }
            }).unwrap();
        }
        
        // Register dependencies (each component depends on the previous 3)
        for i in 3..NUM_COMPONENTS {
            let component_id = format!("component_{}", i);
            for j in 1..=3 {
                let dependency = format!("component_{}", i - j);
                monitor.register_dependency(&component_id, &dependency).unwrap();
            }
        }
        
        // Test dependency analysis performance
        let start = Instant::now();
        let tree = monitor.dependency_tree();
        let analysis_time = start.elapsed();
        
        println!("Analyzed dependencies for {} components in {:?}", NUM_COMPONENTS, analysis_time);
        
        // Verify results
        assert_eq!(tree.len(), NUM_COMPONENTS);
        
        for i in 3..NUM_COMPONENTS {
            let component_id = format!("component_{}", i);
            let dependencies = tree.get(&component_id).unwrap();
            assert_eq!(dependencies.len(), 3);
        }
    }
}
```

### 6.4 Chaos Tests

Chaos testing will verify the Health Monitoring System's resilience to failures:

```rust
#[cfg(test)]
mod chaos_tests {
    use super::*;
    
    #[tokio::test]
    #[ignore] // Run only during chaos testing
    async fn test_health_monitor_with_failing_health_checks() {
        let monitor = HealthMonitor::new(Duration::from_secs(1), 100);
        
        // Register a check that occasionally panics
        monitor.register_check("flaky_component", || {
            if rand::random::<f64>() < 0.2 {
                panic!("Simulated health check failure");
            }
            
            HealthCheckResult {
                component_id: "flaky_component".to_string(),
                status: HealthStatus::Healthy,
                message: "Component is working".to_string(),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        }).unwrap();
        
        // Start monitoring
        monitor.start().await.unwrap();
        
        // Run for a while to trigger the panic
        for _ in 0..10 {
            tokio::time::sleep(Duration::from_secs(1)).await;
            
            // Check that the monitor is still running
            assert!(monitor.is_running());
            
            // Verify we can still get status (even if Unknown)
            let status = monitor.get_status("flaky_component");
            assert!(status.is_some());
        }
        
        // Stop monitoring
        monitor.stop().await.unwrap();
    }
    
    #[tokio::test]
    #[ignore] // Run only during chaos testing
    async fn test_health_monitor_with_slow_health_checks() {
        let monitor = HealthMonitor::new(Duration::from_secs(1), 100);
        
        // Register a check that's occasionally very slow
        monitor.register_check("slow_component", || {
            if rand::random::<f64>() < 0.3 {
                // Simulate a slow operation
                std::thread::sleep(Duration::from_secs(3));
            }
            
            HealthCheckResult {
                component_id: "slow_component".to_string(),
                status: HealthStatus::Healthy,
                message: "Component is working".to_string(),
                timestamp: Utc::now(),
                metadata: HashMap::new(),
                metrics: HashMap::new(),
            }
        }).unwrap();
        
        // Start monitoring
        monitor.start().await.unwrap();
        
        // Run for a while to trigger the slow checks
        for i in 0..5 {
            tokio::time::sleep(Duration::from_secs(1)).await;
            println!("Iteration {}: monitor still running", i);
        }
        
        // Verify the monitor didn't get stuck
        assert!(monitor.is_running());
        
        // Stop monitoring
        monitor.stop().await.unwrap();
    }
}
```

## 7. Implementation Plan

The Health Monitoring System will be implemented in the following phases:

### 7.1 Phase 1: Core Framework (Week 1-2)

1. Implement basic HealthCheckResult and HealthStatus types
2. Implement HealthMonitor with basic check registration and execution
3. Implement health history management
4. Create simple threshold-based health detection
5. Write unit tests for core functionality

### 7.2 Phase 2: Integration Framework (Week 3-4)

1. Implement dependency graph management
2. Develop circuit breaker integration
3. Implement recovery manager integration
4. Create metrics collector integration
5. Write integration tests

### 7.3 Phase 3: Advanced Algorithms (Week 5-6)

1. Implement statistical anomaly detection
2. Develop trend analysis algorithms
3. Create health prediction capabilities
4. Implement correlation analysis for root cause determination
5. Write performance tests

### 7.4 Phase 4: HMS-Specific Implementations (Week 7-8)

1. Implement agent health checks
2. Develop API service health checks
3. Create database health checks
4. Implement resource usage health checks
5. Write chaos tests

### 7.5 Phase 5: Integration and Optimization (Week 9-10)

1. Integrate with the entire HMS self-healing system
2. Optimize performance for high-volume health checking
3. Implement visualization and reporting tools
4. Conduct end-to-end testing
5. Document API and usage examples

## 8. Conclusion

The Health Monitoring System is a critical component of the HMS self-healing architecture. It provides comprehensive monitoring, detection, and notification capabilities that enable other components such as the Recovery Manager and Adaptive Configuration system to maintain system health and performance. The implementation plan outlined above will ensure a robust, scalable, and fully integrated Health Monitoring System that meets the needs of the HMS ecosystem.