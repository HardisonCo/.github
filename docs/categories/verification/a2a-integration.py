#!/usr/bin/env python3
"""
HMS A2A MCP Integration for Verification and Status Tracking

This script integrates the verification system and status tracking with the A2A MCP
framework, enabling agents to:

1. Verify themselves for specific components
2. Track component status
3. Generate component summaries
4. Create and handle work tickets for self-optimization
5. Test and report on component functionality

This provides a centralized interface for agent-to-agent interactions around
component status and verification.
"""

import os
import sys
import json
import time
import datetime
import argparse
import subprocess
from typing import Dict, List, Any, Optional, Tuple, Union

# Add verification directory to the path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

# Try to import verification modules
try:
    from mcp_verification_adapter import (
        check_verification,
        verify_agent,
        block_if_unverified
    )
except ImportError:
    print("Warning: mcp_verification_adapter.py not found. Verification functions will be limited.")
    
    def check_verification(agent_id: str, component: str = None) -> Dict[str, Any]:
        return {"success": False, "error": "mcp_verification_adapter.py not available"}
    
    def verify_agent(agent_id: str, component: str = None) -> Dict[str, Any]:
        return {"success": False, "error": "mcp_verification_adapter.py not available"}
    
    def block_if_unverified(agent_id: str, component: str, operation: str) -> Dict[str, Any]:
        return {"success": False, "error": "mcp_verification_adapter.py not available"}

# Try to import status tracking modules
try:
    from status_tracker import (
        get_component_status,
        record_component_start,
        record_test_run,
        Colors,
        print_header,
        print_success,
        print_error,
        print_info,
        print_warning
    )
except ImportError:
    print("Warning: status_tracker.py not found. Status tracking functions will be limited.")
    
    def get_component_status(component: str) -> Dict[str, Any]:
        return {"component": component, "operational_status": "unknown"}
    
    def record_component_start(component: str, success: bool, output: str = None) -> Dict[str, Any]:
        return {"component": component, "success": success}
    
    def record_test_run(component: str, success: bool, results: Dict[str, Any] = None) -> Dict[str, Any]:
        return {"component": component, "success": success}
    
    class Colors:
        RESET = ""
        BOLD = ""
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
    
    def print_header(text: str) -> None: print(text)
    def print_success(text: str) -> None: print(text)
    def print_error(text: str) -> None: print(text)
    def print_info(text: str) -> None: print(text)
    def print_warning(text: str) -> None: print(text)

# Try to import summary generator modules
try:
    from component_summary_generator import (
        generate_component_summary,
        generate_markdown_summary,
        save_component_summary,
        save_markdown_summary
    )
except ImportError:
    print("Warning: component_summary_generator.py not found. Summary functions will be limited.")
    
    def generate_component_summary(component: str) -> Dict[str, Any]:
        return {"component": component, "error": "component_summary_generator.py not available"}
    
    def generate_markdown_summary(component: str, summary: Dict[str, Any]) -> str:
        return f"# {component}\n\nSummary generation not available."
    
    def save_component_summary(component: str, summary: Dict[str, Any]) -> str:
        return ""
    
    def save_markdown_summary(component: str, markdown: str) -> str:
        return ""

# Constants
API_VERSION = "1.0"
WORK_TICKETS_DIR = os.path.join(SCRIPT_DIR, "work_tickets")
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")

