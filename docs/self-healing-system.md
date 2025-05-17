# Advanced Self-Healing System for Economic Theorem Proving

This document describes the advanced self-healing system implemented for the Economic Theorem Proving platform, which uses genetic algorithms to optimize recovery strategies and automatically heal detected issues.

## Overview

The self-healing system provides robust automatic recovery capabilities for the Economic Theorem Prover with Genetic Agents. It combines sophisticated anomaly detection, intelligent recovery strategy selection, and genetic algorithm optimization to create an adaptive system that improves over time.

Key features:

- **Proactive anomaly detection** across metrics, logs, and component behavior patterns
- **Graduated recovery strategies** that minimize disruption
- **Genetic algorithm optimization** for complex recovery scenarios
- **Learning from past recoveries** to improve future healing attempts
- **Configurable operation modes** from fully automatic to supervised with approval
- **Real-time monitoring and dashboard** for system health visualization

## Architecture

The self-healing system consists of the following components:

1. **Anomaly Detection System**
   - Time-series anomaly detection for metrics
   - Pattern recognition for error logs
   - Behavioral anomaly detection for component interactions
   - Statistical outlier detection

2. **Recovery Strategy Framework**
   - Graduated recovery strategies of increasing invasiveness
   - Restart component strategy
   - Circuit breaker pattern implementation
   - Configuration optimization
   - Genetic algorithm-based recovery

3. **Self-Healing Coordinator**
   - Central orchestration of detection and recovery
   - Recovery queue management
   - Approval workflow for critical issues
   - Notification system

4. **Integration Layer**
   - Integration with existing monitoring systems
   - Configuration management
   - Lifecycle management
   - Dashboard integration

## Component Details

### Anomaly Detection System

The anomaly detection system uses multiple detection methods to identify issues before they cause system failures:

#### Time Series Anomaly Detection

Identifies abnormal patterns in metric data using:
- Isolation Forest for statistical outlier detection
- Z-score analysis for severity determination
- Adaptive thresholds based on historical patterns

```python
# Example of detecting an anomaly in a metric
detector = TimeSeriesAnomalyDetector()
anomalies = detector.detect_anomalies()
for anomaly in anomalies:
    print(f"Detected anomaly in {anomaly['metric_name']}: {anomaly['value']}")
```

#### Log Anomaly Detection

Analyzes log files to detect error patterns:
- Regex pattern matching for known error signatures
- Severity classification based on message content
- Temporal correlation of related log events

#### Behavioral Anomaly Detection

Monitors component interactions to detect relationship changes:
- Component profile creation and tracking
- Correlation analysis between related components
- Detection of significant behavior changes

### Recovery Strategy Framework

The recovery strategy framework provides multiple strategies with increasing levels of invasiveness:

#### Restart Component Strategy

The simplest strategy that restarts failing components:
- Targeted component restarts based on health checks
- Frequency limiting to prevent restart storms
- Validation of successful recovery

#### Circuit Breaker Strategy

Implements the circuit breaker pattern to prevent cascading failures:
- Automatic isolation of failing components or connections
- Graduated circuit states (closed, open, half-open)
- Automatic recovery testing and circuit closing

#### Reconfiguration Strategy

Adjusts configuration parameters to recover from issues:
- Rule-based parameter selection
- Learning from successful configurations
- Progressive parameter adjustments

#### Genetic Recovery Strategy

Uses genetic algorithms to evolve optimal recovery parameters:
- Population-based parameter optimization
- Fitness evaluation based on recovery success
- Multi-generation learning for complex issues

```python
# Example of applying a recovery strategy
recovery_manager = RecoveryStrategyManager.get_instance()
result = recovery_manager.apply_recovery(issue, context)
if result['success']:
    print(f"Recovery successful using {result['strategy']}")
else:
    print(f"Recovery failed: {result.get('error')}")
```

### Self-Healing Coordinator

The coordinator orchestrates the entire self-healing process:

#### Recovery Workflow

1. Anomalies are detected by the anomaly detection system
2. Anomalies are converted to issues with context
3. Recovery priority is determined based on severity
4. Appropriate recovery strategies are selected
5. Recovery is executed (with approval if needed)
6. Results are validated and recorded

#### Operation Modes

The system supports four operating modes:

- **Manual**: All recovery actions require explicit approval
- **Supervised**: Low/medium severity issues are auto-healed, high/critical require approval
- **Automated**: All recovery actions are performed automatically
- **Learning**: No actual recovery is performed, but decisions are recorded for analysis

#### Approval Workflow

For issues requiring approval:
1. A notification is sent with issue details and approval ID
2. Operators can approve or reject the proposed recovery
3. If approved, recovery proceeds automatically
4. Results are reported back to operators

### Integration Layer

The integration layer connects the self-healing system with the main application:

#### Configuration Management

Provides a flexible configuration system:
- File-based configuration
- Dynamic configuration updates
- Component-specific settings

#### Lifecycle Management

Manages the self-healing system lifecycle:
- Initialization and startup
- Graceful shutdown
- Signal handling

#### Dashboard Integration

Integrates with the metrics dashboard:
- Real-time anomaly visualization
- Recovery status tracking
- Historical recovery performance

## Usage Examples

### Initializing the Self-Healing System

```python
from src.python.self_healing.integrator import initialize_self_healing

# Initialize from config file
self_healing = initialize_self_healing('/path/to/config.json')

# Or initialize with explicit configuration
from src.python.self_healing.integrator import SelfHealingIntegrator

integrator = SelfHealingIntegrator.get_instance()
integrator.initialize({
    'enabled': True,
    'mode': 'supervised',
    'detection_interval': 30
})
integrator.start()
```

### Registering Custom Components

```python
# Register a custom anomaly detector
from src.python.self_healing.anomaly_detection import BaseAnomalyDetector, AnomalyDetectionManager

class CustomDetector(BaseAnomalyDetector):
    def __init__(self):
        super().__init__("custom_detector", ["custom.*"])
        
    def detect_anomalies(self):
        # Custom detection logic
        return anomalies

# Register with the manager
detector = CustomDetector()
manager = AnomalyDetectionManager.get_instance()
manager.register_detector(detector)
```

### Manual Recovery Approval

```python
# Approving a recovery action
from src.python.self_healing.coordinator import SelfHealingCoordinator

coordinator = SelfHealingCoordinator.get_instance()
coordinator.approve_recovery("approval_12345")

# Rejecting a recovery action
coordinator.reject_recovery("approval_12345", "Not the right time for this operation")
```

### Getting System Status

```python
# Get current status of the self-healing system
from src.python.self_healing.integrator import SelfHealingIntegrator

integrator = SelfHealingIntegrator.get_instance()
status = integrator.get_status()

print(f"Active: {status['active']}")
print(f"Mode: {status['mode']}")
print(f"Active recoveries: {status['active_recoveries']}")
print(f"Auto-healing rate: {status['auto_healing_rate']}%")
```

## Configuration Reference

The self-healing system is configured using a JSON configuration file with the following options:

| Option | Description | Default |
|--------|-------------|---------|
| `enabled` | Enable/disable the self-healing system | `true` |
| `mode` | Operating mode: `manual`, `supervised`, `automated`, `learning` | `supervised` |
| `detection_interval` | Interval between anomaly detection runs (seconds) | `30` |
| `max_concurrent_recoveries` | Maximum number of concurrent recovery actions | `3` |
| `quarantine_period` | Time to quarantine failed recoveries (seconds) | `600` |
| `dashboard_enabled` | Enable/disable the metrics dashboard | `true` |
| `dashboard_port` | Port for the metrics dashboard | `8080` |
| `notification_webhook` | URL for webhook notifications | `null` |
| `log_level` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |
| `metrics_history_days` | Days to retain metrics history | `7` |
| `component_restart_commands` | Mapping of component names to restart commands | `{}` |
| `custom_detectors` | List of custom detectors to load | `[]` |
| `custom_strategies` | List of custom strategies to load | `[]` |

