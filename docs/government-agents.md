# Government Agents

This document provides an in-depth guide to the Government Agent system in Codex-GOV, which enables AI agents to represent government agencies for both internal operations and civilian engagement.

## Overview

The Government Agent system provides a framework for creating AI agents that represent government agencies at federal, state, local, and international levels. These agents combine advanced reasoning capabilities with strict compliance enforcement to ensure secure, compliant, and efficient government operations.

## Agent Types

### Government Agent

The `GovernmentAgent` class provides an agent for internal government operations:

- Access to all agency tools and capabilities
- Compliance with government-specific standards
- Enhanced security and validation
- Internal process knowledge
- Government-specific prompt instructions

```python
from gov_agents import AgentFactory

# Create a government agent for the FBI
fbi_agent = AgentFactory.create_government_agent("FBI")

# Process a government task
response = await fbi_agent.process_task(
    "Analyze internal threat assessment data for cybersecurity vulnerabilities"
)
```

### Civilian Agent

The `CivilianAgent` class provides a public-facing agent for civilians:

- Limited to public-facing tools only
- Focus on citizen service and assistance
- Prevention of sensitive information disclosure
- Public service standards compliance
- Equitable service to all individuals

```python
from gov_agents import AgentFactory

# Create a civilian agent for the IRS
irs_agent = AgentFactory.create_civilian_agent("IRS")

# Process a civilian query
response = await irs_agent.process_task(
    "How do I file for a tax extension?"
)
```

### CoRT-Enhanced Government Agent

The `CoRTGovernmentAgent` class enhances the standard government agent with Chain of Recursive Thoughts capabilities:

- Multiple alternatives generation for complex decisions
- Self-critique and evaluation of each alternative
- Recursive thinking for improved decision quality
- Transparent reasoning traces for accountability

```python
from gov_agents import AgentFactory

# Create a CoRT-enhanced government agent for the Department of Defense
dod_agent = AgentFactory.create_government_agent(
    "DoD",
    use_cort=True,
    cort_max_rounds=4,
    cort_alternatives=3
)

# Process a security assessment with enhanced reasoning
response = await dod_agent.process_task(
    "Evaluate potential security vulnerabilities in the proposed system",
    metadata={"use_cort": True}
)
```

## Agency Registry

The `AgencyRegistry` provides centralized management of agency agents:

```python
from gov_agents import AgencyRegistry

# Get the registry singleton
registry = AgencyRegistry()

# Get an agent for a specific agency
cia_agent = registry.get_government_agent("CIA")
ssa_agent = registry.get_civilian_agent("SSA")

# List all available agencies
agencies = registry.list_agencies()

# Check if an agency exists
exists = registry.agency_exists("EPA")
```

## Agent Factory

The `AgentFactory` provides methods for creating different types of agents:

```python
from gov_agents import AgentFactory

# Create a government agent
fbi_agent = AgentFactory.create_government_agent("FBI")

# Create a civilian agent
irs_agent = AgentFactory.create_civilian_agent("IRS")

# Create all government agents
all_gov_agents = AgentFactory.create_all_government_agents()

# Create all civilian agents
all_civilian_agents = AgentFactory.create_all_civilian_agents()
```

## MCP Integration

The system integrates with the Model Context Protocol (MCP) through:

```python
from gov_agents import register_all_agencies_as_mcp_tools

# Register all agency agents as MCP tools
tools = register_all_agencies_as_mcp_tools()

# Get a specific agency MCP tool
from gov_agents import GovAgentMCPRegistry
mcp_registry = GovAgentMCPRegistry()
fbi_tool = mcp_registry.get_tool("FBI_government_agent")
```

## Supported Agencies

The system currently supports agents for all major federal agencies, including:

### Executive Departments

- Department of Agriculture (USDA)
- Department of Commerce (DOC)
- Department of Defense (DoD)
- Department of Education (ED)
- Department of Energy (DOE)
- Department of Health and Human Services (HHS)
- Department of Homeland Security (DHS)
- Department of Housing and Urban Development (HUD)
- Department of the Interior (DOI)
- Department of Justice (DOJ)
- Department of Labor (DOL)
- Department of State (DOS)
- Department of Transportation (DOT)
- Department of the Treasury
- Department of Veterans Affairs (VA)

### Independent Agencies and Government Corporations

- Central Intelligence Agency (CIA)
- Environmental Protection Agency (EPA)
- Federal Bureau of Investigation (FBI)
- Federal Communications Commission (FCC)
- Federal Emergency Management Agency (FEMA)
- Federal Reserve System (Fed)
- General Services Administration (GSA)
- National Aeronautics and Space Administration (NASA)
- National Science Foundation (NSF)
- Nuclear Regulatory Commission (NRC)
- Securities and Exchange Commission (SEC)
- Small Business Administration (SBA)
- Social Security Administration (SSA)
- United States Agency for International Development (USAID)
- United States Postal Service (USPS)

