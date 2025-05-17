# HMS Integration

This document outlines how Codex-GOV integrates with the HMS (Health Management System) component ecosystem to create a comprehensive government AI system.

## Overview

Codex-GOV is designed to integrate seamlessly with the following HMS components:

1. **HMS-A2A**: Agent-to-Agent communication framework
2. **HMS-GOV**: Administrative interface for policy and legislation
3. **HMS-API**: Core backend services and business logic
4. **HMS-CDF**: Legislative engine for real-time lawmaking
5. **HMS-AGX**: Knowledge graph builder for policy insights
6. **HMS-SVC**: Program and protocol management
7. **HMS-MKT**: Citizen-facing program management interfaces
8. **HMS-MFE**: Micro frontends for specialized interfaces
9. **HMS-UHC/EHR/EMR**: Healthcare-specific components
10. **HMS-ACH/CUR**: Financial transaction components

## Integration Architecture

```
                     ┌───────────────┐
                     │    HMS-SYS    │
                     │(Infrastructure)│
                     └───────┬───────┘
                             │
            ┌────────────────┴────────────────┐
            │                                 │
    ┌───────▼──────┐                 ┌────────▼────────┐
    │    HMS-SVC   │◄───────────────►│     HMS-A2A     │
    │(Core Backend)│                 │  (AI/ML Agents)  │
    └───────┬──────┘                 └────────┬─────────┘
            │                                 │
            │                       ┌─────────┴─────────┐
            │                       │                   │
            │              ┌────────▼────────┐  ┌───────▼───────┐
            │              │ Specialized     │  │  Government   │
            │              │   Agents        │  │    Agents     │
            │              └────────┬────────┘  └───────┬───────┘
            │                       │                   │
    ┌───────▼───────┐      ┌────────▼────────┐  ┌───────▼───────┐
    │   HMS-DTA/NFO │◄─────┤  A2A Protocol   │  │  MCP Protocol │
    │ (Data & ETL)  │      │  Integration    │  │  Integration  │
    └───────────────┘      └─────────────────┘  └───────────────┘
```

## HMS-A2A Integration

HMS-A2A serves as the core AI/ML Agent layer in the Codex-GOV platform:

### Integration Points

1. **Core Framework**: Codex-GOV leverages HMS-A2A's agent framework and Chain of Recursive Thoughts
2. **MCP Protocol**: Uses Model Context Protocol for agent communication
3. **Government Agent System**: Inherits the government agent implementation
4. **Specialized Agents**: Accesses domain-specific specialized agents

### Implementation Example

```python
from gov_agents import AgentFactory
from hms_a2a.integration import HMSIntegration

# Create a government agent
fbi_agent = AgentFactory.create_government_agent("FBI")

# Access HMS-A2A integration
hms_integration = HMSIntegration()

# Register the agent with HMS-A2A
hms_integration.register_agent(fbi_agent)

# Access specialized agents
agriculture_agent = hms_integration.get_specialized_agent("agriculture")
telemedicine_agent = hms_integration.get_specialized_agent("telemedicine")

# Collaborate between agents
collaboration_session = hms_integration.create_collaboration_session(
    [fbi_agent, agriculture_agent],
    session_type="cross_domain_investigation"
)
```

## HMS-GOV Integration

HMS-GOV provides the administrative interface for policy and legislation:

### Integration Points

1. **Policy Management**: Interface for defining and managing policies
2. **Legislative Framework**: Tools for creating and evaluating legislation
3. **Administrative Dashboard**: Management interface for Codex-GOV
4. **User Governance**: Access control and permissions management

### Implementation Example

```javascript
// Vue.js component in HMS-GOV that integrates with Codex-GOV
import { ref, onMounted } from 'vue'
import { useCodexGov } from '@/composables/useCodexGov'

export default {
  setup() {
    const { getAgencies, getAgentInsights, createLegislation } = useCodexGov()
    const agencies = ref([])
    const selectedAgency = ref(null)
    const legislativeInsights = ref(null)
    
    onMounted(async () => {
      agencies.value = await getAgencies()
    })
    
    const selectAgency = async (agency) => {
      selectedAgency.value = agency
      legislativeInsights.value = await getAgentInsights(agency.id, 'legislative')
    }
    
    const createNewLegislation = async (draft) => {
      const result = await createLegislation({
        agencyId: selectedAgency.value.id,
        draft,
        useCoRT: true  // Enable Chain of Recursive Thoughts
      })
      return result
    }
    
    return {
      agencies,
      selectedAgency,
      legislativeInsights,
      selectAgency,
      createNewLegislation
    }
  }
}
```

