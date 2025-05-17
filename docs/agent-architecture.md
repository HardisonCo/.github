# HMS Agent Architecture

This document describes the agent architecture used throughout the HMS system, focusing on agent capabilities, collaboration patterns, and implementation guidelines.

## Core Agent Concepts

The HMS agent architecture is built on these foundational concepts:

### Agent Definition

An **agent** in the HMS ecosystem is an autonomous software entity that:

- Has specific responsibilities for a component or domain
- Possesses specialized knowledge and capabilities
- Makes decisions based on clearly defined reasoning processes
- Collaborates with other agents through structured protocols
- Self-improves through feedback and experience

### Agent Responsibility Model

Each HMS component has a dedicated intelligent agent that:

- Fully understands its component's codebase, purpose, and integration points
- Can develop sub-agents to manage specific aspects of the component
- Interacts with other component agents using agreed-upon protocols
- Self-verifies using external validators rather than other LLMs
- Implements Chain of Recursive Thoughts (CoRT) for complex decisions

## Agent Hierarchy

HMS implements a hierarchical agent structure:

### Primary Component Agents

- One primary agent per HMS component (HMS-DEV, HMS-A2A, HMS-DOC, etc.)
- Full understanding of component's architecture and responsibilities
- Authority to make high-level decisions for the component
- Capability to spawn and manage sub-agents
- Direct integration with the CoRT supervisor

### Specialized Sub-Agents

- Created by primary agents for specific tasks
- Limited domain scope and focused expertise
- Typically short-lived for completion of specific tasks
- Operates with parameters set by the primary agent
- Reports results back to the primary agent

### Background Supervisor

- Long-running CoRT-based supervisor process
- Reviews agent journals and decisions
- Identifies optimization opportunities
- Issues improvement tickets to agents
- Ensures architectural consistency across components

## Agent Capabilities

HMS agents possess these core capabilities:

### Knowledge Management

- Comprehensive understanding of assigned component
- Access to component documentation and codebase
- Awareness of integration points with other components
- Memory of past decisions and their outcomes
- Updated knowledge through continuous learning

### Reasoning Processes

- **Chain of Recursive Thoughts (CoRT)**: Deep recursive reasoning for complex decisions
- **Step-by-Step Planning**: Breaking tasks into clear sequential steps
- **Verification-First Approach**: Focusing on verifiable outputs over complex reasoning
- **Pomodoro-Based Work Sessions**: Structured development sprints with reflection periods

### Communication Protocols

- Standardized request/response patterns
- Task assignment and delegation
- Progress reporting and status updates
- Error handling and recovery processes
- Knowledge sharing and discovery

## Agent Implementation

### Agent Structure

```
HMS-[COMPONENT]/
  ├── agent/
  │   ├── agent_profile.yaml    # Agent capabilities and permissions
  │   ├── agent_journal.md      # Decision log and reasoning
  │   ├── knowledge_base/       # Component-specific knowledge
  │   │   ├── architecture.md
  │   │   ├── api.md
  │   │   └── integration.md
  │   ├── sub_agents/           # Specialized task agents
  │   │   ├── code_agent.py
  │   │   ├── doc_agent.py
  │   │   └── test_agent.py
  │   └── reasoning/            # Reasoning implementations
  │       ├── cort.py
  │       └── verification.py
```

### Agent Profile Schema

```yaml
# agent_profile.yaml
agent:
  id: "HMS-DEV-Agent"
  name: "HMS Development Tools Agent"
  version: "1.0.0"
  description: "Primary agent responsible for HMS-DEV component"
  
capabilities:
  - "code_development"
  - "documentation"
  - "testing"
  - "agent_delegation"
  
permissions:
  - "read:all"
  - "write:hms-dev"
  - "exec:development-tools"
  - "spawn:sub-agents"
  
knowledge_areas:
  - "development_workflows"
  - "verification_systems"
  - "tool_integration"
  
integration_points:
  - component: "HMS-A2A"
    interface: "agent_communication"
  - component: "HMS-DOC"
    interface: "documentation_generation"
```

### Agent Journal Format

