# Codex Custom Boot Sequence Implementation Plan

## Overview

This document outlines the implementation plan for creating a custom boot sequence for the Codex CLI that displays system components and their statuses during initialization. The boot sequence will provide users with a visually appealing and informative display of the system's startup process.

## Goals

1. Create a visually engaging boot sequence
2. Display HMS system components and their initialization status
3. Show real-time progress of system initialization
4. Provide useful information about component states
5. Maintain compatibility with both TypeScript and Rust CLI implementations

## Key Components

The boot sequence will visualize the following HMS system components:

| Component | Description | Priority |
|-----------|-------------|----------|
| HMS-SYS | Core infrastructure and operations (replaces HMS-OPS) | High |
| HMS-API | Application Programming Interface | High |
| HMS-A2A | Agency-to-Agency integration | Medium |
| HMS-DEV | Development environment | High |
| HMS-DOC | Documentation system | Medium |
| HMS-NFO | Information framework | Medium |
| HMS-GOV | Governance system | Medium |
| HMS-CDF | Policy development framework | Low |
| HMS-MBL | Moneyball trade system | Low |
| HMS-ETL | Data processing pipeline | Medium |

## Implementation Approach

### 1. Extend Initialization Flows

#### TypeScript CLI

Modify the initialization process in `codex-cli/src/cli.tsx` and `codex-cli/src/app.tsx` to include the custom boot sequence:

```typescript
// In cli.tsx
import { BootSequence } from "./boot-sequence";

// After line 191 (before handling command line arguments)
// Initialize and display boot sequence
const bootSequence = new BootSequence({
  components: config.enabledComponents || DEFAULT_COMPONENTS,
  displayMode: config.bootDisplayMode || "standard"
});
await bootSequence.start();
```

#### Rust CLI

Extend the initialization process in `codex-rs/cli/src/main.rs`:

```rust
// In main.rs, add after line 64 (before handling subcommands)
use codex_cli::boot_sequence::BootSequence;

// Initialize and display boot sequence
let boot_sequence = BootSequence::new(
    &config.enabled_components.unwrap_or(DEFAULT_COMPONENTS.to_vec()),
    &config.boot_display_mode.unwrap_or("standard".to_string())
);
boot_sequence.start()?;
```

### 2. Boot Sequence Component

#### TypeScript Implementation

Create a new component at `codex-cli/src/boot-sequence.tsx`:

```typescript
import { Box, Text } from "ink";
import React, { useState, useEffect } from "react";
import { statusFromAPI } from "./utils/status";

type BootComponentStatus = "pending" | "loading" | "success" | "error" | "skipped";

interface BootComponent {
  id: string;
  name: string;
  description: string;
  status: BootComponentStatus;
  dependencies?: string[];
}

interface BootSequenceProps {
  components: string[];
  displayMode: "minimal" | "standard" | "verbose";
}

export class BootSequence {
  private components: BootComponent[];
  private displayMode: "minimal" | "standard" | "verbose";
  
  constructor(props: BootSequenceProps) {
    this.displayMode = props.displayMode;
    this.components = this.resolveComponents(props.components);
  }
  
  private resolveComponents(componentIds: string[]): BootComponent[] {
    // Convert component IDs to full component definitions with default status
    // This would be replaced with actual component definitions
    return componentIds.map(id => ({
      id,
      name: `HMS-${id}`,
      description: this.getComponentDescription(id),
      status: "pending",
    }));
  }
  
  private getComponentDescription(id: string): string {
    // Component descriptions
    const descriptions: Record<string, string> = {
      SYS: "System infrastructure and operations",
      API: "Application Programming Interface",
      A2A: "Agency-to-Agency integration",
      DEV: "Development environment",
      DOC: "Documentation system",
      NFO: "Information framework",
      GOV: "Governance system",
      CDF: "Policy development framework",
      MBL: "Moneyball trade system",
      ETL: "Data processing pipeline",
    };
    
    return descriptions[id] || `HMS-${id} Component`;
  }
  
  async start(): Promise<void> {
    // Render the boot sequence
    const { render, unmount } = render(<BootSequenceRenderer 
      components={this.components}
      displayMode={this.displayMode}
      onComplete={() => {
        // Unmount after completion
        setTimeout(() => unmount(), 1000);
      }}
    />);
    
    // Wait for completion
    return new Promise((resolve) => {
      const checkInterval = setInterval(() => {
        const allComplete = this.components.every(
          c => ["success", "error", "skipped"].includes(c.status)
        );
        
        if (allComplete) {
          clearInterval(checkInterval);
          setTimeout(() => {
            resolve();
          }, 1500); // Allow time to see the completed state
        }
      }, 100);
    });
  }
}

interface BootSequenceRendererProps {
  components: BootComponent[];
  displayMode: "minimal" | "standard" | "verbose";
  onComplete: () => void;
}

function BootSequenceRenderer({ 
  components, 
  displayMode,
  onComplete 
}: BootSequenceRendererProps): JSX.Element {
  const [bootComponents, setBootComponents] = useState<BootComponent[]>(components);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [complete, setComplete] = useState<boolean>(false);
  
  // Simulate the boot process
  useEffect(() => {
    const interval = setInterval(async () => {
      if (currentIndex >= bootComponents.length) {
        clearInterval(interval);
        setComplete(true);
        onComplete();
        return;
      }
      
      // Start loading the current component
      setBootComponents(prev => {
        const updated = [...prev];
        updated[currentIndex].status = "loading";
        return updated;
      });
      
      // Simulate checking component status
      try {
        // In a real implementation, this would call an actual status API
        const status = await statusFromAPI(bootComponents[currentIndex].id);
        
        // Update component status
        setTimeout(() => {
          setBootComponents(prev => {
            const updated = [...prev];
            updated[currentIndex].status = status ? "success" : "error";
            return updated;
          });
          
          // Move to next component
          setCurrentIndex(prev => prev + 1);
        }, Math.random() * 1000 + 500); // Random time between 500-1500ms
      } catch (error) {
        setBootComponents(prev => {
          const updated = [...prev];
          updated[currentIndex].status = "error";
          return updated;
        });
        
        // Move to next component
        setCurrentIndex(prev => prev + 1);
      }
    }, 100);
    
    return () => clearInterval(interval);
  }, [currentIndex, bootComponents]);
  
  return (
    <Box flexDirection="column" paddingY={1}>
      <Box borderStyle="round" paddingX={1} marginBottom={1}>
        <Text>
          ● Codex <Text bold>Boot Sequence</Text>{" "}
          <Text dimColor>v1.0.0</Text>
        </Text>
      </Box>
      
      <Box flexDirection="column">
        {bootComponents.map((component, index) => (
          <ComponentStatus 
            key={component.id}
            component={component}
            displayMode={displayMode}
            isActive={index === currentIndex}
          />
        ))}
      </Box>
      
      {complete && (
        <Box marginTop={1} paddingX={1}>
          <Text bold color="green">
            ✓ System initialization complete
          </Text>
        </Box>
      )}
    </Box>
  );
}

interface ComponentStatusProps {
  component: BootComponent;
  displayMode: "minimal" | "standard" | "verbose";
  isActive: boolean;
}

function ComponentStatus({ 
  component, 
  displayMode,
  isActive 
}: ComponentStatusProps): JSX.Element {
  // Status indicators
  const statusIndicator = {
    pending: <Text color="gray">⧖</Text>,
    loading: <Text color="yellow">↻</Text>,
    success: <Text color="green">✓</Text>,
    error: <Text color="red">✗</Text>,
    skipped: <Text color="blue">→</Text>,
  };
  
  // Status labels for verbose mode
  const statusLabel = {
    pending: <Text color="gray">Pending</Text>,
    loading: <Text color="yellow">Initializing</Text>,
    success: <Text color="green">Ready</Text>,
    error: <Text color="red">Failed</Text>,
    skipped: <Text color="blue">Skipped</Text>,
  };
  
  return (
    <Box>
      <Box marginRight={1}>
        {statusIndicator[component.status]}
      </Box>
      
      <Text bold={isActive} color={isActive ? "cyan" : undefined}>
        {component.name}
      </Text>
      
      {displayMode !== "minimal" && (
        <Box marginLeft={2}>
          <Text dimColor>{component.description}</Text>
        </Box>
      )}
      
      {displayMode === "verbose" && (
        <Box marginLeft={2}>
          {statusLabel[component.status]}
        </Box>
      )}
    </Box>
  );
}
```

#### Rust Implementation

Create a new module at `codex-rs/cli/src/boot_sequence.rs`:

```rust
use std::thread;
use std::time::{Duration, Instant};
use ratatui::backend::CrosstermBackend;
use ratatui::Terminal;
use ratatui::widgets::{Block, Borders, Paragraph};
use ratatui::layout::{Layout, Constraint, Direction};
use ratatui::style::{Color, Style, Modifier};
use crossterm::event::{Event, KeyCode};
use crossterm::terminal::{disable_raw_mode, enable_raw_mode};
use anyhow::Result;

pub struct BootSequence {
    components: Vec<BootComponent>,
    display_mode: String,
}

struct BootComponent {
    id: String,
    name: String,
    description: String,
    status: BootComponentStatus,
}

enum BootComponentStatus {
    Pending,
    Loading,
    Success,
    Error,
    Skipped,
}

impl BootSequence {
    pub fn new(component_ids: &Vec<String>, display_mode: &str) -> Self {
        let components = component_ids.iter()
            .map(|id| {
                BootComponent {
                    id: id.clone(),
                    name: format!("HMS-{}", id),
                    description: Self::get_component_description(id),
                    status: BootComponentStatus::Pending,
                }
            })
            .collect();
            
        BootSequence {
            components,
            display_mode: display_mode.to_string(),
        }
    }
    
    fn get_component_description(id: &str) -> String {
        match id.as_str() {
            "SYS" => "System infrastructure and operations".to_string(),
            "API" => "Application Programming Interface".to_string(),
            "A2A" => "Agency-to-Agency integration".to_string(),
            "DEV" => "Development environment".to_string(),
            "DOC" => "Documentation system".to_string(),
            "NFO" => "Information framework".to_string(),
            "GOV" => "Governance system".to_string(),
            "CDF" => "Policy development framework".to_string(),
            "MBL" => "Moneyball trade system".to_string(),
            "ETL" => "Data processing pipeline".to_string(),
            _ => format!("HMS-{} Component", id),
        }
    }
    
    pub fn start(&self) -> Result<()> {
        // Setup terminal
        enable_raw_mode()?;
        let stdout = std::io::stdout();
        let backend = CrosstermBackend::new(stdout);
        let mut terminal = Terminal::new(backend)?;
        terminal.clear()?;
        
        // Clone components to modify during boot
        let mut components = self.components.clone();
        let mut current_index = 0;
        let start_time = Instant::now();
        
        // Main boot loop
        while current_index < components.len() {
            // Update component status
            components[current_index].status = BootComponentStatus::Loading;
            
            // Render current state
            terminal.draw(|f| {
                // Layout
                let chunks = Layout::default()
                    .direction(Direction::Vertical)
                    .margin(1)
                    .constraints([
                        Constraint::Length(3), // Header
                        Constraint::Min(0),    // Components
                    ].as_ref())
                    .split(f.size());
                
                // Header
                let header = Paragraph::new("● Codex Boot Sequence v1.0.0")
                    .block(Block::default().borders(Borders::ALL))
                    .style(Style::default().fg(Color::White));
                f.render_widget(header, chunks[0]);
                
                // Components
                let component_chunks = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints(vec![Constraint::Length(1); components.len()].as_ref())
                    .split(chunks[1]);
                
                for (i, component) in components.iter().enumerate() {
                    let status_symbol = match component.status {
                        BootComponentStatus::Pending => "⧖",
                        BootComponentStatus::Loading => "↻",
                        BootComponentStatus::Success => "✓",
                        BootComponentStatus::Error => "✗",
                        BootComponentStatus::Skipped => "→",
                    };
                    
                    let status_color = match component.status {
                        BootComponentStatus::Pending => Color::DarkGray,
                        BootComponentStatus::Loading => Color::Yellow,
                        BootComponentStatus::Success => Color::Green,
                        BootComponentStatus::Error => Color::Red,
                        BootComponentStatus::Skipped => Color::Blue,
                    };
                    
                    let is_active = i == current_index;
                    let style = if is_active {
                        Style::default().fg(Color::Cyan).add_modifier(Modifier::BOLD)
                    } else {
                        Style::default()
                    };
                    
                    let mut display_text = format!("{} {}", status_symbol, component.name);
                    
                    if self.display_mode != "minimal" {
                        display_text = format!("{} - {}", display_text, component.description);
                    }
                    
                    let component_widget = Paragraph::new(display_text)
                        .style(style);
                    
                    f.render_widget(component_widget, component_chunks[i]);
                }
            })?;
            
            // Simulate component initialization (500-1500ms)
            let wait_time = rand::random::<u64>() % 1000 + 500;
            thread::sleep(Duration::from_millis(wait_time));
            
            // Update status to success (or sometimes error for realism)
            components[current_index].status = if rand::random::<u8>() % 20 == 0 {
                BootComponentStatus::Error
            } else {
                BootComponentStatus::Success
            };
            
            // Move to next component
            current_index += 1;
        }
        
        // Show completion message
        terminal.draw(|f| {
            // Layout
            let chunks = Layout::default()
                .direction(Direction::Vertical)
                .margin(1)
                .constraints([
                    Constraint::Length(3), // Header
                    Constraint::Min(0),    // Components
                    Constraint::Length(2), // Footer
                ].as_ref())
                .split(f.size());
            
            // Header
            let header = Paragraph::new("● Codex Boot Sequence v1.0.0")
                .block(Block::default().borders(Borders::ALL))
                .style(Style::default().fg(Color::White));
            f.render_widget(header, chunks[0]);
            
            // Components
            let component_chunks = Layout::default()
                .direction(Direction::Vertical)
                .constraints(vec![Constraint::Length(1); components.len()].as_ref())
                .split(chunks[1]);
            
            for (i, component) in components.iter().enumerate() {
                let status_symbol = match component.status {
                    BootComponentStatus::Pending => "⧖",
                    BootComponentStatus::Loading => "↻",
                    BootComponentStatus::Success => "✓",
                    BootComponentStatus::Error => "✗",
                    BootComponentStatus::Skipped => "→",
                };
                
                let status_color = match component.status {
                    BootComponentStatus::Pending => Color::DarkGray,
                    BootComponentStatus::Loading => Color::Yellow,
                    BootComponentStatus::Success => Color::Green,
                    BootComponentStatus::Error => Color::Red,
                    BootComponentStatus::Skipped => Color::Blue,
                };
                
                let mut display_text = format!("{} {}", status_symbol, component.name);
                
                if self.display_mode != "minimal" {
                    display_text = format!("{} - {}", display_text, component.description);
                }
                
                let component_widget = Paragraph::new(display_text)
                    .style(Style::default());
                
                f.render_widget(component_widget, component_chunks[i]);
            }
            
            // Footer
            let elapsed = start_time.elapsed();
            let footer = Paragraph::new(format!("✓ System initialization complete in {:.2}s", elapsed.as_secs_f32()))
                .style(Style::default().fg(Color::Green).add_modifier(Modifier::BOLD));
            f.render_widget(footer, chunks[2]);
        })?;
        
        // Wait for 1.5 seconds to show completion message
        thread::sleep(Duration::from_millis(1500));
        
        // Restore terminal
        disable_raw_mode()?;
        terminal.clear()?;
        
        Ok(())
    }
}
```