## HMS-API Integration

HMS-API serves as the primary backend service for Codex-GOV:

### Integration Points

1. **Data Access**: Access to centralized data services
2. **Business Logic**: Core application logic and rules
3. **Agent Management**: Backend for agent management
4. **Authentication**: Identity and access management

### Implementation Example

```php
<?php
// Laravel API endpoint in HMS-API for Codex-GOV integration
namespace App\Http\Controllers;

use App\Models\GovAgent;
use App\Services\CodexGovService;
use Illuminate\Http\Request;

class GovAgentController extends Controller
{
    protected $codexGovService;
    
    public function __construct(CodexGovService $codexGovService)
    {
        $this->codexGovService = $codexGovService;
    }
    
    public function processQuery(Request $request, $agencyId)
    {
        $this->authorize('access-agency', $agencyId);
        
        $query = $request->input('query');
        $useCoRT = $request->input('use_cort', false);
        
        $response = $this->codexGovService->processAgentQuery($agencyId, $query, $useCoRT);
        
        return response()->json($response);
    }
    
    public function listAgencies()
    {
        $agencies = GovAgent::where('active', true)
            ->with('capabilities')
            ->paginate(20);
            
        return response()->json($agencies);
    }
}
```

## HMS-CDF Integration

HMS-CDF provides the legislative engine for real-time lawmaking:

### Integration Points

1. **Legislative Processing**: Policy and legislation processing
2. **Real-time Democracy Workflows**: Streamlined legislative processes
3. **Compliance Validation**: Automated legislative compliance checks
4. **Impact Assessment**: Evaluation of legislative impacts

### Implementation Example

```rust
// Rust integration in HMS-CDF for Codex-GOV
use cdf::legislative_engine::{LegislativeProcessor, PolicyValidator};
use codex_gov::agents::GovernmentAgent;

pub async fn process_legislation(
    legislation_text: String,
    agency_id: String,
    use_cort: bool,
) -> Result<LegislationAnalysis, Error> {
    // Create a legislative processor
    let processor = LegislativeProcessor::new();
    
    // Parse the legislation
    let parsed = processor.parse(legislation_text)?;
    
    // Access the government agent for evaluation
    let agent = GovernmentAgent::for_agency(&agency_id)?;
    
    // Process with CoRT if enabled
    let analysis = if use_cort {
        agent.evaluate_legislation_with_cort(parsed, 4, 3)?
    } else {
        agent.evaluate_legislation(parsed)?
    };
    
    // Validate against policy requirements
    let validator = PolicyValidator::new();
    let validation = validator.validate(&analysis)?;
    
    Ok(LegislationAnalysis {
        summary: analysis.summary,
        impacts: analysis.impacts,
        compliance: validation.compliance_status,
        recommendations: analysis.recommendations,
        thinking_trace: analysis.thinking_trace,
    })
}
```

## HMS-AGX Integration

HMS-AGX provides knowledge graph capabilities for deeper insights:

### Integration Points

1. **Knowledge Graph**: Graph-based representation of domain knowledge
2. **Relationship Mapping**: Connections between entities and concepts
3. **Inference Engine**: Automated reasoning over graph data
4. **Visualization**: Graph visualization tools

### Implementation Example

```typescript
// TypeScript integration with HMS-AGX
import { KnowledgeGraph } from '@hms/agx-client';
import { GovernmentAgentFactory } from '@codex-gov/agents';

async function buildAgencyKnowledgeGraph(agencyId: string): Promise<void> {
  // Create the knowledge graph
  const graph = new KnowledgeGraph({
    name: `${agencyId}-knowledge-graph`,
    description: `Knowledge graph for ${agencyId}`,
  });
  
  // Create a government agent for the agency
  const agent = await GovernmentAgentFactory.createGovernmentAgent(agencyId);
  
  // Extract domain knowledge
  const domainKnowledge = await agent.extractDomainKnowledge();
  
  // Add entities to the graph
  for (const entity of domainKnowledge.entities) {
    await graph.addEntity(entity);
  }
  
  // Add relationships
  for (const relationship of domainKnowledge.relationships) {
    await graph.addRelationship(relationship);
  }
  
  // Add policies as specialized nodes
  for (const policy of domainKnowledge.policies) {
    await graph.addSpecializedNode('policy', policy);
  }
  
  // Persist the graph
  await graph.persist();
  
  // Analyze the graph for insights
  const insights = await graph.generateInsights();
  
  return insights;
}
```

