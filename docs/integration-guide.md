# HMS Component Integration Guide

This document provides a comprehensive guide for integrating HMS components and tools within the HMS ecosystem. It covers standard integration patterns, protocols, and examples to ensure seamless communication between components.

## Integration Principles

HMS follows these core integration principles:

1. **Standardized Interfaces**: All components expose well-defined APIs
2. **Loose Coupling**: Components interact through contracts, not implementations
3. **Resilient Communication**: All integration points handle failures gracefully
4. **Cross-Component Verification**: Integration tests validate communication
5. **Documentation-First**: API contracts are documented before implementation

## Integration Patterns

HMS supports several integration patterns:

### 1. RESTful API

Components communicate over HTTP using standard REST conventions:

```
POST /api/v1/tools
GET /api/v1/tools/{id}
PUT /api/v1/tools/{id}
DELETE /api/v1/tools/{id}
```

**Example Request:**
```json
POST /api/v1/tools
{
  "name": "Code Analyzer",
  "description": "Analyzes code quality and complexity",
  "version": "1.0.0",
  "category": "development",
  "entrypoint": "/analyze"
}
```

**Example Response:**
```json
{
  "id": "tool-12345",
  "name": "Code Analyzer",
  "description": "Analyzes code quality and complexity",
  "status": "pending_verification"
}
```

### 2. Message Queue

For asynchronous operations, components communicate via message queues:

```javascript
// Publishing a message
await messageQueue.publish('hms.tools.verified', {
  toolId: 'tool-12345',
  verificationResult: 'passed',
  timestamp: new Date().toISOString()
});

// Subscribing to messages
messageQueue.subscribe('hms.tools.verified', async (message) => {
  await toolRegistry.updateStatus(message.toolId, 'verified');
});
```

### 3. WebSocket

For real-time updates and notifications:

```javascript
// Server (Component A)
const wsServer = new WebSocketServer({ port: 8080 });
wsServer.on('connection', (socket) => {
  socket.on('toolStatusUpdate', (data) => {
    // Process tool status update
  });
});

// Client (Component B)
const socket = new WebSocket('ws://localhost:8080');
socket.send(JSON.stringify({
  type: 'toolStatusUpdate',
  data: { toolId: 'tool-12345', status: 'verified' }
}));
```

### 4. Direct Function Calls

For in-process integration within the same application:

```javascript
// Component A exports function
export async function verifyTool(toolId) {
  // Verification logic
  return { passed: true, score: 95 };
}

// Component B imports and calls function
import { verifyTool } from '@hms/verification';
const result = await verifyTool('tool-12345');
```

## Inter-Component Communication Protocol

HMS components follow a standardized communication protocol:

### Request Format

```json
{
  "requestId": "req-12345",
  "timestamp": "2023-05-15T10:30:00Z",
  "source": "HMS-DEV",
  "target": "HMS-A2A",
  "action": "executeTask",
  "payload": {
    "taskId": "task-6789",
    "parameters": {}
  },
  "metadata": {
    "priority": "high",
    "timeout": 30000
  }
}
```

### Response Format

```json
{
  "requestId": "req-12345",
  "timestamp": "2023-05-15T10:30:05Z",
  "source": "HMS-A2A",
  "target": "HMS-DEV",
  "status": "success",
  "payload": {
    "result": {},
    "metrics": {}
  },
  "metadata": {
    "processingTime": 5000
  }
}
```

### Error Response Format

```json
{
  "requestId": "req-12345",
  "timestamp": "2023-05-15T10:30:05Z",
  "source": "HMS-A2A",
  "target": "HMS-DEV",
  "status": "error",
  "error": {
    "code": "TASK_EXECUTION_FAILED",
    "message": "Failed to execute task due to missing parameters",
    "details": {}
  },
  "metadata": {
    "processingTime": 1000
  }
}
```

## Authentication & Authorization

HMS components authenticate using:

### JWT Authentication

