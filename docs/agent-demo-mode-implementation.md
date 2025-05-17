# HMS Agent System Demo Mode Implementation

## Overview

This document provides the complete implementation details for the HMS Agent System Demo Mode, which showcases the full capabilities of the system-wide agent architecture through practical, real-world scenarios. The demo mode demonstrates how component agents collaborate to identify, analyze, and resolve GitHub issues while leveraging Chain of Recursive Thoughts (CoRT) for complex decision-making and maintaining standards compliance.

## Demo Architecture

The demo implementation follows a modular architecture:

```
┌───────────────────────────────────────────────────────────────┐
│                     Demo Orchestrator                         │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                    Scenario Manager                           │
└──┬────────────────┬─────────────────┬────────────────┬────────┘
   │                │                 │                │
   ▼                ▼                 ▼                ▼
┌─────────┐   ┌──────────┐    ┌──────────────┐  ┌─────────────┐
│ GitHub  │   │   Agent   │    │ Visualization│  │    Logger   │
│ Service │   │  System   │    │    Engine    │  │             │
└────┬────┘   └─────┬─────┘    └──────┬───────┘  └──────┬──────┘
     │             │                  │                 │
     └─────────────┴──────────────────┴─────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                    UI Presentation Layer                      │
└───────────────────────────────────────────────────────────────┘
```

## Implementation Components

### 1. Demo Orchestrator

The Demo Orchestrator manages the overall demo flow and coordinates all components:

```python
# demo/orchestrator.py

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

from demo.scenario import ScenarioManager, GitHubIssueScenario, DealMonitoringScenario
from demo.visualization import VisualizationEngine
from demo.github import GitHubService
from demo.logger import DemoLogger

class DemoOrchestrator:
    """Orchestrates the HMS Agent System Demo Mode."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the Demo Orchestrator.
        
        Args:
            config: Configuration parameters
        """
        self.config = config
        self.session_id = f"demo-{uuid.uuid4().hex[:8]}"
        self.start_time = datetime.now()
        
        # Initialize components
        self.logger = DemoLogger(
            log_dir=config.get("log_dir", "./logs"),
            session_id=self.session_id
        )
        
        self.github_service = GitHubService(
            github_token=config.get("github_token"),
            repository=config.get("github_repository"),
            logger=self.logger
        )
        
        self.visualization = VisualizationEngine(
            output_dir=config.get("visualization_dir", "./visualizations"),
            session_id=self.session_id,
            logger=self.logger
        )
        
        self.scenario_manager = ScenarioManager(
            github_service=self.github_service,
            visualization=self.visualization,
            logger=self.logger,
            config=config
        )
        
        self.logger.info(f"Demo Orchestrator initialized with session ID: {self.session_id}")
    
    def run_github_issue_demo(self, issue_id: Optional[str] = None) -> Dict[str, Any]:
        """Run the GitHub issue resolution demo.
        
        Args:
            issue_id: Specific GitHub issue ID to use, or None for automatic selection
            
        Returns:
            Dict containing demo results
        """
        self.logger.info(f"Starting GitHub Issue Resolution Demo")
        
        # Create and initialize the scenario
        scenario = self.scenario_manager.create_scenario(
            scenario_type="github_issue",
            parameters={
                "issue_id": issue_id
            }
        )
        
        # Execute the scenario
        result = scenario.execute()
        
        # Generate visualization
        visualization_url = self.visualization.generate_scenario_visualization(
            scenario=scenario,
            result=result
        )
        
        # Log completion
        self.logger.info(f"GitHub Issue Resolution Demo completed: {result['status']}")
        
        return {
            "session_id": self.session_id,
            "scenario_type": "github_issue",
            "result": result,
            "visualization_url": visualization_url,
            "duration": (datetime.now() - self.start_time).total_seconds()
        }
    
    def run_deal_monitoring_demo(self, deal_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Run the Deal Monitoring demo.
        
        Args:
            deal_parameters: Parameters for the deal to monitor
            
        Returns:
            Dict containing demo results
        """
        self.logger.info(f"Starting Deal Monitoring Demo")
        
        # Create and initialize the scenario
        scenario = self.scenario_manager.create_scenario(
            scenario_type="deal_monitoring",
            parameters=deal_parameters
        )
        
        # Execute the scenario
        result = scenario.execute()
        
        # Generate visualization
        visualization_url = self.visualization.generate_scenario_visualization(
            scenario=scenario,
            result=result
        )
        
        # Log completion
        self.logger.info(f"Deal Monitoring Demo completed: {result['status']}")
        
        return {
            "session_id": self.session_id,
            "scenario_type": "deal_monitoring",
            "result": result,
            "visualization_url": visualization_url,
            "duration": (datetime.now() - self.start_time).total_seconds()
        }
    
    def shutdown(self) -> None:
        """Shutdown the demo orchestrator."""
        self.logger.info(f"Shutting down Demo Orchestrator")
        self.scenario_manager.cleanup()
        self.visualization.cleanup()
        self.logger.info(f"Demo Orchestrator shutdown complete")
```

### 2. Scenario Manager

The Scenario Manager creates and manages different demo scenarios:

