# Chain of Recursive Thoughts (CoRT) Integration Guide

## Overview

This guide provides comprehensive instructions for integrating the Chain of Recursive Thoughts (CoRT) reasoning framework across all HMS component agents. CoRT enables agents to perform advanced recursive reasoning, generating multiple alternative solutions, self-critiquing, and selecting optimal approaches through a structured thought process.

## CoRT Architecture

The CoRT integration is built on the existing implementation in HMS-A2A and extends it across all component agents:

```
┌────────────────────────────────────────────────────────────┐
│                      CoRT Framework                        │
├────────────────────────────────────────────────────────────┤
│ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐  │
│ │ Initial Thought │ │  Alternative   │ │   Evaluation   │  │
│ │    Generator   │ │   Generator    │ │     Engine     │  │
│ └────────────────┘ └────────────────┘ └────────────────┘  │
│                                                            │
│ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐  │
│ │    Reasoning   │ │   Checkpoint   │ │  Optimization  │  │
│ │     Tracer     │ │    Validator   │ │     Engine     │  │
│ └────────────────┘ └────────────────┘ └────────────────┘  │
└────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                   Agent CoRT Integration                   │
├───────────────┬───────────────┬───────────────┬────────────┤
│ HMS-Component │ HMS-Component │ HMS-Component │    ...     │
│  Agent CoRT   │  Agent CoRT   │  Agent CoRT   │            │
└───────────────┴───────────────┴───────────────┴────────────┘
```

## Integration Steps

### 1. Set Up CoRT Dependencies

Ensure each component agent has the necessary dependencies:

```python
# In your component's requirements.txt or pyproject.toml
cort_framework = ">=1.5.0"
recursive_thought = ">=2.2.1"
```

### 2. Create Component-Specific CoRT Implementation

Each component needs a specialized CoRT implementation that extends the base framework:

```python
# In [component]/agent/cort/component_cort.py

from hms_a2a.cort import BaseCoRTFramework

class ComponentCoRT(BaseCoRTFramework):
    """Component-specific implementation of Chain of Recursive Thoughts."""
    
    def __init__(self, 
                 component_name: str,
                 max_rounds: int = 3,
                 alternatives_per_round: int = 3,
                 dynamic_depth: bool = True):
        """Initialize component-specific CoRT framework.
        
        Args:
            component_name: Name of the component
            max_rounds: Maximum number of reasoning rounds
            alternatives_per_round: Number of alternatives to generate per round
            dynamic_depth: Whether to adjust depth based on complexity
        """
        super().__init__(
            name=f"{component_name}CoRT",
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_depth=dynamic_depth
        )
        
        self.component_name = component_name
        self.domain_knowledge = self._load_domain_knowledge()
    
    def _load_domain_knowledge(self):
        """Load component-specific domain knowledge for CoRT."""
        # Implementation depends on component's knowledge structure
        return {}
    
    def generate_initial_thought(self, problem: dict) -> dict:
        """Generate initial thought incorporating component expertise."""
        # Override to include component-specific initial approach
        base_thought = super().generate_initial_thought(problem)
        
        # Enhance with component domain knowledge
        domain_enhanced_thought = self._apply_domain_knowledge(
            base_thought, 
            self.domain_knowledge
        )
        
        return domain_enhanced_thought
    
    def _apply_domain_knowledge(self, thought: dict, domain_knowledge: dict) -> dict:
        """Apply domain knowledge to enhance a thought."""
        # Implementation depends on component's domain knowledge structure
        return thought
    
    def evaluate_alternatives(self, alternatives: list, problem: dict) -> dict:
        """Evaluate alternatives using component-specific criteria."""
        # Override to include component-specific evaluation criteria
        base_evaluations = super().evaluate_alternatives(alternatives, problem)
        
        # Add component-specific evaluation criteria
        for alt in base_evaluations:
            alt['component_specific_score'] = self._calculate_component_score(
                alt['thought'], 
                problem
            )
        
        return base_evaluations
    
    def _calculate_component_score(self, thought: dict, problem: dict) -> float:
        """Calculate component-specific score for a thought."""
        # Implementation depends on component's evaluation criteria
        return 0.0
    
    def reasoning_checkpoint(self, current_state: dict) -> bool:
        """Apply component-specific checkpoint validation."""
        # Override to add component-specific checkpoints
        base_valid = super().reasoning_checkpoint(current_state)
        
        # Add component-specific validation
        component_valid = self._validate_component_constraints(current_state)
        
        return base_valid and component_valid
    
    def _validate_component_constraints(self, state: dict) -> bool:
        """Validate component-specific constraints."""
        # Implementation depends on component's constraints
        return True
```

