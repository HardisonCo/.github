# Deal Negotiation with Chain of Recursive Thoughts

This document explains how to use the Chain of Recursive Thoughts (CoRT) framework for deal negotiations, legislative evaluation, and policy analysis in the Codex-GOV system.

## Overview

The Deal Negotiation system in Codex-GOV leverages Chain of Recursive Thoughts (CoRT) to enhance decision-making in complex scenarios involving multiple stakeholders, competing priorities, and significant consequences. This approach is particularly valuable for government scenarios such as:

1. **Legislative Evaluation**: Assessing proposed legislation against regulatory requirements
2. **Policy Analysis**: Analyzing the impacts of policy changes
3. **Agency Collaboration**: Negotiating agreements between government agencies
4. **Program Development**: Creating new government programs with multiple components
5. **Resource Allocation**: Determining optimal allocation of limited resources

## Key Components

### CoRTDealEvaluator

The `CoRTDealEvaluator` class provides specialized capabilities for deal evaluations:

```python
class CoRTDealEvaluator:
    """Evaluator for deals using Chain of Recursive Thoughts."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        max_rounds: int = 3,
        generate_alternatives: int = 3,
        dynamic_rounds: bool = True
    ):
        """Initialize the CoRT deal evaluator.
        
        Args:
            llm_generator: Function that generates responses from prompts
            max_rounds: Maximum number of thinking rounds
            generate_alternatives: Number of alternatives to generate per round
            dynamic_rounds: Whether to dynamically determine optimal rounds
        """
        self.processor = CoRTProcessor(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            generate_alternatives=generate_alternatives,
            dynamic_rounds=dynamic_rounds
        )
        
    def evaluate_deal(
        self,
        deal: Deal,
        evaluator_role: str,
        evaluation_criteria: List[Dict[str, str]],
        prompt_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Evaluate a deal with recursive thinking.
        
        Args:
            deal: The deal to evaluate
            evaluator_role: The role of the evaluator
            evaluation_criteria: Criteria for evaluation
            prompt_instructions: Optional domain-specific instructions
            
        Returns:
            Dictionary with the evaluation results including approval status
        """
        # Implement evaluation with recursive thinking
        
    def compare_solutions(
        self,
        problem: Problem,
        solutions: List[Solution],
        evaluator_role: str,
        comparison_criteria: List[Dict[str, str]],
        prompt_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Compare solutions with recursive thinking.
        
        Args:
            problem: The problem to solve
            solutions: List of solutions to compare
            evaluator_role: The role of the evaluator
            comparison_criteria: Criteria for comparison
            prompt_instructions: Optional domain-specific instructions
            
        Returns:
            Dictionary with the comparison results
        """
        # Implement comparison with recursive thinking
        
    def negotiate_transaction(
        self,
        transaction: Transaction,
        from_player: Player,
        to_player: Player,
        negotiator_role: str,
        negotiation_context: Dict[str, str],
        prompt_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Negotiate a transaction with recursive thinking.
        
        Args:
            transaction: The transaction to negotiate
            from_player: The sending party
            to_player: The receiving party
            negotiator_role: The role of the negotiator
            negotiation_context: Context for negotiation
            prompt_instructions: Optional domain-specific instructions
            
        Returns:
            Dictionary with the negotiation results
        """
        # Implement negotiation with recursive thinking
```

### Deal Framework

The Deal Framework provides structures for representing deals, problems, solutions, and transactions:

```python
class Deal:
    """Representation of a deal between entities."""
    
    def __init__(
        self,
        name: str,
        description: str,
        participants: List[str],
        deal_type: str = "standard",
        id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.participants = participants
        self.deal_type = deal_type
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.problems = []
        self.solutions = []
        self.transactions = []
        
    def add_problem(self, problem: 'Problem') -> None:
        """Add a problem to the deal."""
        self.problems.append(problem)
        self.updated_at = datetime.now()
        
    def add_solution(self, solution: 'Solution') -> None:
        """Add a solution to the deal."""
        self.solutions.append(solution)
        self.updated_at = datetime.now()
        
    def add_transaction(self, transaction: 'Transaction') -> None:
        """Add a transaction to the deal."""
        self.transactions.append(transaction)
        self.updated_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "participants": self.participants,
            "deal_type": self.deal_type,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "problems": [p.to_dict() for p in self.problems],
            "solutions": [s.to_dict() for s in self.solutions],
            "transactions": [t.to_dict() for t in self.transactions]
        }
```