```python
# demo/scenario.py

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

from demo.github import GitHubService
from demo.visualization import VisualizationEngine
from demo.logger import DemoLogger

class DemoScenario(ABC):
    """Abstract base class for demo scenarios."""
    
    def __init__(self, github_service, visualization, logger, parameters):
        """Initialize the demo scenario.
        
        Args:
            github_service: GitHub service instance
            visualization: Visualization engine instance
            logger: Demo logger instance
            parameters: Scenario-specific parameters
        """
        self.github_service = github_service
        self.visualization = visualization
        self.logger = logger
        self.parameters = parameters
        self.events = []
        
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the scenario.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """Execute the scenario.
        
        Returns:
            Dict containing execution results
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources after scenario execution."""
        pass
    
    def log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log a scenario event.
        
        Args:
            event_type: Type of event
            details: Event details
        """
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.events.append(event)
        self.logger.info(f"Scenario event: {event_type}", extra=details)

class GitHubIssueScenario(DemoScenario):
    """GitHub issue resolution demo scenario."""
    
    def initialize(self) -> bool:
        """Initialize the GitHub issue scenario.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        self.log_event("scenario_init", {"type": "github_issue"})
        
        # Get issue ID from parameters or select an open issue
        issue_id = self.parameters.get("issue_id")
        if issue_id:
            self.issue = self.github_service.get_issue(issue_id)
            if not self.issue:
                self.logger.error(f"Issue {issue_id} not found")
                return False
        else:
            # Select a suitable open issue
            open_issues = self.github_service.get_open_issues()
            if not open_issues:
                self.logger.error("No open issues found")
                return False
            
            # Select an issue with appropriate labels for demo
            self.issue = self._select_appropriate_issue(open_issues)
            if not self.issue:
                self.logger.error("No suitable issues found for demo")
                return False
        
        self.log_event("issue_selected", {"issue_id": self.issue["id"], "title": self.issue["title"]})
        return True
    
    def _select_appropriate_issue(self, issues: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Select an appropriate issue for the demo.
        
        Args:
            issues: List of open issues
            
        Returns:
            Selected issue or None if no suitable issue found
        """
        # Look for issues with bug, feature, or documentation labels
        for issue in issues:
            labels = [label["name"] for label in issue["labels"]]
            if any(label in labels for label in ["bug", "feature", "documentation"]):
                return issue
        
        # If no matching labels, return the first issue
        if issues:
            return issues[0]
        
        return None
    
    def execute(self) -> Dict[str, Any]:
        """Execute the GitHub issue resolution scenario.
        
        Returns:
            Dict containing execution results
        """
        self.log_event("scenario_execution_start", {"issue_id": self.issue["id"]})
        
        # Step 1: Issue Analysis
        analysis_result = self._analyze_issue()
        self.log_event("issue_analysis_complete", analysis_result)
        
        # Step 2: Component Agent Assignment
        assignment_result = self._assign_component_agents(analysis_result)
        self.log_event("component_agent_assignment_complete", assignment_result)
        
        # Step 3: Collaboration Session
        collaboration_result = self._run_collaboration_session(assignment_result)
        self.log_event("collaboration_session_complete", collaboration_result)
        
        # Step 4: Solution Implementation
        implementation_result = self._implement_solution(collaboration_result)
        self.log_event("solution_implementation_complete", implementation_result)
        
        # Step 5: Verification
        verification_result = self._verify_implementation(implementation_result)
        self.log_event("implementation_verification_complete", verification_result)
        
        # Step 6: Issue Resolution
        if verification_result["verified"]:
            resolution_result = self._resolve_issue(verification_result)
            self.log_event("issue_resolution_complete", resolution_result)
            status = "resolved"
        else:
            self.log_event("issue_resolution_failed", verification_result)
            status = "failed"
        
        self.log_event("scenario_execution_complete", {"status": status})
        
        return {
            "issue": self.issue,
            "analysis": analysis_result,
            "assignment": assignment_result,
            "collaboration": collaboration_result,
            "implementation": implementation_result,
            "verification": verification_result,
            "status": status,
            "events": self.events
        }
    
    def _analyze_issue(self) -> Dict[str, Any]:
        """Analyze the GitHub issue.
        
        Returns:
            Issue analysis result
        """
        # Implementation for issue analysis
        # In a full implementation, this would call agent-based analysis
        pass
    
    def _assign_component_agents(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Assign component agents based on issue analysis.
        
        Args:
            analysis_result: Issue analysis result
            
        Returns:
            Component agent assignment result
        """
        # Implementation for component agent assignment
        # In a full implementation, this would assign agents based on analysis
        pass
    
    def _run_collaboration_session(self, assignment_result: Dict[str, Any]) -> Dict[str, Any]:
        """Run a collaboration session among assigned agents.
        
        Args:
            assignment_result: Component agent assignment result
            
        Returns:
            Collaboration session result
        """
        # Implementation for collaboration session
        # In a full implementation, this would run agent collaboration
        pass
    
    def _implement_solution(self, collaboration_result: Dict[str, Any]) -> Dict[str, Any]:
        """Implement the solution based on collaboration result.
        
        Args:
            collaboration_result: Collaboration session result
            
        Returns:
            Solution implementation result
        """
        # Implementation for solution implementation
        # In a full implementation, this would implement changes
        pass
    
    def _verify_implementation(self, implementation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Verify the implemented solution.
        
        Args:
            implementation_result: Solution implementation result
            
        Returns:
            Verification result
        """
        # Implementation for solution verification
        # In a full implementation, this would verify changes
        pass
    
    def _resolve_issue(self, verification_result: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve the GitHub issue.
        
        Args:
            verification_result: Verification result
            
        Returns:
            Issue resolution result
        """
        # Implementation for issue resolution
        # In a full implementation, this would close the issue
        pass
    
    def cleanup(self) -> None:
        """Clean up resources after scenario execution."""
        # Implementation for cleanup
        pass

class DealMonitoringScenario(DemoScenario):
    """Deal monitoring demo scenario."""
    
    def initialize(self) -> bool:
        """Initialize the deal monitoring scenario.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        self.log_event("scenario_init", {"type": "deal_monitoring"})
        
        # Initialize deal parameters
        self.deal_parameters = self.parameters
        self.deal_id = f"deal-{uuid.uuid4().hex[:8]}"
        
        self.log_event("deal_initialization", {
            "deal_id": self.deal_id,
            "parameters": self.deal_parameters
        })
        
        return True
    
    def execute(self) -> Dict[str, Any]:
        """Execute the deal monitoring scenario.
        
        Returns:
            Dict containing execution results
        """
        self.log_event("scenario_execution_start", {"deal_id": self.deal_id})
        
        # Step 1: Deal Creation
        creation_result = self._create_deal()
        self.log_event("deal_creation_complete", creation_result)
        
        # Step 2: Deal Evaluation
        evaluation_result = self._evaluate_deal(creation_result)
        self.log_event("deal_evaluation_complete", evaluation_result)
        
        # Step 3: Deal Execution
        execution_result = self._execute_deal(evaluation_result)
        self.log_event("deal_execution_complete", execution_result)
        
        # Step 4: Deal Reporting
        reporting_result = self._generate_report(execution_result)
        self.log_event("deal_reporting_complete", reporting_result)
        
        self.log_event("scenario_execution_complete", {"status": "completed"})
        
        return {
            "deal_id": self.deal_id,
            "parameters": self.deal_parameters,
            "creation": creation_result,
            "evaluation": evaluation_result,
            "execution": execution_result,
            "reporting": reporting_result,
            "status": "completed",
            "events": self.events
        }
    
    def _create_deal(self) -> Dict[str, Any]:
        """Create a deal based on parameters.
        
        Returns:
            Deal creation result
        """
        # Implementation for deal creation
        # In a full implementation, this would create a deal
        pass
    
    def _evaluate_deal(self, creation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the created deal.
        
        Args:
            creation_result: Deal creation result
            
        Returns:
            Deal evaluation result
        """
        # Implementation for deal evaluation
        # In a full implementation, this would evaluate the deal
        pass
    
    def _execute_deal(self, evaluation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the evaluated deal.
        
        Args:
            evaluation_result: Deal evaluation result
            
        Returns:
            Deal execution result
        """
        # Implementation for deal execution
        # In a full implementation, this would execute the deal
        pass
    
    def _generate_report(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a report for the executed deal.
        
        Args:
            execution_result: Deal execution result
            
        Returns:
            Deal reporting result
        """
        # Implementation for report generation
        # In a full implementation, this would generate reports
        pass
    
    def cleanup(self) -> None:
        """Clean up resources after scenario execution."""
        # Implementation for cleanup
        pass

class ScenarioManager:
    """Manages demo scenarios."""
    
    def __init__(self, github_service, visualization, logger, config):
        """Initialize the scenario manager.
        
        Args:
            github_service: GitHub service instance
            visualization: Visualization engine instance
            logger: Demo logger instance
            config: Configuration parameters
        """
        self.github_service = github_service
        self.visualization = visualization
        self.logger = logger
        self.config = config
        self.active_scenarios = {}
        
        self.logger.info("Scenario Manager initialized")
    
    def create_scenario(self, scenario_type: str, parameters: Dict[str, Any]) -> DemoScenario:
        """Create a new demo scenario.
        
        Args:
            scenario_type: Type of scenario to create
            parameters: Scenario-specific parameters
            
        Returns:
            Initialized scenario instance
            
        Raises:
            ValueError: If scenario type is invalid
        """
        self.logger.info(f"Creating scenario of type: {scenario_type}")
        
        if scenario_type == "github_issue":
            scenario = GitHubIssueScenario(
                github_service=self.github_service,
                visualization=self.visualization,
                logger=self.logger,
                parameters=parameters
            )
        elif scenario_type == "deal_monitoring":
            scenario = DealMonitoringScenario(
                github_service=self.github_service,
                visualization=self.visualization,
                logger=self.logger,
                parameters=parameters
            )
        else:
            raise ValueError(f"Invalid scenario type: {scenario_type}")
        
        # Initialize the scenario
        success = scenario.initialize()
        if not success:
            self.logger.error(f"Failed to initialize scenario of type: {scenario_type}")
            raise RuntimeError(f"Failed to initialize scenario of type: {scenario_type}")
        
        # Store active scenario
        scenario_id = f"{scenario_type}-{uuid.uuid4().hex[:8]}"
        self.active_scenarios[scenario_id] = scenario
        
        self.logger.info(f"Scenario created with ID: {scenario_id}")
        
        return scenario
    
    def get_scenario(self, scenario_id: str) -> Optional[DemoScenario]:
        """Get an active scenario by ID.
        
        Args:
            scenario_id: Scenario ID
            
        Returns:
            Scenario instance or None if not found
        """
        return self.active_scenarios.get(scenario_id)
    
    def cleanup(self) -> None:
        """Clean up all active scenarios."""
        self.logger.info(f"Cleaning up {len(self.active_scenarios)} active scenarios")
        
        for scenario_id, scenario in self.active_scenarios.items():
            try:
                scenario.cleanup()
                self.logger.info(f"Cleaned up scenario: {scenario_id}")
            except Exception as e:
                self.logger.error(f"Error cleaning up scenario {scenario_id}: {str(e)}")
        
        self.active_scenarios = {}
        self.logger.info("Scenario cleanup complete")
```

