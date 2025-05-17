# HMS Component Agent Creation Guide

This guide provides a step-by-step process for creating a new component agent in the HMS ecosystem. Each HMS component has its own dedicated agent responsible for managing all aspects of that component.

## Overview

Creating a new component agent involves:
1. Analyzing and understanding the component
2. Establishing verification mechanisms
3. Implementing Chain of Recursive Thoughts (CoRT)
4. Setting up collaboration interfaces
5. Training and optimizing the agent

## Prerequisites

Before creating a component agent, ensure you have:
- Access to the full component codebase
- Understanding of the HMS ecosystem architecture
- Knowledge of the component's domain and purpose
- Access to the HMS-DEV and HMS-DOC components

## Step 1: Component Analysis

### Five-Pass Codebase Understanding

#### Pass 1: High-Level Context
- [ ] Read the component's README and documentation
- [ ] Identify the technology stack and dependencies
- [ ] Map directory structure and code organization
- [ ] Locate entry points and cross-cutting concerns
- [ ] Document output in [component]/agent/context.md

#### Pass 2: Component-Specific Analysis
- [ ] Customize analysis for the specific technology stack
- [ ] Generate detailed component architecture documentation
- [ ] Identify component-specific patterns and practices
- [ ] Document build, test, and deployment processes
- [ ] Map internal module relationships
- [ ] Document output in [component]/agent/architecture.md

#### Pass 3: Ecosystem Integration
- [ ] Document component's role in the HMS ecosystem
- [ ] Map integration points with other components
- [ ] Identify shared resources and dependencies
- [ ] Document communication patterns and protocols
- [ ] Analyze domain-specific knowledge requirements
- [ ] Document output in [component]/agent/integration.md

#### Pass 4: Development Process
- [ ] Document component development workflow
- [ ] Integrate with HMS-DEV processes
- [ ] Map documentation generation with HMS-DOC
- [ ] Establish testing and verification procedures
- [ ] Document deployment and release processes
- [ ] Document output in [component]/agent/workflow.md

#### Pass 5: Optimization Opportunities
- [ ] Identify collaboration patterns with other agents
- [ ] Define sub-agent organization for component aspects
- [ ] Plan Chain of Recursive Thoughts implementation
- [ ] Establish verification mechanism strategy
- [ ] Document output in [component]/agent/optimization.md

## Step 2: Verification Mechanism Implementation

### Identify Appropriate Verification Tools
- [ ] Select language-specific linters and static analyzers
- [ ] Configure test coverage requirements
- [ ] Implement architecture conformance checkers
- [ ] Set up documentation verification tools
- [ ] Document in [component]/agent/verification.md

### Implement Verification Pipelines
- [ ] Create automated verification workflows
- [ ] Integrate with CI/CD processes
- [ ] Implement pre-commit and post-commit checks
- [ ] Establish integration verification procedures
- [ ] Configure in [component]/agent/verification/config/

## Step 3: Chain of Recursive Thoughts (CoRT) Implementation

### Define Reasoning Framework
- [ ] Create problem decomposition templates
- [ ] Establish reasoning tree structure
- [ ] Define checkpoint verification steps
- [ ] Implement recursive refinement process
- [ ] Document in [component]/agent/cort.md

### Implement Decision Processes
- [ ] Create decision templates for common tasks
- [ ] Implement auditable reasoning trails
- [ ] Set up validation checkpoints
- [ ] Configure decision thresholds
- [ ] Store templates in [component]/agent/cort/templates/

## Step 4: Collaboration Interface Setup

### Define Component-Specific APIs
- [ ] Document component agent capabilities
- [ ] Define request/response formats
- [ ] Establish resource sharing protocols
- [ ] Create conflict resolution procedures
- [ ] Document in [component]/agent/collaboration.md

### Implement Communication Channels
- [ ] Set up agent registry integration
- [ ] Configure notification mechanisms
- [ ] Implement request handling
- [ ] Create response formatters
- [ ] Configure in [component]/agent/interfaces/

## Step 5: Agent Training and Optimization

### Configure Training Environment
- [ ] Set up isolated testing environment
- [ ] Create component-specific scenarios
- [ ] Define performance metrics
- [ ] Implement feedback collection
- [ ] Configure in [component]/agent/training/

### Implement Continuous Improvement
- [ ] Set up monitoring and performance tracking
- [ ] Create optimization suggestion system
- [ ] Implement knowledge base versioning
- [ ] Configure regular assessment cycles
- [ ] Document in [component]/agent/improvement.md

## Agent Structure

The component agent should be structured as follows:

```
[component]/agent/
  ├── README.md                 # Agent overview and guide
  ├── context.md                # Pass 1 output - high-level context
  ├── architecture.md           # Pass 2 output - component architecture
  ├── integration.md            # Pass 3 output - ecosystem integration
  ├── workflow.md               # Pass 4 output - development processes
  ├── optimization.md           # Pass 5 output - optimization strategy
  ├── verification/             # Verification mechanisms
  │   ├── config/               # Verification tool configurations
  │   └── templates/            # Verification templates
  ├── cort/                     # Chain of Recursive Thoughts
  │   ├── templates/            # Reasoning templates
  │   └── checkpoints/          # Validation checkpoints
  ├── interfaces/               # Collaboration interfaces
  │   ├── incoming/             # Request handlers
  │   └── outgoing/             # Response formatters
  ├── subagents/                # Component-specific sub-agents
  ├── training/                 # Agent training resources
  │   ├── scenarios/            # Test scenarios
  │   └── feedback/             # Human feedback collection
  └── knowledge/                # Component knowledge base
      ├── codebase/             # Code understanding
      ├── domain/               # Domain-specific knowledge
      └── history/              # Historical context
```

## Integration with Existing Agents

After creating the component agent:

1. Register with HMS-DEV agent:
   - [ ] Document component development workflow
   - [ ] Configure tool integration
   - [ ] Set up Pomodoro session management

2. Register with HMS-DOC agent:
   - [ ] Establish documentation generation processes
   - [ ] Configure documentation verification
   - [ ] Set up cross-component documentation integration

3. Identify key collaborator agents:
   - [ ] List primary integration components
   - [ ] Establish collaboration protocols with each
   - [ ] Schedule regular synchronization

## Best Practices

1. **Verification First**: Always implement sound verification mechanisms before adding new capabilities.

2. **Documentation Driven**: Document all agent decisions and capabilities as they're implemented.

3. **Incremental Enhancement**: Start with core functionality and gradually enhance capabilities.

4. **Explicit Reasoning**: Use Chain of Recursive Thoughts for all non-trivial decisions.

5. **Integration Testing**: Thoroughly test all collaboration interfaces.

6. **Human Feedback Loop**: Maintain regular human feedback cycles during initial training.

7. **Component Autonomy**: Respect the boundaries and responsibilities of other component agents.

## Conclusion

Following this guide will help you create a robust, well-integrated component agent that effectively manages its domain within the HMS ecosystem while collaborating productively with other agents through standardized interfaces.

The resulting agent will use sound verification mechanisms rather than relying on multi-LLM debates, implement Chain of Recursive Thoughts for complex reasoning, and continuously improve through systematic training and optimization.