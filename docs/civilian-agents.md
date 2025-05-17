# Civilian Agents

This document provides detailed guidance on implementing and using Civilian Agents in the Codex-GOV system, which enables public-facing AI assistants for government agencies to serve citizens.

## Overview

Civilian Agents are specialized AI agents designed specifically for public-facing government interactions. Unlike Government Agents which handle internal operations, Civilian Agents focus exclusively on providing accessible, equitable, and informative assistance to citizens interacting with government agencies.

## Key Characteristics

Civilian Agents are distinguished by several key characteristics:

1. **Public Information Only**: Access is strictly limited to publicly available information
2. **Equitable Service**: Designed to provide fair and equal service to all citizens
3. **Plain Language**: Communication prioritizes clarity and accessibility
4. **Privacy Protection**: Enhanced safeguards for citizen data and queries
5. **Verification-First**: All information provided is verified against authoritative sources
6. **Multi-Channel Support**: Available across web, mobile, and other access points
7. **Accessibility**: WCAG 2.1 AA compliant with support for assistive technologies

## Implementation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Civilian Agent System                     │
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                  A2A Protocol Interface                      │
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                    Civilian Base Agent                       │
└───────────────────────────────┬─────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
┌───────────────▼───────────────┐ ┌─────────────▼─────────────┐
│    Chain of Recursive         │ │      Public Access        │
│        Thoughts               │ │       Controls            │
└───────────────┬───────────────┘ └─────────────┬─────────────┘
                │                               │
