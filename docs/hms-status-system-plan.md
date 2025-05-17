# HMS Status System Technical Plan

## Overview

The HMS Status System is a comprehensive monitoring, tracking, and documentation framework for the HMS ecosystem. It continuously tracks the operational status of all 33 HMS components, analyzes their code repositories, monitors their development environments, and updates documentation with current status information.

The system implements a self-healing approach to component health, automatically detecting issues and updating documentation to reflect the current state of each component. This ensures that developers and stakeholders always have accurate, up-to-date information about the status of any HMS component.

## System Architecture

The status system consists of five core components:

1. **Status Tracker** (`status_tracker.py`): Records operational events for HMS components, including component starts, test runs, and issues. Maintains a history of these events and calculates health metrics based on this data.

2. **Repository Analyzer** (`repository_analyzer.py`): Analyzes HMS component repositories for code quality metrics, structure, and potential issues. Generates structured summaries of repository health.

3. **Environment Monitor** (`environment_monitor.py`): Validates development environments for HMS components, checking for required tools, dependencies, and proper configuration. Attempts to fix issues when possible.

4. **Docs Integrator** (`docs_integrator.py`): Updates documentation for HMS components with current status information. Adds status badges to README files and creates comprehensive status summaries.

5. **System Runner** (`run_system.py`): Orchestrates the status system, coordinating the execution of the other components. Provides commands for full and quick updates, as well as continuous monitoring.

![HMS Status System Architecture](../images/hms_status_system_architecture.png)

## Data Model

The status system uses a consistent data model to store and track component status:

### Status Data

```json
{
  "component_id": "HMS-XYZ",
  "last_updated": "2025-05-04T15:30:00Z",
  "operational_status": "green|yellow|red|unknown",
  "health_metrics": {
    "uptime_percentage": 99.5,
    "test_pass_rate": 98.2,
    "issue_count": 3,
    "critical_issue_count": 0
  },
  "start_history": [
    {
      "timestamp": "2025-05-04T12:30:00Z",
      "success": true,
      "environment": "dev|staging|prod",
      "version": "1.2.3",
      "duration_ms": 1500
    }
  ],
  "test_history": [
    {
      "timestamp": "2025-05-04T13:45:00Z",
      "success": true,
      "results": {
        "passed": 42,
        "failed": 0,
        "skipped": 3
      },
      "duration_ms": 3500
    }
  ],
  "issues": [
    {
      "id": "WT-HMS-XYZ-001",
      "title": "Issue title",
      "severity": "low|medium|high|critical",
      "detected_at": "2025-05-03T10:15:00Z",
      "status": "open|assigned|resolved",
      "assigned_to": "username",
      "resolution": "Resolution description"
    }
  ],
  "environment_status": {
    "dev_environment": "not_configured|issues|ready",
    "dependencies_status": "unknown|missing|outdated|up_to_date",
    "configuration_status": "unknown|issues|valid"
  }
}
```

### Analysis Data

```json
{
  "component_id": "HMS-XYZ",
  "timestamp": "2025-05-04T15:30:00Z",
  "full_analysis": true,
  "structure": {
    "exists": true,
    "file_count": 153,
    "directory_count": 27,
    "file_types": {
      ".py": 48,
      ".md": 15,
      ".json": 8
    },
    "top_level_dirs": ["src", "tests", "docs"],
    "top_level_files": ["README.md", "setup.py", "requirements.txt"],
    "has_readme": true,
    "has_tests": true,
    "has_docs": true,
    "has_package_json": false,
    "has_docker": true
  },
  "git": {
    "has_git": true,
    "commit_count": 285,
    "contributors": [
      {"name": "Dev Name", "commits": 157}
    ],
    "last_commit": {
      "hash": "abcd123",
      "author": "Dev Name",
      "date": "Wed May 3 14:23:01 2025 -0700",
      "message": "Fix database connection issue"
    },
    "recent_commits": []
  },
  "dependencies": {
    "has_package_json": false,
    "has_requirements_txt": true,
    "has_cargo_toml": false,
    "has_gemfile": false,
    "dependency_count": 12,
    "dev_dependency_count": 5,
    "dependencies": [
      {"name": "requests", "version": "2.28.1"}
    ],
    "dev_dependencies": []
  },
  "issues": [
    {
      "type": "missing_tests",
      "severity": "high",
      "description": "Component is missing tests for key functionality"
    }
  ]
}
```

### Environment Data

```json
{
  "component_id": "HMS-XYZ",
  "last_checked": "2025-05-04T15:30:00Z",
  "dev_environment": "not_configured|issues|ready",
  "dependencies_status": "unknown|missing|outdated|up_to_date",
  "configuration_status": "unknown|issues|valid",
  "required_tools": ["python3", "docker"],
  "missing_tools": ["docker-compose"],
  "required_dependencies": ["requests==2.28.1"],
  "missing_dependencies": [],
  "configuration_issues": [
    {
      "issue": "missing_env_file",
      "message": ".env file is missing (but .env.example exists)"
    }
  ],
  "checks": [
    {
      "check": "python_version",
      "status": "success",
      "value": "3.9.5"
    }
  ]
}
```

## Implementation Details

### Status Calculation

The system calculates operational status for each component based on multiple factors:

