# HMS-AGX FFI Documentation

## Overview

The HMS-AGX (Agent Execution) component provides execution environments and runtime support for agents in the HMS system. This document details the Foreign Function Interface (FFI) implementation for HMS-AGX, allowing integration with various programming languages.

## Proto Definitions

HMS-AGX defines the following protocol buffer files:

- `execution.proto`: Defines agent execution environments and operations
- `runtime.proto`: Defines runtime support for agent execution
- `environment.proto`: Defines environment configurations for agent execution

These files are located in `ffi/proto/hms-ffi-protos/hms/agx/v1/`.

## Service Interfaces

### ExecutionService

The main service for agent execution:

```protobuf
service ExecutionService {
  // Execute an agent action
  rpc ExecuteAction(ExecuteActionRequest) returns (ExecuteActionResponse);
  
  // Execute an agent action and stream results
  rpc StreamExecuteAction(ExecuteActionRequest) returns (stream ExecuteActionEvent);
  
  // Cancel a running execution
  rpc CancelExecution(CancelExecutionRequest) returns (CancelExecutionResponse);
  
  // Get execution status
  rpc GetExecutionStatus(GetExecutionStatusRequest) returns (GetExecutionStatusResponse);
  
  // List executions
  rpc ListExecutions(ListExecutionsRequest) returns (ListExecutionsResponse);
}
```

### RuntimeService

Service for managing agent runtime:

```protobuf
service RuntimeService {
  // Allocate resources for agent execution
  rpc AllocateResources(AllocateResourcesRequest) returns (AllocateResourcesResponse);
  
  // Release allocated resources
  rpc ReleaseResources(ReleaseResourcesRequest) returns (ReleaseResourcesResponse);
  
  // Get runtime metrics
  rpc GetRuntimeMetrics(GetRuntimeMetricsRequest) returns (GetRuntimeMetricsResponse);
  
  // Scale runtime resources
  rpc ScaleResources(ScaleResourcesRequest) returns (ScaleResourcesResponse);
  
  // Configure runtime settings
  rpc ConfigureRuntime(ConfigureRuntimeRequest) returns (ConfigureRuntimeResponse);
}
```

### EnvironmentService

Service for managing execution environments:

```protobuf
service EnvironmentService {
  // Create an execution environment
  rpc CreateEnvironment(CreateEnvironmentRequest) returns (CreateEnvironmentResponse);
  
  // Delete an execution environment
  rpc DeleteEnvironment(DeleteEnvironmentRequest) returns (DeleteEnvironmentResponse);
  
  // Update an environment
  rpc UpdateEnvironment(UpdateEnvironmentRequest) returns (UpdateEnvironmentResponse);
  
  // Get environment information
  rpc GetEnvironment(GetEnvironmentRequest) returns (GetEnvironmentResponse);
  
  // List environments
  rpc ListEnvironments(ListEnvironmentsRequest) returns (ListEnvironmentsResponse);
  
  // Check environment health
  rpc CheckEnvironmentHealth(CheckEnvironmentHealthRequest) returns (CheckEnvironmentHealthResponse);
}
```

## Language Bindings

### Go Bindings

To use HMS-AGX in Go:

```go
import (
    agxpb "github.com/hardisonco/hms/gen/go/hms/agx/v1"
    "google.golang.org/grpc"
)

func main() {
    conn, err := grpc.Dial("localhost:50052", grpc.WithInsecure())
    if err != nil {
        log.Fatalf("Failed to connect: %v", err)
    }
    defer conn.Close()
    
    client := agxpb.NewExecutionServiceClient(conn)
    
    // Execute an agent action
    resp, err := client.ExecuteAction(context.Background(), &agxpb.ExecuteActionRequest{
        AgentId: "agent-001",
        Action: &agxpb.Action{
            Name: "process_text",
            Parameters: map[string]string{
                "text": "Hello, world!",
            },
        },
        Environment: "default",
    })
    
    // Use the response...
}
```

### Python Bindings

To use HMS-AGX in Python:

```python
import grpc
from hms.agx.v1 import execution_pb2, execution_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = execution_pb2_grpc.ExecutionServiceStub(channel)
        
        # Execute an agent action
        response = stub.ExecuteAction(execution_pb2.ExecuteActionRequest(
            agent_id="agent-001",
            action=execution_pb2.Action(
                name="process_text",
                parameters={"text": "Hello, world!"}
            ),
            environment="default"
        ))
        
        # Use the response...

if __name__ == '__main__':
    run()
```

### Rust Bindings

To use HMS-AGX in Rust:

```rust
use hms_agx::v1::{Action, ExecuteActionRequest};
use tonic::Request;
use std::collections::HashMap;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = hms_agx::v1::execution_service_client::ExecutionServiceClient::connect("http://localhost:50052").await?;
    
    // Create parameters map
    let mut parameters = HashMap::new();
    parameters.insert("text".to_string(), "Hello, world!".to_string());
    
    // Execute an agent action
    let request = Request::new(ExecuteActionRequest {
        agent_id: "agent-001".to_string(),
        action: Some(Action {
            name: "process_text".to_string(),
            parameters,
            ..Default::default()
        }),
        environment: "default".to_string(),
        ..Default::default()
    });
    
    let response = client.execute_action(request).await?;
    println!("RESPONSE={:?}", response);
    
    // Use the response...
    
    Ok(())
}
```

## Testing

### Unit Tests

Unit tests for each language binding can be found in the respective language directories:

- Go: `ffi/proto/hms-ffi-protos/gen/go/tests/agx_test.go`
- Python: `ffi/proto/hms-ffi-protos/gen/python/tests/test_agx.py`
- Rust: `ffi/proto/hms-ffi-protos/gen/rust/tests/agx_test.rs`

### Integration Tests

Integration tests that verify cross-language interoperability:

- `ffi/proto/hms-ffi-protos/tests/integration/test_agx_execution.py`

## Implementation Plan

HMS-AGX FFI implementation is part of Phase 1 (Critical Path) with target completion in 2 weeks.

### Binding Generation

To generate language bindings:

```bash
cd ffi/proto/hms-ffi-protos
./generate-bindings.sh --component=agx --languages=go,python,rust,typescript
```

### Testing

To run tests for HMS-AGX:

```bash
cd ffi/proto/hms-ffi-protos
./run-tests.sh --component=agx
```

## API Reference

### Common Types

#### Action

```protobuf
message Action {
  string id = 1;
  string name = 2;
  map<string, string> parameters = 3;
  Timeout timeout = 4;
  ActionPriority priority = 5;
  repeated string required_capabilities = 6;
}

enum ActionPriority {
  ACTION_PRIORITY_UNSPECIFIED = 0;
  ACTION_PRIORITY_LOW = 1;
  ACTION_PRIORITY_NORMAL = 2;
  ACTION_PRIORITY_HIGH = 3;
  ACTION_PRIORITY_CRITICAL = 4;
}

message Timeout {
  uint32 seconds = 1;
}
```

#### Execution

```protobuf
message Execution {
  string id = 1;
  string agent_id = 2;
  Action action = 3;
  ExecutionStatus status = 4;
  google.protobuf.Timestamp start_time = 5;
  google.protobuf.Timestamp end_time = 6;
  ExecutionResult result = 7;
  ResourceUsage resource_usage = 8;
  string environment = 9;
}

enum ExecutionStatus {
  EXECUTION_STATUS_UNSPECIFIED = 0;
  EXECUTION_STATUS_PENDING = 1;
  EXECUTION_STATUS_RUNNING = 2;
  EXECUTION_STATUS_SUCCEEDED = 3;
  EXECUTION_STATUS_FAILED = 4;
  EXECUTION_STATUS_CANCELLED = 5;
  EXECUTION_STATUS_TIMEOUT = 6;
}

message ExecutionResult {
  oneof result {
    string text_result = 1;
    bytes binary_result = 2;
    string json_result = 3;
    Error error = 4;
  }
}

message Error {
  string code = 1;
  string message = 2;
  string details = 3;
}
```

#### Environment

```protobuf
message Environment {
  string id = 1;
  string name = 2;
  string description = 3;
  EnvironmentType type = 4;
  ResourceLimits resource_limits = 5;
  map<string, string> variables = 6;
  SecurityPolicy security_policy = 7;
  map<string, string> metadata = 8;
}

enum EnvironmentType {
  ENVIRONMENT_TYPE_UNSPECIFIED = 0;
  ENVIRONMENT_TYPE_CONTAINER = 1;
  ENVIRONMENT_TYPE_VIRTUAL_MACHINE = 2;
  ENVIRONMENT_TYPE_SERVERLESS = 3;
  ENVIRONMENT_TYPE_ISOLATED = 4;
  ENVIRONMENT_TYPE_SHARED = 5;
}

message ResourceLimits {
  uint32 cpu_cores = 1;
  uint32 memory_mb = 2;
  uint32 storage_mb = 3;
  uint32 network_bandwidth_mbps = 4;
}

message SecurityPolicy {
  bool allow_network_access = 1;
  bool allow_file_system_access = 2;
  repeated string allowed_domains = 3;
  repeated string allowed_file_paths = 4;
  repeated string allowed_capabilities = 5;
}
```

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2023-05-05 | 0.1.0 | Initial FFI documentation |
| 2023-05-05 | 0.1.1 | Added proto files: execution.proto, runtime.proto, environment.proto |