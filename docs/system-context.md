# HMS System Components Context

This document provides a brief overview of each HMS system component, explaining its purpose, key functionality, and when to use it.

## HMS-A2A (Agent-to-Agent)
**Purpose:** Enables collaborative communication between intelligent agents.  
**Key Functionality:** Agent collaboration patterns, communication protocols, recursive thought chains.  
**When to Use:** When you need agents to work together, share knowledge, and collectively solve problems.

## HMS-ABC (Adaptive Business Capabilities)
**Purpose:** Provides flexible business capability modeling and implementation.  
**Key Functionality:** Business process automation, capability mapping, adaptive workflows.  
**When to Use:** When defining organizational capabilities or implementing flexible business processes.

## HMS-ACH (Automated Clearing House)
**Purpose:** Handles financial transaction processing and clearing.  
**Key Functionality:** Payment processing, transaction clearing, financial settlement.  
**When to Use:** When implementing payment systems or financial transaction processing.

## HMS-ACT (Agent Collaboration Tools)
**Purpose:** Toolkit for building agent collaboration systems.  
**Key Functionality:** Agent workflow design, team formation, collaboration metrics.  
**When to Use:** When building systems where multiple agents need to collaborate on tasks.

## HMS-AGT (Agent Tooling)
**Purpose:** Provides tools and utilities for agent functionality.  
**Key Functionality:** Tool registration, tool discovery, tool execution framework.  
**When to Use:** When developing or extending agent capabilities through specialized tools.

## HMS-AGX (Advanced Graph Experience)
**Purpose:** Graph-based reasoning and visualization for complex systems.  
**Key Functionality:** Graph generation, relationship mapping, visual analytics.  
**When to Use:** When mapping complex relationships or visualizing interconnected systems.

## HMS-API (API Services)
**Purpose:** API management and integration layer.  
**Key Functionality:** API definition, request handling, service integration.  
**When to Use:** When building or consuming APIs across the HMS ecosystem.

## HMS-CDF (Collaborative Decision Framework)
**Purpose:** Framework for policy formalization, debate, and implementation.  
**Key Functionality:** Policy modeling, legislative process management, stakeholder debate.  
**When to Use:** When changing how politicians implement policy or formalizing decision processes.

## HMS-CUR (Currency Management)
**Purpose:** Financial and currency management system.  
**Key Functionality:** Currency operations, exchange rates, financial tracking.  
**When to Use:** When implementing financial systems or currency-related functionality.

## HMS-DEV (Development Framework)
**Purpose:** Development tools and OSS marketplace.  
**Key Functionality:** Tool monetization, development workflows, verification mechanisms.  
**When to Use:** When developing new components or monetizing tools for agent consumption.

## HMS-DOC (Documentation System)
**Purpose:** Documentation generation and management.  
**Key Functionality:** Auto-documentation, standards validation, documentation integration.  
**When to Use:** When creating or managing documentation across the HMS ecosystem.

## HMS-EDU (Education System)
**Purpose:** Educational content and learning management.  
**Key Functionality:** Learning paths, educational content, knowledge assessment.  
**When to Use:** When implementing learning systems or educational content.

## HMS-EHR (Electronic Health Records)
**Purpose:** Health record management and processing.  
**Key Functionality:** Patient data handling, medical record integration, health analytics.  
**When to Use:** When working with healthcare data or medical record systems.

## HMS-EMR (Electronic Medical Records)
**Purpose:** Detailed medical record system with clinical focus.  
**Key Functionality:** Clinical data management, medical workflows, provider interfaces.  
**When to Use:** When implementing systems for clinical settings or medical practices.

## HMS-ESQ (Enhanced System Quality)
**Purpose:** Quality assurance and system improvement.  
**Key Functionality:** Quality metrics, testing frameworks, improvement analytics.  
**When to Use:** When implementing quality control or system quality improvement.

## HMS-ESR (Economic System Representation)
**Purpose:** Economic modeling and simulation.  
**Key Functionality:** Economic models, market simulation, financial projection.  
**When to Use:** When modeling economic systems or simulating market behaviors.

## HMS-ETL (Extract, Transform, Load)
**Purpose:** Data pipeline and transformation system.  
**Key Functionality:** Data extraction, transformation rules, data loading.  
**When to Use:** When building data pipelines or transformation processes.

## HMS-FLD (Field Data Collection)
**Purpose:** Mobile and field data collection tools.  
**Key Functionality:** Mobile forms, offline capabilities, field synchronization.  
**When to Use:** When collecting data in the field or via mobile devices.

## HMS-GOV (Governance Framework)
**Purpose:** System governance and compliance management.  
**Key Functionality:** Policy enforcement, compliance checking, governance workflows.  
**When to Use:** When implementing governance rules or compliance requirements.

## HMS-LLM (Large Language Model Operations Platform)
**Purpose:** Comprehensive LLMOps platform for building, deploying, and monitoring production-grade LLM applications.  
**Key Functionality:** Prompt playground, prompt management, configuration versioning, LLM evaluation, human evaluation, observability, tracing, cost and performance monitoring.  
**When to Use:** When developing LLM applications that require systematic experimentation, evaluation, deployment, and monitoring. Particularly valuable for engineering and product teams creating reliable LLM apps that need:
- Comparing outputs across multiple LLM models
- Building custom LLM workflows (RAG, agents, etc.)
- Evaluating LLM performance using automated or human evaluators
- Managing and versioning prompts across environments
- Monitoring usage, costs, and performance metrics
- Tracing and debugging LLM application behavior

