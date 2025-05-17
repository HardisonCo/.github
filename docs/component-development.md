# HMS Component Development Guide

This document provides a step-by-step guide for developing new components within the HMS ecosystem. It covers the entire development lifecycle from initial planning to deployment and integration.

## Component Development Lifecycle

The HMS component development lifecycle follows these phases:

### 1. Planning & Specification

1. **Define Component Purpose**
   - Identify the specific problem the component solves
   - Document use cases and requirements
   - Define scope and boundaries

2. **Architecture Design**
   - Create high-level architecture
   - Identify integration points with other HMS components
   - Define data flows and processing models

3. **Interface Specification**
   - Document APIs and integration interfaces
   - Define request/response formats
   - Establish error handling patterns

4. **Acceptance Criteria**
   - Define functional requirements
   - Establish performance metrics
   - Document security requirements

### 2. Development Process

1. **Environment Setup**
   ```bash
   # Clone HMS-DEV repository
   git clone https://github.com/CodifyHQ/HMS-DEV.git
   
   # Create new component directory
   ./scripts/flow-tools.sh component create HMS-COMPONENT-NAME
   
   # Initialize development environment
   cd HMS-COMPONENT-NAME
   ./scripts/flow-tools.sh init
   ```

2. **Component Structure Setup**
   ```bash
   # Generate standard component structure
   ./scripts/flow-tools.sh scaffold
   
   # Initialize agent profile
   ./scripts/flow-tools.sh agent init
   ```

3. **Feature Development**
   ```bash
   # Create feature branch
   ./scripts/flow-tools.sh feature start feature-name
   
   # Work in Pomodoro sessions
   ./scripts/flow-tools.sh session start
   
   # Complete feature
   ./scripts/flow-tools.sh feature finish
   ```

4. **Documentation**
   ```bash
   # Generate initial documentation
   ./scripts/flow-tools.sh docs generate
   
   # Update integration points
   ./scripts/flow-tools.sh docs update-integration
   ```

### 3. Testing & Verification

1. **Unit Testing**
   ```bash
   # Create test suite
   ./scripts/flow-tools.sh test generate unit
   
   # Run unit tests
   npm test -- --testPathPattern=unit
   ```

2. **Integration Testing**
   ```bash
   # Create integration tests
   ./scripts/flow-tools.sh test generate integration
   
   # Run integration tests
   npm test -- --testPathPattern=integration
   ```

3. **Security Verification**
   ```bash
   # Run security scan
   ./scripts/flow-tools.sh security scan
   
   # Fix security issues
   ./scripts/flow-tools.sh security fix
   ```

4. **Performance Testing**
   ```bash
   # Run performance tests
   ./scripts/flow-tools.sh perf test
   
   # Analyze performance results
   ./scripts/flow-tools.sh perf analyze
   ```

### 4. Integration & Deployment

1. **HMS-A2A Integration**
   ```bash
   # Register component with HMS-A2A
   ./scripts/flow-tools.sh a2a register
   
   # Test A2A integration
   ./scripts/flow-tools.sh a2a test
   ```

2. **Registry Integration**
   ```bash
   # Register in HMS Registry
   ./scripts/flow-tools.sh registry register
   
   # Verify registry entry
   ./scripts/flow-tools.sh registry verify
   ```

3. **Deployment**
   ```bash
   # Prepare for deployment
   ./scripts/flow-tools.sh deploy prepare
   
   # Deploy component
   ./scripts/flow-tools.sh deploy execute
   
   # Verify deployment
   ./scripts/flow-tools.sh deploy verify
   ```

## Component Structure

HMS components should follow this standard structure:

