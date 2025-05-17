# HMS Foreign Function Interface (FFI) API Specification

This document defines the Application Programming Interface (API) for the HMS Foreign Function Interface (FFI) system, providing a standard interface for cross-language function calls across the HMS ecosystem.

## 1. Core APIs

### 1.1 Service API

The Service API provides the primary mechanism for defining and invoking services across language boundaries.

#### 1.1.1 ServiceDefinition

```protobuf
syntax = "proto3";

package hms.ffi.v1;

// Defines a service that can be called across language boundaries
message ServiceDefinition {
  // Unique service identifier
  string service_id = 1;
  
  // Human-readable service name
  string display_name = 2;
  
  // Service description
  string description = 3;
  
  // Service version
  string version = 4;
  
  // Methods provided by this service
  repeated MethodDefinition methods = 5;
  
  // Service metadata
  map<string, string> metadata = 6;
  
  // Security requirements
  SecurityRequirements security = 7;
}

// Defines a method within a service
message MethodDefinition {
  // Method name (must be unique within a service)
  string name = 1;
  
  // Method description
  string description = 2;
  
  // Input parameter schema
  Schema input_schema = 3;
  
  // Output schema
  Schema output_schema = 4;
  
  // Error schemas that can be returned
  repeated Schema error_schemas = 5;
  
  // Whether this method is streaming
  bool is_streaming = 6;
  
  // Stream type (if is_streaming is true)
  StreamType stream_type = 7;
  
  // Method metadata
  map<string, string> metadata = 8;
  
  // Method-specific security requirements (overrides service-level)
  SecurityRequirements security = 9;
  
  // Timeout in milliseconds (0 = use default)
  int32 timeout_ms = 10;
}

// Type of streaming for streaming methods
enum StreamType {
  // Unknown stream type (invalid)
  STREAM_TYPE_UNSPECIFIED = 0;
  
  // Server streams results to client
  SERVER_STREAMING = 1;
  
  // Client streams data to server
  CLIENT_STREAMING = 2;
  
  // Bidirectional streaming
  BIDIRECTIONAL_STREAMING = 3;
}

// Security requirements for a service or method
message SecurityRequirements {
  // Authentication requirement
  AuthType auth_type = 1;
  
  // Required roles (if any)
  repeated string required_roles = 2;
  
  // Custom security rules (if any)
  repeated string security_rules = 3;
}

// Authentication types
enum AuthType {
  // Use default authentication
  AUTH_TYPE_DEFAULT = 0;
  
  // No authentication required
  AUTH_TYPE_NONE = 1;
  
  // Token-based authentication
  AUTH_TYPE_TOKEN = 2;
  
  // Certificate-based authentication
  AUTH_TYPE_CERT = 3;
  
  // Custom authentication
  AUTH_TYPE_CUSTOM = 4;
}
```

#### 1.1.2 ServiceRegistry

```protobuf
syntax = "proto3";

package hms.ffi.v1;

import "service_definition.proto";

// Service used to register and discover FFI services
service ServiceRegistry {
  // Register a new service with the registry
  rpc RegisterService(RegisterServiceRequest) returns (RegisterServiceResponse);
  
  // Unregister a service from the registry
  rpc UnregisterService(UnregisterServiceRequest) returns (UnregisterServiceResponse);
  
  // Get information about a specific service
  rpc GetService(GetServiceRequest) returns (GetServiceResponse);
  
  // List available services matching criteria
  rpc ListServices(ListServicesRequest) returns (ListServicesResponse);
  
  // Watch for service changes
  rpc WatchServices(WatchServicesRequest) returns (stream ServiceEvent);
}

// Request to register a service
message RegisterServiceRequest {
  // Service definition to register
  ServiceDefinition service = 1;
  
  // Registration metadata
  map<string, string> metadata = 2;
}

// Response to service registration
message RegisterServiceResponse {
  // Success status
  bool success = 1;
  
  // Error message if registration failed
  string error_message = 2;
  
  // Generated service ID (if one wasn't provided)
  string service_id = 3;
}

// Request to unregister a service
message UnregisterServiceRequest {
  // ID of service to unregister
  string service_id = 1;
}

// Response to service unregistration
message UnregisterServiceResponse {
  // Success status
  bool success = 1;
  
  // Error message if unregistration failed
  string error_message = 2;
}

// Request to get a specific service
message GetServiceRequest {
  // ID of service to retrieve
  string service_id = 1;
}

// Response with service information
message GetServiceResponse {
  // Service definition
  ServiceDefinition service = 1;
  
  // Service status
  ServiceStatus status = 2;
  
  // Error message if retrieval failed
  string error_message = 3;
}

// Request to list services
message ListServicesRequest {
  // Optional filter by service name pattern
  string name_pattern = 1;
  
  // Optional filter by metadata
  map<string, string> metadata_filter = 2;
  
  // Maximum number of services to return
  int32 limit = 3;
  
  // Pagination token for additional results
  string page_token = 4;
}

// Response with list of services
message ListServicesResponse {
  // List of services matching criteria
  repeated ServiceDefinition services = 1;
  
  // Token for next page of results (if available)
  string next_page_token = 2;
}

// Request to watch for service changes
message WatchServicesRequest {
  // Optional filter by service name pattern
  string name_pattern = 1;
  
  // Optional filter by metadata
  map<string, string> metadata_filter = 2;
}

// Event representing a service change
message ServiceEvent {
  // Type of event
  EventType type = 1;
  
  // Service definition
  ServiceDefinition service = 2;
  
  // Timestamp of the event (Unix timestamp in milliseconds)
  int64 timestamp = 3;
}

// Type of service event
enum EventType {
  // Unknown event type
  EVENT_TYPE_UNSPECIFIED = 0;
  
  // Service was added
  SERVICE_ADDED = 1;
  
  // Service was modified
  SERVICE_MODIFIED = 2;
  
  // Service was removed
  SERVICE_REMOVED = 3;
}

// Status of a service
enum ServiceStatus {
  // Unknown status
  STATUS_UNSPECIFIED = 0;
  
  // Service is available and healthy
  AVAILABLE = 1;
  
  // Service is unavailable
  UNAVAILABLE = 2;
  
  // Service is in degraded state
  DEGRADED = 3;
}
```

#### 1.1.3 ServiceClient

