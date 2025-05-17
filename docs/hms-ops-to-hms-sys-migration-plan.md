# HMS-OPS to HMS-SYS Migration Plan

## Executive Summary

This document outlines the plan to migrate functionality from HMS-OPS to HMS-SYS, with the goal of eventually removing HMS-OPS entirely. The migration will consolidate deployment, monitoring, and operations functionality into HMS-SYS, which is better equipped to handle these responsibilities as the system's core infrastructure component.

## Background Analysis

### HMS-OPS Current Functions

Based on our analysis, HMS-OPS currently provides the following key functions:

1. **Deployment Management**
   - Laravel Forge API deployments
   - AWS ECS deployments 
   - Kubernetes deployments (via integration with HMS-SYS)

2. **Monitoring & Error Aggregation**
   - Centralized logging for deployments, status checks, and errors
   - Background monitoring of deployment status
   - Notifications on failures

3. **Integration**
   - Integration with HMS-DEV for development workflow
   - Integration with HMS-SYS for Kubernetes operations
   
4. **Command-Line Interface**
   - HMS-OPS command for operations tasks

### HMS-SYS Capabilities

HMS-SYS is the system core component that already has:

1. **Container Orchestration**
   - Kubernetes/Cilium-based container orchestration
   - Deployment tooling through Makefile and CLI tools

2. **System Monitoring**
   - Health checking
   - Status reporting

3. **Infrastructure Management**
   - Multi-cloud support (AWS, Azure, AlibabaCloud)
   - Network management

## Migration Plan

### Phase 1: Enhance HMS-SYS for Deployment Operations

1. **Create Deployment Module in HMS-SYS**
   - Create `operations/deployment` directory in HMS-SYS
   - Implement the following files:
     - `deployment.go` - Core deployment logic
     - `forge.go` - Laravel Forge API client (migrated from HMS-OPS)
     - `aws.go` - AWS ECS deployment logic (migrated from HMS-OPS)
     - `kubernetes.go` - Enhanced Kubernetes deployment logic

2. **Implement HMS-SYS Deployment CLI**
   - Enhance `HMS-SYS` CLI to include deployment commands:
     ```
     HMS-SYS deploy [forge|aws|k8s] <project> <environment> [options]
     HMS-SYS status [forge|aws|k8s] <project> <environment>
     ```

3. **Migrate Configuration**
   - Create a unified configuration format in HMS-SYS
   - Implement configuration migration tool to convert from HMS-OPS format

### Phase 2: Enhance HMS-SYS for Monitoring

1. **Enhance Monitoring System**
   - Create `operations/monitoring` directory in HMS-SYS
   - Implement the following:
     - `logs.go` - Centralized logging
     - `alerting.go` - Notification system (Slack, email)
     - `status.go` - Status checking and reporting

2. **Implement HMS-SYS Monitoring CLI**
   - Add monitoring commands to HMS-SYS CLI:
     ```
     HMS-SYS monitor [start|stop]
     HMS-SYS errors [count]
     ```

3. **Migrate Monitoring Configuration**
   - Migrate monitoring settings from HMS-OPS to HMS-SYS

### Phase 3: Implement Integration Functionality

1. **Create Integration Module**
   - Create `operations/integration` directory in HMS-SYS
   - Implement integration logic for other HMS components

2. **Implement HMS-DEV Integration**
   - Create specific integration for HMS-DEV
   - Migrate existing integration logic from HMS-OPS

### Phase 4: Testing and Validation

1. **Develop Test Suite**
   - Create comprehensive tests for all migrated functionality
   - Include integration tests with actual services (Forge, AWS, Kubernetes)

2. **Validate All Deployment Paths**
   - Test each deployment method (Forge, AWS, Kubernetes)
   - Verify monitoring and alerting
   - Test integration with other HMS components

### Phase 5: Switchover and Cleanup

1. **Create HMS-OPS Command Wrapper**
   - Implement a wrapper script that redirects HMS-OPS commands to HMS-SYS
   - Example:
     ```bash
     #!/bin/bash
     # HMS-OPS compatibility wrapper
     echo "Warning: HMS-OPS is deprecated. Please use HMS-SYS instead."
     
     # Map HMS-OPS command to HMS-SYS equivalent
     case "$1" in
       "deploy")
         HMS-SYS deploy "$@"
         ;;
       "status")
         HMS-SYS status "$@"
         ;;
       # Add other commands as needed
       *)
         echo "Command not supported. Please use HMS-SYS."
         exit 1
         ;;
     esac
     ```

2. **Update Documentation**
   - Update all documentation to reference HMS-SYS instead of HMS-OPS
   - Create migration guide for users

3. **Remove HMS-OPS**
   - After successful switchover, mark HMS-OPS as deprecated
   - Eventually remove HMS-OPS from the system

## Migration Implementation Details

### Directory Structure Changes

New directories to be created in HMS-SYS:

```
HMS-SYS/
  ├── operations/
  │   ├── deployment/
  │   │   ├── deployment.go
  │   │   ├── forge.go
  │   │   ├── aws.go
  │   │   └── kubernetes.go
  │   ├── monitoring/
  │   │   ├── logs.go
  │   │   ├── alerting.go
  │   │   └── status.go
  │   └── integration/
  │       ├── integration.go
  │       └── hms_dev.go
  └── cmd/
      └── hms-sys-cli/
          ├── cmd_deploy.go
          ├── cmd_status.go
          └── cmd_monitor.go
```

### Configuration Migration

HMS-OPS configuration from `.hms-ops-config.json` will be migrated to HMS-SYS in a structured format that aligns with existing HMS-SYS configuration patterns.

### Code Migration Approach

1. **Extract and Refactor**
   - Extract core functionality from HMS-OPS
   - Refactor to match HMS-SYS coding standards and patterns

2. **Enhance and Extend**
   - Enhance functionality where appropriate
   - Extend to integrate better with HMS-SYS architecture

3. **Test and Validate**
   - Ensure all migrated code works as expected
   - Validate with real-world deployment scenarios

## Timeline and Milestones

1. **Phase 1: Enhance HMS-SYS for Deployment Operations**
   - Estimated time: 2 weeks
   - Key milestone: First successful deployment through HMS-SYS

2. **Phase 2: Enhance HMS-SYS for Monitoring**
   - Estimated time: 1 week
   - Key milestone: Monitoring system operational in HMS-SYS

3. **Phase 3: Implement Integration Functionality**
   - Estimated time: 1 week
   - Key milestone: HMS-DEV integration working through HMS-SYS

4. **Phase 4: Testing and Validation**
   - Estimated time: 1 week
   - Key milestone: All functionality validated with tests

5. **Phase 5: Switchover and Cleanup**
   - Estimated time: 1 week
   - Key milestone: HMS-OPS marked as deprecated

Total estimated time: 6 weeks

## Risks and Mitigation

1. **Risk**: Deployment failures during migration
   **Mitigation**: Implement dual-deployment mode during testing phase

2. **Risk**: Missing HMS-OPS functionality
   **Mitigation**: Comprehensive audit of HMS-OPS before migration

3. **Risk**: Integration issues with other HMS components
   **Mitigation**: Thorough testing with all components, maintain compatibility layer

## Conclusion

This migration plan provides a structured approach to moving functionality from HMS-OPS to HMS-SYS. By following the phased approach, we can ensure a smooth transition while minimizing disruption to existing systems and workflows. Upon completion, HMS-SYS will provide a more integrated and cohesive operations platform for the entire HMS ecosystem.