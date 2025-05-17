# HMS Foreign Function Interface (FFI) Documentation

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Getting Started](#3-getting-started)
4. [Core Concepts](#4-core-concepts)
5. [Language-Specific Guides](#5-language-specific-guides)
6. [Component Integration](#6-component-integration)
7. [Advanced Topics](#7-advanced-topics)
8. [Testing and Validation](#8-testing-and-validation)
9. [Deployment and Operations](#9-deployment-and-operations)
10. [Security Considerations](#10-security-considerations)
11. [Troubleshooting](#11-troubleshooting)
12. [Reference](#12-reference)
13. [Glossary](#13-glossary)

## 1. Introduction

The HMS Foreign Function Interface (FFI) system enables seamless cross-language function calls across the HMS ecosystem. This documentation provides comprehensive guidance for developers working with the FFI system.

### 1.1 Purpose and Scope

The HMS-FFI system is designed to:

- **Enable Cross-Language Communication**: Allow HMS components written in different languages to call each other's functions
- **Maintain Type Safety**: Ensure that function calls across language boundaries maintain type safety
- **Optimize Performance**: Provide high-performance cross-language function calls
- **Ensure Security**: Secure all cross-language communication
- **Facilitate Integration**: Make it easy to integrate components regardless of language

### 1.2 Supported Languages

The HMS-FFI system currently supports the following languages:

- **Go**: Used in HMS-SYS and HMS-EMR
- **Rust**: Used in HMS-CDF
- **Python**: Used in HMS-A2A, HMS-AGT, and HMS-ETL
- **JavaScript/TypeScript**: Used in HMS-ABC, HMS-AGX, and HMS-GOV
- **PHP**: Used in HMS-API
- **Ruby**: Used in HMS-ACH and HMS-ESR

### 1.3 Key Benefits

Using the HMS-FFI system provides these key benefits:

- **Language Freedom**: Choose the best language for each component
- **Consistent Interfaces**: Standardized interface definitions
- **Performance Optimization**: Transport selection based on deployment topology
- **Strong Type Safety**: Schema-validated function parameters and results
- **Comprehensive Security**: Authentication, authorization, and secure communication

## 2. Architecture Overview

The HMS-FFI system follows a layered architecture:

### 2.1 High-Level Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                     HMS Component Applications                     │
└───────────────────────────────────────────────────────────────────┘
                ▲                    ▲                    ▲
                │                    │                    │
┌───────────────┴───────┐  ┌────────┴───────────┐  ┌────┴───────────────┐
│  Language-Specific    │  │  Language-Specific  │  │  Language-Specific │
│  Bindings (Go)        │  │  Bindings (Rust)    │  │  Bindings (Python) │
└───────────────┬───────┘  └────────┬───────────┘  └────┬───────────────┘
                │                    │                    │
                ▼                    ▼                    ▼
┌───────────────────────────────────────────────────────────────────┐
│                       HMS-FFI Core Library                         │
├───────────────────────────────────────────────────────────────────┤
│  Interface Definition  │  Type System  │  Function Registry        │
├───────────────────────┴───────────────┴───────────────────────────┤
│  Serialization Layer   │  Transport Layer  │  Error Handling       │
└───────────────────────┬───────────────────┬───────────────────────┘
                         │                   │
      ┌──────────────────┘                   └───────────────────┐
      ▼                                                          ▼
┌─────────────────────────┐                          ┌────────────────────────┐
│   Local Communication    │                          │   Remote Communication  │
│   (Shared Memory/IPC)    │                          │   (Network/RPC)         │
└─────────────────────────┘                          └────────────────────────┘
```

### 2.2 Core Components

The HMS-FFI system consists of these core components:

#### 2.2.1 HMS-FFI Core Library

The central component providing core functionality:

- **Interface Definition**: Schema-driven interface definitions
- **Type System**: Cross-language type mapping
- **Function Registry**: Function registration and discovery
- **Serialization Layer**: Data conversion between languages
- **Transport Layer**: Communication between components
- **Error Handling**: Error propagation and translation

#### 2.2.2 Language-Specific Bindings

Bindings for each supported language:

- **Go Bindings**: Idiomatic Go integration
- **Rust Bindings**: Idiomatic Rust integration
- **Python Bindings**: Idiomatic Python integration
- **JavaScript/TypeScript Bindings**: Idiomatic JS/TS integration
- **PHP Bindings**: Idiomatic PHP integration
- **Ruby Bindings**: Idiomatic Ruby integration

#### 2.2.3 Communication Mechanisms

Transport mechanisms for different scenarios:

- **In-Process**: Direct memory access for same-process calls
- **Shared Memory**: Shared memory for cross-process calls
- **Local Sockets**: Unix domain sockets for local communication
- **gRPC**: High-performance RPC for network communication
- **WebSockets**: Bidirectional communication for web clients
- **REST**: HTTP-based communication for simple integrations

### 2.3 Integration with HMS Components

The HMS-FFI system integrates with all HMS components:

- **HMS-SYS** (Go): System operations and deployment management
- **HMS-CDF** (Rust): Computational debate framework
- **HMS-API** (PHP): API services
- **HMS-GOV** (JavaScript): Governance interface
- **HMS-EMR** (Go): Electronic medical record services
- **HMS-ACH** (Ruby): Automated clearing house
- **HMS-ESR** (Ruby): Electronic session reporting
- **HMS-ETL** (Python): Extract-transform-load pipelines
- **HMS-A2A** (Python): Agent-to-agent communication
- And other HMS components

## 3. Getting Started

### 3.1 Installation

Install the HMS-FFI system in your component:

#### 3.1.1 Go Installation

```bash
go get github.com/hardisonco/hms-ffi
```

#### 3.1.2 Rust Installation

```bash
cargo add hms-ffi
```

#### 3.1.3 Python Installation

```bash
pip install hms-ffi
```

#### 3.1.4 JavaScript/TypeScript Installation

```bash
npm install @hardisonco/hms-ffi
```

#### 3.1.5 PHP Installation

```bash
composer require hardisonco/hms-ffi
```

#### 3.1.6 Ruby Installation

```bash
gem install hms-ffi
```

### 3.2 Basic Configuration

Configure the HMS-FFI system in your component:

#### 3.2.1 Go Configuration

```go
package main

import (
    "github.com/hardisonco/hms-ffi"
)

func main() {
    // Configure FFI system
    config := ffi.Config{
        ServiceName: "hms-sys",
        RegistryURL: "http://registry:8080",
        SecurityConfig: ffi.SecurityConfig{
            TokenValidationURL: "http://auth:8080/validate",
            RequiredClaims:     []string{"sub", "role"},
        },
    }
    
    // Initialize FFI system
    if err := ffi.Initialize(config); err != nil {
        log.Fatalf("Failed to initialize FFI: %v", err)
    }
    
    // Register services
    RegisterServices()
    
    // Start application
    // ...
}
```

#### 3.2.2 Rust Configuration

```rust
use hms_ffi::Config;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Configure FFI system
    let config = Config {
        service_name: "hms-cdf".to_string(),
        registry_url: "http://registry:8080".to_string(),
        security_config: Some(SecurityConfig {
            token_validation_url: "http://auth:8080/validate".to_string(),
            required_claims: vec!["sub".to_string(), "role".to_string()],
        }),
        ..Default::default()
    };
    
    // Initialize FFI system
    hms_ffi::initialize(config)?;
    
    // Register services
    register_services()?;
    
    // Start application
    // ...
    
    Ok(())
}
```

### 3.3 Hello World Example

A simple example of using HMS-FFI:

#### 3.3.1 Service Definition (Protocol Buffer)

```protobuf
syntax = "proto3";

package hms.examples.v1;

service GreetingService {
  // Say hello to someone
  rpc SayHello(SayHelloRequest) returns (SayHelloResponse);
}

message SayHelloRequest {
  // Name to greet
  string name = 1;
}

message SayHelloResponse {
  // Greeting message
  string greeting = 1;
}
```

#### 3.3.2 Service Implementation (Go)

```go
package main

import (
    "context"
    "fmt"
    
    "github.com/hardisonco/hms-ffi"
)

// GreetingService implements the greeting service
type GreetingService struct{}

// SayHello says hello to the specified name
func (s *GreetingService) SayHello(ctx context.Context, name string) (string, error) {
    greeting := fmt.Sprintf("Hello, %s!", name)
    return greeting, nil
}

func RegisterServices() {
    // Create service
    service := &GreetingService{}
    
    // Register with FFI
    registry := ffi.GetServiceRegistry()
    registry.RegisterMethod("hms.examples.greeting", "SayHello", service.SayHello)
}
```

#### 3.3.3 Client Usage (Python)

```python
from hms_ffi import Client

# Create client
client = Client("hms.examples.greeting")

# Call service
response = client.call("SayHello", {"name": "World"})

# Print result
print(response["greeting"])  # Output: Hello, World!
```

## 4. Core Concepts

### 4.1 Service Definition

Services are defined using Protocol Buffers, which provide a language-neutral way to define interfaces:

```protobuf
service UserService {
  // Get user by ID
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  
  // Create a new user
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  
  // Update an existing user
  rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
  
  // Delete a user
  rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
}
```

### 4.2 Type System

The HMS-FFI type system provides consistent type mapping across languages:

| FFI Type       | Go                | Rust              | Python            | TypeScript        | PHP               | Ruby              |
|----------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|
| Null           | nil | Option::None | None | null | null | nil |
| Boolean        | bool | bool | bool | boolean | bool | TrueClass/FalseClass |
| Integer (32)   | int32 | i32 | int | number | int | Integer |
| Integer (64)   | int64 | i64 | int | bigint | int/string | Integer |
| Float (64)     | float64 | f64 | float | number | float | Float |
| String         | string | String | str | string | string | String |
| Bytes          | []byte | Vec<u8> | bytes | Uint8Array | string | String |
| Array          | slice/array | Vec<T> | list | Array<T> | array | Array |
| Object         | struct | struct | dict/class | interface | array/object | Hash/Object |
| Map            | map[K]V | HashMap<K,V> | dict | Map<K,V> | array | Hash |

### 4.3 Service Registry

The Service Registry manages the registration and discovery of services:

```go
// Register a service
registry.RegisterService(&ffi.ServiceDefinition{
    ServiceID:   "hms.sys.deployment",
    DisplayName: "HMS-SYS Deployment Service",
    Description: "Manages deployments across environments",
    Version:     "1.0.0",
    Methods:     methods,
})

// Discover a service
service, err := registry.GetService("hms.sys.deployment")
```

### 4.4 Function Call Patterns

The HMS-FFI system supports multiple function call patterns:

#### 4.4.1 Synchronous Calls

```go
// Go client making a synchronous call
result, err := client.Call(ctx, "GetUser", map[string]interface{}{
    "user_id": "12345",
})
```

#### 4.4.2 Asynchronous Calls

```typescript
// TypeScript client making an asynchronous call
const result = await client.callAsync("CreateUser", {
    name: "John Doe",
    email: "john@example.com",
});
```

#### 4.4.3 Streaming Calls

```python
# Python client making a streaming call
for result in client.stream("GetUserUpdates", {"user_id": "12345"}):
    print(f"Update: {result}")
```

#### 4.4.4 Pub/Sub Calls

```ruby
# Ruby client subscribing to events
client.subscribe("user.created") do |event|
  puts "New user created: #{event['user_id']}"
end

# Ruby client publishing events
client.publish("user.created", { user_id: "12345" })
```

### 4.5 Error Handling

Errors are propagated across language boundaries with appropriate context:

```go
// Go error handling
func (s *UserService) GetUser(ctx context.Context, userID string) (*User, error) {
    user, err := s.repository.GetUser(userID)
    if err != nil {
        if errors.Is(err, repository.ErrUserNotFound) {
            return nil, ffi.NewError(ffi.ErrorCodeNotFound, "User not found", map[string]string{
                "user_id": userID,
            })
        }
        return nil, ffi.NewError(ffi.ErrorCodeInternal, "Failed to get user", nil)
    }
    return user, nil
}
```

```python
# Python error handling
try:
    user = client.call("GetUser", {"user_id": "invalid"})
except FFIError as e:
    if e.code == ErrorCode.NOT_FOUND:
        print(f"User not found: {e.details['user_id']}")
    else:
        print(f"Error: {e.message}")
```

## 5. Language-Specific Guides

### 5.1 Go Guide

#### 5.1.1 Installation and Setup

```bash
go get github.com/hardisonco/hms-ffi
```

#### 5.1.2 Service Definition

```go
// Define a service
type DeploymentService struct {
    // Service dependencies
    config   *Config
    executor *Executor
}

// Execute a deployment
func (s *DeploymentService) ExecuteDeployment(ctx context.Context, request *DeploymentRequest) (*DeploymentResponse, error) {
    // Implementation
}

// Register with FFI
func RegisterServices() {
    service := &DeploymentService{
        config:   LoadConfig(),
        executor: NewExecutor(),
    }
    
    registry := ffi.GetServiceRegistry()
    registry.RegisterMethod("hms.sys.deployment", "ExecuteDeployment", service.ExecuteDeployment)
}
```

#### 5.1.3 Client Usage

```go
// Create a client
client, err := ffi.NewClient("hms.cdf.debate")
if err != nil {
    log.Fatalf("Failed to create client: %v", err)
}

// Call a service
ctx := context.Background()
req := &DebateRequest{
    Topic: "AI Ethics",
}

var resp DebateResponse
err = client.Call(ctx, "CreateDebate", req, &resp)
if err != nil {
    log.Fatalf("Failed to call service: %v", err)
}

fmt.Printf("Created debate: %s\n", resp.DebateID)
```

#### 5.1.4 Error Handling

```go
// Return an error
if invalidInput {
    return nil, ffi.NewError(ffi.ErrorCodeInvalidArgument, "Invalid input", map[string]string{
        "field": "topic",
        "reason": "Topic cannot be empty",
    })
}

// Handle an error
if err != nil {
    if ffiErr, ok := ffi.AsError(err); ok {
        switch ffiErr.Code {
        case ffi.ErrorCodeNotFound:
            // Handle not found error
        case ffi.ErrorCodeInvalidArgument:
            // Handle invalid argument error
        default:
            // Handle other errors
        }
    } else {
        // Handle non-FFI error
    }
}
```

### 5.2 Rust Guide

#### 5.2.1 Installation and Setup

```bash
cargo add hms-ffi
```

#### 5.2.2 Service Definition

```rust
// Define a service
struct DebateService {
    // Service dependencies
    framework: DebateFramework,
}

impl DebateService {
    // Create a new debate
    fn create_debate(&self, topic: String, description: String) -> Result<Debate, Error> {
        // Implementation
    }
}

// Register with FFI
fn register_services() -> Result<(), Error> {
    let service = DebateService {
        framework: DebateFramework::new(),
    };
    
    let registry = ffi::get_service_registry();
    registry.register_method("hms.cdf.debate", "CreateDebate", service.create_debate)?;
    
    Ok(())
}
```

#### 5.2.3 Client Usage

```rust
// Create a client
let client = ffi::Client::new("hms.sys.deployment")?;

// Call a service
let request = DeploymentRequest {
    component_id: "hms-api".to_string(),
    version: "1.2.0".to_string(),
    environment: Environment::Staging,
};

let response: DeploymentResponse = client.call("ExecuteDeployment", &request)?;
println!("Deployment ID: {}", response.deployment_id);
```

#### 5.2.4 Error Handling

```rust
// Return an error
if invalid_input {
    return Err(ffi::Error::new(
        ffi::ErrorCode::InvalidArgument,
        "Invalid input".to_string(),
        Some(hashmap! {
            "field".to_string() => "topic".to_string(),
            "reason".to_string() => "Topic cannot be empty".to_string(),
        }),
    ));
}

// Handle an error
match client.call("ExecuteDeployment", &request) {
    Ok(response) => {
        // Process response
    }
    Err(e) => {
        match e.code() {
            ffi::ErrorCode::NotFound => {
                // Handle not found error
            }
            ffi::ErrorCode::InvalidArgument => {
                // Handle invalid argument error
            }
            _ => {
                // Handle other errors
            }
        }
    }
}
```

### 5.3 Python Guide

#### 5.3.1 Installation and Setup

```bash
pip install hms-ffi
```

#### 5.3.2 Service Definition

```python
# Define a service
class ETLService:
    def __init__(self):
        # Service dependencies
        self.pipeline_manager = PipelineManager()
    
    def execute_pipeline(self, pipeline_id, parameters):
        """Execute an ETL pipeline."""
        # Implementation
        execution = self.pipeline_manager.execute(pipeline_id, parameters)
        return {
            "execution_id": execution.id,
            "status": execution.status,
        }

# Register with FFI
def register_services():
    service = ETLService()
    
    registry = ffi.get_service_registry()
    registry.register_method("hms.etl.pipeline", "ExecutePipeline", service.execute_pipeline)
```

#### 5.3.3 Client Usage

```python
# Create a client
client = ffi.Client("hms.cdf.debate")

# Call a service
request = {
    "topic": "AI Ethics",
    "description": "Debate about ethical considerations in AI development",
}

response = client.call("CreateDebate", request)
print(f"Created debate: {response['debate_id']}")

# Async usage
async def create_debate_async():
    response = await client.call_async("CreateDebate", request)
    print(f"Created debate: {response['debate_id']}")
```

#### 5.3.4 Error Handling

```python
# Return an error
if invalid_input:
    raise ffi.Error(
        code=ffi.ErrorCode.INVALID_ARGUMENT,
        message="Invalid input",
        details={
            "field": "topic",
            "reason": "Topic cannot be empty",
        }
    )

# Handle an error
try:
    response = client.call("CreateDebate", request)
except ffi.Error as e:
    if e.code == ffi.ErrorCode.NOT_FOUND:
        # Handle not found error
        print(f"Not found: {e.details.get('resource_id')}")
    elif e.code == ffi.ErrorCode.INVALID_ARGUMENT:
        # Handle invalid argument error
        print(f"Invalid argument: {e.details.get('field')} - {e.details.get('reason')}")
    else:
        # Handle other errors
        print(f"Error: {e.message}")
```

### 5.4 JavaScript/TypeScript Guide

#### 5.4.1 Installation and Setup

```bash
npm install @hardisonco/hms-ffi
```

#### 5.4.2 Service Definition

```typescript
// Define a service
class PolicyService {
  private policyManager: PolicyManager;
  
  constructor() {
    // Service dependencies
    this.policyManager = new PolicyManager();
  }
  
  async createPolicy(name: string, description: string, rules: Rule[]): Promise<Policy> {
    // Implementation
    const policy = await this.policyManager.createPolicy(name, description, rules);
    return policy;
  }
}

// Register with FFI
function registerServices() {
  const service = new PolicyService();
  
  const registry = ffi.getServiceRegistry();
  registry.registerMethod("hms.gov.policy", "CreatePolicy", service.createPolicy.bind(service));
}
```

#### 5.4.3 Client Usage

```typescript
// Create a client
const client = new ffi.Client("hms.sys.deployment");

// Call a service
const request = {
  component_id: "hms-api",
  version: "1.2.0",
  environment: "staging",
};

try {
  const response = await client.call("ExecuteDeployment", request);
  console.log(`Deployment ID: ${response.deployment_id}`);
} catch (error) {
  console.error(`Error: ${error.message}`);
}

// Streaming usage
const stream = client.stream("GetDeploymentLogs", { deployment_id: "12345" });
for await (const log of stream) {
  console.log(`${log.timestamp}: ${log.message}`);
}
```

#### 5.4.4 Error Handling

```typescript
// Return an error
if (invalidInput) {
  throw new ffi.Error({
    code: ffi.ErrorCode.INVALID_ARGUMENT,
    message: "Invalid input",
    details: {
      field: "name",
      reason: "Name cannot be empty",
    },
  });
}

// Handle an error
try {
  const response = await client.call("CreatePolicy", request);
} catch (error) {
  if (error instanceof ffi.Error) {
    switch (error.code) {
      case ffi.ErrorCode.NOT_FOUND:
        // Handle not found error
        console.error(`Not found: ${error.details.resource_id}`);
        break;
      case ffi.ErrorCode.INVALID_ARGUMENT:
        // Handle invalid argument error
        console.error(`Invalid argument: ${error.details.field} - ${error.details.reason}`);
        break;
      default:
        // Handle other errors
        console.error(`Error: ${error.message}`);
    }
  } else {
    // Handle non-FFI error
    console.error(`Unexpected error: ${error}`);
  }
}
```

### 5.5 PHP Guide

#### 5.5.1 Installation and Setup

```bash
composer require hardisonco/hms-ffi
```

#### 5.5.2 Service Definition

```php
// Define a service
class ApiService
{
    private $userRepository;
    
    public function __construct()
    {
        // Service dependencies
        $this->userRepository = new UserRepository();
    }
    
    public function getUser(string $userId): array
    {
        // Implementation
        $user = $this->userRepository->findById($userId);
        
        if (!$user) {
            throw new FFI\Error(
                FFI\ErrorCode::NOT_FOUND,
                "User not found",
                ["user_id" => $userId]
            );
        }
        
        return [
            "id" => $user->getId(),
            "name" => $user->getName(),
            "email" => $user->getEmail(),
        ];
    }
}

// Register with FFI
function registerServices()
{
    $service = new ApiService();
    
    $registry = FFI\ServiceRegistry::getInstance();
    $registry->registerMethod("hms.api.user", "GetUser", [$service, "getUser"]);
}
```

#### 5.5.3 Client Usage

```php
// Create a client
$client = new FFI\Client("hms.etl.pipeline");

// Call a service
try {
    $response = $client->call("ExecutePipeline", [
        "pipeline_id" => "data-import",
        "parameters" => [
            "source" => "s3://data-bucket/input.csv",
            "destination" => "database",
        ],
    ]);
    
    echo "Execution ID: " . $response["execution_id"] . "\n";
} catch (FFI\Error $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
```

#### 5.5.4 Error Handling

```php
// Return an error
if ($invalidInput) {
    throw new FFI\Error(
        FFI\ErrorCode::INVALID_ARGUMENT,
        "Invalid input",
        [
            "field" => "pipeline_id",
            "reason" => "Pipeline ID cannot be empty",
        ]
    );
}

// Handle an error
try {
    $response = $client->call("ExecutePipeline", $request);
} catch (FFI\Error $e) {
    switch ($e->getCode()) {
        case FFI\ErrorCode::NOT_FOUND:
            // Handle not found error
            echo "Not found: " . $e->getDetails()["resource_id"] . "\n";
            break;
        case FFI\ErrorCode::INVALID_ARGUMENT:
            // Handle invalid argument error
            echo "Invalid argument: " . $e->getDetails()["field"] . " - " . $e->getDetails()["reason"] . "\n";
            break;
        default:
            // Handle other errors
            echo "Error: " . $e->getMessage() . "\n";
    }
}
```

### 5.6 Ruby Guide

#### 5.6.1 Installation and Setup

```bash
gem install hms-ffi
```

#### 5.6.2 Service Definition

```ruby
# Define a service
class TransactionService
  def initialize
    # Service dependencies
    @processor = TransactionProcessor.new
  end
  
  def process_transaction(type, amount, source_account_id, destination_account_id, description)
    # Implementation
    transaction = @processor.process(
      type: type,
      amount: amount,
      source_account_id: source_account_id,
      destination_account_id: destination_account_id,
      description: description
    )
    
    {
      transaction_id: transaction.id,
      status: transaction.status,
      confirmation_code: transaction.confirmation_code
    }
  end
end

# Register with FFI
def register_services
  service = TransactionService.new
  
  registry = HMS::FFI::ServiceRegistry.instance
  registry.register_method("hms.ach.transaction", "ProcessTransaction", service.method(:process_transaction))
end
```

#### 5.6.3 Client Usage

```ruby
# Create a client
client = HMS::FFI::Client.new("hms.ach.transaction")

# Call a service
begin
  response = client.call("ProcessTransaction", {
    type: "TRANSFER",
    amount: {
      currency_code: "USD",
      amount: 10000  # $100.00
    },
    source_account_id: "account123",
    destination_account_id: "account456",
    description: "Monthly transfer"
  })
  
  puts "Transaction ID: #{response[:transaction_id]}"
rescue HMS::FFI::Error => e
  puts "Error: #{e.message}"
end
```

#### 5.6.4 Error Handling

```ruby
# Return an error
if invalid_input
  raise HMS::FFI::Error.new(
    code: HMS::FFI::ErrorCode::INVALID_ARGUMENT,
    message: "Invalid input",
    details: {
      field: "amount",
      reason: "Amount must be positive"
    }
  )
end

# Handle an error
begin
  response = client.call("ProcessTransaction", request)
rescue HMS::FFI::Error => e
  case e.code
  when HMS::FFI::ErrorCode::NOT_FOUND
    # Handle not found error
    puts "Not found: #{e.details[:resource_id]}"
  when HMS::FFI::ErrorCode::INVALID_ARGUMENT
    # Handle invalid argument error
    puts "Invalid argument: #{e.details[:field]} - #{e.details[:reason]}"
  else
    # Handle other errors
    puts "Error: #{e.message}"
  end
end
```

## 6. Component Integration

### 6.1 HMS-SYS Integration

HMS-SYS provides system operations and deployment management:

```go
// Register HMS-SYS services
func RegisterServices() {
    // Create service implementations
    deploymentSvc := &DeploymentService{
        config:   LoadConfig(),
        executor: NewExecutor(),
    }
    
    monitoringSvc := &MonitoringService{
        metrics: NewMetricsCollector(),
    }
    
    // Register with FFI
    registry := ffi.GetServiceRegistry()
    
    // Register deployment service methods
    registry.RegisterMethod("hms.sys.deployment", "ExecuteDeployment", deploymentSvc.ExecuteDeployment)
    registry.RegisterMethod("hms.sys.deployment", "GetDeploymentStatus", deploymentSvc.GetDeploymentStatus)
    registry.RegisterMethod("hms.sys.deployment", "CancelDeployment", deploymentSvc.CancelDeployment)
    
    // Register monitoring service methods
    registry.RegisterMethod("hms.sys.monitoring", "GetSystemHealth", monitoringSvc.GetSystemHealth)
    registry.RegisterMethod("hms.sys.monitoring", "GetMetrics", monitoringSvc.GetMetrics)
}
```

### 6.2 HMS-CDF Integration

HMS-CDF provides the computational debate framework:

```rust
// Register HMS-CDF services
fn register_services() -> Result<(), Error> {
    // Create service implementations
    let debate_svc = DebateService::new()?;
    let policy_svc = PolicyService::new()?;
    
    // Register with FFI
    let registry = ffi::get_service_registry();
    
    // Register debate service methods
    registry.register_method("hms.cdf.debate", "CreateDebate", debate_svc.create_debate)?;
    registry.register_method("hms.cdf.debate", "AddPosition", debate_svc.add_position)?;
    registry.register_method("hms.cdf.debate", "AddEvidence", debate_svc.add_evidence)?;
    registry.register_method("hms.cdf.debate", "EvaluateDebate", debate_svc.evaluate_debate)?;
    
    // Register policy service methods
    registry.register_method("hms.cdf.policy", "EvaluatePolicy", policy_svc.evaluate_policy)?;
    
    Ok(())
}
```

### 6.3 HMS-API Integration

HMS-API provides API services:

```php
// Register HMS-API services
function registerServices()
{
    // Create service implementations
    $userSvc = new UserService();
    $authSvc = new AuthenticationService();
    
    // Register with FFI
    $registry = FFI\ServiceRegistry::getInstance();
    
    // Register user service methods
    $registry->registerMethod("hms.api.user", "GetUser", [$userSvc, "getUser"]);
    $registry->registerMethod("hms.api.user", "CreateUser", [$userSvc, "createUser"]);
    $registry->registerMethod("hms.api.user", "UpdateUser", [$userSvc, "updateUser"]);
    $registry->registerMethod("hms.api.user", "DeleteUser", [$userSvc, "deleteUser"]);
    
    // Register authentication service methods
    $registry->registerMethod("hms.api.authentication", "Authenticate", [$authSvc, "authenticate"]);
    $registry->registerMethod("hms.api.authentication", "ValidateToken", [$authSvc, "validateToken"]);
    $registry->registerMethod("hms.api.authentication", "RefreshToken", [$authSvc, "refreshToken"]);
}
```

### 6.4 HMS-GOV Integration

HMS-GOV provides the governance interface:

```typescript
// Register HMS-GOV services
function registerServices() {
  // Create service implementations
  const policySvc = new PolicyService();
  const complianceSvc = new ComplianceService();
  
  // Register with FFI
  const registry = ffi.getServiceRegistry();
  
  // Register policy service methods
  registry.registerMethod("hms.gov.policy", "CreatePolicy", policySvc.createPolicy.bind(policySvc));
  registry.registerMethod("hms.gov.policy", "GetPolicy", policySvc.getPolicy.bind(policySvc));
  registry.registerMethod("hms.gov.policy", "UpdatePolicy", policySvc.updatePolicy.bind(policySvc));
  registry.registerMethod("hms.gov.policy", "DeletePolicy", policySvc.deletePolicy.bind(policySvc));
  
  // Register compliance service methods
  registry.registerMethod("hms.gov.compliance", "CheckCompliance", complianceSvc.checkCompliance.bind(complianceSvc));
}
```

### 6.5 Cross-Component Integration

Example of cross-component integration between HMS-SYS and HMS-CDF:

```go
// HMS-SYS code calling HMS-CDF
func (s *PolicyService) EvaluateDeploymentPolicy(ctx context.Context, deploymentID string) (*PolicyEvaluation, error) {
    // Get deployment details
    deployment, err := s.deploymentRepository.GetDeployment(deploymentID)
    if err != nil {
        return nil, fmt.Errorf("failed to get deployment: %w", err)
    }
    
    // Prepare policy evaluation request
    resource := map[string]interface{}{
        "type": "Deployment",
        "id": deployment.ID,
        "environment": deployment.Environment,
        "component": deployment.ComponentID,
        "version": deployment.Version,
    }
    
    // Create FFI client for HMS-CDF policy service
    client, err := ffi.NewClient("hms.cdf.policy")
    if err != nil {
        return nil, fmt.Errorf("failed to create CDF client: %w", err)
    }
    
    // Call HMS-CDF to evaluate policy
    var evaluation PolicyEvaluation
    err = client.Call(ctx, "EvaluatePolicy", map[string]interface{}{
        "policy_id": "deployment-policy",
        "resource": resource,
    }, &evaluation)
    
    if err != nil {
        return nil, fmt.Errorf("policy evaluation failed: %w", err)
    }
    
    return &evaluation, nil
}
```

## 7. Advanced Topics

### 7.1 Streaming Data

Streaming enables the transfer of large datasets or continuous data:

```go
// Go streaming server
func (s *LogService) StreamLogs(ctx context.Context, request *LogRequest, stream ffi.ServerStream) error {
    // Set up log source
    source, err := s.getLogSource(request.Source)
    if err != nil {
        return fmt.Errorf("failed to get log source: %w", err)
    }
    
    // Stream logs
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case log, ok := <-source.Logs():
            if !ok {
                return nil // End of stream
            }
            
            // Send log entry to client
            err := stream.Send(log)
            if err != nil {
                return fmt.Errorf("failed to send log: %w", err)
            }
        }
    }
}
```

```typescript
// TypeScript streaming client
async function streamLogs() {
  const client = new ffi.Client("hms.sys.logging");
  
  const stream = client.stream("StreamLogs", {
    source: "app-logs",
    filter: "level=error",
    tail: true,
  });
  
  for await (const log of stream) {
    console.log(`${log.timestamp} [${log.level}] ${log.message}`);
    
    // Process until we decide to stop
    if (shouldStop()) {
      await stream.close();
      break;
    }
  }
}
```

### 7.2 Binary Data Handling

Efficient handling of binary data:

```rust
// Rust binary data handling
fn process_image(&self, image_data: Vec<u8>) -> Result<ImageMetadata, Error> {
    // Process binary image data
    let image = image::load_from_memory(&image_data)
        .map_err(|e| Error::new(ErrorCode::InvalidArgument, format!("Invalid image data: {}", e), None))?;
    
    // Extract metadata
    let metadata = ImageMetadata {
        width: image.width(),
        height: image.height(),
        format: format!("{:?}", image.color()),
        size_bytes: image_data.len() as u64,
    };
    
    Ok(metadata)
}
```

```python
# Python binary data handling
def upload_file(self, file_name, file_data):
    """Upload a file to storage."""
    # Handle binary file data
    try:
        # Upload to storage
        location = self.storage.put_object(
            bucket="uploads",
            key=file_name,
            body=file_data
        )
        
        # Return file metadata
        return {
            "file_name": file_name,
            "size_bytes": len(file_data),
            "content_type": self._detect_content_type(file_name),
            "location": location,
        }
    except Exception as e:
        raise ffi.Error(
            code=ffi.ErrorCode.INTERNAL,
            message=f"Failed to upload file: {str(e)}",
            details={"file_name": file_name}
        )
```

### 7.3 Performance Optimization

Techniques for optimizing FFI performance:

#### 7.3.1 Zero-Copy

```go
// Go zero-copy optimization
func (s *DataService) ProcessLargeData(ctx context.Context, data []byte) ([]byte, error) {
    // Use ffi.WithZeroCopy to avoid copying large data
    result, err := ffi.WithZeroCopy(func() ([]byte, error) {
        // Process data in place
        // ...
        return processedData, nil
    }, data)
    
    return result, err
}
```

#### 7.3.2 Connection Pooling

```ruby
# Ruby connection pooling
HMS::FFI.configure do |config|
  # Configure connection pool
  config.connection_pool = {
    # Maximum number of connections in the pool
    max_size: 20,
    
    # Minimum number of connections to keep open
    min_size: 5,
    
    # Maximum idle time before a connection is closed
    max_idle_time: 60,
    
    # Maximum time to wait for a connection
    checkout_timeout: 5
  }
end
```

#### 7.3.3 Batching

```typescript
// TypeScript request batching
async function processBatch(items: Item[]): Promise<ProcessResult[]> {
  const client = new ffi.Client("hms.etl.processor");
  
  // Process items in a single batch call
  const results = await client.call("ProcessBatch", { items });
  
  return results.processed_items;
}
```

### 7.4 Security Hardening

Advanced security techniques:

#### 7.4.1 Mutual TLS

```go
// Go mTLS configuration
func configureMTLS() *tls.Config {
    // Load certificates
    cert, err := tls.LoadX509KeyPair("client.crt", "client.key")
    if err != nil {
        log.Fatalf("Failed to load client certificates: %v", err)
    }
    
    // Load CA certificate
    caCert, err := os.ReadFile("ca.crt")
    if err != nil {
        log.Fatalf("Failed to load CA certificate: %v", err)
    }
    
    caCertPool := x509.NewCertPool()
    caCertPool.AppendCertsFromPEM(caCert)
    
    // Create TLS configuration
    return &tls.Config{
        Certificates: []tls.Certificate{cert},
        RootCAs:      caCertPool,
        ClientAuth:   tls.RequireAndVerifyClientCert,
        ClientCAs:    caCertPool,
    }
}
```

#### 7.4.2 Fine-Grained Authorization

```php
// PHP fine-grained authorization
class AuthorizationService
{
    public function hasPermission(string $userId, string $resource, string $action): bool
    {
        // Get user roles and permissions
        $user = $this->userRepository->findById($userId);
        if (!$user) {
            return false;
        }
        
        $roles = $user->getRoles();
        
        // Check permissions for each role
        foreach ($roles as $role) {
            $permissions = $this->permissionRepository->findByRole($role);
            
            // Check if any permission grants access
            foreach ($permissions as $permission) {
                if ($this->matchesResource($permission->getResource(), $resource) &&
                    $this->matchesAction($permission->getAction(), $action)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    // Check if resource pattern matches resource
    private function matchesResource(string $pattern, string $resource): bool
    {
        // Implementation
    }
    
    // Check if action pattern matches action
    private function matchesAction(string $pattern, string $action): bool
    {
        // Implementation
    }
}
```

## 8. Testing and Validation

### 8.1 Unit Testing

Testing individual FFI components:

```go
// Go unit test for FFI service
func TestDeploymentService_ExecuteDeployment(t *testing.T) {
    // Create mock dependencies
    mockExecutor := &MockExecutor{}
    mockExecutor.On("Execute", mock.Anything, mock.Anything).Return(&Execution{
        ID:     "exec-123",
        Status: "CREATED",
    }, nil)
    
    // Create service with mocks
    service := &DeploymentService{
        executor: mockExecutor,
    }
    
    // Create test request
    req := &DeploymentRequest{
        ComponentID: "test-component",
        Version:     "1.0.0",
        Environment: "development",
    }
    
    // Call method
    resp, err := service.ExecuteDeployment(context.Background(), req)
    
    // Verify results
    assert.NoError(t, err)
    assert.NotNil(t, resp)
    assert.Equal(t, "exec-123", resp.DeploymentID)
    assert.Equal(t, "CREATED", resp.Status)
    
    // Verify mock was called
    mockExecutor.AssertExpectations(t)
}
```

### 8.2 Integration Testing

Testing cross-language function calls:

```python
# Python integration test for FFI client
def test_call_go_service():
    # Create client to Go service
    client = ffi.Client("hms.sys.deployment")
    
    # Create test request
    request = {
        "component_id": "test-component",
        "version": "1.0.0",
        "environment": "development",
    }
    
    # Call Go service
    response = client.call("ExecuteDeployment", request)
    
    # Verify response
    assert response is not None
    assert "deployment_id" in response
    assert "status" in response
    assert response["status"] == "CREATED"
```

### 8.3 Mock Services

Creating mock FFI services for testing:

```typescript
// TypeScript mock FFI service
class MockPolicyService {
  async createPolicy(name: string, description: string, rules: Rule[]): Promise<Policy> {
    // Return mock data
    return {
      id: "policy-123",
      name,
      description,
      rules,
      status: "ACTIVE",
      version: "1.0.0",
    };
  }
}

// Register mock service
function registerMockServices() {
  const mockService = new MockPolicyService();
  
  const registry = ffi.getServiceRegistry();
  registry.registerMethod("hms.gov.policy", "CreatePolicy", mockService.createPolicy.bind(mockService));
}
```

### 8.4 Performance Testing

Benchmarking FFI performance:

```go
// Go FFI benchmark
func BenchmarkFFICall(b *testing.B) {
    // Create client
    client, err := ffi.NewClient("hms.cdf.debate")
    if err != nil {
        b.Fatalf("Failed to create client: %v", err)
    }
    
    // Prepare request
    req := &DebateRequest{
        Topic:       "Benchmark Topic",
        Description: "Benchmark description",
    }
    
    // Reset timer
    b.ResetTimer()
    
    // Run benchmark
    for i := 0; i < b.N; i++ {
        var resp DebateResponse
        err := client.Call(context.Background(), "CreateDebate", req, &resp)
        if err != nil {
            b.Fatalf("Failed to call service: %v", err)
        }
    }
}
```

## 9. Deployment and Operations

### 9.1 Container Deployment

Deploying HMS-FFI in containers:

```dockerfile
# Dockerfile for HMS-SYS with FFI
FROM golang:1.21-alpine as builder

WORKDIR /app

# Copy and build the application
COPY . .
RUN go build -o hms-sys .

# Create production image
FROM alpine:3.18

WORKDIR /app

# Copy the built binary
COPY --from=builder /app/hms-sys /app/hms-sys

# Copy FFI configuration
COPY config/ffi.yaml /app/config/ffi.yaml

# Set environment variables
ENV HMS_FFI_REGISTRY_URL=http://registry:8080
ENV HMS_FFI_CONFIG_PATH=/app/config/ffi.yaml

# Expose ports
EXPOSE 8080

# Run the application
CMD ["/app/hms-sys"]
```

### 9.2 Kubernetes Deployment

Deploying HMS-FFI in Kubernetes:

```yaml
# Kubernetes deployment for HMS-FFI Registry
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hms-ffi-registry
  namespace: hms
  labels:
    app: hms-ffi-registry
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hms-ffi-registry
  template:
    metadata:
      labels:
        app: hms-ffi-registry
    spec:
      containers:
      - name: registry
        image: hardisonco/hms-ffi-registry:latest
        ports:
        - containerPort: 8080
        env:
        - name: HMS_FFI_STORAGE_TYPE
          value: "postgres"
        - name: HMS_FFI_DB_HOST
          valueFrom:
            secretKeyRef:
              name: hms-ffi-db
              key: host
        - name: HMS_FFI_DB_USER
          valueFrom:
            secretKeyRef:
              name: hms-ffi-db
              key: username
        - name: HMS_FFI_DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: hms-ffi-db
              key: password
        - name: HMS_FFI_DB_NAME
          valueFrom:
            secretKeyRef:
              name: hms-ffi-db
              key: database
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 15
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
```

### 9.3 Monitoring and Logging

Monitoring HMS-FFI:

```go
// Go FFI monitoring
func configureMonitoring() {
    // Configure metrics
    ffi.ConfigureMetrics(&ffi.MetricsConfig{
        Prometheus: &ffi.PrometheusConfig{
            Endpoint: "/metrics",
            Port:     9090,
        },
    })
    
    // Configure tracing
    ffi.ConfigureTracing(&ffi.TracingConfig{
        ServiceName:    "hms-sys",
        SamplingRate:   0.1,
        ExporterType:   "jaeger",
        ExporterConfig: map[string]string{
            "endpoint": "http://jaeger-collector:14268/api/traces",
        },
    })
    
    // Configure logging
    ffi.ConfigureLogging(&ffi.LoggingConfig{
        Level:        "info",
        Format:       "json",
        OutputPaths:  []string{"stdout", "/var/log/hms-sys.log"},
        ErrorOutput:  []string{"stderr", "/var/log/hms-sys-error.log"},
        InitialFields: map[string]interface{}{
            "service": "hms-sys",
            "version": "1.0.0",
        },
    })
}
```

### 9.4 Scaling and High Availability

Scaling HMS-FFI:

```yaml
# Scaling configuration for HMS-FFI Registry
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hms-ffi-registry
  namespace: hms
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hms-ffi-registry
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 10. Security Considerations

### 10.1 Authentication

Setting up authentication:

```go
// Go FFI authentication
func configureAuthentication() {
    // Configure authentication
    ffi.ConfigureAuthentication(&ffi.AuthConfig{
        TokenValidation: &ffi.TokenValidationConfig{
            Issuer:     "https://auth.hardisonco.com",
            Audience:   "hms-sys",
            JwksURL:    "https://auth.hardisonco.com/.well-known/jwks.json",
        },
        RequiredClaims: []string{"sub", "role"},
    })
}
```

### 10.2 Authorization

Setting up authorization:

```go
// Go FFI authorization
func configureAuthorization() {
    // Configure authorization
    ffi.ConfigureAuthorization(&ffi.AuthzConfig{
        PolicyFile: "config/authz.yaml",
        Mode:       "enforcing",
        DefaultDeny: true,
    })
}
```

```yaml
# Authorization policy file (authz.yaml)
policies:
  - service: "hms.sys.deployment"
    method: "ExecuteDeployment"
    allow_roles:
      - "admin"
      - "deployer"
    deny_roles:
      - "readonly"
    
  - service: "hms.sys.deployment"
    method: "GetDeploymentStatus"
    allow_roles:
      - "admin"
      - "deployer"
      - "readonly"
```

### 10.3 Secure Communication

Setting up secure communication:

```go
// Go FFI secure communication
func configureSecureCommunication() {
    // Load TLS certificates
    cert, err := tls.LoadX509KeyPair("cert.pem", "key.pem")
    if err != nil {
        log.Fatalf("Failed to load certificates: %v", err)
    }
    
    // Configure transport security
    ffi.ConfigureTransportSecurity(&ffi.TransportSecurityConfig{
        TLS: &ffi.TLSConfig{
            Enabled:      true,
            Certificates: []tls.Certificate{cert},
            MinVersion:   tls.VersionTLS13,
            CipherSuites: []uint16{
                tls.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
                tls.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
            },
        },
    })
}
```

### 10.4 Audit Logging

Setting up audit logging:

```go
// Go FFI audit logging
func configureAuditLogging() {
    // Configure audit logging
    ffi.ConfigureAuditLogging(&ffi.AuditConfig{
        Enabled:     true,
        LogRequests: true,
        LogResponses: true,
        SensitiveFields: []string{
            "password",
            "token",
            "secret",
        },
        OutputPath: "/var/log/hms-sys-audit.log",
    })
}
```

## 11. Troubleshooting

### 11.1 Common Issues

#### 11.1.1 Connection Issues

```
Problem: FFI client cannot connect to service
Error: "Failed to connect to service: connection refused"

Troubleshooting steps:
1. Check if the service is running
2. Verify network connectivity between client and service
3. Check firewall settings
4. Verify service registration with the registry
5. Check service URL and port

Solution:
- Ensure the service is running and registered
- Check network connectivity and firewall settings
- Verify the registry has the correct service information
```

#### 11.1.2 Serialization Issues

```
Problem: FFI call fails with serialization error
Error: "Failed to serialize parameters: field 'amount' has invalid type"

Troubleshooting steps:
1. Check the parameter types against the service schema
2. Verify that the client is using the correct schema version
3. Look for type mismatches (e.g., string vs. number)
4. Check for null values in required fields

Solution:
- Ensure parameter types match the schema
- Update client to use the correct schema version
- Fix type mismatches
- Provide values for all required fields
```

#### 11.1.3 Authorization Issues

```
Problem: FFI call fails with authorization error
Error: "Access denied: insufficient permissions for hms.sys.deployment.ExecuteDeployment"

Troubleshooting steps:
1. Check the user's roles and permissions
2. Verify the authorization policy for the service
3. Check the token claims
4. Verify the token is valid and not expired

Solution:
- Grant the necessary roles to the user
- Update the authorization policy
- Ensure the token has the required claims
- Renew the token if expired
```

### 11.2 Debugging Tools

#### 11.2.1 FFI Inspector

The FFI Inspector tool helps debug FFI issues:

```bash
# Install FFI Inspector
go install github.com/hardisonco/hms-ffi/cmd/ffi-inspector@latest

# Inspect service schema
ffi-inspector schema hms.sys.deployment

# Trace FFI calls
ffi-inspector trace hms.sys.deployment ExecuteDeployment

# Monitor FFI registry
ffi-inspector monitor registry
```

#### 11.2.2 Diagnostic Logging

Enable diagnostic logging for detailed information:

```go
// Go diagnostic logging
ffi.SetLogLevel(ffi.LogLevelDebug)
ffi.EnableDiagnostics(true)
```

```python
# Python diagnostic logging
ffi.set_log_level(ffi.LogLevel.DEBUG)
ffi.enable_diagnostics(True)
```

### 11.3 Performance Issues

Troubleshooting performance issues:

```
Problem: FFI calls have high latency
Symptom: Calls take 500ms+ to complete

Troubleshooting steps:
1. Check network latency between components
2. Monitor system resource usage (CPU, memory)
3. Look for connection pooling issues
4. Check for serialization overhead
5. Verify if the correct transport is being used

Solution:
- Use more efficient transport (e.g., shared memory for local calls)
- Implement connection pooling
- Optimize serialization (use zero-copy where possible)
- Consider batching multiple calls
- Reduce payload size
```

## 12. Reference

### 12.1 API Reference

#### 12.1.1 Core API

| Function | Description |
|----------|-------------|
| `Initialize(config)` | Initialize the FFI system |
| `GetClient(serviceID)` | Get a client for a service |
| `GetServiceRegistry()` | Get the service registry |
| `RegisterMethod(serviceID, method, handler)` | Register a method handler |
| `NewError(code, message, details)` | Create a new FFI error |

#### 12.1.2 Client API

| Function | Description |
|----------|-------------|
| `client.Call(method, params, result)` | Make a synchronous call |
| `client.CallAsync(method, params)` | Make an asynchronous call |
| `client.Stream(method, params)` | Create a stream |
| `client.Close()` | Close the client |

#### 12.1.3 Service API

| Function | Description |
|----------|-------------|
| `registry.RegisterService(service)` | Register a service |
| `registry.RegisterMethod(serviceID, method, handler)` | Register a method handler |
| `registry.GetService(serviceID)` | Get a service by ID |
| `registry.ListServices(pattern)` | List services matching a pattern |

### 12.2 Error Codes

| Code | Name | Description |
|------|------|-------------|
| 0 | OK | No error |
| 1 | CANCELLED | The operation was cancelled |
| 2 | UNKNOWN | Unknown error |
| 3 | INVALID_ARGUMENT | The client specified an invalid argument |
| 4 | DEADLINE_EXCEEDED | The deadline expired before the operation could complete |
| 5 | NOT_FOUND | The requested entity was not found |
| 6 | ALREADY_EXISTS | The entity already exists |
| 7 | PERMISSION_DENIED | The caller does not have permission to execute the operation |
| 8 | RESOURCE_EXHAUSTED | Some resource has been exhausted |
| 9 | FAILED_PRECONDITION | The operation was rejected because the system is not in a state required for execution |
| 10 | ABORTED | The operation was aborted |
| 11 | OUT_OF_RANGE | The operation was attempted past the valid range |
| 12 | UNIMPLEMENTED | The operation is not implemented or supported |
| 13 | INTERNAL | Internal error |
| 14 | UNAVAILABLE | The service is currently unavailable |
| 15 | DATA_LOSS | Unrecoverable data loss or corruption |
| 16 | UNAUTHENTICATED | The request does not have valid authentication credentials |

### 12.3 Configuration Options

#### 12.3.1 Core Configuration

| Option | Description | Default |
|--------|-------------|---------|
| `ServiceName` | Name of this service | `"unnamed"` |
| `RegistryURL` | URL of the service registry | `"http://localhost:8080"` |
| `LogLevel` | Log level for FFI operations | `"info"` |
| `Diagnostics` | Enable diagnostic logging | `false` |

#### 12.3.2 Transport Configuration

| Option | Description | Default |
|--------|-------------|---------|
| `DefaultTransport` | Default transport type | `"auto"` |
| `InProcess.Enabled` | Enable in-process transport | `true` |
| `SharedMemory.Enabled` | Enable shared memory transport | `true` |
| `SharedMemory.Path` | Path for shared memory files | `"/tmp/hms-ffi"` |
| `Grpc.Enabled` | Enable gRPC transport | `true` |
| `Grpc.MaxConcurrentStreams` | Maximum concurrent streams | `100` |

#### 12.3.3 Security Configuration

| Option | Description | Default |
|--------|-------------|---------|
| `Auth.Enabled` | Enable authentication | `true` |
| `Auth.TokenValidation.Issuer` | Token issuer | `""` |
| `Auth.TokenValidation.Audience` | Token audience | `""` |
| `Auth.TokenValidation.JwksURL` | JWKS URL | `""` |
| `Auth.RequiredClaims` | Required token claims | `[]` |
| `Authz.Mode` | Authorization mode | `"enforcing"` |
| `Authz.DefaultDeny` | Deny by default | `true` |
| `Authz.PolicyFile` | Authorization policy file | `""` |

## 13. Glossary

| Term | Definition |
|------|------------|
| FFI | Foreign Function Interface - A mechanism for one programming language to call functions in another language. |
| Service | A collection of related functions exposed via the FFI system. |
| Method | A specific function within a service that can be called via FFI. |
| Schema | A formal definition of the data types used in FFI calls. |
| Proto | Short for Protocol Buffers, a format for serializing structured data. |
| Transport | The mechanism used to communicate between components (e.g., in-process, shared memory, gRPC). |
| Registry | A central repository of information about available FFI services. |
| Serialization | The process of converting data structures to a format that can be transmitted. |
| Deserialization | The process of converting transmitted data back into data structures. |
| Client | A component that calls functions in another component via FFI. |
| Server | A component that implements functions that can be called via FFI. |
| Zero-Copy | A technique to avoid copying data between processes. |
| Streaming | A technique for transferring large datasets or continuous data. |
| JWT | JSON Web Token - A compact, URL-safe means of representing claims to be transferred between two parties. |
| mTLS | Mutual TLS - A TLS configuration where both client and server authenticate each other. |