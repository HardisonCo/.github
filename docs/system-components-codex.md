# HMS System Components - Detailed Reference

## System Architecture
The HMS (Health Management System) ecosystem consists of 33 specialized components that work together to provide a comprehensive healthcare platform. Each component has specific responsibilities, integration points, and technical specifications.

## Component Details

### HMS-A2A (Agent-to-Agent)
- **Primary Purpose**: Chain of Recursive Thought (CoRT) AI agent system
- **Key Technologies**: LangGraph, MCP, Chain-of-Recursive-Thought
- **Integration Points**: HMS-SVC, HMS-DTA, HMS-NFO
- **Authentication**: OAuth 2.0 Client Credentials
- **API Base URL**: `/v1/a2a`
- **Dependencies**: HMS-MCP, HMS-LLM

### HMS-ABC (Accountability-Based Coverage)
- **Primary Purpose**: Client/clinic web access for accountability-focused coverage
- **Key Technologies**: Next.js, TypeScript, TailwindCSS
- **Integration Points**: HMS-UHC, HMS-ACH
- **Authentication**: OAuth 2.0 Authorization Code
- **API Base URL**: `/v1/abc`
- **Dependencies**: HMS-API

### HMS-ACH (Automated Clearing House)
- **Primary Purpose**: Financial services and payment processing
- **Key Technologies**: Ruby, Rails, PostgreSQL
- **Integration Points**: HMS-CUR, External Financial Services
- **Authentication**: OAuth 2.0 + IP Whitelisting
- **API Base URL**: `/v1/ach`
- **Dependencies**: HMS-API

### HMS-ACT (Agent Collaboration Toolkit)
- **Primary Purpose**: Lightweight agent framework
- **Key Technologies**: Python, OpenAI, Anthropic, Azure
- **Integration Points**: LLM Providers, HMS-MCP
- **Authentication**: API Keys + OAuth 2.0
- **API Base URL**: `/v1/act`
- **Dependencies**: HMS-MCP

### HMS-AGT (Agent Technology)
- **Primary Purpose**: LangChain question-answering over documentation
- **Key Technologies**: LangChain, Vector Stores, LangGraph
- **Integration Points**: HMS-DOC, HMS-MCP
- **Authentication**: API Keys
- **API Base URL**: `/v1/agt`
- **Dependencies**: HMS-LLM, HMS-DOC

### HMS-AGX (Agent Extended)
- **Primary Purpose**: Deep research assistant with knowledge graph generation
- **Key Technologies**: CoRT, Knowledge Graphs, Research Tools
- **Integration Points**: Search Engines, Knowledge Bases
- **Authentication**: API Keys + JWT
- **API Base URL**: `/v1/agx`
- **Dependencies**: HMS-A2A, HMS-MCP

### HMS-API (Application Programming Interface)
- **Primary Purpose**: Core PHP backend API system
- **Key Technologies**: Laravel, MySQL, Redis
- **Integration Points**: All HMS Frontend Components
- **Authentication**: OAuth 2.0 (all flows)
- **API Base URL**: `/v1`
- **Dependencies**: Database Systems

### HMS-CDF (Codified Democracy Foundation)
- **Primary Purpose**: Policy verification and legislative analysis
- **Key Technologies**: Rust, Debate Frameworks, Economic Models
- **Integration Points**: Professional Standards, Legislative Systems
- **Authentication**: OAuth 2.0
- **API Base URL**: `/v1/cdf`
- **Dependencies**: HMS-A2A, HMS-SME

### HMS-CUR (Currency)
- **Primary Purpose**: Banking/Financial Mobile App
- **Key Technologies**: React Native, MobX-State-Tree
- **Integration Points**: HMS-ACH, Financial Institutions
- **Authentication**: OAuth 2.0 + Biometrics
- **API Base URL**: Mobile SDK
- **Dependencies**: HMS-ACH

### HMS-DEV (Development)
- **Primary Purpose**: Development framework for agent tools
- **Key Technologies**: TypeScript/Node.js, pnpm Workspaces
- **Integration Points**: HMS-A2A, MCP, OSS Marketplace
- **Authentication**: API Keys
- **API Base URL**: Dev Tools
- **Dependencies**: HMS-MCP

