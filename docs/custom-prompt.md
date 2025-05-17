# HMS System Custom Prompts

This file contains custom prompts for use when analyzing Hardison Management Systems (HMS) components - an Expert-Led, Data-Driven, AI-Powered multi-party workflow automation platform for governments and private industry.

## HMS-API Prompt

When analyzing HMS-API, focus on these aspects:

```
As you analyze the HMS-API codebase, pay special attention to:

1. **Core Model Architecture**:
   - How `app/Models` are organized, particularly Core, Program, and Protocol models
   - The inheritance and dependency relationships between models
   - Key interfaces and abstract classes that define the architecture

2. **Module Organization**:
   - The structure and purpose of the `Modules/` directory
   - How modules interact with models
   - Patterns used for module composition and extension

3. **Deal Flow Implementation**:
   - How the 5-step deal pattern is implemented in code
   - Classes and interfaces related to problem definition, solution codification, 
     program setup, execution, and outcome verification
   - Data structures that support the deal flow process

4. **Legislative Process Components**:
   - Code related to the 10-step legislative workflow
   - How legislative steps interact with the deal flow system
   - Components responsible for tracking legislative progress

5. **API Structure**:
   - Key controllers and routes that expose functionality
   - Authentication and authorization mechanisms
   - How the API supports multiple frontend clients (GOV, MKT, MFE)

Your analysis should help developers understand both the high-level architecture 
and the detailed implementation patterns that enable the complex deal flow and 
legislative process integration.
```

## HMS-GOV Prompt

When analyzing HMS-GOV, focus on these aspects:

```
As you analyze the HMS-GOV Vue.js codebase, pay special attention to:

1. **Admin Interface Components**:
   - Vue components for managing policies and programs
   - Dashboard elements for monitoring legislative process
   - User interface patterns for governance workflows
   - How the "gov-ai.co" domain interfaces are structured

2. **HMS-API Integration**:
   - How the Vue frontend connects to HMS-API endpoints
   - Authentication and session management
   - Data fetching and state management patterns (Vuex, composables)
   - How tenant and program models are accessed and managed

3. **Agency Layer Visualization**:
   - Components that represent the three agency layers (Governance, Management, Interface)
   - How administrators interact with these different layers
   - Visualization of agency relationships and hierarchies
   - How regional governance (federal/state/local) is represented

4. **Legislative Workflow UI**:
   - How the 10-step legislative process is represented in the interface
   - Vue components for tracking and managing legislative progress
   - User permissions and roles related to legislative actions
   - How the hierarchy of governance levels affects workflows

5. **Deal Flow Interaction**:
   - UI elements for initiating and monitoring deals
   - How the 5-step deal pattern is exposed to administrators
   - Forms and workflows for deal creation and management
   - Integration with the agent system for administrative assistance

Your analysis should help developers understand how the Vue.js administrative interface 
enables governance of the HMS system, particularly how it provides tools for 
managing the legislative process and deal flow across different governance levels.
```

## HMS-MKT Prompt

When analyzing HMS-MKT, focus on these aspects:

```
As you analyze the HMS-MKT Vue.js codebase, pay special attention to:

1. **Program Creation Interface**:
   - Components in `pages/protocol-builder/_protocol` and `pages/protocol-builder`
   - How users create and configure programs and protocols
   - The UI flow for program setup and configuration
   - How program configurations map to HMS-API models

2. **Module Components**:
   - Components in `components/Modules`
   - How they correspond to modules in HMS-API's `Modules/` directory
   - Reusable module patterns and component structure
   - Data validation and submission to the API

3. **Marketplace Integration**:
   - Components in `components/marketplace`
   - How programs are shared, discovered, and purchased
   - User interaction patterns for marketplace activities
   - Integration with payment and distribution systems

4. **Agent Interaction**:
   - Components in `pages/follow-program/_target/_id/agent.vue`
   - State management in `store/agent.js`
   - How users interact with agents during program usage
   - Connection patterns to HMS-A2A services

5. **Domain Structure Implementation**:
   - How the "ai-gov.co" domains are structured and routed
   - Regional differences in interfaces (federal/state/local)
   - How routing and navigation works across the platform
   - User session and context management

Your analysis should help developers understand how the Vue.js user interface 
enables program creation, management, and interaction with the HMS system,
particularly how end users leverage the platform for program engagement.
```

## HMS-MFE Prompt

When analyzing HMS-MFE, focus on these aspects:

```
As you analyze the HMS-MFE Vue.js codebase, pay special attention to:

1. **Micro-Frontend Architecture**:
   - How components are structured for embedding in other applications
   - Component isolation and communication patterns
   - Styling and theming approaches for consistent UI
   - Loading and initialization patterns
   - Directory structure in `src/components/pages/*`

2. **Specialized Interface Components**:
   - Implementations of specialized interfaces like:
     - Banking dashboards (`src/components/pages/dashboards/banking/`)
     - Food delivery interface (`src/components/pages/apps/FoodDeliveryApp.vue`)
     - Course dashboard (`src/components/pages/dashboards/business/CourseDashboard.vue`)
     - Task management (`src/components/pages/apps/KanbanApp.vue`)
     - Publishing tools (`/article`, `/story-board`, `/video`)
     - Program dashboards (`/dashboard/orders`, `/invoice`, `/dashboard/sales`, `/dashboard/health`)
     - Booking interfaces (`/booking`, `/housing`)
     - Messaging interfaces (`/messaging`, `/chat`)
     - Form interfaces (`/form/*`)
     - Wizards (`src/pages/wizard-v1`)
     - Status interfaces (`/status`)
     - Jobs interfaces (`/jobs`)
     - Analytics interfaces (`/analytics`)
     - Finance interfaces (`/finance/bank`, `/finance/fund`, `/finance/acct`)
     - Team interfaces (`/team/card`)
     - Card interfaces (`/card/*`)

3. **Integration with HMS-MKT and Programs**:
   - How components are loaded and embedded in the main applications
   - Data passing and state synchronization approaches
   - Event handling between parent and micro-frontend
   - Authentication and authorization handling
   - How agents select appropriate MFE components based on program context

4. **Agency Mappings and Government Integration**:
   - How components map to agency goals via `fed.agents.json`
   - Customization for federal, state, and local government requirements
   - Domain-specific adaptations for program types
   - Integration with program protocols and policy requirements

5. **Customization and Adaptability**:
   - How the same component can be used for different program contexts
   - For example, how Kanban boards can be used for both business tasks and wedding planning
   - How wizards can be adapted for different onboarding processes like ICE and DHS
   - Configuration options and extension points
   - Theming and styling customization
   - Feature toggles and capability management

Your analysis should help developers understand how the micro-frontend architecture
provides specialized, reusable UI components that can be embedded in different
program contexts while maintaining consistent user experience, and how these components
are selected and used by agents to help users complete their programs.
```

## HMS-A2A Prompt

When analyzing HMS-A2A, focus on these aspects:

```
As you analyze the HMS-A2A codebase, pay special attention to:

1. **Agent Architecture**:
   - Core agent implementation and lifecycle
   - Agent capabilities and skill management
   - Communication protocols between agents
   - Integration with language models and AI services

2. **Integration with HMS-API**:
   - How agents connect to `app/Agents` in HMS-API
   - Data access patterns and permissions
   - Event handling and notifications
   - State synchronization between systems

3. **User Interaction Patterns**:
   - How agents are surfaced to users through frontends
   - Conversation management and context handling
   - UI components for agent interaction
   - Feedback mechanisms and learning patterns

4. **Program Assistance Capabilities**:
   - How agents help users navigate programs
   - Domain-specific knowledge and reasoning
   - Task automation and workflow assistance
   - Decision support and recommendations

5. **MFE Component Selection**:
   - How agents determine appropriate interfaces for users
   - Selection logic for matching MFE components to program contexts
   - Dynamic interface generation based on user needs
   - Integration with HMS-MFE component library

6. **Multi-level Support**:
   - How agents support both administrators and end-users
   - Contextual understanding of user roles and permissions
   - Different interaction patterns based on user type
   - Knowledge sharing between agent instances

7. **Integration with HMS-AGX**:
   - How agents leverage deeper research from HMS-AGX
   - Knowledge graph consumption and application
   - Handling user obstacles and program improvements
   - Feedback loops for continuously improving programs

Your analysis should help developers understand how the agent system provides
intelligent assistance throughout the HMS platform, connecting users with
the capabilities they need across different roles and program contexts, and
how it selects appropriate interfaces to help users complete their programs.
```

## HMS-AGX Prompt

When analyzing HMS-AGX, focus on these aspects:

```
As you analyze the HMS-AGX codebase, pay special attention to:

1. **Knowledge Graph Architecture**:
   - Core graph data structures and relationships
   - Node and edge representations for program context
   - Graph construction and maintenance algorithms
   - Query patterns and traversal optimizations

2. **Integration with HMS-A2A and Programs**:
   - How HMS-AGX connects to HMS-A2A for agent assistance
   - Knowledge representation for program obstacles and solutions
   - Data flow between program execution and deep research
   - Feedback mechanisms for program improvement

3. **Research Capabilities**:
   - Deep research methodologies and algorithms
   - Information extraction and synthesis
   - Domain-specific knowledge representation
   - Context building for complex program scenarios

4. **Interface Generation**:
   - How research insights influence interface creation
   - Connection to HMS-MFE component recommendations
   - Customization patterns for specialized user needs
   - Adaptation to different program types and contexts

5. **User Obstacle Analysis**:
   - Pattern recognition for identifying user challenges
   - Classification of common program obstacles
   - Personalized assistance strategies
   - Success metric tracking and optimization

6. **Continuous Improvement Mechanisms**:
   - Learning from user interactions
   - Program refinement suggestions
   - Protocol optimization based on research findings
   - Cross-program knowledge transfer

Your analysis should help developers understand how the deep research system
enhances the overall HMS platform by providing deeper context understanding
when users encounter obstacles, and how this research drives improvements
to programs, protocols, and interfaces.
```

## HMS-CDF Prompt

When analyzing HMS-CDF, focus on these aspects:

```
As you analyze the HMS-CDF (Codified Democracy Foundation) Rust codebase, pay special attention to:

1. **Legislative Process Engine**:
   - Core Rust implementation of the legislative process
   - How the `legislative_process.json` defines the workflow
   - Performance optimizations for high-throughput processing
   - Real-time codification of laws at "AI-speed"

2. **Integration with HMS-GOV**:
   - How the CDF engine is accessed by HMS-GOV instances
   - API endpoints for policy management
   - Authentication and governance controls
   - Cross-domain communication patterns

3. **Voting System Architecture**:
   - Global instant voting mechanisms at scale
   - Verification and validation of voting processes
   - Optimization techniques for high-performance vote processing
   - Security measures for democratic integrity

4. **Democratic Process Representation**:
   - How democratic principles are codified in the system
   - Representation of various governance structures
   - Adaptability to different political systems
   - Balance between efficiency and deliberative processes

5. **Agent Direction and Compliance**:
   - How HMS-CDF guides agent behavior through policy
   - Compliance verification mechanisms
   - Integration with HMS-A2A for agent governance
   - Audit trails and transparency features

6. **Multi-party Workflow Management**:
   - Rust data structures for representing complex workflows
   - Cross-organizational process coordination
   - State management and persistence
   - Error handling and recovery processes

Your analysis should help developers understand how the Rust-based HMS-CDF engine
enables "AI-speed" democratic processes while maintaining governance integrity,
and how it serves as the foundation for policy management throughout the HMS ecosystem.
```

## HMS-NFO Prompt

When analyzing HMS-NFO, focus on these aspects:

```
As you analyze the HMS-NFO (System-Level Information Repository) codebase, pay special attention to:

1. **System-Level Information Structure**:
   - Organization of the `_/SYSTEM-LEVEL/` directory
   - Schema and content of `fed.json` and `std.json`
   - Referential integrity between system-level documents
   - Versioning and change management approaches

2. **Legislative Process Reference Data**:
   - How system-level information supports the legislative process
   - Reference data structures and taxonomies
   - Standard definitions and protocols
   - Configuration parameters for HMS-CDF

3. **Knowledge Graph Support**:
   - How HMS-NFO data is consumed by HMS-AGX for knowledge graph generation
   - Reference information for entity relationships
   - Domain-specific knowledge organization
   - Ontology and semantic structures

4. **Cross-Component Integration**:
   - How HMS-NFO serves as a central reference for other HMS components
   - Data sharing patterns across the ecosystem
   - Consistency enforcement mechanisms
   - System-wide configuration management

5. **Government and Agency Structure Representation**:
   - How government hierarchies and relationships are modeled
   - Agency definitions and capabilities
   - Cross-agency interaction patterns
   - Regional and jurisdictional modeling

6. **Standards and Protocol Definitions**:
   - Standard formats and protocols used across the HMS ecosystem
   - Interoperability specifications
   - Compliance requirements and validation rules
   - Evolution of standards over time

Your analysis should help developers understand how HMS-NFO provides critical
reference information that enables consistent operation across the HMS ecosystem,
particularly for the legislative process and knowledge graph generation.
```

## Domain Structure Analysis Prompt

When analyzing the HMS domain structure, focus on these aspects:

```
As you analyze the HMS domain structure, pay special attention to:

1. **Domain Organization Patterns**:
   - The hierarchical structure of domains (federal, state, local)
   - Naming conventions across different domain types
   - Relationship between domains and organizational structures
   - Domain grouping by function, service type, and governance level

2. **Political and Administrative Domains**:
   - Structure and purpose of political interfaces (dnc.dev, rnc.dev)
   - Agency collaboration hub patterns (agency.dev, gov.agency.dev)
   - Admin policy interface organization (region.country.gov-ai.co)
   - Federal agency subdomain patterns (agency.us.gov-ai.co)

3. **User and Program Interface Domains**:
   - Main user interface domains (region.country.ai-gov.co)
   - AI governance utility domains (gov-ai.co, ai-gov.co)
   - Status monitoring domain structures (us-gov.ai, log.medicare.dev)
   - Domain separation between admin and user interfaces

4. **Service-Specific Domain Families**:
   - Healthcare domain family (medicare.dev, nhs.dev, spuhc.ai)
   - Education domain family (pub.school, pub.education)
   - Condition-specific domain families (ibd.center ecosystem)
   - Community service domain patterns (naacp.ai, xx.clinic, xy.clinic)

5. **Domain-Component Relationships**:
   - How domains map to specific HMS-MFE components
   - Relationship between domains and HMS-API modules
   - How domains integrate with the agent system
   - Cross-domain navigation and authentication patterns

6. **Domain Configuration and Management**:
   - Configuration files governing domain routing (from domainConfigs)
   - Component mapping between domains and Vue.js components
   - Domain-specific styling, branding, and configuration
   - Domain metadata management for SEO and accessibility

Your analysis should help developers understand the comprehensive domain ecosystem
that connects all HMS components, how different domain families serve specific
purposes, and how the domain structure supports the overall workflow automation
platform across government and private industry contexts.
```