```python
class Problem:
    """Representation of a problem within a deal."""
    
    def __init__(
        self,
        name: str,
        description: str,
        success_criteria: List[str],
        constraints: List[str],
        id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.success_criteria = success_criteria
        self.constraints = constraints
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "success_criteria": self.success_criteria,
            "constraints": self.constraints,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
```

```python
class Solution:
    """Representation of a solution to a problem."""
    
    def __init__(
        self,
        name: str,
        description: str,
        approach: str,
        problem_id: Optional[str] = None,
        id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.approach = approach
        self.problem_id = problem_id
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "approach": self.approach,
            "problem_id": self.problem_id,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
```

```python
class Transaction:
    """Representation of a transaction between participants."""
    
    def __init__(
        self,
        name: str,
        transaction_type: str,
        amount: float,
        from_player: str,
        to_player: str,
        currency: str,
        description: str,
        terms: List[str],
        id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.transaction_type = transaction_type
        self.amount = amount
        self.from_player = from_player
        self.to_player = to_player
        self.currency = currency
        self.description = description
        self.terms = terms
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "from_player": self.from_player,
            "to_player": self.to_player,
            "currency": self.currency,
            "description": self.description,
            "terms": self.terms,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
```

```python
class Player:
    """Representation of a participant in a deal."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.metadata = metadata or {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "metadata": self.metadata
        }
```

## Government-Specific Implementations

### LegislativeEvaluator

The `LegislativeEvaluator` extends the `CoRTDealEvaluator` for legislative analysis:

```python
class LegislativeEvaluator(CoRTDealEvaluator):
    """Evaluator for legislative proposals using Chain of Recursive Thoughts."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        max_rounds: int = 4,  # More rounds for legislative evaluation
        generate_alternatives: int = 3,
        dynamic_rounds: bool = True
    ):
        super().__init__(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            generate_alternatives=generate_alternatives,
            dynamic_rounds=dynamic_rounds
        )
        
    def evaluate_legislation(
        self,
        legislation_text: str,
        applicable_laws: List[str],
        evaluator_role: str,
        prompt_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Evaluate proposed legislation with recursive thinking.
        
        Args:
            legislation_text: The text of the proposed legislation
            applicable_laws: List of applicable laws and regulations
            evaluator_role: The role of the evaluator
            prompt_instructions: Optional domain-specific instructions
            
        Returns:
            Dictionary with the evaluation results
        """
        # Create a deal object from the legislation
        deal = Deal(
            name="Legislative Proposal",
            description="Evaluation of proposed legislation",
            participants=["legislature", "agencies", "citizens"],
            deal_type="legislation"
        )
        
        # Add problems addressed by the legislation
        problem = Problem(
            name="Regulatory Need",
            description="The regulatory need addressed by this legislation",
            success_criteria=["Constitutional compliance", "Regulatory effectiveness"],
            constraints=["Budget constraints", "Existing laws"]
        )
        deal.add_problem(problem)
        
        # Add the legislation as a solution
        solution = Solution(
            name="Proposed Legislation",
            description=legislation_text[:500] + "...",  # Truncated for brevity
            approach="Legislative approach",
            problem_id=problem.id
        )
        deal.add_solution(solution)
        
        # Define evaluation criteria
        evaluation_criteria = [
            {"name": "Constitutional Compliance", "description": "Does the legislation comply with constitutional requirements?"},
            {"name": "Regulatory Effectiveness", "description": "How effectively does the legislation address the regulatory need?"},
            {"name": "Implementation Feasibility", "description": "How feasible is implementation of the legislation?"},
            {"name": "Stakeholder Impact", "description": "What are the impacts on various stakeholders?"},
            {"name": "Compliance with Existing Laws", "description": "Does the legislation comply with or properly amend existing laws?"}
        ]
        
        # Create domain-specific instructions
        instructions = f"""
        As a legislative evaluator examining this proposed legislation, consider:
        
        1. The text of the legislation: {legislation_text[:1000]}...
        
        2. Applicable laws and regulations:
           {', '.join(applicable_laws)}
        
        3. Consider both the letter and spirit of existing law
        
        4. Analyze potential unintended consequences
        
        5. Evaluate implementation challenges
        
        Provide a thorough analysis with specific references to the text where possible.
        """
        
        if prompt_instructions:
            instructions += "\n\n" + prompt_instructions
        
        # Evaluate the legislation
        result = self.evaluate_deal(
            deal=deal,
            evaluator_role=evaluator_role,
            evaluation_criteria=evaluation_criteria,
            prompt_instructions=instructions
        )
        
        # Add legislation-specific fields
        result["constitutional_concerns"] = self._extract_constitutional_concerns(result)
        result["implementation_recommendations"] = self._extract_implementation_recommendations(result)
        
        return result
        
    def _extract_constitutional_concerns(self, evaluation_result: Dict[str, Any]) -> List[str]:
        """Extract constitutional concerns from evaluation result."""
        # Implementation logic
        
    def _extract_implementation_recommendations(self, evaluation_result: Dict[str, Any]) -> List[str]:
        """Extract implementation recommendations from evaluation result."""
        # Implementation logic
```