```markdown
# Agent Journal: HMS-DEV-Agent

## Session: 2023-05-15-1

### Decisions
1. **Implementation Approach for Tool Registry**
   - Selected Express.js for the API implementation
   - Reasoning: Provides robust middleware ecosystem and aligns with existing components
   - Alternatives considered: FastAPI (Python), Rust Actix

2. **Data Storage Decision**
   - Selected MongoDB for tool registry storage
   - Reasoning: Schema flexibility needed for evolving tool definitions
   - Verification: Ran performance tests with simulated load of 10k tools

### Blockers
1. **Integration with HMS-A2A**
   - Current blocker: Authentication mechanism not finalized
   - Proposed solution: Implement JWT-based auth with shared secret
   - Waiting on: HMS-A2A team to confirm approach

### Next Steps
1. Complete tool verification endpoint implementation
2. Create integration tests for HMS-DOC integration
3. Document API endpoints in OpenAPI format
```

## Agent Collaboration

### Collaboration Patterns

HMS agents collaborate through these patterns:

#### 1. Task Delegation

```javascript
// Primary agent delegates a task to a sub-agent
const codeReviewResponse = await delegateTask({
  agentType: "code_review",
  task: "Review pull request #123",
  parameters: {
    repository: "HMS-DEV",
    pullRequestId: 123,
    focusAreas: ["security", "performance"]
  },
  timeframe: "25min" // Pomodoro timeframe
});
```

#### 2. Knowledge Sharing

```javascript
// Agent shares knowledge with another agent
await shareKnowledge({
  recipient: "HMS-DOC-Agent",
  knowledge: {
    type: "api_documentation",
    content: {
      endpoints: [/* API endpoint details */],
      schemas: [/* Data schemas */]
    }
  }
});
```

#### 3. Consensus Building

```javascript
// Multiple agents collaborate on a decision
const decisionResult = await buildConsensus({
  decision: "architecture_change",
  proposal: {
    title: "Migrate from REST to GraphQL",
    description: "Proposal to change API architecture",
    implications: [/* List of impacts */]
  },
  participants: ["HMS-DEV-Agent", "HMS-API-Agent", "HMS-DOC-Agent"],
  consensusThreshold: 0.8
});
```

#### 4. Progress Reporting

```javascript
// Agent reports progress to supervisor
await reportProgress({
  taskId: "implement-registry-service",
  completion: 0.75,
  milestones: [
    { name: "API Design", status: "completed" },
    { name: "Core Implementation", status: "completed" },
    { name: "Integration Tests", status: "in_progress" },
    { name: "Documentation", status: "pending" }
  ],
  blockers: [/* Any blockers */]
});
```

## Chain of Recursive Thoughts (CoRT)

The HMS system implements CoRT as its primary reasoning methodology:

### CoRT Process

1. **Initial Thought**: Form an initial approach to the problem
2. **Recursive Exploration**: Recursively explore the solution space by questioning assumptions
3. **Alternative Branching**: Generate alternative solutions at each branch point
4. **Depth-Limited Search**: Apply depth limits to prevent infinite recursion
5. **Solution Verification**: Verify solutions against concrete acceptance criteria
6. **Synthesis**: Combine insights from multiple branches

### CoRT Implementation

```python
def cort_reasoning(problem, depth=0, max_depth=3):
    if depth >= max_depth:
        return {"reasoning": "Reached maximum recursion depth", "solutions": []}
    
    # Initial thought
    initial_thought = analyze_problem(problem)
    
    # Generate questions about the approach
    questions = generate_critical_questions(initial_thought)
    
    # Explore branches for each question
    branches = []
    for question in questions:
        refined_problem = refine_problem(problem, question)
        branch_result = cort_reasoning(refined_problem, depth + 1, max_depth)
        branches.append(branch_result)
    
    # Generate alternatives
    alternatives = generate_alternatives(initial_thought, branches)
    
    # Verify solutions
    verified_solutions = []
    for solution in alternatives:
        if verify_solution(solution, problem):
            verified_solutions.append(solution)
    
    # Synthesize insights
    synthesis = synthesize_insights(initial_thought, branches, verified_solutions)
    
    return {
        "reasoning": synthesis,
        "solutions": verified_solutions
    }
```

## Agent Verification System

HMS agents prioritize verification over complex reasoning:

### Verification Principles

1. **Verification is harder than generation**: Focus on proving correctness
2. **External validators over LLM checks**: Use concrete tools for validation
3. **Test-driven development**: Write tests before implementation
4. **Continuous validation**: Verify at each development step
5. **Concrete acceptance criteria**: Define clear verification metrics

### Verification Mechanisms

- **Unit Tests**: Validate individual functions and methods
- **Integration Tests**: Verify component interactions
- **Static Analysis**: Check code quality and security
- **Runtime Verification**: Monitor behavior during execution
- **Formal Verification**: Apply formal methods where feasible

