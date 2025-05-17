# HMS Status System Integration Guide

This document provides guidance on integrating with the HMS Status System in Rust and TypeScript environments.

## Overview

The HMS Status System is a comprehensive monitoring and tracking solution that allows components to:

1. Record their operational status
2. Report issues and create work tickets
3. Track test results and component startup
4. Analyze repository health
5. Monitor environment resources

The system provides integrations for both Rust-based and TypeScript-based components through:

- Rust library API in the codex-rs workspace
- TypeScript API in the codex-cli
- Command-line interface
- Visual components for terminal UI

## Rust Integration (codex-rs)

### Basic Usage

To use the Status System in a Rust component:

```rust
use status_system::{StatusTracker, StatusValue, Severity};

fn main() -> anyhow::Result<()> {
    // Create a status tracker
    let tracker = StatusTracker::new()?;
    
    // Set component status
    tracker.set_status(
        "my-component",
        StatusValue::Healthy,
        "Component is operating normally",
    )?;
    
    // Record an issue
    tracker.record_issue(
        "my-component",
        "Connection timeout",
        "The component is experiencing timeouts when connecting to the database",
        Severity::High,
    )?;
    
    // Record test results
    let test_results = serde_json::json!({
        "passed": 95,
        "failed": 2,
        "skipped": 3,
        "coverage": 0.87
    });
    
    let result_map = if let serde_json::Value::Object(map) = test_results {
        map
    } else {
        serde_json::Map::new()
    };
    
    tracker.record_test("my-component", true, result_map)?;
    
    // Record component start
    tracker.record_start(
        "my-component",
        true,
        "development",
        "1.2.3",
    )?;
    
    Ok(())
}
```

### Using the Plugin System

For components that need to publish status events or integrate with the broader system:

```rust
use status_system::integration::core::{StatusSystemPlugin, StatusEvent};
use std::sync::Arc;

fn main() -> anyhow::Result<()> {
    // Create the status system plugin
    let plugin = StatusSystemPlugin::new()?;
    
    // Register for status events
    plugin.register_event_listener(|event| {
        match event {
            StatusEvent::ComponentStatusChanged(notification) => {
                println!("Component {} status changed to {}: {}",
                    notification.component,
                    notification.status,
                    notification.message,
                );
            },
            StatusEvent::IssueDetected(issue) => {
                println!("Issue detected in {}: {} ({})",
                    issue.component,
                    issue.title,
                    issue.severity,
                );
            },
            _ => {},
        }
    });
    
    // Use the plugin
    plugin.set_status(
        "my-component",
        StatusValue::Healthy,
        "Component is operating normally",
    )?;
    
    // Access underlying components if needed
    let tracker = plugin.tracker();
    let analyzer = plugin.analyzer();
    let monitor = plugin.monitor();
    
    Ok(())
}
```

### Boot Sequence Integration

For components that participate in the boot sequence:

```rust
use status_system::integration::core::BootSequenceStatusPlugin;

fn main() -> anyhow::Result<()> {
    // Create boot sequence status plugin
    let mut boot_plugin = BootSequenceStatusPlugin::new()?;
    
    // Record components starting
    boot_plugin.record_start("component1", true, "dev", "1.0.0")?;
    boot_plugin.record_start("component2", true, "dev", "1.0.0")?;
    
    // Check if all are healthy
    if !boot_plugin.all_components_healthy() {
        let unhealthy = boot_plugin.unhealthy_components();
        eprintln!("Boot sequence failed. Unhealthy components: {:?}", unhealthy);
        // Handle boot failure
    }
    
    Ok(())
}
```

### Repository Analysis

For working with repository health metrics:

```rust
use status_system::analyzer::RepositoryAnalyzer;

fn main() -> anyhow::Result<()> {
    // Create repository analyzer
    let analyzer = RepositoryAnalyzer::new(None)?;
    
    // Analyze a specific repository
    let analysis = analyzer.analyze_repository("my-repo", None)?;
    
    println!("Repository status: {}", analysis.overall_status);
    println!("Git status: {}", analysis.git_status.status);
    println!("Test status: {}", analysis.test_status.status);
    
    // Print issues if any
    if !analysis.issues.is_empty() {
        println!("Issues:");
        for issue in &analysis.issues {
            println!("- [{}] {}", issue.component, issue.description);
        }
    }
    
    // Generate a system-wide summary
    let summary = analyzer.generate_summary()?;
    
    println!("Total repositories: {}", summary.repository_count);
    println!("Healthy: {}", summary.healthy_count);
    println!("Degraded: {}", summary.degraded_count);
    println!("Unhealthy: {}", summary.unhealthy_count);
    
    Ok(())
}
```

