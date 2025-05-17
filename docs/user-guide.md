# Boot Sequence User Guide

## Overview

The Codex CLI Boot Sequence provides a visual representation of system initialization, showing component status, dependencies, and timing information as the CLI starts up. This guide explains how to use, configure, and customize the boot sequence.

## Getting Started

### Enabling the Boot Sequence

The boot sequence is enabled by default. You can toggle it with:

#### Environment Variable

```bash
# Enable
export CODEX_BOOT_ENABLED=true

# Disable
export CODEX_BOOT_ENABLED=false
```

#### Command Line Flag

```bash
# Enable
codex --show-boot

# Disable
codex --no-show-boot
```

#### Configuration File

In your `~/.codex/config.toml` file:

```toml
[bootSequence]
enabled = true
```

### Basic Usage

When enabled, the boot sequence will display before the CLI initializes, showing the status of each system component as it loads.

## Display Modes

The boot sequence offers three display modes with increasing levels of detail:

### 1. Minimal Mode

Shows a compact view with basic component status, ideal for smaller terminals.

```bash
codex --boot-display-mode minimal
```

### 2. Standard Mode (Default)

Shows component status with timing information and a progress bar.

```bash
codex --boot-display-mode standard
```

### 3. Detailed Mode

Shows complete component details including descriptions and dependencies.

```bash
codex --boot-display-mode detailed
```

## Accessibility Features

### Text Mode

For screen reader compatibility, use text mode which outputs plain text without terminal UI elements:

```bash
codex --boot-accessibility-mode text
```

### High Contrast Mode

For better readability, enable high contrast mode:

```bash
codex --boot-high-contrast
```

### Disable Animations

To reduce visual stimuli or improve performance:

```bash
codex --boot-disable-animations
```

## Configuration Options

All configuration options can be set via environment variables, command line flags, or in the config file.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CODEX_BOOT_ENABLED` | Enable/disable boot sequence | `true` |
| `CODEX_BOOT_DISPLAY_MODE` | Display mode (minimal, standard, detailed) | `standard` |
| `CODEX_BOOT_ACCESSIBILITY_MODE` | Accessibility mode (visual, text) | `visual` |
| `CODEX_BOOT_HIGH_CONTRAST` | Enable high contrast mode | `false` |
| `CODEX_BOOT_DISABLE_ANIMATIONS` | Disable animations | `false` |
| `CODEX_BOOT_TIMEOUT_MS` | Component timeout in milliseconds | `30000` |
| `CODEX_BOOT_COMPONENT_DELAY_MS` | Delay between components in milliseconds | `300` |
| `CODEX_BOOT_COMPONENTS` | Comma-separated list of components to display | All components |

### Command Line Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--show-boot` | Enable boot sequence | - |
| `--no-show-boot` | Disable boot sequence | - |
| `--boot-display-mode <mode>` | Display mode | `standard` |
| `--boot-accessibility-mode <mode>` | Accessibility mode | `visual` |
| `--boot-high-contrast` | Enable high contrast mode | `false` |
| `--boot-disable-animations` | Disable animations | `false` |

### Configuration File

In `~/.codex/config.toml`:

```toml
[bootSequence]
enabled = true
displayMode = "standard"
accessibilityMode = "visual"
highContrast = false
disableAnimations = false
timeoutMs = 30000
componentDelayMs = 300
components = ["SYS", "API", "A2A", "DEV", "DOC", "NFO", "GOV"]
```

## Interactive Controls

During the boot sequence, you can use these keyboard shortcuts:

| Key | Action |
|-----|--------|
| `↑` | Navigate up |
| `↓` | Navigate down |
| `Tab` | Toggle component details |
| `q`, `Esc` | Skip boot sequence |
| `h` | Show help |

## Customizing Components

### Default Components

The boot sequence displays these standard components by default:

| ID | Name | Description |
|----|------|-------------|
| `SYS` | System Core | Core system components and runtime environment |
| `API` | API Client | Communication with backend services |
| `A2A` | Agent Protocol | A2A/MCP protocol implementation |
| `DEV` | Development Tools | Tools for software development workflows |
| `DOC` | Documentation | Documentation and help systems |
| `NFO` | Information Services | Information retrieval and storage |
| `GOV` | Governance | Compliance and governance systems |

### Filtering Components

To display only specific components:

```bash
# Environment variable
export CODEX_BOOT_COMPONENTS=SYS,API,DOC

# Command line
codex --boot-components SYS,API,DOC

# Config file
[bootSequence]
components = ["SYS", "API", "DOC"]
```

## Troubleshooting

### Boot Sequence Not Displaying

1. Check if it's enabled:
   ```bash
   echo $CODEX_BOOT_ENABLED
   ```

2. Verify it's not disabled in your config:
   ```bash
   cat ~/.codex/config.toml | grep bootSequence
   ```

3. Try forcing it with the command line flag:
   ```bash
   codex --show-boot
   ```

### Visual Mode Not Working

If the visual mode fails to display properly:

1. Try text mode instead:
   ```bash
   codex --boot-accessibility-mode text
   ```

2. Check terminal capabilities:
   ```bash
   echo $TERM
   ```

3. Verify terminal size:
   ```bash
   stty size
   ```

### Performance Issues

If the boot sequence is slow:

1. Try minimal display mode:
   ```bash
   codex --boot-display-mode minimal
   ```

2. Disable animations:
   ```bash
   codex --boot-disable-animations
   ```

3. Reduce the number of displayed components:
   ```bash
   export CODEX_BOOT_COMPONENTS=SYS,API
   ```

## Advanced Usage

### Telemetry Data

Boot sequence telemetry is stored in the logs directory and can be viewed with:

```bash
codex logs --boot-sequence
```

### Custom Component Integration

For developers extending the Codex CLI, you can register custom components:

```typescript
// TypeScript
import { registerBootComponent } from '@openai/codex-cli/boot-sequence';

registerBootComponent({
  id: 'CUSTOM',
  name: 'Custom Component',
  description: 'My custom functionality',
  dependencies: ['API'],
  check: async () => {
    // Custom initialization logic
    return true;
  }
});
```

```rust
// Rust
use codex_boot_sequence::{BootComponent, register_component};

let component = BootComponent::new(
    "CUSTOM",
    "Custom Component",
    "My custom functionality"
).with_dependency("API");

register_component(component, Box::new(|| async {
    // Custom initialization logic
    Ok(true)
}));
```

## Examples

### Basic Usage with Default Settings

```bash
codex --show-boot
```

### Accessible High Contrast Mode

```bash
codex --boot-high-contrast --boot-disable-animations
```

### Detailed Display with Selected Components

```bash
codex --boot-display-mode detailed --boot-components SYS,API,DEV
```

### Full Custom Configuration

```bash
codex --show-boot \
  --boot-display-mode standard \
  --boot-accessibility-mode visual \
  --boot-high-contrast \
  --boot-disable-animations \
  --boot-components SYS,API,DOC
```