```protobuf
syntax = "proto3";

package hms.ffi.v1;

import "service_definition.proto";

// Client API for invoking FFI services
service ServiceClient {
  // Call a service method synchronously
  rpc Call(CallRequest) returns (CallResponse);
  
  // Call a service method asynchronously
  rpc CallAsync(CallRequest) returns (AsyncCallResponse);
  
  // Get result of an asynchronous call
  rpc GetAsyncResult(GetAsyncResultRequest) returns (CallResponse);
  
  // Call a streaming service method
  rpc StreamCall(CallRequest) returns (stream StreamResponse);
  
  // Client streaming call
  rpc ClientStreamCall(stream StreamRequest) returns (CallResponse);
  
  // Bidirectional streaming call
  rpc BidirectionalStreamCall(stream StreamRequest) returns (stream StreamResponse);
  
  // Cancel an in-progress call
  rpc CancelCall(CancelCallRequest) returns (CancelCallResponse);
}

// Request to call a service method
message CallRequest {
  // Target service ID
  string service_id = 1;
  
  // Method name to call
  string method = 2;
  
  // Input parameters (serialized according to method's input schema)
  bytes parameters = 3;
  
  // Call metadata
  map<string, string> metadata = 4;
  
  // Call timeout in milliseconds (0 = use default)
  int32 timeout_ms = 5;
  
  // Authentication token (if required)
  string auth_token = 6;
}

// Response from a synchronous call
message CallResponse {
  // Call status
  CallStatus status = 1;
  
  // Result data (serialized according to method's output schema)
  bytes result = 2;
  
  // Error details (if status is not OK)
  ErrorDetails error = 3;
  
  // Response metadata
  map<string, string> metadata = 4;
}

// Response from an asynchronous call
message AsyncCallResponse {
  // Unique call ID for retrieving the result later
  string call_id = 1;
  
  // Estimated completion time (Unix timestamp in milliseconds)
  int64 estimated_completion_time = 2;
  
  // Initial status
  CallStatus status = 3;
}

// Request to get an async call result
message GetAsyncResultRequest {
  // Call ID from AsyncCallResponse
  string call_id = 1;
  
  // Whether to wait for completion if not ready
  bool wait = 2;
  
  // Maximum wait time in milliseconds (if wait is true)
  int32 max_wait_ms = 3;
}

// Request for streaming calls
message StreamRequest {
  // Target service ID (only needed in first message)
  string service_id = 1;
  
  // Method name (only needed in first message)
  string method = 2;
  
  // Stream sequence number (must increase monotonically)
  int32 sequence = 3;
  
  // Input chunk (serialized according to method's input schema)
  bytes data = 4;
  
  // Whether this is the last chunk
  bool end_of_stream = 5;
  
  // Stream metadata
  map<string, string> metadata = 6;
}

// Response for streaming calls
message StreamResponse {
  // Stream sequence number (increases monotonically)
  int32 sequence = 1;
  
  // Output chunk (serialized according to method's output schema)
  bytes data = 2;
  
  // Whether this is the last chunk
  bool end_of_stream = 3;
  
  // Error details (if any)
  ErrorDetails error = 4;
  
  // Stream metadata
  map<string, string> metadata = 5;
}

// Request to cancel a call
message CancelCallRequest {
  // Call ID to cancel
  string call_id = 1;
}

// Response to cancel request
message CancelCallResponse {
  // Whether cancellation was successful
  bool success = 1;
  
  // Error message if cancellation failed
  string error_message = 2;
}

// Status of a service call
enum CallStatus {
  // Unknown status
  CALL_STATUS_UNSPECIFIED = 0;
  
  // Call completed successfully
  OK = 1;
  
  // Call is in progress
  IN_PROGRESS = 2;
  
  // Call failed
  FAILED = 3;
  
  // Call was cancelled
  CANCELLED = 4;
  
  // Call timed out
  TIMEOUT = 5;
}

// Detailed error information
message ErrorDetails {
  // Error code
  int32 code = 1;
  
  // Error message
  string message = 2;
  
  // Source of the error
  string source = 3;
  
  // Additional error details
  map<string, string> details = 4;
  
  // Stack trace (if available)
  string stack_trace = 5;
}
```

### 1.2. Type System API

The Type System API defines the schema system used for data serialization and validation.

#### 1.2.1 Schema

```protobuf
syntax = "proto3";

package hms.ffi.v1;

// Schema definition for type validation and serialization
message Schema {
  // Schema identifier
  string schema_id = 1;
  
  // Schema type
  SchemaType type = 2;
  
  // Format (for primitive types)
  string format = 3;
  
  // Human-readable description
  string description = 4;
  
  // For object types, the object fields
  repeated Field fields = 5;
  
  // For array types, the item schema
  Schema items = 6;
  
  // For map types, the key schema
  Schema key_schema = 7;
  
  // For map types, the value schema
  Schema value_schema = 8;
  
  // For enum types, the allowed values
  repeated EnumValue enum_values = 9;
  
  // For union types, the possible schemas
  repeated Schema one_of = 10;
  
  // For reference types, the referenced schema ID
  string ref = 11;
  
  // Validation constraints
  Constraints constraints = 12;
  
  // Default value (serialized)
  bytes default_value = 13;
  
  // Examples (serialized)
  repeated bytes examples = 14;
  
  // Additional schema metadata
  map<string, string> metadata = 15;
}

// Field definition within an object schema
message Field {
  // Field name
  string name = 1;
  
  // Field schema
  Schema schema = 2;
  
  // Whether field is required
  bool required = 3;
  
  // Default value (serialized)
  bytes default_value = 4;
  
  // Field description
  string description = 5;
}

// Enum value definition
message EnumValue {
  // String value
  string value = 1;
  
  // Display name
  string display_name = 2;
  
  // Description
  string description = 3;
}

// Schema constraints for validation
message Constraints {
  // String minimum length
  int32 min_length = 1;
  
  // String maximum length
  int32 max_length = 2;
  
  // String pattern (regex)
  string pattern = 3;
  
  // Number minimum value
  double minimum = 4;
  
  // Number maximum value
  double maximum = 5;
  
  // Whether minimum is exclusive
  bool exclusive_minimum = 6;
  
  // Whether maximum is exclusive
  bool exclusive_maximum = 7;
  
  // Number multiple of
  double multiple_of = 8;
  
  // Array minimum items
  int32 min_items = 9;
  
  // Array maximum items
  int32 max_items = 10;
  
  // Whether array items must be unique
  bool unique_items = 11;
  
  // Object minimum properties
  int32 min_properties = 12;
  
  // Object maximum properties
  int32 max_properties = 13;
}

// Schema types
enum SchemaType {
  // Unknown schema type
  SCHEMA_TYPE_UNSPECIFIED = 0;
  
  // Null value
  NULL = 1;
  
  // Boolean value
  BOOLEAN = 2;
  
  // Integer value
  INTEGER = 3;
  
  // Number value (floating point)
  NUMBER = 4;
  
  // String value
  STRING = 5;
  
  // Array value
  ARRAY = 6;
  
  // Object value
  OBJECT = 7;
  
  // Map value
  MAP = 8;
  
  // Enum value
  ENUM = 9;
  
  // Union type (one of multiple schemas)
  UNION = 10;
  
  // Reference to another schema
  REF = 11;
  
  // Any value
  ANY = 12;
  
  // Binary data
  BINARY = 13;
  
  // Date value
  DATE = 14;
  
  // Date-time value
  DATETIME = 15;
  
  // Time value
  TIME = 16;
  
  // Duration value
  DURATION = 17;
  
  // UUID value
  UUID = 18;
  
  // URI value
  URI = 19;
  
  // Email value
  EMAIL = 20;
}
```

#### 1.2.2 SchemaRegistry