┌───────────────▼───────────────┐ ┌─────────────▼─────────────┐
│   Public-Facing Tools &       │ │  Specialized Engagements  │
│        Services               │ │   (Programs, Benefits)    │
└───────────────────────────────┘ └───────────────────────────┘
```

## Civilian Agent Implementation

### CivilianAgent Class

The `CivilianAgent` class extends the `BaseAgent` with public-facing capabilities:

```python
class CivilianAgent(BaseAgent):
    """Agent for civilian engagement with government."""
    
    def __init__(
        self,
        agency_label: str,
        agency_name: str,
        domain: str,
        supported_standards: List[str],
        model_name: str = "gemini-2.0-flash",
        port: int = None
    ):
        super().__init__(
            agency_label=agency_label,
            agency_name=agency_name,
            domain=domain,
            supported_standards=supported_standards,
            model_name=model_name,
            port=port
        )
        # Initialize only public-facing tools
        self._initialize_public_tools()
        
    def _initialize_public_tools(self):
        """Initialize only public-facing tools."""
        self.tools = []
        
        # Add program information tool
        self.tools.append(ProgramInformationTool(self.agency_label))
        
        # Add benefits eligibility tool
        self.tools.append(BenefitsEligibilityTool(self.agency_label))
        
        # Add document requirements tool
        self.tools.append(DocumentRequirementsTool(self.agency_label))
        
        # Add location finder tool
        self.tools.append(LocationFinderTool(self.agency_label))
        
        # Add form assistance tool
        self.tools.append(FormAssistanceTool(self.agency_label))
        
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
        You must NEVER pretend to be able to perform actual government services or claim 
        official authority that you do not have.
        
        Always clarify that you are an AI assistant providing information, not an official 
        government representative who can take official actions.
        """
        
    def validateTask(self, task: TaskRequest) -> ValidationResult:
        """Validate a task against public service standards."""
        issues = []
        
        # Check for requests for non-public information
        if self._contains_nonpublic_request(task.query):
            issues.append(ValidationIssue(
                standard="PUBLIC_INFO_ONLY",
                description="Request for non-public or internal information",
                severity="critical",
                recommendation="Explain that you can only provide publicly available information"
            ))
        
        # Check for requests for preferential treatment
        if self._contains_preferential_request(task.query):
            issues.append(ValidationIssue(
                standard="EQUAL_SERVICE",
                description="Request for preferential treatment",
                severity="critical",
                recommendation="Explain that you provide equal service to all individuals"
            ))
        
        # Check for potentially harmful advice
        if self._contains_harmful_advice_request(task.query):
            issues.append(ValidationIssue(
                standard="SAFE_ADVICE",
                description="Request for potentially harmful advice",
                severity="critical",
                recommendation="Provide safe, accurate information only"
            ))
        
        # Validate against agency-specific standards
        agency_issues = self._validate_agency_standards(task.query)
        issues.extend(agency_issues)
        
        return ValidationResult(
            valid=len([i for i in issues if i.severity == "critical"]) == 0,
            issues=issues
        )
        
    def _contains_nonpublic_request(self, query: str) -> bool:
        """Check if query requests non-public information."""
        nonpublic_indicators = [
            "internal", "classified", "confidential", "sensitive",
            "secret", "private", "personal data", "personnel", 
            "not public", "restricted", "secure", "login", "password"
        ]
        
        query_lower = query.lower()
        for indicator in nonpublic_indicators:
            if indicator in query_lower:
                return True
                
        return False
        
    def _contains_preferential_request(self, query: str) -> bool:
        """Check if query requests preferential treatment."""
        preferential_indicators = [
            "special treatment", "priority", "bypass", "skip the line",
            "ahead of others", "faster than normal", "expedite",
            "special access", "favor", "pull strings"
        ]
        
        query_lower = query.lower()
        for indicator in preferential_indicators:
            if indicator in query_lower:
                return True
                
        return False
        
    def _contains_harmful_advice_request(self, query: str) -> bool:
        """Check if query requests potentially harmful advice."""
        harmful_indicators = [
            "avoid taxes", "evade", "circumvent", "loophole", 
            "get around", "bypass security", "ignore regulation",
            "without reporting", "hide from"
        ]
        
        query_lower = query.lower()
        for indicator in harmful_indicators:
            if indicator in query_lower:
                return True
                
        return False
```

### CoRT-Enhanced Civilian Agent

The `CoRTCivilianAgent` enhances the standard civilian agent with Chain of Recursive Thoughts capabilities:

```python
class CoRTCivilianAgent(CoRTAgentMixin, CivilianAgent):
    """Civilian agent with Chain of Recursive Thoughts capabilities."""
    
    def __init__(
        self,
        agency_label: str,
        agency_name: str,
        domain: str,
        supported_standards: List[str],
        model_name: str = "gemini-2.0-flash",
        port: int = None,
        cort_max_rounds: int = 2,  # Fewer rounds for civilian interactions
        cort_alternatives: int = 2,  # Fewer alternatives for civilian interactions
        cort_enabled_by_default: bool = False  # Disabled by default for efficiency
    ):
        super().__init__(
            agency_label=agency_label,
            agency_name=agency_name,
            domain=domain,
            supported_standards=supported_standards,
            model_name=model_name,
            port=port,
            cort_max_rounds=cort_max_rounds,
            cort_alternatives=cort_alternatives
        )
        
        self.cort_enabled_by_default = cort_enabled_by_default
        
    def process_task(self, task: TaskRequest) -> TaskResponse:
        """Process a task with recursive thinking capabilities if enabled."""
        # Determine if CoRT should be used - enabled for complex queries
        use_cort = self.cort_enabled_by_default
        if task.metadata and "use_cort" in task.metadata:
            use_cort = bool(task.metadata["use_cort"])
        
        # Enable CoRT automatically for complex questions
        if self._is_complex_query(task.query):
            use_cort = True
            
        # Rest of implementation
        # ...
        
    def _is_complex_query(self, query: str) -> bool:
        """Determine if a query is complex and would benefit from CoRT."""
        # Check length - longer queries tend to be more complex
        if len(query.split()) > 20:
            return True
            
        # Check for complex question indicators
        complex_indicators = [
            "eligibility", "qualify for", "requirements for", "how do I apply",
            "appeal process", "exception", "waiver", "compare", "difference between",
            "timeline for", "deadline", "extension", "special circumstances"
        ]
        
        query_lower = query.lower()
        for indicator in complex_indicators:
            if indicator in query_lower:
                return True
                
        return False
```

## Public-Facing Tools

Civilian Agents have access to a range of specialized public-facing tools:

### ProgramInformationTool

```python
class ProgramInformationTool(Tool):
    """Tool for accessing public program information."""
    
    def __init__(self, agency_label: str):
        super().__init__(
            name="program_information",
            description="Get information about government programs",
            agency_label=agency_label
        )
        
    async def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get information about a government program."""
        program_name = args.get("program_name", "")
        detail_level = args.get("detail_level", "summary")
        
        # Fetch program information from public data source
        # Implement access to program database filtered for public information only
        
        return {
            "name": program_name,
            "agency": self.agency_label,
            "description": "Program description",
            "eligibility": "Eligibility requirements",
            "application_process": "Application process details",
            "deadlines": "Upcoming deadlines",
            "contact_information": "Public contact information"
        }
