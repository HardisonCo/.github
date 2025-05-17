# HMS FFI Integration Strategy

This document outlines the integration strategy for enabling seamless cross-component function calling via FFI across the HMS ecosystem.

## 1. Introduction

The HMS ecosystem consists of multiple components implemented in different programming languages. The Foreign Function Interface (FFI) system enables these components to call each other's functions regardless of the implementation language. This integration strategy defines how these cross-component calls are structured, implemented, and managed.

## 2. Integration Architecture

The integration architecture follows a layered approach:

```
┌────────────────────────────────────────────────────────────────┐
│                      HMS Components                             │
├────────────┬───────────────┬───────────────┬───────────────────┤
│  HMS-SYS   │   HMS-CDF     │   HMS-API     │   Other Components│
│  (Go)      │   (Rust)      │   (PHP)       │                   │
└────────────┴───────────────┴───────────────┴───────────────────┘
              ▲               ▲                ▲
              │               │                │
              │     Service API Calls          │
              │               │                │
              ▼               ▼                ▼
┌────────────────────────────────────────────────────────────────┐
│                      HMS-FFI System                             │
├────────────────────────────────────────────────────────────────┤
│                      Service Registry                           │
├────────────────────────────────────────────────────────────────┤
│                     Function Dispatcher                         │
├────────────────────────────────────────────────────────────────┤
│                    Serialization Layer                          │
├────────────────────────────────────────────────────────────────┤
│                      Transport Layer                            │
└────────────────────────────────────────────────────────────────┘
```

### 2.1 Key Integration Components

#### 2.1.1 Service Registry

The Service Registry provides a centralized registry of all available services across the HMS ecosystem:

- **Service Registration**: Components register their services with the registry
- **Service Discovery**: Components discover available services
- **Service Metadata**: Information about service capabilities and requirements
- **Version Management**: Tracking of service versions and compatibility

#### 2.1.2 Function Dispatcher

The Function Dispatcher routes function calls to the appropriate service:

- **Call Routing**: Determines the target service for a function call
- **Parameter Marshaling**: Converts parameters to the appropriate format
- **Result Handling**: Processes and returns function results
- **Error Handling**: Manages errors and exceptions

#### 2.1.3 Serialization Layer

The Serialization Layer handles data conversion between languages:

- **Type Mapping**: Maps types between languages
- **Schema Validation**: Validates data against schemas
- **Format Selection**: Chooses the optimal serialization format
- **Optimization**: Applies performance optimizations

#### 2.1.4 Transport Layer

The Transport Layer handles communication between components:

- **Transport Selection**: Chooses the optimal transport mechanism
- **Connection Management**: Manages connections between components
- **Security**: Ensures secure communication
- **Performance Optimization**: Optimizes transport for performance

## 3. Integration Patterns

### 3.1 Direct Function Call

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│ Component A│      │  HMS-FFI   │      │ Component B│
│ Function   │─────►│  System    │─────►│ Function   │
└────────────┘      └────────────┘      └────────────┘
```

- Synchronous function call from one component to another
- Blocking until result is returned
- Simple and straightforward integration pattern
- Useful for simple operations that return quickly

### 3.2 Async Function Call

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│ Component A│──1──►│  HMS-FFI   │──2──►│ Component B│
│            │      │  System    │      │            │
└────────────┘      └────────────┘      └────────────┘
       ▲                  │                    │
       │                  │                    │
       └───────4──────────┴───────3───────────┘
```

1. Component A makes an asynchronous call
2. HMS-FFI forwards the call to Component B
3. Component B returns the result to HMS-FFI
4. HMS-FFI delivers the result to Component A via callback or future

- Non-blocking function call
- Caller continues execution while callee processes
- Result delivered via callback, future, or promise
- Useful for operations that take longer to complete

### 3.3 Streaming Data

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│ Component A│──1──►│  HMS-FFI   │──2──►│ Component B│
│            │◄─5───│  System    │◄─4───│            │
└────────────┘      └────────────┘      └────────────┘
       │                  ▲                    │
       │                  │                    │
       └───────6──────────┴───────3───────────┘
```

1. Component A initiates a streaming call
2. HMS-FFI forwards the call to Component B
3. Component B begins processing
4. Component B streams data chunks to HMS-FFI
5. HMS-FFI forwards data chunks to Component A
6. Process continues until complete or canceled

- Continuous data flow between components
- Data processed and delivered in chunks
- Useful for large datasets or real-time data

### 3.4 Pub/Sub Communication

```
                      ┌────────────┐
                  ┌──►│ Component B│
                  │   └────────────┘
