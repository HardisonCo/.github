# HMS FFI Component Extension Plan

This document outlines the plan for extending FFI capabilities to all HMS system components, ensuring consistent cross-component communication and interoperability.

## 1. Component Analysis

The HMS ecosystem includes the following key components that require FFI integration:

| Component | Primary Language | Key Functionality | Integration Priority |
|-----------|-----------------|-------------------|---------------------|
| HMS-SYS   | Go              | System operations, deployment management | High |
| HMS-CDF   | Rust            | Computational debate framework | High |
| HMS-API   | PHP/Laravel     | API services | Medium |
| HMS-GOV   | JavaScript/Vue  | Governance interface | Medium |
| HMS-EMR   | Go              | Electronic medical record services | Medium |
| HMS-ACH   | Ruby            | Automated clearing house | Low |
| HMS-ESR   | Ruby            | Electronic session reporting | Low |
| HMS-ETL   | Python          | Extract-transform-load pipelines | Low |

## 2. Extension Approach

For each component, we will follow a standardized extension process:

### 2.1 Component-Specific FFI Interface

1. **Identify Core Services**: Determine the key services that need to be exposed via FFI
2. **Define Protocol Buffer Schemas**: Create Protocol Buffer definitions for all interfaces
3. **Implement FFI Exports**: Create language-specific FFI exports

### 2.2 Integration with Core FFI Framework

1. **Register with Service Registry**: Register component services with the central registry
2. **Implement Transport Adapters**: Create appropriate transport adapters
3. **Add Security Controls**: Implement authorization and authentication

## 3. Component-Specific Plans

### 3.1 HMS-SYS (Go)

#### 3.1.1 Core Services to Expose

- **DeploymentManager**: Manage deployments across environments
- **ConfigManager**: System-wide configuration management
- **MonitoringService**: System monitoring and health checks
- **LoggingService**: Centralized logging

#### 3.1.2 Implementation Approach

```go
// HMS-SYS FFI exports
package ffi

import (
    "context"
    "github.com/hardisonco/hms-sys/deployment"
    "github.com/hardisonco/hms-sys/config"
    pbffi "github.com/hardisonco/hms-ffi/protos/hms/sys/v1"
    "google.golang.org/protobuf/proto"
)

// DeploymentManagerFFI provides FFI bindings for the DeploymentManager
type DeploymentManagerFFI struct {
    manager *deployment.Manager
}

// NewDeploymentManagerFFI creates a new DeploymentManagerFFI
func NewDeploymentManagerFFI() *DeploymentManagerFFI {
    return &DeploymentManagerFFI{
        manager: deployment.NewManager(),
    }
}

// ExecuteDeployment deploys a component
func (m *DeploymentManagerFFI) ExecuteDeployment(reqBytes []byte) ([]byte, error) {
    var request pbffi.ExecuteDeploymentRequest
    if err := proto.Unmarshal(reqBytes, &request); err != nil {
        return nil, err
    }
    
    // Execute deployment
    result, err := m.manager.ExecuteDeployment(context.Background(), request.ComponentId, request.Version, request.Environment)
    if err != nil {
        return nil, err
    }
    
    // Convert to protobuf response
    response := &pbffi.ExecuteDeploymentResponse{
        DeploymentId: result.ID,
        Status: result.Status,
    }
    
    return proto.Marshal(response)
}

// Register with FFI registry during initialization
func init() {
    registry.RegisterService("hms.sys.deployment", NewDeploymentManagerFFI())
}
```

### 3.2 HMS-CDF (Rust)

#### 3.2.1 Core Services to Expose

- **DebateFramework**: Core computational debate functionality
- **PolicyEvaluator**: Policy evaluation engine
- **EconomicModeler**: Economic modeling and simulation

#### 3.2.2 Implementation Approach

