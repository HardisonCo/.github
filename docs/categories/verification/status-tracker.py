#!/usr/bin/env python3
"""
HMS Component Status Tracker

This script tracks the status of HMS components, including:
1. Last start time
2. Last test run time and results
3. Current operational status

If components fail to start or tests don't run successfully, it:
1. Logs the issues
2. Generates work tickets for HMS-DEV or other relevant agents
3. Facilitates self-optimization of the HMS ecosystem
"""

import os
import json
import time
import subprocess
import datetime
import uuid
import argparse
import sys
from typing import Dict, List, Any, Optional, Tuple, Union

# Constants
STATUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "status")
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
WORK_TICKETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "work_tickets")
REPO_LOGS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    "../../codex-cli/repo_analysis_logs"
)

# Status file format version
STATUS_VERSION = "1.0"

# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

def print_header(text: str) -> None:
    """Print a formatted header."""
    print("\n" + Colors.BOLD + Colors.BLUE + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + Colors.RESET + "\n")

def print_success(text: str) -> None:
    """Print a success message."""
    print(Colors.GREEN + "✓ " + text + Colors.RESET)

def print_error(text: str) -> None:
    """Print an error message."""
    print(Colors.RED + "✗ " + text + Colors.RESET)

def print_info(text: str) -> None:
    """Print an info message."""
    print(Colors.CYAN + "ℹ " + text + Colors.RESET)

def print_warning(text: str) -> None:
    """Print a warning message."""
    print(Colors.YELLOW + "⚠ " + text + Colors.RESET)

def ensure_directories() -> None:
    """Ensure all required directories exist."""
    for directory in [STATUS_DIR, LOGS_DIR, WORK_TICKETS_DIR]:
        os.makedirs(directory, exist_ok=True)

def get_available_components() -> List[str]:
    """Get a list of components with analysis data available or all known components."""
    # Start with a comprehensive list of all known HMS components
    all_known_components = [
        "HMS-A2A",  # Agent-to-Agent
        "HMS-ABC",  # Accountability Based Coverage
        "HMS-ACH",  # Automated Clearing House
        "HMS-ACT",  # Activity
        "HMS-AGT",  # Agent
        "HMS-AGX",  # Agent Extensions
        "HMS-API",  # API
        "HMS-CDF",  # Component Definition Framework
        "HMS-CUR",  # Currency
        "HMS-DEV",  # Development
        "HMS-DOC",  # Documentation
        "HMS-DTA",  # Data
        "HMS-EDU",  # Education
        "HMS-EHR",  # Electronic Health Records
        "HMS-EMR",  # Electronic Medical Records
        "HMS-ESQ",  # Enterprise Service Queue
        "HMS-ESR",  # Enterprise Service Registry
        "HMS-ETL",  # Extract Transform Load
        "HMS-FLD",  # Field
        "HMS-GOV",  # Government
        "HMS-LLM",  # Large Language Model
        "HMS-MBL",  # Mobile
        "HMS-MCP",  # Model Context Protocol
        "HMS-MED",  # Medical
        "HMS-MFE",  # Micro Frontend
        "HMS-MKT",  # Marketing
        "HMS-NFO",  # Information
        "HMS-OMS",  # Order Management System
        "HMS-OPS",  # Operations
        "HMS-RED",  # Reduction
        "HMS-SCM",  # Supply Chain Management
        "HMS-SKL",  # Skills
        "HMS-SME",  # Subject Matter Expertise
        "HMS-SVC",  # Service
        "HMS-SYS",  # System
        "HMS-UHC",  # Universal Health Coverage
        "HMS-UTL",  # Utilities
    ]
    
    # Try to find components with repository analysis data
    repo_components = []
    try:
        summary_files = [f for f in os.listdir(REPO_LOGS_DIR) if f.endswith("_summary.json")]
        
        for file_name in summary_files:
            # Extract component name from file path
            component = file_name.split("_summary.json")[0]
            
            # Check if there's a corresponding last_commit file
            commit_file = os.path.join(REPO_LOGS_DIR, f"{component}_last_commit.txt")
            if os.path.exists(commit_file):
                repo_components.append(component)
    except FileNotFoundError:
        print_warning(f"Repository logs directory not found: {REPO_LOGS_DIR}")
    
    # Combine both lists, ensuring no duplicates
    combined_components = list(set(all_known_components + repo_components))
    
    return combined_components

