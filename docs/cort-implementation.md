# Chain of Recursive Thoughts (CoRT) Implementation

This document provides an overview of the Chain of Recursive Thoughts (CoRT) implementation in the Codex-GOV system, which enhances the reasoning capabilities of government agents.

## Overview

Chain of Recursive Thoughts (CoRT) is a technique that enhances AI decision-making by enabling agents to:

1. Generate multiple alternatives for each decision point
2. Critically evaluate each alternative against specific criteria
3. Select the best option through recursive self-critique
4. Maintain a transparent thinking trace for all decisions

This approach helps government agents make better decisions in complex scenarios by considering more options and engaging in structured multi-round thinking.

## Core Components

### CoRTProcessor

The `CoRTProcessor` class implements the core recursive thinking pattern:

- **Alternative Generation**: Creates multiple approaches to solve a problem
- **Alternative Evaluation**: Critically assesses each alternative against criteria
- **Alternative Selection**: Chooses the best alternative through recursive improvement
- **Dynamic Thinking Depth**: Automatically determines the optimal number of thinking rounds based on problem complexity

```python
class CoRTProcessor:
    """Processor for Chain of Recursive Thoughts."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        max_rounds: int = 3,
        generate_alternatives: int = 3,
        dynamic_rounds: bool = True,
        detailed_logging: bool = False
    ):
        """Initialize the CoRT processor.
        
        Args:
            llm_generator: Function that generates responses from prompts
            max_rounds: Maximum number of thinking rounds
            generate_alternatives: Number of alternatives to generate per round
            dynamic_rounds: Whether to dynamically determine optimal rounds
            detailed_logging: Whether to enable detailed logging
        """
        # Initialize the processor
        
    def process(
        self,
        query: str,
        initial_response: Optional[str] = None,
        task_context: Optional[Dict[str, Any]] = None,
        prompt_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a query with recursive thinking.
        
        Args:
            query: The query to process
            initial_response: Optional starting point
            task_context: Optional context for the task
            prompt_instructions: Optional domain-specific instructions
            
        Returns:
            Dictionary with the processing results
        """
        # Process with recursive thinking
        
    def process_with_tools(
        self,
        query: str,
        tools: List[Dict[str, Any]],
        tool_executor: Callable[[str, Dict[str, Any]], str],
        initial_response: Optional[str] = None,
        task_context: Optional[Dict[str, Any]] = None,
        prompt_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a query with recursive thinking and tools.
        
        Args:
            query: The query to process
            tools: List of available tools
            tool_executor: Function to execute tool calls
            initial_response: Optional starting point
            task_context: Optional context for the task
            prompt_instructions: Optional domain-specific instructions
            
        Returns:
            Dictionary with the processing results including tool usage
        """
        # Process with recursive thinking and tools
```

### CoRTAgentMixin

The `CoRTAgentMixin` class provides CoRT capabilities to any agent:

```python
class CoRTAgentMixin:
    """Mixin that adds Chain of Recursive Thoughts capabilities to agents."""
    
    def __init__(
        self,
        cort_max_rounds: int = 3,
        cort_alternatives: int = 3,
        **kwargs
    ):
        """Initialize the CoRT mixin.
        
        Args:
            cort_max_rounds: Maximum number of thinking rounds
            cort_alternatives: Number of alternatives to generate per round
        """
        self.cort_max_rounds = cort_max_rounds
        self.cort_alternatives = cort_alternatives
        self.cort_processor = None
        super().__init__(**kwargs)
        
    def init_cort_processor(self, model=None):
        """Initialize the CoRT processor with the appropriate LLM."""
        # Initialize the processor
        
    def process_with_cort(
        self,
        task: TaskRequest,
        query_transformer: Optional[Callable[[str], str]] = None,
        enable_cort: bool = True
    ) -> Dict[str, Any]:
        """Process a task with Chain of Recursive Thoughts.
        
        Args:
            task: The task request to process
            query_transformer: Optional function to transform the query
            enable_cort: Whether to enable CoRT
            
        Returns:
            Dictionary with the processing results
        """
        # Process with recursive thinking
        
    def process_with_cort_and_tools(
        self,
        task: TaskRequest,
        tools: List[Any],
        tool_executor: Callable[[str, Any], str],
        enable_cort: bool = True
    ) -> Dict[str, Any]:
        """Process a task with Chain of Recursive Thoughts and tools.
        
        Args:
            task: The task request to process
            tools: List of available tools
            tool_executor: Function to execute tool calls
            enable_cort: Whether to enable CoRT
            
        Returns:
            Dictionary with the processing results including tool usage
        """
        # Process with recursive thinking and tools
        
    def cort_enhanced_task_response(
        self,
        task: TaskRequest,
        cort_result: Dict[str, Any]
    ) -> TaskResponse:
        """Create a task response enhanced with CoRT results.
        
        Args:
            task: The original task request
            cort_result: The CoRT processing result
            
        Returns:
            Enhanced task response
        """
        # Create an enhanced response with thinking trace
```

