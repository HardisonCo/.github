# HMS Foreign Function Interface (FFI) Implementation Plan

This document outlines the comprehensive plan for implementing FFI across all 33+ system components in the HMS system.

## 1. Overview

The HMS Foreign Function Interface (FFI) system enables cross-language communication between different components of the HMS ecosystem. Each component requires protocol buffer (proto) definitions to standardize data structures and service interfaces for cross-language communication.

### 1.1 Current Status

Currently, the `hms-ffi-protos` directory contains proto definitions for the following components:

- Core (common definitions)
- ACH (transactions)
- API (authentication)
- CDF (debate)
- EMR (patient)
- ESR (session)
- ETL (pipeline)
- GOV (policy)
- SYS (deployment)

However, we need to implement proto definitions for all 33+ system components to ensure complete interoperability.

### 1.2 Objectives

- Create proto files for all HMS system components following a standardized approach
- Ensure consistency in naming, versioning, and structure
- Implement language-specific bindings for all components
- Create tests to verify FFI functionality
- Develop documentation for FFI usage

## 2. Component Analysis

### 2.1 Existing Components with Proto Files

| Component | Purpose | Proto Status | Priority |
|-----------|---------|--------------|----------|
| HMS-CORE | Common definitions | Complete | Done |
| HMS-ACH | Payment processing | Basic | High |
| HMS-API | API interfaces | Basic | High |
| HMS-CDF | Decision framework | Basic | Medium |
| HMS-EMR | Electronic medical records | Basic | High |
| HMS-ESR | Session records | Basic | Medium |
| HMS-ETL | Data pipeline | Basic | Medium |
| HMS-GOV | Governance | Basic | Medium |
| HMS-SYS | System management | Basic | High |

### 2.2 Components Requiring Proto Files

| Component | Purpose | Priority |
|-----------|---------|----------|
| HMS-A2A | Agent-to-agent communication | Critical |
| HMS-ABC | Component management | High |
| HMS-ACT | Workflow actions | High |
| HMS-AGT | Agent framework | Critical |
| HMS-AGX | Agent execution | Critical |
| HMS-CUR | Currency/financial | Medium |
| HMS-DEV | Development tools | Low |
| HMS-DOC | Documentation | Low |
| HMS-EDU | Education | Medium |
| HMS-EHR | Electronic health records | High |
| HMS-ESQ | Data query system | Medium |
| HMS-FLD | Field operations | Medium |
| HMS-KNO | Knowledge system | High |
| HMS-LLM | Language model integration | Critical |
| HMS-MCP | Model Context Protocol | Critical |
| HMS-MFE | Micro frontend | Medium |
| HMS-MKT | Marketing | Low |
| HMS-NFO | Knowledge framework | High |
| HMS-OMS | Order management | High |
| HMS-OPS | Operations | Medium |
| HMS-RED | Redaction/security | High |
| HMS-SCM | Supply chain | Medium |
| HMS-SKL | Skills framework | High |
| HMS-SME | Subject matter expertise | Medium |
| HMS-UHC | Universal health coverage | High |
| HMS-UTL | Utilities | Low |

## 3. Implementation Approach

### 3.1 Proto File Structure

Each component will have a proto file structure following this standard:

```
hms-ffi-protos/
  hms/
    [component-code]/
      v1/
        [domain].proto
```

For example:
- `hms/a2a/v1/agent.proto`
- `hms/a2a/v1/graph.proto`
- `hms/mcp/v1/context.proto`

### 3.2 Proto File Template

Each proto file should include:

1. Appropriate package name (`hms.[component-code].v1`)
2. Import statements for dependencies
3. Language-specific options
4. Service definitions (if applicable)
5. Message definitions
6. Enum definitions (if applicable)
7. Documentation comments

Example template:

```protobuf
syntax = "proto3";

package hms.[component-code].v1;

import "google/protobuf/timestamp.proto";
import "hms/core/v1/common.proto";

option go_package = "github.com/hardisonco/hms-ffi-protos/hms/[component-code]/v1;[component-code]pb";
option java_package = "com.hardisonco.hms.ffi.protos.[component-code].v1";
option java_multiple_files = true;
option php_namespace = "HMS\\FFI\\Protos\\[Component-Code]\\V1";
option ruby_package = "HMS::FFI::Protos::[ComponentCode]::V1";

// [Service definition if applicable]
service [ServiceName] {
  // [Method definitions]
}

// [Message definitions]
message [MessageName] {
  // [Field definitions]
}

// [Enum definitions if applicable]
enum [EnumName] {
  // [Enum value definitions]
}
```

## 4. Implementation Phases

### 4.1 Phase 1: Critical Components (Month 1)

Focus on components essential for system operation:

1. HMS-A2A (Agent-to-agent communication)
2. HMS-AGT (Agent framework)
3. HMS-AGX (Agent execution)
4. HMS-LLM (Language model integration)
5. HMS-MCP (Model Context Protocol)

### 4.2 Phase 2: High-Priority Components (Month 2)

Focus on components with high business value:

1. HMS-ABC (Component management)
2. HMS-ACT (Workflow actions)
3. HMS-EHR (Electronic health records)
4. HMS-KNO (Knowledge system)
5. HMS-NFO (Knowledge framework)
6. HMS-OMS (Order management)
7. HMS-RED (Redaction/security)
8. HMS-SKL (Skills framework)
9. HMS-UHC (Universal health coverage)