### PolicyAnalyzer

The `PolicyAnalyzer` extends the `CoRTDealEvaluator` for policy analysis:

```python
class PolicyAnalyzer(CoRTDealEvaluator):
    """Analyzer for policy proposals using Chain of Recursive Thoughts."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        max_rounds: int = 4,
        generate_alternatives: int = 3,
        dynamic_rounds: bool = True
    ):
        super().__init__(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            generate_alternatives=generate_alternatives,
            dynamic_rounds=dynamic_rounds
        )
        
    def analyze_policy(
        self,
        policy_text: str,
        policy_context: Dict[str, str],
        affected_stakeholders: List[str],
        analyzer_role: str,
        prompt_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze a policy proposal with recursive thinking.
        
        Args:
            policy_text: The text of the proposed policy
            policy_context: Context information for the policy
            affected_stakeholders: List of stakeholders affected by the policy
            analyzer_role: The role of the analyzer
            prompt_instructions: Optional domain-specific instructions
            
        Returns:
            Dictionary with the analysis results
        """
        # Implementation logic similar to evaluate_legislation
        
    def compare_policy_alternatives(
        self,
        policy_problem: str,
        policy_alternatives: List[Dict[str, str]],
        evaluation_criteria: List[Dict[str, str]],
        analyzer_role: str,
        prompt_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Compare alternative policy approaches with recursive thinking.
        
        Args:
            policy_problem: Description of the policy problem
            policy_alternatives: List of alternative policy approaches
            evaluation_criteria: Criteria for evaluation
            analyzer_role: The role of the analyzer
            prompt_instructions: Optional domain-specific instructions
            
        Returns:
            Dictionary with the comparison results
        """
        # Implementation logic
```

### AgencyCollaborator

The `AgencyCollaborator` facilitates collaboration between government agencies:

```python
class AgencyCollaborator:
    """Facilitator for agency collaboration using Chain of Recursive Thoughts."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        agency_registry: 'AgencyRegistry',
        max_rounds: int = 3,
        generate_alternatives: int = 3,
        dynamic_rounds: bool = True
    ):
        self.deal_evaluator = CoRTDealEvaluator(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            generate_alternatives=generate_alternatives,
            dynamic_rounds=dynamic_rounds
        )
        self.agency_registry = agency_registry
        
    async def create_collaboration(
        self,
        lead_agency_id: str,
        partner_agency_ids: List[str],
        collaboration_purpose: str,
        collaboration_scope: str,
        prompt_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a collaboration between agencies with CoRT.
        
        Args:
            lead_agency_id: ID of the lead agency
            partner_agency_ids: IDs of partner agencies
            collaboration_purpose: Purpose of the collaboration
            collaboration_scope: Scope of the collaboration
            prompt_instructions: Optional domain-specific instructions
            
        Returns:
            Dictionary with the collaboration setup
        """
        # Get the agency agents
        lead_agent = self.agency_registry.get_government_agent(lead_agency_id)
        partner_agents = [
            self.agency_registry.get_government_agent(agency_id)
            for agency_id in partner_agency_ids
        ]
        
        # Create players for the deal
        players = [
            Player(
                agent_id=lead_agency_id,
                name=lead_agent.agency_name,
                role="lead_agency"
            )
        ]
        
        for i, partner_agent in enumerate(partner_agents):
            players.append(
                Player(
                    agent_id=partner_agent.agency_label,
                    name=partner_agent.agency_name,
                    role=f"partner_agency_{i+1}"
                )
            )
        
        # Create the collaboration deal
        collaboration_deal = Deal(
            name=f"{lead_agent.agency_name} Collaboration",
            description=collaboration_purpose,
            participants=[player.agent_id for player in players],
            deal_type="agency_collaboration"
        )
        
        # Define the problem
        problem = Problem(
            name="Interagency Coordination",
            description=collaboration_scope,
            success_criteria=[
                "Effective coordination",
                "Clear responsibilities",
                "Measurable outcomes",
                "Regulatory compliance"
            ],
            constraints=[
                "Agency mandates",
                "Budget limitations",
                "Timeline constraints"
            ]
        )
        collaboration_deal.add_problem(problem)
        
        # Define evaluation criteria
        evaluation_criteria = [
            {"name": "Alignment with Agency Missions", "description": "How well does the collaboration align with each agency's mission?"},
            {"name": "Resource Efficiency", "description": "How efficiently does the collaboration use resources?"},
            {"name": "Coordination Mechanisms", "description": "How effective are the coordination mechanisms?"},
            {"name": "Outcome Metrics", "description": "How well-defined are the outcome metrics?"},
            {"name": "Compliance Considerations", "description": "How thoroughly are compliance considerations addressed?"}
        ]
        
        # Generate collaboration structure with CoRT
        result = await self.deal_evaluator.evaluate_deal(
            deal=collaboration_deal,
            evaluator_role="Interagency Coordinator",
            evaluation_criteria=evaluation_criteria,
            prompt_instructions=prompt_instructions
        )
        
        # Extract collaboration structure
        collaboration_structure = {
            "id": str(uuid.uuid4()),
            "lead_agency": lead_agency_id,
            "partner_agencies": partner_agency_ids,
            "purpose": collaboration_purpose,
            "scope": collaboration_scope,
            "responsibilities": self._extract_responsibilities(result),
            "communication_protocol": self._extract_communication_protocol(result),
            "timeline": self._extract_timeline(result),
            "success_metrics": self._extract_success_metrics(result),
            "thinking_trace": result.get("thinking_trace", [])
        }
        
        return collaboration_structure
        
    def _extract_responsibilities(self, result: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extract agency responsibilities from the evaluation result."""
        # Implementation logic
        
    def _extract_communication_protocol(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract communication protocol from the evaluation result."""
        # Implementation logic
        
    def _extract_timeline(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract timeline from the evaluation result."""
        # Implementation logic
        
    def _extract_success_metrics(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract success metrics from the evaluation result."""
        # Implementation logic
```

## Usage Examples

### Legislative Evaluation