### CoRTDealEvaluator

The `CoRTDealEvaluator` class provides specialized CoRT capabilities for deal negotiation:

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
        """Initialize the CoRT deal evaluator."""
        # Initialize the evaluator
        
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
            Dictionary with the evaluation results
        """
        # Evaluate with recursive thinking
        
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
        # Compare with recursive thinking
        
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
        # Negotiate with recursive thinking
```

## Government Agent Integration

### CoRTGovernmentAgent

The `CoRTGovernmentAgent` class integrates the `CoRTAgentMixin` with the `GovernmentAgent`:

```python
class CoRTGovernmentAgent(CoRTAgentMixin, GovernmentAgent):
    """Government agent with Chain of Recursive Thoughts capabilities."""
    
    def __init__(
        self,
        agency_label: str,
        agency_name: str,
        domain: str,
        supported_standards: List[str],
        model_name: str = "gemini-2.0-flash",
        port: int = None,
        cort_max_rounds: int = 3,
        cort_alternatives: int = 3,
        cort_enabled_by_default: bool = True
    ):
        """Initialize a CoRT-enhanced government agent."""
        # Initialize with CoRT capabilities
        
    def process_task(self, task: TaskRequest) -> TaskResponse:
        """Process a task with recursive thinking capabilities."""
        # Enhanced processing with CoRT
```

## Usage Examples

### Basic Usage

```python
from common.utils.recursive_thought import get_recursive_thought_processor
from langchain_google_genai import ChatGoogleGenerativeAI

# Create a model and LLM generator function
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
def llm_generator(prompt):
    return model.invoke(prompt).content

# Create the CoRT processor
processor = get_recursive_thought_processor(
    llm_fn=llm_generator,
    max_rounds=3,
    generate_alternatives=3,
    dynamic_rounds=True
)

# Process a query
result = processor.process(
    query="What are the potential impacts of climate change on agricultural production?",
    initial_response=None,  # Optional starting point
    task_context={"domain": "environmental_science"},  # Optional context
    prompt_instructions="Focus on evidence-based findings and scientific consensus"  # Domain-specific guidance
)

# Access the results
print(f"Processing completed after {result['rounds_completed']} rounds of thinking")
print("\nFinal response:")
print(result["final_response"])

# Access the thinking trace if needed
thinking_trace = result["thinking_trace"]
for round_data in thinking_trace:
    print(f"Round {round_data.get('round', 0)}: {len(round_data.get('alternatives', []))} alternatives considered")
```

### Using CoRT with Government Agents

```python
from gov_agents import AgentFactory

# Create a CoRT-enhanced government agent
fbi_agent = AgentFactory.create_government_agent(
    "FBI",
    cort_max_rounds=4,
    cort_alternatives=3,
    cort_enabled_by_default=True
)

# Process a task with recursive thinking
task_request = TaskRequest(
    id="task-123",
    query="Analyze the potential cybersecurity implications of this new policy",
    metadata={"use_cort": True}  # Explicitly enable CoRT
)

# Process the task
response = fbi_agent.process_task(task_request)

# Access the thinking trace from the response artifacts
thinking_trace = None
for artifact in response.artifacts or []:
    if artifact.get("type") == "thinking_trace":
        thinking_trace = artifact.get("content")
        break

if thinking_trace:
    print(f"Completed {len(thinking_trace)} rounds of thinking")
    for round_data in thinking_trace:
        print(f"Round {round_data.get('round')}: {len(round_data.get('alternatives', []))} alternatives")
```

### Deal Evaluation with CoRT

```python
from specialized_agents.collaboration.cort_deal_negotiator import CoRTDealEvaluator
from specialized_agents.collaboration.deals import Deal

# Create the CoRT Deal Evaluator
evaluator = CoRTDealEvaluator(
    llm_generator=llm_generator,
    max_rounds=3,
    generate_alternatives=3,
    dynamic_rounds=True
)

# Create a deal object
deal = Deal(
    name="Federal Data Sharing Agreement",
    description="An agreement between two agencies for sharing citizen data",
    participants=["Department of Treasury", "Social Security Administration"]
)

# Define evaluation criteria
criteria = [
    {"name": "Privacy Protection", "description": "Does the agreement protect citizen privacy?"},
    {"name": "Security Measures", "description": "Are adequate security measures in place?"},
    {"name": "Regulatory Compliance", "description": "Does the agreement comply with all relevant regulations?"}
]

# Evaluate the deal with recursive thinking
result = evaluator.evaluate_deal(
    deal=deal,
    evaluator_role="Federal Privacy Officer",
    evaluation_criteria=criteria,
    prompt_instructions="Focus on FISMA compliance and PII protection"
)

# Access the results
print(f"Deal evaluation completed after {result['rounds_completed']} rounds of thinking")
print(f"Approval status: {result['approval_status']}")
print("\nFinal evaluation:")
print(result["evaluation"])
```

## Key Features

### 1. Robust JSON Parsing

The processor handles various LLM response formats:

- Attempts to parse structured JSON responses first
- Falls back to text extraction with regex patterns if JSON parsing fails
- Uses multiple extraction methods to handle different response formats

### 2. Dynamic Thinking Rounds

CoRT can automatically determine the optimal number of thinking rounds:

```python
processor = CoRTProcessor(
    llm_generator=llm_fn,
    max_rounds=5,       # Upper limit on rounds
    dynamic_rounds=True # Enable dynamic round determination
)
```

### 3. Error Handling and Fallbacks

The implementation includes comprehensive error handling:

- Graceful recovery from LLM generation failures
- Alternative extraction fallbacks when structured parsing fails
- Default to previous best response when evaluation fails

### 4. Tool Integration

CoRT can be integrated with external tools through the `process_with_tools` method:

```python
result = processor.process_with_tools(
    query="What is the GDP of France in 2023?",
    tools=[calculator_tool, search_tool],
    tool_executor=execute_tool
)
```

## Performance Considerations

- **Token Usage**: CoRT increases token usage due to multiple thinking rounds
- **Latency**: Expect increased processing time, especially with many thinking rounds
- **Memory Usage**: Thinking traces can be large for complex scenarios

To optimize performance:

```python
# For simpler scenarios, use fewer rounds
simple_processor = CoRTProcessor(
    llm_generator=llm_generator,
    max_rounds=2,
    generate_alternatives=2,
    dynamic_rounds=False  # Use fixed rounds for predictable performance
)

# For critical decisions, use more rounds
critical_processor = CoRTProcessor(
    llm_generator=llm_generator,
    max_rounds=4,
    generate_alternatives=3,
    dynamic_rounds=True  # Adapt to complexity
)
```

## Best Practices

1. **Start with Dynamic Rounds**: Let the system determine optimal thinking depth initially
2. **Store Thinking Traces**: Retain reasoning for auditability and analysis
3. **Match Rounds to Complexity**: Use more rounds for critical decisions, fewer for simple ones
4. **Provide Rich Context**: Include relevant information in the task context
5. **Use Domain-Specific Instructions**: Customize instructions for government scenarios

## Government-Specific Enhancements

For government scenarios, CoRT has been enhanced with:

1. **Compliance Verification**: Each thinking round includes automatic compliance checks
2. **Security Assessment**: Critical decisions include security implications in evaluation
3. **Multi-Stakeholder Perspective**: Considers impacts across different government entities
4. **Regulatory Framework Awareness**: Evaluates alternatives against applicable regulations
5. **Documentation Requirements**: Produces comprehensive documentation for audit purposes

## Logging and Auditing

CoRT includes comprehensive logging for government accountability:

- **Decision Traces**: Complete record of all alternatives considered
- **Evaluation Criteria**: Documentation of how each alternative was assessed
- **Selection Rationale**: Clear explanation of why the final option was chosen
- **Time Stamps**: Record of when each thinking stage occurred
- **Compliance Checks**: Documentation of all compliance validations performed

## Conclusion

Chain of Recursive Thoughts (CoRT) significantly enhances the reasoning capabilities of government agents in the Codex-GOV system. By enabling structured multi-round thinking with alternative generation and evaluation, CoRT helps agencies make better decisions while maintaining transparency, compliance, and accountability throughout the decision-making process.

For more details on specific use cases, see the [Government Agents](government_agents.md) and [Deal Negotiation](deal_negotiation.md) documentation.