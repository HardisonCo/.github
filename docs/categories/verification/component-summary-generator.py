#!/usr/bin/env python3
"""
HMS Component Summary Generator

This script generates comprehensive summary documents for HMS components including:
1. Component information from repository analysis
2. Operational status from the status tracker
3. Recent test results
4. Integration points
5. Work items for self-optimization

If a component fails to start or tests don't pass, it automatically creates
work tickets for other agents to help resolve the issues.
"""

import os
import json
import sys
import time
import datetime
import argparse
import subprocess
from typing import Dict, List, Any, Optional, Tuple, Union

# Add parent directory to path to allow importing status_tracker
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

# Import status tracker
try:
    from status_tracker import (
        get_available_components,
        get_component_status,
        get_component_summary,
        print_header,
        print_success,
        print_error,
        print_info,
        print_warning,
        Colors
    )
except ImportError:
    print("Error: status_tracker.py module not found. Please ensure it exists in the same directory.")
    sys.exit(1)

# Constants
SUMMARY_DIR = os.path.join(SCRIPT_DIR, "summaries")
REPO_LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "codex-cli/repo_analysis_logs")

def ensure_directories() -> None:
    """Ensure all required directories exist."""
    os.makedirs(SUMMARY_DIR, exist_ok=True)

def load_component_data(component: str) -> Dict[str, Any]:
    """Load analysis data for a specific component."""
    summary_file = os.path.join(REPO_LOGS_DIR, f"{component}_summary.json")
    commit_file = os.path.join(REPO_LOGS_DIR, f"{component}_last_commit.txt")
    
    data = {
        "summary": {},
        "last_commit": ""
    }
    
    # Load summary data if available
    if os.path.exists(summary_file):
        try:
            with open(summary_file, 'r') as f:
                data["summary"] = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print_warning(f"Error loading summary for {component}: {e}")
    
    # Load last commit if available
    if os.path.exists(commit_file):
        try:
            with open(commit_file, 'r') as f:
                data["last_commit"] = f.read().strip()
        except IOError as e:
            print_warning(f"Error loading last commit for {component}: {e}")
    
    return data

def generate_component_summary(component: str) -> Dict[str, Any]:
    """
    Generate a comprehensive summary for a component.
    
    Args:
        component: Component ID (e.g., "HMS-API")
        
    Returns:
        Dict: The generated summary
    """
    # Get component status
    status = get_component_status(component)
    status_summary = get_component_summary(component)
    
    # Load repository analysis data
    repo_data = load_component_data(component)
    
    # Build the summary
    summary = {
        "component": component,
        "generated_at": datetime.datetime.now().isoformat(),
        "operational_status": status["operational_status"],
        "repository": {
            "last_commit": repo_data["last_commit"],
            "description": extract_component_description(repo_data),
            "tech_stack": extract_tech_stack(repo_data),
            "integration_points": extract_integration_points(repo_data),
            "architecture": extract_architecture(repo_data)
        },
        "status": {
            "last_start": status["start"]["last_success"],
            "start_attempts": status["start"]["attempts"],
            "start_successes": status["start"]["successes"],
            "start_failures": status["start"]["failures"],
            "last_test_run": status["tests"]["last_run"],
            "test_runs": status["tests"]["total_runs"],
            "test_passes": status["tests"]["total_passed"],
            "test_failures": status["tests"]["total_failed"],
            "last_test_results": status["tests"]["last_results"]
        },
        "issues": extract_active_issues(status),
        "work_items": []
    }
    
    # Add work items if needed
    work_items = generate_work_items(component, status, repo_data)
    if work_items:
        summary["work_items"] = work_items
    
    return summary

def extract_component_description(repo_data: Dict[str, Any]) -> str:
    """Extract component description from repository data."""
    try:
        body = repo_data["summary"].get("body", {})
        context = body.get("context", {})
        return context.get("description", "No description available")
    except (KeyError, AttributeError):
        return "No description available"