┌────────────┐    │
│ Component A│────┤   ┌────────────┐
│ (Publisher)│    ├──►│ Component C│
└────────────┘    │   └────────────┘
                  │
                  │   ┌────────────┐
                  └──►│ Component D│
                      └────────────┘
```

- One component publishes messages
- Multiple components subscribe to receive messages
- Decoupled communication
- Useful for event-driven architectures

## 4. Integration Scenarios

### 4.1 HMS-SYS to HMS-CDF Integration

**Scenario**: HMS-SYS needs to invoke HMS-CDF's debate framework for policy evaluation

**Implementation**:

```go
// Go code in HMS-SYS
import (
    "context"
    "github.com/hardisonco/hms-ffi/client"
)

func EvaluatePolicy(policyID string, resource map[string]string) (*PolicyEvaluation, error) {
    // Create FFI client for HMS-CDF debate service
    cdfClient, err := client.NewClient("hms.cdf.debate")
    if err != nil {
        return nil, fmt.Errorf("failed to create CDF client: %w", err)
    }
    
    // Prepare request parameters
    params := map[string]interface{}{
        "policy_id": policyID,
        "resource": resource,
    }
    
    // Call HMS-CDF function via FFI
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    
    var result PolicyEvaluation
    err = cdfClient.Call(ctx, "EvaluatePolicy", params, &result)
    if err != nil {
        return nil, fmt.Errorf("policy evaluation failed: %w", err)
    }
    
    return &result, nil
}
```

**Rust Implementation in HMS-CDF**:

```rust
// Rust code in HMS-CDF
use hms_ffi::{service, method, Result};
use crate::debate::{DebateFramework, PolicyEvaluation};

#[service("hms.cdf.debate")]
pub struct DebateService {
    framework: DebateFramework,
}

impl DebateService {
    #[method]
    pub fn evaluate_policy(&self, policy_id: String, resource: HashMap<String, String>) -> Result<PolicyEvaluation> {
        // Use the debate framework to evaluate the policy
        let evaluation = self.framework.evaluate_policy(&policy_id, &resource)?;
        
        // Return the evaluation result
        Ok(evaluation)
    }
}
```

### 4.2 HMS-API to HMS-EMR Integration

**Scenario**: HMS-API needs to retrieve patient data from HMS-EMR

**Implementation**:

```php
// PHP code in HMS-API
use HMS\FFI\Client;

class PatientController extends Controller
{
    public function getPatient($patientId)
    {
        try {
            // Create FFI client for HMS-EMR patient service
            $emrClient = new Client("hms.emr.patient");
            
            // Call HMS-EMR function via FFI
            $patient = $emrClient->call("GetPatient", [
                "patient_id" => $patientId
            ]);
            
            // Process and return the patient data
            return response()->json($patient);
        } catch (FFIException $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }
}
```

**Go Implementation in HMS-EMR**:

```go
// Go code in HMS-EMR
import (
    "context"
    "github.com/hardisonco/hms-ffi/service"
)

// Register patient service with FFI system
func RegisterPatientService() {
    service.Register("hms.emr.patient", &PatientService{})
}

// PatientService provides patient-related functionality
type PatientService struct {
    repository PatientRepository
}

// GetPatient retrieves a patient by ID
func (s *PatientService) GetPatient(ctx context.Context, patientID string) (*Patient, error) {
    // Retrieve patient from repository
    patient, err := s.repository.GetPatientByID(patientID)
    if err != nil {
        return nil, fmt.Errorf("failed to retrieve patient: %w", err)
    }
    
    return patient, nil
}
```

### 4.3 HMS-ETL to HMS-ACH Integration

**Scenario**: HMS-ETL needs to process financial transactions in HMS-ACH

**Implementation**:

```python
# Python code in HMS-ETL
from hms_ffi.client import Client

class FinancialTransactionProcessor:
    def __init__(self):
        # Create FFI client for HMS-ACH transaction service
        self.ach_client = Client("hms.ach.transaction")
    
    async def process_transactions(self, transactions):
        results = []
        
        for transaction in transactions:
            # Process each transaction via FFI
            try:
                result = await self.ach_client.call_async("ProcessTransaction", {
                    "type": transaction["type"],
                    "amount": transaction["amount"],
                    "source_account_id": transaction["source"],
                    "destination_account_id": transaction["destination"],
                    "description": transaction["description"]
                })
                results.append({"id": transaction["id"], "status": "success", "result": result})
            except Exception as e:
                results.append({"id": transaction["id"], "status": "error", "error": str(e)})
        