### 3. Configure CoRT Templates

Create reasoning templates specific to your component:

```yaml
# In [component]/agent/cort/templates/problem_decomposition.yaml
template_type: "problem_decomposition"
description: "Template for breaking down problems in [Component]"
steps:
  - "Identify the core [Component] elements involved"
  - "Break down the problem into [Component]-specific sub-problems"
  - "Determine dependencies on other components"
  - "Establish verification criteria for each sub-problem"
  - "Prioritize sub-problems based on [Component] constraints"
```

```yaml
# In [component]/agent/cort/templates/solution_evaluation.yaml
template_type: "solution_evaluation"
description: "Template for evaluating solutions in [Component]"
criteria:
  - name: "technical_feasibility"
    description: "How feasible is the solution within [Component]'s technical constraints?"
    weight: 0.25
  - name: "integration_impact"
    description: "How does the solution impact integration with other components?"
    weight: 0.20
  - name: "performance"
    description: "What is the performance impact on [Component]?"
    weight: 0.20
  - name: "compliance"
    description: "Does the solution comply with [Component]'s standards and regulations?"
    weight: 0.25
  - name: "complexity"
    description: "How complex is the implementation within [Component]?"
    weight: 0.10
```

### 4. Set Up CoRT Checkpoint Validators

Create validators to check reasoning at various checkpoints:

```python
# In [component]/agent/cort/checkpoints/validators.py

from hms_a2a.cort.validation import BaseValidator

class ComponentSpecificValidator(BaseValidator):
    """Validator for component-specific constraints and requirements."""
    
    def __init__(self, component_name: str):
        self.component_name = component_name
        self.standards = self._load_component_standards()
    
    def _load_component_standards(self):
        """Load component-specific standards and requirements."""
        # Implementation depends on component's standards
        return {}
    
    def validate_thought(self, thought: dict) -> dict:
        """Validate a thought against component-specific criteria."""
        result = {
            "valid": True,
            "issues": [],
            "warnings": []
        }
        
        # Check compliance with component standards
        compliance_issues = self._check_compliance(thought)
        if compliance_issues:
            result["valid"] = False
            result["issues"].extend(compliance_issues)
        
        # Check for technical feasibility
        feasibility_issues = self._check_feasibility(thought)
        if feasibility_issues:
            result["valid"] = False
            result["issues"].extend(feasibility_issues)
        
        # Check for potential warnings
        warnings = self._check_for_warnings(thought)
        if warnings:
            result["warnings"].extend(warnings)
        
        return result
    
    def _check_compliance(self, thought: dict) -> list:
        """Check compliance with component standards."""
        # Implementation depends on component's compliance requirements
        return []
    
    def _check_feasibility(self, thought: dict) -> list:
        """Check technical feasibility within component."""
        # Implementation depends on component's technical constraints
        return []
    
    def _check_for_warnings(self, thought: dict) -> list:
        """Check for potential warnings or issues."""
        # Implementation depends on component's warning criteria
        return []
```

### 5. Integrate CoRT with Component Agent

Update the component agent to use CoRT for complex reasoning:

```python
# In [component]/agent/agent.py

from [component].agent.cort.component_cort import ComponentCoRT
from [component].agent.cort.checkpoints.validators import ComponentSpecificValidator

class ComponentAgent:
    """Agent for [Component] with CoRT integration."""
    
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        
        # Initialize CoRT framework
        self.cort = ComponentCoRT(
            component_name=name,
            max_rounds=config.get("cort_max_rounds", 3),
            alternatives_per_round=config.get("cort_alternatives", 3),
            dynamic_depth=config.get("cort_dynamic_depth", True)
        )
        
        # Initialize CoRT validator
        self.validator = ComponentSpecificValidator(name)
        
        # Register validator with CoRT
        self.cort.register_validator(self.validator)
    
    def process_complex_task(self, task: dict) -> dict:
        """Process a complex task using CoRT reasoning."""
        # Determine if CoRT is needed based on task complexity
        if self._requires_cort(task):
            # Use CoRT for complex reasoning
            result = self.cort.solve_problem(task)
            return self._format_cort_result(result)
        else:
            # Use standard processing for simple tasks
            return self._process_simple_task(task)
    
    def _requires_cort(self, task: dict) -> bool:
        """Determine if a task requires CoRT reasoning."""
        # Implement logic to determine task complexity
        complexity_factors = [
            len(task.get("dependencies", [])) > 2,  # Multiple dependencies
            task.get("impact_level", "low") in ["medium", "high"],  # Medium/high impact
            task.get("certainty", 1.0) < 0.8,  # Low certainty
            task.get("explicit_cort_request", False)  # Explicit request
        ]
        
        # If any complexity factors are true, use CoRT
        return any(complexity_factors)
    
    def _process_simple_task(self, task: dict) -> dict:
        """Process a simple task without CoRT."""
        # Standard task processing logic
        return {}
    
    def _format_cort_result(self, result: dict) -> dict:
        """Format CoRT result for the agent's response."""
        return {
            "solution": result["best_solution"],
            "confidence": result["confidence"],
            "alternatives_considered": len(result["alternatives"]),
            "reasoning_trace": result["reasoning_trace"] if self.config.get("include_trace", False) else None,
            "component_specific_details": self._extract_component_details(result)
        }
    
    def _extract_component_details(self, result: dict) -> dict:
        """Extract component-specific details from CoRT result."""
        # Implementation depends on component's result structure
        return {}
```

### 6. Setting Up Collaborative CoRT Sessions

Enable agents to participate in multi-agent CoRT reasoning:

```python
# In [component]/agent/interfaces/collaboration.py

from hms_a2a.collaboration import CollaborationSession

class ComponentCollaborator:
    """Handles collaborative CoRT sessions for the component."""
    
    def __init__(self, agent):
        self.agent = agent
        self.active_sessions = {}
    
    async def join_cort_session(self, session_id: str, topic: str, context: dict) -> dict:
        """Join a collaborative CoRT session."""
        # Create a session handler
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = {
                "topic": topic,
                "context": context,
                "contributions": [],
                "status": "joined"
            }
        
        return {
            "status": "joined",
            "agent_id": self.agent.name,
            "capabilities": self.agent.cort.get_capabilities()
        }
    
    async def contribute_thought(self, session_id: str, round_id: str, context: dict) -> dict:
        """Contribute a thought to a collaborative CoRT session."""
        if session_id not in self.active_sessions:
            return {"error": "Not a member of this session"}
        
        # Generate component-specific thought
        thought = self.agent.cort.generate_thought_for_context(
            context=context,
            session_data=self.active_sessions[session_id]
        )
        
        # Record the contribution
        self.active_sessions[session_id]["contributions"].append({
            "round_id": round_id,
            "thought": thought,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "agent_id": self.agent.name,
            "round_id": round_id,
            "thought": thought
        }
    
    async def evaluate_thoughts(self, session_id: str, round_id: str, thoughts: list) -> dict:
        """Evaluate thoughts from all participants in a collaborative CoRT session."""
        if session_id not in self.active_sessions:
            return {"error": "Not a member of this session"}
        
        # Evaluate thoughts using component expertise
        evaluations = self.agent.cort.evaluate_collaborative_thoughts(
            thoughts=thoughts,
            context=self.active_sessions[session_id]["context"]
        )
        
        return {
            "agent_id": self.agent.name,
            "round_id": round_id,
            "evaluations": evaluations
        }
    
    async def end_session(self, session_id: str) -> dict:
        """End participation in a collaborative CoRT session."""
        if session_id in self.active_sessions:
            session_data = self.active_sessions[session_id]
            del self.active_sessions[session_id]
            return {
                "status": "ended",
                "session_id": session_id,
                "contributions": len(session_data["contributions"])
            }
        
        return {"error": "Not a member of this session"}
```