```rust
// HMS-CDF FFI exports
use hms_ffi::registry::ServiceRegistry;
use hms_cdf::debate::{DebateFramework, DebateConfig};
use hms_cdf::policy::PolicyEvaluator;
use prost::Message;

// Generated protobuf code
use hms_ffi_protos::hms::cdf::v1::{
    CreateDebateRequest, CreateDebateResponse,
    EvaluatePolicyRequest, EvaluatePolicyResponse,
};

// DebateFrameworkFFI provides FFI bindings for the DebateFramework
pub struct DebateFrameworkFFI {
    framework: DebateFramework,
}

impl DebateFrameworkFFI {
    // Create a new DebateFrameworkFFI
    pub fn new() -> Self {
        Self {
            framework: DebateFramework::new(DebateConfig::default()),
        }
    }
    
    // Create a new debate
    pub fn create_debate(&self, request_bytes: &[u8]) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
        // Deserialize request
        let request = CreateDebateRequest::decode(request_bytes)?;
        
        // Create debate
        let debate = self.framework.create_debate(
            &request.topic,
            &request.description,
            request.participants.as_slice(),
        )?;
        
        // Create response
        let response = CreateDebateResponse {
            debate_id: debate.id().to_string(),
            status: debate.status() as i32,
        };
        
        // Serialize response
        let mut response_bytes = Vec::new();
        response.encode(&mut response_bytes)?;
        
        Ok(response_bytes)
    }
}

// Register with FFI registry during initialization
pub fn register_ffi_services() {
    let registry = ServiceRegistry::global();
    registry.register_service("hms.cdf.debate", Box::new(DebateFrameworkFFI::new()));
}
```

### 3.3 HMS-API (PHP/Laravel)

#### 3.3.1 Core Services to Expose

- **AuthenticationService**: User authentication
- **DataAccessService**: Data access APIs
- **ReportingService**: Reporting functionality

#### 3.3.2 Implementation Approach

```php
<?php
// HMS-API FFI bindings
namespace HMS\API\FFI;

use HMS\API\Services\AuthenticationService;
use HMS\API\Services\DataAccessService;
use HMS\FFI\Registry\ServiceRegistry;
use Google\Protobuf\Internal\Message;

// Authentication FFI service
class AuthenticationServiceFFI {
    private $service;
    
    public function __construct() {
        $this->service = new AuthenticationService();
    }
    
    // Authenticate user
    public function authenticate(string $requestBytes): string {
        // Deserialize request
        $request = new \HMS\FFI\Protos\HMS\API\V1\AuthenticateRequest();
        $request->mergeFromString($requestBytes);
        
        // Authenticate
        $result = $this->service->authenticate(
            $request->getUsername(),
            $request->getPassword()
        );
        
        // Create response
        $response = new \HMS\FFI\Protos\HMS\API\V1\AuthenticateResponse();
        $response->setSuccess($result->success);
        $response->setToken($result->token);
        $response->setUserId($result->userId);
        
        // Serialize response
        return $response->serializeToString();
    }
}

// Register with FFI registry
$registry = ServiceRegistry::getInstance();
$registry->registerService("hms.api.authentication", new AuthenticationServiceFFI());
```

### 3.4 HMS-GOV (JavaScript/Vue)

#### 3.4.1 Core Services to Expose

- **PolicyService**: Policy management
- **ComplianceService**: Compliance checking
- **AuditService**: Auditing functionality

#### 3.4.2 Implementation Approach

```typescript
// HMS-GOV FFI bindings
import { PolicyService } from '@/services/PolicyService';
import { ComplianceService } from '@/services/ComplianceService';
import { register } from '@hardisonco/hms-ffi/registry';
import { PolicyRequest, PolicyResponse } from '@hardisonco/hms-ffi/protos/hms/gov/v1';

// Policy FFI service
class PolicyServiceFFI {
  private service: PolicyService;
  
  constructor() {
    this.service = new PolicyService();
  }
  
  // Create policy
  async createPolicy(requestBytes: Uint8Array): Promise<Uint8Array> {
    // Deserialize request
    const request = PolicyRequest.decode(requestBytes);
    
    // Create policy
    const result = await this.service.createPolicy({
      title: request.title,
      description: request.description,
      rules: request.rules,
      scope: request.scope
    });
    
    // Create response
    const response = PolicyResponse.create({
      policyId: result.policyId,
      status: result.status,
      version: result.version
    });
    
    // Serialize response
    return PolicyResponse.encode(response).finish();
  }
}

// Register with FFI registry
register('hms.gov.policy', new PolicyServiceFFI());
```

### 3.5 HMS-EMR (Go)

#### 3.5.1 Core Services to Expose

- **PatientService**: Patient record management
- **EncounterService**: Clinical encounter handling
- **MedicationService**: Medication management

#### 3.5.2 Implementation Approach