```

### BenefitsEligibilityTool

```python
class BenefitsEligibilityTool(Tool):
    """Tool for checking potential benefits eligibility."""
    
    def __init__(self, agency_label: str):
        super().__init__(
            name="benefits_eligibility",
            description="Check potential eligibility for benefits programs",
            agency_label=agency_label
        )
        
    async def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Check potential eligibility for a benefits program."""
        program_name = args.get("program_name", "")
        
        # IMPORTANT: This is a pre-screening only, not official determination
        # Civilian agents must clearly communicate this limitation
        
        # PRIVACY: No PII is collected or stored during this process
        
        return {
            "program": program_name,
            "potential_eligibility": "Based on general requirements",
            "next_steps": "How to officially apply",
            "disclaimer": "This is not an official determination of eligibility."
        }
```

### DocumentRequirementsTool

```python
class DocumentRequirementsTool(Tool):
    """Tool for identifying required documents for government services."""
    
    def __init__(self, agency_label: str):
        super().__init__(
            name="document_requirements",
            description="Get information about required documents",
            agency_label=agency_label
        )
        
    async def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get document requirements for a government service."""
        service_name = args.get("service_name", "")
        
        # Fetch document requirements from public source
        
        return {
            "service": service_name,
            "required_documents": [
                {"name": "Document 1", "description": "Purpose and requirements"},
                {"name": "Document 2", "description": "Purpose and requirements"}
            ],
            "alternative_documents": [
                {"name": "Alternative 1", "description": "When this can be used"}
            ],
            "submission_method": "How to submit documents"
        }
```

### LocationFinderTool

```python
class LocationFinderTool(Tool):
    """Tool for finding government service locations."""
    
    def __init__(self, agency_label: str):
        super().__init__(
            name="location_finder",
            description="Find government service locations",
            agency_label=agency_label
        )
        
    async def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Find service locations near a specified area."""
        service_type = args.get("service_type", "")
        zip_code = args.get("zip_code", "")
        
        # PRIVACY: Only zip code is used, not precise location
        
        # Fetch locations from public database
        
        return {
            "service_type": service_type,
            "locations": [
                {
                    "name": "Location 1",
                    "address": "Public address",
                    "hours": "Operating hours",
                    "services": ["Service 1", "Service 2"],
                    "contact": "Public contact information",
                    "accessibility": "Accessibility information"
                }
            ]
        }
```

### FormAssistanceTool

```python
class FormAssistanceTool(Tool):
    """Tool for providing guidance on government forms."""
    
    def __init__(self, agency_label: str):
        super().__init__(
            name="form_assistance",
            description="Get help with government forms",
            agency_label=agency_label
        )
        
    async def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Provide guidance on completing a government form."""
        form_number = args.get("form_number", "")
        section = args.get("section", "all")
        
        # IMPORTANT: This provides general guidance only, not legal advice
        # Civilian agents must clearly communicate this limitation
        
        return {
            "form": form_number,
            "section": section,
            "guidance": "General guidance on completing this section",
            "common_mistakes": "Common errors to avoid",
            "additional_resources": "Where to get more help",
            "disclaimer": "This is general guidance only, not legal advice."
        }
```

## HMS Integration

Civilian Agents integrate with various HMS components to provide comprehensive services:

### HMS-MKT Integration

```python
class HMSMKTIntegration:
    """Integration with HMS-MKT for civilian engagement."""
    
    def __init__(self, agent: CivilianAgent):
        self.agent = agent
        
    async def get_program_listing(self) -> List[Dict[str, Any]]:
        """Get a list of available programs for the agency."""
        # Implement integration with HMS-MKT program listing
        
    async def get_service_status(self, service_id: str) -> Dict[str, Any]:
        """Get the current status of a service."""
        # Implement integration with HMS-MKT service status
        
    async def get_application_requirements(self, program_id: str) -> Dict[str, Any]:
        """Get requirements for a program application."""
        # Implement integration with HMS-MKT application requirements
