# HMS Unified Animation Framework Overview

## Executive Summary

This document outlines a comprehensive strategy for implementing animated Mermaid diagrams within the Hardison Management Systems (HMS) ecosystem. By leveraging Mermaid\'s diagramming capabilities and extending them with animation techniques (primarily CSS and JavaScript sequencing), we aim to create dynamic, engaging visualizations of HMS architecture, processes, and data flows that enhance understanding and communication of complex systems.

## Background Analysis

1.  **HMS-UTL Component**: Contains a fork of the mermaid-live-editor, indicating existing interest in Mermaid diagramming.
2.  **Mermaid Core Capabilities**: Flowcharts, sequence diagrams, class diagrams, state diagrams, etc.
3.  **Animation Gap**: Mermaid itself does not natively support animations.
4.  **Integration Needs**: Animations must work within the HMS documentation (HMS-DOC, HMS-MFE) and visualization systems.

## Recommended Technical Approach: Hybrid Model

We utilize a hybrid approach combining multiple techniques:

### 1. Primary Implementation: CSS Animation Framework

-   Create a purpose-built CSS animation library (`src/visualization/animation.css`) specifically for Mermaid diagrams.
-   Develop standard animation patterns (pulse, highlight, flow) for common HMS visualization needs.
-   Use a JavaScript controller (`src/visualization/controller.ts`) for animation sequencing and coordination.
-   Implement automatic detection of Mermaid SVG structure for robustness.
-   Leverage CSS custom properties for theme customization (e.g., `--hms-highlight-color`).

### 2. Secondary Implementation: Sequenced Diagram System

-   For more complex state changes, implement a step-by-step diagram sequence system.
-   Create standardized diagram templates with animation \"keyframes.\"
-   Build a transition manager (within the JS controller) to handle sequencing and transitions.
-   Add user controls for stepping through animations manually.

## Technical Architecture

```mermaid
graph TB
    A[Agency Data Source (e.g., fed.agents.js)] --> B(Agency Data Processor)
    B --> C{Processed Agency Data}
    C --> D(Mermaid Diagram Generator)
    C --> E(Animation Controller Config)
    D --> F{Mermaid Diagram Definition}
    F --> G[Mermaid Renderer]
    G --> H(Base SVG Output)
    H --> I(HMS Animation Post-Processor)
    
    subgraph \"Animation Engine (JS/CSS)\"
        I --> J[Element Identifier]
        J --> K[Animation Pattern Applier]
        K --> L[CSS Animation Library]
        K --> M[Animation Sequence Manager (Controller)]
        E --> M
    end
    
    L --> N[Animated Diagram (HTML/SVG)]
    M --> N
    
    UserControls[User Controls] --> M
```

## Implementation Plan (General)

1.  **Foundation**: Develop core CSS animation library, Mermaid integration layer (post-processor, element identifier), basic JS controller, simple demos.
2.  **HMS-Specific Patterns**: Define patterns for architecture, data flow, state transitions; create configuration system (YAML/JSON or JS objects); build user controls.
3.  **Advanced Features**: Implement sequential diagram system (keyframes, diffing), optimize performance, create documentation and examples.
4.  **Integration & Deployment**: Integrate with HMS-UTL, HMS-DOC, HMS-MFE; create presets; test thoroughly.

## Technical Implementation Details

### CSS Animation Framework (`src/visualization/animation.css`)

Contains keyframes (`@keyframes hmsPulse`, `@keyframes hmsFlow`, etc.) and utility classes (`.hms-pulse`, `.hms-highlight`, `.hms-flow-path`). Respects `prefers-reduced-motion`.

### JavaScript Controller (`src/visualization/controller.ts`)

A TypeScript class (`AnimationController`) manages:
-   Loading animation steps (defined in config).
-   Finding SVG elements based on selectors.
-   Applying/removing CSS animation classes.
-   Handling user controls (next, previous, play, reset).
-   Updating step descriptions and counters.
-   Observing diagram container for SVG rendering.

### Animation Configuration Format

A JavaScript object (`AnimationControllerConfig`) passed to the controller, defining:
-   `diagramContainerId`: HTML element ID for the diagram.
-   `steps`: An array of `AnimationStep` objects, each with `id`, `elements` (CSS selectors), and `description`.
-   `controls`: IDs for the UI buttons and display elements.
-   Optional `playIntervalMs` and `onStepChange` callback.

## Integration with HMS Components

-   **HMS-NFO**: Provides component descriptions and potentially relationship data used by the `AgencyDataProcessor`.
-   **HMS-DEV / `scripts/generate-docs.ts`**: Uses `AgencyDataProcessor` and `MermaidDiagramGenerator` to create documentation, diagrams, and animation configurations (`agency-portal-data.js`).
-   **HMS-UTL**: Can incorporate the animation controller and CSS for enhancing the live editor.
-   **HMS-DOC / HMS-MFE**: Consumes the generated documentation and potentially embeds the interactive animations (see MFE Plan).
-   **codex-rs / codex-cli**: Could potentially trigger or display simplified animation states via A2A protocol messages (using `VisualizationInit`, `VisualizationStep`, `VisualizationEnd` events defined in `protocol_v1.md`).

## Success Metrics

-   **Performance**: Animation frame rate > 30fps.
-   **Browser Support**: Chrome, Firefox, Safari, Edge.
-   **Adoption**: Used in >50% of relevant HMS documentation.
-   **User Satisfaction**: Positive feedback >80%.
-   **Developer Experience**: Animation creation time < 30 minutes per standard diagram.

## Conclusion

The HMS Unified Animation System provides a robust and scalable method for creating dynamic visualizations. By combining CSS and JavaScript control, and integrating with core HMS data and generation tools, it enhances understanding of complex systems across the platform.

## Next Steps

1.  Finalize shared library components (`animation.css`, `controller.ts`).
2.  Refactor existing demos and portals to use the shared library.
3.  Complete integration with documentation generation script (`scripts/generate-docs.ts`).
4.  Implement documentation display within HMS-MFE. 