### Environment Monitoring

For monitoring system resources:

```rust
use status_system::monitor::EnvironmentMonitor;

fn main() -> anyhow::Result<()> {
    // Create environment monitor
    let monitor = EnvironmentMonitor::new()?;
    
    // Check environment for a component
    let env_data = monitor.check_environment("my-component")?;
    
    // Print system information
    println!("Platform: {}", env_data.system.platform);
    println!("Architecture: {}", env_data.system.architecture);
    
    // Print resource usage
    println!("CPU usage: {:.2}%", env_data.resources.cpu_usage);
    println!("Memory usage: {:.2}%", env_data.resources.memory_usage_percent);
    println!("Disk usage: {:.2}%", env_data.resources.disk_usage_percent);
    
    // Print health status
    println!("Health status: {}", env_data.health.status);
    
    // Print issues if any
    if !env_data.health.issues.is_empty() {
        println!("Issues:");
        for issue in &env_data.health.issues {
            println!("- {}", issue);
        }
    }
    
    Ok(())
}
```

## TypeScript Integration (codex-cli)

### Basic Usage

To use the Status System in a TypeScript component:

```typescript
import { statusSystem, StatusValue, Severity } from './utils/status-system';

async function main() {
    try {
        // Set component status
        await statusSystem.setStatus(
            'my-component',
            StatusValue.Healthy,
            'Component is operating normally',
        );
        
        // Get component status
        const status = await statusSystem.getStatus('my-component');
        console.log(`Status: ${status.status}`);
        
        // Record an issue
        await statusSystem.recordIssue(
            'my-component',
            'Connection timeout',
            'The component is experiencing timeouts when connecting to the database',
            Severity.High,
        );
        
        // Record test results
        await statusSystem.recordTest(
            'my-component',
            true,
            {
                passed: 95,
                failed: 2,
                skipped: 3,
                coverage: 0.87
            }
        );
        
        // Record component start
        await statusSystem.recordStart(
            'my-component',
            true,
            'development',
            '1.2.3',
        );
    } catch (error) {
        console.error('Status system error:', error);
    }
}

main();
```

### React Components

The Status System provides React components for the terminal UI:

```typescript
import { Box } from 'ink';
import React from 'react';
import { 
    StatusReport,
    RepositoryAnalysisReport,
    SystemSummaryReport,
    EnvironmentReport
} from './utils/status-system/commands';

function StatusDashboard() {
    return (
        <Box flexDirection="column">
            <Box marginBottom={1}>
                <Box width="50%">
                    <StatusReport component="component1" />
                </Box>
                <Box width="50%">
                    <StatusReport component="component2" />
                </Box>
            </Box>
            
            <Box marginBottom={1}>
                <RepositoryAnalysisReport repository="my-repo" />
            </Box>
            
            <Box marginBottom={1}>
                <EnvironmentReport component="component1" />
            </Box>
            
            <Box>
                <SystemSummaryReport />
            </Box>
        </Box>
    );
}
```

## Command-Line Interface

The Status System provides a command-line interface for manual interaction:

```bash
# Get component status
status get my-component

# Set component status
status set my-component HEALTHY "Component is operating normally"

# Record test results
status test my-component --success --results '{"passed":95,"failed":2,"skipped":3,"coverage":0.87}'

# Record an issue
status issue my-component --title "Connection timeout" \
    --description "The component is experiencing timeouts when connecting to the database" \
    --severity high

# Record component start
status start my-component --success --env development --version 1.2.3

# List all components
status list

# Get status of all components
status all

# Get issues
status issues --component my-component

# Create work ticket from issue
status ticket <issue-id> --assigned-to jdoe --priority high

# Analyze repository
status analyze my-repo

# Generate repository summary
status summary

# Check environment
status check my-component
```