```python
# Create a legislative evaluator
from specialized_agents.legislation import LegislativeEvaluator
from langchain_google_genai import ChatGoogleGenerativeAI

# Create a model and LLM generator function
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
def llm_generator(prompt):
    return model.invoke(prompt).content

# Create the evaluator
evaluator = LegislativeEvaluator(
    llm_generator=llm_generator,
    max_rounds=4,
    generate_alternatives=3,
    dynamic_rounds=True
)

# Define the legislation
legislation_text = """
H.R. 1234 - Secure Digital Identity Act of 2023

To establish a framework for federal, state, and private sector entities to develop 
and provide secure digital identity verification systems that protect privacy and
give citizens control over their personal data.

SECTION 1. SHORT TITLE.
This Act may be cited as the "Secure Digital Identity Act of 2023".

SECTION 2. DEFINITIONS.
In this Act:
(1) DIGITAL IDENTITY VERIFICATION - The term "digital identity verification" means...

SECTION 3. ESTABLISHMENT OF DIGITAL IDENTITY FRAMEWORK.
(a) IN GENERAL - The Secretary shall establish a framework for...
"""

# Define applicable laws
applicable_laws = [
    "Privacy Act of 1974",
    "E-Government Act of 2002",
    "REAL ID Act of 2005",
    "NIST Digital Identity Guidelines SP 800-63-3"
]

# Evaluate the legislation
result = evaluator.evaluate_legislation(
    legislation_text=legislation_text,
    applicable_laws=applicable_laws,
    evaluator_role="Legislative Compliance Officer",
    prompt_instructions="Pay special attention to privacy implications and technical feasibility."
)

# Access the results
print(f"Legislative evaluation completed after {result['rounds_completed']} rounds of thinking")
print(f"\nApproval status: {result['approval_status']}")
print("\nConstitutional concerns:")
for concern in result['constitutional_concerns']:
    print(f"- {concern}")
print("\nImplementation recommendations:")
for recommendation in result['implementation_recommendations']:
    print(f"- {recommendation}")
```

### Policy Comparison

```python
# Create a policy analyzer
from specialized_agents.policy import PolicyAnalyzer

# Create the analyzer
analyzer = PolicyAnalyzer(
    llm_generator=llm_generator,
    max_rounds=4,
    generate_alternatives=3,
    dynamic_rounds=True
)

# Define the policy problem
policy_problem = "Reducing carbon emissions from federal government operations by 50% by 2030"

# Define policy alternatives
policy_alternatives = [
    {
        "name": "Electrification Approach",
        "description": "Transition all federal fleet vehicles to electric vehicles and install renewable energy sources at federal facilities.",
        "key_components": [
            "100% EV transition for federal fleet by 2028",
            "Solar and wind installation at all major federal buildings",
            "Energy efficiency retrofits for all buildings",
            "Carbon offset purchases for remaining emissions"
        ]
    },
    {
        "name": "Carbon Pricing Approach",
        "description": "Implement an internal carbon price on all federal operations and use market mechanisms to drive emissions reductions.",
        "key_components": [
            "Internal carbon price of $100/ton CO2e",
            "Departmental carbon budgets with trading allowed",
            "Revenue recycling for green investments",
            "Quarterly emissions reporting and adjustments"
        ]
    },
    {
        "name": "Hybrid Regulatory Approach",
        "description": "Establish regulations mandating specific emissions reductions with flexibility on implementation methods.",
        "key_components": [
            "Mandatory emission reduction targets by department",
            "Annual compliance reporting requirements",
            "Minimum renewable energy purchasing requirements",
            "Travel restrictions and remote work incentives"
        ]
    }
]

# Define evaluation criteria
evaluation_criteria = [
    {"name": "Cost-Effectiveness", "description": "Cost per ton of CO2e reduced"},
    {"name": "Implementation Feasibility", "description": "Practical challenges to implementation"},
    {"name": "Timeline to Impact", "description": "How quickly emissions reductions would occur"},
    {"name": "Co-Benefits", "description": "Additional positive impacts beyond emissions reduction"},
    {"name": "Political Viability", "description": "Likelihood of support from key stakeholders"}
]

# Compare the policy alternatives
result = analyzer.compare_policy_alternatives(
    policy_problem=policy_problem,
    policy_alternatives=policy_alternatives,
    evaluation_criteria=evaluation_criteria,
    analyzer_role="Federal Sustainability Officer",
    prompt_instructions="Consider both short-term implementation challenges and long-term sustainability."
)

# Access the results
print(f"Policy comparison completed after {result['rounds_completed']} rounds of thinking")
print("\nRanked solutions:")
for i, solution in enumerate(result["ranked_solutions"]):
    print(f"{i+1}. {solution['name']}: {solution['summary']}")
print("\nDetailed comparison:")
print(result["comparison"])
```