```

### HMS-MFE Integration

```python
class HMSMFEIntegration:
    """Integration with HMS-MFE for specialized interfaces."""
    
    def __init__(self, agent: CivilianAgent):
        self.agent = agent
        
    async def get_form_interface(self, form_id: str) -> Dict[str, Any]:
        """Get specialized form interface."""
        # Implement integration with HMS-MFE form interface
        
    async def get_dashboard_component(self, dashboard_type: str) -> Dict[str, Any]:
        """Get specialized dashboard component."""
        # Implement integration with HMS-MFE dashboard component
```

## Deployment and Implementation

### Creating Civilian Agents

```python
from gov_agents import AgentFactory

# Create a standard civilian agent
irs_agent = AgentFactory.create_civilian_agent("IRS")

# Create a CoRT-enhanced civilian agent
ssa_agent = AgentFactory.create_civilian_agent(
    "SSA",
    use_cort=True,
    cort_max_rounds=3,
    cort_alternatives=2
)

# Create all civilian agents
all_civilian_agents = AgentFactory.create_all_civilian_agents()
```

### Deployment Options

Civilian Agents can be deployed in various contexts:

1. **Web Integration**: Embedded in agency websites
2. **Mobile Applications**: Integrated with agency mobile apps
3. **Call Center Support**: Assisting human call center staff
4. **Kiosk Deployment**: Self-service kiosks in government offices
5. **SMS Interface**: Text message-based assistance
6. **Smart Speaker**: Voice-based assistance

### Web Integration Example

```javascript
// React component for agency website
import React, { useState, useEffect } from 'react';
import { useCivilianAgent } from '@codex-gov/civilian-integration';

