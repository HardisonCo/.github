# HMS Agent Model

This document outlines the agent model used throughout the HMS ecosystem, detailing the responsibilities, capabilities, and collaboration patterns of agents across all components.

## Agent Responsibility Model

Each HMS component has a dedicated intelligent agent that:

1. **Component Expertise**: Fully understands its component's codebase, purpose, and integration points
2. **Sub-Agent Management**: Can develop and orchestrate sub-agents to manage specific aspects of the component
3. **Inter-Agent Communication**: Interacts with other component agents using agreed-upon protocols via HMS-A2A
4. **Verification-First**: Self-verifies using external validators rather than other LLMs
5. **Decision Making**: Implements Chain of Recursive Thoughts (CoRT) for complex decisions

## Agent Hierarchy

The HMS ecosystem implements a hierarchical agent structure:

```
┌────────────────────┐
│ Background         │
│ CoRT Supervisor    │
└─────────┬──────────┘
          │ monitors & provides feedback
          ▼
┌────────────────────┐     delegates     ┌────────────────────┐
│ Component          │─────────────────▶ │ Sub-Agent 1        │
│ Agent              │                   └────────────────────┘
└─────────┬──────────┘                   ┌────────────────────┐
          │                              │ Sub-Agent 2        │
          ▼                              └────────────────────┘
┌────────────────────┐      interacts    ┌────────────────────┐
│ Other Component    │◀───────────────▶ │ Other Component    │
│ Agents             │                   │ Agents             │
└────────────────────┘                   └────────────────────┘
```

### Component Agents

Component agents are the primary agents responsible for an entire HMS component. They:

- Understand the entire component architecture
- Make high-level decisions about component development
- Delegate specific tasks to sub-agents
- Maintain the component's agent journal
- Participate in inter-component collaboration
- Report to the Background Supervisor

### Sub-Agents

Sub-agents are specialized agents created by component agents to handle specific tasks. They:

- Receive minimal prompts with exact scope
- Use HMS-DEV tooling for development
- Report completion status to parent agents
- Must pass certification to commit to protected branches
- Focus on a single responsibility

### Background Supervisor

The Background Supervisor implements the Chain of Recursive Thoughts (CoRT) algorithm to:

- Monitor all component agent journals
- Detect sub-optimal plans and decisions
- Propose refactors or new experiments
- Assign improvement tickets to agents
- Ensure continuous improvement across the ecosystem

## Agent Workflow: Pomodoro Sprints

Agents follow a Pomodoro-based workflow:

1. **Focus Phase (25 minutes)**
   - Work on assigned tasks
   - Document decisions and progress
   - Implement code and documentation

2. **Break Phase (5 minutes)**
   - Log decisions and blockers to agent journal
   - Push intermediate results via HMS-DEV commit hooks
   - Request feedback from Background Supervisor

3. **Review & Adjust**
   - Process feedback from Background Supervisor
   - Adjust plans based on feedback
   - Prioritize improvement tickets

## Agent Communication Protocols

Agents communicate using standardized protocols:

1. **Parent-Sub Communication**
   - Task delegation with clear scope and acceptance criteria
   - Status reporting and completion notification
   - Resource and permission requests

2. **Inter-Component Communication**
   - Uses HMS-A2A protocols and endpoints
   - Follows integration points defined in component registry
   - Respects direction constraints (incoming/outgoing/bidirectional)
   - Maintains proper authentication and authorization

3. **Supervisor Communication**
   - Journal entries for decisions and blockers
   - Improvement tickets with concrete acceptance criteria
   - Progress reporting on assigned tickets

## Agent Certification & Onboarding

Before sub-agents can commit to protected branches, they must:

1. Pass the trivia & onboarding quiz in `_HMS-DEV/STATE.md`
2. Demonstrate understanding of component architecture
3. Show proficiency with HMS-DEV tooling
4. Understand verification requirements and procedures
5. Commit to following the HMS development workflow

## Agent Development Standards

When developing new agents or enhancing existing ones:

1. Use the 5-pass approach to understand the relevant codebase
2. Follow the agent profile template in HMS-DOC
3. Implement all required interfaces for proper integration
4. Include comprehensive self-documentation
5. Build in verification mechanisms
6. Support the pomodoro workflow with proper journaling

## Implementation Resources

- `HMS-AGT/`: Parent and sub-agent entrypoints
- `agent_knowledge_base/`: Component-specific knowledge
- `HMS-DEV/supervisor/cort_supervisor.py`: Background Supervisor implementation
- `HMS-DOC/utils/generate_agent_profile.py`: Agent profile generator
- `_HMS-DEV/README.raw`: Source for trivia onboarding questions