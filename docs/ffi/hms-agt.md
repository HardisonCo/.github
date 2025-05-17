# HMS-AGT FFI Documentation

## Overview

The HMS-AGT (Agent Framework) component provides the core agent abstractions and functionality used throughout the HMS system. This document details the Foreign Function Interface (FFI) implementation for HMS-AGT, allowing integration with various programming languages.

## Proto Definitions

HMS-AGT defines the following protocol buffer files:

- `agent.proto`: Defines agent identity, capabilities, and state
- `capability.proto`: Defines agent capabilities and requirements
- `lifecycle.proto`: Defines agent lifecycle operations and states
- `tool.proto`: Defines tools that agents can use

These files are located in `ffi/proto/hms-ffi-protos/hms/agt/v1/`.

## Service Interfaces

### AgentService

The main service for agent management:

```protobuf
service AgentService {
  // Create a new agent
  rpc CreateAgent(CreateAgentRequest) returns (CreateAgentResponse);
  
  // Get an agent by ID
  rpc GetAgent(GetAgentRequest) returns (GetAgentResponse);
  
  // Update an agent's properties
  rpc UpdateAgent(UpdateAgentRequest) returns (UpdateAgentResponse);
  
  // Delete an agent
  rpc DeleteAgent(DeleteAgentRequest) returns (DeleteAgentResponse);
  
  // List agents with optional filtering
  rpc ListAgents(ListAgentsRequest) returns (ListAgentsResponse);
  
  // Get agent metrics
  rpc GetAgentMetrics(GetAgentMetricsRequest) returns (GetAgentMetricsResponse);
}
```

### LifecycleService

Service for managing agent lifecycle:

```protobuf
service LifecycleService {
  // Initialize an agent
  rpc InitializeAgent(InitializeAgentRequest) returns (InitializeAgentResponse);
  
  // Start an agent
  rpc StartAgent(StartAgentRequest) returns (StartAgentResponse);
  
  // Pause an agent
  rpc PauseAgent(PauseAgentRequest) returns (PauseAgentResponse);
  
  // Resume a paused agent
  rpc ResumeAgent(ResumeAgentRequest) returns (ResumeAgentResponse);
  
  // Stop an agent
  rpc StopAgent(StopAgentRequest) returns (StopAgentResponse);
  
  // Reset an agent to initial state
  rpc ResetAgent(ResetAgentRequest) returns (ResetAgentResponse);
}
```

### CapabilityService

Service for managing agent capabilities:

```protobuf
service CapabilityService {
  // Register a capability
  rpc RegisterCapability(RegisterCapabilityRequest) returns (RegisterCapabilityResponse);
  
  // Unregister a capability
  rpc UnregisterCapability(UnregisterCapabilityRequest) returns (UnregisterCapabilityResponse);
  
  // List available capabilities
  rpc ListCapabilities(ListCapabilitiesRequest) returns (ListCapabilitiesResponse);
  
  // Check if an agent has a specific capability
  rpc HasCapability(HasCapabilityRequest) returns (HasCapabilityResponse);
  
  // Add capability to an agent
  rpc AddCapabilityToAgent(AddCapabilityRequest) returns (AddCapabilityResponse);
  
  // Remove capability from an agent
  rpc RemoveCapabilityFromAgent(RemoveCapabilityRequest) returns (RemoveCapabilityResponse);
}
```

### ToolService

Service for managing agent tools:

```protobuf
service ToolService {
  // Register a tool
  rpc RegisterTool(RegisterToolRequest) returns (RegisterToolResponse);
  
  // Unregister a tool
  rpc UnregisterTool(UnregisterToolRequest) returns (UnregisterToolResponse);
  
  // List available tools
  rpc ListTools(ListToolsRequest) returns (ListToolsResponse);
  
  // Execute a tool
  rpc ExecuteTool(ExecuteToolRequest) returns (ExecuteToolResponse);
  
  // Stream tool execution results
  rpc StreamToolExecution(ExecuteToolRequest) returns (stream ToolExecutionEvent);
  
  // Grant tool access to an agent
  rpc GrantToolAccess(GrantToolAccessRequest) returns (GrantToolAccessResponse);
  
  // Revoke tool access from an agent
  rpc RevokeToolAccess(RevokeToolAccessRequest) returns (RevokeToolAccessResponse);
}
```

## Language Bindings

### Go Bindings

To use HMS-AGT in Go:

```go
import (
    agtpb "github.com/hardisonco/hms/gen/go/hms/agt/v1"
    "google.golang.org/grpc"
)

func main() {
    conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
    if err != nil {
        log.Fatalf("Failed to connect: %v", err)
    }
    defer conn.Close()
    
    client := agtpb.NewAgentServiceClient(conn)
    
    // Create an agent
    resp, err := client.CreateAgent(context.Background(), &agtpb.CreateAgentRequest{
        Agent: &agtpb.Agent{
            Name: "Test Agent",
            Type: agtpb.AgentType.AUTONOMOUS,
            Capabilities: []string{"natural-language", "reasoning"},
        },
    })
    
    // Use the agent...
}
```

### Python Bindings

To use HMS-AGT in Python:

```python
import grpc
from hms.agt.v1 import agent_pb2, agent_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = agent_pb2_grpc.AgentServiceStub(channel)
        
        # Create an agent
        response = stub.CreateAgent(agent_pb2.CreateAgentRequest(
            agent=agent_pb2.Agent(
                name="Test Agent",
                type=agent_pb2.AgentType.AUTONOMOUS,
                capabilities=["natural-language", "reasoning"]
            )
        ))
        
        # Use the agent...

if __name__ == '__main__':
    run()
```

### Rust Bindings

To use HMS-AGT in Rust:

```rust
use hms_agt::v1::{Agent, AgentType, CreateAgentRequest};
use tonic::Request;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = hms_agt::v1::agent_service_client::AgentServiceClient::connect("http://localhost:50051").await?;
    
    // Create an agent
    let request = Request::new(CreateAgentRequest {
        agent: Some(Agent {
            name: "Test Agent".to_string(),
            type_: AgentType::Autonomous as i32,
            capabilities: vec!["natural-language".to_string(), "reasoning".to_string()],
            ..Default::default()
        }),
    });
    
    let response = client.create_agent(request).await?;
    println!("RESPONSE={:?}", response);
    
    // Use the agent...
    
    Ok(())
}
```

## Testing

### Unit Tests

Unit tests for each language binding can be found in the respective language directories:

- Go: `ffi/proto/hms-ffi-protos/gen/go/tests/agt_test.go`
- Python: `ffi/proto/hms-ffi-protos/gen/python/tests/test_agt.py`
- Rust: `ffi/proto/hms-ffi-protos/gen/rust/tests/agt_test.rs`

### Integration Tests

Integration tests that verify cross-language interoperability:

- `ffi/proto/hms-ffi-protos/tests/integration/test_agt_agent.py`

## Implementation Plan

HMS-AGT FFI implementation is part of Phase 1 (Critical Path) with target completion in 2 weeks.

### Binding Generation

To generate language bindings:

```bash
cd ffi/proto/hms-ffi-protos
./generate-bindings.sh --component=agt --languages=go,python,rust,typescript
```

### Testing

To run tests for HMS-AGT:

```bash
cd ffi/proto/hms-ffi-protos
./run-tests.sh --component=agt
```

## API Reference

### Common Types

#### Agent

```protobuf
message Agent {
  string id = 1;
  string name = 2;
  AgentType type = 3;
  repeated string capabilities = 4;
  AgentState state = 5;
  map<string, string> metadata = 6;
  AgentSettings settings = 7;
}

enum AgentType {
  AGENT_TYPE_UNSPECIFIED = 0;
  AGENT_TYPE_AUTONOMOUS = 1;
  AGENT_TYPE_ASSISTIVE = 2;
  AGENT_TYPE_SUPERVISED = 3;
}

enum AgentState {
  AGENT_STATE_UNSPECIFIED = 0;
  AGENT_STATE_INITIALIZING = 1;
  AGENT_STATE_READY = 2;
  AGENT_STATE_RUNNING = 3;
  AGENT_STATE_PAUSED = 4;
  AGENT_STATE_ERROR = 5;
  AGENT_STATE_TERMINATED = 6;
}
```

#### Capability

```protobuf
message Capability {
  string id = 1;
  string name = 2;
  string description = 3;
  repeated string required_permissions = 4;
  map<string, string> parameters = 5;
  bool requires_authorization = 6;
}
```

#### Tool

```protobuf
message Tool {
  string id = 1;
  string name = 2;
  string description = 3;
  ToolType type = 4;
  repeated string required_capabilities = 5;
  ToolSchema schema = 6;
  map<string, string> metadata = 7;
}

enum ToolType {
  TOOL_TYPE_UNSPECIFIED = 0;
  TOOL_TYPE_FUNCTION = 1;
  TOOL_TYPE_SERVICE = 2;
  TOOL_TYPE_BROWSER = 3;
  TOOL_TYPE_SYSTEM = 4;
  TOOL_TYPE_CUSTOM = 5;
}
```

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2023-05-05 | 0.1.0 | Initial FFI documentation |
| 2023-05-05 | 0.1.1 | Added proto files: agent.proto, capability.proto, lifecycle.proto, tool.proto |