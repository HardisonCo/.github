# HMS-DEV Integration Map

This document outlines how HMS-DEV integrates with other components in the HMS ecosystem, detailing the specific integration points, data flows, and collaborative patterns.

## HMS-DEV Component Overview

HMS-DEV serves as the central development framework and OSS marketplace in the HMS ecosystem. Its primary responsibilities include:

1. **Tool Monetization**: Transform open source tools into monetizable components for agent consumption
2. **Development Workflows**: Provide structured workflows for component development
3. **Verification Mechanisms**: Implement verification-first approaches to ensure quality
4. **Agent-Based Development**: Support agent-based development with parent/sub-agent patterns

## Primary Integration Points

### 1. HMS-A2A (Agent-to-Agent)

**Integration Type**: Bidirectional API
**Purpose**: Enable tools to be discovered and used by agents in the A2A ecosystem

**Key Components**:
- **A2A Adapter**: Translates tool interfaces for A2A consumption
- **Authorization Service**: Manages access control for tools
- **Tool Execution Service**: Handles tool invocation requests from agents

**Data Flows**:
- HMS-DEV → HMS-A2A: Tool registration, capability advertising
- HMS-A2A → HMS-DEV: Tool discovery requests, invocation requests, usage metrics

**Implementation Files**:
- `/tool-marketplace/integration/a2a-adapter/index.js`
- `/tool-marketplace/integration/a2a-adapter/services/tool_executor.js`
- `/tool-marketplace/integration/a2a-adapter/services/authorization_service.js`

### 2. HMS-DOC (Documentation System)

**Integration Type**: Service integration
**Purpose**: Generate and maintain documentation for tools and components

**Key Components**:
- **API Documentation Interface**: Generates tool API documentation
- **Markdown Generator**: Creates standardized documentation
- **OpenAPI Generator**: Produces OpenAPI specifications for tools

**Data Flows**:
- HMS-DEV → HMS-DOC: Tool metadata, API specifications, example usage
- HMS-DOC → HMS-DEV: Documentation quality metrics, verification results

**Implementation Files**:
- `/tool-marketplace/api-interface/index.js`
- `/tool-marketplace/api-interface/models/api_doc.js`
- `/tool-marketplace/api-interface/controllers/doc_controller.js`

### 3. HMS-MCP (Model-Compute-Publish)

**Integration Type**: Service consumption
**Purpose**: Utilize models for verification and tool analysis

**Key Components**:
- **MCP Adapter**: Interface for model execution requests
- **Result Consumer**: Processes model execution results
- **Verification Bridge**: Uses models for verification tasks

**Data Flows**:
- HMS-DEV → HMS-MCP: Model execution requests, verification tasks
- HMS-MCP → HMS-DEV: Model execution results, verification outcomes

**Implementation Files**:
- `/tool-marketplace/integration/mcp-adapter/index.js`
- `/tool-marketplace/verification/analyzers/mcp_analyzer.js`

### 4. HMS-SYS (System Core)

**Integration Type**: Infrastructure dependency
**Purpose**: Utilize core system services for operation

**Key Components**:
- **Service Discovery**: Find and connect to other HMS components
- **Message Routing**: Communication between components
- **System Monitoring**: Overall system health tracking

**Data Flows**:
- HMS-DEV → HMS-SYS: Service registration, health metrics
- HMS-SYS → HMS-DEV: Service discovery, system events, alerts

**Implementation Files**:
- `/agent-workflow/supervisor/system_integration.js`
- `/tool-marketplace/registry/service/discovery.js`

## Secondary Integration Points

### 5. HMS-AGX (Advanced Graph Experience)

**Integration Type**: Tool integration
**Purpose**: Provide graph-based visualization and analysis of tools

**Key Components**:
- **Graph Generator**: Creates tool relationship graphs
- **Visualization Adapter**: Prepares data for AGX visualization

**Data Flows**:
- HMS-DEV → HMS-AGX: Tool relationship data, dependency graphs
- HMS-AGX → HMS-DEV: Graph analysis results, visualization outputs