```protobuf
syntax = "proto3";

package hms.ffi.v1;

import "schema.proto";

// Service for managing schemas
service SchemaRegistry {
  // Register a new schema
  rpc RegisterSchema(RegisterSchemaRequest) returns (RegisterSchemaResponse);
  
  // Get a schema by ID
  rpc GetSchema(GetSchemaRequest) returns (GetSchemaResponse);
  
  // List schemas matching criteria
  rpc ListSchemas(ListSchemasRequest) returns (ListSchemasResponse);
  
  // Validate data against a schema
  rpc ValidateSchema(ValidateSchemaRequest) returns (ValidateSchemaResponse);
}

// Request to register a schema
message RegisterSchemaRequest {
  // Schema to register
  Schema schema = 1;
}

// Response to schema registration
message RegisterSchemaResponse {
  // Whether registration was successful
  bool success = 1;
  
  // Error message if registration failed
  string error_message = 2;
  
  // Generated schema ID (if one wasn't provided)
  string schema_id = 3;
}

// Request to get a schema
message GetSchemaRequest {
  // Schema ID to retrieve
  string schema_id = 1;
  
  // Whether to resolve references
  bool resolve_refs = 2;
}

// Response with schema information
message GetSchemaResponse {
  // Requested schema
  Schema schema = 1;
  
  // Error message if retrieval failed
  string error_message = 2;
}

// Request to list schemas
message ListSchemasRequest {
  // Optional filter by name pattern
  string name_pattern = 1;
  
  // Optional filter by type
  SchemaType type = 2;
  
  // Maximum number of schemas to return
  int32 limit = 3;
  
  // Pagination token for additional results
  string page_token = 4;
}

// Response with list of schemas
message ListSchemasResponse {
  // List of schemas matching criteria
  repeated Schema schemas = 1;
  
  // Token for next page of results (if available)
  string next_page_token = 2;
}

// Request to validate data against a schema
message ValidateSchemaRequest {
  // Schema to validate against
  Schema schema = 1;
  
  // Data to validate (serialized)
  bytes data = 2;
}

// Response with validation result
message ValidateSchemaResponse {
  // Whether validation passed
  bool valid = 1;
  
  // Validation errors (if any)
  repeated ValidationError errors = 2;
}

// Validation error
message ValidationError {
  // Path to the invalid element
  string path = 1;
  
  // Error message
  string message = 2;
  
  // Error code
  string code = 3;
}
```

### 1.3. Transport API

The Transport API provides abstractions for the different transport mechanisms used in the FFI system.

```protobuf
syntax = "proto3";

package hms.ffi.v1;

// Service for managing transports
service TransportManager {
  // Register a new transport
  rpc RegisterTransport(RegisterTransportRequest) returns (RegisterTransportResponse);
  
  // Get information about available transports
  rpc GetTransports(GetTransportsRequest) returns (GetTransportsResponse);
  
  // Get optimal transport for a given source and target
  rpc GetOptimalTransport(GetOptimalTransportRequest) returns (GetOptimalTransportResponse);
}

// Request to register a transport
message RegisterTransportRequest {
  // Transport definition
  TransportDefinition transport = 1;
}

// Response to transport registration
message RegisterTransportResponse {
  // Whether registration was successful
  bool success = 1;
  
  // Error message if registration failed
  string error_message = 2;
}

// Request to get available transports
message GetTransportsRequest {
  // Optional filter by transport type
  TransportType type = 1;
}

// Response with transport information
message GetTransportsResponse {
  // Available transports
  repeated TransportDefinition transports = 1;
}

// Request to get optimal transport
message GetOptimalTransportRequest {
  // Source service ID
  string source_service_id = 1;
  
  // Target service ID
  string target_service_id = 2;
  
  // Performance requirements
  PerformanceRequirements requirements = 3;
}

// Response with optimal transport
message GetOptimalTransportResponse {
  // Recommended transport
  TransportDefinition transport = 1;
  
  // Expected performance characteristics
  PerformanceCharacteristics performance = 2;
}

// Transport definition
message TransportDefinition {
  // Transport ID
  string transport_id = 1;
  
  // Transport type
  TransportType type = 2;
  
  // Human-readable name
  string name = 3;
  
  // Description
  string description = 4;
  
  // Performance characteristics
  PerformanceCharacteristics performance = 5;
  
  // Configuration options
  map<string, string> config = 6;
  
  // Supported languages
  repeated string supported_languages = 7;
}

// Transport types
enum TransportType {
  // Unknown transport type
  TRANSPORT_TYPE_UNSPECIFIED = 0;
  
  // In-process transport (same process)
  IN_PROCESS = 1;
  
  // Shared memory transport (same machine)
  SHARED_MEMORY = 2;
  
  // Local socket transport (same machine)
  LOCAL_SOCKET = 3;
  
  // TCP/IP transport (network)
  TCP = 4;
  
  // HTTP/REST transport
  HTTP = 5;
  
  // gRPC transport
  GRPC = 6;
  
  // WebSocket transport
  WEBSOCKET = 7;
  
  // Message queue transport
  MESSAGE_QUEUE = 8;
}

// Performance characteristics
message PerformanceCharacteristics {
  // Average latency in microseconds
  int32 avg_latency_us = 1;
  
  // Maximum throughput in calls per second
  int32 max_throughput_cps = 2;
  
  // Maximum message size in bytes
  int32 max_message_size_bytes = 3;
  
  // Memory overhead per call in bytes
  int32 memory_overhead_bytes = 4;
}

// Performance requirements
message PerformanceRequirements {
  // Maximum acceptable latency in microseconds
  int32 max_latency_us = 1;
  
  // Minimum required throughput in calls per second
  int32 min_throughput_cps = 2;
  
  // Minimum required message size support in bytes
  int32 min_message_size_bytes = 3;
  
  // Maximum acceptable memory overhead in bytes
  int32 max_memory_overhead_bytes = 4;
}
```

### 1.4. Security API

The Security API provides mechanisms for securing FFI calls.