### 3. GitHub Service

The GitHub Service interfaces with GitHub to manage issues:

```python
# demo/github.py

import requests
import logging
from typing import Dict, List, Any, Optional

class GitHubService:
    """Service for interacting with GitHub."""
    
    def __init__(self, github_token: str, repository: str, logger):
        """Initialize the GitHub service.
        
        Args:
            github_token: GitHub API token
            repository: Repository in format 'owner/repo'
            logger: Logger instance
        """
        self.github_token = github_token
        self.repository = repository
        self.logger = logger
        self.api_base_url = "https://api.github.com"
        
        self.logger.info(f"GitHub Service initialized for repository: {repository}")
    
    def get_issue(self, issue_number: str) -> Optional[Dict[str, Any]]:
        """Get a specific GitHub issue.
        
        Args:
            issue_number: Issue number
            
        Returns:
            Issue data or None if not found
        """
        url = f"{self.api_base_url}/repos/{self.repository}/issues/{issue_number}"
        
        try:
            response = self._make_github_request("GET", url)
            return response
        except Exception as e:
            self.logger.error(f"Error getting issue {issue_number}: {str(e)}")
            return None
    
    def get_open_issues(self, labels: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Get open GitHub issues.
        
        Args:
            labels: Optional list of labels to filter by
            
        Returns:
            List of open issues
        """
        url = f"{self.api_base_url}/repos/{self.repository}/issues"
        params = {"state": "open"}
        
        if labels:
            params["labels"] = ",".join(labels)
        
        try:
            response = self._make_github_request("GET", url, params=params)
            return response if response else []
        except Exception as e:
            self.logger.error(f"Error getting open issues: {str(e)}")
            return []
    
    def create_comment(self, issue_number: str, comment: str) -> Optional[Dict[str, Any]]:
        """Create a comment on a GitHub issue.
        
        Args:
            issue_number: Issue number
            comment: Comment text
            
        Returns:
            Comment data or None if failed
        """
        url = f"{self.api_base_url}/repos/{self.repository}/issues/{issue_number}/comments"
        payload = {"body": comment}
        
        try:
            response = self._make_github_request("POST", url, json=payload)
            return response
        except Exception as e:
            self.logger.error(f"Error creating comment on issue {issue_number}: {str(e)}")
            return None
    
    def close_issue(self, issue_number: str, comment: Optional[str] = None) -> bool:
        """Close a GitHub issue.
        
        Args:
            issue_number: Issue number
            comment: Optional comment to add before closing
            
        Returns:
            True if successful, False otherwise
        """
        # Add comment if provided
        if comment:
            self.create_comment(issue_number, comment)
        
        # Close the issue
        url = f"{self.api_base_url}/repos/{self.repository}/issues/{issue_number}"
        payload = {"state": "closed"}
        
        try:
            response = self._make_github_request("PATCH", url, json=payload)
            return response is not None and response.get("state") == "closed"
        except Exception as e:
            self.logger.error(f"Error closing issue {issue_number}: {str(e)}")
            return False
    
    def _make_github_request(self, method: str, url: str, **kwargs) -> Any:
        """Make a request to the GitHub API.
        
        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional request parameters
            
        Returns:
            Response data
            
        Raises:
            Exception: If request fails
        """
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                **kwargs
            )
            
            response.raise_for_status()
            
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"GitHub API request failed: {str(e)}")
            raise
```

