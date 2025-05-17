#!/usr/bin/env python3
"""
HMS MCP Verification Adapter

This script serves as an adapter for integrating the HMS verification system
with the Model Context Protocol (MCP). It allows A2A MCP agents to:

1. Check verification status
2. Complete verification for components
3. Enforce verification before sensitive operations

Usage via MCP:
- check_verification(agent_id, component=None)
- verify_agent(agent_id, component=None)
- block_if_unverified(agent_id, component, operation)
"""

import os
import sys
import json
import time
import argparse
import subprocess
from typing import Dict, Any, List, Optional, Tuple, Union

# Add the verification directory to the path
VERIFICATION_DIR = os.path.dirname(os.path.abspath(__file__))
if VERIFICATION_DIR not in sys.path:
    sys.path.append(VERIFICATION_DIR)

# Import verification modules
try:
    from agent_verification import (
        agent_verification_check, 
        conduct_agent_verification,
        save_agent_verification
    )
except ImportError:
    # Fallback to subprocess calls if direct import fails
    def agent_verification_check(agent_id: str, component: str = None) -> bool:
        """Check if an agent has valid verification."""
        script_path = os.path.join(VERIFICATION_DIR, "agent_verification.py")
        cmd = [sys.executable, script_path, agent_id, "--check"]
        if component:
            cmd.extend(["--component", component])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

    def conduct_agent_verification(agent_id: str, component: str = None) -> bool:
        """Conduct verification for an agent."""
        script_path = os.path.join(VERIFICATION_DIR, "agent_verification.py")
        cmd = [sys.executable, script_path, agent_id]
        if component:
            cmd.extend(["--component", component])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

# MCP protocol response formatter
def mcp_response(success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
    """Format response according to MCP protocol."""
    response = {
        "success": success,
        "timestamp": time.time()
    }
    
    if data is not None:
        response["data"] = data
    
    if error is not None:
        response["error"] = error
    
    return response

def check_verification(agent_id: str, component: str = None) -> Dict[str, Any]:
    """
    Check if an agent has valid verification.
    
    Args:
        agent_id: The agent's identifier
        component: Optional component to check verification for
        
    Returns:
        Dict: MCP-formatted response with verification status
    """
    try:
        is_verified = agent_verification_check(agent_id, component)
        return mcp_response(True, {
            "agent_id": agent_id,
            "component": component,
            "verified": is_verified,
            "timestamp": time.time()
        })
    except Exception as e:
        return mcp_response(False, error=f"Verification check failed: {str(e)}")

def verify_agent(agent_id: str, component: str = None) -> Dict[str, Any]:
    """
    Conduct verification for an agent.
    
    Args:
        agent_id: The agent's identifier
        component: Optional component to verify for
        
    Returns:
        Dict: MCP-formatted response with verification result
    """
    try:
        passed = conduct_agent_verification(agent_id, component)
        return mcp_response(True, {
            "agent_id": agent_id,
            "component": component,
            "verified": passed,
            "timestamp": time.time()
        })
    except Exception as e:
        return mcp_response(False, error=f"Verification failed: {str(e)}")

def block_if_unverified(agent_id: str, component: str, operation: str) -> Dict[str, Any]:
    """
    Block an operation if the agent is not verified for the component.
    
    Args:
        agent_id: The agent's identifier
        component: The component the agent wants to modify
        operation: Description of the operation being performed
        
    Returns:
        Dict: MCP-formatted response indicating if operation is allowed
    """
    is_verified = agent_verification_check(agent_id, component)
    
    if is_verified:
        return mcp_response(True, {
            "agent_id": agent_id,
            "component": component,
            "operation": operation,
            "allowed": True,
            "message": f"Operation '{operation}' is allowed."
        })
    else:
        return mcp_response(False, {
            "agent_id": agent_id,
            "component": component,
            "operation": operation,
            "allowed": False,
            "message": f"Operation '{operation}' is blocked. Verification required for {component}."
        }, error="Verification required")

def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle MCP API request.
    
    Args:
        request: The MCP request object
        
    Returns:
        Dict: MCP-formatted response
    """
    action = request.get("action")
    params = request.get("params", {})
    
    if action == "check_verification":
        return check_verification(
            params.get("agent_id", ""),
            params.get("component")
        )
    elif action == "verify_agent":
        return verify_agent(
            params.get("agent_id", ""),
            params.get("component")
        )
    elif action == "block_if_unverified":
        return block_if_unverified(
            params.get("agent_id", ""),
            params.get("component", ""),
            params.get("operation", "unknown operation")
        )
    else:
        return mcp_response(False, error=f"Unknown action: {action}")

def main() -> None:
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(description="HMS MCP Verification Adapter")
    parser.add_argument("--agent-id", "-a", required=True, help="Agent identifier")
    parser.add_argument("--component", "-c", help="Component to verify for")
    parser.add_argument("--action", choices=["check", "verify", "block"], default="check",
                       help="Action to perform (check, verify, block)")
    parser.add_argument("--operation", help="Operation description (for block action)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()
    
    if args.action == "check":
        result = check_verification(args.agent_id, args.component)
    elif args.action == "verify":
        result = verify_agent(args.agent_id, args.component)
    elif args.action == "block":
        if not args.component:
            print("Error: Component is required for block action.")
            sys.exit(1)
        result = block_if_unverified(args.agent_id, args.component, args.operation or "unspecified operation")
    else:
        result = mcp_response(False, error="Invalid action")
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            if "data" in result and "verified" in result["data"]:
                verified = result["data"]["verified"]
                if verified:
                    print(f"✓ Agent {args.agent_id} is verified for {args.component or 'generic operations'}")
                else:
                    print(f"✗ Agent {args.agent_id} is NOT verified for {args.component or 'generic operations'}")
            elif "data" in result and "allowed" in result["data"]:
                allowed = result["data"]["allowed"]
                if allowed:
                    print(f"✓ Operation allowed for {args.agent_id} on {args.component}")
                else:
                    print(f"✗ Operation blocked for {args.agent_id} on {args.component}")
            else:
                print("Operation completed successfully")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # CLI mode
        main()
    else:
        # Read from stdin for MCP integration
        try:
            request = json.loads(sys.stdin.read())
            response = handle_mcp_request(request)
            print(json.dumps(response))
        except json.JSONDecodeError:
            print(json.dumps(mcp_response(False, error="Invalid JSON input")))
        except Exception as e:
            print(json.dumps(mcp_response(False, error=f"Unexpected error: {str(e)}")))