## HMS-MCP (Model-Compute-Publish)
**Purpose:** Framework for model execution and result publishing.  
**Key Functionality:** Model execution, computation management, result distribution.  
**When to Use:** When running AI models and distributing their outputs.

## HMS-MFE (Micro Frontend Engine)
**Purpose:** Micro frontend architecture and management.  
**Key Functionality:** Frontend composition, UI integration, module federation.  
**When to Use:** When building modular frontend applications or UI components.

## HMS-MKT (Market Analytics)
**Purpose:** Market analysis and business intelligence.  
**Key Functionality:** Market trends, competitive analysis, opportunity identification.  
**When to Use:** When analyzing markets or conducting business intelligence activities.

## HMS-NFO (National Financial Organizations)
**Purpose:** Management system for financial organization data.  
**Key Functionality:** Financial institution data, regulatory information, organizational analytics.  
**When to Use:** When working with financial organizations or regulatory frameworks.

## HMS-OMS (Order Management System)
**Purpose:** Order processing and management.  
**Key Functionality:** Order capture, fulfillment workflows, inventory integration.  
**When to Use:** When implementing systems for order processing or management.

## HMS-OPS (Operations Management)
**Purpose:** Operational processes and management tools.  
**Key Functionality:** Process automation, operational metrics, workflow optimization.  
**When to Use:** When building operational systems or process automation.

## HMS-RED (Reactive Data Engine)
**Purpose:** Reactive data processing and event handling.  
**Key Functionality:** Event processing, data streams, reactive patterns.  
**When to Use:** When implementing event-driven or reactive data systems.

## HMS-SCM (Supply Chain Management)
**Purpose:** Supply chain visibility and management.  
**Key Functionality:** Inventory tracking, supplier management, logistics coordination.  
**When to Use:** When implementing supply chain solutions or logistics systems.

## HMS-SKL (Skills Management)
**Purpose:** Skills tracking and development system.  
**Key Functionality:** Skills assessment, learning paths, competency tracking.  
**When to Use:** When building skills development or management systems.

## HMS-SME (Subject Matter Expertise)
**Purpose:** Knowledge management and expert systems.  
**Key Functionality:** Expert knowledge capture, knowledge graphs, expertise identification.  
**When to Use:** When developing systems for knowledge management or expert assistance.

## HMS-SYS (System Core)
**Purpose:** Core system infrastructure and services.  
**Key Functionality:** Service discovery, message routing, system monitoring.  
**When to Use:** When working on core infrastructure or system-wide services.

## HMS-UHC (Universal Healthcare Components)
**Purpose:** Universal healthcare system components.  
**Key Functionality:** Care coordination, population health, universal access.  
**When to Use:** When building universal healthcare systems or components.

## HMS-UTL (Utilities)
**Purpose:** Common utilities and shared functions.  
**Key Functionality:** Helper functions, common patterns, shared utilities.  
**When to Use:** When you need common functionality shared across multiple components.

## Rules for Adding New System Components

All directories with the `HMS-` prefix are considered system components and must follow these guidelines:

1. **Naming Convention**: 
   - Use the prefix `HMS-` followed by a three-letter uppercase acronym (e.g., `HMS-XYZ`)
   - Choose a unique acronym that clearly represents the component's purpose
   - Document the acronym meaning in both the component README and in this SYSTEM_CONTEXT.md file

2. **Required Documentation**:
   - Each component must include a detailed README.md
   - Must include a CLAUDE.md file with component-specific guidance
   - Must have a docs/ directory with detailed documentation
   - Must document integration points with other HMS components

3. **Directory Structure**:
   - Follow the standardized structure outlined in CLAUDE.md
   - Include src/, tests/, and examples/ directories
   - Provide clear separation of concerns within the component

4. **Agent Implementation**:
   - Every component requires a dedicated agent implementation
   - Agent must implement the verification-first principle
   - Must support Chain of Recursive Thoughts (CoRT) for reasoning
   - Must include agent_profile.yaml defining capabilities

5. **Registration Process**:
   - New components must be added to this SYSTEM_CONTEXT.md file
   - Must register with HMS-DOC for documentation integration
   - Must register with HMS-DEV for development workflow integration
   - Must define integration points with other components

6. **Component Requirements**:
   - Must solve a specific, well-defined problem in the ecosystem
   - Must not duplicate functionality of existing components
   - Must include comprehensive tests and examples
   - Must follow the HMS code style guidelines

## Component Integration Guidelines

When working across multiple HMS components:

1. Use HMS-DEV for development workflows and tool registration
2. Document all integration points in HMS-DOC
3. Utilize HMS-A2A for agent communication between components
4. Leverage HMS-MCP for model execution across components
5. Consult HMS-SYS for core infrastructure services
6. Register monetizable tools with the HMS-DEV marketplace

Each component has its own dedicated agent responsible for managing everything related to that component within the ecosystem. Agents should use external validators rather than other LLMs for verification, and implement Chain of Recursive Thoughts (CoRT) for complex decisions.