## Data Model

### Component Status

```typescript
interface Status {
    component: string;
    status: "HEALTHY" | "DEGRADED" | "UNHEALTHY" | "UNKNOWN";
    message: string;
    last_update: string;
    history?: Array<{
        status: string;
        message: string;
        timestamp: string;
    }>;
}
```

### Issue

```typescript
interface Issue {
    id: string;
    component: string;
    title: string;
    description: string;
    severity: "critical" | "high" | "medium" | "low";
    status: "open" | "assigned" | "in_progress" | "resolved" | "closed";
    created: string;
    updated: string;
    ticket_id?: string;
}
```

### Work Ticket

```typescript
interface WorkTicket {
    id: string;
    issue_id: string;
    component: string;
    title: string;
    description: string;
    assigned_to: string;
    priority: "high" | "medium" | "low";
    status: string;
    created: string;
    updated: string;
}
```

### Repository Analysis

```typescript
interface RepositoryAnalysis {
    repository: string;
    timestamp: string;
    path: string;
    overall_status: string;
    git_status: {
        status: string;
        exists: boolean;
        is_git_repo: boolean;
        branch?: string;
        latest_commit?: string;
        has_uncommitted_changes?: boolean;
        issues: string[];
    };
    test_status: {
        status: string;
        has_tests: boolean;
        last_run?: string;
        age_days?: number;
        passed?: number;
        failed?: number;
        skipped?: number;
        total?: number;
        pass_rate?: number;
        coverage?: number;
        issues: string[];
    };
    // Additional status fields omitted for brevity
    issues: Array<{
        component: string;
        description: string;
    }>;
}
```

### Environment Data

```typescript
interface EnvironmentData {
    component: string;
    timestamp: string;
    system: {
        platform: string;
        platform_version: string;
        platform_release: string;
        processor: string;
        architecture: string;
        hostname: string;
    };
    resources: {
        cpu_count: number;
        cpu_usage: number;
        memory_total: number;
        memory_available: number;
        memory_usage_percent: number;
        disk_total: number;
        disk_free: number;
        disk_usage_percent: number;
    };
    component_info: {
        found: boolean;
        status: string;
        start_found: boolean;
        version: string;
        environment: string;
        last_start?: string;
    };
    health: {
        status: string;
        issues: string[];
    };
}
```

## Best Practices

1. **Regular Status Updates**: Components should update their status regularly, especially during significant operations.

2. **Meaningful Messages**: Status messages should be descriptive and provide context about the current state.

3. **Appropriate Severity Levels**: Use appropriate severity levels for issues:
   - **Critical**: Issues that prevent core functionality and require immediate attention
   - **High**: Significant issues affecting functionality but not completely blocking
   - **Medium**: Issues that degrade performance or affect non-critical features
   - **Low**: Minor issues or suggestions for improvement

4. **Automated Analysis**: Set up automated repository analysis in CI/CD pipelines to keep track of repository health.

5. **Environment Monitoring**: Regularly monitor environment health to detect resource issues early.

6. **Boot Sequence Integration**: Integrate with the boot sequence to ensure all components start correctly.

7. **Issue Resolution Workflow**: Follow the issue resolution workflow:
   - Record issues
   - Create work tickets
   - Assign to developers
   - Track progress
   - Resolve issues
   - Close tickets

## Troubleshooting

### Common Issues

1. **Status Files Not Found**: Ensure that data directories exist and have appropriate permissions.

2. **FFI Integration Issues**: Make sure the Rust library is properly built and available to TypeScript.

3. **Repository Analysis Failures**: Ensure git is available and repositories are properly configured.

4. **Environment Monitoring Errors**: Check that the component has permissions to access system resources.

### Diagnostic Procedures

1. Check status files in the `data/status` directory.
2. Verify that test result files are correctly formatted in `data/test-results`.
3. Look for issue and work ticket files in `data/issues` and `data/work-tickets`.
4. Examine repository analysis results in `data/analysis`.
5. Check environment data in `data/environments`.

## Conclusion

The HMS Status System provides a robust framework for monitoring and tracking component health across the HMS ecosystem. By following this integration guide, components can take advantage of the status tracking, issue management, repository analysis, and environment monitoring capabilities of the system.