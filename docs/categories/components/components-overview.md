# HMS Components Overview

This document provides a comprehensive overview of the core components that make up the HMS platform, explaining their purpose, functionality, and relationships.

## Component Ecosystem

```mermaid
graph TD
    subgraph Interface_Layer[Interface Layer]
        MFE[HMS-MFE: Micro Frontend]
        GOV[HMS-GOV: Admin Portal]
    end
    
    subgraph Management_Layer[Management Layer]
        API[HMS-API: API Gateway]
        SVC[HMS-SVC: Backend Services]
        ACT[HMS-ACT: Action Orchestrator]
        ACH[HMS-ACH: Financial Engine]
    end
    
    subgraph Governance_Layer[Governance Layer]
        AGT[HMS-AGT: AI Representative]
        CDF[HMS-CDF: Policy Engine]
        ESQ[HMS-ESQ: Legal Reasoner]
        A2A[HMS-A2A: Inter-Agency Exchange]
    end
    
    subgraph Cross_Cutting[Cross-Cutting Components]
        SYS[HMS-SYS: Core Infrastructure]
        DTA[HMS-DTA: Data Repository]
        MCP[HMS-MCP: Model Context Protocol]
        OPS[HMS-OPS: Operations Monitoring]
        MKT[HMS-MKT: Marketplace]
        NFO[HMS-NFO: Knowledge Framework]
        UTL[HMS-UTL: Utilities]
    end
    
    subgraph Healthcare_Components[Healthcare Components]
        UHC[HMS-UHC: Universal Health Connector]
        EHR[HMS-EHR: Electronic Health Records]
        EMR[HMS-EMR: Electronic Medical Records]
    end
    
    MFE --> API
    GOV --> API
    GOV --> CDF
    
    API --> SVC
    API --> ACT
    
    ACT --> SVC
    ACT --> AGT
    ACT --> A2A
    
    AGT --> CDF
    AGT --> ESQ
    
    SVC --> ACH
    SVC --> DTA
    SVC --> UHC
    
    UHC --> EHR
    UHC --> EMR
    
    A2A --> AGT

    classDef interface fill:#e6f7ff,stroke:#0088ff
    classDef management fill:#e6ffe6,stroke:#00cc00
    classDef governance fill:#ffe6e6,stroke:#ff0000
    classDef crosscutting fill:#f2e6ff,stroke:#8800ff
    classDef healthcare fill:#fff2e6,stroke:#ff8800
    
    class MFE,GOV interface
    class API,SVC,ACT,ACH management
    class AGT,CDF,ESQ,A2A governance
    class SYS,DTA,MCP,OPS,MKT,NFO,UTL crosscutting
    class UHC,EHR,EMR healthcare
```

## Core Component Descriptions

### Interface Layer

| Component | Description | Primary Functionality |
|-----------|-------------|----------------------|
| **HMS-MFE** | Micro Frontend Experience | Provides modular UI components, enables consistent user experiences across agencies, and supports intent-driven navigation |
| **HMS-GOV** | Administrative Portal | Offers governance tools, admin interfaces, configuration controls, and policy management interfaces |

### Management Layer

| Component | Description | Primary Functionality |
|-----------|-------------|----------------------|
| **HMS-API** | API Gateway | Manages API routing, authentication, rate limiting, and serves as the entry point for all service requests |
| **HMS-SVC** | Backend Services | Provides core business logic, implements domain-specific functionality, and orchestrates workflows |
| **HMS-ACT** | Action Orchestrator | Coordinates agent activities, manages workflow execution, and handles complex process flows |
| **HMS-ACH** | Financial Engine | Processes financial transactions, handles payment clearance, and manages fiscal operations |

### Governance Layer

| Component | Description | Primary Functionality |
|-----------|-------------|----------------------|
| **HMS-AGT** | AI Representative Agent | Provides AI assistant capabilities, expert guidance, and intelligent interfaces for users |
| **HMS-AGX** | Agent Extensions | Extends agent capabilities with specialized skills, domain knowledge, and additional tools |
| **HMS-CDF** | Codified Democracy Foundation | Implements legislative engines, policy workflows, and democratic process modeling |
| **HMS-ESQ** | Legal Reasoning | Provides compliance checks, legal analysis, regulatory assessment, and risk evaluation |
| **HMS-A2A** | Inter-Agency Exchange | Facilitates secure agency communication, cross-agency workflows, and data sharing |

### Cross-Cutting Components

| Component | Description | Primary Functionality |
|-----------|-------------|----------------------|
| **HMS-SYS** | Core Infrastructure | Manages system infrastructure, deployment, scaling, and foundational services |
| **HMS-DTA** | Data Repository | Provides centralized data storage, knowledge management, and data governance |
| **HMS-MCP** | Model Context Protocol | Standardizes AI model interactions, provides context management, and ensures consistent model behavior |
| **HMS-OPS** | Operations Monitoring | Handles system monitoring, alerting, logging, and operational metrics |
| **HMS-MKT** | Marketplace | Provides capability discovery, component sharing, and extension distribution |
| **HMS-NFO** | Knowledge Framework | Manages domain knowledge, training data, and information retrieval services |
| **HMS-UTL** | Utilities | Provides shared utilities, common code libraries, and reusable functions |