def get_status_file_path(component: str) -> str:
    """Get the path to a component's status file."""
    return os.path.join(STATUS_DIR, f"{component}_status.json")

def get_component_status(component: str) -> Dict[str, Any]:
    """Get the current status of a component."""
    status_file = get_status_file_path(component)
    
    if os.path.exists(status_file):
        try:
            with open(status_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print_warning(f"Invalid status file for {component}. Creating new status.")
    
    # Create a new status object if none exists
    return {
        "component": component,
        "version": STATUS_VERSION,
        "created_at": datetime.datetime.now().isoformat(),
        "last_updated": datetime.datetime.now().isoformat(),
        "start": {
            "last_attempt": None,
            "last_success": None,
            "attempts": 0,
            "successes": 0,
            "failures": 0,
            "status": "unknown"
        },
        "tests": {
            "last_run": None,
            "last_success": None,
            "total_runs": 0,
            "total_passed": 0,
            "total_failed": 0,
            "status": "unknown",
            "last_results": {}
        },
        "issues": [],
        "operational_status": "unknown"
    }

def update_component_status(component: str, status: Dict[str, Any]) -> None:
    """Update a component's status file."""
    status_file = get_status_file_path(component)
    
    # Update the last_updated timestamp
    status["last_updated"] = datetime.datetime.now().isoformat()
    
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=2)

def record_component_start(component: str, success: bool, output: str = None) -> Dict[str, Any]:
    """
    Record a component start attempt.
    
    Args:
        component: Component ID (e.g., "HMS-API")
        success: Whether the start was successful
        output: Optional output from the start attempt
        
    Returns:
        Dict: The updated status object
    """
    # Get current status
    status = get_component_status(component)
    
    # Update start information
    status["start"]["last_attempt"] = datetime.datetime.now().isoformat()
    status["start"]["attempts"] += 1
    
    if success:
        status["start"]["last_success"] = datetime.datetime.now().isoformat()
        status["start"]["successes"] += 1
        status["start"]["status"] = "running"
        print_success(f"{component} started successfully")
    else:
        status["start"]["failures"] += 1
        status["start"]["status"] = "failed"
        print_error(f"{component} failed to start")
        
        # Log the issue
        issue_id = str(uuid.uuid4())
        issue = {
            "id": issue_id,
            "type": "start_failure",
            "component": component,
            "timestamp": datetime.datetime.now().isoformat(),
            "details": {
                "output": output
            },
            "status": "open"
        }
        status["issues"].append(issue)
        
        # Generate a work ticket if this is a new failure or repeated failure
        if status["start"]["failures"] > status["start"]["successes"]:
            generate_work_ticket(component, "start_failure", issue)
    
    # Update operational status
    update_operational_status(status)
    
    # Save the updated status
    update_component_status(component, status)
    
    return status