def extract_tech_stack(repo_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract tech stack information from repository data."""
    tech_stack = {
        "languages": [],
        "frameworks": [],
        "databases": [],
        "key_libraries": []
    }
    
    try:
        body = repo_data["summary"].get("body", {})
        context = body.get("context", {})
        tech_data = context.get("tech_stack", {})
        
        for key in tech_stack:
            if key in tech_data:
                tech_stack[key] = tech_data[key]
    except (KeyError, AttributeError):
        pass
    
    return tech_stack

def extract_integration_points(repo_data: Dict[str, Any]) -> List[str]:
    """Extract integration points from repository data."""
    try:
        body = repo_data["summary"].get("body", {})
        context = body.get("context", {})
        return context.get("integration_points", [])
    except (KeyError, AttributeError):
        return []

def extract_architecture(repo_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract architecture information from repository data."""
    architecture = {
        "pattern": "unknown",
        "key_dirs": [],
        "entry_points": []
    }
    
    try:
        body = repo_data["summary"].get("body", {})
        structure = body.get("structure", {})
        
        architecture["pattern"] = structure.get("architecture_pattern", "unknown")
        architecture["key_dirs"] = structure.get("domain_dirs", [])
        architecture["entry_points"] = structure.get("entrypoints", [])
    except (KeyError, AttributeError):
        pass
    
    return architecture

def extract_active_issues(status: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract active issues from component status."""
    active_issues = []
    
    for issue in status.get("issues", []):
        if issue.get("status") == "open":
            active_issues.append(issue)
    
    return active_issues

def generate_work_items(component: str, status: Dict[str, Any], repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate work items for self-optimization."""
    work_items = []
    
    # Check for start failures
    if status["start"]["status"] == "failed":
        work_items.append({
            "type": "start_failure",
            "priority": "high",
            "description": f"Fix {component} startup failure",
            "assigned_to": "HMS-DEV",
            "suggested_actions": [
                f"Check {component} logs for error messages",
                f"Verify all dependencies for {component} are available",
                "Check environment variables and configuration"
            ]
        })
    
    # Check for test failures
    if status["tests"]["status"] == "failing":
        work_items.append({
            "type": "test_failure",
            "priority": "medium",
            "description": f"Fix failing tests for {component}",
            "assigned_to": component.replace("HMS-", "HMS-AGT-"),
            "suggested_actions": [
                "Review failing tests",
                "Check for recent code changes",
                "Verify test environment"
            ]
        })
    
    # Check for missing integration tests
    integration_points = extract_integration_points(repo_data)
    if integration_points and status["tests"]["total_runs"] > 0:
        # This is a simplified check - a real implementation would have more sophisticated analysis
        work_items.append({
            "type": "enhancement",
            "priority": "low",
            "description": f"Add integration tests for {component} with {', '.join(integration_points)}",
            "assigned_to": component.replace("HMS-", "HMS-AGT-"),
            "suggested_actions": [
                f"Develop integration tests for {component} with its integration points",
                "Set up test fixtures for integration testing",
                "Add CI configuration for integration tests"
            ]
        })
    
    return work_items

def save_component_summary(component: str, summary: Dict[str, Any]) -> str:
    """
    Save a component summary to a file.
    
    Args:
        component: Component ID (e.g., "HMS-API")
        summary: The component summary
        
    Returns:
        str: Path to the saved summary file
    """
    # Format date for filename
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    
    # Create filename
    filename = f"{component}_summary_{date_str}.json"
    file_path = os.path.join(SUMMARY_DIR, filename)
    
    # Save the summary
    with open(file_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Also save a "latest" version
    latest_path = os.path.join(SUMMARY_DIR, f"{component}_summary_latest.json")
    with open(latest_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print_success(f"Summary saved to {file_path}")
    return file_path

def generate_markdown_summary(component: str, summary: Dict[str, Any]) -> str:
    """
    Generate a Markdown summary document for a component.
    
    Args:
        component: Component ID (e.g., "HMS-API")
        summary: The component summary
        
    Returns:
        str: Markdown content
    """
    # Format timestamp
    generated_at = "Unknown"
    try:
        dt = datetime.datetime.fromisoformat(summary["generated_at"])
        generated_at = dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        pass
    
    # Format operational status
    status = summary["operational_status"]
    if status == "operational":
        status_icon = "✅"
    elif status == "degraded":
        status_icon = "⚠️"
    elif status == "offline":
        status_icon = "❌"
    else:
        status_icon = "❓"
    
    # Format last start
    last_start = "Never"
    if summary["status"]["last_start"]:
        try:
            dt = datetime.datetime.fromisoformat(summary["status"]["last_start"])
            last_start = dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            pass
    
    # Format last test run
    last_test = "Never"
    if summary["status"]["last_test_run"]:
        try:
            dt = datetime.datetime.fromisoformat(summary["status"]["last_test_run"])
            last_test = dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            pass
    
    # Build Markdown content
    md = f"""# {component} Component Summary

*Generated at: {generated_at}*

## Status Overview

**Current Status:** {status_icon} {status.capitalize()}

### Runtime Status
- **Last Successful Start:** {last_start}
- **Start Success Rate:** {summary["status"]["start_successes"]}/{summary["status"]["start_attempts"]} ({calculate_percentage(summary["status"]["start_successes"], summary["status"]["start_attempts"])}%)

### Test Status
- **Last Test Run:** {last_test}
- **Test Success Rate:** {summary["status"]["test_passes"]}/{summary["status"]["test_runs"]} ({calculate_percentage(summary["status"]["test_passes"], summary["status"]["test_runs"])}%)

## Component Information

**Description:** 
{summary["repository"]["description"]}

**Latest Commit:** {summary["repository"]["last_commit"] or "Unknown"}

### Technology Stack
- **Languages:** {", ".join(summary["repository"]["tech_stack"]["languages"]) or "Unknown"}
- **Frameworks:** {", ".join(summary["repository"]["tech_stack"]["frameworks"]) or "None"}
- **Databases:** {", ".join(summary["repository"]["tech_stack"]["databases"]) or "None"}
- **Key Libraries:** {", ".join(summary["repository"]["tech_stack"]["key_libraries"]) or "None"}

### Architecture
- **Pattern:** {summary["repository"]["architecture"]["pattern"]}
- **Key Directories:** {", ".join(summary["repository"]["architecture"]["key_dirs"]) or "Unknown"}

### Integration Points
{format_integration_points(summary["repository"]["integration_points"])}

"""
    
    # Add issues section if there are active issues
    if summary["issues"]:
        md += "## Active Issues\n\n"
        for i, issue in enumerate(summary["issues"], 1):
            issue_time = "Unknown"
            try:
                dt = datetime.datetime.fromisoformat(issue["timestamp"])
                issue_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                pass
            
            md += f"### Issue {i}: {issue['type']}\n"
            md += f"- **Opened:** {issue_time}\n"
            md += f"- **Status:** {issue['status']}\n"
            
            if "details" in issue:
                md += "- **Details:**\n"
                for key, value in issue["details"].items():
                    if isinstance(value, dict) or isinstance(value, list):
                        md += f"  - **{key}:** {json.dumps(value)}\n"
                    else:
                        md += f"  - **{key}:** {value}\n"
            
            md += "\n"
    
    # Add work items section if there are work items
    if summary["work_items"]:
        md += "## Work Items for Self-Optimization\n\n"
        for i, item in enumerate(summary["work_items"], 1):
            md += f"### Work Item {i}: {item['description']}\n"
            md += f"- **Type:** {item['type']}\n"
            md += f"- **Priority:** {item['priority']}\n"
            md += f"- **Assigned To:** {item['assigned_to']}\n"
            
            if "suggested_actions" in item:
                md += "- **Suggested Actions:**\n"
                for action in item["suggested_actions"]:
                    md += f"  - {action}\n"
            
            md += "\n"
    
    return md

def calculate_percentage(part: int, total: int) -> float:
    """Calculate percentage with handling for zero division."""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 1)

def format_integration_points(integration_points: List[str]) -> str:
    """Format integration points for Markdown display."""
    if not integration_points:
        return "No integration points defined."
    
    md = ""
    for point in integration_points:
        md += f"- {point}\n"
    
    return md

def save_markdown_summary(component: str, markdown: str) -> str:
    """
    Save a Markdown summary to a file.
    
    Args:
        component: Component ID (e.g., "HMS-API")
        markdown: The Markdown content
        
    Returns:
        str: Path to the saved Markdown file
    """
    # Format date for filename
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    
    # Create filename
    filename = f"{component}_summary_{date_str}.md"
    file_path = os.path.join(SUMMARY_DIR, filename)
    
    # Save the Markdown
    with open(file_path, 'w') as f:
        f.write(markdown)
    
    # Also save a "latest" version
    latest_path = os.path.join(SUMMARY_DIR, f"{component}_summary_latest.md")
    with open(latest_path, 'w') as f:
        f.write(markdown)
    
    print_success(f"Markdown summary saved to {file_path}")
    return file_path

def generate_summaries_for_all_components() -> None:
    """Generate summaries for all available components."""
    components = get_available_components()
    print_header(f"Generating summaries for {len(components)} components")
    
    for component in components:
        print_info(f"Generating summary for {component}...")
        try:
            summary = generate_component_summary(component)
            save_component_summary(component, summary)
            
            markdown = generate_markdown_summary(component, summary)
            save_markdown_summary(component, markdown)
            
            print_success(f"Summary for {component} completed")
        except Exception as e:
            print_error(f"Error generating summary for {component}: {e}")
    
    print_header("Summary generation complete")

def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="HMS Component Summary Generator")
    parser.add_argument("--component", "-c", help="Specific component to generate summary for")
    parser.add_argument("--all", "-a", action="store_true", help="Generate summaries for all components")
    args = parser.parse_args()
    
    # Ensure directories exist
    ensure_directories()
    
    if args.all:
        generate_summaries_for_all_components()
    elif args.component:
        print_header(f"Generating summary for {args.component}")
        try:
            summary = generate_component_summary(args.component)
            save_component_summary(args.component, summary)
            
            markdown = generate_markdown_summary(args.component, summary)
            save_markdown_summary(args.component, markdown)
            
            print_success(f"Summary for {args.component} completed")
        except Exception as e:
            print_error(f"Error generating summary for {args.component}: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)