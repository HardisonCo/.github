# MAC-Tmux Integration Guide

This document provides a comprehensive guide to the Multi-Agent Coordination (MAC) and tmux integration, which creates a terminal-based collaborative environment for agent interaction. 

## Overview

MAC-Tmux combines the HMS Multi-Agent Coordination (MAC) system with tmux, inspired by the tmuxai project, to enable agents to collaborate effectively in a terminal environment. It provides a powerful interface for observing terminal activities, coordinating agent actions, and managing collaborative workflows.

## Architecture

The MAC-Tmux integration consists of several key components:

1. **Session Management**: Creates and manages tmux sessions with appropriate layouts for agent collaboration
2. **Agent Integration**: Integrates MAC agents (Coordinator, Supervisor, Economist) with tmux panes
3. **Terminal Observation**: Monitors terminal activities and extracts context using techniques from tmuxai
4. **Command Interface**: Provides a command-line interface for controlling agents and sessions
5. **UI Components**: Visual indicators and formatting for agent activities

### Component Diagram

```
                           ┌─────────────────┐
                           │                 │
                           │   MAC System    │
                           │                 │
                           └────────┬────────┘
                                    │
                                    ▼
┌───────────────┐          ┌─────────────────┐          ┌───────────────┐
│               │          │                 │          │               │
│ MAC Core      │◄─────────┤   MAC-Tmux      ├─────────►│ tmux          │
│               │          │                 │          │               │
└───────────────┘          └────────┬────────┘          └───────────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │                 │
                           │  Terminal UI    │
                           │                 │
                           └─────────────────┘
```

## Key Features

### Multi-Mode Operation

MAC-Tmux supports four distinct operational modes:

- **Observe Mode**: Passive observation of terminal activities
- **Prepare Mode**: Enhanced shell interaction with command preparation
- **Watch Mode**: Proactive terminal monitoring
- **Collaborate Mode**: Full multi-agent collaboration

### Terminal Context Awareness

Similar to tmuxai, MAC-Tmux captures and understands terminal context:

- Command history tracking
- Shell detection and adaptation
- Context extraction (current directory, git status, etc.)
- Output analysis

### Agent Collaboration

Agents communicate and collaborate within the tmux environment:

- Coordinator agent manages workflow and tasks
- Supervisor agent monitors system health
- Economist agent handles resource allocation
- Observer agent understands terminal context
- Specialized agents provide domain-specific capabilities

### Command Interface

A rich command interface allows controlling the system:

- Session management commands
- Agent control commands
- Task management commands
- Context and configuration commands

## Integration Points

### Integration with MAC System

MAC-Tmux integrates with the MAC system through:

1. Agent traits from `mac::MACAgent`, `mac::CoordinatorAgent`, `mac::SupervisorAgent`
2. Message passing via `mac::models::Message` and `mac::models::Response`
3. Session management via MAC coordinator's session handling
4. Market network integration for resource allocation

### Integration with tmux

MAC-Tmux integrates with tmux through:

1. Session creation and management
2. Window and pane manipulation
3. Command execution in panes
4. Content capture and analysis
5. Status bar and UI customization

## Implementation Details

### Session Management

The `MacTmuxSession` struct manages tmux sessions with appropriate windows and panes for different agent roles. It provides methods for:

- Creating and initializing a session
- Adding windows and panes
- Setting layouts
- Sending commands to panes
- Capturing content
- Attaching and detaching

### Agent Integration

The `TmuxAgent` trait defines the interface for agents to interact with tmux:

- Initialization with a tmux pane
- Content handling
- Command processing
- Message passing

Implementations like `CoordinatorTmuxAgent`, `SupervisorTmuxAgent`, and `EconomistTmuxAgent` integrate specific MAC agents with tmux.

### Terminal Observation

The `TerminalObserver` handles monitoring terminal activities:

- Content capture and parsing
- Command extraction
- Context building
- Shell detection
- Git information extraction

### Command Interface

The `CommandParser` processes user commands and dispatches them to appropriate handlers:

- Session management commands
- Agent control commands
- Task management commands
- Context commands
- Configuration commands

## Usage Examples

### Starting a MAC-Tmux Session

```bash
# Start a session in collaborate mode
mac-tmux start --name my-session --mode collaborate
```

### In-Session Commands

```
# List active agents
agents list

# Start a work session
session start my-work-session

# Create a task
task create "Implement feature X" "Description of the task"

# Show terminal context
context show
```

### Agent Coordination

```
# In a coordinator pane
coordinator start-session development

# In a supervisor pane
supervisor monitor-system

# In an economist pane
economist allocate-resources
```

## Configuration

MAC-Tmux configuration is stored in TOML format:

```toml
[general]
default_session_name = "hms-mac"
auto_attach = true
enable_mac_integration = true

[agents]
roles = ["coordinator", "supervisor", "economist"]

[ui]
default_layout = "MainHorizontal"
color_theme = "default"
enable_status_bar = true

[session]
default_window_name = "mac-collaboration"
refresh_interval = 5
```

## Future Directions

1. **Enhanced Context Understanding**: Deeper parsing of terminal content
2. **Improved Agent Collaboration**: More sophisticated market-based coordination
3. **Visual Indicators**: Better visualization of agent activities
4. **Plugin System**: Extensibility for custom agents and capabilities
5. **Integration with Other Tools**: VSCode, JetBrains IDEs, etc.

## References

- [tmuxai GitHub repository](https://github.com/alvinunreal/tmuxai)
- [HMS MAC System Documentation](/docs/AGENTS/HMS_COMPONENT_INTEGRATION.md)
- [tmux Documentation](https://github.com/tmux/tmux/wiki)
- [MAC-MODEL-CORE-IMPLEMENTATION.md](/docs/MAC-MODEL-CORE-IMPLEMENTATION.md)

## Conclusion

The MAC-Tmux integration provides a powerful, terminal-based environment for agent collaboration, enabling seamless interaction between the MAC system and terminal activities. It combines the strengths of the tmuxai approach with the rich agent ecosystem of the MAC system, resulting in a versatile tool for development and operations in the HMS platform.