def record_test_run(component: str, success: bool, results: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Record the results of a test run.
    
    Args:
        component: Component ID (e.g., "HMS-API")
        success: Whether all tests passed
        results: Test results data
        
    Returns:
        Dict: The updated status object
    """
    # Get current status
    status = get_component_status(component)
    
    # Update test information
    now = datetime.datetime.now().isoformat()
    status["tests"]["last_run"] = now
    status["tests"]["total_runs"] += 1
    
    # Initialize results object if none provided
    if results is None:
        results = {"passed": 0, "failed": 0, "skipped": 0}
    
    if success:
        status["tests"]["last_success"] = now
        status["tests"]["total_passed"] += 1
        status["tests"]["status"] = "passing"
        print_success(f"{component} tests passed successfully")
    else:
        status["tests"]["total_failed"] += 1
        status["tests"]["status"] = "failing"
        print_error(f"{component} tests failed")
        
        # Log the issue
        issue_id = str(uuid.uuid4())
        issue = {
            "id": issue_id,
            "type": "test_failure",
            "component": component,
            "timestamp": now,
            "details": {
                "results": results
            },
            "status": "open"
        }
        status["issues"].append(issue)
        
        # Generate a work ticket if tests are consistently failing
        if status["tests"]["total_failed"] > status["tests"]["total_passed"]:
            generate_work_ticket(component, "test_failure", issue)
    
    # Save the test results
    status["tests"]["last_results"] = results
    
    # Update operational status
    update_operational_status(status)
    
    # Save the updated status
    update_component_status(component, status)
    
    return status

def update_operational_status(status: Dict[str, Any]) -> None:
    """Update the overall operational status based on start and test status."""
    start_status = status["start"]["status"]
    test_status = status["tests"]["status"]
    
    if start_status == "unknown" or test_status == "unknown":
        status["operational_status"] = "unknown"
    elif start_status == "failed":
        status["operational_status"] = "offline"
    elif test_status == "failing":
        status["operational_status"] = "degraded"
    elif start_status == "running" and test_status == "passing":
        status["operational_status"] = "operational"
    else:
        status["operational_status"] = "degraded"

def generate_work_ticket(component: str, issue_type: str, issue: Dict[str, Any]) -> str:
    """
    Generate a work ticket for HMS-DEV or other agents to resolve an issue.
    
    Args:
        component: Component ID (e.g., "HMS-API")
        issue_type: Type of issue (e.g., "start_failure", "test_failure")
        issue: Issue data
        
    Returns:
        str: The ID of the created work ticket
    """
    # Determine which agent is responsible for this component
    assigned_agent = determine_responsible_agent(component, issue_type)
    
    # Create the work ticket
    ticket_id = f"WRK-{uuid.uuid4().hex[:8]}"
    now = datetime.datetime.now().isoformat()
    
    ticket = {
        "id": ticket_id,
        "component": component,
        "issue_id": issue["id"],
        "issue_type": issue_type,
        "created_at": now,
        "updated_at": now,
        "assigned_to": assigned_agent,
        "status": "open",
        "priority": determine_priority(component, issue_type, issue),
        "details": {
            "component": component,
            "issue": issue,
            "description": generate_ticket_description(component, issue_type, issue),
            "suggested_actions": generate_suggested_actions(component, issue_type, issue)
        }
    }
    
    # Save the work ticket
    ticket_file = os.path.join(WORK_TICKETS_DIR, f"{ticket_id}.json")
    with open(ticket_file, 'w') as f:
        json.dump(ticket, f, indent=2)
    
    print_info(f"Generated work ticket {ticket_id} for {component} ({issue_type}) assigned to {assigned_agent}")
    
    # Notify the assigned agent (in a real implementation, this would use the MCP to send a message)
    notify_agent_about_ticket(assigned_agent, ticket_id, ticket)
    
    return ticket_id

def determine_responsible_agent(component: str, issue_type: str) -> str:
    """Determine which agent is responsible for handling this issue."""
    # In a more sophisticated implementation, this would use component relationships
    # and expertise data to identify the most appropriate agent
    
    # Default assignments based on issue type
    if issue_type == "start_failure":
        return "HMS-DEV"  # Development and operations team handles start issues
    elif issue_type == "test_failure":
        # For test failures, assign to the component's own agent if it exists
        component_agent = component.replace("HMS-", "HMS-AGT-")
        return component_agent
    
    # Default fallback
    return "HMS-DEV"

def determine_priority(component: str, issue_type: str, issue: Dict[str, Any]) -> str:
    """Determine the priority of a work ticket based on the issue details."""
    # In a more sophisticated implementation, this would use rules based on
    # component criticality, issue history, and dependencies
    
    # Simple priority rules
    if issue_type == "start_failure":
        return "high"  # Start failures are always high priority
    elif issue_type == "test_failure":
        # Test failures depend on how many tests failed
        results = issue.get("details", {}).get("results", {})
        failed = results.get("failed", 0)
        total = failed + results.get("passed", 0) + results.get("skipped", 0)
        
        if total > 0 and failed / total > 0.5:
            return "high"  # More than 50% of tests failing
        else:
            return "medium"
    
    # Default priority
    return "medium"

def generate_ticket_description(component: str, issue_type: str, issue: Dict[str, Any]) -> str:
    """Generate a description for a work ticket."""
    if issue_type == "start_failure":
        return f"The {component} component failed to start. This is affecting the operational status of the HMS ecosystem and should be resolved as soon as possible."
    elif issue_type == "test_failure":
        results = issue.get("details", {}).get("results", {})
        failed = results.get("failed", 0)
        total = failed + results.get("passed", 0) + results.get("skipped", 0)
        
        if total > 0:
            return f"Tests for {component} are failing ({failed}/{total} tests failed). This may indicate issues with recent changes or integration problems."
        else:
            return f"Tests for {component} failed to run properly. This may indicate configuration or dependency issues."
    
    return f"Issue detected with {component}: {issue_type}"

def generate_suggested_actions(component: str, issue_type: str, issue: Dict[str, Any]) -> List[str]:
    """Generate suggested actions for resolving an issue."""
    if issue_type == "start_failure":
        return [
            f"Check the {component} logs for error messages",
            f"Verify all dependencies for {component} are available and correctly configured",
            "Check for recent changes that might have affected the component's ability to start",
            "Verify environment variables and configuration files"
        ]
    elif issue_type == "test_failure":
        return [
            f"Review failing tests for {component}",
            "Check for recent code changes that might have broken tests",
            "Verify test environment and fixtures",
            "Check for integration issues with dependent components",
            "Run tests with verbose output to diagnose specific failures"
        ]
    
    return ["Investigate the issue", "Check component logs", "Review recent changes"]

def notify_agent_about_ticket(agent: str, ticket_id: str, ticket: Dict[str, Any]) -> None:
    """Notify an agent about a new work ticket."""
    # In a real implementation, this would use MCP to send a message to the agent
    print_info(f"Notifying {agent} about ticket {ticket_id}")
    
    # For now, we'll just log that a notification would be sent
    log_file = os.path.join(LOGS_DIR, "notifications.log")
    
    with open(log_file, 'a') as f:
        f.write(f"{datetime.datetime.now().isoformat()} - Notified {agent} about {ticket_id} ({ticket['component']} - {ticket['issue_type']})\n")

def get_component_summary(component: str) -> Dict[str, Any]:
    """Get a summary of a component's status for display."""
    status = get_component_status(component)
    
    # Calculate operational uptime percentage
    start_attempts = status["start"]["attempts"]
    start_successes = status["start"]["successes"]
    start_percentage = (start_successes / start_attempts * 100) if start_attempts > 0 else 0
    
    test_runs = status["tests"]["total_runs"]
    test_passed = status["tests"]["total_passed"]
    test_percentage = (test_passed / test_runs * 100) if test_runs > 0 else 0
    
    return {
        "component": component,
        "operational_status": status["operational_status"],
        "last_start_attempt": status["start"]["last_attempt"],
        "last_start_success": status["start"]["last_success"],
        "start_success_rate": f"{start_percentage:.1f}%",
        "last_test_run": status["tests"]["last_run"],
        "last_test_success": status["tests"]["last_success"],
        "test_success_rate": f"{test_percentage:.1f}%",
        "open_issues": sum(1 for issue in status["issues"] if issue["status"] == "open"),
        "last_updated": status["last_updated"]
    }

def display_status_table(components: List[str]) -> None:
    """Display a table of component statuses."""
    print_header("HMS Component Status Summary")
    
    # Print table header
    print(f"{'Component':<15} {'Status':<12} {'Last Start':<20} {'Start Rate':<10} {'Last Test':<20} {'Test Rate':<10}")
    print(f"{'-'*15} {'-'*12} {'-'*20} {'-'*10} {'-'*20} {'-'*10}")
    
    for component in sorted(components):
        summary = get_component_summary(component)
        
        # Format dates
        last_start = "Never"
        if summary["last_start_success"]:
            try:
                dt = datetime.datetime.fromisoformat(summary["last_start_success"])
                last_start = dt.strftime("%Y-%m-%d %H:%M")
            except (ValueError, TypeError):
                pass
        
        last_test = "Never"
        if summary["last_test_success"]:
            try:
                dt = datetime.datetime.fromisoformat(summary["last_test_success"])
                last_test = dt.strftime("%Y-%m-%d %H:%M")
            except (ValueError, TypeError):
                pass
        
        # Colorize status
        status = summary["operational_status"]
        if status == "operational":
            status_str = Colors.GREEN + status + Colors.RESET
        elif status == "degraded":
            status_str = Colors.YELLOW + status + Colors.RESET
        elif status == "offline":
            status_str = Colors.RED + status + Colors.RESET
        else:
            status_str = Colors.CYAN + status + Colors.RESET
        
        print(f"{component:<15} {status_str:<22} {last_start:<20} {summary['start_success_rate']:<10} {last_test:<20} {summary['test_success_rate']:<10}")

def generate_system_health_report() -> Dict[str, Any]:
    """Generate a comprehensive system health report."""
    components = get_available_components()
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_components": len(components),
        "operational": 0,
        "degraded": 0,
        "offline": 0,
        "unknown": 0,
        "component_status": {},
        "open_issues": 0,
        "recent_starts": 0,
        "recent_test_runs": 0,
        "system_health_score": 0.0,
        "recommendations": []
    }
    
    # 24 hours ago
    recent_threshold = datetime.datetime.now() - datetime.timedelta(hours=24)
    recent_threshold_iso = recent_threshold.isoformat()
    
    for component in components:
        status = get_component_status(component)
        summary = get_component_summary(component)
        
        # Count by operational status
        if status["operational_status"] == "operational":
            report["operational"] += 1
        elif status["operational_status"] == "degraded":
            report["degraded"] += 1
        elif status["operational_status"] == "offline":
            report["offline"] += 1
        else:
            report["unknown"] += 1
        
        # Add component status to report
        report["component_status"][component] = {
            "status": status["operational_status"],
            "last_start": status["start"]["last_success"],
            "last_test": status["tests"]["last_success"],
            "open_issues": sum(1 for issue in status["issues"] if issue["status"] == "open")
        }
        
        # Count open issues
        report["open_issues"] += sum(1 for issue in status["issues"] if issue["status"] == "open")
        
        # Count recent activities
        if status["start"]["last_attempt"] and status["start"]["last_attempt"] > recent_threshold_iso:
            report["recent_starts"] += 1
        
        if status["tests"]["last_run"] and status["tests"]["last_run"] > recent_threshold_iso:
            report["recent_test_runs"] += 1
    
    # Calculate system health score (0-100)
    if len(components) > 0:
        operational_weight = 0.5
        degraded_weight = 0.3
        activity_weight = 0.2
        
        operational_score = (report["operational"] / len(components)) * 100
        degraded_score = (report["degraded"] / len(components)) * 50  # Degraded is half as good as operational
        
        # Activity score based on recent actions
        activity_score = ((report["recent_starts"] + report["recent_test_runs"]) / (len(components) * 2)) * 100
        
        health_score = (
            operational_weight * operational_score +
            degraded_weight * degraded_score +
            activity_weight * activity_score
        )
        
        report["system_health_score"] = round(health_score, 1)
    
    # Generate recommendations
    if report["offline"] > 0:
        report["recommendations"].append(f"Prioritize starting {report['offline']} offline components")
    
    if report["degraded"] > 0:
        report["recommendations"].append(f"Investigate and fix issues with {report['degraded']} degraded components")
    
    if report["recent_test_runs"] < len(components) / 2:
        report["recommendations"].append("Run tests for components that haven't been tested recently")
    
    if report["open_issues"] > 0:
        report["recommendations"].append(f"Address {report['open_issues']} open issues")
    
    return report