### 6. HMS-LLM (Large Language Model Operations Platform)

**Integration Type**: Service consumption
**Purpose**: Utilize LLM capabilities for development assistance

**Key Components**:
- **LLM Integration**: Interface for LLM service consumption
- **Prompt Management**: Standardized prompts for development tasks
- **Output Processing**: Handling and verification of LLM outputs

**Data Flows**:
- HMS-DEV → HMS-LLM: Development assistance requests, code generation tasks
- HMS-LLM → HMS-DEV: Generated code, documentation snippets, analysis results

## Agent Collaboration Model

HMS-DEV implements the agent-based development workflow as described in CLAUDE.md:

```
┌─────────────┐      ┌────────────────┐      ┌─────────────────────┐
│  Component  │─req→│  Parent Agent   │─dlg→│  HMS-DEV Sub-Agent   │
│  Docs/Issues│      │  (this file)   │      │  (code writing)     │
└─────────────┘      └────────────────┘      └─────────────────────┘
        ↑                     ↓                         ↑
        │            ┌────────────────┐                │
        │            │ Background     │ agg/fbk         │
        └────────────│  CoRT Supervisor│<───────────────┘
                     └────────────────┘
```

The HMS-DEV agent collaborates with other component agents through:

1. **Request-Response Pattern**: Simple task delegation with completion acknowledgment
2. **Expert Consultation Pattern**: Specialized tasks delegated to component experts
3. **Collaborative Development Pattern**: Multi-agent work on cross-component features
4. **Supervisor Optimization Pattern**: Background process improvements

## Integration Implementation Guide

When integrating a new HMS component with HMS-DEV:

1. **Register Component in HMS-DEV**:
   - Add component metadata to `agent_knowledge_base/component_registry.json`
   - Create component profile in knowledge base
   - Define integration points and capabilities

2. **Set Up Development Workflow**:
   - Configure agent-based development process
   - Set up verification mechanisms
   - Establish CoRT supervisor integration

3. **Implement Tool Registration** (if applicable):
   - Register component tools in the marketplace
   - Define tool interfaces and capabilities
   - Set up verification and documentation

4. **Configure Documentation Integration**:
   - Set up automatic documentation generation
   - Define API documentation structure
   - Establish documentation verification

5. **Implement A2A Integration** (if applicable):
   - Configure A2A adapter for tool discovery
   - Set up authorization and execution services
   - Implement usage tracking and metrics

## Verification Framework Integration

The verification framework integrates with other HMS components to ensure quality:

1. **HMS-ESQ** (Enhanced System Quality):
   - Shares verification results and quality metrics
   - Receives quality improvement suggestions
   - Coordinates system-wide quality standards

2. **HMS-DOC** (Documentation System):
   - Verifies documentation completeness and accuracy
   - Ensures API documentation matches implementation
   - Validates cross-component integration docs

3. **HMS-LLM** (Large Language Model Operations):
   - Uses LLMs for code analysis and improvement suggestions
   - Implements verification for LLM-generated outputs
   - Leverages Chain of Recursive Thoughts for complex verifications

## OSS Marketplace Integration

The OSS marketplace integrates with:

1. **HMS-API** (API Services):
   - Registers tool APIs in the API catalog
   - Manages API versioning and compatibility
   - Monitors API usage and performance

2. **HMS-MKT** (Market Analytics):
   - Shares tool usage and performance metrics
   - Receives market trend analysis
   - Coordinates pricing strategy optimization

3. **HMS-A2A** (Agent-to-Agent):
   - Enables tool discovery by agents
   - Facilitates tool invocation and usage
   - Collects agent feedback on tools

## Conclusion

HMS-DEV serves as a central hub in the HMS ecosystem, providing development tools, verification mechanisms, and a marketplace for agent-consumable tools. Its integration with other HMS components enables a cohesive, well-structured development process that follows the verification-first principle and leverages agent-based workflows for improved quality and efficiency.

The implementation we've created establishes the foundational integration points with HMS-A2A, HMS-DOC, HMS-MCP, and HMS-SYS, while providing a framework for integration with additional components as needed.