## HMS-SVC Integration

HMS-SVC provides program and protocol management:

### Integration Points

1. **Program Management**: Creation and management of government programs
2. **Protocol Execution**: Step-by-step protocol execution
3. **Assessment Modules**: Specialized assessment functionality
4. **Notification Systems**: Alert and notification management

### Implementation Example

```python
from hms_svc.program import ProgramManager
from hms_svc.protocol import ProtocolExecutor
from codex_gov.agents import AgentRegistry

# Get the agency registry
registry = AgencyRegistry()

# Get an agent for the Small Business Administration
sba_agent = registry.get_government_agent("SBA")

# Create a program manager
program_manager = ProgramManager()

# Create a loan application program
loan_program = program_manager.create_program(
    name="Small Business Loan Application",
    agency_id="SBA",
    description="Application process for small business loans"
)

# Add protocols to the program
loan_program.add_protocol(
    name="Eligibility Assessment",
    steps=[
        {"type": "form", "name": "Business Information"},
        {"type": "document_upload", "name": "Financial Statements"},
        {"type": "agent_assessment", "agent_id": sba_agent.id}
    ]
)

loan_program.add_protocol(
    name="Application Review",
    steps=[
        {"type": "agent_assessment", "agent_id": sba_agent.id},
        {"type": "human_review", "role": "loan_officer"},
        {"type": "decision", "options": ["approve", "reject", "request_more_info"]}
    ]
)

# Create a protocol executor
executor = ProtocolExecutor()

# Execute a protocol for a specific application
result = executor.execute_protocol(
    protocol_id=loan_program.protocols[0].id,
    application_id="APP-12345",
    context={
        "use_cort": True,
        "max_rounds": 3,
        "thinking_depth": "detailed"
    }
)
```

## HMS-MKT Integration

HMS-MKT provides the main frontend for citizen-facing program management:

### Integration Points

1. **Program Discovery**: Interface for discovering government programs
2. **Application Flows**: User interfaces for program applications
3. **Agent Assistance**: Integration of civilian agents for assistance
4. **Eligibility Checks**: Automated eligibility verification

### Implementation Example

```javascript
// Vue.js component in HMS-MKT that integrates with Codex-GOV
import { ref, onMounted } from 'vue'
import { useCivilianAgent } from '@/composables/useCivilianAgent'

export default {
  setup() {
    const { getAgent, askQuestion, checkEligibility } = useCivilianAgent()
    const selectedProgram = ref(null)
    const question = ref('')
    const response = ref('')
    const eligibilityResult = ref(null)
    const agentInstance = ref(null)
    
    onMounted(async () => {
      // Get the civilian agent for the program's agency
      agentInstance.value = await getAgent(selectedProgram.value.agencyId)
    })
    
    const askAgentQuestion = async () => {
      response.value = await askQuestion(agentInstance.value.id, question.value)
    }
    
    const checkProgramEligibility = async (userProfile) => {
      eligibilityResult.value = await checkEligibility(
        agentInstance.value.id,
        selectedProgram.value.id,
        userProfile
      )
    }
    
    return {
      selectedProgram,
      question,
      response,
      eligibilityResult,
      askAgentQuestion,
      checkProgramEligibility
    }
  }
}
```

## HMS-MFE Integration

HMS-MFE provides micro frontends for specialized interfaces:

### Integration Points

1. **Micro Frontend Components**: Specialized UI components
2. **Dashboard Integration**: Integration with data dashboards
3. **Workflow UIs**: User interfaces for government workflows
4. **Visualization Tools**: Data visualization components

### Implementation Example