```javascript
// Generate a token
const token = jwt.sign(
  { componentId: 'HMS-DEV', permissions: ['read:tools', 'write:tools'] },
  process.env.JWT_SECRET,
  { expiresIn: '1h' }
);

// Include in request
fetch('https://api.hms.com/tools', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

### API Key Authentication

```javascript
// Include API key in request
fetch('https://api.hms.com/tools', {
  headers: {
    'X-API-Key': process.env.HMS_API_KEY
  }
});
```

## Integration with Key HMS Components

### HMS-A2A Integration

The HMS-A2A (Agent-to-Agent) component facilitates task execution across the system:

```javascript
// Register a tool with HMS-A2A
await hmsA2aClient.registerTool({
  id: 'tool-12345',
  name: 'Code Analyzer',
  capabilities: ['analyze-code', 'suggest-improvements'],
  apiEndpoint: 'https://api.hms.com/tools/tool-12345'
});

// Execute a task through HMS-A2A
const result = await hmsA2aClient.executeTask({
  toolId: 'tool-12345',
  action: 'analyze-code',
  parameters: {
    repository: 'https://github.com/user/repo',
    language: 'javascript'
  }
});
```

### HMS-DOC Integration

Automatic documentation integration:

```javascript
// Register component documentation
await hmsDocClient.registerComponent({
  id: 'HMS-DEV',
  name: 'HMS Development Tools',
  description: 'Development tools and workflows for HMS components',
  documentation: {
    overview: '/docs/overview.md',
    api: '/docs/api.md',
    integration: '/docs/integration.md'
  }
});

// Update documentation on changes
await hmsDocClient.updateDocumentation({
  componentId: 'HMS-DEV',
  section: 'api',
  content: fs.readFileSync('/docs/api.md', 'utf8')
});
```

### Registry Service Integration

Tool registration and discovery:

```javascript
// Register a tool with the registry
const tool = await registryClient.registerTool({
  name: 'Code Analyzer',
  description: 'Analyzes code quality and complexity',
  version: '1.0.0',
  category: 'development',
  entrypoint: '/analyze'
});

// Search for tools by category
const tools = await registryClient.searchTools({
  category: 'development',
  status: 'verified'
});
```

## Integration Testing

HMS provides utilities for testing component integration:

```javascript
// Integration test example
describe('HMS-DEV and Registry Integration', () => {
  it('should register a tool and find it in search results', async () => {
    // Register a test tool
    const tool = await hmsDevClient.createTool({
      name: 'Test Tool',
      category: 'testing'
    });
    
    // Verify it appears in registry search
    const searchResults = await registryClient.searchTools({
      category: 'testing'
    });
    
    expect(searchResults).toContainEqual(expect.objectContaining({
      id: tool.id,
      name: 'Test Tool'
    }));
  });
});
```

## Configuration Management

HMS components use environment variables for integration configuration:

```
# HMS-DEV configuration
HMS_REGISTRY_URL=https://registry.hms.com
HMS_A2A_URL=https://a2a.hms.com
HMS_DOC_URL=https://doc.hms.com
HMS_API_KEY=hms_key_123456
HMS_JWT_SECRET=jwt_secret_123456

# Authentication timeouts
HMS_AUTH_TOKEN_EXPIRY=3600
HMS_REFRESH_TOKEN_EXPIRY=86400
```

## Error Handling

HMS defines standard error codes for integration issues:

| Error Code                | Description                                   |
|---------------------------|-----------------------------------------------|
| `AUTHENTICATION_FAILED`   | Invalid or expired authentication credentials |
| `AUTHORIZATION_DENIED`    | Insufficient permissions for the operation    |
| `RESOURCE_NOT_FOUND`      | The requested resource does not exist         |
| `VALIDATION_FAILED`       | Request data failed validation                |
| `RATE_LIMIT_EXCEEDED`     | Too many requests in a given time period      |
| `INTEGRATION_ERROR`       | Generic integration failure                   |
| `DEPENDENCY_UNAVAILABLE`  | Required dependent service is unavailable     |

## Versioning Strategy

HMS components follow semantic versioning:

- **Major version**: Incompatible API changes
- **Minor version**: Backwards-compatible functionality
- **Patch version**: Backwards-compatible bug fixes

When integrating components, version compatibility should be verified using the compatibility matrix in the HMS-DOC system.

## Adding New Integration Points

To add a new integration point:

1. Document the API contract in HMS-DOC
2. Implement the integration in your component
3. Create integration tests
4. Register the integration with HMS-A2A if agent interaction is required
5. Update this integration guide with examples