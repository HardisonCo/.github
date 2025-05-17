# HMS-DEV Tool Registry Service

The Tool Registry Service provides a centralized registry for managing tools within the HMS ecosystem. It handles tool registration, discovery, verification, and integration with other HMS components.

## Overview

The Tool Registry Service is a RESTful API that allows:

- Registering new tools in the marketplace
- Discovering tools based on various criteria
- Managing tool verification status
- Defining and managing integration endpoints
- Tracking tool metrics and usage

## Architecture

The service follows a modular architecture with the following key components:

### Core Components

1. **Registry Service**: The main service implementation that manages the tool catalog.
2. **Tool Controller**: Handles HTTP requests and responses for tool operations.
3. **Middleware**: Provides authentication, validation, and other cross-cutting concerns.
4. **Routes**: Defines the API endpoints and their handlers.

### Integration Points

The Registry Service integrates with other HMS components:

- **HMS-A2A**: Tool discovery and execution
- **HMS-DOC**: Documentation generation for registered tools
- **HMS-MCP**: Verification task submission and results

## API Endpoints

### Tool Management

- `POST /api/tools` - Register a new tool
- `PUT /api/tools/:toolId` - Update an existing tool
- `GET /api/tools/:toolId` - Get a tool by ID
- `GET /api/tools` - List all tools, with optional filtering
- `DELETE /api/tools/:toolId` - Remove a tool

### Verification

- `PUT /api/tools/:toolId/verification` - Update tool verification status

### Integration Endpoints

- `GET /api/tools/:toolId/integrations` - Get tool integration endpoints
- `POST /api/tools/:toolId/integrations` - Register a new integration endpoint

## Tool Schema

Tools in the registry follow this schema:

```json
{
  "id": "unique-tool-id",
  "name": "Tool Name",
  "description": "Tool description",
  "version": "1.0.0",
  "category": "category",
  "capabilities": ["capability1", "capability2"],
  "creator": {
    "name": "Creator Name",
    "email": "creator@example.com",
    "organization": "Organization"
  },
  "homepage": "https://example.com",
  "documentation": "https://docs.example.com",
  "repository": "https://github.com/example/repository",
  "hasApi": true,
  "apiSpec": {},
  "pricing": {
    "model": "free",
    "details": {}
  },
  "interfaces": {},
  "integrationPoints": [
    {
      "name": "integration-name",
      "path": "/api/integration",
      "method": "POST",
      "description": "Integration description"
    }
  ],
  "registrationDate": "2023-01-01T00:00:00Z",
  "verificationStatus": "pending",
  "version": "1.0.0"
}
```

## Verification Process

Tools in the registry go through a verification process to ensure quality and security:

1. **Initial Registration**: Tools start with a `pending` verification status.
2. **Static Analysis**: Tools undergo static code analysis for security and quality.
3. **Dynamic Testing**: APIs and functionality are tested for correctness.
4. **Verification Decision**: Tools are marked as `verified` or `rejected`.

## Integration with A2A

The Registry Service integrates with HMS-A2A to enable tool discovery and execution:

1. **Tool Discovery**: A2A queries the registry for tools matching specific criteria.
2. **Authorization**: A2A obtains authorization to use specific tools.
3. **Execution**: A2A executes tools through their defined interfaces.

## Usage

### Starting the Service

```bash
# Install dependencies
npm install

# Start the service
npm start
```

### Environment Variables

- `PORT` - Port to run the service on (default: 3000)
- `NODE_ENV` - Environment (development, production)
- `JWT_SECRET` - Secret key for JWT authentication
- `SKIP_AUTH` - Skip authentication in development (true/false)

## Development

### Adding New Endpoints

1. Create a controller function in `controllers/toolController.js`
2. Add the route in `routes/toolRoutes.js`
3. Update the schema validation if needed

### Authentication

The service uses JWT for authentication. To authenticate:

1. Obtain a JWT token (implementation details depend on the HMS environment)
2. Include the token in the Authorization header: `Authorization: Bearer <token>`

## Integration with HMS Components

### HMS-A2A Integration

The Registry Service provides these endpoints for A2A integration:

- **Tool Discovery**: `GET /api/tools` with capability filtering
- **Tool Authorization**: Token-based authorization for tool access
- **Tool Execution**: Integration endpoints for tool execution

### HMS-DOC Integration

When a tool with `hasApi: true` is registered, the service automatically:

1. Generates OpenAPI documentation from the tool's API specification
2. Registers the documentation with HMS-DOC

### HMS-MCP Integration

The verification process integrates with HMS-MCP:

1. Verification tasks are submitted to MCP
2. MCP executes verification checks and returns results
3. The registry updates tool verification status based on results