### HMS-DOC (Documentation)
- **Primary Purpose**: Documentation generation system
- **Key Technologies**: Python, Markdown, A2A Agents
- **Integration Points**: All HMS Components, Agency Data
- **Authentication**: OAuth 2.0
- **API Base URL**: `/v1/doc`
- **Dependencies**: HMS-A2A

### HMS-EDU (Education)
- **Primary Purpose**: Learning Management System with LTI integration
- **Key Technologies**: Ruby, Sinatra
- **Integration Points**: HMS-SKL, HMS-UHC
- **Authentication**: OAuth 2.0 + LTI
- **API Base URL**: `/v1/edu`
- **Dependencies**: HMS-API

### HMS-EHR (Electronic Health Records)
- **Primary Purpose**: Healthcare documentation chatbots
- **Key Technologies**: LangChain, LangGraph, FHIR
- **Integration Points**: HMS-API, Healthcare Systems
- **Authentication**: OAuth 2.0 + SMART on FHIR
- **API Base URL**: `/v1/ehr`
- **Dependencies**: HMS-API, HMS-MCP

### HMS-EMR (Electronic Medical Records)
- **Primary Purpose**: FHIR-compliant personal health record aggregator
- **Key Technologies**: Go, FHIR, Kubernetes
- **Integration Points**: Healthcare Providers, HMS-EHR
- **Authentication**: OAuth 2.0 + SMART on FHIR
- **API Base URL**: `/v1/emr`
- **Dependencies**: HMS-API

### HMS-ESQ (eSquire)
- **Primary Purpose**: Legal kiosk system for IoT
- **Key Technologies**: JavaScript, IoT Frameworks
- **Integration Points**: HMS-API, Legal Services
- **Authentication**: OAuth 2.0 + Device Flow
- **API Base URL**: `/v1/esq`
- **Dependencies**: HMS-API

### HMS-ESR (Engineering Support Request)
- **Primary Purpose**: Developer support and bug tracking
- **Key Technologies**: Ruby, Tmux, Ghost Mode
- **Integration Points**: Bugsnag, Kibana/Elasticsearch
- **Authentication**: OAuth 2.0
- **API Base URL**: `/v1/esr`
- **Dependencies**: HMS-API

### HMS-ETL (Extract, Transform, Load)
- **Primary Purpose**: Data pipeline orchestration with Dagster
- **Key Technologies**: Python, Dagster, Pandas
- **Integration Points**: Databases, Event Systems
- **Authentication**: API Keys + Service Accounts
- **API Base URL**: `/v1/etl`
- **Dependencies**: HMS-API

### HMS-FLD (Field)
- **Primary Purpose**: Mobile navigation and field operations
- **Key Technologies**: React Native, Mapbox, GPS
- **Integration Points**: HMS-SCM, HMS-OMS
- **Authentication**: OAuth 2.0 + Location Services
- **API Base URL**: Mobile SDK
- **Dependencies**: HMS-API

### HMS-GOV (Government)
- **Primary Purpose**: Government interface admin portal
- **Key Technologies**: Vue.js, Nuxt.js
- **Integration Points**: HMS-API, Government Systems
- **Authentication**: OAuth 2.0 + MFA
- **API Base URL**: `/v1/gov`
- **Dependencies**: HMS-API

### HMS-KNO (Knowledge)
- **Primary Purpose**: Recursive thinking AI implementation
- **Key Technologies**: Python, OpenRouter, LLMs
- **Integration Points**: HMS-A2A, HMS-MCP
- **Authentication**: API Keys
- **API Base URL**: `/v1/kno`
- **Dependencies**: HMS-MCP

### HMS-LLM (Large Language Models)
- **Primary Purpose**: LLMOps platform for prompt management
- **Key Technologies**: Python, 50+ LLM models
- **Integration Points**: LLM Providers, Evaluation Tools
- **Authentication**: API Keys + OAuth 2.0
- **API Base URL**: `/v1/llm`
- **Dependencies**: HMS-MCP

### HMS-MCP (Model Context Protocol)
- **Primary Purpose**: Standardized LLM interactions
- **Key Technologies**: TypeScript, A2A Protocol
- **Integration Points**: OpenAI, Anthropic, Local LLMs
- **Authentication**: API Keys
- **API Base URL**: `/v1/mcp`
- **Dependencies**: LLM Providers