### 4. Visualization Engine

The Visualization Engine creates visualizations of the demo:

```python
# demo/visualization.py

import os
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import networkx as nx

class VisualizationEngine:
    """Engine for creating visualizations of demo scenarios."""
    
    def __init__(self, output_dir: str, session_id: str, logger):
        """Initialize the visualization engine.
        
        Args:
            output_dir: Directory for output files
            session_id: Demo session ID
            logger: Logger instance
        """
        self.output_dir = output_dir
        self.session_id = session_id
        self.logger = logger
        self.visualization_data = {}
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        self.logger.info(f"Visualization Engine initialized with output directory: {output_dir}")
    
    def generate_scenario_visualization(self, scenario, result: Dict[str, Any]) -> str:
        """Generate visualization for a scenario.
        
        Args:
            scenario: Scenario instance
            result: Scenario execution result
            
        Returns:
            URL to the visualization
        """
        self.logger.info(f"Generating visualization for scenario: {type(scenario).__name__}")
        
        # Create a unique ID for this visualization
        visualization_id = f"vis-{uuid.uuid4().hex[:8]}"
        
        # Store scenario data
        self.visualization_data[visualization_id] = {
            "scenario_type": type(scenario).__name__,
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        
        # Generate visualizations based on scenario type
        if isinstance(scenario, GitHubIssueScenario):
            return self._generate_github_issue_visualization(visualization_id, result)
        elif isinstance(scenario, DealMonitoringScenario):
            return self._generate_deal_monitoring_visualization(visualization_id, result)
        else:
            self.logger.warning(f"Unknown scenario type for visualization: {type(scenario).__name__}")
            return self._generate_generic_visualization(visualization_id, result)
    
    def _generate_github_issue_visualization(self, visualization_id: str, result: Dict[str, Any]) -> str:
        """Generate visualization for GitHub issue scenario.
        
        Args:
            visualization_id: Visualization ID
            result: Scenario execution result
            
        Returns:
            URL to the visualization
        """
        # Output file paths
        output_dir = os.path.join(self.output_dir, visualization_id)
        os.makedirs(output_dir, exist_ok=True)
        
        agent_graph_path = os.path.join(output_dir, "agent_graph.png")
        timeline_path = os.path.join(output_dir, "timeline.png")
        cort_path = os.path.join(output_dir, "cort_reasoning.png")
        data_path = os.path.join(output_dir, "data.json")
        html_path = os.path.join(output_dir, "index.html")
        
        # Generate agent interaction graph
        self._generate_agent_interaction_graph(result, agent_graph_path)
        
        # Generate timeline visualization
        self._generate_timeline_visualization(result["events"], timeline_path)
        
        # Generate CoRT visualization if available
        if "collaboration" in result and "cort_reasoning" in result["collaboration"]:
            self._generate_cort_visualization(result["collaboration"]["cort_reasoning"], cort_path)
        
        # Save full data as JSON
        with open(data_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        # Generate HTML dashboard
        self._generate_html_dashboard(
            visualization_id=visualization_id,
            scenario_type="GitHub Issue Resolution",
            result=result,
            output_path=html_path,
            artifact_paths={
                "agent_graph": os.path.basename(agent_graph_path),
                "timeline": os.path.basename(timeline_path),
                "cort": os.path.basename(cort_path) if "collaboration" in result and "cort_reasoning" in result["collaboration"] else None,
                "data": os.path.basename(data_path)
            }
        )
        
        return html_path
    
    def _generate_deal_monitoring_visualization(self, visualization_id: str, result: Dict[str, Any]) -> str:
        """Generate visualization for deal monitoring scenario.
        
        Args:
            visualization_id: Visualization ID
            result: Scenario execution result
            
        Returns:
            URL to the visualization
        """
        # Implementation for deal monitoring visualization
        # Similar to GitHub issue visualization with deal-specific graphs
        pass
    
    def _generate_generic_visualization(self, visualization_id: str, result: Dict[str, Any]) -> str:
        """Generate generic visualization for any scenario.
        
        Args:
            visualization_id: Visualization ID
            result: Scenario execution result
            
        Returns:
            URL to the visualization
        """
        # Implementation for generic visualization
        pass
    
    def _generate_agent_interaction_graph(self, result: Dict[str, Any], output_path: str) -> None:
        """Generate agent interaction graph visualization.
        
        Args:
            result: Scenario execution result
            output_path: Output file path
        """
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes for all agents involved
        agents = set()
        if "assignment" in result and "assigned_agents" in result["assignment"]:
            agents.update(result["assignment"]["assigned_agents"])
        
        # Add supervisor node
        agents.add("Supervisor")
        
        # Add nodes to graph
        for agent in agents:
            G.add_node(agent)
        
        # Add edges for interactions
        interactions = []
        for event in result.get("events", []):
            if event["type"] == "agent_interaction":
                source = event["details"].get("source")
                target = event["details"].get("target")
                if source and target and source in agents and target in agents:
                    interactions.append((source, target))
        
        # Add unique interactions to graph
        for source, target in set(interactions):
            G.add_edge(source, target)
        
        # Create the visualization
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue", alpha=0.8)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color="gray", arrows=True, arrowsize=20)
        
        # Add labels
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
        
        plt.title("Agent Interaction Graph", fontsize=16)
        plt.axis("off")
        
        # Save the figure
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
    
    def _generate_timeline_visualization(self, events: List[Dict[str, Any]], output_path: str) -> None:
        """Generate timeline visualization.
        
        Args:
            events: List of scenario events
            output_path: Output file path
        """
        # Group events by type
        event_types = {}
        for i, event in enumerate(events):
            event_type = event["type"]
            if event_type not in event_types:
                event_types[event_type] = []
            event_types[event_type].append((i, event))
        
        # Create the visualization
        plt.figure(figsize=(14, 8))
        
        # Plot each event type
        y_pos = 0
        for event_type, type_events in event_types.items():
            y_pos += 1
            for i, event in type_events:
                timestamp = datetime.fromisoformat(event["timestamp"])
                plt.scatter(timestamp, y_pos, c="blue", s=100, alpha=0.7)
                plt.text(timestamp, y_pos + 0.1, str(i), fontsize=8, ha="center")
        
        # Set y-axis labels
        plt.yticks(range(1, len(event_types) + 1), list(event_types.keys()))
        
        # Format x-axis as time
        plt.gcf().autofmt_xdate()
        
        plt.title("Scenario Timeline", fontsize=16)
        plt.xlabel("Timestamp", fontsize=12)
        plt.ylabel("Event Type", fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Save the figure
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
    
    def _generate_cort_visualization(self, cort_reasoning: Dict[str, Any], output_path: str) -> None:
        """Generate CoRT reasoning visualization.
        
        Args:
            cort_reasoning: CoRT reasoning data
            output_path: Output file path
        """
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes for all thoughts
        thoughts = {}
        for round_id, round_data in cort_reasoning.get("rounds", {}).items():
            for thought_id, thought in round_data.get("thoughts", {}).items():
                node_id = f"{round_id}_{thought_id}"
                thoughts[node_id] = thought
                G.add_node(node_id, round=round_id, thought=thought_id)
        
        # Add edges between thoughts
        for round_id, round_data in cort_reasoning.get("rounds", {}).items():
            for thought_id, thought in round_data.get("thoughts", {}).items():
                node_id = f"{round_id}_{thought_id}"
                
                # Add edge from parent thought
                if "parent_thought" in thought:
                    parent_id = thought["parent_thought"]
                    parent_round = thought.get("parent_round", str(int(round_id) - 1))
                    parent_node_id = f"{parent_round}_{parent_id}"
                    
                    if parent_node_id in thoughts:
                        G.add_edge(parent_node_id, node_id)
        
        # Create the visualization
        plt.figure(figsize=(14, 10))
        
        # Use hierarchical layout
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
        
        # Group nodes by round
        rounds = {}
        for node, data in G.nodes(data=True):
            round_id = data["round"]
            if round_id not in rounds:
                rounds[round_id] = []
            rounds[round_id].append(node)
        
        # Draw nodes by round with different colors
        colors = plt.cm.viridis(np.linspace(0, 1, len(rounds)))
        for i, (round_id, nodes) in enumerate(rounds.items()):
            nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=1500, node_color=[colors[i]] * len(nodes), alpha=0.8, label=f"Round {round_id}")
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color="gray", arrows=True, arrowsize=20)
        
        # Add labels
        labels = {node: f"{data['thought']}" for node, data in G.nodes(data=True)}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)
        
        plt.title("Chain of Recursive Thoughts (CoRT)", fontsize=16)
        plt.axis("off")
        plt.legend()
        
        # Save the figure
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
    
    def _generate_html_dashboard(self, visualization_id: str, scenario_type: str, result: Dict[str, Any], output_path: str, artifact_paths: Dict[str, str]) -> None:
        """Generate HTML dashboard.
        
        Args:
            visualization_id: Visualization ID
            scenario_type: Scenario type
            result: Scenario execution result
            output_path: Output file path
            artifact_paths: Paths to visualization artifacts
        """
        # Generate HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>HMS Agent System Demo - {scenario_type}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1, h2, h3 {{
                    color: #333;
                }}
                .status {{
                    display: inline-block;
                    padding: 5px 10px;
                    border-radius: 3px;
                    color: white;
                    font-weight: bold;
                }}
                .status-success {{
                    background-color: #28a745;
                }}
                .status-failure {{
                    background-color: #dc3545;
                }}
                .visualization {{
                    margin-top: 20px;
                    margin-bottom: 30px;
                }}
                .visualization img {{
                    max-width: 100%;
                    height: auto;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }}
                .details {{
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-radius: 5px;
                    margin-top: 20px;
                }}
                .tabs {{
                    display: flex;
                    margin-bottom: 10px;
                }}
                .tab {{
                    padding: 10px 15px;
                    background-color: #eee;
                    cursor: pointer;
                    border-radius: 5px 5px 0 0;
                    margin-right: 5px;
                }}
                .tab.active {{
                    background-color: #f9f9f9;
                    font-weight: bold;
                }}
                .tab-content {{
                    display: none;
                }}
                .tab-content.active {{
                    display: block;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                table, th, td {{
                    border: 1px solid #ddd;
                }}
                th, td {{
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>HMS Agent System Demo</h1>
                <h2>{scenario_type}</h2>
                
                <div>
                    <p><strong>Session ID:</strong> {self.session_id}</p>
                    <p><strong>Visualization ID:</strong> {visualization_id}</p>
                    <p><strong>Status:</strong> <span class="status {'status-success' if result.get('status') == 'resolved' or result.get('status') == 'completed' else 'status-failure'}">{result.get('status', 'Unknown')}</span></p>
                </div>
                
                <div class="tabs">
                    <div class="tab active" onclick="switchTab('agent-graph')">Agent Interaction</div>
                    <div class="tab" onclick="switchTab('timeline')">Timeline</div>
                    {'<div class="tab" onclick="switchTab(\'cort\')">CoRT Reasoning</div>' if artifact_paths.get('cort') else ''}
                    <div class="tab" onclick="switchTab('details')">Details</div>
                    <div class="tab" onclick="switchTab('raw-data')">Raw Data</div>
                </div>
                
                <div id="agent-graph" class="tab-content active">
                    <div class="visualization">
                        <h3>Agent Interaction Graph</h3>
                        <img src="{artifact_paths['agent_graph']}" alt="Agent Interaction Graph">
                    </div>
                </div>
                
                <div id="timeline" class="tab-content">
                    <div class="visualization">
                        <h3>Scenario Timeline</h3>
                        <img src="{artifact_paths['timeline']}" alt="Scenario Timeline">
                    </div>
                </div>
                
                {'<div id="cort" class="tab-content"><div class="visualization"><h3>Chain of Recursive Thoughts (CoRT)</h3><img src="' + artifact_paths['cort'] + '" alt="CoRT Reasoning"></div></div>' if artifact_paths.get('cort') else ''}
                
                <div id="details" class="tab-content">
                    <div class="details">
                        <h3>Scenario Details</h3>
                        
                        <!-- Display details based on scenario type -->
                        {'<h4>Issue Information</h4><p><strong>Issue:</strong> #' + str(result['issue']['number']) + ' - ' + result['issue']['title'] + '</p>' if 'issue' in result else ''}
                        {'<h4>Deal Information</h4><p><strong>Deal ID:</strong> ' + result.get('deal_id', 'N/A') + '</p>' if 'deal_id' in result else ''}
                        
                        <!-- Display event table -->
                        <h4>Events</h4>
                        <table>
                            <thead>
                                <tr>
                                    <th>Timestamp</th>
                                    <th>Event Type</th>
                                    <th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join(['<tr><td>' + event['timestamp'] + '</td><td>' + event['type'] + '</td><td>' + str(event['details']) + '</td></tr>' for event in result.get('events', [])])}
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div id="raw-data" class="tab-content">
                    <div class="details">
                        <h3>Raw Data</h3>
                        <p>Download the full data: <a href="{artifact_paths['data']}" download>data.json</a></p>
                        <pre id="json-display" style="background-color: #f8f8f8; padding: 10px; max-height: 500px; overflow: auto;"></pre>
                    </div>
                </div>
            </div>
            
            <script>
                // Tab switching
                function switchTab(tabId) {{
                    // Hide all tab contents
                    var tabContents = document.getElementsByClassName('tab-content');
                    for (var i = 0; i < tabContents.length; i++) {{
                        tabContents[i].classList.remove('active');
                    }}
                    
                    // Deactivate all tabs
                    var tabs = document.getElementsByClassName('tab');
                    for (var i = 0; i < tabs.length; i++) {{
                        tabs[i].classList.remove('active');
                    }}
                    
                    // Activate the selected tab
                    document.getElementById(tabId).classList.add('active');
                    
                    // Activate the clicked tab button
                    var tabButtons = document.getElementsByClassName('tab');
                    for (var i = 0; i < tabButtons.length; i++) {{
                        if (tabButtons[i].innerHTML.toLowerCase().includes(tabId)) {{
                            tabButtons[i].classList.add('active');
                        }}
                    }}
                    
                    // Load JSON data if raw-data tab is selected
                    if (tabId === 'raw-data') {{
                        fetch('{artifact_paths['data']}')
                            .then(response => response.json())
                            .then(data => {{
                                document.getElementById('json-display').textContent = JSON.stringify(data, null, 2);
                            }});
                    }}
                }}
            </script>
        </body>
        </html>
        """
        
        # Write HTML content to file
        with open(output_path, 'w') as f:
            f.write(html_content)
    
    def cleanup(self) -> None:
        """Clean up resources."""
        self.logger.info("Visualization Engine cleanup complete")
```

