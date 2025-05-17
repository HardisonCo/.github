# HMS Agent System Demo Mode Specification

## Overview

This document specifies the implementation of the HMS Agent System Demo Mode, which showcases the capabilities of the system-wide agent architecture using a practical example of GitHub issue resolution and cross-component collaboration.

The demo illustrates:
1. Component agents identifying and discussing GitHub issues
2. The supervisor agent orchestrating the collaboration process 
3. Specialized agents applying domain knowledge to resolve issues
4. The use of Chain of Recursive Thoughts (CoRT) for complex decision-making
5. System status updates and reporting

## Demo Scenario: GitHub Issue Resolution

### Scenario Description

The demo simulates the resolution of a GitHub issue that spans multiple HMS components. The scenario demonstrates how component agents collaborate to:
1. Analyze the issue
2. Formulate a solution strategy
3. Implement and test the fix
4. Update system status

### Flow Diagram

```
┌────────────────┐     1. Issue Detection     ┌─────────────────┐
│  GitHub Issue  │──────────────────────────▶│  HMS-DEV Agent  │
└────────────────┘                           └────────┬─────────┘
                                                     │
                                                     │ 2. Issue Analysis
                                                     ▼
┌────────────────┐     3. Task Assignment    ┌─────────────────┐
│ Component      │◀──────────────────────────│ CoRT Supervisor │
│ Agents         │                           └─────────────────┘
└───────┬────────┘
        │
        │ 4. Collaboration
        ▼
┌────────────────────────────────────────────────────┐
│                                                    │
│  ┌─────────────┐     ┌─────────────┐              │
│  │ HMS-DOC     │◀───▶│ HMS-API     │              │
│  │ Agent       │     │ Agent       │              │
│  └─────────────┘     └─────────────┘              │
│                                                    │
│  ┌─────────────┐     ┌─────────────┐              │
│  │ HMS-CDF     │◀───▶│ HMS-A2A     │              │
│  │ Agent       │     │ Agent       │              │
│  └─────────────┘     └─────────────┘              │
│                                                    │
└────────────────────────┬───────────────────────────┘
                         │
                         │ 5. Solution Implementation
                         ▼
┌────────────────┐     6. Status Update     ┌─────────────────┐
│  System Status │◀──────────────────────────│ HMS-DEV Agent  │
└────────────────┘                           └─────────────────┘
```

## Component Agent Roles

### HMS-DEV Agent
- **Role**: Lead agent for development workflows and issue management
- **Demo Responsibilities**:
  - Monitor GitHub issues
  - Perform initial issue analysis
  - Coordinate with component agents for resolution
  - Implement fixes to development tools
  - Update system status

### CoRT Supervisor
- **Role**: Orchestrates agent collaboration and provides decision support
- **Demo Responsibilities**:
  - Analyze issue complexity and impact
  - Assign tasks to appropriate component agents
  - Evaluate proposed solutions using CoRT reasoning
  - Provide improvement suggestions
  - Monitor agent progress

### Component Agents (HMS-API, HMS-A2A, HMS-DOC, HMS-CDF)
- **Role**: Domain-specific agents for each HMS component
- **Demo Responsibilities**:
  - Analyze issue impact on their component
  - Contribute domain expertise to solution formulation
  - Implement fixes related to their component
  - Validate component-specific functionality
  - Document changes and integration points

## Demo Implementation Details

### 1. Initialization Phase

```python
# Start supervisor and component agents
def initialize_demo():
    # Initialize the CoRT Supervisor
    supervisor = CoRTSupervisor(config={
        "journal_dir": "/path/to/journals",
        "ticket_dir": "/path/to/tickets",
        "feedback_dir": "/path/to/feedback",
        "check_interval_seconds": 5  # Shortened for demo purposes
    })
    
    # Initialize component agents
    dev_agent = ComponentAgent("HMS-DEV", "Development Tools")
    api_agent = ComponentAgent("HMS-API", "API Services")
    doc_agent = ComponentAgent("HMS-DOC", "Documentation")
    a2a_agent = ComponentAgent("HMS-A2A", "Agent-to-Agent Protocol")
    cdf_agent = ComponentAgent("HMS-CDF", "Codified Democracy Foundation")
    
    # Register all agents with the supervisor
    registry = AgentRegistry()
    registry.register_agent(dev_agent)
    registry.register_agent(api_agent)
    registry.register_agent(doc_agent)
    registry.register_agent(a2a_agent)
    registry.register_agent(cdf_agent)
    
    return {
        "supervisor": supervisor,
        "agents": {
            "dev": dev_agent,
            "api": api_agent,
            "doc": doc_agent,
            "a2a": a2a_agent,
            "cdf": cdf_agent
        },
        "registry": registry
    }
```