### 3. Status API Integration

Create a utility to check component status:

#### TypeScript Implementation (`codex-cli/src/utils/status.ts`):

```typescript
/**
 * Utility for checking component status during boot
 */

export async function statusFromAPI(componentId: string): Promise<boolean> {
  // In a real implementation, this would call APIs to check each component's status
  // For demo purposes, we'll simulate success with occasional failures
  
  // Check for standard HMS components
  const componentMap: Record<string, Function> = {
    'SYS': checkSystemStatus,
    'API': checkAPIStatus,
    'DEV': checkDevEnvironment,
    // Add other components as needed
  };
  
  // If we have a specific checker, use it
  if (componentMap[componentId]) {
    return await componentMap[componentId]();
  }
  
  // Default checker with 95% success rate
  return Math.random() > 0.05;
}

async function checkSystemStatus(): Promise<boolean> {
  // Simulate checking system status
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(true); // System should always be available
    }, 300);
  });
}

async function checkAPIStatus(): Promise<boolean> {
  // Simulate checking API status
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(Math.random() > 0.02); // 98% success rate
    }, 500);
  });
}

async function checkDevEnvironment(): Promise<boolean> {
  // Simulate checking dev environment
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(Math.random() > 0.01); // 99% success rate
    }, 200);
  });
}
```

#### Rust Implementation (`codex-rs/cli/src/status.rs`):