## Customizing CoRT for Component Domains

### Domain-Specific Reasoning Templates

Create reasoning templates tailored to your component's domain:

1. **HMS-DEV Templates**:
   - Tool development reasoning
   - Development workflow optimization
   - Code quality assessment

2. **HMS-DOC Templates**:
   - Documentation structure reasoning
   - Content clarity assessment
   - Cross-reference validation

3. **HMS-API Templates**:
   - API design reasoning
   - Endpoint security assessment
   - Performance optimization

4. **HMS-CDF Templates**:
   - Policy compliance reasoning
   - Legislative impact assessment
   - Stakeholder consideration

### Component-Specific Evaluation Criteria

Customize evaluation criteria based on component priorities:

1. **HMS-DEV Criteria**:
   - Development efficiency
   - Tool usability
   - Integration with other tools

2. **HMS-DOC Criteria**:
   - Documentation completeness
   - Clarity and readability
   - Cross-component consistency

3. **HMS-API Criteria**:
   - API performance
   - Security considerations
   - Standard compliance
   - Client compatibility

4. **HMS-CDF Criteria**:
   - Policy compliance
   - Democratic principles
   - Legislative validity
   - Stakeholder impact

## CoRT Configuration Parameters

Configure CoRT behavior using these parameters:

| Parameter | Description | Default | Recommended Range |
|-----------|-------------|---------|------------------|
| `max_rounds` | Maximum reasoning rounds | 3 | 2-5 |
| `alternatives_per_round` | Alternatives to generate per round | 3 | 2-5 |
| `dynamic_depth` | Adjust depth based on complexity | True | True/False |
| `minimum_confidence` | Minimum confidence for solution acceptance | 0.7 | 0.6-0.9 |
| `trace_verbosity` | Detail level in reasoning trace | "medium" | "low", "medium", "high" |
| `optimization_level` | Level of reasoning optimization | "standard" | "minimal", "standard", "aggressive" |
| `timeout_seconds` | Maximum time for reasoning | 60 | 30-300 |

## Advanced CoRT Features

### 1. Dynamic Thinking Depth

Automatically adjust reasoning depth based on problem complexity:

```python
# Example configuration for dynamic thinking depth
dynamic_config = {
    "base_rounds": 2,
    "complexity_factors": [
        {"factor": "dependencies", "threshold": 3, "additional_rounds": 1},
        {"factor": "impact", "threshold": "high", "additional_rounds": 1},
        {"factor": "uncertainty", "threshold": 0.3, "additional_rounds": 1}
    ],
    "max_additional_rounds": 3
}
```

### 2. Multi-Agent Consensus Building

Enable collaborative decision-making across component agents:

```python
# Example of consensus building configuration
consensus_config = {
    "threshold": 0.75,  # Required agreement level (0.0-1.0)
    "max_discussion_rounds": 5,
    "voting_method": "weighted",  # "simple", "weighted", or "domain_expertise"
    "conflict_resolution": "supervisor_decides"  # How to handle deadlocks
}
```

### 3. Reasoning Trace Visualization