Example configuration:

```json
{
  "enabled": true,
  "mode": "supervised",
  "detection_interval": 30,
  "max_concurrent_recoveries": 3,
  "dashboard_enabled": true,
  "dashboard_port": 8080,
  "log_level": "INFO",
  "component_restart_commands": {
    "proof_engine": "systemctl restart hms-proof-engine",
    "theorem_repository": "systemctl restart hms-theorem-repository"
  }
}
```

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│            HMS Components               │
│                                         │
│  ┌─────────┐  ┌────────┐  ┌──────────┐ │
│  │  Proof  │  │Theorem │  │ Genetic  │ │
│  │ Engine  │  │  Repo  │  │Optimizer │ │
│  └────┬────┘  └────┬───┘  └─────┬────┘ │
└───────┼─────────────┼─────────────┼────┘
         │             │             │
┌────────┼─────────────┼─────────────┼────┐
│        ▼             ▼             ▼    │
│   ┌─────────────────────────────────┐   │
│   │        Metrics Collection       │   │
│   └───────────────────┬─────────────┘   │
│                       │                 │
│                       ▼                 │
│   ┌─────────────────────────────────┐   │
│   │       Anomaly Detection         │   │ Self-Healing
│   └───────────────────┬─────────────┘   │ System
│                       │                 │
│                       ▼                 │
│   ┌─────────────────────────────────┐   │
│   │    Self-Healing Coordinator     │   │
│   └───────────────────┬─────────────┘   │
│                       │                 │
│                       ▼                 │
│   ┌─────────────────────────────────┐   │
│   │    Recovery Strategy Manager    │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## Best Practices

1. **Start in Supervised Mode**
   - Begin with `supervised` mode until confidence in the system is established
   - Gradually transition to `automated` mode for non-critical components

2. **Tune Detection Sensitivity**
   - Adjust anomaly detection sensitivity based on false positive/negative rates
   - Start with lower sensitivity and increase as confidence grows

3. **Define Component-Specific Strategies**
   - Create custom strategies tailored to specific components
   - Leverage domain knowledge for more effective recovery

4. **Monitor Recovery Performance**
   - Regularly review the auto-healing rate
   - Analyze failed recoveries to improve strategies

5. **Implement Circuit Breakers**
   - Use circuit breakers to prevent overloading dependencies
   - Configure appropriate thresholds and reset timeouts

## Integration with Genetic Optimization

The self-healing system integrates with the genetic agent framework to provide automated optimization of theorem proving strategies:

1. **Recovery Strategy Evolution**
   - The genetic recovery strategy evolves optimal parameters over time
   - Successful recoveries influence future genetic selection

2. **Theorem Proving Optimization**
   - Performance metrics from the theorem prover feed into the self-healing system
   - Self-healing interventions improve overall theorem proving efficiency

3. **Feedback Loop**
   - Recovery success feeds back into genetic algorithm fitness
   - System self-optimizes over time based on real-world performance

## Future Work

1. **Enhanced Predictive Capabilities**
   - Add machine learning models for predictive anomaly detection
   - Implement trend analysis to forecast potential issues

2. **Multi-System Coordination**
   - Coordinate self-healing across multiple instances
   - Implement leader election for distributed recovery decisions

3. **User Interface Improvements**
   - Develop a dedicated self-healing dashboard
   - Add visualization of recovery workflows

4. **Automated A/B Testing**
   - Test multiple recovery strategies in parallel
   - Automatically select the most effective strategies

## Conclusion

The advanced self-healing system provides a robust framework for automatic detection and recovery from issues in the Economic Theorem Proving platform. By leveraging genetic algorithms and sophisticated anomaly detection, the system continuously improves its recovery capabilities, leading to higher availability and reliability.