### State and Local Government Support

The system can also be configured for state and local government agencies with customizable standards and regulations.

## Standards Compliance

All government agents enforce compliance with applicable regulations and standards:

- **FISMA**: Federal Information Security Modernization Act
- **FedRAMP**: Federal Risk and Authorization Management Program
- **HIPAA**: Health Insurance Portability and Accountability Act for healthcare agencies
- **NIST**: National Institute of Standards and Technology cybersecurity framework
- **OMB**: Office of Management and Budget guidelines
- **GSA**: General Services Administration procurement regulations
- **Agency-specific policies**: Individual agency regulations and procedures

## Task Processing

### Task Request Structure

```python
class TaskRequest:
    """Request to process a task."""
    
    id: str                                  # Unique identifier
    query: str                               # The task query
    session_id: Optional[str] = None         # Optional session identifier
    metadata: Optional[Dict[str, Any]] = None # Optional metadata
```

### Task Response Structure

```python
class TaskResponse:
    """Response from processing a task."""
    
    id: str                                  # Matching request identifier
    status: str                              # Success, error, or pending
    message: str                             # Response message
    artifacts: Optional[List[Dict[str, Any]]] = None # Additional data
    needs_human_review: bool = False         # Whether human review is needed
```

### Processing Flow

1. **Validation**: Task is validated against agency standards
2. **Processing**: Task is processed with appropriate tools
3. **Enhancement**: Response is enhanced with CoRT if enabled
4. **Compliance Check**: Final response is checked for compliance
5. **Human Review Flag**: Critical responses are flagged for review

```python
# Task processing flow
def process_task(self, task: TaskRequest) -> TaskResponse:
    # Validate task against standards
    validation_result = self.validateTask(task)
    if not validation_result.valid:
        # Handle validation failures
        
    # Process the task
    if self._task_needs_tools(task.query):
        # Process with tools
        response = self._process_with_tools(task)
    else:
        # Process directly
        response = self._process_directly(task)
    
    # Enhance with CoRT if enabled
    if self._should_use_cort(task):
        response = self._enhance_with_cort(task, response)
    
    # Final compliance check
    final_validation = self.validateResponse(response)
    
    # Flag for human review if needed
    needs_review = self._needs_human_review(task, response)
    
    # Return the final response
    return TaskResponse(
        id=task.id,
        status="success",
        message=response,
        artifacts=self._create_artifacts(task, response),
        needs_human_review=needs_review
    )
```

## Domain-Specific Prompting

Each agent type has specialized prompt instructions:

### Government Agent Prompting

```python
def getDomainPromptInstructions(self) -> str:
    """Get government-specific prompt instructions."""
    return f"""
    You are an internal government agent for {self.agency_name} ({self.agency_label}).
    
    Agency Mission:
    {self.agency_mission}
    
    You have access to internal government tools and processes for {self.domain}.
    
    Key Responsibilities:
    1. Provide accurate, authoritative information about internal government operations
    2. Maintain security and confidentiality of sensitive information
    3. Ensure compliance with all applicable regulations and standards
    4. Support internal government functions and workflows
    
    Your responses must adhere to the following standards:
    {self._format_standards()}
    
    You must prioritize security, privacy, and compliance in all operations.
    """
```

### Civilian Agent Prompting

```python
def getDomainPromptInstructions(self) -> str:
    """Get public service prompt instructions."""
    return f"""
    You are a public-facing representative of {self.agency_name} ({self.agency_label}).
    
    Agency Mission:
    {self.agency_mission}
    
    You have access to public information only about {self.domain}.
    
    Key Responsibilities:
    1. Provide accurate, helpful information to the public
    2. Assist civilians with navigating government services
    3. Ensure equitable service to all individuals
    4. Protect privacy and confidentiality of all individuals
    
    Your responses must adhere to the following standards:
    {self._format_standards()}
    
    You must NOT provide any non-public information or give preferential treatment.
    """
```

## Chain of Recursive Thoughts Integration

Government agents can be enhanced with Chain of Recursive Thoughts (CoRT) capabilities for improved reasoning:

```python
# Create a government agent with CoRT
agent = GovernmentAgent("Department of Defense", "DoD")

# Enable CoRT for complex security assessments
agent.enable_cort(
    max_rounds=4,              # More rounds for security-critical tasks
    generate_alternatives=4,   # Consider multiple security scenarios
    dynamic_rounds=True        # Adapt thinking depth to complexity
)

# Process a sensitive task with chain of thought reasoning
result = await agent.process_with_cort(
    "Evaluate potential security vulnerabilities in the proposed system",
    prompt_instructions="Consider both offensive and defensive perspectives"
)

# Access the complete thinking trace for audit
thinking_trace = result["thinking_trace"]
```

## Security Measures