def display_health_report(report: Dict[str, Any]) -> None:
    """Display the system health report."""
    print_header("HMS System Health Report")
    
    # Format timestamp
    timestamp = "Unknown"
    try:
        dt = datetime.datetime.fromisoformat(report["timestamp"])
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        pass
    
    print(f"Report generated: {timestamp}")
    print(f"Total components: {report['total_components']}")
    print("")
    
    # Component status summary
    print(f"Operational: {report['operational']} components")
    print(f"Degraded: {report['degraded']} components")
    print(f"Offline: {report['offline']} components")
    print(f"Unknown: {report['unknown']} components")
    print("")
    
    # Activity summary
    print(f"Components started in last 24h: {report['recent_starts']}")
    print(f"Components tested in last 24h: {report['recent_test_runs']}")
    print(f"Open issues: {report['open_issues']}")
    print("")
    
    # Health score
    health_score = report["system_health_score"]
    if health_score >= 80:
        print(f"System Health Score: {Colors.GREEN}{health_score}/100{Colors.RESET}")
    elif health_score >= 50:
        print(f"System Health Score: {Colors.YELLOW}{health_score}/100{Colors.RESET}")
    else:
        print(f"System Health Score: {Colors.RED}{health_score}/100{Colors.RESET}")
    print("")
    
    # Recommendations
    if report["recommendations"]:
        print("Recommendations:")
        for i, recommendation in enumerate(report["recommendations"], 1):
            print(f"  {i}. {recommendation}")
    else:
        print("No recommendations at this time.")