### Verification Example

```javascript
// Verification of a tool registration implementation
const verificationResults = await verifyImplementation({
  component: "registry-service",
  implementation: "tool-registration-endpoint",
  verifications: [
    {
      type: "unit_test",
      description: "Validates tool schema correctly",
      script: "src/tests/unit/registry/validate-schema.test.js"
    },
    {
      type: "integration_test",
      description: "Tool registration end-to-end flow",
      script: "src/tests/integration/registry/tool-registration.test.js"
    },
    {
      type: "security_scan",
      description: "Check for security vulnerabilities",
      tool: "security-scanner",
      parameters: {
        targetPath: "src/controllers/toolController.js",
        ruleSet: "owasp-top-10"
      }
    }
  ]
});
```

## Developing New Agents

Guidelines for creating new agents in the HMS ecosystem:

### Agent Development Process

1. **Define Agent Profile**: Create agent_profile.yaml with capabilities and permissions
2. **Build Knowledge Base**: Compile relevant documentation and information
3. **Implement Reasoning Modules**: Add CoRT and verification implementations
4. **Create Communication Interfaces**: Implement standardized APIs
5. **Add Integration Points**: Connect with other HMS components
6. **Implement Verification Tests**: Create comprehensive test suite
7. **Deploy and Register**: Register agent with HMS-A2A

### Agent Quality Checklist

- [ ] Agent has clearly defined responsibilities
- [ ] Knowledge base is comprehensive and structured
- [ ] CoRT reasoning implementation is present
- [ ] Verification mechanisms are robust
- [ ] Communication protocols follow HMS standards
- [ ] Integration points are properly documented
- [ ] Tests cover all agent capabilities
- [ ] Security review completed
- [ ] Agent journal mechanism implemented

## HMS Agent System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CoRT Supervisor (HMS-SUP)                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Agent Communication Layer (HMS-A2A)           │
└───────┬───────────────┬───────────────┬───────────────┬─────────┘
        │               │               │               │
        ▼               ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  HMS-DEV      │ │  HMS-DOC      │ │  HMS-API      │ │  HMS-MCP      │
│  Agent        │ │  Agent        │ │  Agent        │ │  Agent        │
└───────┬───────┘ └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
        │                 │                 │                 │
        ▼                 ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  Sub-Agents   │ │  Sub-Agents   │ │  Sub-Agents   │ │  Sub-Agents   │
└───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘
```

## Future Directions

Planned improvements to the HMS agent architecture:

1. **Improved CoRT Algorithm**: Enhance recursive reasoning with better pruning strategies
2. **Learning from Journal Entries**: Implement learning from past decisions
3. **Multi-Agent Optimization**: Better coordination for complex tasks
4. **Context-Aware Delegation**: Improved task allocation based on agent capabilities
5. **Dynamic Knowledge Updates**: Real-time knowledge base maintenance
6. **Agent Performance Metrics**: Comprehensive evaluation of agent effectiveness

## Multi-Dimensional Agent Classification

The HMS agent architecture implements a versatile classification system that extends beyond the component-focused approach to incorporate specialized needs such as government-specific agents, standards-compliant agents, and domain specialists.

### Classification Dimensions

HMS agents are classified along multiple dimensions:

#### Primary Type
- **Component**: Responsible for HMS system components (API, CDF, A2A, etc.)
- **Domain**: Specialized in particular knowledge domains
- **Service**: Provides system-wide services
- **Interface**: Manages external system interactions

#### Application Domain
- **Government**: Designed for government-specific requirements
- **Civilian**: For general civilian use cases
- **Enterprise**: Focused on enterprise environments
- **Research**: Specialized for research applications

#### Capability Traits
- **A2A-Compliant**: Implements full agent-to-agent communication protocol
- **CoRT-Enhanced**: Utilizes Chain of Recursive Thoughts reasoning
- **Learning-Enabled**: Can adapt through experience
- **Standards-Compliant**: Adheres to specific standards (FedRAMP, HPC, etc.)

#### Structural Role
- **Supervisor**: Coordinates other agents
- **Peer**: Works collaboratively with other agents
- **Sub-Agent**: Operates under a parent agent's direction

#### Lifecycle
- **Persistent**: Long-running agent that maintains state
- **Ephemeral**: Short-lived agent for specific tasks
- **Scheduled**: Activated on a predetermined schedule
- **On-Demand**: Activated when needed

#### Security Clearance
- **Full-Access**: Unrestricted system access
- **Restricted**: Limited access based on role
- **Public**: Only public data access

### Classification Notation

Agents use a dot-notation to express their multi-dimensional classification:

```
PrimaryType.Domain.Capability.Role.Lifecycle.Security
```

Example:
```
Component.Government.CoRT.Supervisor.Persistent.Restricted
```

This describes a component agent for government use with CoRT reasoning, acting as a supervisor, with a persistent lifecycle and restricted security access.

## Agent Implementation Framework

### Agent Interface

All HMS agents implement a standard interface:

```typescript
interface IHMSAgent {
  // Core identity and classification
  id: string;
  classification: AgentClassification;
  