Generate visual representations of recursive reasoning processes:

```python
# Example of reasoning trace visualization
visualization_config = {
    "format": "graph",  # "graph", "tree", or "timeline"
    "include_alternatives": True,
    "highlight_decision_points": True,
    "show_evaluation_scores": True,
    "max_depth": 3
}
```

## Testing CoRT Integration

### Unit Testing

Create unit tests for your component's CoRT implementation:

```python
# In [component]/agent/tests/test_cort.py
import unittest
from [component].agent.cort.component_cort import ComponentCoRT

class TestComponentCoRT(unittest.TestCase):
    """Tests for component-specific CoRT implementation."""
    
    def setUp(self):
        self.cort = ComponentCoRT(
            component_name="TestComponent",
            max_rounds=2,
            alternatives_per_round=2
        )
    
    def test_initial_thought_generation(self):
        problem = {"description": "Test problem", "context": {}}
        thought = self.cort.generate_initial_thought(problem)
        
        self.assertIsNotNone(thought)
        self.assertIn("reasoning", thought)
        self.assertIn("approach", thought)
    
    def test_alternative_generation(self):
        problem = {"description": "Test problem", "context": {}}
        initial_thought = self.cort.generate_initial_thought(problem)
        alternatives = self.cort.generate_alternatives(initial_thought, problem)
        
        self.assertEqual(len(alternatives), 2)
        self.assertNotEqual(alternatives[0], alternatives[1])
    
    def test_evaluation(self):
        problem = {"description": "Test problem", "context": {}}
        initial_thought = self.cort.generate_initial_thought(problem)
        alternatives = self.cort.generate_alternatives(initial_thought, problem)
        evaluations = self.cort.evaluate_alternatives(alternatives, problem)
        
        self.assertEqual(len(evaluations), 2)
        self.assertIn("score", evaluations[0])
        self.assertIn("component_specific_score", evaluations[0])
    
    def test_full_reasoning_cycle(self):
        problem = {"description": "Test problem", "context": {}}
        result = self.cort.solve_problem(problem)
        
        self.assertIn("best_solution", result)
        self.assertIn("confidence", result)
        self.assertIn("reasoning_trace", result)
        self.assertEqual(len(result["reasoning_rounds"]), 2)
```

### Integration Testing

Test collaborative CoRT scenarios:

```python
# In [component]/agent/tests/test_collaboration.py
import unittest
from unittest.mock import MagicMock
from [component].agent.interfaces.collaboration import ComponentCollaborator

class TestCollaborativeCoRT(unittest.TestCase):
    """Tests for collaborative CoRT sessions."""
    
    def setUp(self):
        self.agent = MagicMock()
        self.agent.name = "TestComponent"
        self.agent.cort.get_capabilities.return_value = ["capability1", "capability2"]
        self.agent.cort.generate_thought_for_context.return_value = {
            "reasoning": "Test reasoning",
            "approach": "Test approach"
        }
        self.agent.cort.evaluate_collaborative_thoughts.return_value = [
            {"thought_id": "thought1", "score": 0.8},
            {"thought_id": "thought2", "score": 0.6}
        ]
        
        self.collaborator = ComponentCollaborator(self.agent)
    
    async def test_join_session(self):
        result = await self.collaborator.join_cort_session(
            session_id="test-session",
            topic="Test Topic",
            context={"key": "value"}
        )
        
        self.assertEqual(result["status"], "joined")
        self.assertEqual(result["agent_id"], "TestComponent")
        self.assertEqual(result["capabilities"], ["capability1", "capability2"])
    
    async def test_contribute_thought(self):
        await self.collaborator.join_cort_session(
            session_id="test-session",
            topic="Test Topic",
            context={"key": "value"}
        )
        
        result = await self.collaborator.contribute_thought(
            session_id="test-session",
            round_id="round1",
            context={"key": "value"}
        )
        
        self.assertEqual(result["agent_id"], "TestComponent")
        self.assertEqual(result["round_id"], "round1")
        self.assertEqual(
            result["thought"], 
            {"reasoning": "Test reasoning", "approach": "Test approach"}
        )
    
    async def test_evaluate_thoughts(self):
        await self.collaborator.join_cort_session(
            session_id="test-session",
            topic="Test Topic",
            context={"key": "value"}
        )
        
        thoughts = [
            {"id": "thought1", "content": "Thought 1"},
            {"id": "thought2", "content": "Thought 2"}
        ]
        
        result = await self.collaborator.evaluate_thoughts(
            session_id="test-session",
            round_id="round1",
            thoughts=thoughts
        )
        
        self.assertEqual(result["agent_id"], "TestComponent")
        self.assertEqual(result["round_id"], "round1")
        self.assertEqual(
            result["evaluations"], 
            [
                {"thought_id": "thought1", "score": 0.8},
                {"thought_id": "thought2", "score": 0.6}
            ]
        )
```