```go
// HMS-EMR FFI exports
package ffi

import (
    "context"
    "github.com/hardisonco/hms-emr/patient"
    pbffi "github.com/hardisonco/hms-ffi/protos/hms/emr/v1"
    "google.golang.org/protobuf/proto"
)

// PatientServiceFFI provides FFI bindings for the PatientService
type PatientServiceFFI struct {
    service *patient.Service
}

// NewPatientServiceFFI creates a new PatientServiceFFI
func NewPatientServiceFFI() *PatientServiceFFI {
    return &PatientServiceFFI{
        service: patient.NewService(),
    }
}

// GetPatient retrieves a patient record
func (s *PatientServiceFFI) GetPatient(reqBytes []byte) ([]byte, error) {
    var request pbffi.GetPatientRequest
    if err := proto.Unmarshal(reqBytes, &request); err != nil {
        return nil, err
    }
    
    // Get patient
    patient, err := s.service.GetPatient(context.Background(), request.PatientId)
    if err != nil {
        return nil, err
    }
    
    // Convert to protobuf response
    response := &pbffi.GetPatientResponse{
        Patient: &pbffi.Patient{
            Id: patient.ID,
            Name: patient.Name,
            DateOfBirth: patient.DateOfBirth.Format("2006-01-02"),
            Gender: patient.Gender,
        },
    }
    
    return proto.Marshal(response)
}

// Register with FFI registry during initialization
func init() {
    registry.RegisterService("hms.emr.patient", NewPatientServiceFFI())
}
```

### 3.6 HMS-ACH (Ruby)

#### 3.6.1 Core Services to Expose

- **TransactionService**: Financial transaction processing
- **ReconciliationService**: Financial reconciliation
- **ReportingService**: Financial reporting

#### 3.6.2 Implementation Approach

```ruby
# HMS-ACH FFI bindings
require 'hms/ach/transaction_service'
require 'hms/ffi/registry'
require 'hms/ffi/protos/hms/ach/v1/transaction_pb'

module HMS
  module ACH
    module FFI
      # Transaction FFI service
      class TransactionServiceFFI
        def initialize
          @service = HMS::ACH::TransactionService.new
        end
        
        # Process transaction
        def process_transaction(request_bytes)
          # Deserialize request
          request = HMS::FFI::Protos::HMS::ACH::V1::ProcessTransactionRequest.decode(request_bytes)
          
          # Process transaction
          result = @service.process_transaction(
            request.transaction_id,
            request.amount,
            request.from_account,
            request.to_account
          )
          
          # Create response
          response = HMS::FFI::Protos::HMS::ACH::V1::ProcessTransactionResponse.new(
            transaction_id: result.transaction_id,
            status: result.status,
            confirmation_code: result.confirmation_code
          )
          
          # Serialize response
          HMS::FFI::Protos::HMS::ACH::V1::ProcessTransactionResponse.encode(response)
        end
      end
    end
  end
end

# Register with FFI registry
HMS::FFI::Registry.register_service("hms.ach.transaction", HMS::ACH::FFI::TransactionServiceFFI.new)
```

### 3.7 HMS-ESR (Ruby)

#### 3.7.1 Core Services to Expose

- **SessionService**: Session management
- **ReportingService**: Session reporting
- **AnalyticsService**: Session analytics

#### 3.7.2 Implementation Approach

```ruby
# HMS-ESR FFI bindings
require 'hms/esr/session_service'
require 'hms/ffi/registry'
require 'hms/ffi/protos/hms/esr/v1/session_pb'

module HMS
  module ESR
    module FFI
      # Session FFI service
      class SessionServiceFFI
        def initialize
          @service = HMS::ESR::SessionService.new
        end
        
        # Create session
        def create_session(request_bytes)
          # Deserialize request
          request = HMS::FFI::Protos::HMS::ESR::V1::CreateSessionRequest.decode(request_bytes)
          
          # Create session
          result = @service.create_session(
            request.user_id,
            request.application_id,
            request.metadata
          )
          
          # Create response
          response = HMS::FFI::Protos::HMS::ESR::V1::CreateSessionResponse.new(
            session_id: result.session_id,
            start_time: result.start_time.to_s,
            status: result.status
          )
          
          # Serialize response
          HMS::FFI::Protos::HMS::ESR::V1::CreateSessionResponse.encode(response)
        end
      end
    end
  end
end

# Register with FFI registry
HMS::FFI::Registry.register_service("hms.esr.session", HMS::ESR::FFI::SessionServiceFFI.new)
```

### 3.8 HMS-ETL (Python)

#### 3.8.1 Core Services to Expose

- **PipelineService**: ETL pipeline management
- **DataSourceService**: Data source management
- **TransformationService**: Data transformation

#### 3.8.2 Implementation Approach