        return results
```

**Ruby Implementation in HMS-ACH**:

```ruby
# Ruby code in HMS-ACH
require 'hms/ffi/service'

module HMS
  module ACH
    class TransactionService
      include HMS::FFI::Service
      
      register_service "hms.ach.transaction"
      
      register_method :process_transaction do |params|
        # Extract parameters
        type = params["type"]
        amount = params["amount"]
        source_account_id = params["source_account_id"]
        destination_account_id = params["destination_account_id"]
        description = params["description"]
        
        # Process the transaction
        transaction = Transaction.new(
          type: type,
          amount: amount,
          source_account_id: source_account_id,
          destination_account_id: destination_account_id,
          description: description
        )
        
        result = transaction.process
        
        # Return the result
        {
          "transaction_id" => result.transaction_id,
          "status" => result.status,
          "confirmation_code" => result.confirmation_code
        }
      end
    end
  end
end
```

## 5. Integration Workflow

### 5.1 Service Registration Workflow

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│ Component  │  1   │  Service   │  2   │  Schema    │
│ Startup    │─────►│  Registry  │─────►│  Validator │
└────────────┘      └────────────┘      └────────────┘
                         │  ▲
                      3  │  │ 4
                         ▼  │
                    ┌────────────┐
                    │  Service   │
                    │  Database  │
                    └────────────┘
```

1. Component registers its services at startup
2. Service Registry validates service schemas
3. Registry stores service information in database
4. Registry acknowledges successful registration

### 5.2 Service Discovery Workflow

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│ Component  │  1   │  Service   │  2   │  Service   │
│ Client     │─────►│  Registry  │─────►│  Database  │
└────────────┘      └────────────┘      └────────────┘
      ▲                   │
      │                   │ 3
      └───────4───────────┘
```

1. Client requests services matching criteria
2. Registry queries database for matching services
3. Registry retrieves matching service information
4. Registry returns service information to client

### 5.3 Function Call Workflow

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│ Caller     │  1   │ Function   │  2   │ Service    │
│ Component  │─────►│ Dispatcher │─────►│ Registry   │
└────────────┘      └────────────┘      └────────────┘
      ▲                   │                    │
      │                   │ 5                  │ 3
      └───────6───────────┘                    ▼
                                        ┌────────────┐
                                        │ Target     │
                                        │ Service    │
                                        └─────┬──────┘
                                              │ 4
                                              ▼
                                        ┌────────────┐
                                        │ Target     │
                                        │ Function   │
                                        └────────────┘
```

1. Caller invokes function via FFI
2. Function Dispatcher queries Service Registry
3. Registry returns target service information
4. Dispatcher routes call to target function
5. Function executes and returns result
6. Result returned to caller

## 6. Service Contracts

Services expose their capabilities through well-defined contracts:

### 6.1 Contract Definition

Service contracts are defined using Protocol Buffers:

```protobuf
// HMS-CDF Debate service contract
service DebateService {
  // Create a new debate
  rpc CreateDebate(CreateDebateRequest) returns (CreateDebateResponse);
  
  // Add a position to a debate
  rpc AddPosition(AddPositionRequest) returns (AddPositionResponse);
  
  // Add evidence to a position
  rpc AddEvidence(AddEvidenceRequest) returns (AddEvidenceResponse);
  
  // Evaluate a debate
  rpc EvaluateDebate(EvaluateDebateRequest) returns (EvaluateDebateResponse);
}
```

### 6.2 Contract Versioning

Service contracts are versioned to maintain compatibility:

```protobuf
// HMS-CDF Debate service contract v2
service DebateServiceV2 {
  // Original methods from v1
  rpc CreateDebate(CreateDebateRequest) returns (CreateDebateResponse);
  rpc AddPosition(AddPositionRequest) returns (AddPositionResponse);
  rpc AddEvidence(AddEvidenceRequest) returns (AddEvidenceResponse);
  rpc EvaluateDebate(EvaluateDebateRequest) returns (EvaluateDebateResponse);
  
  // New methods in v2
  rpc MergeDebates(MergeDebatesRequest) returns (MergeDebatesResponse);
  rpc ExportDebate(ExportDebateRequest) returns (ExportDebateResponse);
}
```

### 6.3 Contract Registration

Services register their contracts with the Service Registry:

```go
// Go code for registering a service contract
func RegisterServiceContract() {
    // Create service definition
    svc := &ffi.ServiceDefinition{
        ServiceID:   "hms.sys.deployment",
        DisplayName: "HMS-SYS Deployment Service",
        Description: "Manages deployments across environments",
        Version:     "1.0.0",
        Methods:     []*ffi.MethodDefinition{
            {
                Name:        "ExecuteDeployment",
                Description: "Executes a deployment",
                InputSchema: deploymentRequestSchema,
                OutputSchema: deploymentResponseSchema,
            },
            {
                Name:        "GetDeploymentStatus",
                Description: "Gets deployment status",
                InputSchema: statusRequestSchema,
                OutputSchema: statusResponseSchema,
            },
        },
    }
    
    // Register with registry
    registry := ffi.GetServiceRegistry()
    if err := registry.RegisterService(svc); err != nil {
        log.Fatalf("Failed to register service: %v", err)
    }
}
```

## 7. Security Integration

### 7.1 Authentication

All cross-component calls are authenticated:

```go
// Go code for authenticating a service call
func AuthenticateServiceCall(ctx context.Context, serviceID, methodName string) error {
    // Get authentication token from context
    token, ok := auth.TokenFromContext(ctx)
    if !ok {
        return errors.New("authentication token not found")
    }
    
    // Validate token
    auth := ffi.GetAuthService()
    valid, claims, err := auth.ValidateToken(token)
    if err != nil {
        return fmt.Errorf("token validation failed: %w", err)
    }
    
    if !valid {
        return errors.New("invalid authentication token")
    }
    
    // Check service access permissions
    if !auth.HasPermission(claims, serviceID, methodName) {
        return errors.New("access denied to service method")
    }
    
    return nil
}
```

### 7.2 Authorization

Access to services and methods is controlled through policies:

```json
{
  "service": "hms.emr.patient",
  "method": "GetPatient",
  "allowed_roles": ["doctor", "nurse", "administrator"],
  "denied_roles": [],
  "requires_mfa": false,
  "audit_level": "standard"
}
```

### 7.3 Secure Transport

Communication between components uses secure transport:

- **In-Process**: Direct memory access (inherently secure)
- **Same-Machine**: Unix domain sockets or shared memory
- **Network**: TLS with mutual authentication

## 8. Error Handling Integration

### 8.1 Error Propagation

Errors are propagated across component boundaries with appropriate context:

```go
// Go code for error propagation
func handleError(err error) *ffi.Error {
    if err == nil {
        return nil
    }
    
    // Convert Go error to FFI error
    var code int32
    var details map[string]string
    
    switch e := err.(type) {
    case *NotFoundError:
        code = ffi.ErrorCodeNotFound
        details = map[string]string{
            "resource_type": e.ResourceType,
            "resource_id": e.ResourceID,
        }
    case *ValidationError:
        code = ffi.ErrorCodeInvalidArgument
        details = map[string]string{
            "field": e.Field,
            "reason": e.Reason,
        }
    default:
        code = ffi.ErrorCodeInternal
    }
    
    return &ffi.Error{
        Code:    code,
        Message: err.Error(),
        Source:  "hms-sys",
        Details: details,
    }
}
```

### 8.2 Error Translation

Errors are translated to appropriate forms in each language:

```python
# Python code for error translation
def translate_error(ffi_error):
    if ffi_error is None:
        return None
    
    # Map FFI error code to Python exception
    if ffi_error.code == FFI_ERROR_CODE_NOT_FOUND:
        return ResourceNotFoundError(
            ffi_error.message,
            resource_type=ffi_error.details.get("resource_type"),
            resource_id=ffi_error.details.get("resource_id")
        )
    elif ffi_error.code == FFI_ERROR_CODE_INVALID_ARGUMENT:
        return ValidationError(
            ffi_error.message,
            field=ffi_error.details.get("field"),
            reason=ffi_error.details.get("reason")
        )
    else:
        return ServiceError(ffi_error.message, code=ffi_error.code)
```

## 9. Monitoring and Observability

### 9.1 Tracing Integration

Distributed tracing is implemented across component boundaries:

```go
// Go code for distributed tracing
func tracedServiceCall(ctx context.Context, serviceID, methodName string, params interface{}) (interface{}, error) {
    // Create trace span
    ctx, span := tracer.StartSpan(ctx, fmt.Sprintf("%s.%s", serviceID, methodName))
    defer span.End()
    
    // Add span attributes
    span.SetAttributes(
        attribute.String("service.id", serviceID),
        attribute.String("method.name", methodName),
    )
    
    // Make service call
    client := ffi.GetClient(serviceID)
    result, err := client.Call(ctx, methodName, params)
    
    // Record error if any
    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
    }
    
    return result, err
}
```

### 9.2 Metrics Integration

Performance metrics are collected for all cross-component calls:

```go
// Go code for metrics collection
func instrumentedServiceCall(ctx context.Context, serviceID, methodName string, params interface{}) (interface{}, error) {
    labels := []attribute.KeyValue{
        attribute.String("service", serviceID),
        attribute.String("method", methodName),
    }
    
    // Start timer
    start := time.Now()
    
    // Track call count
    metrics.Calls.Add(ctx, 1, labels...)
    
    // Make service call
    result, err := client.Call(ctx, methodName, params)
    
    // Record duration
    duration := time.Since(start)
    metrics.CallDuration.Record(ctx, duration.Milliseconds(), labels...)
    
    // Track errors
    if err != nil {
        metrics.Errors.Add(ctx, 1, labels...)
    }
    
    return result, err
}
```

### 9.3 Logging Integration

Consistent logging is implemented across component boundaries:

```go
// Go code for consistent logging
func logServiceCall(ctx context.Context, serviceID, methodName string, params interface{}) {
    // Extract trace ID from context
    traceID := trace.SpanFromContext(ctx).SpanContext().TraceID().String()
    
    // Log service call
    logger := ffi.GetLogger()
    logger.Info("Service call",
        "trace_id", traceID,
        "service_id", serviceID,
        "method", methodName,
        "user_id", auth.UserIDFromContext(ctx),
    )
}
```

## 10. Deployment Integration

### 10.1 Component Deployment

Components are deployed with their FFI dependencies:

```yaml
# Docker Compose example
services:
  hms-sys:
    image: hardisonco/hms-sys:latest
    environment:
      - HMS_FFI_REGISTRY_URL=http://registry:8080
    volumes:
      - hms-ffi-data:/var/lib/hms-ffi
    depends_on:
      - registry
  
  hms-cdf:
    image: hardisonco/hms-cdf:latest
    environment:
      - HMS_FFI_REGISTRY_URL=http://registry:8080
    volumes:
      - hms-ffi-data:/var/lib/hms-ffi
    depends_on:
      - registry
  
  registry:
    image: hardisonco/hms-ffi-registry:latest
    volumes:
      - registry-data:/var/lib/registry

volumes:
  hms-ffi-data:
  registry-data:
```

### 10.2 Service Discovery Configuration

Service discovery is configured for each environment:

```yaml
# HMS-FFI configuration
ffi:
  registry:
    url: http://registry:8080
    cache_ttl: 300s
    refresh_interval: 60s
  
  transport:
    default: grpc
    in_process:
      enabled: true
    local_socket:
      enabled: true
      path: /var/run/hms-ffi/sockets
    grpc:
      enabled: true
      max_concurrent_streams: 100
  
  security:
    token_validation_endpoint: http://auth:8080/validate
    required_claims:
      - sub
      - role
    permission_policy: strict
```

## 11. Implementation Plan

### 11.1 Phase 1: Core Integration (2 weeks)

1. **Service Registry**: Implement central service registry
2. **Protocol Definitions**: Define Protocol Buffer schemas for all services
3. **Core Libraries**: Implement core FFI libraries for key languages

### 11.2 Phase 2: Initial Component Integration (3 weeks)

1. **HMS-SYS and HMS-CDF**: Integrate core system components
2. **HMS-API and HMS-EMR**: Integrate API and data components
3. **Testing**: Implement integration tests

### 11.3 Phase 3: Extended Component Integration (2 weeks)

1. **HMS-ACH and HMS-ETL**: Integrate financial and data processing components
2. **HMS-ESR**: Integrate session reporting components
3. **Testing**: Expand integration test coverage

### 11.4 Phase 4: Advanced Features (2 weeks)

1. **Streaming**: Implement streaming data support
2. **Pub/Sub**: Implement publish/subscribe patterns
3. **Security**: Enhance security features

## 12. Conclusion

This integration strategy provides a comprehensive approach to enabling cross-component function calls via FFI across the HMS ecosystem. By implementing this strategy, we will create a seamless interoperability layer that allows components to work together regardless of their implementation language.

The key benefits of this approach include:

1. **Language Flexibility**: Components can be implemented in the most appropriate language
2. **Performance Optimization**: Communication is optimized based on deployment topology
3. **Strong Typing**: Function calls are schema-validated for type safety
4. **Security**: All cross-component communication is secured and authenticated
5. **Observability**: Comprehensive monitoring of cross-component calls

With this integration strategy in place, the HMS ecosystem will achieve a new level of cohesion and flexibility, enabling more powerful cross-component workflows while maintaining the benefits of language-specific implementations.