### Agency Collaboration

```python
# Create an agency collaborator
from gov_agents import AgencyRegistry
from specialized_agents.collaboration import AgencyCollaborator

# Get the agency registry
registry = AgencyRegistry()

# Create the collaborator
collaborator = AgencyCollaborator(
    llm_generator=llm_generator,
    agency_registry=registry,
    max_rounds=3,
    generate_alternatives=3,
    dynamic_rounds=True
)

# Create a collaboration
result = await collaborator.create_collaboration(
    lead_agency_id="FEMA",
    partner_agency_ids=["EPA", "HHS", "DOT"],
    collaboration_purpose="Coordinated response to extreme weather events",
    collaboration_scope="Establish joint protocols for emergency response, public health protection, and infrastructure recovery during and after extreme weather events.",
    prompt_instructions="Focus on clear communication protocols and rapid deployment capabilities."
)

# Access the results
print(f"Collaboration framework created for {result['lead_agency']} with {len(result['partner_agencies'])} partner agencies")
print("\nResponsibilities:")
for agency, responsibilities in result["responsibilities"].items():
    print(f"\n{agency}:")
    for responsibility in responsibilities:
        print(f"- {responsibility}")
print("\nCommunication Protocol:")
print(result["communication_protocol"])
print("\nTimeline:")
for milestone in result["timeline"]:
    print(f"- {milestone['date']}: {milestone['description']}")
print("\nSuccess Metrics:")
for metric in result["success_metrics"]:
    print(f"- {metric['name']}: {metric['description']}")
```

## Integration with HMS-CDF

The Deal Negotiation system integrates with HMS-CDF (Legislative Engine) for legislative processing:

```python
from specialized_agents.legislation import LegislativeEvaluator
from hms_integration.cdf import HMSCDFIntegration

# Create legislative evaluator
evaluator = LegislativeEvaluator(llm_generator=llm_generator)

# Create HMS-CDF integration
cdf_integration = HMSCDFIntegration()

# Evaluate legislation with HMS-CDF context
async def evaluate_with_cdf_context(legislation_id: str, evaluator_role: str) -> Dict[str, Any]:
    # Get legislation from HMS-CDF
    legislation = await cdf_integration.get_legislation(legislation_id)
    
    # Get applicable laws from HMS-CDF
    applicable_laws = await cdf_integration.get_applicable_laws(legislation)
    
    # Get legislative history from HMS-CDF
    legislative_history = await cdf_integration.get_legislative_history(legislation_id)
    
    # Create custom instructions with CDF context
    instructions = f"""
    Evaluate this legislation in the context of its legislative history:
    {legislative_history}
    
    Consider the specific procedural requirements for this type of legislation,
    as well as the substantive legal requirements.
    """
    
    # Evaluate the legislation
    result = evaluator.evaluate_legislation(
        legislation_text=legislation.text,
        applicable_laws=applicable_laws,
        evaluator_role=evaluator_role,
        prompt_instructions=instructions
    )
    
    # Store results in HMS-CDF
    await cdf_integration.store_evaluation(legislation_id, result)
    
    return result
```

## Security and Compliance

The Deal Negotiation system implements several security and compliance measures:

1. **Thinking Trace Auditing**: Complete record of all alternatives considered and evaluations made
2. **Verification Checks**: Mandatory compliance validation at each stage
3. **Human Review**: Critical evaluations are flagged for human review
4. **Access Controls**: Role-based access to different evaluation capabilities
5. **Regulatory References**: Explicit citations of relevant regulations and standards
6. **Fairness Mechanisms**: Evaluations checked for bias and fairness

## Best Practices

### Legislative Evaluation

