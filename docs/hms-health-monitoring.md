# HMS Health Monitoring System

This document provides information about the health monitoring capabilities in the HMS status system, including the tmux-based health dashboard.

## Overview

The health monitoring system provides real-time visibility into:

1. Component health status across the HMS ecosystem
2. System resource utilization
3. Repository status and analysis
4. Environment health indicators
5. Active alerts and issues

The system is designed to be lightweight, user-friendly, and integrates with both the Rust-based CLI and the TypeScript-based codex-cli tools.

## Dashboard Types

### Basic Health Dashboard

A focused view of component health and basic system metrics. This dashboard provides:

- Component status indicators (HEALTHY, DEGRADED, UNHEALTHY)
- Basic system resource monitoring (CPU, memory, disk)
- Critical alerts for component status changes
- Summary view of overall system health

### Detailed Health Dashboard

An extended view with comprehensive monitoring capabilities, including:

- Everything in the basic dashboard
- Per-process resource utilization
- Disk space monitoring by partition
- Detailed git status for repositories
- Component-specific metrics
- Historical status trends
- Active issue tracking

## Using the Health Dashboard

### CLI Command

```bash
# Launch basic health dashboard
status health-dashboard

# Launch detailed health dashboard
status health-dashboard --detailed

# Launch with notification command
status health-dashboard --notify-command "notify-send 'HMS Alert'"

# Launch and attach to the session
status health-dashboard --attach
```

### From Codex CLI

```typescript
// Using the StatusSystem class
import { statusSystem } from './utils/status-system';

// Launch a health dashboard
await statusSystem.launchHealthDashboard({
  detailed: true,    // For detailed dashboard
  attach: true,      // To attach to the session
  notifyCommand: 'notify-send "HMS Alert" "$COMPONENT is $STATUS"'
});

// Or use the helper component
import { createHealthDashboard } from './utils/status-system/commands';
createHealthDashboard();
```

## Dashboard Windows and Panes

The health dashboard creates a tmux session with multiple windows:

1. **Health Window**
   - Component status indicators
   - Overall system health
   - Alert summary

2. **Resources Window**
   - CPU usage (htop)
   - Memory consumption
   - Disk space
   - Top processes by resource usage

3. **Component Health Window**
   - Detailed status for each component
   - Health history
   - Active issues
   - Resource consumption by component

## Notifications

The health monitoring system supports multiple notification methods:

- Terminal bell alerts
- Desktop notifications (using notify-send or terminal-notifier)
- Custom command execution on alerts
- Visual indicators within the dashboard

## Integration with Existing Tools

The health dashboard seamlessly integrates with:

- codex-cli environment
- HMS component visualization tools
- Repository analysis system
- Environment monitoring
- Status tracking

## Requirements

- tmux (version 2.8 or higher)
- bash
- htop (for detailed system monitoring)
- jq (for JSON parsing)
- notify-send/terminal-notifier (optional, for desktop notifications)

## Customization

To customize the health dashboard, you can modify the following configuration files:

- `logs/health/monitor_script.sh` - Generated component health monitor script
- `logs/health/notify.sh` - Generated notification script

You can also extend the dashboard by adding your own tmux windows and panes.