- **Green (Operational)**: No critical issues, test pass rate over 95%, no open issues
- **Yellow (Minor Issues)**: No critical issues, test pass rate between 80-95%, or open non-critical issues
- **Red (Major Issues)**: Critical issues present, or test pass rate below 80%

### Directory Structure

The status system uses the following directory structure:

```
HMS_ROOT/
├── status-system/
│   ├── status_tracker.py
│   ├── repository_analyzer.py
│   ├── environment_monitor.py
│   ├── docs_integrator.py
│   └── run_system.py
├── data/
│   ├── status/
│   ├── analysis/
│   ├── environments/
│   ├── issues/
│   ├── work-tickets/
│   ├── test-results/
│   └── summaries/
└── SYSTEM-COMPONENTS/
    ├── HMS-A2A/
    │   ├── HMS-docs/
    │   │   ├── codex.md
    │   │   └── STATUS.md
    │   └── README.md
    └── ...
```

### Self-Healing Capabilities

The status system implements several self-healing capabilities:

1. **Automatic Documentation Updates**: When status changes, documentation is automatically updated to reflect the current state.

2. **Test Failure Ticket Generation**: When tests fail, work tickets are automatically created to track the issues.

3. **Environment Issue Resolution**: The environment monitor can attempt to fix common environment issues.

4. **Status Badge Updates**: README badges are automatically updated to show current component status.

## Integration with HMS Components

The status system integrates with HMS components in multiple ways:

### Documentation Integration

The system adds status information to component documentation:

1. **README Badges**: Status badges show operational status at a glance.

2. **Codex.md Status Section**: A detailed status section is added to each component's codex.md file.

3. **STATUS.md**: A comprehensive status summary file is created in each component's HMS-docs directory.

### Work Ticket Integration

When issues are detected, the system creates work tickets:

1. **Test Failures**: Automatically creates tickets for failing tests.

2. **Configuration Issues**: Tracks environment configuration issues.

3. **Issue Resolution**: Records issue resolutions for historical tracking.

## Usage

### Command Line Interface

The status system provides a comprehensive CLI for interacting with the system:

#### Status Tracker

```bash
# Record a component start
python3 status_tracker.py start HMS-API --success --env dev --version 1.2.3

# Record a test run
python3 status_tracker.py test HMS-API --success --results '{"passed": 42, "failed": 0, "skipped": 3}'

# Record an issue
python3 status_tracker.py issue HMS-API --title "Database connection timeout" --severity medium

# Resolve an issue
python3 status_tracker.py resolve WT-HMS-API-001 --resolution "Increased database connection timeout"

# Get component status
python3 status_tracker.py get HMS-API
```

#### Repository Analyzer

```bash
# Analyze a specific component
python3 repository_analyzer.py analyze HMS-API

# Analyze a component with full analysis
python3 repository_analyzer.py analyze HMS-API --full

# Analyze all components
python3 repository_analyzer.py all
```

#### Environment Monitor

```bash
# Check a component's environment
python3 environment_monitor.py check HMS-API

# Check and attempt to fix environment issues
python3 environment_monitor.py check HMS-API --fix

# Check all environments
python3 environment_monitor.py all
```

#### Docs Integrator

```bash
# Update component documentation
python3 docs_integrator.py update HMS-API

# Add a status badge to README.md
python3 docs_integrator.py badge HMS-API --add

# Create a status summary
python3 docs_integrator.py summary HMS-API

# Update documentation for all components
python3 docs_integrator.py all
```

#### System Runner

```bash
# Run a full system update for all components
python3 run_system.py full-update

# Run a quick update for a specific component
python3 run_system.py quick-update --component HMS-API

# Start continuous monitoring
python3 run_system.py monitor --interval 3600
```

### Setup and Initialization

The `setup_status_system.sh` script initializes the status system:

```bash
# Create required directories
mkdir -p data/status
mkdir -p data/analysis
mkdir -p data/environments
mkdir -p data/issues
mkdir -p data/work-tickets
mkdir -p data/test-results
mkdir -p data/summaries

# Make scripts executable
chmod +x status-system/status_tracker.py
chmod +x status-system/repository_analyzer.py
chmod +x status-system/environment_monitor.py
chmod +x status-system/docs_integrator.py
chmod +x status-system/run_system.py

# Run initial status update
python3 status-system/run_system.py quick-update
```

## Future Enhancements

The following enhancements are planned for future iterations:

1. **Web Dashboard**: A web-based dashboard for visualizing status across all components.

2. **Notification System**: Alerts for critical status changes via email, Slack, etc.

3. **Historical Analytics**: Advanced analytics on long-term component health trends.

4. **Integration with CI/CD**: Automatic status updates from CI/CD pipelines.

5. **Component Dependency Tracking**: Track relationships between components for impact analysis.

6. **Automated Testing**: Add more automated tests for self-healing capabilities.

7. **AI-Powered Issue Resolution**: Use AI to suggest or automatically implement issue resolutions.

## Conclusion

The HMS Status System provides a comprehensive solution for monitoring and maintaining the health of all HMS components. By automating status tracking, environment validation, and documentation updates, it ensures that all stakeholders have accurate, up-to-date information about component health while reducing manual maintenance efforts.

This technical plan serves as a guide for understanding, using, and extending the HMS Status System.