### 5. Demo Logger

The Demo Logger provides detailed logging for the demo:

```python
# demo/logger.py

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class DemoLogger:
    """Logger for demo scenarios."""
    
    def __init__(self, log_dir: str, session_id: str):
        """Initialize the demo logger.
        
        Args:
            log_dir: Directory for log files
            session_id: Demo session ID
        """
        self.log_dir = log_dir
        self.session_id = session_id
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(f"demo_logger_{session_id}")
        self.logger.setLevel(logging.DEBUG)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(sessionid)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Create file handler
        log_file = os.path.join(log_dir, f"demo_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        # Add default extra
        self.extra = {'sessionid': session_id}
        
        self.info(f"Demo Logger initialized for session {session_id}")
    
    def debug(self, message: str, extra: dict = None) -> None:
        """Log a debug message.
        
        Args:
            message: Message to log
            extra: Additional log information
        """
        self._log(logging.DEBUG, message, extra)
    
    def info(self, message: str, extra: dict = None) -> None:
        """Log an info message.
        
        Args:
            message: Message to log
            extra: Additional log information
        """
        self._log(logging.INFO, message, extra)
    
    def warning(self, message: str, extra: dict = None) -> None:
        """Log a warning message.
        
        Args:
            message: Message to log
            extra: Additional log information
        """
        self._log(logging.WARNING, message, extra)
    
    def error(self, message: str, extra: dict = None) -> None:
        """Log an error message.
        
        Args:
            message: Message to log
            extra: Additional log information
        """
        self._log(logging.ERROR, message, extra)
    
    def critical(self, message: str, extra: dict = None) -> None:
        """Log a critical message.
        
        Args:
            message: Message to log
            extra: Additional log information
        """
        self._log(logging.CRITICAL, message, extra)
    
    def _log(self, level: int, message: str, extra: dict = None) -> None:
        """Log a message at the specified level.
        
        Args:
            level: Log level
            message: Message to log
            extra: Additional log information
        """
        log_extra = self.extra.copy()
        if extra:
            log_extra.update(extra)
        
        self.logger.log(level, message, extra=log_extra)
```

