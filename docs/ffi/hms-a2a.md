# HMS-A2A FFI Documentation

## Overview

The HMS-A2A (Agent-to-Agent) component provides a framework for agent communication and coordination. This document details the Foreign Function Interface (FFI) implementation for HMS-A2A, allowing integration with various programming languages.

## Proto Definitions

HMS-A2A defines the following protocol buffer files:

- `agent.proto`: Defines agent identity, capabilities, and state
- `graph.proto`: Defines agent communication network structures
- `message.proto`: Defines message formats for agent communication
- `task.proto`: Defines task structures that agents can perform

These files are located in `ffi/proto/hms-ffi-protos/hms/a2a/v1/`.

## Service Interfaces

### AgentService

The main service for agent-to-agent communication:

```protobuf
service AgentService {
  // Register an agent with the system
  rpc Register(RegisterAgentRequest) returns (RegisterAgentResponse);
  
  // Deregister an agent from the system
  rpc Deregister(DeregisterAgentRequest) returns (DeregisterAgentResponse);
  
  // Send a message to another agent
  rpc SendMessage(SendMessageRequest) returns (SendMessageResponse);
  
  // Stream messages from the system to this agent
  rpc ReceiveMessages(ReceiveMessagesRequest) returns (stream Message);
  
  // Assign a task to an agent
  rpc AssignTask(AssignTaskRequest) returns (AssignTaskResponse);
  
  // Get the status of a task
  rpc GetTaskStatus(TaskStatusRequest) returns (TaskStatusResponse);
}
```

### GraphService

Service for managing the agent communication network:

```protobuf
service GraphService {
  // Create a new communication graph
  rpc CreateGraph(CreateGraphRequest) returns (CreateGraphResponse);
  
  // Add an agent to a graph
  rpc AddAgentToGraph(AddAgentRequest) returns (AddAgentResponse);
  
  // Remove an agent from a graph
  rpc RemoveAgentFromGraph(RemoveAgentRequest) returns (RemoveAgentResponse);
  
  // Add a connection between two agents
  rpc AddConnection(AddConnectionRequest) returns (AddConnectionResponse);
  
  // Remove a connection between two agents
  rpc RemoveConnection(RemoveConnectionRequest) returns (RemoveConnectionResponse);
  
  // Get the current state of a graph
  rpc GetGraphState(GraphStateRequest) returns (GraphStateResponse);
}
```

## Language Bindings

### Go Bindings

To use HMS-A2A in Go:

```go
import (
    a2apb "github.com/hardisonco/hms/gen/go/hms/a2a/v1"
    "google.golang.org/grpc"
)

func main() {
    conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
    if err != nil {
        log.Fatalf("Failed to connect: %v", err)
    }
    defer conn.Close()
    
    client := a2apb.NewAgentServiceClient(conn)
    
    // Register an agent
    resp, err := client.Register(context.Background(), &a2apb.RegisterAgentRequest{
        Agent: &a2apb.Agent{
            Id: "agent-001",
            Name: "Test Agent",
            Capabilities: []string{"text-processing", "data-analysis"},
        },
    })
    
    // Use the agent...
}
```

### Python Bindings

To use HMS-A2A in Python:

```python
import grpc
from hms.a2a.v1 import agent_pb2, agent_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = agent_pb2_grpc.AgentServiceStub(channel)
        
        # Register an agent
        response = stub.Register(agent_pb2.RegisterAgentRequest(
            agent=agent_pb2.Agent(
                id="agent-001",
                name="Test Agent",
                capabilities=["text-processing", "data-analysis"]
            )
        ))
        
        # Use the agent...

if __name__ == '__main__':
    run()
```

### Rust Bindings

To use HMS-A2A in Rust:

```rust
use hms_a2a::v1::{Agent, RegisterAgentRequest};
use tonic::Request;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = hms_a2a::v1::agent_service_client::AgentServiceClient::connect("http://localhost:50051").await?;
    
    // Register an agent
    let request = Request::new(RegisterAgentRequest {
        agent: Some(Agent {
            id: "agent-001".to_string(),
            name: "Test Agent".to_string(),
            capabilities: vec!["text-processing".to_string(), "data-analysis".to_string()],
            ..Default::default()
        }),
    });
    
    let response = client.register(request).await?;
    println!("RESPONSE={:?}", response);
    
    // Use the agent...
    
    Ok(())
}
```

## Testing

### Unit Tests

Unit tests for each language binding can be found in the respective language directories:

- Go: `ffi/proto/hms-ffi-protos/gen/go/tests/a2a_test.go`
- Python: `ffi/proto/hms-ffi-protos/gen/python/tests/test_a2a.py`
- Rust: `ffi/proto/hms-ffi-protos/gen/rust/tests/a2a_test.rs`

### Integration Tests

Integration tests that verify cross-language interoperability:

- `ffi/proto/hms-ffi-protos/tests/integration/test_a2a_agent.py`

## Implementation Plan

HMS-A2A FFI implementation is part of Phase 1 (Critical Path) with target completion in 2 weeks.

### Binding Generation

To generate language bindings:

```bash
cd ffi/proto/hms-ffi-protos
./generate-bindings.sh --component=a2a --languages=go,python,rust,typescript
```

### Testing

To run tests for HMS-A2A:

```bash
cd ffi/proto/hms-ffi-protos
./run-tests.sh --component=a2a
```

## API Reference

### Common Types

#### Agent

```protobuf
message Agent {
  string id = 1;
  string name = 2;
  repeated string capabilities = 3;
  AgentState state = 4;
  map<string, string> metadata = 5;
}

enum AgentState {
  AGENT_STATE_UNSPECIFIED = 0;
  AGENT_STATE_IDLE = 1;
  AGENT_STATE_BUSY = 2;
  AGENT_STATE_OFFLINE = 3;
}
```

#### Message

```protobuf
message Message {
  string id = 1;
  string sender_id = 2;
  string recipient_id = 3;
  MessageType type = 4;
  bytes content = 5;
  google.protobuf.Timestamp created_at = 6;
  map<string, string> metadata = 7;
}

enum MessageType {
  MESSAGE_TYPE_UNSPECIFIED = 0;
  MESSAGE_TYPE_TEXT = 1;
  MESSAGE_TYPE_JSON = 2;
  MESSAGE_TYPE_BINARY = 3;
  MESSAGE_TYPE_TASK = 4;
}
```

#### Task

```protobuf
message Task {
  string id = 1;
  string title = 2;
  string description = 3;
  string assignee_id = 4;
  string assigner_id = 5;
  TaskPriority priority = 6;
  TaskStatus status = 7;
  google.protobuf.Timestamp created_at = 8;
  google.protobuf.Timestamp updated_at = 9;
  google.protobuf.Duration deadline = 10;
  map<string, string> metadata = 11;
}

enum TaskPriority {
  TASK_PRIORITY_UNSPECIFIED = 0;
  TASK_PRIORITY_LOW = 1;
  TASK_PRIORITY_MEDIUM = 2;
  TASK_PRIORITY_HIGH = 3;
  TASK_PRIORITY_CRITICAL = 4;
}

enum TaskStatus {
  TASK_STATUS_UNSPECIFIED = 0;
  TASK_STATUS_PENDING = 1;
  TASK_STATUS_IN_PROGRESS = 2;
  TASK_STATUS_COMPLETED = 3;
  TASK_STATUS_FAILED = 4;
  TASK_STATUS_CANCELLED = 5;
}
```

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2023-05-05 | 0.1.0 | Initial FFI documentation |