  // Lifecycle methods
  initialize(): Promise<void>;
  start(): Promise<void>;
  pause(): Promise<void>;
  resume(): Promise<void>;
  stop(): Promise<void>;
  
  // Communication methods
  sendMessage(recipient: string, message: any): Promise<void>;
  receiveMessage(sender: string, message: any): Promise<void>;
  
  // Reasoning and task execution
  executeTask(task: Task): Promise<TaskResult>;
  applyCoRT(problem: Problem, options?: CoRTOptions): Promise<Solution>;
  
  // Verification
  verifySolution(solution: Solution): Promise<VerificationResult>;
  
  // Agent management
  createSubAgent(spec: SubAgentSpec): Promise<IHMSAgent>;
  updateKnowledge(knowledge: Knowledge): Promise<void>;
}
```

### Agent Class Hierarchy

```
BaseAgent
├── ComponentAgent
│   ├── DevAgent
│   ├── DocAgent
│   ├── ApiAgent
│   └── A2AAgent
├── DomainAgent
│   ├── GovernmentAgent
│   ├── EnterpriseAgent
│   └── ResearchAgent
├── ServiceAgent
│   ├── SupervisorAgent
│   └── RegistryAgent
└── InterfaceAgent
    ├── ExternalSystemAgent
    └── UserInterfaceAgent
```

### Agent Registry

The HMS Agent Registry extends the existing system to support multi-dimensional classification:

```typescript
interface AgentRegistry {
  // Registration
  registerAgent(agent: IHMSAgent): Promise<void>;
  updateAgentStatus(agentId: string, status: AgentStatus): Promise<void>;
  
  // Discovery
  findAgents(query: AgentQuery): Promise<IHMSAgent[]>;
  getAgentById(agentId: string): Promise<IHMSAgent>;
  
  // Classification-based queries
  findByClassification(classification: Partial<AgentClassification>): Promise<IHMSAgent[]>;
  findByCapability(capability: string): Promise<IHMSAgent[]>;
  findByDomain(domain: string): Promise<IHMSAgent[]>;
}
```

## Implementation Roadmap

The implementation of this enhanced agent architecture will proceed in four phases:

### Phase 1: Foundation & Abstraction (Weeks 1-3)
- Define the `IHMSAgent` interface and `AgentClassification` structure
- Enhance the Agent Registry to support classification-based queries
- Create base agent classes for each primary type
- Update agent documentation and design patterns

### Phase 2: Component & Specialized Agent Integration (Weeks 4-7)
- Migrate existing component agents to the new classification system
- Implement government-specific agents with compliance capabilities
- Standardize sub-agent lifecycle management
- Develop agent verification systems for specialized domains

### Phase 3: Multi-Agent Collaboration & Orchestration (Weeks 8-12)
- Enhance supervisor patterns for cross-classification coordination
- Implement peer collaboration protocols
- Develop security models based on classification dimensions
- Create specialized collaboration flows for government and enterprise domains

### Phase 4: Advanced Features & Optimization (Weeks 13-16)
- Integrate enhanced CoRT reasoning across agent types
- Implement learning capabilities for appropriate agent classes
- Optimize agent discovery and collaboration performance
- Develop comprehensive monitoring and debugging tools

## Agent Governance

HMS implements a structured governance model for agent development and evolution:

### Agent Taxonomy Board
- Reviews and approves new agent classifications
- Ensures consistent implementation across systems
- Manages security and compliance requirements

### Development Process
- Standardized templates for new agent types
- Classification-specific testing requirements
- Documentation standards for each classification dimension

### Evolution Process
- Quarterly review of classification system
- Feedback loop from operational metrics
- Migration path for agent classification changes