The government agent system implements robust security measures:

- **Role-Based Access**: Different agent types have different access levels
- **Validation Gates**: All requests and responses are validated against standards
- **Human Review**: Critical operations are flagged for human review
- **Audit Logging**: Comprehensive logging of all agent actions
- **Content Filtering**: Prevention of sensitive information disclosure
- **Compliance Enforcement**: Automatic enforcement of regulatory requirements

## Example Use Cases

### Internal Government Operations

```python
# FBI Threat Analysis
fbi_agent = AgentFactory.create_government_agent("FBI")
response = await fbi_agent.process_task(
    "Analyze the pattern of cybersecurity incidents reported last quarter"
)

# EPA Regulatory Assessment
epa_agent = AgentFactory.create_government_agent("EPA")
response = await epa_agent.process_task(
    "Evaluate compliance of the proposed rule with existing environmental standards"
)

# DoD Security Evaluation
dod_agent = AgentFactory.create_government_agent("DoD", use_cort=True)
response = await dod_agent.process_task(
    "Assess the security implications of the new communication protocol"
)
```

### Civilian Engagement

```python
# IRS Tax Assistance
irs_agent = AgentFactory.create_civilian_agent("IRS")
response = await irs_agent.process_task(
    "What documents do I need to file my small business taxes?"
)

# Social Security Benefits
ssa_agent = AgentFactory.create_civilian_agent("SSA")
response = await ssa_agent.process_task(
    "How do I apply for disability benefits?"
)

# FEMA Disaster Assistance
fema_agent = AgentFactory.create_civilian_agent("FEMA")
response = await fema_agent.process_task(
    "What assistance is available for hurricane victims in my area?"
)
```

## HMS Integration

The Government Agent system integrates with various HMS components:

- **HMS-GOV**: Administrative interface for managing agency agents
- **HMS-API**: Backend services for agent data access
- **HMS-A2A**: Core agent-to-agent communication framework
- **HMS-CDF**: Legislative engine for policy and regulation processing
- **HMS-AGX**: Knowledge graph integration for deeper insights

```python
# Example of using HMS-API integration
from gov_agents.integration import HMSAPIIntegration

# Get HMS-API integration for an agent
api_integration = HMSAPIIntegration(fbi_agent)

# Access data through the integration
user_data = await api_integration.get_user_data(user_id)
program_data = await api_integration.get_program_data(program_id)
```

## Customization

The Government Agent system can be customized for specific needs:

### Adding New Agencies

```python
from gov_agents import AgencyRegistry, BaseAgencyData

# Create new agency data
new_agency = BaseAgencyData(
    agency_label="NEWAGENCY",
    agency_name="New Government Agency",
    domain="specialized_domain",
    mission="The mission of the new agency",
    supported_standards=["STANDARD1", "STANDARD2"]
)

# Register the new agency
registry = AgencyRegistry()
registry.register_agency(new_agency)

# Create agents for the new agency
gov_agent = AgentFactory.create_government_agent("NEWAGENCY")
civilian_agent = AgentFactory.create_civilian_agent("NEWAGENCY")
```

### Custom Agent Implementation

```python
from gov_agents import GovernmentAgent

class SpecializedGovernmentAgent(GovernmentAgent):
    """Specialized government agent with custom capabilities."""
    
    def __init__(self, agency_label, agency_name, domain, supported_standards):
        super().__init__(agency_label, agency_name, domain, supported_standards)
        # Initialize specialized capabilities
        
    def getDomainPromptInstructions(self) -> str:
        """Get specialized prompt instructions."""
        instructions = super().getDomainPromptInstructions()
        # Add specialized instructions
        return instructions + "\nAdditional specialized instructions..."
        
    def process_task(self, task: TaskRequest) -> TaskResponse:
        """Process a task with specialized capabilities."""
        # Custom processing logic
        response = super().process_task(task)
        # Enhance response with specialized capabilities
        return response
```

## Best Practices

1. **Use CoRT for Complex Decisions**: Enable Chain of Recursive Thoughts for complex or critical decisions
2. **Validate All Inputs and Outputs**: Always validate tasks and responses against applicable standards
3. **Store Thinking Traces**: Retain reasoning traces for audit and accountability
4. **Flag for Human Review**: Set `needs_human_review=True` for critical operations
5. **Use Domain-Specific Instructions**: Customize prompt instructions for specific government scenarios
6. **Balance Security and Performance**: Adjust thinking depth based on security requirements and performance needs

## Conclusion

The Government Agent system in Codex-GOV provides a powerful framework for creating AI agents that represent government agencies. By combining advanced reasoning capabilities with strict compliance enforcement, these agents enable secure, compliant, and efficient government operations while providing improved services to citizens.

For implementation details, see the [Agent Architecture](agent_architecture.md) and [Chain of Recursive Thoughts](cort_implementation.md) documentation.