## Command-Line Interface

The Command-Line Interface provides a way to run the demo:

```python
# demo_cli.py

import argparse
import json
import os
from demo.orchestrator import DemoOrchestrator

def main():
    """Main entry point for demo CLI."""
    parser = argparse.ArgumentParser(description="HMS Agent System Demo")
    parser.add_argument("--mode", choices=["github", "deal"], default="github", help="Demo mode")
    parser.add_argument("--issue", help="GitHub issue number (for GitHub mode)")
    parser.add_argument("--deal-file", help="JSON file with deal parameters (for Deal mode)")
    parser.add_argument("--github-token", help="GitHub API token")
    parser.add_argument("--github-repo", help="GitHub repository in format 'owner/repo'")
    parser.add_argument("--log-dir", default="./logs", help="Log directory")
    parser.add_argument("--visualization-dir", default="./visualizations", help="Visualization directory")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--slow", action="store_true", help="Run in slow motion with pauses")
    parser.add_argument("--interactive", action="store_true", help="Allow user interaction at key points")
    parser.add_argument("--save-logs", action="store_true", help="Save all logs for later analysis")
    
    args = parser.parse_args()
    
    # Set up configuration
    config = {
        "github_token": args.github_token or os.environ.get("GITHUB_TOKEN"),
        "github_repository": args.github_repo or os.environ.get("GITHUB_REPOSITORY"),
        "log_dir": args.log_dir,
        "visualization_dir": args.visualization_dir,
        "verbose": args.verbose,
        "slow_mode": args.slow,
        "interactive": args.interactive,
        "save_logs": args.save_logs
    }
    
    # Check required parameters
    if not config["github_token"]:
        print("Error: GitHub token is required. Use --github-token or set GITHUB_TOKEN environment variable.")
        return 1
    
    if not config["github_repository"]:
        print("Error: GitHub repository is required. Use --github-repo or set GITHUB_REPOSITORY environment variable.")
        return 1
    
    if args.mode == "deal" and not args.deal_file:
        print("Error: Deal file is required for deal mode. Use --deal-file.")
        return 1
    
    # Initialize orchestrator
    orchestrator = DemoOrchestrator(config)
    
    try:
        # Run appropriate demo
        if args.mode == "github":
            result = orchestrator.run_github_issue_demo(args.issue)
            print(f"\nGitHub Issue Resolution Demo completed with status: {result['result']['status']}")
            print(f"Visualization available at: {result['visualization_url']}")
        elif args.mode == "deal":
            # Load deal parameters from file
            with open(args.deal_file, 'r') as f:
                deal_parameters = json.load(f)
            
            result = orchestrator.run_deal_monitoring_demo(deal_parameters)
            print(f"\nDeal Monitoring Demo completed with status: {result['result']['status']}")
            print(f"Visualization available at: {result['visualization_url']}")
    finally:
        # Cleanup
        orchestrator.shutdown()
    
    return 0

if __name__ == "__main__":
    exit(main())
```