```typescript
// TypeScript integration with HMS-MFE
import { MicroFrontendRegistry } from '@hms/mfe-registry';
import { AgentAssistant } from '@codex-gov/civilian-agent';

export async function registerAgentComponents() {
  // Get the MFE registry
  const registry = new MicroFrontendRegistry();
  
  // Register agent assistant component
  await registry.register({
    name: 'agent-assistant',
    component: AgentAssistant,
    props: {
      placement: 'bottom-right',
      theme: 'government',
      persistenceEnabled: true
    },
    routes: ['*'],  // Available on all routes
    permissions: ['citizen.basic']
  });
  
  // Register agency-specific components
  for (const agency of await getAgencies()) {
    await registry.register({
      name: `${agency.id}-dashboard`,
      component: () => import(`./components/${agency.id}-dashboard.vue`),
      routes: [`/agency/${agency.id}/*`],
      permissions: [`agency.${agency.id}.view`]
    });
  }
}
```

## HMS-UHC/EHR/EMR Integration

Integration with healthcare-specific HMS components:

### Integration Points

1. **Healthcare Data Access**: Access to healthcare data systems
2. **Patient Information**: Secure access to patient records
3. **Clinical Workflows**: Integration with clinical processes
4. **Medical Knowledge**: Access to medical knowledge bases

### Implementation Example

```python
from hms_ehr.client import EHRClient
from hms_uhc.eligibility import EligibilityService
from codex_gov.agents import AgentFactory

# Create a government agent for HHS
hhs_agent = AgentFactory.create_government_agent("HHS", use_cort=True)

# Connect to EHR system
ehr_client = EHRClient(secure=True, hipaa_compliant=True)

# Connect to eligibility service
eligibility_service = EligibilityService()

# Create a healthcare-aware agent processor
async def process_healthcare_query(query, patient_id=None, user_role=None):
    # Check access permissions
    if patient_id and not eligibility_service.check_access(user_role, patient_id):
        return {"error": "Access denied"}
    
    # For patient-specific queries, get relevant EHR data
    context = {}
    if patient_id:
        context["patient_data"] = await ehr_client.get_patient_summary(patient_id)
    
    # Process with HHS agent
    response = await hhs_agent.process_task(
        query,
        metadata={
            "use_cort": True,
            "domain": "healthcare",
            "context": context
        }
    )
    
    return response
```

## HMS-ACH/CUR Integration

Integration with financial transaction HMS components:

### Integration Points

1. **Financial Transactions**: Processing government payments
2. **Budget Management**: Integration with budget systems
3. **Financial Reporting**: Automated financial reports
4. **Compliance Tracking**: Financial compliance monitoring

### Implementation Example

```python
from hms_ach.client import ACHClient
from hms_cur.budget import BudgetService
from codex_gov.agents import AgentFactory

# Create a government agent for the Treasury
treasury_agent = AgentFactory.create_government_agent("Treasury", use_cort=True)

# Connect to ACH system
ach_client = ACHClient(secure=True)

# Connect to budget service
budget_service = BudgetService()

# Create a transaction processor
async def process_financial_operation(operation_type, amount, recipient_id, program_id):
    # Verify budget allocation
    budget_check = await budget_service.check_allocation(program_id, amount)
    if not budget_check["sufficient"]:
        return {"error": "Insufficient budget allocation"}
    
    # Get agent insights
    insights = await treasury_agent.process_task(
        f"Analyze financial transaction of {amount} for {recipient_id} under {program_id}",
        metadata={
            "use_cort": True,
            "domain": "finance",
            "operation_type": operation_type
        }
    )
    
    # If approved, process the transaction
    if insights.status == "success" and not insights.needs_human_review:
        transaction = await ach_client.create_transaction({
            "amount": amount,
            "recipient_id": recipient_id,
            "program_id": program_id,
            "description": insights.message,
            "approved_by": "treasury_agent"
        })
        return {"status": "success", "transaction_id": transaction.id}
    else:
        return {"status": "pending_review", "insights": insights.message}
```

## Security Considerations

When integrating Codex-GOV with HMS components, the following security considerations must be addressed:

1. **Data Isolation**: Each component maintains isolation of sensitive data
2. **Authentication**: Robust authentication between components
3. **Access Control**: Fine-grained access control for all integrations
4. **Audit Logging**: Comprehensive logging of all cross-component operations
5. **Encryption**: End-to-end encryption for all data transfers
6. **Compliance Checks**: Automated compliance validation at integration points

## Best Practices

1. **Use Agent Registry**: Access agents through the centralized registry
2. **Leverage CoRT**: Enable Chain of Recursive Thoughts for complex decisions
3. **Batch Operations**: Use batch operations for efficiency when appropriate
4. **Enable Monitoring**: Implement comprehensive monitoring across all integrations
5. **Follow Security Guidelines**: Adhere to component-specific security requirements
6. **Validate Compliance**: Verify compliance at each integration point
7. **Document Integrations**: Maintain detailed documentation of all integration points

## Conclusion

The integration of Codex-GOV with the HMS component ecosystem creates a powerful government AI system that combines the strengths of each component. Through these integrations, Codex-GOV provides advanced agent capabilities, policy management, legislative processing, knowledge graphs, program management, and user interfaces for both government operations and citizen engagement.

For more details on specific components, see the documentation for each HMS system.