```rust
use std::thread;
use std::time::Duration;
use rand::Rng;

pub async fn check_component_status(component_id: &str) -> bool {
    // In a real implementation, this would call APIs to check each component's status
    // For demo purposes, we'll simulate success with occasional failures
    
    match component_id {
        "SYS" => check_system_status().await,
        "API" => check_api_status().await,
        "DEV" => check_dev_environment().await,
        // Default case with 95% success rate
        _ => {
            let mut rng = rand::thread_rng();
            thread::sleep(Duration::from_millis(rng.gen_range(200..600)));
            rng.gen::<f32>() > 0.05
        }
    }
}

async fn check_system_status() -> bool {
    // Simulate checking system status
    thread::sleep(Duration::from_millis(300));
    true // System should always be available
}

async fn check_api_status() -> bool {
    // Simulate checking API status
    thread::sleep(Duration::from_millis(500));
    let mut rng = rand::thread_rng();
    rng.gen::<f32>() > 0.02 // 98% success rate
}

async fn check_dev_environment() -> bool {
    // Simulate checking dev environment
    thread::sleep(Duration::from_millis(200));
    let mut rng = rand::thread_rng();
    rng.gen::<f32>() > 0.01 // 99% success rate
}
```

### 4. Configuration Integration

#### TypeScript Implementation

Update `codex-cli/src/utils/config.ts` to include boot sequence settings:

```typescript
// Add to the AppConfig interface
export interface AppConfig {
  // existing fields...
  
  // Boot sequence configuration
  bootDisplayMode?: "minimal" | "standard" | "verbose";
  enabledComponents?: string[];
}

// Add default values
const DEFAULT_CONFIG: AppConfig = {
  // existing defaults...
  
  bootDisplayMode: "standard",
  enabledComponents: ["SYS", "API", "A2A", "DEV", "DOC", "NFO", "GOV"],
};
```

#### Rust Implementation

Update `codex-rs/core/src/config.rs` to include boot sequence settings:

```rust
// Add to the Config struct
pub struct Config {
    // existing fields...
    
    // Boot sequence configuration
    pub boot_display_mode: Option<String>,
    pub enabled_components: Option<Vec<String>>,
}

// Add default values
impl Default for Config {
    fn default() -> Self {
        Config {
            // existing defaults...
            
            boot_display_mode: Some("standard".to_string()),
            enabled_components: Some(vec![
                "SYS".to_string(), 
                "API".to_string(), 
                "A2A".to_string(), 
                "DEV".to_string(), 
                "DOC".to_string(), 
                "NFO".to_string(), 
                "GOV".to_string(),
            ]),
        }
    }
}
```

## Configuration Options

Users can customize the boot sequence through the configuration file:

```toml
# ~/.codex/config.toml

[boot_sequence]
# Display mode: "minimal", "standard", or "verbose"
display_mode = "standard"

# Enabled components
enabled_components = ["SYS", "API", "DEV", "DOC", "NFO", "GOV"]

# Enable/disable boot sequence animation
enabled = true
```

## Testing Strategy

1. **Unit Tests**: Create tests for the boot sequence component logic
2. **Integration Tests**: Test the boot sequence within both CLI implementations
3. **Visual Tests**: Manually verify the appearance and behavior of the boot sequence
4. **Configuration Tests**: Verify configuration options are correctly applied

## Implementation Timeline

1. **Phase 1 (1-2 days)**:
   - Create TypeScript boot sequence implementation
   - Add configuration options
   - Basic visual testing

2. **Phase 2 (1-2 days)**:
   - Create Rust boot sequence implementation
   - Add configuration options
   - Integration testing

3. **Phase 3 (1 day)**:
   - Refinements based on testing
   - Documentation updates
   - Final review and deployment

## Key Benefits

1. **User Experience**: Provides a more engaging startup experience
2. **Transparency**: Shows system component status clearly
3. **Diagnostics**: Makes it easier to identify startup issues
4. **Professional Appearance**: Enhances the professional look and feel of the CLI

## Future Enhancements

1. **Detailed Component Diagnostics**: Add the ability to show detailed diagnostics for components
2. **Interactive Troubleshooting**: Allow users to interact with the boot sequence for troubleshooting
3. **Custom Themes**: Support for custom themes in the boot sequence
4. **Persistent Status Display**: Option to keep a minimal status display during CLI operation
5. **Animated Transitions**: Add smooth animated transitions between boot states

## Conclusion

The custom boot sequence will enhance the Codex CLI by providing a visually appealing and informative display during system initialization. It will help users understand the system's components and their status, making the CLI more professional and user-friendly.