```protobuf
syntax = "proto3";

package hms.ffi.v1;

// Service for FFI security management
service SecurityManager {
  // Get security configuration
  rpc GetSecurityConfig(GetSecurityConfigRequest) returns (GetSecurityConfigResponse);
  
  // Check authorization for a call
  rpc CheckAuthorization(CheckAuthorizationRequest) returns (CheckAuthorizationResponse);
  
  // Generate access token
  rpc GenerateToken(GenerateTokenRequest) returns (GenerateTokenResponse);
  
  // Validate token
  rpc ValidateToken(ValidateTokenRequest) returns (ValidateTokenResponse);
  
  // Revoke token
  rpc RevokeToken(RevokeTokenRequest) returns (RevokeTokenResponse);
}

// Request to get security configuration
message GetSecurityConfigRequest {
  // Service ID to get config for
  string service_id = 1;
}

// Response with security configuration
message GetSecurityConfigResponse {
  // Security configuration
  SecurityConfig config = 1;
}

// Request to check authorization
message CheckAuthorizationRequest {
  // Service ID
  string service_id = 1;
  
  // Method name
  string method = 2;
  
  // Authentication token
  string auth_token = 3;
  
  // Caller identity (if available)
  string caller_id = 4;
}

// Response with authorization result
message CheckAuthorizationResponse {
  // Whether call is authorized
  bool authorized = 1;
  
  // Reason for denial (if not authorized)
  string denial_reason = 2;
}

// Request to generate token
message GenerateTokenRequest {
  // Identity to generate token for
  string identity = 1;
  
  // Roles to include in token
  repeated string roles = 2;
  
  // Expiration time in seconds
  int32 expiration_seconds = 3;
  
  // Additional claims
  map<string, string> additional_claims = 4;
}

// Response with generated token
message GenerateTokenResponse {
  // Generated token
  string token = 1;
  
  // Expiration timestamp (Unix timestamp in seconds)
  int64 expiration_timestamp = 2;
}

// Request to validate token
message ValidateTokenRequest {
  // Token to validate
  string token = 1;
}

// Response with token validation result
message ValidateTokenResponse {
  // Whether token is valid
  bool valid = 1;
  
  // Token claims (if valid)
  map<string, string> claims = 2;
  
  // Identity from token
  string identity = 3;
  
  // Roles from token
  repeated string roles = 4;
  
  // Expiration timestamp (Unix timestamp in seconds)
  int64 expiration_timestamp = 5;
  
  // Validation error (if not valid)
  string error = 6;
}

// Request to revoke token
message RevokeTokenRequest {
  // Token to revoke
  string token = 1;
}

// Response to token revocation
message RevokeTokenResponse {
  // Whether revocation was successful
  bool success = 1;
  
  // Error message if revocation failed
  string error_message = 2;
}

// Security configuration
message SecurityConfig {
  // Authentication requirements
  AuthenticationConfig authentication = 1;
  
  // Authorization requirements
  AuthorizationConfig authorization = 2;
  
  // Audit logging configuration
  AuditConfig audit = 3;
}

// Authentication configuration
message AuthenticationConfig {
  // Authentication type
  AuthType auth_type = 1;
  
  // Token configuration (if using tokens)
  TokenConfig token_config = 2;
  
  // Certificate configuration (if using certificates)
  CertConfig cert_config = 3;
}

// Token configuration
message TokenConfig {
  // Token issuer
  string issuer = 1;
  
  // Token audience
  string audience = 2;
  
  // Token lifetime in seconds
  int32 token_lifetime_seconds = 3;
  
  // Whether to use JWTs
  bool use_jwt = 4;
}

// Certificate configuration
message CertConfig {
  // Trusted CAs
  repeated string trusted_cas = 1;
  
  // Whether to check revocation
  bool check_revocation = 2;
  
  // Whether to allow self-signed certificates
  bool allow_self_signed = 3;
}

// Authorization configuration
message AuthorizationConfig {
  // Role definitions
  repeated RoleDefinition roles = 1;
  
  // Per-method permissions
  repeated MethodPermission method_permissions = 2;
}

// Role definition
message RoleDefinition {
  // Role name
  string name = 1;
  
  // Role description
  string description = 2;
  
  // Inherited roles
  repeated string inherits_from = 3;
}

// Method permission
message MethodPermission {
  // Method pattern (supports wildcards)
  string method_pattern = 1;
  
  // Allowed roles
  repeated string allowed_roles = 2;
}

// Audit configuration
message AuditConfig {
  // Whether to enable audit logging
  bool enabled = 1;
  
  // Log level
  LogLevel log_level = 2;
  
  // Whether to log request parameters
  bool log_parameters = 3;
  
  // Whether to log response data
  bool log_responses = 4;
}

// Log level
enum LogLevel {
  // Default log level
  LOG_LEVEL_DEFAULT = 0;
  
  // Debug level
  DEBUG = 1;
  
  // Info level
  INFO = 2;
  
  // Warning level
  WARNING = 3;
  
  // Error level
  ERROR = 4;
}
```

### 1.5. Observability API

The Observability API provides mechanisms for monitoring and debugging FFI calls.

```protobuf
syntax = "proto3";

package hms.ffi.v1;

// Service for FFI observability
service ObservabilityManager {
  // Get metrics for FFI usage
  rpc GetMetrics(GetMetricsRequest) returns (GetMetricsResponse);
  
  // Start tracing FFI calls
  rpc StartTracing(StartTracingRequest) returns (StartTracingResponse);
  
  // Stop tracing FFI calls
  rpc StopTracing(StopTracingRequest) returns (StopTracingResponse);
  
  // Get trace data
  rpc GetTraces(GetTracesRequest) returns (stream TraceData);
  
  // Stream logs
  rpc StreamLogs(StreamLogsRequest) returns (stream LogEntry);
}

// Request to get metrics
message GetMetricsRequest {
  // Service ID to get metrics for (optional)
  string service_id = 1;
  
  // Method name to get metrics for (optional)
  string method = 2;
  
  // Start time for metrics period (Unix timestamp in milliseconds)
  int64 start_time = 3;
  
  // End time for metrics period (Unix timestamp in milliseconds)
  int64 end_time = 4;
  
  // Metrics to include
  repeated MetricType metrics = 5;
}

// Response with metrics data
message GetMetricsResponse {
  // Metrics data
  repeated MetricData metrics = 1;
}

// Request to start tracing
message StartTracingRequest {
  // Filter for services to trace
  string service_filter = 1;
  
  // Filter for methods to trace
  string method_filter = 2;
  
  // Sampling rate (0.0-1.0)
  float sampling_rate = 3;
  
  // Maximum trace duration in seconds
  int32 max_duration_seconds = 4;
}

// Response to trace start request
message StartTracingResponse {
  // Trace session ID
  string trace_session_id = 1;
}

// Request to stop tracing
message StopTracingRequest {
  // Trace session ID
  string trace_session_id = 1;
}

// Response to trace stop request
message StopTracingResponse {
  // Whether stop was successful
  bool success = 1;
  
  // Number of traces collected
  int32 trace_count = 2;
}

// Request to get traces
message GetTracesRequest {
  // Trace session ID
  string trace_session_id = 1;
  
  // Maximum number of traces to return
  int32 limit = 2;
}

// Trace data
message TraceData {
  // Trace ID
  string trace_id = 1;
  
  // Service ID
  string service_id = 2;
  
  // Method called
  string method = 3;
  
  // Call start time (Unix timestamp in milliseconds)
  int64 start_time = 4;
  
  // Call duration in milliseconds
  int32 duration_ms = 5;
  
  // Call status
  CallStatus status = 6;
  
  // Call spans
  repeated TraceSpan spans = 7;
  
  // Call metadata
  map<string, string> metadata = 8;
}

// Trace span
message TraceSpan {
  // Span ID
  string span_id = 1;
  
  // Parent span ID
  string parent_span_id = 2;
  
  // Span name
  string name = 3;
  
  // Span start time (Unix timestamp in milliseconds)
  int64 start_time = 4;
  
  // Span duration in milliseconds
  int32 duration_ms = 5;
  
  // Span attributes
  map<string, string> attributes = 6;
  
  // Span events
  repeated SpanEvent events = 7;
}

// Span event
message SpanEvent {
  // Event name
  string name = 1;
  
  // Event time (Unix timestamp in milliseconds)
  int64 time = 2;
  
  // Event attributes
  map<string, string> attributes = 3;
}

// Request to stream logs
message StreamLogsRequest {
  // Service ID filter (optional)
  string service_id = 1;
  
  // Log level filter
  LogLevel min_level = 2;
  
  // Filter pattern
  string filter_pattern = 3;
}

// Log entry
message LogEntry {
  // Log timestamp (Unix timestamp in milliseconds)
  int64 timestamp = 1;
  
  // Log level
  LogLevel level = 2;
  
  // Service ID
  string service_id = 3;
  
  // Method name (if applicable)
  string method = 4;
  
  // Log message
  string message = 5;
  
  // Log metadata
  map<string, string> metadata = 6;
}

// Metric data
message MetricData {
  // Metric type
  MetricType type = 1;
  
  // Service ID
  string service_id = 2;
  
  // Method name
  string method = 3;
  
  // Time series data points
  repeated DataPoint data_points = 4;
}

// Data point in a time series
message DataPoint {
  // Timestamp (Unix timestamp in milliseconds)
  int64 timestamp = 1;
  
  // Value
  double value = 2;
}

// Metric types
enum MetricType {
  // Unknown metric type
  METRIC_TYPE_UNSPECIFIED = 0;
  
  // Calls per second
  CALLS_PER_SECOND = 1;
  
  // Error rate
  ERROR_RATE = 2;
  
  // Average latency
  AVG_LATENCY = 3;
  
  // 95th percentile latency
  P95_LATENCY = 4;
  
  // 99th percentile latency
  P99_LATENCY = 5;
  
  // Active calls
  ACTIVE_CALLS = 6;
  
  // Memory usage
  MEMORY_USAGE = 7;
  
  // CPU usage
  CPU_USAGE = 8;
}
```

