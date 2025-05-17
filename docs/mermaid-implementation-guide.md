# Mermaid Diagram Implementation Guide for HMS Documentation

## Overview

This guide explains how to correctly implement Mermaid diagrams within HMS documentation. Mermaid is a JavaScript-based diagramming and charting tool that renders Markdown-inspired text definitions to create diagrams dynamically.

## Supported Diagram Types

The HMS documentation system supports the following Mermaid diagram types:

1. **Flowcharts** - For process flows and algorithms
2. **Sequence Diagrams** - For interaction sequences
3. **Gantt Charts** - For project timelines
4. **Entity Relationship Diagrams** - For data models
5. **Class Diagrams** - For component relationships
6. **State Diagrams** - For state transitions

## Diagram Implementation

### Basic Syntax

To include a Mermaid diagram in any Markdown document, use the following format:

```markdown
```mermaid
<diagram-type>
    <diagram-definition>
```
```

### Flowchart Example

```markdown
```mermaid
flowchart TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```
```

Renders as:

```mermaid
flowchart TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

### Sequence Diagram Example

```markdown
```mermaid
sequenceDiagram
    participant User
    participant HMS-API
    participant HMS-NFO
    
    User->>HMS-API: Request data
    HMS-API->>HMS-NFO: Forward request
    HMS-NFO-->>HMS-API: Return data
    HMS-API-->>User: Display data
```
```

Renders as:

```mermaid
sequenceDiagram
    participant User
    participant HMS-API
    participant HMS-NFO
    
    User->>HMS-API: Request data
    HMS-API->>HMS-NFO: Forward request
    HMS-NFO-->>HMS-API: Return data
    HMS-API-->>User: Display data
```

### Gantt Chart Example

```markdown
```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    
    section Phase 1
    Task 1        :a1, 2025-05-01, 7d
    Task 2        :a2, after a1, 5d
    
    section Phase 2
    Task 3        :b1, after a2, 10d
    Task 4        :b2, after a2, 15d
```
```

Renders as:

```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    
    section Phase 1
    Task 1        :a1, 2025-05-01, 7d
    Task 2        :a2, after a1, 5d
    
    section Phase 2
    Task 3        :b1, after a2, 10d
    Task 4        :b2, after a2, 15d
```

### Entity Relationship Diagram Example

```markdown
```mermaid
erDiagram
    ENTITY ||--o{ COMPONENT : implements
    COMPONENT ||--o{ USE-CASE : supports
```
```

Renders as:

```mermaid
erDiagram
    ENTITY ||--o{ COMPONENT : implements
    COMPONENT ||--o{ USE-CASE : supports
```

## Styling Guidelines

### Colors

Use the HMS standard color palette for consistent styling:

```markdown
```mermaid
graph TD
    A[HMS-NFO] --> B[HMS-API]
    
    style A fill:#f8cecc,stroke:#b85450
    style B fill:#d5e8d4,stroke:#82b366
```
```

### Node Shapes

Use appropriate node shapes to represent different elements:

- Rectangles `[Text]` for processes
- Rounded rectangles `(Text)` for states
- Diamonds `{Text}` for decisions
- Circles `((Text))` for events

### Class Definitions

For larger diagrams, use class definitions to apply styles consistently:

```markdown
```mermaid
graph TD
    A[Process 1]
    B[Process 2]
    C{Decision}
    
    classDef process fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef decision fill:#e1f5fe,stroke:#01579b,stroke-width:1px;
    
    class A,B process;
    class C decision;
```
```

## Common Diagram Types for HMS Documentation

### Component Integration Diagram

Use flowcharts to show how HMS components integrate:

```mermaid
flowchart TD
    NFO[HMS-NFO] --> API[HMS-API]
    NFO --> ETL[HMS-ETL]
    API --> MCP[HMS-MCP]
    ETL --> EHR[HMS-EHR]
    
    style NFO fill:#f8cecc,stroke:#b85450
    style API fill:#d5e8d4,stroke:#82b366
    style ETL fill:#d5e8d4,stroke:#82b366
    style MCP fill:#dae8fc,stroke:#6c8ebf
    style EHR fill:#dae8fc,stroke:#6c8ebf
```

### Documentation Pipeline Diagram

Use flowcharts to illustrate the documentation pipeline:

```mermaid
flowchart TD
    A[Environment Setup] --> B[Agency Issue Finder]
    B --> C[Use Case Enhancement]
    C --> D[Component Integration]
    D --> E[Tutorials]
    E --> F[Publication]
    
    style A fill:#e1f5fe,stroke:#01579b
    style B fill:#e8f5e9,stroke:#1b5e20
    style C fill:#fff8e1,stroke:#ff8f00
    style D fill:#f3e5f5,stroke:#7b1fa2
    style E fill:#ffebee,stroke:#c62828
    style F fill:#e8eaf6,stroke:#3f51b5
```

### Implementation Timeline

Use Gantt charts to visualize implementation timelines:

```mermaid
gantt
    title Implementation Timeline
    dateFormat  YYYY-MM-DD
    
    section Phase 1
    Foundation        :done, p1, 2025-05-01, 30d
    
    section Phase 2
    Acceleration      :active, p2, after p1, 60d
    
    section Phase 3
    Scaling           :p3, after p2, 180d
    
    section Phase 4
    Completion        :p4, after p3, 90d
```

### Data Model Relationships

Use entity-relationship diagrams to show data models:

```mermaid
erDiagram
    ENTITY ||--o{ COMPONENT : implements
    COMPONENT ||--o{ USE-CASE : supports
    
    ENTITY {
        string id
        string name
        string type
    }
    
    COMPONENT {
        string id
        string name
        string category
    }
```

## Best Practices

1. **Keep diagrams simple** - Focus on clarity over complexity
2. **Use consistent styling** - Follow HMS color and style guidelines
3. **Add meaningful labels** - Label all connections and relationships
4. **Test diagrams locally** - Verify rendering before committing
5. **Update diagrams when changes occur** - Keep diagrams in sync with text
6. **Use appropriate diagram types** - Choose the right type for your content
7. **Include diagrams in high-level sections** - Use diagrams for overviews

## Troubleshooting

### Common Issues

1. **Diagram not rendering**
   - Check for syntax errors in the Mermaid code
   - Ensure proper markdown format with triple backticks
   - Verify that there's no extra whitespace at the start of lines

2. **Formatting issues**
   - Use single spaces for indentation in Mermaid code
   - Make sure quotes are properly escaped
   - Avoid special characters in node labels

3. **Complex diagrams not displaying correctly**
   - Break into smaller, focused diagrams
   - Simplify the structure
   - Reduce the number of nodes and connections

## References

- [Mermaid Documentation](https://mermaid-js.github.io/mermaid/#/)
- [HMS Style Guide](/Users/arionhardison/Desktop/CodifyHQ/HMS-DOC/CLAUDE.md)
- [Example Diagrams](/Users/arionhardison/Desktop/CodifyHQ/HMS-DOC/comprehensive_documentation_progress_tracker.md)