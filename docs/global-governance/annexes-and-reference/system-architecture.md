# HMS System Architecture

This document provides an overview of the HMS system architecture, showing how all components work together to support government agencies at federal, state, and international levels.

## Three-Layer Architecture

The HMS system follows a three-layer architecture:

```mermaid
flowchart TD
    subgraph "Interface Layer"
        MFE["HMS-MFE<br>(Micro-frontend)"]
        GOV["HMS-GOV<br>(Admin Portal)"]
        MKT["HMS-MKT<br>(Main Frontend)"]
    end
    
    subgraph "Management Layer"
        API["HMS-API<br>(Core Backend)"]
        ACT["HMS-ACT<br>(Workflow Engine)"]
        AGX["HMS-AGX<br>(Agent Extensions)"]
        A2A["HMS-A2A<br>(Inter-Agency Exchange)"]
    end
    
    subgraph "Governance Layer"
        CDF["HMS-CDF<br>(Codified Democracy)"]
        NFO["HMS-NFO<br>(Information Repository)"]
        MBL["HMS-MBL<br>(Moneyball Analytics)"]
    end

    MFE --> API
    GOV --> API
    MKT --> API
    
    API --> ACT
    API --> A2A
    API --> AGX
    
    ACT --> CDF
    AGX --> NFO
    A2A --> NFO
    A2A --> MBL
    
    NFO <--> MBL
    CDF --> NFO
    
    classDef interface fill:#e6f7ff,stroke:#0088ff
    classDef management fill:#e6ffe6,stroke:#00cc00
    classDef governance fill:#ffe6e6,stroke:#ff0000
    
    class MFE,GOV,MKT interface
    class API,ACT,AGX,A2A management
    class CDF,NFO,MBL governance
```

### 1. Interface Layer
The Interface Layer provides user interfaces for different stakeholders:

- **HMS-MFE**: Micro-frontend components that can be embedded in various applications
- **HMS-GOV**: Administrative portal for government officials to manage policies
- **HMS-MKT**: Main frontend application for public users and service marketplace

### 2. Management Layer
The Management Layer handles business logic, workflow orchestration, and integration:

- **HMS-API**: Core backend API services that process business logic
- **HMS-ACT**: Workflow orchestration engine that manages process flows
- **HMS-AGX**: Agent extension system that provides AI capabilities
- **HMS-A2A**: Inter-agency exchange system for secure communication

### 3. Governance Layer
The Governance Layer provides policy management, data intelligence, and regulatory compliance:

- **HMS-CDF**: Codified Democracy Foundation engine for legislative processes
- **HMS-NFO**: Information repository for data intelligence
- **HMS-MBL**: Moneyball analytics for optimizing resource allocation

## Domain-Specific Components

In addition to the core architecture, HMS provides specialized components for different domains:

### Healthcare Components

```mermaid
flowchart LR
    API["HMS-API<br>(Core Backend)"] --> UHC["HMS-UHC<br>(Universal Health<br>Connector)"]
    API --> EHR["HMS-EHR<br>(Electronic Health<br>Records)"]
    API --> EMR["HMS-EMR<br>(Electronic Medical<br>Records)"]
    
    UHC --> IntlHealth["International<br>Health Systems"]
    UHC --> StateHealth["State Health<br>Departments"]
    UHC --> FedHealth["Federal Health<br>Agencies"]
    
    EHR --> PatientData["Patient Data<br>Repository"]
    EMR --> ProviderSystems["Provider<br>Systems"]
    
    classDef core fill:#e6f7ff,stroke:#0088ff
    classDef health fill:#ffe6f7,stroke:#ff00aa
    classDef external fill:#f9f9f9,stroke:#999
    
    class API core
    class UHC,EHR,EMR health
    class IntlHealth,StateHealth,FedHealth,PatientData,ProviderSystems external
```

### Financial Components

```mermaid
flowchart LR
    API["HMS-API<br>(Core Backend)"] --> ACH["HMS-ACH<br>(Payment System)"]
    API --> CUR["HMS-CUR<br>(Currency Services)"]
    
    ACH --> IntlPayments["International<br>Payment Systems"]
    ACH --> StateFinSys["State Financial<br>Systems"]
    ACH --> FedTreasury["Federal Treasury<br>Systems"]
    
    CUR --> DigitalCurrency["Digital Currency<br>Infrastructure"]
    
    classDef core fill:#e6f7ff,stroke:#0088ff
    classDef finance fill:#e6ffe6,stroke:#00cc00
    classDef external fill:#f9f9f9,stroke:#999
    
    class API core
    class ACH,CUR finance
    class IntlPayments,StateFinSys,FedTreasury,DigitalCurrency external
```

## Cross-Cutting Components

Several components provide cross-cutting functionality across the system:

- **HMS-OPS**: Operations and monitoring
- **HMS-MCP**: Model context protocol for AI interactions
- **HMS-UTL**: Utility services and shared libraries
- **HMS-SCM**: Supply chain management
- **HMS-ETL**: Extract, transform, load data pipeline

## Agency Integration

The architecture is designed to support multiple agency types:

```mermaid
flowchart TD
    HMS["HMS Platform"] --> Federal["Federal<br>Agencies"]
    HMS --> State["State<br>Agencies"]
    HMS --> International["International<br>Agencies"]
    
    Federal --> CabinetLevel["Cabinet-Level<br>Departments"]
    Federal --> Independent["Independent<br>Agencies"]
    Federal --> Commissions["Federal<br>Commissions"]
    
    State --> StateHealth["State Health<br>Departments"]
    State --> StateFinance["State Finance<br>Agencies"]
    State --> StateOther["Other State<br>Agencies"]
    
    International --> HealthSystems["National Health<br>Systems"]
    International --> IntlFinance["Financial<br>Authorities"]
    International --> IntlOther["Other International<br>Organizations"]
    
    classDef platform fill:#e6f7ff,stroke:#0088ff
    classDef agency fill:#ffe6e6,stroke:#ff0000
    classDef subagency fill:#f5f5ff,stroke:#8888ff
    
    class HMS platform
    class Federal,State,International agency
    class CabinetLevel,Independent,Commissions,StateHealth,StateFinance,StateOther,HealthSystems,IntlFinance,IntlOther subagency
```

## Data Flow

The data flow through the HMS system follows a consistent pattern:

1. User interfaces (HMS-MFE, HMS-GOV, HMS-MKT) collect and display information
2. Core backend (HMS-API) processes business logic and transactions
3. Specialized components handle domain-specific operations
4. Data is stored and managed in the central data repository
5. AI-powered analytics (HMS-NFO, HMS-MBL) provide insights and recommendations
6. Policy engines (HMS-CDF) ensure compliance with regulations

This architecture ensures that agencies of all types can leverage the HMS platform while maintaining their unique requirements and workflows.