```python
# HMS-ETL FFI bindings
from hms.etl.pipeline import PipelineService
from hms.ffi.registry import register_service
from hms.ffi.protos.hms.etl.v1.pipeline_pb2 import (
    ExecutePipelineRequest,
    ExecutePipelineResponse
)

class PipelineServiceFFI:
    def __init__(self):
        self.service = PipelineService()
    
    def execute_pipeline(self, request_bytes):
        # Deserialize request
        request = ExecutePipelineRequest()
        request.ParseFromString(request_bytes)
        
        # Execute pipeline
        result = self.service.execute_pipeline(
            pipeline_id=request.pipeline_id,
            parameters={k: v for k, v in request.parameters.items()},
            schedule_time=request.schedule_time
        )
        
        # Create response
        response = ExecutePipelineResponse(
            execution_id=result.execution_id,
            status=result.status,
            start_time=result.start_time
        )
        
        # Serialize response
        return response.SerializeToString()

# Register with FFI registry
register_service("hms.etl.pipeline", PipelineServiceFFI())
```

## 4. Protocol Buffer Schema Definitions

For each component, we will create Protocol Buffer schema definitions. Here are examples for key components:

### 4.1 HMS-SYS

```protobuf
syntax = "proto3";

package hms.sys.v1;

// Deployment service
service DeploymentService {
  // Execute a deployment
  rpc ExecuteDeployment(ExecuteDeploymentRequest) returns (ExecuteDeploymentResponse);
  
  // Get deployment status
  rpc GetDeploymentStatus(GetDeploymentStatusRequest) returns (GetDeploymentStatusResponse);
  
  // Cancel a deployment
  rpc CancelDeployment(CancelDeploymentRequest) returns (CancelDeploymentResponse);
}

// Request to execute a deployment
message ExecuteDeploymentRequest {
  // Component ID to deploy
  string component_id = 1;
  
  // Version to deploy
  string version = 2;
  
  // Environment to deploy to
  string environment = 3;
  
  // Deployment parameters
  map<string, string> parameters = 4;
}

// Response to a deployment execution
message ExecuteDeploymentResponse {
  // Deployment ID
  string deployment_id = 1;
  
  // Deployment status
  DeploymentStatus status = 2;
}

// Deployment status
enum DeploymentStatus {
  // Unknown status
  DEPLOYMENT_STATUS_UNSPECIFIED = 0;
  
  // Deployment is pending
  PENDING = 1;
  
  // Deployment is in progress
  IN_PROGRESS = 2;
  
  // Deployment succeeded
  SUCCEEDED = 3;
  
  // Deployment failed
  FAILED = 4;
  
  // Deployment was cancelled
  CANCELLED = 5;
}
```

### 4.2 HMS-CDF

```protobuf
syntax = "proto3";

package hms.cdf.v1;

// Debate framework service
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

// Request to create a debate
message CreateDebateRequest {
  // Debate topic
  string topic = 1;
  
  // Debate description
  string description = 2;
  
  // Debate participants
  repeated string participants = 3;
  
  // Debate parameters
  map<string, string> parameters = 4;
}

// Response to creating a debate
message CreateDebateResponse {
  // Debate ID
  string debate_id = 1;
  
  // Debate status
  DebateStatus status = 2;
}

// Debate status
enum DebateStatus {
  // Unknown status
  DEBATE_STATUS_UNSPECIFIED = 0;
  
  // Debate is created
  CREATED = 1;
  
  // Debate is in progress
  IN_PROGRESS = 2;
  
  // Debate is completed
  COMPLETED = 3;
  
  // Debate is cancelled
  CANCELLED = 4;
}
```

## 5. Implementation Timeline

| Phase | Component | Duration |
|-------|-----------|----------|
| 1 | Core Protocol Buffer Definitions | 1 week |
| 2 | HMS-SYS and HMS-CDF | 1 week |
| 3 | HMS-API and HMS-GOV | 1 week |
| 4 | HMS-EMR | 3 days |
| 5 | HMS-ACH and HMS-ESR | 3 days |
| 6 | HMS-ETL | 2 days |
| 7 | Integration and Testing | 1 week |

Total: ~4 weeks

## 6. Key Deliverables

For each component, we will deliver:

1. Protocol Buffer schema definitions
2. FFI interface implementations
3. Service registry integration
4. Language-specific bindings
5. Example usage documentation

## 7. Integration Strategy

The component extensions will integrate with the core FFI framework through:

1. **Standardized Service Registration**: All components will register their services with the central registry
2. **Unified Type System**: All components will use the same type mapping system
3. **Common Error Handling**: All components will follow the standard error handling approach
4. **Transport Abstraction**: All components will work with the same transport abstractions

## 8. Testing Strategy

Component-specific testing will be integrated into the unified testing framework, which will be developed after completing the component extensions.