# Animated Mermaid – Overview

The fenced block below demonstrates the **step-wise animation** syntax we
support in this repository.  Each key-frame is delimited by a Markdown
comment of the form `%% step:N` where `N` is an integer that starts at 0.

```mermaid
%% step:0
sequenceDiagram
    participant API
    participant Poller
    API->>Poller: 0. every 30 mins
%% step:1
sequenceDiagram
    participant API
    participant Poller
    participant PollerState
    API->>Poller: 0. every 30 mins
    Poller->>PollerState: 1. request state
%% step:2
sequenceDiagram
    participant API
    participant Poller
    participant PollerState
    participant Handler
    API->>Poller: 0. every 30 mins
    Poller->>PollerState: 1. request state
    PollerState-->>Poller: 2. state response
    Poller->>Handler: 3. for each cfg
```

When the page loads:

1. Each key-frame is rendered to an SVG via Mermaid.
2. The helper script stacks the frames and cycles every 1.2 s.
3. A **📈 Live** link opens the standard Mermaid editor
   and **🎞️ Animate** opens the timeline editor that can export a GIF.

> 📝 Tip – commit your diagram, then run the pre-commit hooks to bake a GIF
> fallback so that PDF exports (or no-JS browsers) still see the animation.