1. **Use Specific Criteria**: Define clear, specific evaluation criteria
2. **Include Relevant Context**: Provide legislative history and precedent
3. **Enable Dynamic Thinking**: Allow CoRT to determine optimal thinking depth
4. **Store Thinking Traces**: Keep complete records for accountability
5. **Verify References**: Ensure all cited regulations are accurate and current
6. **Consider Multiple Stakeholders**: Evaluate impacts across stakeholder groups

### Policy Analysis

1. **Define the Problem Clearly**: Start with a precise problem statement
2. **Compare Diverse Alternatives**: Include fundamentally different approaches
3. **Use Consistent Criteria**: Apply the same criteria to all alternatives
4. **Consider Implementation Challenges**: Assess practical feasibility
5. **Evaluate Unintended Consequences**: Look beyond immediate impacts
6. **Include Long-Term Perspective**: Consider sustainability and adaptability

### Agency Collaboration

1. **Clarify Roles and Responsibilities**: Define each agency's specific role
2. **Establish Clear Communication**: Define communication protocols
3. **Create Shared Metrics**: Develop common success measures
4. **Address Resource Allocation**: Specify how resources will be shared
5. **Plan for Contingencies**: Include plans for unexpected scenarios
6. **Define Escalation Paths**: Create clear processes for issue resolution

## Advanced Configuration

### LLM Model Configuration

You can configure the LLM model used by the CoRT processor:

```python
from langchain_google_genai import ChatGoogleGenerativeAI

# Create a model with specific configuration
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # More powerful model for complex evaluations
    temperature=0.2,         # Lower temperature for more consistent results
    top_p=0.95,
    top_k=40,
    max_output_tokens=4096   # Longer output for detailed evaluations
)

def llm_generator(prompt):
    return model.invoke(prompt).content

# Create the deal evaluator with this generator
evaluator = LegislativeEvaluator(llm_generator=llm_generator)
```

### Custom Evaluation Criteria

You can create domain-specific criteria sets:

```python
# Constitutional criteria
constitutional_criteria = [
    {"name": "Due Process", "description": "Does the legislation adhere to due process requirements?"},
    {"name": "Equal Protection", "description": "Does the legislation provide equal protection under the law?"},
    {"name": "Federalism", "description": "Does the legislation respect the division of powers between federal and state governments?"},
    {"name": "First Amendment", "description": "Does the legislation comply with First Amendment protections?"},
    {"name": "Fourth Amendment", "description": "Does the legislation respect privacy and search/seizure protections?"}
]

# Administrative criteria
administrative_criteria = [
    {"name": "Implementation Feasibility", "description": "Can the provisions be reasonably implemented?"},
    {"name": "Resource Requirements", "description": "What resources are required for implementation?"},
    {"name": "Timeline Practicality", "description": "Are the timelines practical and achievable?"},
    {"name": "Coordination Requirements", "description": "What inter-agency coordination is required?"},
    {"name": "Enforcement Mechanisms", "description": "Are the enforcement mechanisms effective?"}
]

# Impact criteria
impact_criteria = [
    {"name": "Economic Impact", "description": "What are the economic impacts of the legislation?"},
    {"name": "Social Impact", "description": "What are the social impacts of the legislation?"},
    {"name": "Environmental Impact", "description": "What are the environmental impacts of the legislation?"},
    {"name": "Stakeholder Impact", "description": "How are different stakeholders affected?"},
    {"name": "Long-term Consequences", "description": "What are the long-term consequences of the legislation?"}
]
```

## Conclusion

The Deal Negotiation system with Chain of Recursive Thoughts provides powerful capabilities for legislative evaluation, policy analysis, and agency collaboration. By enabling structured multi-round thinking, CoRT helps government agents make better decisions in complex scenarios by considering more options, evaluating them systematically, and maintaining comprehensive reasoning traces.

These capabilities are particularly valuable in the government context, where decisions often involve multiple stakeholders, complex regulations, and significant consequences. The integration with HMS components, particularly HMS-CDF, further enhances these capabilities by providing specialized legislative processing and comprehensive compliance validation.

For implementation details, see the [Agent Architecture](agent_architecture.md), [Chain of Recursive Thoughts](cort_implementation.md), and [Government Agents](government_agents.md) documentation.