### Healthcare Components

| Component | Description | Primary Functionality |
|-----------|-------------|----------------------|
| **HMS-UHC** | Universal Health Connector | Connects to health systems, standardizes health data, and integrates with care providers |
| **HMS-EHR** | Electronic Health Records | Manages longitudinal patient records, health history, and cross-provider information |
| **HMS-EMR** | Electronic Medical Records | Handles provider-specific medical records, clinical documentation, and treatment data |

## Component Interactions and Workflows

HMS components interact through well-defined interfaces to provide comprehensive workflows. Below are key interaction patterns:

### User Request Flow

```mermaid
sequenceDiagram
    actor User
    participant MFE as HMS-MFE
    participant API as HMS-API
    participant SVC as HMS-SVC
    participant AGT as HMS-AGT
    participant CDF as HMS-CDF
    participant DTA as HMS-DTA
    
    User->>MFE: Submit request
    MFE->>API: Forward request
    API->>AGT: Request assistance
    
    par Process in parallel
        AGT->>CDF: Policy check
        AGT->>DTA: Retrieve data
    end
    
    CDF-->>AGT: Policy response
    DTA-->>AGT: Data response
    
    AGT->>SVC: Process request
    SVC-->>API: Response
    API-->>MFE: Format response
    MFE-->>User: Display result
```

### Agency Integration Flow

```mermaid
sequenceDiagram
    participant ExtAgency as External Agency
    participant A2A as HMS-A2A
    participant ACT as HMS-ACT
    participant SVC as HMS-SVC
    participant ESQ as HMS-ESQ
    participant DTA as HMS-DTA
    
    ExtAgency->>A2A: Integration request
    A2A->>ESQ: Compliance check
    ESQ-->>A2A: Approval
    
    A2A->>ACT: Workflow creation
    ACT->>SVC: Service orchestration
    SVC->>DTA: Data exchange
    
    DTA-->>SVC: Processed data
    SVC-->>ACT: Completed workflow
    ACT-->>A2A: Integration response
    A2A-->>ExtAgency: Confirmation
```

## Component Versioning

HMS components follow semantic versioning (MAJOR.MINOR.PATCH) with consistent upgrade paths and backward compatibility guarantees. Version alignment ensures compatibility across the ecosystem.

## Extension Points

Each HMS component provides extension points to customize functionality:

- **HMS-MFE**: Custom UI components, themes, and navigation flows
- **HMS-SVC**: Service plugins, custom endpoints, and business logic extensions
- **HMS-AGT**: Agent skills, specialized knowledge bases, and interaction patterns
- **HMS-CDF**: Policy templates, workflow definitions, and process models
- **HMS-A2A**: Agency connection adapters, protocol extensions, and data mappings

## Cross-Component Services

Several services span multiple components:

1. **Authentication & Authorization**: Identity management, roles, and permissions
2. **Logging & Monitoring**: Centralized logging, metrics collection, and alerting
3. **Configuration Management**: Dynamic configuration, feature flags, and settings
4. **Error Handling**: Standardized error responses, retry mechanisms, and fallbacks
5. **Data Validation**: Schema validation, data quality checks, and normalization

## Component Discovery

The HMS-MKT component provides dynamic discovery of available components and their capabilities. This enables agencies to find, evaluate, and integrate components based on their specific needs.

## Component Dependencies

```mermaid
graph TD
    MFE[HMS-MFE] --> SYS
    MFE --> UTL
    
    GOV[HMS-GOV] --> MFE
    GOV --> SYS
    
    API[HMS-API] --> SYS
    API --> UTL
    
    SVC[HMS-SVC] --> API
    SVC --> DTA
    SVC --> UTL
    
    AGT[HMS-AGT] --> MCP
    AGT --> NFO
    AGT --> UTL
    
    CDF[HMS-CDF] --> DTA
    CDF --> NFO
    CDF --> ESQ
    
    A2A[HMS-A2A] --> MCP
    A2A --> SYS
    A2A --> UTL
    
    ACT[HMS-ACT] --> SVC
    ACT --> MCP
    ACT --> UTL
    
    UHC[HMS-UHC] --> SVC
    UHC --> DTA
    UHC --> UTL
    
    SYS[HMS-SYS]
    DTA[HMS-DTA]
    MCP[HMS-MCP]
    OPS[HMS-OPS]
    MKT[HMS-MKT]
    NFO[HMS-NFO]
    UTL[HMS-UTL]
```

This diagram illustrates the dependency relationships between components, helping with deployment planning and understanding component coupling.

## Agency-Specific Component Customizations

Different agency types may require specialized component configurations:

### Federal Agencies

Federal agencies typically use the full HMS component stack with additional security and compliance extensions for HMS-ESQ and HMS-CDF components.

### State Agencies

State agencies often focus on HMS-MFE, HMS-SVC, HMS-AGT, and HMS-UHC components with state-specific policy extensions and local integrations.

### International Health Systems

International health systems typically emphasize HMS-UHC, HMS-EHR, HMS-EMR with region-specific adaptations for language, regulatory requirements, and healthcare standards.