# HMS Monitoring System

This document outlines the HMS Monitoring System implementation, which provides real-time health monitoring, visualization, and knowledge registry capabilities for HMS components.

## System Components

The monitoring system consists of three main components:

1. **Basic Monitoring**: Core health tracking and metrics collection
2. **TMUX Integration**: Terminal-based visualization of component health status
3. **Knowledge Registry**: Storage and retrieval system for healing strategies

## Features

- **Component Health Tracking**: Monitor the health status of system components
- **Real-time Visualization**: View component status in TMUX terminal sessions
- **Status Change Alerts**: Get notified of component status changes
- **Strategy Storage**: Store, retrieve, and manage healing strategies
- **TTL-based Knowledge**: Time-to-live functionality for temporary knowledge items
- **Query System**: Find strategies based on multiple criteria

## Running Tests

To run all monitoring tests:

```bash
./scripts/run_all_monitoring_tests.sh
```

To run individual tests:

```bash
./scripts/test_monitoring.sh       # Basic monitoring test
./scripts/test_tmux_monitoring.sh  # TMUX visualization test
./scripts/test_knowledge_registry.sh # Knowledge registry test
```

### Test Features

#### 1. Basic Monitoring Test

- Component registration and status tracking
- Health monitoring based on metrics (CPU, memory, error rates)
- Status change detection
- Console visualization

#### 2. TMUX Integrated Monitoring Test

- TMUX session management
- Component health visualization in TMUX panes
- Real-time status updates
- Visual status change tracking

**Note**: This test requires TMUX to be installed on your system.

#### 3. Knowledge Registry Test

- Storage and retrieval of healing strategies
- Query capabilities with filtering
- Item expiration management
- Strategy metadata management
- TTL-based automatic cleanup

## Implementation Details

### Component Status Levels

The monitoring system defines five health status levels for components:

- **Healthy**: Component is functioning normally
- **Degraded**: Performance is suboptimal but functional
- **Warning**: Issues detected that require attention
- **Critical**: Severe issues that may cause imminent failure
- **Failed**: Component has stopped functioning

### Metrics Collection

The system collects and analyzes the following metrics:

- **CPU Usage**: Percentage of CPU utilization
- **Memory Usage**: Memory consumption in MB
- **Error Rate**: Percentage of operations resulting in errors
- **Response Time**: Time taken to respond to requests
- **Last Update**: Timestamp of the last heartbeat

### TMUX Visualization

The TMUX integration provides:

- Split-pane layout for status monitoring
- Color-coded status indicators (✅, ⚠️, 🔶, ❌, 💀)
- Real-time updates for component metrics
- Status change history

### Knowledge Registry

The knowledge registry stores:

- **Healing Strategies**: Actions to recover from failures
- **Component Configurations**: Settings for different components
- **System Policies**: Rules for system behavior

The registry supports:

- **Namespaces**: Organize knowledge by domain
- **Tags**: Categorize items for easy retrieval
- **TTL**: Set expiration for temporary knowledge
- **Query System**: Find items by multiple criteria

## Building from Source

To build the monitoring components:

```bash
# Build all monitoring components
./scripts/build_monitoring_components.sh

# Build specific examples
./scripts/build_monitoring_example.sh
```

## Integration with Other HMS Components

The monitoring system integrates with:

- **Self-Healing System**: Provides health status for recovery decisions
- **Supervisor**: Centralizes monitoring and control
- **HMS-A2A**: Enables agent-to-agent communication for distributed monitoring
- **HMS-CDF**: Supports component definition framework

## Architecture Diagram

```
┌───────────────────┐     ┌───────────────────┐
│  HMS Components   │◄────┤ Metrics Collector │
└────────┬──────────┘     └─────────▲─────────┘
         │                          │
         ▼                          │
┌────────────────────────────────────────────┐
│            Monitoring System               │
├────────────────────┬───────────────────────┤
│   Health Tracker   │   Status Evaluator    │
└────────┬───────────┴──────────┬────────────┘
         │                      │
         ▼                      ▼
┌────────────────┐     ┌────────────────────┐
│ TMUX Visualizer│     │ Knowledge Registry │
└────────────────┘     └────────────────────┘
```

## Future Enhancements

Planned improvements for the monitoring system:

1. **Web-based Dashboard**: Browser-based visualization alternative to TMUX
2. **Historical Data Analysis**: Track metrics over time for trend analysis
3. **Anomaly Detection**: Automatically identify unusual patterns
4. **Predictive Health Monitoring**: Anticipate failures before they occur
5. **Distributed Monitoring**: Scale to monitor thousands of components
6. **Custom Visualization Templates**: User-defined status displays
7. **Full Self-Healing Integration**: Complete the integration with the self-healing system

## Current Limitations

- TMUX integration requires a terminal environment
- Knowledge registry is currently in-memory only (no persistence)
- Limited to monitoring a single host
- No distributed consensus for large-scale deployments

## Documentation

For more detailed information, please refer to:

- [Monitoring Implementation Plan](docs/MONITORING_IMPLEMENTATION_PLAN.md): Detailed implementation plan for all components
- [Monitoring Implementation Summary](docs/MONITORING_IMPLEMENTATION_SUMMARY.md): Summary of implemented features and technical decisions
- [TMUX Supervisor Knowledge Implementation Plan](docs/TMUX_SUPERVISOR_KNOWLEDGE_IMPLEMENTATION_PLAN.md): Integration plan for the three main components
- [HMS Health Monitoring](docs/HMS-HEALTH-MONITORING.md): Overview of the health monitoring architecture
- [Terminal Interface Guide](docs/TERMINAL_INTERFACE_GUIDE.md): Guide for using the terminal-based monitoring interfaces

## Contributing

To enhance the monitoring system:

1. Write tests for new functionality
2. Ensure backward compatibility with existing components
3. Follow the HMS coding style guidelines
4. Update documentation with changes