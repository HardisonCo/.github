# Boot Sequence Component Model

This document defines the standardized component model that should be used across both TypeScript and Rust implementations of the boot sequence.

## Overview

The boot sequence component model represents system components that are initialized during CLI startup. Each component has a unique identity, dependencies, status, and associated metadata. The model is designed to be:

1. Serializable between implementations
2. Expressive enough to capture component relationships
3. Consistent across different display modes
4. Extensible for future enhancements

## Core Components

### BootComponent

This is the primary data structure representing a system component.

#### TypeScript Definition

```typescript
export interface BootComponent {
  /** Unique identifier for the component */
  id: string;
  
  /** Human-readable name */
  name: string;
  
  /** Detailed description of component purpose */
  description: string;
  
  /** Current initialization status */
  status: BootComponentStatus;
  
  /** Optional error message if initialization failed */
  error?: string;
  
  /** Time taken to initialize in milliseconds */
  durationMs?: number;
  
  /** Delay before initializing this component (for visualization) */
  delay?: number;
  
  /** IDs of components this component depends on */
  dependencies: string[];
  
  /** Sub-components of this component */
  children: BootComponent[];
}
```

#### Rust Definition

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BootComponent {
    /// Unique identifier for the component
    pub id: String,
    
    /// Human-readable name
    pub name: String,
    
    /// Detailed description of component purpose
    pub description: String,
    
    /// Current initialization status
    pub status: BootComponentStatus,
    
    /// Optional error message if initialization failed
    pub error: Option<String>,
    
    /// Time taken to initialize in milliseconds
    pub duration_ms: Option<u64>,
    
    /// Delay before initializing this component (for visualization)
    pub delay: Option<Duration>,
    
    /// IDs of components this component depends on
    pub dependencies: Vec<String>,
    
    /// Sub-components of this component
    pub children: Vec<BootComponent>,
}
```

### BootComponentStatus

Enum representing possible component initialization states.

#### TypeScript Definition

```typescript
export enum BootComponentStatus {
  /** Component is waiting to be initialized */
  Waiting = 'waiting',
  
  /** Component is currently initializing */
  Initializing = 'initializing',
  
  /** Component has been successfully initialized */
  Ready = 'ready',
  
  /** Component failed to initialize */
  Failed = 'failed',
  
  /** Component initialization timed out */
  TimedOut = 'timedOut',
}
```

#### Rust Definition

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum BootComponentStatus {
    /// Component is waiting to be initialized
    Waiting,
    
    /// Component is currently initializing
    Initializing,
    
    /// Component has been successfully initialized
    Ready,
    
    /// Component failed to initialize
    Failed,
    
    /// Component initialization timed out
    TimedOut,
}
```

### BootSequenceConfig

Configuration for controlling boot sequence behavior.

#### TypeScript Definition

```typescript
export interface BootSequenceConfig {
  /** Enable/disable boot sequence */
  enabled: boolean;
  
  /** Display mode for boot sequence */
  displayMode: 'minimal' | 'standard' | 'detailed';
  
  /** Accessibility mode */
  accessibilityMode: 'visual' | 'text';
  
  /** Whether to use high contrast mode */
  highContrast: boolean;
  
  /** Whether to disable animations */
  disableAnimations: boolean;
  
  /** Timeout for component initialization in milliseconds */
  timeoutMs: number;
  
  /** Delay between component initializations in milliseconds */
  componentDelayMs: number;
  
  /** Components to display in boot sequence */
  components: string[];
}
```

#### Rust Definition

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BootSequenceConfig {
    /// Enable/disable boot sequence
    pub enabled: bool,
    
    /// Display mode for boot sequence
    pub display_mode: String,
    
    /// Accessibility mode
    pub accessibility_mode: String,
    
    /// Whether to use high contrast mode
    pub high_contrast: bool,
    
    /// Whether to disable animations
    pub disable_animations: bool,
    
    /// Timeout for component initialization in milliseconds
    pub timeout_ms: u64,
    
    /// Delay between component initializations in milliseconds
    pub component_delay_ms: u64,
    
    /// Components to display in boot sequence
    pub components: Vec<String>,
}
```

## Standard Components

The following standard components should be available in all implementations:

| ID | Name | Description | Dependencies |
|----|------|-------------|-------------|
| `SYS` | System Core | Core system components and runtime environment | None |
| `API` | API Client | Communication with backend services | `SYS` |
| `A2A` | Agent Protocol | A2A/MCP protocol implementation | `API` |
| `DEV` | Development Tools | Tools for software development workflows | `SYS` |
| `DOC` | Documentation | Documentation and help systems | `SYS` |
| `NFO` | Information Services | Information retrieval and storage | `API` |
| `GOV` | Governance | Compliance and governance systems | `API`, `SYS` |

## Component Lifecycle

Components follow this lifecycle:

1. **Creation**: Component is instantiated with the `Waiting` status
2. **Dependency Check**: Prerequisites are validated
3. **Initialization**: Status changes to `Initializing` 
4. **Completion**: 
   - Success → `Ready` status
   - Failure → `Failed` status with error message
   - Timeout → `TimedOut` status

## Serialization

For cross-implementation compatibility, components should be serializable to/from JSON using these field mappings:

| TypeScript | Rust | JSON |
|------------|------|------|
| `id` | `id` | `id` |
| `name` | `name` | `name` |
| `description` | `description` | `description` |
| `status` | `status` | `status` |
| `error` | `error` | `error` |
| `durationMs` | `duration_ms` | `durationMs` |
| `delay` | `delay` | `delay` |
| `dependencies` | `dependencies` | `dependencies` |
| `children` | `children` | `children` |

Status values should be serialized as:

| TypeScript | Rust | JSON |
|------------|------|------|
| `BootComponentStatus.Waiting` | `BootComponentStatus::Waiting` | `"waiting"` |
| `BootComponentStatus.Initializing` | `BootComponentStatus::Initializing` | `"initializing"` |
| `BootComponentStatus.Ready` | `BootComponentStatus::Ready` | `"ready"` |
| `BootComponentStatus.Failed` | `BootComponentStatus::Failed` | `"failed"` |
| `BootComponentStatus.TimedOut` | `BootComponentStatus::TimedOut` | `"timedOut"` |

## Implementation Notes

### TypeScript

- Use TypeScript interfaces for compile-time type checking
- Implement validation for component structure
- Use enums with string values for status

### Rust

- Use Serde for serialization/deserialization
- Implement `Default` trait for optional fields
- Use proper Rust idioms (Option<T> for optional fields)

## Extension Points

The component model includes these extension points:

1. **Custom Components**: Adding new components beyond the standard set
2. **Sub-components**: Nesting child components within parent components
3. **Custom Status Checks**: Implementing alternative status checking logic
4. **Enhanced Telemetry**: Adding additional performance metrics
5. **Serialization Formats**: Supporting alternative serialization formats