# Ensure directories exist
os.makedirs(WORK_TICKETS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

def handle_api_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle an API request from the A2A MCP system.
    
    Args:
        request: The API request object
        
    Returns:
        Dict: The API response
    """
    # Extract request data
    api_version = request.get("api_version", "1.0")
    action = request.get("action", "")
    params = request.get("params", {})
    timestamp = request.get("timestamp", time.time())
    
    # Log the request
    log_api_request(action, params)
    
    # Process the request
    if action == "check_verification":
        response = handle_check_verification(params)
    elif action == "verify_agent":
        response = handle_verify_agent(params)
    elif action == "block_if_unverified":
        response = handle_block_if_unverified(params)
    elif action == "record_component_start":
        response = handle_record_start(params)
    elif action == "record_test_run":
        response = handle_record_test(params)
    elif action == "get_component_status":
        response = handle_get_status(params)
    elif action == "generate_component_summary":
        response = handle_generate_summary(params)
    elif action == "get_work_tickets":
        response = handle_get_work_tickets(params)
    elif action == "update_work_ticket":
        response = handle_update_work_ticket(params)
    else:
        response = {
            "success": False,
            "error": f"Unknown action: {action}"
        }
    
    # Add standard response fields
    response["api_version"] = API_VERSION
    response["timestamp"] = time.time()
    response["request_action"] = action
    
    return response

def log_api_request(action: str, params: Dict[str, Any]) -> None:
    """Log an API request to the log file."""
    log_file = os.path.join(LOGS_DIR, "a2a_api.log")
    
    # Remove sensitive data from params
    clean_params = params.copy()
    if "auth_token" in clean_params:
        clean_params["auth_token"] = "***"
    
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "params": clean_params
    }
    
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def handle_check_verification(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a check_verification request."""
    agent_id = params.get("agent_id", "")
    component = params.get("component")
    
    if not agent_id:
        return {"success": False, "error": "Missing required parameter: agent_id"}
    
    return check_verification(agent_id, component)

def handle_verify_agent(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a verify_agent request."""
    agent_id = params.get("agent_id", "")
    component = params.get("component")
    
    if not agent_id:
        return {"success": False, "error": "Missing required parameter: agent_id"}
    
    return verify_agent(agent_id, component)

def handle_block_if_unverified(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a block_if_unverified request."""
    agent_id = params.get("agent_id", "")
    component = params.get("component", "")
    operation = params.get("operation", "unknown operation")
    
    if not agent_id:
        return {"success": False, "error": "Missing required parameter: agent_id"}
    
    if not component:
        return {"success": False, "error": "Missing required parameter: component"}
    
    return block_if_unverified(agent_id, component, operation)

def handle_record_start(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a record_component_start request."""
    component = params.get("component", "")
    success = params.get("success", False)
    output = params.get("output", "")
    
    if not component:
        return {"success": False, "error": "Missing required parameter: component"}
    
    try:
        status = record_component_start(component, success, output)
        return {"success": True, "data": {"status": status}}
    except Exception as e:
        return {"success": False, "error": f"Error recording component start: {str(e)}"}

def handle_record_test(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a record_test_run request."""
    component = params.get("component", "")
    success = params.get("success", False)
    results = params.get("results", {})
    
    if not component:
        return {"success": False, "error": "Missing required parameter: component"}
    
    try:
        status = record_test_run(component, success, results)
        return {"success": True, "data": {"status": status}}
    except Exception as e:
        return {"success": False, "error": f"Error recording test run: {str(e)}"}

def handle_get_status(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a get_component_status request."""
    component = params.get("component", "")
    
    if not component:
        return {"success": False, "error": "Missing required parameter: component"}
    
    try:
        status = get_component_status(component)
        return {"success": True, "data": {"status": status}}
    except Exception as e:
        return {"success": False, "error": f"Error getting component status: {str(e)}"}

def handle_generate_summary(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a generate_component_summary request."""
    component = params.get("component", "")
    format_type = params.get("format", "json")  # 'json' or 'markdown'
    
    if not component:
        return {"success": False, "error": "Missing required parameter: component"}
    
    try:
        summary = generate_component_summary(component)
        
        if format_type.lower() == "markdown":
            markdown = generate_markdown_summary(component, summary)
            file_path = save_markdown_summary(component, markdown)
            return {
                "success": True, 
                "data": {
                    "summary_path": file_path,
                    "markdown": markdown
                }
            }
        else:
            file_path = save_component_summary(component, summary)
            return {
                "success": True, 
                "data": {
                    "summary_path": file_path,
                    "summary": summary
                }
            }
    except Exception as e:
        return {"success": False, "error": f"Error generating component summary: {str(e)}"}

def handle_get_work_tickets(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a get_work_tickets request."""
    agent_id = params.get("agent_id", "")
    component = params.get("component", "")
    status = params.get("status", "open")
    
    try:
        tickets = get_work_tickets(agent_id, component, status)
        return {"success": True, "data": {"tickets": tickets}}
    except Exception as e:
        return {"success": False, "error": f"Error getting work tickets: {str(e)}"}

def handle_update_work_ticket(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle an update_work_ticket request."""
    ticket_id = params.get("ticket_id", "")
    updates = params.get("updates", {})
    
    if not ticket_id:
        return {"success": False, "error": "Missing required parameter: ticket_id"}
    
    if not updates:
        return {"success": False, "error": "Missing required parameter: updates"}
    
    try:
        updated = update_work_ticket(ticket_id, updates)
        return {"success": True, "data": {"ticket": updated}}
    except Exception as e:
        return {"success": False, "error": f"Error updating work ticket: {str(e)}"}

def get_work_tickets(agent_id: str = None, component: str = None, status: str = "open") -> List[Dict[str, Any]]:
    """
    Get work tickets filtered by agent, component, and status.
    
    Args:
        agent_id: Optional agent ID to filter by
        component: Optional component to filter by
        status: Ticket status to filter by (default: 'open')
        
    Returns:
        List[Dict]: List of matching work tickets
    """
    tickets = []
    
    try:
        # Get all ticket files
        ticket_files = [f for f in os.listdir(WORK_TICKETS_DIR) if f.endswith(".json")]
        
        for filename in ticket_files:
            file_path = os.path.join(WORK_TICKETS_DIR, filename)
            
            try:
                with open(file_path, 'r') as f:
                    ticket = json.load(f)
                
                # Apply filters
                include = True
                
                if agent_id and ticket.get("assigned_to") != agent_id:
                    include = False
                
                if component and ticket.get("component") != component:
                    include = False
                
                if status and ticket.get("status") != status:
                    include = False
                
                if include:
                    tickets.append(ticket)
            except (json.JSONDecodeError, IOError):
                continue
    except Exception as e:
        print_warning(f"Error loading work tickets: {e}")
    
    return tickets

def update_work_ticket(ticket_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a work ticket.
    
    Args:
        ticket_id: The ID of the ticket to update
        updates: Dictionary of updates to apply
        
    Returns:
        Dict: The updated ticket
    """
    file_path = os.path.join(WORK_TICKETS_DIR, f"{ticket_id}.json")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Work ticket not found: {ticket_id}")
    
    # Load the ticket
    with open(file_path, 'r') as f:
        ticket = json.load(f)
    
    # Apply updates
    for key, value in updates.items():
        if key == "details" and isinstance(value, dict):
            # Merge details instead of replacing
            if "details" not in ticket:
                ticket["details"] = {}
            
            for detail_key, detail_value in value.items():
                ticket["details"][detail_key] = detail_value
        else:
            ticket[key] = value
    
    # Update the timestamp
    ticket["updated_at"] = datetime.datetime.now().isoformat()
    
    # Save the updated ticket
    with open(file_path, 'w') as f:
        json.dump(ticket, f, indent=2)
    
    return ticket

def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="HMS A2A MCP Integration for Verification and Status")
    parser.add_argument("--serve", action="store_true", help="Run as a server (read from stdin)")
    parser.add_argument("--check", help="Check agent verification (format: agent_id:component)")
    parser.add_argument("--verify", help="Verify an agent (format: agent_id:component)")
    parser.add_argument("--status", help="Get component status")
    parser.add_argument("--summary", help="Generate component summary")
    parser.add_argument("--tickets", help="Get work tickets for agent")
    args = parser.parse_args()
    
    if args.serve:
        # Server mode - read requests from stdin
        print_header("Starting A2A MCP Integration server")
        print_info("Reading requests from stdin. Send JSON requests, one per line.")
        
        try:
            for line in sys.stdin:
                try:
                    request = json.loads(line.strip())
                    response = handle_api_request(request)
                    print(json.dumps(response))
                    sys.stdout.flush()
                except json.JSONDecodeError:
                    print(json.dumps({
                        "success": False,
                        "error": "Invalid JSON request",
                        "api_version": API_VERSION,
                        "timestamp": time.time()
                    }))
                    sys.stdout.flush()
        except KeyboardInterrupt:
            print_info("Server stopped")
    
    elif args.check:
        # Check verification
        parts = args.check.split(":", 1)
        agent_id = parts[0]
        component = parts[1] if len(parts) > 1 else None
        
        response = check_verification(agent_id, component)
        print(json.dumps(response, indent=2))
    
    elif args.verify:
        # Verify an agent
        parts = args.verify.split(":", 1)
        agent_id = parts[0]
        component = parts[1] if len(parts) > 1 else None
        
        response = verify_agent(agent_id, component)
        print(json.dumps(response, indent=2))
    
    elif args.status:
        # Get component status
        try:
            status = get_component_status(args.status)
            print(json.dumps(status, indent=2))
        except Exception as e:
            print_error(f"Error getting status: {e}")
    
    elif args.summary:
        # Generate component summary
        try:
            summary = generate_component_summary(args.summary)
            file_path = save_component_summary(args.summary, summary)
            
            markdown = generate_markdown_summary(args.summary, summary)
            md_path = save_markdown_summary(args.summary, markdown)
            
            print_success(f"Summary generated: {file_path}")
            print_success(f"Markdown summary: {md_path}")
        except Exception as e:
            print_error(f"Error generating summary: {e}")
    
    elif args.tickets:
        # Get work tickets
        tickets = get_work_tickets(args.tickets)
        print(json.dumps(tickets, indent=2))
    
    else:
        # Show usage
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