## 2. Client API

The Client API includes high-level interfaces for calling FFI services from each supported language.

### 2.1 Go Client API

```go
// Package hmsffi provides the Go client API for HMS Foreign Function Interface
package hmsffi

import (
    "context"
    "time"
)

// Client is the main entry point for FFI operations
type Client interface {
    // GetService returns a service client for a specific service
    GetService(ctx context.Context, serviceID string) (ServiceClient, error)
    
    // ListServices returns available services matching a pattern
    ListServices(ctx context.Context, pattern string) ([]ServiceInfo, error)
    
    // Close releases resources used by the client
    Close() error
}

// ServiceClient provides methods for interacting with a specific FFI service
type ServiceClient interface {
    // Call invokes a service method synchronously
    Call(ctx context.Context, method string, params interface{}, result interface{}) error
    
    // CallAsync invokes a service method asynchronously
    CallAsync(ctx context.Context, method string, params interface{}) (AsyncCall, error)
    
    // StreamCall invokes a streaming service method
    StreamCall(ctx context.Context, method string, params interface{}) (Stream, error)
    
    // Close releases resources used by the service client
    Close() error
}

// AsyncCall represents an asynchronous FFI call
type AsyncCall interface {
    // ID returns the unique identifier for this call
    ID() string
    
    // Result waits for the call to complete and returns the result
    Result(ctx context.Context, result interface{}) error
    
    // Cancel attempts to cancel the in-progress call
    Cancel() error
    
    // Status returns the current status of the call
    Status() CallStatus
}

// Stream represents a bidirectional stream for FFI calls
type Stream interface {
    // Send sends data to the stream
    Send(data interface{}) error
    
    // Receive receives data from the stream
    Receive(result interface{}) error
    
    // Close closes the stream
    Close() error
    
    // IsClosed returns whether the stream is closed
    IsClosed() bool
}

// CallStatus represents the status of an FFI call
type CallStatus int

// Call status values
const (
    CallStatusUnknown CallStatus = iota
    CallStatusOK
    CallStatusInProgress
    CallStatusFailed
    CallStatusCancelled
    CallStatusTimeout
)

// ServiceInfo provides information about an FFI service
type ServiceInfo struct {
    ID          string
    Name        string
    Description string
    Version     string
    Methods     []MethodInfo
    Metadata    map[string]string
}

// MethodInfo provides information about a service method
type MethodInfo struct {
    Name        string
    Description string
    IsStreaming bool
    StreamType  StreamType
    Metadata    map[string]string
}

// StreamType represents the type of streaming method
type StreamType int

// Stream type values
const (
    StreamTypeUnknown StreamType = iota
    StreamTypeServerStreaming
    StreamTypeClientStreaming
    StreamTypeBidirectional
)

// ClientOptions contains options for creating an FFI client
type ClientOptions struct {
    Timeout     time.Duration
    MaxRetries  int
    Transport   TransportType
    AuthToken   string
    Logger      Logger
}

// TransportType represents the type of transport to use
type TransportType int

// Transport type values
const (
    TransportTypeDefault TransportType = iota
    TransportTypeInProcess
    TransportTypeSharedMemory
    TransportTypeLocalSocket
    TransportTypeTCP
    TransportTypeHTTP
    TransportTypeGRPC
    TransportTypeWebSocket
    TransportTypeMessageQueue
)

// Logger interface for client logging
type Logger interface {
    Debug(msg string, keyvals ...interface{})
    Info(msg string, keyvals ...interface{})
    Warn(msg string, keyvals ...interface{})
    Error(msg string, keyvals ...interface{})
}

// NewClient creates a new FFI client
func NewClient(options ClientOptions) (Client, error) {
    // Implementation
    return nil, nil
}
```

### 2.2. Rust Client API

```rust
//! HMS FFI client API for Rust

use std::collections::HashMap;
use std::fmt;
use std::future::Future;
use std::time::Duration;

/// Main entry point for FFI operations
pub trait Client {
    /// Get a service client for a specific service
    fn get_service(&self, service_id: &str) -> Result<Box<dyn ServiceClient>, Error>;
    
    /// List available services matching a pattern
    fn list_services(&self, pattern: &str) -> Result<Vec<ServiceInfo>, Error>;
    
    /// Close and release resources
    fn close(&self) -> Result<(), Error>;
}

/// Client for interacting with a specific FFI service
pub trait ServiceClient {
    /// Call a service method synchronously
    fn call<P, R>(&self, method: &str, params: P) -> Result<R, Error>
    where
        P: Serialize,
        R: for<'de> Deserialize<'de>;
    
    /// Call a service method asynchronously
    fn call_async<P, R>(&self, method: &str, params: P) -> impl Future<Output = Result<R, Error>>
    where
        P: Serialize,
        R: for<'de> Deserialize<'de>;
    
    /// Create a stream for a streaming method
    fn stream_call<P, R>(&self, method: &str, params: P) -> Result<Box<dyn Stream<Item = Result<R, Error>>>, Error>
    where
        P: Serialize,
        R: for<'de> Deserialize<'de>;
    
    /// Close and release resources
    fn close(&self) -> Result<(), Error>;
}

/// Status of an FFI call
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CallStatus {
    Unknown,
    Ok,
    InProgress,
    Failed,
    Cancelled,
    Timeout,
}

/// Information about an FFI service
#[derive(Debug, Clone)]
pub struct ServiceInfo {
    pub id: String,
    pub name: String,
    pub description: String,
    pub version: String,
    pub methods: Vec<MethodInfo>,
    pub metadata: HashMap<String, String>,
}

/// Information about a service method
#[derive(Debug, Clone)]
pub struct MethodInfo {
    pub name: String,
    pub description: String,
    pub is_streaming: bool,
    pub stream_type: StreamType,
    pub metadata: HashMap<String, String>,
}

/// Type of streaming method
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StreamType {
    Unknown,
    ServerStreaming,
    ClientStreaming,
    Bidirectional,
}

/// Options for creating an FFI client
#[derive(Debug, Clone)]
pub struct ClientOptions {
    pub timeout: Option<Duration>,
    pub max_retries: Option<u32>,
    pub transport: Option<TransportType>,
    pub auth_token: Option<String>,
    pub log_level: Option<LogLevel>,
}

/// Transport type
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransportType {
    Default,
    InProcess,
    SharedMemory,
    LocalSocket,
    Tcp,
    Http,
    Grpc,
    WebSocket,
    MessageQueue,
}

/// Log level
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LogLevel {
    Debug,
    Info,
    Warn,
    Error,
}

/// FFI error
#[derive(Debug)]
pub struct Error {
    pub code: i32,
    pub message: String,
    pub source: Option<String>,
    pub details: HashMap<String, String>,
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "FFI error {}: {}", self.code, self.message)
    }
}

impl std::error::Error for Error {}

/// Create a new FFI client
pub fn new_client(options: ClientOptions) -> Result<Box<dyn Client>, Error> {
    // Implementation
    todo!()
}
```

