# HMS Chain of Recursive Thoughts (CoRT) Implementation

## Overview

This document outlines the design and implementation of the Chain of Recursive Thoughts (CoRT) framework for the HMS agent system. CoRT provides agents with enhanced reasoning capabilities through a structured, multi-round thinking process that generates, evaluates, and refines multiple solution approaches before selecting the optimal outcome.

CoRT represents a significant advancement over traditional agent reasoning methods, enabling more thorough exploration of possible solutions, explicit consideration of alternatives, and transparent reasoning traces. This implementation builds on the core principles described in the [Chain-of-Recursive-Thoughts](https://github.com/PhialsBasement/Chain-of-Recursive-Thoughts) repository while extending and adapting the framework for the specific needs of the HMS ecosystem.

## Core Principles

The HMS CoRT implementation follows these core principles:

1. **Recursive Self-Improvement**: Agents refine their thinking through multiple rounds
2. **Alternative Generation**: Explicit generation of multiple solution approaches
3. **Structured Evaluation**: Systematic assessment of alternatives against criteria
4. **Transparent Reasoning**: Complete trace of the reasoning process
5. **Verification Integration**: Reasoning steps are verified throughout the process
6. **Domain Adaptation**: Framework tailored for specific domain requirements

## CoRT Architecture

The CoRT framework follows a layered architecture with progressive specialization:

```
┌─────────────────────────────────────────────────────────────┐
│                   Base CoRT Framework                       │
│                                                             │
│  - Core reasoning process                                   │
│  - Alternative generation                                   │
│  - Alternative evaluation                                   │
│  - Alternative selection                                    │
│  - Reasoning trace management                               │
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                    Domain CoRT Adapters                     │
│                                                             │
│  - Domain-specific reasoning templates                      │
│  - Domain-specific evaluation criteria                      │
│  - Domain-specific knowledge integration                    │
│  - Domain-specific verification                             │
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                  Component CoRT Extensions                  │
│                                                             │
│  - Component-specific reasoning                             │
│  - Component-specific evaluation                            │
│  - Component-specific tooling                               │
│  - Component-specific adaptation                            │
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                 Task-Specific CoRT Instances                │
│                                                             │
│  - Task-specific configuration                              │
│  - Task-specific processing                                 │
│  - Task-specific knowledge                                  │
│  - Task-specific optimization                               │
└─────────────────────────────────────────────────────────────┘
```

## Base CoRT Implementation

The base CoRT framework provides the core reasoning process:

```python
class CoRTProcessor:
    """Base Chain of Recursive Thoughts processor."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        max_rounds: int = 3,
        alternatives_per_round: int = 3,
        dynamic_rounds: bool = True,
        trace_manager: Optional['CoRTTraceManager'] = None,
        evaluation_criteria: Optional[List[Dict[str, str]]] = None
    ):
        """Initialize the CoRT processor.
        
        Args:
            llm_generator: Function to generate LLM responses
            max_rounds: Maximum reasoning rounds
            alternatives_per_round: Number of alternatives per round
            dynamic_rounds: Whether to dynamically adjust rounds
            trace_manager: Optional trace manager
            evaluation_criteria: Optional default evaluation criteria
        """
        self.llm_generator = llm_generator
        self.max_rounds = max_rounds
        self.alternatives_per_round = alternatives_per_round
        self.dynamic_rounds = dynamic_rounds
        self.trace_manager = trace_manager or CoRTTraceManager()
        self.evaluation_criteria = evaluation_criteria or self._default_evaluation_criteria()
        
    def solve(
        self,
        problem: Dict[str, Any],
        initial_prompt: Optional[str] = None,
        evaluation_criteria: Optional[List[Dict[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Solve a problem using recursive thinking.
        
        Args:
            problem: Problem to solve
            initial_prompt: Optional prompt to start reasoning
            evaluation_criteria: Optional criteria for this specific problem
            context: Optional additional context
            
        Returns:
            Solution with reasoning trace
        """
        # Initialize trace
        trace_id = self.trace_manager.create_trace(problem)
        
        # Get evaluation criteria for this problem
        criteria = evaluation_criteria or self.evaluation_criteria
        
        # Create problem context
        problem_context = self._create_problem_context(problem, context)
        
        # Generate initial prompt if not provided
        if not initial_prompt:
            initial_prompt = self._generate_initial_prompt(problem_context, criteria)
            
        # Record initial prompt
        self.trace_manager.add_prompt(trace_id, initial_prompt)
        
        # Begin recursive thinking
        current_round = 1
        best_thought = None
        
        while current_round <= self.max_rounds:
            # Record round start
            round_id = self.trace_manager.start_round(trace_id, current_round)
            
            # Generate alternatives
            alternatives = self._generate_alternatives(
                problem_context,
                best_thought,
                criteria,
                current_round
            )
            
            # Record alternatives
            for i, alternative in enumerate(alternatives):
                self.trace_manager.add_alternative(
                    trace_id,
                    round_id,
                    f"alternative_{i+1}",
                    alternative
                )
            
            # Evaluate alternatives
            evaluations = self._evaluate_alternatives(
                problem_context,
                alternatives,
                criteria,
                current_round
            )
            
            # Record evaluations
            for i, evaluation in enumerate(evaluations):
                self.trace_manager.add_evaluation(
                    trace_id,
                    round_id,
                    f"alternative_{i+1}",
                    evaluation
                )
            
            # Select best alternative
            best_index, best_thought = self._select_best_alternative(
                alternatives,
                evaluations,
                criteria
            )
            
            # Record selection
            self.trace_manager.add_selection(
                trace_id,
                round_id,
                f"alternative_{best_index + 1}",
                best_thought
            )
            
            # Check if we should continue
            if self.dynamic_rounds and self._should_terminate_early(
                problem_context,
                best_thought,
                current_round,
                criteria
            ):
                # Record early termination
                self.trace_manager.add_event(
                    trace_id,
                    "early_termination",
                    {
                        "round": current_round,
                        "reason": "Sufficient confidence reached"
                    }
                )
                break
                
            # Update round
            current_round += 1
            
        # Generate final solution
        solution = self._generate_solution(
            problem_context,
            best_thought,
            criteria
        )
        
        # Record solution
        self.trace_manager.add_solution(trace_id, solution)
        
        # Get complete trace
        trace = self.trace_manager.get_trace(trace_id)
        
        # Return solution with trace
        return {
            "solution": solution,
            "trace_id": trace_id,
            "trace": trace,
            "rounds_completed": current_round,
            "max_rounds": self.max_rounds,
            "confidence": solution.get("confidence", 0.0)
        }
        
    def _default_evaluation_criteria(self) -> List[Dict[str, str]]:
        """Default evaluation criteria.
        
        Returns:
            List of default criteria
        """
        return [
            {
                "name": "correctness",
                "description": "The accuracy and correctness of the solution"
            },
            {
                "name": "completeness",
                "description": "How thoroughly the solution addresses all aspects of the problem"
            },
            {
                "name": "efficiency",
                "description": "How efficiently the solution uses resources"
            },
            {
                "name": "practicality",
                "description": "How practical the solution is to implement"
            }
        ]
        
    def _create_problem_context(
        self,
        problem: Dict[str, Any],
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create problem context for reasoning.
        
        Args:
            problem: Problem to solve
            additional_context: Additional context
            
        Returns:
            Complete problem context
        """
        context = {
            "problem": problem,
            "timestamp": datetime.now().isoformat(),
            "cort_config": {
                "max_rounds": self.max_rounds,
                "alternatives_per_round": self.alternatives_per_round,
                "dynamic_rounds": self.dynamic_rounds
            }
        }
        
        if additional_context:
            context.update(additional_context)
            
        return context
        
    def _generate_initial_prompt(
        self,
        problem_context: Dict[str, Any],
        criteria: List[Dict[str, str]]
    ) -> str:
        """Generate initial prompt for reasoning.
        
        Args:
            problem_context: Problem context
            criteria: Evaluation criteria
            
        Returns:
            Initial prompt
        """
        problem = problem_context["problem"]
        
        prompt = f"""
        # Problem Analysis

        I need to solve the following problem:
        
        {json.dumps(problem, indent=2)}
        
        I will use a Chain of Recursive Thoughts approach to solve this problem. This involves:
        
        1. Generating multiple alternative approaches
        2. Evaluating each alternative against these criteria:
           {self._format_criteria(criteria)}
        3. Selecting the best alternative
        4. Refining my thinking through multiple rounds
        5. Producing a final solution
        
        Let me start by analyzing the problem and generating initial approaches.
        """
        
        return prompt
        
    def _format_criteria(self, criteria: List[Dict[str, str]]) -> str:
        """Format criteria for inclusion in prompts.
        
        Args:
            criteria: Evaluation criteria
            
        Returns:
            Formatted criteria
        """
        return "\n".join([
            f"   - {criterion['name']}: {criterion['description']}"
            for criterion in criteria
        ])
        
    def _generate_alternatives(
        self,
        problem_context: Dict[str, Any],
        previous_best: Optional[Dict[str, Any]],
        criteria: List[Dict[str, str]],
        current_round: int
    ) -> List[Dict[str, Any]]:
        """Generate alternative approaches.
        
        Args:
            problem_context: Problem context
            previous_best: Previous best thought (if any)
            criteria: Evaluation criteria
            current_round: Current reasoning round
            
        Returns:
            List of alternative approaches
        """
        problem = problem_context["problem"]
        
        # Create prompt for alternative generation
        if previous_best and current_round > 1:
            prompt = f"""
            # Alternative Generation - Round {current_round}
            
            I am solving this problem:
            
            {json.dumps(problem, indent=2)}
            
            In the previous round, my best approach was:
            
            {json.dumps(previous_best, indent=2)}
            
            Now I'll generate {self.alternatives_per_round} alternative approaches to solve this problem.
            These alternatives should be diverse and explore different aspects of the solution space.
            Each alternative should be an improvement or variation on the previous best approach.
            
            I'll evaluate these alternatives against these criteria:
            {self._format_criteria(criteria)}
            
            Alternative approaches:
            """
        else:
            prompt = f"""
            # Alternative Generation - Round 1
            
            I am solving this problem:
            
            {json.dumps(problem, indent=2)}
            
            I'll generate {self.alternatives_per_round} alternative approaches to solve this problem.
            These alternatives should be diverse and explore different aspects of the solution space.
            
            I'll evaluate these alternatives against these criteria:
            {self._format_criteria(criteria)}
            
            Alternative approaches:
            """
            
        # Use LLM to generate alternatives
        generation_result = self._call_llm_for_alternatives(prompt, self.alternatives_per_round)
        
        return generation_result
        
    def _call_llm_for_alternatives(
        self,
        prompt: str,
        num_alternatives: int
    ) -> List[Dict[str, Any]]:
        """Call LLM to generate alternatives.
        
        Args:
            prompt: Prompt for alternative generation
            num_alternatives: Number of alternatives to generate
            
        Returns:
            List of alternative approaches
        """
        # In a real implementation, this would use the LLM to generate alternatives
        # For now, return dummy alternatives
        alternatives = []
        
        for i in range(num_alternatives):
            alternative = {
                "id": f"alt_{i+1}",
                "approach": f"Approach {i+1}",
                "description": f"Description of approach {i+1}",
                "steps": [
                    f"Step 1 for approach {i+1}",
                    f"Step 2 for approach {i+1}",
                    f"Step 3 for approach {i+1}"
                ],
                "advantages": [
                    f"Advantage 1 for approach {i+1}",
                    f"Advantage 2 for approach {i+1}"
                ],
                "disadvantages": [
                    f"Disadvantage 1 for approach {i+1}",
                    f"Disadvantage 2 for approach {i+1}"
                ]
            }
            
            alternatives.append(alternative)
            
        return alternatives
        
    def _evaluate_alternatives(
        self,
        problem_context: Dict[str, Any],
        alternatives: List[Dict[str, Any]],
        criteria: List[Dict[str, str]],
        current_round: int
    ) -> List[Dict[str, Any]]:
        """Evaluate alternative approaches.
        
        Args:
            problem_context: Problem context
            alternatives: Alternative approaches
            criteria: Evaluation criteria
            current_round: Current reasoning round
            
        Returns:
            List of evaluations
        """
        problem = problem_context["problem"]
        
        # Create prompt for evaluation
        prompt = f"""
        # Alternative Evaluation - Round {current_round}
        
        I am solving this problem:
        
        {json.dumps(problem, indent=2)}
        
        I'll evaluate these alternative approaches against these criteria:
        {self._format_criteria(criteria)}
        
        Alternatives:
        {json.dumps(alternatives, indent=2)}
        
        Evaluations:
        """
            
        # Use LLM to evaluate alternatives
        evaluation_result = self._call_llm_for_evaluations(prompt, alternatives, criteria)
        
        return evaluation_result
        
    def _call_llm_for_evaluations(
        self,
        prompt: str,
        alternatives: List[Dict[str, Any]],
        criteria: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """Call LLM to evaluate alternatives.
        
        Args:
            prompt: Prompt for alternative evaluation
            alternatives: Alternative approaches
            criteria: Evaluation criteria
            
        Returns:
            List of evaluations
        """
        # In a real implementation, this would use the LLM to evaluate alternatives
        # For now, return dummy evaluations
        evaluations = []
        
        for i, alternative in enumerate(alternatives):
            evaluation = {
                "alternative_id": alternative["id"],
                "scores": {}
            }
            
            for criterion in criteria:
                criterion_name = criterion["name"]
                evaluation["scores"][criterion_name] = {
                    "score": random.uniform(0.6, 0.95),
                    "justification": f"Justification for {criterion_name} score of alternative {i+1}"
                }
                
            evaluation["overall_score"] = sum(
                score_data["score"] for score_data in evaluation["scores"].values()
            ) / len(criteria)
            
            evaluation["confidence"] = random.uniform(0.7, 0.95)
            
            evaluation["summary"] = f"Summary evaluation of alternative {i+1}"
            
            evaluations.append(evaluation)
            
        return evaluations
        
    def _select_best_alternative(
        self,
        alternatives: List[Dict[str, Any]],
        evaluations: List[Dict[str, Any]],
        criteria: List[Dict[str, str]]
    ) -> Tuple[int, Dict[str, Any]]:
        """Select the best alternative approach.
        
        Args:
            alternatives: Alternative approaches
            evaluations: Alternative evaluations
            criteria: Evaluation criteria
            
        Returns:
            Index of best alternative and the alternative itself
        """
        # Find the alternative with the highest overall score
        best_index = 0
        best_score = evaluations[0]["overall_score"]
        
        for i, evaluation in enumerate(evaluations):
            if evaluation["overall_score"] > best_score:
                best_index = i
                best_score = evaluation["overall_score"]
                
        # Combine the alternative with its evaluation
        best_alternative = alternatives[best_index]
        best_evaluation = evaluations[best_index]
        
        best_thought = {
            "alternative": best_alternative,
            "evaluation": best_evaluation
        }
        
        return best_index, best_thought
        
    def _should_terminate_early(
        self,
        problem_context: Dict[str, Any],
        best_thought: Dict[str, Any],
        current_round: int,
        criteria: List[Dict[str, str]]
    ) -> bool:
        """Determine if recursive thinking should terminate early.
        
        Args:
            problem_context: Problem context
            best_thought: Current best thought
            current_round: Current reasoning round
            criteria: Evaluation criteria
            
        Returns:
            True if thinking should terminate, False otherwise
        """
        # Early termination criteria:
        # 1. If confidence is very high (> 0.95)
        # 2. If we have completed at least 2 rounds
        
        if current_round >= 2:
            confidence = best_thought["evaluation"].get("confidence", 0.0)
            if confidence > 0.95:
                return True
                
        return False
        
    def _generate_solution(
        self,
        problem_context: Dict[str, Any],
        best_thought: Dict[str, Any],
        criteria: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Generate final solution.
        
        Args:
            problem_context: Problem context
            best_thought: Best thought from recursive thinking
            criteria: Evaluation criteria
            
        Returns:
            Final solution
        """
        problem = problem_context["problem"]
        
        # Create prompt for solution generation
        prompt = f"""
        # Solution Generation
        
        I have been solving this problem:
        
        {json.dumps(problem, indent=2)}
        
        Through recursive thinking, I have identified this as the best approach:
        
        {json.dumps(best_thought, indent=2)}
        
        Now I'll generate a comprehensive solution based on this approach.
        
        Solution:
        """
            
        # Use LLM to generate final solution
        solution_result = self._call_llm_for_solution(prompt, best_thought)
        
        return solution_result
        
    def _call_llm_for_solution(
        self,
        prompt: str,
        best_thought: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call LLM to generate final solution.
        
        Args:
            prompt: Prompt for solution generation
            best_thought: Best thought from recursive thinking
            
        Returns:
            Final solution
        """
        # In a real implementation, this would use the LLM to generate the solution
        # For now, return a dummy solution
        solution = {
            "approach": best_thought["alternative"]["approach"],
            "description": f"Refined description based on {best_thought['alternative']['approach']}",
            "steps": [
                "Detailed step 1",
                "Detailed step 2",
                "Detailed step 3",
                "Detailed step 4"
            ],
            "confidence": best_thought["evaluation"]["confidence"],
            "reasoning": {
                "approach_selection": f"Selected {best_thought['alternative']['approach']} because...",
                "refinements": [
                    "Refinement 1 from recursive thinking",
                    "Refinement 2 from recursive thinking"
                ]
            },
            "implementation_guidance": {
                "prerequisites": [
                    "Prerequisite 1",
                    "Prerequisite 2"
                ],
                "considerations": [
                    "Consideration 1",
                    "Consideration 2"
                ]
            }
        }
        
        return solution
```

## CoRT Trace Manager

The CoRT trace manager maintains a complete record of the reasoning process:

```python
class CoRTTraceManager:
    """Manager for CoRT reasoning traces."""
    
    def __init__(self):
        """Initialize the trace manager."""
        self.traces = {}
        
    def create_trace(self, problem: Dict[str, Any]) -> str:
        """Create a new trace.
        
        Args:
            problem: Problem being solved
            
        Returns:
            Trace ID
        """
        trace_id = str(uuid.uuid4())
        
        self.traces[trace_id] = {
            "id": trace_id,
            "created_at": datetime.now().isoformat(),
            "problem": problem,
            "rounds": [],
            "events": [],
            "solution": None,
            "prompts": []
        }
        
        return trace_id
        
    def add_prompt(self, trace_id: str, prompt: str) -> None:
        """Add a prompt to the trace.
        
        Args:
            trace_id: Trace ID
            prompt: Prompt to add
        """
        if trace_id not in self.traces:
            raise ValueError(f"Trace {trace_id} not found")
            
        self.traces[trace_id]["prompts"].append({
            "timestamp": datetime.now().isoformat(),
            "content": prompt
        })
        
    def start_round(self, trace_id: str, round_number: int) -> str:
        """Start a new round in the trace.
        
        Args:
            trace_id: Trace ID
            round_number: Round number
            
        Returns:
            Round ID
        """
        if trace_id not in self.traces:
            raise ValueError(f"Trace {trace_id} not found")
            
        round_id = f"{trace_id}_round_{round_number}"
        
        self.traces[trace_id]["rounds"].append({
            "id": round_id,
            "number": round_number,
            "timestamp": datetime.now().isoformat(),
            "alternatives": [],
            "evaluations": {},
            "selection": None
        })
        
        return round_id
        
    def add_alternative(
        self,
        trace_id: str,
        round_id: str,
        alternative_id: str,
        alternative: Dict[str, Any]
    ) -> None:
        """Add an alternative to a round.
        
        Args:
            trace_id: Trace ID
            round_id: Round ID
            alternative_id: Alternative ID
            alternative: Alternative to add
        """
        if trace_id not in self.traces:
            raise ValueError(f"Trace {trace_id} not found")
            
        round_index = None
        for i, round_data in enumerate(self.traces[trace_id]["rounds"]):
            if round_data["id"] == round_id:
                round_index = i
                break
                
        if round_index is None:
            raise ValueError(f"Round {round_id} not found in trace {trace_id}")
            
        self.traces[trace_id]["rounds"][round_index]["alternatives"].append({
            "id": alternative_id,
            "timestamp": datetime.now().isoformat(),
            "content": alternative
        })
        
    def add_evaluation(
        self,
        trace_id: str,
        round_id: str,
        alternative_id: str,
        evaluation: Dict[str, Any]
    ) -> None:
        """Add an evaluation to a round.
        
        Args:
            trace_id: Trace ID
            round_id: Round ID
            alternative_id: Alternative ID
            evaluation: Evaluation to add
        """
        if trace_id not in self.traces:
            raise ValueError(f"Trace {trace_id} not found")
            
        round_index = None
        for i, round_data in enumerate(self.traces[trace_id]["rounds"]):
            if round_data["id"] == round_id:
                round_index = i
                break
                
        if round_index is None:
            raise ValueError(f"Round {round_id} not found in trace {trace_id}")
            
        self.traces[trace_id]["rounds"][round_index]["evaluations"][alternative_id] = {
            "timestamp": datetime.now().isoformat(),
            "content": evaluation
        }
        
    def add_selection(
        self,
        trace_id: str,
        round_id: str,
        alternative_id: str,
        selection: Dict[str, Any]
    ) -> None:
        """Add a selection to a round.
        
        Args:
            trace_id: Trace ID
            round_id: Round ID
            alternative_id: Selected alternative ID
            selection: Selection to add
        """
        if trace_id not in self.traces:
            raise ValueError(f"Trace {trace_id} not found")
            
        round_index = None
        for i, round_data in enumerate(self.traces[trace_id]["rounds"]):
            if round_data["id"] == round_id:
                round_index = i
                break
                
        if round_index is None:
            raise ValueError(f"Round {round_id} not found in trace {trace_id}")
            
        self.traces[trace_id]["rounds"][round_index]["selection"] = {
            "alternative_id": alternative_id,
            "timestamp": datetime.now().isoformat(),
            "content": selection
        }
        
    def add_event(
        self,
        trace_id: str,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> None:
        """Add an event to the trace.
        
        Args:
            trace_id: Trace ID
            event_type: Event type
            event_data: Event data
        """
        if trace_id not in self.traces:
            raise ValueError(f"Trace {trace_id} not found")
            
        self.traces[trace_id]["events"].append({
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": event_data
        })
        
    def add_solution(
        self,
        trace_id: str,
        solution: Dict[str, Any]
    ) -> None:
        """Add a solution to the trace.
        
        Args:
            trace_id: Trace ID
            solution: Solution to add
        """
        if trace_id not in self.traces:
            raise ValueError(f"Trace {trace_id} not found")
            
        self.traces[trace_id]["solution"] = {
            "timestamp": datetime.now().isoformat(),
            "content": solution
        }
        
    def get_trace(self, trace_id: str) -> Dict[str, Any]:
        """Get a trace.
        
        Args:
            trace_id: Trace ID
            
        Returns:
            Complete trace
        """
        if trace_id not in self.traces:
            raise ValueError(f"Trace {trace_id} not found")
            
        return self.traces[trace_id]
        
    def list_traces(self) -> List[str]:
        """List all traces.
        
        Returns:
            List of trace IDs
        """
        return list(self.traces.keys())
```

## Domain-Specific CoRT Adapters

The CoRT framework can be adapted for specific domains:

### Policy Analysis CoRT

```python
class PolicyAnalysisCoRT(CoRTProcessor):
    """CoRT processor for policy analysis."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        max_rounds: int = 4,
        alternatives_per_round: int = 3,
        dynamic_rounds: bool = True,
        trace_manager: Optional['CoRTTraceManager'] = None
    ):
        """Initialize the policy analysis CoRT processor.
        
        Args:
            llm_generator: Function to generate LLM responses
            max_rounds: Maximum reasoning rounds
            alternatives_per_round: Number of alternatives per round
            dynamic_rounds: Whether to dynamically adjust rounds
            trace_manager: Optional trace manager
        """
        # Define policy analysis evaluation criteria
        evaluation_criteria = [
            {
                "name": "effectiveness",
                "description": "How effectively the policy addresses its stated goals"
            },
            {
                "name": "feasibility",
                "description": "How feasible the policy is to implement"
            },
            {
                "name": "compliance",
                "description": "How well the policy complies with legal and regulatory requirements"
            },
            {
                "name": "stakeholder_impact",
                "description": "How the policy impacts various stakeholders"
            },
            {
                "name": "cost_benefit",
                "description": "The balance of costs and benefits associated with the policy"
            }
        ]
        
        super().__init__(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_rounds=dynamic_rounds,
            trace_manager=trace_manager,
            evaluation_criteria=evaluation_criteria
        )
        
    def analyze_policy(
        self,
        policy_text: str,
        policy_context: Dict[str, Any],
        evaluation_criteria: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Analyze a policy using CoRT.
        
        Args:
            policy_text: Text of the policy
            policy_context: Context for the policy
            evaluation_criteria: Optional evaluation criteria
            
        Returns:
            Policy analysis with reasoning trace
        """
        # Create problem structure
        problem = {
            "type": "policy_analysis",
            "policy_text": policy_text,
            "policy_context": policy_context
        }
        
        # Create initial prompt
        initial_prompt = self._generate_policy_analysis_prompt(policy_text, policy_context)
        
        # Solve using CoRT
        result = self.solve(
            problem=problem,
            initial_prompt=initial_prompt,
            evaluation_criteria=evaluation_criteria,
            context={"domain": "policy"}
        )
        
        return result
        
    def _generate_policy_analysis_prompt(
        self,
        policy_text: str,
        policy_context: Dict[str, Any]
    ) -> str:
        """Generate policy analysis prompt.
        
        Args:
            policy_text: Text of the policy
            policy_context: Context for the policy
            
        Returns:
            Policy analysis prompt
        """
        prompt = f"""
        # Policy Analysis
        
        I need to analyze the following policy:
        
        ## Policy Text
        {policy_text}
        
        ## Policy Context
        {json.dumps(policy_context, indent=2)}
        
        I will use a Chain of Recursive Thoughts approach to analyze this policy. This involves:
        
        1. Generating multiple alternative analyses
        2. Evaluating each analysis against these criteria:
           {self._format_criteria(self.evaluation_criteria)}
        3. Selecting the best analysis
        4. Refining my thinking through multiple rounds
        5. Producing a final comprehensive analysis
        
        Let me start by analyzing the policy and generating initial approaches.
        """
        
        return prompt
```

### Economic Impact CoRT

```python
class EconomicImpactCoRT(CoRTProcessor):
    """CoRT processor for economic impact analysis."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        max_rounds: int = 4,
        alternatives_per_round: int = 3,
        dynamic_rounds: bool = True,
        trace_manager: Optional['CoRTTraceManager'] = None
    ):
        """Initialize the economic impact CoRT processor.
        
        Args:
            llm_generator: Function to generate LLM responses
            max_rounds: Maximum reasoning rounds
            alternatives_per_round: Number of alternatives per round
            dynamic_rounds: Whether to dynamically adjust rounds
            trace_manager: Optional trace manager
        """
        # Define economic impact evaluation criteria
        evaluation_criteria = [
            {
                "name": "model_validity",
                "description": "How well the economic model captures the relevant factors and interactions"
            },
            {
                "name": "empirical_support",
                "description": "The degree of empirical support for the impact estimates"
            },
            {
                "name": "comprehensiveness",
                "description": "How comprehensively the analysis covers different economic impacts"
            },
            {
                "name": "uncertainty_handling",
                "description": "How well the analysis addresses uncertainty and provides confidence intervals"
            },
            {
                "name": "stakeholder_coverage",
                "description": "How well the analysis covers impacts on different stakeholders"
            }
        ]
        
        super().__init__(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_rounds=dynamic_rounds,
            trace_manager=trace_manager,
            evaluation_criteria=evaluation_criteria
        )
        
    def analyze_economic_impact(
        self,
        policy_change: Dict[str, Any],
        economic_context: Dict[str, Any],
        model_type: str = "abundance",
        evaluation_criteria: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Analyze economic impact using CoRT.
        
        Args:
            policy_change: Description of the policy change
            economic_context: Economic context
            model_type: Type of economic model (abundance/sustainable)
            evaluation_criteria: Optional evaluation criteria
            
        Returns:
            Economic impact analysis with reasoning trace
        """
        # Create problem structure
        problem = {
            "type": "economic_impact_analysis",
            "policy_change": policy_change,
            "economic_context": economic_context,
            "model_type": model_type
        }
        
        # Create initial prompt
        initial_prompt = self._generate_economic_impact_prompt(
            policy_change,
            economic_context,
            model_type
        )
        
        # Solve using CoRT
        result = self.solve(
            problem=problem,
            initial_prompt=initial_prompt,
            evaluation_criteria=evaluation_criteria,
            context={"domain": "economics", "model_type": model_type}
        )
        
        return result
        
    def _generate_economic_impact_prompt(
        self,
        policy_change: Dict[str, Any],
        economic_context: Dict[str, Any],
        model_type: str
    ) -> str:
        """Generate economic impact prompt.
        
        Args:
            policy_change: Description of the policy change
            economic_context: Economic context
            model_type: Type of economic model
            
        Returns:
            Economic impact prompt
        """
        prompt = f"""
        # Economic Impact Analysis
        
        I need to analyze the economic impact of the following policy change:
        
        ## Policy Change
        {json.dumps(policy_change, indent=2)}
        
        ## Economic Context
        {json.dumps(economic_context, indent=2)}
        
        ## Economic Model Type
        {model_type}
        
        I will use a Chain of Recursive Thoughts approach to analyze this economic impact. This involves:
        
        1. Generating multiple alternative economic models and analyses
        2. Evaluating each analysis against these criteria:
           {self._format_criteria(self.evaluation_criteria)}
        3. Selecting the best analysis
        4. Refining my thinking through multiple rounds
        5. Producing a final comprehensive economic impact analysis
        
        Let me start by analyzing the policy change and generating initial approaches.
        """
        
        return prompt
```

## Component-Specific CoRT Extensions

The framework can be extended for HMS components:

### HMS-CDF CoRT Extension

```python
class CDFCoRTExtension(CoRTProcessor):
    """CoRT extension for HMS-CDF component."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        max_rounds: int = 4,
        alternatives_per_round: int = 3,
        dynamic_rounds: bool = True,
        trace_manager: Optional['CoRTTraceManager'] = None,
        standards_registry: Optional['StandardsRegistry'] = None
    ):
        """Initialize the CDF CoRT extension.
        
        Args:
            llm_generator: Function to generate LLM responses
            max_rounds: Maximum reasoning rounds
            alternatives_per_round: Number of alternatives per round
            dynamic_rounds: Whether to dynamically adjust rounds
            trace_manager: Optional trace manager
            standards_registry: Optional standards registry
        """
        super().__init__(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_rounds=dynamic_rounds,
            trace_manager=trace_manager
        )
        
        self.standards_registry = standards_registry
        self.policy_analysis_cort = PolicyAnalysisCoRT(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_rounds=dynamic_rounds,
            trace_manager=trace_manager
        )
        self.economic_impact_cort = EconomicImpactCoRT(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_rounds=dynamic_rounds,
            trace_manager=trace_manager
        )
        
    def analyze_legislation(
        self,
        legislation_text: str,
        applicable_laws: List[str],
        standards: List[str],
        evaluation_criteria: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Analyze legislation using CoRT.
        
        Args:
            legislation_text: Text of the legislation
            applicable_laws: Applicable laws for analysis
            standards: Standards to apply
            evaluation_criteria: Optional evaluation criteria
            
        Returns:
            Legislation analysis with reasoning trace
        """
        # Create policy context
        policy_context = {
            "applicable_laws": applicable_laws,
            "standards": standards
        }
        
        # Use policy analysis CoRT
        result = self.policy_analysis_cort.analyze_policy(
            policy_text=legislation_text,
            policy_context=policy_context,
            evaluation_criteria=evaluation_criteria
        )
        
        # Add standards compliance
        if self.standards_registry:
            result["standards_compliance"] = self._check_standards_compliance(
                legislation_text,
                standards
            )
            
        return result
        
    def analyze_economic_legislation(
        self,
        legislation_text: str,
        economic_parameters: Dict[str, Any],
        model_type: str = "abundance",
        evaluation_criteria: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Analyze economic legislation using CoRT.
        
        Args:
            legislation_text: Text of the legislation
            economic_parameters: Economic parameters
            model_type: Type of economic model
            evaluation_criteria: Optional evaluation criteria
            
        Returns:
            Economic legislation analysis with reasoning trace
        """
        # Create policy change
        policy_change = {
            "type": "legislation",
            "text": legislation_text,
            "parameters": economic_parameters
        }
        
        # Create economic context
        economic_context = {
            "model_type": model_type,
            "parameters": economic_parameters
        }
        
        # Use economic impact CoRT
        result = self.economic_impact_cort.analyze_economic_impact(
            policy_change=policy_change,
            economic_context=economic_context,
            model_type=model_type,
            evaluation_criteria=evaluation_criteria
        )
        
        return result
        
    def _check_standards_compliance(
        self,
        legislation_text: str,
        standards: List[str]
    ) -> Dict[str, Any]:
        """Check standards compliance.
        
        Args:
            legislation_text: Text of the legislation
            standards: Standards to check
            
        Returns:
            Standards compliance result
        """
        if not self.standards_registry:
            return {
                "status": "unknown",
                "message": "Standards registry not available"
            }
            
        compliance_results = {}
        
        for standard in standards:
            compliance_results[standard] = self.standards_registry.check_compliance(
                standard,
                legislation_text
            )
            
        return {
            "standards": standards,
            "results": compliance_results,
            "compliant": all(
                result.get("compliant", False)
                for result in compliance_results.values()
            )
        }
```

### HMS-MBL CoRT Extension

```python
class MBLCoRTExtension(CoRTProcessor):
    """CoRT extension for HMS-MBL component."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        max_rounds: int = 4,
        alternatives_per_round: int = 3,
        dynamic_rounds: bool = True,
        trace_manager: Optional['CoRTTraceManager'] = None,
        economic_model_registry: Optional['EconomicModelRegistry'] = None
    ):
        """Initialize the MBL CoRT extension.
        
        Args:
            llm_generator: Function to generate LLM responses
            max_rounds: Maximum reasoning rounds
            alternatives_per_round: Number of alternatives per round
            dynamic_rounds: Whether to dynamically adjust rounds
            trace_manager: Optional trace manager
            economic_model_registry: Optional economic model registry
        """
        super().__init__(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_rounds=dynamic_rounds,
            trace_manager=trace_manager
        )
        
        self.economic_model_registry = economic_model_registry
        self.economic_impact_cort = EconomicImpactCoRT(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_rounds=dynamic_rounds,
            trace_manager=trace_manager
        )
        
    def analyze_deal(
        self,
        deal: Dict[str, Any],
        economic_parameters: Dict[str, Any],
        model_type: str = "abundance",
        evaluation_criteria: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Analyze a deal using CoRT.
        
        Args:
            deal: Deal to analyze
            economic_parameters: Economic parameters
            model_type: Type of economic model
            evaluation_criteria: Optional evaluation criteria
            
        Returns:
            Deal analysis with reasoning trace
        """
        # Create policy change
        policy_change = {
            "type": "deal",
            "deal": deal,
            "parameters": economic_parameters
        }
        
        # Create economic context
        economic_context = {
            "model_type": model_type,
            "parameters": economic_parameters,
            "deal_type": deal.get("deal_type", "standard")
        }
        
        # Use economic impact CoRT
        result = self.economic_impact_cort.analyze_economic_impact(
            policy_change=policy_change,
            economic_context=economic_context,
            model_type=model_type,
            evaluation_criteria=evaluation_criteria
        )
        
        # Add moneyball metrics
        result["moneyball_metrics"] = self._calculate_moneyball_metrics(
            deal,
            result["solution"]["content"]
        )
        
        return result
        
    def optimize_deal(
        self,
        deal: Dict[str, Any],
        optimization_parameters: Dict[str, Any],
        model_type: str = "abundance",
        evaluation_criteria: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Optimize a deal using CoRT.
        
        Args:
            deal: Deal to optimize
            optimization_parameters: Optimization parameters
            model_type: Type of economic model
            evaluation_criteria: Optional evaluation criteria
            
        Returns:
            Optimized deal with reasoning trace
        """
        # Create problem
        problem = {
            "type": "deal_optimization",
            "deal": deal,
            "optimization_parameters": optimization_parameters,
            "model_type": model_type
        }
        
        # Create initial prompt
        initial_prompt = self._generate_deal_optimization_prompt(
            deal,
            optimization_parameters,
            model_type
        )
        
        # Solve using CoRT
        result = self.solve(
            problem=problem,
            initial_prompt=initial_prompt,
            evaluation_criteria=evaluation_criteria,
            context={"domain": "economics", "model_type": model_type}
        )
        
        # Add moneyball metrics
        result["moneyball_metrics"] = self._calculate_moneyball_metrics(
            result["solution"]["content"]["optimized_deal"],
            result["solution"]["content"]
        )
        
        return result
        
    def _generate_deal_optimization_prompt(
        self,
        deal: Dict[str, Any],
        optimization_parameters: Dict[str, Any],
        model_type: str
    ) -> str:
        """Generate deal optimization prompt.
        
        Args:
            deal: Deal to optimize
            optimization_parameters: Optimization parameters
            model_type: Type of economic model
            
        Returns:
            Deal optimization prompt
        """
        prompt = f"""
        # Deal Optimization
        
        I need to optimize the following deal:
        
        ## Deal
        {json.dumps(deal, indent=2)}
        
        ## Optimization Parameters
        {json.dumps(optimization_parameters, indent=2)}
        
        ## Economic Model Type
        {model_type}
        
        I will use a Chain of Recursive Thoughts approach to optimize this deal. This involves:
        
        1. Generating multiple alternative optimization approaches
        2. Evaluating each approach against relevant criteria
        3. Selecting the best optimization approach
        4. Refining my thinking through multiple rounds
        5. Producing a final optimized deal structure
        
        Let me start by analyzing the deal and generating initial optimization approaches.
        """
        
        return prompt
        
    def _calculate_moneyball_metrics(
        self,
        deal: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate moneyball metrics for a deal.
        
        Args:
            deal: Deal to analyze
            analysis: Deal analysis
            
        Returns:
            Moneyball metrics
        """
        # In a real implementation, this would use the economic model registry
        # For now, return dummy metrics
        return {
            "win_win_score": 0.85,
            "deal_complexity": 0.65,
            "chain_value": 0.92,
            "network_effect": 0.78,
            "circularity_bonus": 0.45,
            "transaction_costs": 0.22,
            "participants": len(deal.get("participants", [])),
            "confidence": 0.87
        }
```

## Task-Specific CoRT Implementations

The framework can be instantiated for specific tasks:

### Legislative Analysis Task

```python
def analyze_legislation_with_cort(
    cdf_cort: CDFCoRTExtension,
    legislation_text: str,
    applicable_laws: List[str],
    standards: List[str]
) -> Dict[str, Any]:
    """Analyze legislation using the CDF CoRT extension.
    
    Args:
        cdf_cort: CDF CoRT extension
        legislation_text: Text of the legislation
        applicable_laws: Applicable laws for analysis
        standards: Standards to apply
        
    Returns:
        Legislation analysis with reasoning trace
    """
    # Define evaluation criteria for legislation
    evaluation_criteria = [
        {
            "name": "constitutional_compliance",
            "description": "How well the legislation complies with constitutional requirements"
        },
        {
            "name": "legal_consistency",
            "description": "How consistent the legislation is with existing laws"
        },
        {
            "name": "implementation_feasibility",
            "description": "How feasible the legislation is to implement"
        },
        {
            "name": "stakeholder_impact",
            "description": "How the legislation impacts various stakeholders"
        },
        {
            "name": "effectiveness",
            "description": "How effectively the legislation addresses its stated goals"
        }
    ]
    
    # Analyze legislation
    result = cdf_cort.analyze_legislation(
        legislation_text=legislation_text,
        applicable_laws=applicable_laws,
        standards=standards,
        evaluation_criteria=evaluation_criteria
    )
    
    return result
```

### Deal Optimization Task

```python
def optimize_deal_with_cort(
    mbl_cort: MBLCoRTExtension,
    deal: Dict[str, Any],
    optimization_goals: List[str],
    model_type: str = "abundance"
) -> Dict[str, Any]:
    """Optimize a deal using the MBL CoRT extension.
    
    Args:
        mbl_cort: MBL CoRT extension
        deal: Deal to optimize
        optimization_goals: Goals for optimization
        model_type: Type of economic model
        
    Returns:
        Optimized deal with reasoning trace
    """
    # Define optimization parameters
    optimization_parameters = {
        "goals": optimization_goals,
        "constraints": [
            f"Must maintain all existing participants",
            f"Must improve overall chain value",
            f"Must maintain compliance with all standards"
        ],
        "metrics": [
            "win_win_score",
            "chain_value",
            "network_effect",
            "circularity_bonus"
        ]
    }
    
    # Define evaluation criteria for deal optimization
    evaluation_criteria = [
        {
            "name": "goal_achievement",
            "description": "How well the optimization achieves the stated goals"
        },
        {
            "name": "constraint_satisfaction",
            "description": "How well the optimization satisfies the constraints"
        },
        {
            "name": "metric_improvement",
            "description": "How much the optimization improves the key metrics"
        },
        {
            "name": "feasibility",
            "description": "How feasible the optimized deal is to implement"
        },
        {
            "name": "stakeholder_value",
            "description": "How well the optimization creates value for all stakeholders"
        }
    ]
    
    # Optimize deal
    result = mbl_cort.optimize_deal(
        deal=deal,
        optimization_parameters=optimization_parameters,
        model_type=model_type,
        evaluation_criteria=evaluation_criteria
    )
    
    return result
```

## Integration with HMS-A2A

The CoRT framework integrates with HMS-A2A:

```python
class A2ACoRTIntegration:
    """Integration of CoRT with A2A."""
    
    def __init__(
        self,
        a2a_client: 'A2AClient',
        llm_generator: Callable[[str], str],
        max_rounds: int = 3,
        alternatives_per_round: int = 3,
        dynamic_rounds: bool = True
    ):
        """Initialize the A2A CoRT integration.
        
        Args:
            a2a_client: A2A client
            llm_generator: Function to generate LLM responses
            max_rounds: Maximum reasoning rounds
            alternatives_per_round: Number of alternatives per round
            dynamic_rounds: Whether to dynamically adjust rounds
        """
        self.a2a_client = a2a_client
        self.trace_manager = CoRTTraceManager()
        self.cort_processor = CoRTProcessor(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_rounds=dynamic_rounds,
            trace_manager=self.trace_manager
        )
        
        # Register CoRT message handlers
        self.a2a_client.register_message_handler(
            "solve_with_cort",
            self._handle_solve_with_cort
        )
        self.a2a_client.register_message_handler(
            "get_cort_trace",
            self._handle_get_cort_trace
        )
        
    def _handle_solve_with_cort(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a solve_with_cort request.
        
        Args:
            parameters: Request parameters
            context: Request context
            
        Returns:
            Solving result
        """
        # Extract parameters
        problem = parameters.get("problem")
        if not problem:
            return {
                "status": "error",
                "error": "Missing problem parameter"
            }
            
        initial_prompt = parameters.get("initial_prompt")
        evaluation_criteria = parameters.get("evaluation_criteria")
        solution_context = parameters.get("context")
        
        # Solve using CoRT
        result = self.cort_processor.solve(
            problem=problem,
            initial_prompt=initial_prompt,
            evaluation_criteria=evaluation_criteria,
            context=solution_context
        )
        
        # Return result
        return {
            "status": "success",
            "solution": result["solution"],
            "trace_id": result["trace_id"],
            "rounds_completed": result["rounds_completed"],
            "confidence": result["solution"].get("confidence", 0.0)
        }
        
    def _handle_get_cort_trace(
        self,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a get_cort_trace request.
        
        Args:
            parameters: Request parameters
            context: Request context
            
        Returns:
            Trace result
        """
        # Extract parameters
        trace_id = parameters.get("trace_id")
        if not trace_id:
            return {
                "status": "error",
                "error": "Missing trace_id parameter"
            }
            
        # Get trace
        try:
            trace = self.trace_manager.get_trace(trace_id)
            return {
                "status": "success",
                "trace": trace
            }
        except ValueError as e:
            return {
                "status": "error",
                "error": str(e)
            }
```

## CoRT Message Format

The A2A protocol includes a CoRT extension for transmitting reasoning traces:

```json
{
  "message_id": "msg-uuid",
  "timestamp": "ISO-8601-timestamp",
  "sender": {
    "id": "component-agent-id",
    "type": "government|civilian|component|specialized|sub",
    "capabilities": ["capability1", "capability2"],
    "component": "component-name"
  },
  "receiver": {
    "id": "component-agent-id",
    "type": "government|civilian|component|specialized|sub",
    "component": "component-name"
  },
  "message_type": "response",
  "content": {
    "action": "solve_with_cort",
    "result": {
      "solution": { /* Solution content */ },
      "trace_id": "trace-uuid",
      "rounds_completed": 3,
      "confidence": 0.95
    }
  },
  "cort": {
    "reasoning_depth": 3,
    "alternatives_considered": 9,
    "confidence": 0.95,
    "verification_steps": ["step1", "step2"],
    "reasoning_trace": "trace-uuid",
    "reasoning_summary": "Generated multiple alternatives for economic impact analysis, evaluated against model validity and empirical support criteria, selected best alternative in round 2, refined in round 3, produced final analysis with 95% confidence."
  },
  "security": {
    "signature": "auth-signature",
    "verification_token": "token-value"
  }
}
```

## Visualization of CoRT Process

CoRT reasoning can be visualized for transparency:

```
┌───────────────────────────────────────────────────────────────┐
│                      CoRT REASONING PROCESS                   │
└───────────────────────────────────────────────────────────────┘

PROBLEM: Analyze economic impact of healthcare policy change

┌─ ROUND 1 ──────────────────────────────────────────────────┐
│                                                             │
│  ┌─ Alternative 1 ─┐    ┌─ Alternative 2 ─┐    ┌─ Alternative 3 ─┐  │
│  │                 │    │                 │    │                 │  │
│  │  Microeconomic  │    │  Macroeconomic  │    │  Sector-Specific│  │
│  │  Analysis       │    │  Analysis       │    │  Analysis       │  │
│  │                 │    │                 │    │                 │  │
│  │  Score: 0.72    │    │  Score: 0.81 ◄──┼────┼── SELECTED     │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─ ROUND 2 ──────────────────────────────────────────────────┐
│                                                             │
│  ┌─ Alternative 1 ─┐    ┌─ Alternative 2 ─┐    ┌─ Alternative 3 ─┐  │
│  │                 │    │                 │    │                 │  │
│  │  Time-Series    │    │  Cross-Sectional│    │  Integrated     │  │
│  │  Analysis       │    │  Analysis       │    │  Analysis       │  │
│  │                 │    │                 │    │                 │  │
│  │  Score: 0.79    │    │  Score: 0.76    │    │  Score: 0.88 ◄──┼──┼─ SELECTED │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─ ROUND 3 ──────────────────────────────────────────────────┐
│                                                             │
│  ┌─ Alternative 1 ─┐    ┌─ Alternative 2 ─┐    ┌─ Alternative 3 ─┐  │
│  │                 │    │                 │    │                 │  │
│  │  5-Year         │    │  10-Year        │    │  Multi-Scenario │  │
│  │  Projection     │    │  Projection     │    │  Projection     │  │
│  │                 │    │                 │    │                 │  │
│  │  Score: 0.86    │    │  Score: 0.82    │    │  Score: 0.93 ◄──┼──┼─ SELECTED │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─ FINAL SOLUTION ───────────────────────────────────────────┐
│                                                             │
│  Multi-Scenario Integrated Macroeconomic Analysis          │
│                                                             │
│  - Incorporates both macro trends and sector-specific impacts │
│  - Provides projections under multiple economic scenarios   │
│  - Includes confidence intervals for all projections        │
│  - Quantifies impacts on different stakeholder groups       │
│  - Addresses both short-term and long-term effects          │
│                                                             │
│  Confidence: 95%                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Integration with Verification Framework

The CoRT framework integrates with the verification framework:

```python
class VerifiedCoRTProcessor(CoRTProcessor):
    """CoRT processor with verification integration."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        verification_manager: 'VerificationManager',
        max_rounds: int = 3,
        alternatives_per_round: int = 3,
        dynamic_rounds: bool = True,
        trace_manager: Optional['CoRTTraceManager'] = None,
        evaluation_criteria: Optional[List[Dict[str, str]]] = None
    ):
        """Initialize the verified CoRT processor.
        
        Args:
            llm_generator: Function to generate LLM responses
            verification_manager: Verification manager
            max_rounds: Maximum reasoning rounds
            alternatives_per_round: Number of alternatives per round
            dynamic_rounds: Whether to dynamically adjust rounds
            trace_manager: Optional trace manager
            evaluation_criteria: Optional default evaluation criteria
        """
        super().__init__(
            llm_generator=llm_generator,
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_rounds=dynamic_rounds,
            trace_manager=trace_manager,
            evaluation_criteria=evaluation_criteria
        )
        
        self.verification_manager = verification_manager
        
    def solve(
        self,
        problem: Dict[str, Any],
        initial_prompt: Optional[str] = None,
        evaluation_criteria: Optional[List[Dict[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Solve a problem using verified recursive thinking.
        
        Args:
            problem: Problem to solve
            initial_prompt: Optional prompt to start reasoning
            evaluation_criteria: Optional criteria for this specific problem
            context: Optional additional context
            
        Returns:
            Solution with reasoning trace and verification
        """
        # Verify the problem
        problem_verification = self.verification_manager.verify_task({
            "task_id": str(uuid.uuid4()),
            "action": "solve_with_cort",
            "parameters": {
                "problem": problem,
                "evaluation_criteria": evaluation_criteria
            },
            "meta": context or {}
        })
        
        if not problem_verification["valid"]:
            return {
                "status": "error",
                "error": "Invalid problem",
                "verification_issues": problem_verification.get("issues", [])
            }
            
        # Proceed with standard solving
        result = super().solve(
            problem=problem,
            initial_prompt=initial_prompt,
            evaluation_criteria=evaluation_criteria,
            context=context
        )
        
        # Verify the solution
        solution_verification = self.verification_manager.verify_result(
            {
                "result_id": str(uuid.uuid4()),
                "task_id": str(uuid.uuid4()),
                "status": "success",
                "result": result["solution"]
            },
            {
                "task_id": str(uuid.uuid4()),
                "action": "solve_with_cort",
                "parameters": {
                    "problem": problem,
                    "evaluation_criteria": evaluation_criteria
                },
                "meta": context or {}
            }
        )
        
        # Add verification information
        result["verification"] = {
            "valid": solution_verification["valid"],
            "issues": solution_verification.get("issues", []),
            "verification_id": solution_verification.get("verification_id")
        }
        
        return result
```

## Human-in-the-Loop (HITL) Integration

The CoRT framework can integrate with human reviewers:

```python
class HITLCoRTProcessor(VerifiedCoRTProcessor):
    """CoRT processor with human-in-the-loop integration."""
    
    def __init__(
        self,
        llm_generator: Callable[[str], str],
        verification_manager: 'VerificationManager',
        human_review_manager: 'HumanReviewManager',
        max_rounds: int = 3,
        alternatives_per_round: int = 3,
        dynamic_rounds: bool = True,
        trace_manager: Optional['CoRTTraceManager'] = None,
        evaluation_criteria: Optional[List[Dict[str, str]]] = None
    ):
        """Initialize the HITL CoRT processor.
        
        Args:
            llm_generator: Function to generate LLM responses
            verification_manager: Verification manager
            human_review_manager: Human review manager
            max_rounds: Maximum reasoning rounds
            alternatives_per_round: Number of alternatives per round
            dynamic_rounds: Whether to dynamically adjust rounds
            trace_manager: Optional trace manager
            evaluation_criteria: Optional default evaluation criteria
        """
        super().__init__(
            llm_generator=llm_generator,
            verification_manager=verification_manager,
            max_rounds=max_rounds,
            alternatives_per_round=alternatives_per_round,
            dynamic_rounds=dynamic_rounds,
            trace_manager=trace_manager,
            evaluation_criteria=evaluation_criteria
        )
        
        self.human_review_manager = human_review_manager
        
    def solve(
        self,
        problem: Dict[str, Any],
        initial_prompt: Optional[str] = None,
        evaluation_criteria: Optional[List[Dict[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        wait_for_human_review: bool = False
    ) -> Dict[str, Any]:
        """Solve a problem using verified recursive thinking with human review.
        
        Args:
            problem: Problem to solve
            initial_prompt: Optional prompt to start reasoning
            evaluation_criteria: Optional criteria for this specific problem
            context: Optional additional context
            wait_for_human_review: Whether to wait for human review completion
            
        Returns:
            Solution with reasoning trace, verification, and human review
        """
        # Get solution with verification
        result = super().solve(
            problem=problem,
            initial_prompt=initial_prompt,
            evaluation_criteria=evaluation_criteria,
            context=context
        )
        
        # Check if solution requires human review
        requires_human_review = self._requires_human_review(problem, result)
        
        if requires_human_review:
            # Request human review
            review_request_id = self.human_review_manager.request_review(
                {
                    "task_id": str(uuid.uuid4()),
                    "action": "solve_with_cort",
                    "parameters": {
                        "problem": problem,
                        "evaluation_criteria": evaluation_criteria
                    },
                    "meta": context or {}
                },
                result["verification"].get("verification_id", str(uuid.uuid4()))
            )
            
            # Add human review information
            result["human_review"] = {
                "required": True,
                "request_id": review_request_id,
                "status": "pending"
            }
            
            # Optionally wait for human review
            if wait_for_human_review:
                review_status = self._wait_for_human_review(review_request_id)
                result["human_review"]["status"] = review_status["status"]
                result["human_review"]["reviewer"] = review_status.get("reviewer")
                result["human_review"]["review_result"] = review_status.get("review_result")
                result["human_review"]["review_comments"] = review_status.get("review_comments")
        else:
            # No human review required
            result["human_review"] = {
                "required": False
            }
            
        return result
        
    def _requires_human_review(
        self,
        problem: Dict[str, Any],
        result: Dict[str, Any]
    ) -> bool:
        """Determine if a solution requires human review.
        
        Args:
            problem: Problem that was solved
            result: Solution result
            
        Returns:
            True if human review is required, False otherwise
        """
        # Check if verification found issues
        if not result["verification"]["valid"]:
            return True
            
        # Check problem type
        problem_type = problem.get("type", "")
        if problem_type in ["policy_analysis", "economic_impact_analysis"]:
            return True
            
        # Check solution confidence
        confidence = result["solution"].get("confidence", 0.0)
        if confidence < 0.8:
            return True
            
        return False
        
    def _wait_for_human_review(self, review_request_id: str) -> Dict[str, Any]:
        """Wait for human review completion.
        
        Args:
            review_request_id: Review request ID
            
        Returns:
            Review status
        """
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            # Get review status
            status = self.human_review_manager.get_review_status(review_request_id)
            
            if status["status"] == "completed":
                return status
                
            # Wait before checking again
            time.sleep(10)
            attempt += 1
            
        return {
            "status": "timeout",
            "message": "Timeout waiting for human review"
        }
```

## Conclusion

The Chain of Recursive Thoughts (CoRT) framework provides HMS agents with advanced reasoning capabilities, enabling more thorough exploration of solution spaces, explicit alternative generation and evaluation, and transparent reasoning traces. By recursively refining thoughts through multiple rounds, the framework produces higher-quality solutions and provides complete traceability of the decision process.

The layered architecture, with progressively increasing specialization from the base framework to task-specific implementations, provides a flexible and extensible approach. Domain-specific adaptations enhance the framework for specific use cases, while component-specific extensions integrate tightly with HMS components.

Integration with the verification framework and human-in-the-loop systems ensures that CoRT reasoning remains reliable, compliant, and trustworthy. The A2A protocol extension enables sharing of CoRT capabilities and reasoning traces across the HMS ecosystem.

This implementation builds on best practices from the original Chain-of-Recursive-Thoughts framework while adapting it to the specific needs of the HMS system, creating a powerful foundation for intelligent agent reasoning.