### 2. Issue Detection

```python
# HMS-DEV agent detects a GitHub issue
def detect_github_issue(dev_agent):
    # Simulate GitHub webhook or API call
    issue = {
        "id": "issue-12345",
        "title": "A2A protocol integration error in API endpoints",
        "description": "When using HMS-API endpoints with A2A protocol, authentication fails intermittently. This appears to affect documentation generation and CDF verification as well.",
        "labels": ["bug", "integration", "high-priority"],
        "components": ["HMS-API", "HMS-A2A", "HMS-DOC", "HMS-CDF"]
    }
    
    # HMS-DEV agent logs the issue to its journal
    dev_agent.log_to_journal(
        title="GitHub Issue Analysis", 
        objective=f"Analyze and resolve GitHub issue #{issue['id']}: {issue['title']}",
        content=f"Detected GitHub issue that spans multiple components: {issue['components']}\n\nDescription: {issue['description']}"
    )
    
    return issue
```

### 3. Issue Analysis and Task Assignment

```python
# CoRT Supervisor analyzes the issue and assigns tasks
def analyze_and_assign_tasks(supervisor, issue, agents, registry):
    # Analyze the issue using Chain of Recursive Thoughts
    analysis = supervisor.analyze_issue(issue)
    
    # Create a collaboration session
    session_id = registry.create_collaboration_session(issue["components"])
    
    # Assign tasks to component agents
    tasks = {}
    for component in issue["components"]:
        agent_id = component.lower().replace("hms-", "")
        if agent_id in agents:
            task = {
                "id": f"task-{uuid.uuid4().hex[:8]}",
                "issue_id": issue["id"],
                "session_id": session_id,
                "description": f"Analyze how {component} is affected by: {issue['title']}",
                "deadline": (datetime.now() + timedelta(minutes=30)).isoformat(),
                "priority": "high"
            }
            agents[agent_id].assign_task(task)
            tasks[agent_id] = task
    
    return {
        "analysis": analysis,
        "session_id": session_id,
        "tasks": tasks
    }
```

### 4. Agent Collaboration

```python
# Component agents collaborate to formulate a solution
def agent_collaboration(session_id, agents, registry):
    # Agents share their analyses
    analyses = {}
    for agent_id, agent in agents.items():
        analysis = agent.analyze_assigned_task()
        registry.share_analysis(session_id, agent_id, analysis)
        analyses[agent_id] = analysis
    
    # Agents discuss and formulate a solution using CoRT
    solution_discussion = registry.initiate_cort_discussion(
        session_id,
        topic="Resolving A2A protocol integration in API endpoints",
        participants=list(agents.keys()),
        rounds=3,
        alternatives=2
    )
    
    # Reach consensus on solution approach
    solution = registry.build_consensus(
        session_id,
        discussion=solution_discussion,
        threshold=0.75
    )
    
    return {
        "analyses": analyses,
        "discussion": solution_discussion,
        "solution": solution
    }
```

### 5. Solution Implementation

```python
# Agents implement the solution
def implement_solution(solution, agents, registry):
    # Break down solution into implementation tasks
    implementation_tasks = registry.create_implementation_plan(solution)
    
    # Assign implementation tasks to agents
    assignments = {}
    for task in implementation_tasks:
        assigned_agent = agents[task["agent_id"]]
        assigned_agent.implement_task(task)
        assignments[task["id"]] = {
            "agent_id": task["agent_id"],
            "status": "in_progress",
            "task": task
        }
    
    # Agents execute their tasks
    results = {}
    for task_id, assignment in assignments.items():
        agent = agents[assignment["agent_id"]]
        result = agent.complete_task(task_id)
        results[task_id] = result
        assignment["status"] = "completed"
    
    # Verify the implementation
    verification = registry.verify_implementation(
        results=results,
        solution=solution
    )
    
    return {
        "tasks": implementation_tasks,
        "assignments": assignments,
        "results": results,
        "verification": verification
    }
```

### 6. Status Update

```python
# Update system status
def update_system_status(issue, solution, implementation, dev_agent):
    # Prepare the status update
    status_update = {
        "issue_id": issue["id"],
        "title": issue["title"],
        "resolution_summary": solution["summary"],
        "components_affected": issue["components"],
        "implementation_status": "completed" if implementation["verification"]["success"] else "failed",
        "verification_results": implementation["verification"],
        "timestamp": datetime.now().isoformat()
    }
    
    # HMS-DEV agent updates the system status
    dev_agent.update_system_status(status_update)
    
    # Close the GitHub issue
    dev_agent.close_github_issue(
        issue_id=issue["id"],
        resolution_comment=f"Resolution summary: {solution['summary']}\n\nImplementation details: {json.dumps(implementation['results'], indent=2)}"
    )
    
    return status_update
```