### 2.3. Python Client API

```python
"""HMS FFI client API for Python."""

from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from enum import Enum
import asyncio
import logging
from dataclasses import dataclass

T = TypeVar('T')
P = TypeVar('P')
R = TypeVar('R')

class CallStatus(Enum):
    """Status of an FFI call."""
    UNKNOWN = 0
    OK = 1
    IN_PROGRESS = 2
    FAILED = 3
    CANCELLED = 4
    TIMEOUT = 5

class StreamType(Enum):
    """Type of streaming method."""
    UNKNOWN = 0
    SERVER_STREAMING = 1
    CLIENT_STREAMING = 2
    BIDIRECTIONAL = 3

class TransportType(Enum):
    """Transport type for FFI calls."""
    DEFAULT = 0
    IN_PROCESS = 1
    SHARED_MEMORY = 2
    LOCAL_SOCKET = 3
    TCP = 4
    HTTP = 5
    GRPC = 6
    WEBSOCKET = 7
    MESSAGE_QUEUE = 8

class LogLevel(Enum):
    """Log level for FFI client."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

@dataclass
class MethodInfo:
    """Information about a service method."""
    name: str
    description: str
    is_streaming: bool
    stream_type: StreamType
    metadata: Dict[str, str]

@dataclass
class ServiceInfo:
    """Information about an FFI service."""
    id: str
    name: str
    description: str
    version: str
    methods: List[MethodInfo]
    metadata: Dict[str, str]

class Error(Exception):
    """FFI error."""
    def __init__(self, code: int, message: str, source: Optional[str] = None, 
                 details: Optional[Dict[str, str]] = None):
        self.code = code
        self.message = message
        self.source = source
        self.details = details or {}
        super().__init__(f"{message} (code: {code})")

class AsyncCall(Generic[R]):
    """Represents an asynchronous FFI call."""
    
    def __init__(self, call_id: str):
        self.call_id = call_id
    
    def result(self, timeout: Optional[float] = None) -> R:
        """Wait for the call to complete and return the result."""
        raise NotImplementedError()
    
    async def async_result(self, timeout: Optional[float] = None) -> R:
        """Asynchronously wait for the call to complete and return the result."""
        raise NotImplementedError()
    
    def cancel(self) -> bool:
        """Attempt to cancel the in-progress call."""
        raise NotImplementedError()
    
    @property
    def status(self) -> CallStatus:
        """Get the current status of the call."""
        raise NotImplementedError()

class Stream(Generic[P, R]):
    """Represents a bidirectional stream for FFI calls."""
    
    def send(self, data: P) -> None:
        """Send data to the stream."""
        raise NotImplementedError()
    
    def receive(self) -> R:
        """Receive data from the stream."""
        raise NotImplementedError()
    
    async def async_send(self, data: P) -> None:
        """Asynchronously send data to the stream."""
        raise NotImplementedError()
    
    async def async_receive(self) -> R:
        """Asynchronously receive data from the stream."""
        raise NotImplementedError()
    
    def close(self) -> None:
        """Close the stream."""
        raise NotImplementedError()
    
    @property
    def is_closed(self) -> bool:
        """Check if the stream is closed."""
        raise NotImplementedError()

class ServiceClient:
    """Client for interacting with a specific FFI service."""
    
    def __init__(self, service_id: str):
        self.service_id = service_id
    
    def call(self, method: str, params: Any) -> Any:
        """Call a service method synchronously."""
        raise NotImplementedError()
    
    def call_async(self, method: str, params: Any) -> AsyncCall:
        """Call a service method asynchronously."""
        raise NotImplementedError()
    
    async def async_call(self, method: str, params: Any) -> Any:
        """Call a service method using asyncio."""
        raise NotImplementedError()
    
    def stream_call(self, method: str, params: Any) -> Stream:
        """Create a stream for a streaming method."""
        raise NotImplementedError()
    
    def close(self) -> None:
        """Close and release resources."""
        raise NotImplementedError()

class Client:
    """Main entry point for FFI operations."""
    
    def __init__(self, timeout: Optional[float] = None, max_retries: int = 3,
                 transport: TransportType = TransportType.DEFAULT,
                 auth_token: Optional[str] = None,
                 log_level: LogLevel = LogLevel.INFO):
        self.timeout = timeout
        self.max_retries = max_retries
        self.transport = transport
        self.auth_token = auth_token
        self.log_level = log_level
    
    def get_service(self, service_id: str) -> ServiceClient:
        """Get a service client for a specific service."""
        raise NotImplementedError()
    
    def list_services(self, pattern: str = "*") -> List[ServiceInfo]:
        """List available services matching a pattern."""
        raise NotImplementedError()
    
    def close(self) -> None:
        """Close and release resources."""
        raise NotImplementedError()

def create_client(timeout: Optional[float] = None, max_retries: int = 3,
                  transport: TransportType = TransportType.DEFAULT,
                  auth_token: Optional[str] = None,
                  log_level: LogLevel = LogLevel.INFO) -> Client:
    """Create a new FFI client."""
    # Implementation
    pass
```

## 3. Server API

The Server API includes interfaces for implementing FFI services in each supported language.

### 3.1 Go Server API

```go
// Package hmsffi provides the Go server API for HMS Foreign Function Interface
package hmsffi

import (
    "context"
    "time"
)

// ServiceHandler is the interface that must be implemented by FFI service handlers
type ServiceHandler interface {
    // ServiceInfo returns information about this service
    ServiceInfo() ServiceInfo
}

// MethodHandler handles a specific method call
type MethodHandler func(ctx context.Context, params []byte) ([]byte, error)

// StreamHandler handles a streaming method call
type StreamHandler func(ctx context.Context, stream Stream) error

// Server is the main entry point for FFI service hosting
type Server interface {
    // RegisterService registers a service handler
    RegisterService(handler ServiceHandler) error
    
    // RegisterMethod registers a method handler
    RegisterMethod(serviceID, method string, handler MethodHandler) error
    
    // RegisterStreamMethod registers a streaming method handler
    RegisterStreamMethod(serviceID, method string, handler StreamHandler) error
    
    // Start starts the server
    Start() error
    
    // Stop stops the server
    Stop() error
    
    // IsRunning returns whether the server is running
    IsRunning() bool
}

// ServerOptions contains options for creating an FFI server
type ServerOptions struct {
    // Server name
    Name string
    
    // Transports to enable
    Transports []TransportType
    
    // Authentication configuration
    AuthConfig *AuthConfig
    
    // Maximum concurrent calls
    MaxConcurrentCalls int
    
    // Call timeout
    CallTimeout time.Duration
    
    // Logger for server logging
    Logger Logger
}

// AuthConfig contains authentication configuration
type AuthConfig struct {
    // Authentication type
    Type AuthType
    
    // Token validation function (for token auth)
    TokenValidator func(token string) (bool, map[string]string, error)
    
    // Certificate validation settings (for cert auth)
    CertValidation *CertValidation
}

// AuthType represents the type of authentication
type AuthType int

// Authentication types
const (
    AuthTypeNone AuthType = iota
    AuthTypeToken
    AuthTypeCert
    AuthTypeCustom
)

// CertValidation contains certificate validation settings
type CertValidation struct {
    // Trusted CA certificates
    TrustedCAs [][]byte
    
    // Whether to check certificate revocation
    CheckRevocation bool
    
    // Whether to allow self-signed certificates
    AllowSelfSigned bool
}

// NewServer creates a new FFI server
func NewServer(options ServerOptions) (Server, error) {
    // Implementation
    return nil, nil
}

// Service is a helper for implementing FFI services
type Service struct {
    // Service ID
    ID string
    
    // Service name
    Name string
    
    // Service description
    Description string
    
    // Service version
    Version string
    
    // Service metadata
    Metadata map[string]string
}

// Method registers a method handler with the service
func (s *Service) Method(name string, handler interface{}) {
    // Implementation
}

// StreamMethod registers a streaming method handler with the service
func (s *Service) StreamMethod(name string, handler interface{}) {
    // Implementation
}
```

