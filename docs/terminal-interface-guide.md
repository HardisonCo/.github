# MAC Terminal Interface Guide

This document provides comprehensive documentation for the MAC Terminal Interface system, which enables human-in-the-loop interaction with the MAC (Multi-Agent Coordination) architecture through a terminal-based interface.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Core Components](#core-components)
- [Terminal Modes](#terminal-modes)
- [Session Management](#session-management)
- [Configuration System](#configuration-system)
- [Command-Line Interface](#command-line-interface)
- [API Usage](#api-usage)
- [TMUX Integration](#tmux-integration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

The MAC Terminal Interface provides a unified system for human-agent interaction through the terminal, with optional TMUX integration for advanced multi-agent visualization and collaboration. Key features include:

- Multiple terminal interaction modes for different use cases
- TMUX integration for multi-pane agent visualization
- Session management for persistence and history
- Configuration system with layered settings
- Human-in-the-loop feedback mechanisms
- Command-line interface for session management
- Comprehensive Python API for integration with other systems

## Installation

### Prerequisites

- Python 3.7 or higher
- TMUX (optional, for multi-pane visualization)
- PyYAML and TOML (for configuration management)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/hardisonco/hms.git
   cd HardisonCo
   ```

2. Install the package:
   ```bash
   cd core/mac/human_interface
   pip install -e .
   ```

3. Verify installation:
   ```bash
   mac-terminal --help
   ```

4. Create default configuration (optional):
   ```bash
   python -c "from mac.human_interface import create_default_user_config; create_default_user_config()"
   ```

## Core Components

The MAC Terminal Interface consists of several core components:

### TerminalInterface

The main interface class that handles terminal interactions, TMUX integration, and human-in-the-loop feedback.

### SessionManager

Manages terminal sessions, providing persistence and history tracking.

### ConfigManager

Handles configuration loading, merging, and validation from multiple sources.

### CLI

Command-line interface for session management and terminal operations.

## Terminal Modes

The terminal interface supports four primary modes of operation:

### Observe Mode

Passive observation mode for monitoring agent activity without direct interaction.

```bash
mac-terminal create --mode observe
```

### Prepare Mode

Preparation mode for designing and planning agent workflows.

```bash
mac-terminal create --mode prepare
```

### Watch Mode

Active monitoring mode with status panels and alert notifications.

```bash
mac-terminal create --mode watch
```

### Collaborate Mode

Full multi-agent collaboration mode with specialized agent panes.

```bash
mac-terminal create --mode collaborate --tmux
```

## Session Management

The terminal interface provides session management capabilities for maintaining state across multiple sessions.

### Creating a Session

```bash
mac-terminal create --name "My Session" --mode collaborate
```

### Listing Sessions

```bash
# List all sessions
mac-terminal list

# List only active sessions
mac-terminal list --active-only

# Show detailed session information
mac-terminal list --verbose
```

### Getting Session Information

```bash
mac-terminal info SESSION_ID
```

### Attaching to a Session

```bash
mac-terminal attach SESSION_ID
```

### Session Lifecycle Management

```bash
# Pause a session
mac-terminal pause SESSION_ID

# Resume a session
mac-terminal resume SESSION_ID

# Complete a session
mac-terminal complete SESSION_ID

# Delete a session
mac-terminal delete SESSION_ID
```

### Session Cleanup

```bash
# Clean up completed sessions older than 30 days
mac-terminal cleanup --days 30
```

## Configuration System

The terminal interface uses a layered configuration system:

1. Default configuration (built-in)
2. System-wide configuration (`/etc/mac/config.json`, `/etc/mac/config.toml`, etc.)
3. User configuration (`~/.mac/config.json`, `~/.config/mac/config.json`, etc.)
4. Explicitly provided configuration

### Configuration Format

Configuration files can be in JSON, TOML, or YAML format:

```json
{
  "terminal": {
    "default_mode": "collaborate",
    "auto_approve_timeout": 30.0,
    "color_enabled": true
  },
  "tmux": {
    "enabled": true,
    "default_layout": "main-horizontal",
    "status_line": "#[fg=green]MAC #[fg=yellow]Mode:#[fg=white] {:mode}"
  },
  "session": {
    "dir": "~/.mac/sessions",
    "auto_save": true,
    "save_interval": 60
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": null
  },
  "agents": {
    "supervisor": {
      "enabled": true,
      "pane_title": "Supervisor",
      "pane_color": "bg=colour52"
    },
    "coordinator": {
      "enabled": true,
      "pane_title": "Coordinator",
      "pane_color": "bg=colour17"
    }
  }
}
```

### Creating Default Configuration

```python
from mac.human_interface import create_default_user_config
create_default_user_config()
```

### Loading Configuration

```python
from mac.human_interface import load_config, get_config

# Load configuration
config = load_config()

# Get specific configuration value
timeout = get_config("terminal.auto_approve_timeout", 30.0)
```

## Command-Line Interface

The MAC Terminal Interface includes a command-line interface for session management and terminal operations.

### Command Overview

```
usage: mac-terminal [-h] [--debug]
                     {create,list,attach,resume,pause,complete,delete,info,stats,cleanup}
                     ...

MAC Terminal Interface CLI

options:
  -h, --help            show this help message and exit
  --debug               Enable debug logging

commands:
  {create,list,attach,resume,pause,complete,delete,info,stats,cleanup}
    create              Create a new terminal session
    list                List terminal sessions
    attach              Attach to a terminal session
    resume              Resume a paused terminal session
    pause               Pause an active terminal session
    complete            Mark a terminal session as completed
    delete              Delete a terminal session
    info                Get information about a terminal session
    stats               Get statistics about terminal sessions
    cleanup             Clean up old terminal sessions
```

### Example Usage

```bash
# Create a new session with TMUX
mac-terminal create --name "My Collaborative Session" --mode collaborate --tmux

# List active sessions
mac-terminal list --active-only

# Get session statistics
mac-terminal stats

# Get information about a session
mac-terminal info SESSION_ID

# Attach to a session
mac-terminal attach SESSION_ID

# Delete a session
mac-terminal delete SESSION_ID --force
```

## API Usage

### Creating a Terminal Interface

```python
from mac.human_interface import (
    create_terminal_interface,
    TerminalMode
)

# Create a terminal interface
terminal = create_terminal_interface(
    mode="collaborate",
    tmux_enabled=True,
    auto_approve_timeout=30.0,
    config_path="~/.mac/config.json",
    session_name="My Session"
)

# Display a message
terminal.display_message(
    "Hello, world!",
    level="info",
    pane="Supervisor"  # Optional, for TMUX only
)

# Request user feedback
feedback = await terminal.request_feedback(
    query_type="decision",
    query_content={
        "title": "Resource Allocation",
        "message": "Approve the proposed allocation?",
        "options": ["Approve", "Reject", "Modify"]
    },
    timeout=60.0
)
```

### Working with Sessions

```python
from mac.human_interface import TerminalSessionManager

# Create a session manager
session_manager = TerminalSessionManager()

# List sessions
sessions = session_manager.list_sessions(active_only=True)

# Get a specific session
session = session_manager.get_session(session_id)

# Add entry to a session
session.add_entry(
    "event",
    {"message": "Something happened"},
    "system"
)

# Add a task to a session
session.add_task(
    "task_123",
    "Process Data",
    {"priority": "high", "deadline": "2023-09-30"}
)

# Update a task
session.update_task(
    "task_123",
    "completed",
    {"result": "success"}
)

# Complete a session
session.complete()
session_manager.update_session(session)
```

## TMUX Integration

The terminal interface provides deep integration with TMUX for multi-pane visualization and agent collaboration.

### Creating a TMUX Session

```python
from mac.human_interface import create_terminal_interface

terminal = create_terminal_interface(
    mode="collaborate",
    tmux_enabled=True
)

# Create TMUX session
terminal.create_tmux_session()

# Attach to TMUX session
terminal.attach_to_session()
```

### Customizing TMUX Layout

```python
from mac.human_interface import TerminalLayout

# Create terminal with custom layout
terminal = create_terminal_interface(
    mode="collaborate",
    tmux_enabled=True,
    config={
        "tmux": {
            "default_layout": TerminalLayout.MAIN_VERTICAL.value
        }
    }
)
```

### Working with TMUX Panes

```python
# Split a pane
terminal._split_pane(0, "-h")

# Set pane title
terminal._set_pane_title(1, "Coordinator")

# Send command to a pane
terminal._send_command(1, "echo 'Hello from Coordinator'")

# Set layout
terminal._set_layout(TerminalLayout.TILED)
```

## Examples

### Basic Terminal Demo

```bash
python examples/terminal_interface_demo.py --tmux
```

### Advanced Terminal Demo

```bash
python examples/advanced_terminal_demo.py --tmux --attach
```

### Multi-Agent Demo

```bash
python examples/mac_tmux_multi_agent_demo.py --tmux
```

## Troubleshooting

### TMUX Not Found

If you see an error like "tmux is not installed", ensure TMUX is installed on your system:

```bash
# Ubuntu/Debian
sudo apt-get install tmux

# macOS with Homebrew
brew install tmux
```

### Session Creation Fails

If session creation fails, check the permissions on the session directory:

```bash
# Create and set permissions on the session directory
mkdir -p ~/.mac/sessions
chmod 755 ~/.mac ~/.mac/sessions
```

### Configuration Issues

If you encounter configuration issues, try creating a default configuration:

```python
from mac.human_interface import create_default_user_config
create_default_user_config()
```

### Debugging

Enable debug logging for more detailed information:

```bash
mac-terminal --debug list
```

Or in Python:

```python
import logging
logging.getLogger("MAC.HumanInterface").setLevel(logging.DEBUG)
```

## Advanced Topics

### Custom Agent Integration

The terminal interface can be integrated with custom agents:

```python
class MyAgent:
    def __init__(self, name, terminal, pane=None):
        self.name = name
        self.terminal = terminal
        self.pane = pane
    
    async def start(self):
        self.terminal.display_message(
            f"{self.name} starting...",
            level="info",
            pane=self.pane
        )
        
        # Add agent to session if available
        if self.terminal.session:
            self.terminal.session.add_agent(
                f"agent_{id(self)}",
                self.name
            )
        
        return self
    
    async def process_task(self, task):
        self.terminal.display_message(
            f"Processing task: {task['name']}",
            level="info",
            pane=self.pane
        )
        
        # Process task...
        
        # Update session if available
        if self.terminal.session:
            self.terminal.session.update_task(
                task["id"],
                "completed",
                {"result": "success"}
            )
```

### Custom Terminal Layouts

You can create custom TMUX layouts for specialized agent configurations:

```python
def create_custom_layout(terminal):
    """Create a custom TMUX layout with specialized panes."""
    # Create base session
    terminal.create_tmux_session()
    
    # Add specialized panes
    terminal._split_pane(0, "-h")  # Split horizontally
    terminal._set_pane_title(1, "Agent1")
    
    terminal._split_pane(1, "-v")  # Split vertically
    terminal._set_pane_title(2, "Agent2")
    
    terminal._split_pane(0, "-v")  # Split main pane vertically
    terminal._set_pane_title(3, "Monitor")
    
    # Set custom layout
    terminal._set_layout(TerminalLayout.TILED)
    
    # Update status line
    terminal._update_status_line()
    
    return terminal
```

### Session Analysis

You can analyze session data for insights:

```python
from mac.human_interface import TerminalSessionManager
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Load sessions
session_manager = TerminalSessionManager()
sessions = session_manager.list_sessions()

# Extract session durations
durations = []
for session in sessions:
    if session.completed_at:
        duration = (session.completed_at - session.created_at).total_seconds() / 60
        durations.append({
            "id": session.id,
            "name": session.name,
            "mode": session.mode,
            "duration_minutes": duration,
            "tasks": len(session.tasks),
            "queries": len(session.queries)
        })

# Create DataFrame
df = pd.DataFrame(durations)

# Analyze
print(f"Average session duration: {df['duration_minutes'].mean():.2f} minutes")
print(f"Average tasks per session: {df['tasks'].mean():.2f}")
print(f"Average queries per session: {df['queries'].mean():.2f}")

# Plot
plt.figure(figsize=(10, 6))
plt.bar(df['name'], df['duration_minutes'])
plt.title('Session Durations')
plt.xlabel('Session Name')
plt.ylabel('Duration (minutes)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('session_durations.png')
```