```
HMS-[COMPONENT]/
  ├── README.md             # Component documentation
  ├── CONTRIBUTING.md       # Contribution guidelines
  ├── LICENSE               # License information
  ├── CLAUDE.md             # Guidance for Claude AI
  ├── docs/                 # Detailed documentation
  │   ├── index.md          # Documentation home
  │   ├── architecture.md   # Architecture details
  │   ├── api.md            # API documentation
  │   └── agent.md          # Agent capabilities
  ├── src/                  # Source code
  │   ├── index.[js|ts|py|rs]  # Entry point
  │   ├── controllers/      # Business logic
  │   ├── models/           # Data models
  │   ├── utils/            # Helper utilities
  │   ├── middleware/       # Middleware components
  │   └── services/         # Service implementations
  ├── tests/                # Test code
  │   ├── unit/             # Unit tests
  │   ├── integration/      # Integration tests
  │   └── fixtures/         # Test fixtures
  ├── agent/                # Agent implementation
  │   ├── agent_profile.yaml    # Agent capabilities
  │   ├── agent_journal.md      # Decision log
  │   ├── knowledge_base/       # Component knowledge
  │   └── sub_agents/           # Specialized agents
  ├── examples/             # Example usage
  └── [build files]         # Build configuration
```

## HMS Component Templates

HMS-DEV provides templates for different component types:

### 1. Service Component Template

```bash
./scripts/flow-tools.sh scaffold --type service
```

Creates a component focused on providing services to other components:
- API-driven design
- Service implementations
- Middleware components
- Request/response handlers

### 2. Agent Component Template

```bash
./scripts/flow-tools.sh scaffold --type agent
```

Creates a component focused on agent capabilities:
- Agent implementation
- Knowledge base structure
- Reasoning modules
- Sub-agent management

### 3. Tool Component Template

```bash
./scripts/flow-tools.sh scaffold --type tool
```

Creates a component focused on providing tools:
- Tool implementation
- I/O handling
- Result formatting
- Integration endpoints

### 4. UI Component Template

```bash
./scripts/flow-tools.sh scaffold --type ui
```

Creates a component focused on user interfaces:
- UI components
- State management
- API integration
- User interaction handling

## Agent Implementation

Each HMS component should include an agent implementation:

### 1. Agent Profile

```yaml
# agent/agent_profile.yaml
agent:
  id: "HMS-COMPONENT-Agent"
  name: "HMS Component Agent"
  version: "1.0.0"
  description: "Agent responsible for HMS-COMPONENT"
  
capabilities:
  - "capability_1"
  - "capability_2"
  
permissions:
  - "read:all"
  - "write:hms-component"
  
knowledge_areas:
  - "knowledge_area_1"
  - "knowledge_area_2"
  
integration_points:
  - component: "HMS-A2A"
    interface: "agent_communication"
  - component: "HMS-DOC"
    interface: "documentation_generation"
```

### 2. Agent Implementation

```javascript
// src/agent/index.js
import { Agent } from '@hms/agent-framework';
import { CortReasoning } from '@hms/cort';

class ComponentAgent extends Agent {
  constructor() {
    super({
      id: 'HMS-COMPONENT-Agent',
      capabilities: ['capability_1', 'capability_2'],
    });
    
    this.reasoning = new CortReasoning();
    this.knowledgeBase = new KnowledgeBase('./agent/knowledge_base');
  }
  
  async handleTask(task) {
    // Agent task handling implementation
    const result = await this.reasoning.solve(task);
    return result;
  }
  
  async createSubAgent(purpose) {
    // Sub-agent creation logic
    return new SubAgent(purpose);
  }
}

export default new ComponentAgent();
```

### 3. Knowledge Base Structure

```
agent/knowledge_base/
  ├── architecture.md       # Component architecture
  ├── api.md                # API documentation
  ├── integration.md        # Integration points
  ├── domain/               # Domain-specific knowledge
  ├── reasoning/            # Reasoning patterns
  └── examples/             # Usage examples
```

## Integration Guidelines

When developing HMS components, follow these integration guidelines:

### 1. HMS-A2A Integration

Implement the standard agent communication interface:

```javascript
// src/integration/a2a.js
import { A2AClient } from '@hms/a2a-client';

class A2AIntegration {
  constructor() {
    this.client = new A2AClient({
      componentId: 'HMS-COMPONENT',
      apiKey: process.env.HMS_A2A_API_KEY,
    });
  }
  
  async registerAgent() {
    await this.client.registerAgent({
      agentId: 'HMS-COMPONENT-Agent',
      capabilities: ['capability_1', 'capability_2'],
      apiEndpoint: '/api/agent',
    });
  }
  
  async sendTask(targetAgent, task) {
    return await this.client.sendTask(targetAgent, task);
  }
  
  async handleIncomingTask(task) {
    // Task handling implementation
  }
}

export default new A2AIntegration();
```

### 2. Registry Integration

Register your component with the HMS Registry:

```javascript
// src/integration/registry.js
import { RegistryClient } from '@hms/registry-client';

class RegistryIntegration {
  constructor() {
    this.client = new RegistryClient({
      componentId: 'HMS-COMPONENT',
      apiKey: process.env.HMS_REGISTRY_API_KEY,
    });
  }
  
  async registerComponent() {
    await this.client.registerComponent({
      id: 'HMS-COMPONENT',
      name: 'HMS Component',
      description: 'Component description',
      version: '1.0.0',
      capabilities: ['capability_1', 'capability_2'],
      apiEndpoint: '/api',
      agentEndpoint: '/api/agent',
    });
  }
  
  async registerTools() {
    await this.client.registerTool({
      id: 'tool-1',
      name: 'Tool Name',
      description: 'Tool description',
      endpoint: '/api/tools/tool-1',
    });
  }
}

export default new RegistryIntegration();
```

### 3. Documentation Integration

Integrate with HMS-DOC for documentation management:

```javascript
// src/integration/doc.js
import { DocClient } from '@hms/doc-client';

class DocIntegration {
  constructor() {
    this.client = new DocClient({
      componentId: 'HMS-COMPONENT',
      apiKey: process.env.HMS_DOC_API_KEY,
    });
  }
  
  async registerDocumentation() {
    await this.client.registerComponent({
      id: 'HMS-COMPONENT',
      name: 'HMS Component',
      documentation: {
        overview: './docs/index.md',
        architecture: './docs/architecture.md',
        api: './docs/api.md',
      },
    });
  }
  
  async updateDocumentation() {
    await this.client.updateDocumentation({
      componentId: 'HMS-COMPONENT',
      section: 'api',
      content: readFileSync('./docs/api.md', 'utf8'),
    });
  }
}

export default new DocIntegration();
```

## Verification Requirements

HMS components must meet these verification requirements:

### 1. Functional Verification

- Component performs all specified functions
- API endpoints return expected responses
- Error handling works correctly
- Edge cases are handled properly

### 2. Integration Verification

- Component integrates correctly with HMS-A2A
- Component integrates correctly with Registry
- Component integrates correctly with HMS-DOC
- All integration points are tested

### 3. Security Verification

- Authentication mechanisms work correctly
- Authorization controls access properly
- Sensitive data is protected
- Input validation prevents security issues

### 4. Performance Verification

- Component meets performance requirements
- Component handles expected load
- Resource usage is within acceptable limits
- Response times meet requirements

## Deployment Checklist

Before deploying an HMS component, ensure:

- [x] All tests pass
- [x] Security verification completed
- [x] Performance verification completed
- [x] Documentation is up-to-date
- [x] Integration points are verified
- [x] Environment configuration is complete
- [x] Monitoring is configured
- [x] Rollback procedures are in place

## Best Practices

1. **Follow the Agent Responsibility Model**
   - Component agents have clear responsibilities
   - Sub-agents handle specialized tasks
   - Agents use CoRT for complex reasoning

2. **Use Verification-First Development**
   - Write tests before implementation
   - Verify all functionality
   - Validate integration points

3. **Maintain Comprehensive Documentation**
   - Document all APIs
   - Keep architecture documentation up-to-date
   - Document integration points clearly

4. **Follow Pomodoro-Based Development**
   - Work in structured sessions
   - Maintain agent journals
   - Regularly review progress

5. **Use HMS-DEV Tools**
   - Leverage workflow automation
   - Use verification tools
   - Integrate with HMS ecosystem