### 3.2 Rust Server API

```rust
//! HMS FFI server API for Rust

use std::collections::HashMap;
use std::error::Error as StdError;
use std::fmt;
use std::future::Future;
use std::time::Duration;

/// Main entry point for FFI service hosting
pub trait Server {
    /// Register a service handler
    fn register_service(&mut self, handler: Box<dyn ServiceHandler>) -> Result<(), Error>;
    
    /// Register a method handler
    fn register_method<F, Fut, P, R>(&mut self, service_id: &str, method: &str, handler: F) -> Result<(), Error>
    where
        F: Fn(P) -> Fut + Send + Sync + 'static,
        Fut: Future<Output = Result<R, Error>> + Send + 'static,
        P: for<'de> Deserialize<'de> + Send + 'static,
        R: Serialize + Send + 'static;
    
    /// Register a streaming method handler
    fn register_stream_method<F, S>(&mut self, service_id: &str, method: &str, handler: F) -> Result<(), Error>
    where
        F: Fn(Box<dyn Stream>) -> Result<(), Error> + Send + Sync + 'static,
        S: Stream + Send + 'static;
    
    /// Start the server
    fn start(&mut self) -> Result<(), Error>;
    
    /// Stop the server
    fn stop(&mut self) -> Result<(), Error>;
    
    /// Check if the server is running
    fn is_running(&self) -> bool;
}

/// Handler for FFI services
pub trait ServiceHandler: Send + Sync {
    /// Get information about this service
    fn service_info(&self) -> ServiceInfo;
}

/// Status of an FFI call
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CallStatus {
    Unknown,
    Ok,
    InProgress,
    Failed,
    Cancelled,
    Timeout,
}

/// Information about an FFI service
#[derive(Debug, Clone)]
pub struct ServiceInfo {
    pub id: String,
    pub name: String,
    pub description: String,
    pub version: String,
    pub methods: Vec<MethodInfo>,
    pub metadata: HashMap<String, String>,
}

/// Information about a service method
#[derive(Debug, Clone)]
pub struct MethodInfo {
    pub name: String,
    pub description: String,
    pub is_streaming: bool,
    pub stream_type: StreamType,
    pub metadata: HashMap<String, String>,
}

/// Type of streaming method
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StreamType {
    Unknown,
    ServerStreaming,
    ClientStreaming,
    Bidirectional,
}

/// Options for creating an FFI server
#[derive(Debug, Clone)]
pub struct ServerOptions {
    pub name: String,
    pub transports: Vec<TransportType>,
    pub auth_config: Option<AuthConfig>,
    pub max_concurrent_calls: Option<usize>,
    pub call_timeout: Option<Duration>,
    pub log_level: Option<LogLevel>,
}

/// Authentication configuration
#[derive(Debug, Clone)]
pub struct AuthConfig {
    pub auth_type: AuthType,
    pub token_validation: Option<Box<dyn Fn(&str) -> Result<bool, Error> + Send + Sync>>,
    pub cert_validation: Option<CertValidation>,
}

/// Authentication type
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AuthType {
    None,
    Token,
    Cert,
    Custom,
}

/// Certificate validation settings
#[derive(Debug, Clone)]
pub struct CertValidation {
    pub trusted_cas: Vec<Vec<u8>>,
    pub check_revocation: bool,
    pub allow_self_signed: bool,
}

/// Transport type
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransportType {
    Default,
    InProcess,
    SharedMemory,
    LocalSocket,
    Tcp,
    Http,
    Grpc,
    WebSocket,
    MessageQueue,
}

/// Log level
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LogLevel {
    Debug,
    Info,
    Warn,
    Error,
}

/// FFI error
#[derive(Debug)]
pub struct Error {
    pub code: i32,
    pub message: String,
    pub source: Option<String>,
    pub details: HashMap<String, String>,
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "FFI error {}: {}", self.code, self.message)
    }
}

impl StdError for Error {}

/// Create a new FFI server
pub fn new_server(options: ServerOptions) -> Result<Box<dyn Server>, Error> {
    // Implementation
    todo!()
}

/// Helper for implementing FFI services
#[macro_export]
macro_rules! ffi_service {
    ($name:ident, $id:expr) => {
        // Implementation
    };
}

/// Helper for implementing FFI methods
#[macro_export]
macro_rules! ffi_method {
    ($name:ident, $fn:expr) => {
        // Implementation
    };
}

/// Helper for implementing FFI streaming methods
#[macro_export]
macro_rules! ffi_stream_method {
    ($name:ident, $fn:expr) => {
        // Implementation
    };
}
```

### 3.3 Python Server API