def save_health_report(report: Dict[str, Any]) -> str:
    """Save the health report to a file."""
    # Format date for filename
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    
    # Create filename with timestamp
    filename = f"health_report_{date_str}.json"
    file_path = os.path.join(LOGS_DIR, filename)
    
    # Save the report
    with open(file_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print_info(f"Health report saved to {file_path}")
    return file_path

def run_component_tests(component: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Run tests for a specific component.
    
    Args:
        component: Component ID (e.g., "HMS-API")
        
    Returns:
        Tuple[bool, Dict]: (success, test_results)
    """
    print_info(f"Running tests for {component}...")
    
    # This is a simulation - in a real implementation, this would
    # execute the component's test suite using the appropriate command
    
    # Simulation: 80% chance of success
    import random
    success = random.random() < 0.8
    
    # Generate simulated test results
    if success:
        results = {
            "passed": random.randint(10, 50),
            "failed": 0,
            "skipped": random.randint(0, 5),
            "duration": random.uniform(0.5, 10.0)
        }
    else:
        # Failed test run
        total_tests = random.randint(15, 55)
        failed = random.randint(1, min(total_tests, 10))
        results = {
            "passed": total_tests - failed,
            "failed": failed,
            "skipped": random.randint(0, 5),
            "duration": random.uniform(0.5, 10.0),
            "failure_details": [
                f"Test failure in {component.lower()}/tests/test_{random.choice(['api', 'core', 'integration', 'models'])}.py"
                for _ in range(failed)
            ]
        }
    
    print_info(f"Test results: {results['passed']} passed, {results['failed']} failed, {results['skipped']} skipped")
    return success, results

def start_component(component: str) -> Tuple[bool, str]:
    """
    Start a specific component.
    
    Args:
        component: Component ID (e.g., "HMS-API")
        
    Returns:
        Tuple[bool, str]: (success, output)
    """
    print_info(f"Starting {component}...")
    
    # This is a simulation - in a real implementation, this would
    # execute the component's start command
    
    # Simulation: 90% chance of success
    import random
    success = random.random() < 0.9
    
    # Generate simulated output
    if success:
        output = f"{component} started successfully on port {random.randint(3000, 9000)}"
    else:
        failures = [
            f"ERROR: Could not connect to dependency {random.choice(['database', 'redis', 'elasticsearch', 'HMS-SYS'])}",
            f"ERROR: Port {random.randint(3000, 9000)} already in use",
            f"ERROR: Configuration file not found: {component.lower()}/config/production.json",
            f"ERROR: Missing environment variable: {component.replace('-', '_')}_API_KEY"
        ]
        output = random.choice(failures)
    
    print_info(f"Start output: {output}")
    return success, output

def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="HMS Component Status Tracker")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show component status")
    status_parser.add_argument("--component", "-c", help="Specific component to show status for")
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Record a component start")
    start_parser.add_argument("component", help="Component ID (e.g., HMS-API)")
    start_parser.add_argument("--success", action="store_true", help="Mark as successful start")
    start_parser.add_argument("--fail", action="store_true", help="Mark as failed start")
    start_parser.add_argument("--output", help="Output from the start attempt")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Record a test run")
    test_parser.add_argument("component", help="Component ID (e.g., HMS-API)")
    test_parser.add_argument("--success", action="store_true", help="Mark as successful test run")
    test_parser.add_argument("--fail", action="store_true", help="Mark as failed test run")
    test_parser.add_argument("--results", help="JSON string with test results")
    
    # Simulate command
    simulate_parser = subparsers.add_parser("simulate", help="Simulate component start and test")
    simulate_parser.add_argument("component", help="Component ID (e.g., HMS-API)")
    
    # Health command
    health_parser = subparsers.add_parser("health", help="Generate system health report")
    health_parser.add_argument("--save", action="store_true", help="Save the report to a file")
    
    args = parser.parse_args()
    
    # Ensure directories exist
    ensure_directories()
    
    if args.command == "status":
        if args.component:
            # Show status for a specific component
            status = get_component_status(args.component)
            print(json.dumps(status, indent=2))
        else:
            # Show status table for all components
            components = get_available_components()
            display_status_table(components)
    
    elif args.command == "start":
        if args.success and args.fail:
            print_error("Cannot specify both --success and --fail")
            sys.exit(1)
        
        success = True if args.success else False if args.fail else None
        
        if success is None:
            print_error("Must specify either --success or --fail")
            sys.exit(1)
        
        record_component_start(args.component, success, args.output)
    
    elif args.command == "test":
        if args.success and args.fail:
            print_error("Cannot specify both --success and --fail")
            sys.exit(1)
        
        success = True if args.success else False if args.fail else None
        
        if success is None:
            print_error("Must specify either --success or --fail")
            sys.exit(1)
        
        results = None
        if args.results:
            try:
                results = json.loads(args.results)
            except json.JSONDecodeError:
                print_error("Invalid JSON for test results")
                sys.exit(1)
        
        record_test_run(args.component, success, results)
    
    elif args.command == "simulate":
        # Simulate starting the component
        success, output = start_component(args.component)
        record_component_start(args.component, success, output)
        
        # If component started successfully, simulate running tests
        if success:
            test_success, test_results = run_component_tests(args.component)
            record_test_run(args.component, test_success, test_results)
    
    elif args.command == "health":
        # Generate and display health report
        report = generate_system_health_report()
        display_health_report(report)
        
        if args.save:
            save_health_report(report)
    
    else:
        # Default action: show status for all components
        components = get_available_components()
        display_status_table(components)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)