## Demo Mode UI/UX

### Console Output Format

The demo will display the following information in the console:

```
==================================================
HMS AGENT SYSTEM DEMO MODE - GitHub Issue Resolution
==================================================

[INITIALIZATION] Starting HMS Agent System Demo...
[INITIALIZATION] Initializing CoRT Supervisor...
[INITIALIZATION] Initializing Component Agents...
[INITIALIZATION] All agents initialized successfully.

[ISSUE DETECTION] New GitHub issue detected by HMS-DEV Agent:
Issue #12345: A2A protocol integration error in API endpoints
Labels: bug, integration, high-priority
Affected Components: HMS-API, HMS-A2A, HMS-DOC, HMS-CDF

[ISSUE ANALYSIS] CoRT Supervisor analyzing issue...
[ISSUE ANALYSIS] Identified root cause candidates:
 - Authentication token format mismatch
 - API endpoint version inconsistency
 - Documentation schema outdated
[ISSUE ANALYSIS] Complexity assessment: HIGH
[ISSUE ANALYSIS] Impact assessment: CRITICAL

[TASK ASSIGNMENT] Assigning tasks to component agents...
[TASK ASSIGNMENT] HMS-API Agent: Analyze API authentication flow
[TASK ASSIGNMENT] HMS-A2A Agent: Verify A2A protocol implementation
[TASK ASSIGNMENT] HMS-DOC Agent: Check documentation consistency
[TASK ASSIGNMENT] HMS-CDF Agent: Validate verification procedures

[AGENT COLLABORATION] Starting agent collaboration session...
[COLLABORATION] HMS-API Agent: "Authentication tokens use v1 format but A2A expects v2"
[COLLABORATION] HMS-A2A Agent: "Our protocol implementation was updated in v2.1.0"
[COLLABORATION] HMS-DOC Agent: "Documentation refers to v1 format in 3 places"
[COLLABORATION] HMS-CDF Agent: "Verification uses outdated schema from v1"

[CORT REASONING] Initiating Chain of Recursive Thoughts...
[CORT] Round 1: Generating initial thoughts...
[CORT] Round 2: Exploring alternatives...
[CORT] Round 3: Selecting optimal solution...
[CORT] Solution consensus reached: 87% agreement

[IMPLEMENTATION] Implementing solution across components...
[IMPLEMENTATION] HMS-API Agent: Updating authentication handlers
[IMPLEMENTATION] HMS-A2A Agent: Adding backward compatibility
[IMPLEMENTATION] HMS-DOC Agent: Updating documentation references
[IMPLEMENTATION] HMS-CDF Agent: Updating verification schemas

[VERIFICATION] Verifying implementation...
[VERIFICATION] Running integration tests...
[VERIFICATION] Checking standards compliance...
[VERIFICATION] Implementation verified successfully!

[STATUS UPDATE] Updating system status...
[STATUS UPDATE] GitHub issue #12345 closed with resolution
[STATUS UPDATE] System status updated: OPERATIONAL

==================================================
DEMO COMPLETED SUCCESSFULLY
==================================================
```

### Visual Components

For enhanced visualization, the demo will include:

1. **Agent Network Diagram**: Real-time visualization of agent interactions
2. **Task Status Dashboard**: Progress tracking for each agent's tasks
3. **CoRT Reasoning Tree**: Visual representation of the reasoning process
4. **System Status Panel**: Current operational status of each component

## Demo Mode Invocation

The demo mode can be launched using:

```bash
./agents-conversation.sh --demo github-issue
```

Additional options:

- `--verbose`: Display detailed agent communications
- `--slow`: Run in slow motion with pauses between steps
- `--interactive`: Allow user interaction at key decision points
- `--save-logs`: Save all demo logs for later analysis

## Success Criteria

The demo is considered successful when:

1. All agents are properly initialized
2. The GitHub issue is correctly analyzed
3. Tasks are appropriately assigned to component agents
4. Agent collaboration produces a viable solution
5. The solution is correctly implemented
6. Implementation is verified successfully
7. System status is updated accurately

## Conclusion

This demo mode specification provides a comprehensive blueprint for showcasing the HMS Agent System's capabilities in a realistic scenario. By demonstrating GitHub issue resolution across multiple components, the demo highlights:

- Intelligent agent collaboration
- Chain of Recursive Thoughts (CoRT) reasoning
- Domain-specific agent specialization
- Cross-component integration
- System status management

This practical demonstration serves as both a validation of the system's capabilities and an educational tool for understanding how the HMS Agent System operates in real-world scenarios.