```python
"""HMS FFI server API for Python."""

from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, Generic
from enum import Enum
import asyncio
import inspect
import logging
from dataclasses import dataclass
import functools

T = TypeVar('T')
P = TypeVar('P')
R = TypeVar('R')

class CallStatus(Enum):
    """Status of an FFI call."""
    UNKNOWN = 0
    OK = 1
    IN_PROGRESS = 2
    FAILED = 3
    CANCELLED = 4
    TIMEOUT = 5

class StreamType(Enum):
    """Type of streaming method."""
    UNKNOWN = 0
    SERVER_STREAMING = 1
    CLIENT_STREAMING = 2
    BIDIRECTIONAL = 3

class TransportType(Enum):
    """Transport type for FFI calls."""
    DEFAULT = 0
    IN_PROCESS = 1
    SHARED_MEMORY = 2
    LOCAL_SOCKET = 3
    TCP = 4
    HTTP = 5
    GRPC = 6
    WEBSOCKET = 7
    MESSAGE_QUEUE = 8

class AuthType(Enum):
    """Authentication type for FFI service."""
    NONE = 0
    TOKEN = 1
    CERT = 2
    CUSTOM = 3

class LogLevel(Enum):
    """Log level for FFI server."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

@dataclass
class MethodInfo:
    """Information about a service method."""
    name: str
    description: str
    is_streaming: bool
    stream_type: StreamType
    metadata: Dict[str, str]

@dataclass
class ServiceInfo:
    """Information about an FFI service."""
    id: str
    name: str
    description: str
    version: str
    methods: List[MethodInfo]
    metadata: Dict[str, str]

@dataclass
class CertValidation:
    """Certificate validation settings."""
    trusted_cas: List[bytes]
    check_revocation: bool = True
    allow_self_signed: bool = False

@dataclass
class AuthConfig:
    """Authentication configuration."""
    auth_type: AuthType
    token_validator: Optional[Callable[[str], bool]] = None
    cert_validation: Optional[CertValidation] = None

class Error(Exception):
    """FFI error."""
    def __init__(self, code: int, message: str, source: Optional[str] = None, 
                 details: Optional[Dict[str, str]] = None):
        self.code = code
        self.message = message
        self.source = source
        self.details = details or {}
        super().__init__(f"{message} (code: {code})")

class Stream(Generic[P, R]):
    """Represents a bidirectional stream for FFI calls."""
    
    def send(self, data: R) -> None:
        """Send data to the stream."""
        raise NotImplementedError()
    
    def receive(self) -> P:
        """Receive data from the stream."""
        raise NotImplementedError()
    
    async def async_send(self, data: R) -> None:
        """Asynchronously send data to the stream."""
        raise NotImplementedError()
    
    async def async_receive(self) -> P:
        """Asynchronously receive data from the stream."""
        raise NotImplementedError()
    
    def close(self) -> None:
        """Close the stream."""
        raise NotImplementedError()
    
    @property
    def is_closed(self) -> bool:
        """Check if the stream is closed."""
        raise NotImplementedError()

class ServiceHandler:
    """Base class for FFI service handlers."""
    
    @property
    def service_info(self) -> ServiceInfo:
        """Get information about this service."""
        raise NotImplementedError()

class Server:
    """Main entry point for FFI service hosting."""
    
    def __init__(self, name: str, transports: List[TransportType] = None,
                 auth_config: Optional[AuthConfig] = None,
                 max_concurrent_calls: int = 100,
                 call_timeout: float = 30.0,
                 log_level: LogLevel = LogLevel.INFO):
        self.name = name
        self.transports = transports or [TransportType.DEFAULT]
        self.auth_config = auth_config
        self.max_concurrent_calls = max_concurrent_calls
        self.call_timeout = call_timeout
        self.log_level = log_level
        self._running = False
    
    def register_service(self, handler: ServiceHandler) -> None:
        """Register a service handler."""
        raise NotImplementedError()
    
    def register_method(self, service_id: str, method: str, 
                        handler: Callable[[Any], Any]) -> None:
        """Register a method handler."""
        raise NotImplementedError()
    
    def register_stream_method(self, service_id: str, method: str,
                              handler: Callable[[Stream], None]) -> None:
        """Register a streaming method handler."""
        raise NotImplementedError()
    
    def start(self) -> None:
        """Start the server."""
        raise NotImplementedError()
    
    def stop(self) -> None:
        """Stop the server."""
        raise NotImplementedError()
    
    @property
    def is_running(self) -> bool:
        """Check if the server is running."""
        return self._running

def create_server(name: str, transports: List[TransportType] = None,
                 auth_config: Optional[AuthConfig] = None,
                 max_concurrent_calls: int = 100,
                 call_timeout: float = 30.0,
                 log_level: LogLevel = LogLevel.INFO) -> Server:
    """Create a new FFI server."""
    # Implementation
    pass

def service(id: str, name: Optional[str] = None, description: Optional[str] = None,
           version: str = "1.0.0", metadata: Optional[Dict[str, str]] = None):
    """Decorator to define an FFI service."""
    def decorator(cls):
        # Implementation
        return cls
    return decorator

def method(name: Optional[str] = None, description: Optional[str] = None, 
          metadata: Optional[Dict[str, str]] = None):
    """Decorator to define an FFI method."""
    def decorator(func):
        # Implementation
        return func
    return decorator

def stream_method(name: Optional[str] = None, description: Optional[str] = None,
                 stream_type: StreamType = StreamType.BIDIRECTIONAL, 
                 metadata: Optional[Dict[str, str]] = None):
    """Decorator to define an FFI streaming method."""
    def decorator(func):
        # Implementation
        return func
    return decorator
```

## 4. Serialization Formats

The FFI system supports multiple serialization formats:

### 4.1 Protocol Buffers

Protocol Buffers is the primary serialization format used for interface definitions and most structured data.

Example Protocol Buffer definition:
```protobuf
syntax = "proto3";

package hms.healthcare.v1;

message PatientRecord {
  string id = 1;
  string name = 2;
  int32 age = 3;
  Gender gender = 4;
  repeated ContactInfo contacts = 5;
  map<string, string> attributes = 6;
}

enum Gender {
  GENDER_UNSPECIFIED = 0;
  MALE = 1;
  FEMALE = 2;
  OTHER = 3;
}

message ContactInfo {
  string type = 1;
  string value = 2;
}
```

### 4.2 CBOR

CBOR (Concise Binary Object Representation) is used for efficient binary serialization when schema-based validation is not required.

Example CBOR data:
```
A3                     # map(3)
   63                  # text(3)
      666F6F           # "foo"
   01                  # unsigned(1)
   63                  # text(3)
      626172           # "bar"
   02                  # unsigned(2)
   63                  # text(3)
      62617A           # "baz"
   83                  # array(3)
      01               # unsigned(1)
      02               # unsigned(2)
      03               # unsigned(3)
```

### 4.3 JSON

JSON is used for human-readable data and debugging.

Example JSON data:
```json
{
  "foo": 1,
  "bar": 2,
  "baz": [1, 2, 3]
}
```

## 5. Security Considerations

### 5.1 Authentication

The FFI system supports multiple authentication mechanisms:

1. **Token-based authentication**: Using JWTs or similar tokens
2. **Certificate-based authentication**: Using X.509 certificates
3. **Custom authentication**: For specialized scenarios

### 5.2 Authorization

Authorization is based on roles and permissions:

1. **Role-based access control**: Methods can be restricted to specific roles
2. **Method-level permissions**: Fine-grained control over which methods can be called

### 5.3 Secure Communication

All FFI communication should be secured:

1. **In-process**: Already secure by nature
2. **Same machine**: Using secure local mechanisms
3. **Network**: Using TLS for all traffic

### 5.4 Input Validation

All inputs must be validated:

1. **Schema-based validation**: Using the schema system
2. **Custom validation**: Additional validation in handlers

## 6. Error Handling

### 6.1 Error Codes

Standard error codes are defined for common errors:

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

### 6.2 Error Details

Errors include detailed information:

1. **Error message**: Human-readable description
2. **Error source**: Component that generated the error
3. **Stack trace**: Where available
4. **Additional details**: Context-specific information

## 7. Versioning

### 7.1 Interface Versioning

Interfaces are versioned using semantic versioning:

1. **Major version**: Incompatible API changes
2. **Minor version**: Backward-compatible additions
3. **Patch version**: Backward-compatible bug fixes

### 7.2 Compatibility Checking

The FFI system checks compatibility between service versions:

1. **Strict compatibility**: For critical services
2. **Loose compatibility**: For less critical services

## 8. Implementation Notes

### 8.1 Performance Considerations

1. **Zero-copy**: Use zero-copy mechanisms where possible
2. **Transport selection**: Automatically select the most efficient transport
3. **Pooling**: Use object pooling to reduce allocation overhead
4. **Caching**: Cache serialization results for frequently used data

### 8.2 Deployment Considerations

1. **Language availability**: Ensure all required languages are available
2. **Transport availability**: Ensure all required transports are available
3. **Resource allocation**: Allocate sufficient resources for FFI overhead

## 9. Future Extensions

### 9.1 Planned Extensions

1. **Distributed tracing**: End-to-end tracing across language boundaries
2. **Dynamic loading**: Runtime loading of FFI components
3. **Streaming optimizations**: Advanced streaming capabilities
4. **Schema evolution**: Improved schema versioning and migration