### HMS-MKT (Market)
- **Primary Purpose**: Vue.js/Nuxt frontend application
- **Key Technologies**: Vue.js, Nuxt.js, Vitest
- **Integration Points**: HMS-API, HMS-FLD
- **Authentication**: OAuth 2.0
- **API Base URL**: Frontend
- **Dependencies**: HMS-API

### HMS-NFO (National Foundation Office)
- **Primary Purpose**: Specialized knowledge processing
- **Key Technologies**: Python, Economic Models
- **Integration Points**: HMS-A2A, HMS-DOC
- **Authentication**: OAuth 2.0
- **API Base URL**: `/v1/nfo`
- **Dependencies**: HMS-A2A

### HMS-OMS (Order Management System)
- **Primary Purpose**: Order processing with workflow
- **Key Technologies**: Ruby, Rails, Camunda
- **Integration Points**: HMS-SCM, HMS-ACH
- **Authentication**: OAuth 2.0
- **API Base URL**: `/v1/oms`
- **Dependencies**: HMS-API

### HMS-OPS (Operations)
- **Primary Purpose**: Unified deployment operations
- **Key Technologies**: Shell, PHP, AWS
- **Integration Points**: Forge, AWS, Error Logging
- **Authentication**: API Keys + Service Accounts
- **API Base URL**: `/v1/ops`
- **Dependencies**: HMS-SYS

### HMS-RED (Red Team)
- **Primary Purpose**: LLM testing and evaluation
- **Key Technologies**: TypeScript, Jest, LLM Test Frameworks
- **Integration Points**: OpenAI, Anthropic, Others
- **Authentication**: API Keys
- **API Base URL**: `/v1/red`
- **Dependencies**: HMS-MCP

### HMS-SCM (Supply Chain Management)
- **Primary Purpose**: Routing and logistics
- **Key Technologies**: PHP, Postgres, Caddy
- **Integration Points**: HMS-OMS, HMS-FLD
- **Authentication**: OAuth 2.0
- **API Base URL**: `/v1/scm`
- **Dependencies**: HMS-API

### HMS-SKL (Skills)
- **Primary Purpose**: Mobile education application
- **Key Technologies**: React Native, OCR, PDF
- **Integration Points**: HMS-EDU, HMS-API
- **Authentication**: OAuth 2.0
- **API Base URL**: Mobile SDK
- **Dependencies**: HMS-EDU

### HMS-SME (Subject Matter Expert)
- **Primary Purpose**: Professional standards platform
- **Key Technologies**: Ruby, Tmux, A2A Integration
- **Integration Points**: HMS-A2A, HMS-MCP
- **Authentication**: OAuth 2.0
- **API Base URL**: `/v1/sme`
- **Dependencies**: HMS-A2A

### HMS-SYS (System)
- **Primary Purpose**: Networking and security platform
- **Key Technologies**: Go, Kubernetes, Observability
- **Integration Points**: Infrastructure, Monitoring
- **Authentication**: Service Accounts
- **API Base URL**: `/v1/sys`
- **Dependencies**: Infrastructure

### HMS-UHC (Universal Health Coverage)
- **Primary Purpose**: Healthcare enrollment and eligibility
- **Key Technologies**: Ruby, Health Benefit Exchange
- **Integration Points**: Government Systems, HMS-API
- **Authentication**: OAuth 2.0
- **API Base URL**: `/v1/uhc`
- **Dependencies**: HMS-API

### HMS-UTL (Utilities)
- **Primary Purpose**: Shared services and cross-component functionality
- **Key Technologies**: Multiple, Shared Libraries
- **Integration Points**: All HMS Components
- **Authentication**: Internal
- **API Base URL**: `/v1/utl`
- **Dependencies**: None

## Integration Diagrams
Refer to `/SYSTEM-COMPONENTS/HMS-DOC/HMS_COMPONENT_INTEGRATION_DIAGRAM.md` for detailed visual representation of component interactions.

## Technical Specifications
Refer to `/SYSTEM-COMPONENTS/HMS-DOC/HMS_TECHNICAL_INTEGRATION_GUIDE.md` for detailed API specifications and integration requirements.

## Integration Process
Refer to `/SYSTEM-COMPONENTS/HMS-DOC/HMS_INTEGRATION_PROCESS.md` for the step-by-step integration process.

## Quick Start
Refer to `/SYSTEM-COMPONENTS/HMS-DOC/HMS_INTEGRATION_QUICKSTART.md` for rapid development guidance and code samples.