const AgencyAssistant = ({ agencyId }) => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const { agent, status } = useCivilianAgent(agencyId);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    setLoading(true);
    
    const result = await agent.ask({
      query,
      useCoRT: true,  // Enable for complex queries
      includeReferences: true,  // Include source citations
      accessibility: {
        format: 'simple',  // Use simplified language
        screenReader: true  // Optimize for screen readers
      }
    });
    
    setResponse(result);
    setLoading(false);
  };
  
  return (
    <div className="agency-assistant">
      <h2>{agencyId} Virtual Assistant</h2>
      
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="How can I help you today?"
          aria-label="Ask a question"
        />
        <button type="submit" disabled={loading || status !== 'ready'}>
          {loading ? 'Processing...' : 'Ask'}
        </button>
      </form>
      
      {response && (
        <div className="response">
          <div className="answer">{response.answer}</div>
          
          {response.references && (
            <div className="references">
              <h3>Sources:</h3>
              <ul>
                {response.references.map((ref, i) => (
                  <li key={i}>
                    <a href={ref.url} target="_blank" rel="noopener noreferrer">
                      {ref.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {response.next_steps && (
            <div className="next-steps">
              <h3>Next Steps:</h3>
              <ul>
                {response.next_steps.map((step, i) => (
                  <li key={i}>{step}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AgencyAssistant;
```

## Best Practices

### Plain Language

Civilian Agents must communicate using plain language principles:

1. **Simple Words**: Use everyday language instead of jargon
2. **Active Voice**: Prefer active voice for clarity
3. **Short Sentences**: Keep sentences brief and focused
4. **Concrete Examples**: Provide specific examples to illustrate points
5. **Organized Structure**: Present information in a logical sequence
6. **Visual Aids**: Use lists, headings, and white space effectively

### Accessibility

Civilian Agents must adhere to accessibility best practices:

1. **WCAG Compliance**: Meet WCAG 2.1 AA standards
2. **Screen Reader Support**: Ensure content works with screen readers
3. **Keyboard Navigation**: Support keyboard-only navigation
4. **Alternative Text**: Provide alt text for all non-text content
5. **Color Contrast**: Maintain sufficient color contrast
6. **Simple Language**: Use plain language for cognitive accessibility

### Privacy Protection

Civilian Agents must implement robust privacy protections:

1. **Minimal Data Collection**: Collect only what's necessary
2. **Secure Storage**: Protect any stored conversation data
3. **Session Isolation**: Maintain strict session boundaries
4. **PII Handling**: Special protections for personally identifiable information
5. **Clear Disclosures**: Transparent privacy practices
6. **Retention Policies**: Clear policies on data retention

### Equitable Service

Civilian Agents must ensure equitable service to all users:

1. **Consistent Responses**: Same information regardless of how it's asked
2. **Language Support**: Multiple language capabilities
3. **Cultural Sensitivity**: Awareness of cultural differences
4. **Digital Divide**: Alternatives for those with limited digital access
5. **Equal Prioritization**: No preferential treatment in response time or quality
6. **Diverse Testing**: Test with diverse user populations

## Example Use Cases

### Service Information

```
User: When is the IRS office in Atlanta open?

IRS Agent: The IRS Taxpayer Assistance Center in Atlanta is located at 401 W. Peachtree St NW, and is open Monday through Friday from 8:30 AM to 4:30 PM. It's closed on federal holidays.

You'll need to make an appointment before visiting. You can schedule one by calling 844-545-5640.

Would you like to know what services are available at this location or what documents to bring for your visit?
```

### Benefits Eligibility

```
User: Am I eligible for Social Security disability benefits?

SSA Agent: To be eligible for Social Security disability benefits, you generally need to:

1. Have worked enough years while paying Social Security taxes
2. Have a medical condition that meets Social Security's definition of disability, which requires that:
   - You cannot do the work you did before
   - You cannot adjust to other work due to your medical condition
   - Your disability has lasted or is expected to last at least one year or result in death

This is just general information. For a personalized assessment, you should:
1. Use the Benefit Eligibility Screening Tool at https://ssabest.benefits.gov/
2. Start an application at https://www.ssa.gov/benefits/disability/
3. Call Social Security at 1-800-772-1213

Would you like more information about the application process or required documentation?
```

### Form Assistance

```
User: I don't understand how to fill out line 8b on tax form 1040.

IRS Agent: Line 8b on Form 1040 is for reporting qualified dividends, which are dividends that qualify for lower tax rates than ordinary income.

You'll find this information in Box 1b of your Form 1099-DIV that you received from companies where you own stock, mutual funds, or other investments that pay dividends.

Simply enter the total amount from all your 1099-DIV forms (Box 1b) on line 8b of your Form 1040.

Important: This is general guidance only. For personalized tax advice, please consult with a tax professional.

Would you like help with any other lines on the 1040 form?
```

### Program Application

```
User: How do I apply for a small business loan from the SBA?

SBA Agent: To apply for a small business loan through the SBA, follow these steps:

1. Determine which loan program fits your needs:
   - 7(a) loans: General small business loans up to $5 million
   - 504 loans: For major fixed assets like equipment or real estate
   - Microloans: Smaller amounts up to $50,000

2. Find an SBA-approved lender: Use the Lender Match tool at https://www.sba.gov/funding-programs/loans/lender-match

3. Prepare your application materials, including:
   - Business plan
   - Financial statements
   - Business and personal tax returns
   - Business licenses
   - Loan application history

4. Submit your application through your chosen lender

The specific requirements and process may vary by loan type and lender. Would you like more information about a specific loan program or help preparing your application materials?
```

## Monitoring and Improvement

Civilian Agents require ongoing monitoring and improvement:

1. **Usage Analytics**: Track common queries and issues
2. **Satisfaction Metrics**: Measure user satisfaction
3. **Error Analysis**: Identify and address common errors
4. **Regular Updates**: Keep information current with policy changes
5. **Feedback Loop**: Incorporate user feedback into improvements
6. **A/B Testing**: Test alternative approaches to determine effectiveness

## Conclusion

Civilian Agents provide a powerful means for government agencies to engage with the public. By implementing these agents with proper security, privacy, accessibility, and equity considerations, agencies can provide improved service to citizens while maintaining compliance with government standards and regulations.

The implementation described in this document ensures that Civilian Agents serve as effective, responsible, and helpful assistants for citizens interacting with government agencies across various channels and contexts.

For implementation details, see the [Agent Architecture](agent_architecture.md) and [HMS Integration](hms_integration.md) documentation.