### 4.3 Phase 3: Medium-Priority Components (Month 3)

Focus on secondary components:

1. HMS-CUR (Currency/financial)
2. HMS-EDU (Education)
3. HMS-ESQ (Data query system)
4. HMS-FLD (Field operations)
5. HMS-MFE (Micro frontend)
6. HMS-OPS (Operations)
7. HMS-SCM (Supply chain)
8. HMS-SME (Subject matter expertise)

### 4.4 Phase 4: Low-Priority Components (Month 4)

Complete remaining components:

1. HMS-DEV (Development tools)
2. HMS-DOC (Documentation)
3. HMS-MKT (Marketing)
4. HMS-UTL (Utilities)

## 5. Component-Specific Implementation Guidelines

### 5.1 HMS-A2A (Agent-to-agent communication)

**Key entities to model:**
- Agent definition
- Graph structure
- Message passing
- Task execution

**Proto files needed:**
- `hms/a2a/v1/agent.proto`
- `hms/a2a/v1/graph.proto`
- `hms/a2a/v1/message.proto`
- `hms/a2a/v1/task.proto`

### 5.2 HMS-AGT (Agent framework)

**Key entities to model:**
- Agent definition
- Capability registration
- Agent lifecycle
- Tool integration

**Proto files needed:**
- `hms/agt/v1/agent.proto`
- `hms/agt/v1/capability.proto`
- `hms/agt/v1/lifecycle.proto`
- `hms/agt/v1/tool.proto`

### 5.3 HMS-LLM (Language model integration)

**Key entities to model:**
- Model configuration
- Inference request/response
- Token counting
- Embedding generation

**Proto files needed:**
- `hms/llm/v1/model.proto`
- `hms/llm/v1/inference.proto`
- `hms/llm/v1/embedding.proto`
- `hms/llm/v1/tokenization.proto`

## 6. Language-Specific Binding Guidelines

### 6.1 Go Bindings

- Use standard protoc-gen-go plugin
- Follow Go style conventions
- Implement idiomatic Go interfaces

### 6.2 Rust Bindings

- Use prost or tonic for Rust bindings
- Implement Rust traits for services
- Use appropriate error handling

### 6.3 Python Bindings

- Use grpcio or grpc-tools
- Create Pythonic wrapper classes
- Implement async support

### 6.4 PHP Bindings

- Use protobuf-php
- Create composer package for each component
- Follow Laravel conventions for HMS-API integration

### 6.5 Ruby Bindings

- Use grpc-tools-ruby
- Follow Ruby idioms
- Integrate with Rails for web components

### 6.6 JavaScript/TypeScript Bindings

- Use protobuf.js or grpc-web
- Create TypeScript type definitions
- Support browser and Node.js environments

## 7. Testing Strategy

### 7.1 Unit Testing

Each proto implementation should include:
- Message serialization/deserialization tests
- Field validation tests
- Edge case handling

### 7.2 Integration Testing

For each language binding:
- Cross-language serialization compatibility tests
- Service invocation tests
- Error handling tests

### 7.3 Performance Testing

- Measure serialization/deserialization performance
- Benchmark cross-language call overhead
- Test with various payload sizes

## 8. Task Tracking

### 8.1 Component Implementation Tasks

Each component implementation will follow these tasks:

1. **Proto Definition**
   - Create message definitions
   - Define service interfaces
   - Add documentation

2. **Language Bindings**
   - Generate language-specific code
   - Create wrapper classes/modules
   - Add language-specific tests

3. **Integration**
   - Integrate with component code
   - Implement service handlers
   - Create client code

4. **Testing**
   - Unit tests
   - Integration tests
   - Performance tests

5. **Documentation**
   - Usage examples
   - API documentation
   - Integration guides

### 8.2 Task Tracking System

A tracking spreadsheet will be maintained with the following columns:
- Component ID
- Proto Status (Not Started, In Progress, Review, Complete)
- Go Binding Status
- Rust Binding Status
- Python Binding Status
- PHP Binding Status
- Ruby Binding Status
- JS/TS Binding Status
- Test Status
- Documentation Status
- Overall Status
- Notes

## 9. Resources and Timeline

### 9.1 Resource Requirements

- **Proto Definition**: 1 engineer per 2-3 components
- **Language Bindings**: 1 engineer per language
- **Integration**: Component owners
- **Testing**: 1-2 QA engineers
- **Documentation**: 1 technical writer

### 9.2 Timeline

- **Phase 1 (Critical)**: 4 weeks
- **Phase 2 (High)**: 4 weeks
- **Phase 3 (Medium)**: 4 weeks
- **Phase 4 (Low)**: 4 weeks
- **Final Testing and Integration**: 2 weeks

Total timeline: ~18 weeks (4.5 months)

## 10. Implementation Checklist

For each component, the following must be completed:

- [ ] Proto file(s) defined
- [ ] Generated language bindings
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance tests
- [ ] Documentation
- [ ] Component integration

## 11. Conclusion

This plan outlines the approach for implementing FFI across all HMS system components. By following this plan, we will create a standardized interface for cross-language communication that enables seamless integration between components.

The phased approach prioritizes critical components first, ensuring that the most important functionality is available early in the implementation process, while still providing a clear path to complete coverage of all system components.