## Running the Demo

The demo can be executed using the following command:

```bash
# Run the GitHub issue resolution demo
python demo_cli.py --mode github --issue 42

# Run the deal monitoring demo
python demo_cli.py --mode deal --deal-file ./deal_parameters.json
```

Alternatively, the demo can be launched using the HMS agent conversation script:

```bash
./agents-conversation.sh --demo github-issue
```

## Demo Output

The demo produces the following outputs:

1. **Console Output**: Real-time status updates and progress information
2. **Log Files**: Detailed logs of all demo activities
3. **Visualizations**: Interactive HTML dashboard with visualizations of agent interactions, timelines, and CoRT reasoning
4. **JSON Data**: Raw data from the demo execution for further analysis

## Integration with HMS-A2A

The demo integrates with HMS-A2A for agent orchestration and communication:

```python
# demo/agent_system.py

from hms_a2a.registry import AgentRegistry
from hms_a2a.collaboration import CollaborationSession
from hms_a2a.cort import CoRTFramework

class AgentSystem:
    """Interface to the HMS-A2A agent system."""
    
    def __init__(self, config: Dict[str, Any], logger):
        """Initialize the agent system.
        
        Args:
            config: Configuration parameters
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        
        # Initialize agent registry
        self.registry = AgentRegistry()
        
        # Initialize component agents
        self.agents = self._initialize_agents()
        
        self.logger.info(f"Agent System initialized with {len(self.agents)} agents")
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize component agents.
        
        Returns:
            Dict mapping agent IDs to agent instances
        """
        agents = {}
        
        # Initialize HMS-DEV agent
        agents["dev"] = self.registry.create_agent(
            agent_type="government",
            component="HMS-DEV",
            name="Development Tools"
        )
        
        # Initialize HMS-DOC agent
        agents["doc"] = self.registry.create_agent(
            agent_type="government",
            component="HMS-DOC",
            name="Documentation"
        )
        
        # Initialize HMS-API agent
        agents["api"] = self.registry.create_agent(
            agent_type="government",
            component="HMS-API",
            name="API Services"
        )
        
        # Initialize HMS-A2A agent
        agents["a2a"] = self.registry.create_agent(
            agent_type="government",
            component="HMS-A2A",
            name="Agent-to-Agent Protocol"
        )
        
        # Initialize HMS-CDF agent
        agents["cdf"] = self.registry.create_agent(
            agent_type="government",
            component="HMS-CDF",
            name="Codified Democracy Foundation"
        )
        
        return agents
    
    def create_collaboration_session(self, topic: str, affected_components: List[str]) -> str:
        """Create a collaboration session.
        
        Args:
            topic: Collaboration topic
            affected_components: Components affected by the collaboration
            
        Returns:
            Session ID
        """
        self.logger.info(f"Creating collaboration session for topic: {topic}")
        
        # Create session
        session = CollaborationSession(
            topic=topic,
            affected_components=affected_components
        )
        
        # Register session with registry
        session_id = self.registry.register_session(session)
        
        self.logger.info(f"Collaboration session created with ID: {session_id}")
        
        return session_id
    
    def coordinate_solution_planning(self, session_id: str, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate solution planning for an issue.
        
        Args:
            session_id: Collaboration session ID
            issue: Issue data
            
        Returns:
            Solution plan
        """
        self.logger.info(f"Coordinating solution planning for session: {session_id}")
        
        # Get session
        session = self.registry.get_session(session_id)
        if not session:
            raise ValueError(f"Invalid session ID: {session_id}")
        
        # Create planning task
        planning_task = {
            "type": "solution_planning",
            "issue": issue,
            "session_id": session_id
        }
        
        # Assign planning task to affected agents
        agent_plans = {}
        for component in session.affected_components:
            agent_id = self._component_to_agent_id(component)
            if agent_id in self.agents:
                self.logger.info(f"Requesting solution plan from agent: {agent_id}")
                agent_plans[agent_id] = self.agents[agent_id].process_task(planning_task)
        
        # Create CoRT framework for solution synthesis
        cort = CoRTFramework(
            name="SolutionPlanning",
            max_rounds=3,
            alternatives_per_round=3
        )
        
        # Use CoRT to synthesize solution plan
        solution_plan = cort.solve_problem({
            "type": "plan_synthesis",
            "agent_plans": agent_plans,
            "issue": issue
        })
        
        self.logger.info(f"Solution planning complete for session: {session_id}")
        
        return solution_plan
    
    def coordinate_implementation(self, session_id: str, solution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate solution implementation.
        
        Args:
            session_id: Collaboration session ID
            solution_plan: Solution plan
            
        Returns:
            Implementation result
        """
        self.logger.info(f"Coordinating solution implementation for session: {session_id}")
        
        # Get session
        session = self.registry.get_session(session_id)
        if not session:
            raise ValueError(f"Invalid session ID: {session_id}")
        
        # Assign implementation tasks to agents
        implementation_results = {}
        for task in solution_plan.get("tasks", []):
            assigned_agent = task.get("assigned_to")
            agent_id = self._component_to_agent_id(assigned_agent)
            
            if agent_id in self.agents:
                self.logger.info(f"Assigning implementation task to agent: {agent_id}")
                implementation_results[task["id"]] = self.agents[agent_id].process_task({
                    "type": "implementation",
                    "task": task,
                    "session_id": session_id
                })
        
        # Combine implementation results
        implementation_result = {
            "tasks": solution_plan.get("tasks", []),
            "results": implementation_results,
            "status": "completed" if all(result.get("status") == "success" for result in implementation_results.values()) else "failed",
            "summary": self._generate_implementation_summary(implementation_results)
        }
        
        self.logger.info(f"Solution implementation complete for session: {session_id} with status: {implementation_result['status']}")
        
        return implementation_result
    
    def verify_implementation(self, session_id: str, implementation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Verify solution implementation.
        
        Args:
            session_id: Collaboration session ID
            implementation_result: Implementation result
            
        Returns:
            Verification result
        """
        self.logger.info(f"Verifying implementation for session: {session_id}")
        
        # Get session
        session = self.registry.get_session(session_id)
        if not session:
            raise ValueError(f"Invalid session ID: {session_id}")
        
        # Create verification task
        verification_task = {
            "type": "verification",
            "implementation_result": implementation_result,
            "session_id": session_id
        }
        
        # Assign verification task to DEV agent
        verification_result = self.agents["dev"].process_task(verification_task)
        
        self.logger.info(f"Implementation verification complete for session: {session_id} with status: {verification_result.get('verified', False)}")
        
        return verification_result
    
    def handle_verification_failure(self, session_id: str, verification_result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle verification failure.
        
        Args:
            session_id: Collaboration session ID
            verification_result: Verification result
            
        Returns:
            Failure handling result
        """
        self.logger.info(f"Handling verification failure for session: {session_id}")
        
        # Get session
        session = self.registry.get_session(session_id)
        if not session:
            raise ValueError(f"Invalid session ID: {session_id}")
        
        # Create failure handling task
        failure_task = {
            "type": "verification_failure",
            "verification_result": verification_result,
            "session_id": session_id
        }
        
        # Assign failure handling task to DEV agent
        failure_result = self.agents["dev"].process_task(failure_task)
        
        self.logger.info(f"Verification failure handling complete for session: {session_id}")
        
        return failure_result
    
    def _component_to_agent_id(self, component: str) -> str:
        """Convert component name to agent ID.
        
        Args:
            component: Component name
            
        Returns:
            Agent ID
        """
        # Convert HMS-XXX to xxx
        if component.startswith("HMS-"):
            return component[4:].lower()
        
        return component.lower()
    
    def _generate_implementation_summary(self, implementation_results: Dict[str, Any]) -> str:
        """Generate implementation summary.
        
        Args:
            implementation_results: Implementation results
            
        Returns:
            Implementation summary
        """
        # Create a summary of the implementation
        total_tasks = len(implementation_results)
        successful_tasks = sum(1 for result in implementation_results.values() if result.get("status") == "success")
        
        summary = f"Implementation completed with {successful_tasks}/{total_tasks} tasks successful."
        
        if successful_tasks < total_tasks:
            failed_tasks = [task_id for task_id, result in implementation_results.items() if result.get("status") != "success"]
            summary += f" Failed tasks: {', '.join(failed_tasks)}"
        
        return summary
```

## Conclusion

The HMS Agent System Demo Mode Implementation provides a comprehensive way to showcase the capabilities of the system-wide agent architecture. By demonstrating how component agents collaborate to identify, analyze, and resolve real-world issues, the demo illustrates the power of agent-based systems for complex problem-solving.

The demo highlights key features of the HMS Agent System:

1. **Intelligent Agent Collaboration**: Multiple agents working together to solve complex problems
2. **Chain of Recursive Thoughts (CoRT)**: Advanced reasoning for complex decision-making
3. **Verification-First Approach**: Ensuring solution correctness through rigorous validation
4. **Visualization and Transparency**: Clear visual representation of agent activities
5. **Integrated Workflows**: End-to-end management of issues from detection to resolution

This implementation serves as both a practical demonstration of the system's capabilities and a reference implementation for future agent-based systems.