## Performance Considerations

When implementing CoRT across components, consider these performance factors:

1. **Resource Usage**:
   - CoRT reasoning can be computationally intensive
   - Limit maximum recursion depth for complex problems
   - Consider implementing resource throttling for concurrent sessions

2. **Response Time**:
   - Deep reasoning increases response times
   - Use dynamic depth to adjust based on problem complexity
   - Set appropriate timeouts to prevent excessive processing

3. **Memory Management**:
   - Reasoning traces can become large
   - Implement trace pruning for long reasoning chains
   - Consider serialization for persistent reasoning sessions

4. **Optimization Techniques**:
   - Cache intermediate reasoning results
   - Implement early stopping for clear solutions
   - Use parallel processing for alternative generation and evaluation

## Best Practices

### 1. CoRT Implementation Guidelines

- Start with simple reasoning templates and gradually increase complexity
- Focus on domain-specific evaluation criteria that leverage component expertise
- Implement comprehensive validation to ensure reasoning quality
- Use dynamic depth adjustment to optimize resource usage

### 2. Collaborative CoRT Guidelines

- Define clear protocols for multi-agent CoRT sessions
- Establish weighting for different component perspectives
- Implement robust conflict resolution mechanisms
- Create structured consensus-building processes

### 3. Performance Optimization Guidelines

- Monitor reasoning time and resource usage
- Implement appropriate timeouts for each reasoning stage
- Cache reasoning results when appropriate
- Use asynchronous processing for non-blocking operations

## Troubleshooting

### Common Issues and Solutions

1. **Infinite Recursion**:
   - **Symptom**: CoRT process never completes
   - **Solution**: Ensure maximum recursion depth is properly set
   
2. **Poor Quality Results**:
   - **Symptom**: Low-quality or inconsistent solutions
   - **Solution**: Refine evaluation criteria and validation checks
   
3. **High Resource Usage**:
   - **Symptom**: Excessive CPU or memory consumption
   - **Solution**: Implement resource limits and optimize reasoning process
   
4. **Collaboration Deadlocks**:
   - **Symptom**: Multi-agent sessions fail to reach consensus
   - **Solution**: Implement timeouts and fallback decision mechanisms

## Conclusion

This CoRT Integration Guide provides a comprehensive framework for implementing advanced reasoning capabilities across all HMS component agents. By following these guidelines, each component can leverage the power of recursive thought while maintaining its domain-specific expertise.

The CoRT integration enables:

1. **Enhanced Decision Quality**: Through recursive self-improvement
2. **Transparent Reasoning**: With detailed reasoning traces
3. **Multi-Agent Collaboration**: Via structured collaborative sessions
4. **Domain-Specific Optimization**: Through component-tailored reasoning

Each component's unique domain knowledge is preserved and enhanced through the CoRT framework, creating a powerful ecosystem of intelligent agents capable of tackling complex problems through recursive, self-improving thought processes.