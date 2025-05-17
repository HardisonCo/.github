#!/usr/bin/env python3
"""
HMS Pre-Commit Verification Hook

This script serves as a pre-commit hook to enforce verification requirements
before allowing commits to protected branches. It verifies that:

1. Human developers have passed the verification process
2. AI agents have passed the component-specific verification

This helps ensure that all contributors understand the codebase context
and prevents unauthorized or uninformed changes.
"""

import os
import sys
import json
import time
import subprocess
from typing import Dict, Any, List, Tuple, Optional

# Constants
VERIFICATION_CHECK_TIMEOUT = 10  # seconds
AGENT_PREFIX = "agent-"  # Prefix used to identify agent committers
AGENT_ENV_VAR = "HMS_AGENT_ID"  # Environment variable that contains agent ID
COMPONENT_ENV_VAR = "HMS_COMPONENT"  # Environment variable that contains component name
VERIFICATION_SCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "agent_verification.py"
)
HUMAN_VERIFICATION_SCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "setup_verification.py"
)

def get_committer_info() -> Dict[str, str]:
    """Get information about the committer from Git."""
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], 
            stderr=subprocess.PIPE,
            text=True
        ).strip()
        
        email = subprocess.check_output(
            ["git", "config", "user.email"], 
            stderr=subprocess.PIPE,
            text=True
        ).strip()
        
        return {"name": name, "email": email}
    except subprocess.CalledProcessError:
        print("Error: Unable to get committer information.")
        return {"name": "", "email": ""}

def is_agent_commit() -> Tuple[bool, Optional[str]]:
    """
    Determine if the commit is being made by an agent.
    
    Returns:
        Tuple[bool, Optional[str]]: (is_agent, agent_id)
    """
    # Check if environment variable is set
    agent_id = os.environ.get(AGENT_ENV_VAR)
    if agent_id:
        return True, agent_id
    
    # Check if committer name has agent prefix
    committer = get_committer_info()
    if committer["name"].startswith(AGENT_PREFIX):
        return True, committer["name"]
    
    return False, None

def get_changed_components() -> List[str]:
    """
    Identify which HMS components are affected by the current commit.
    
    Returns:
        List[str]: List of component IDs (e.g., ["HMS-API", "HMS-DOC"])
    """
    # First check if a specific component is set in environment
    component = os.environ.get(COMPONENT_ENV_VAR)
    if component:
        return [component]
    
    # Otherwise, try to determine from changed files
    changed_files = []
    try:
        # Get staged files
        output = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            stderr=subprocess.PIPE,
            text=True
        )
        changed_files = output.strip().split("\n")
    except subprocess.CalledProcessError:
        print("Error: Unable to get changed files.")
    
    # Mapping of directory patterns to components
    component_patterns = {
        "HMS-API": ["api/", "src/api/"],
        "HMS-DOC": ["docs/", "documentation/"],
        "HMS-DEV": ["tools/", "scripts/"],
        "HMS-A2A": ["agent/", "agents/", "a2a/"],
        "HMS-MCP": ["mcp/", "model/"],
        "HMS-MFE": ["ui/", "frontend/", "client/"],
        # Add more component patterns as needed
    }
    
    # Identify components affected
    affected_components = set()
    for file in changed_files:
        for component, patterns in component_patterns.items():
            if any(file.startswith(pattern) for pattern in patterns):
                affected_components.add(component)
    
    return list(affected_components)

def is_human_verified() -> bool:
    """Check if the human committer has a valid verification."""
    verification_file = os.path.expanduser("~/.hms_verification")
    
    if not os.path.exists(verification_file):
        return False
    
    try:
        with open(verification_file, "r") as f:
            token = f.read().strip()
        
        # Parse the token
        _, expiry_str, _ = token.split(":")
        expiry = int(expiry_str)
        
        # Check if verification has expired
        return time.time() < expiry
    except:
        return False

def is_agent_verified(agent_id: str, components: List[str]) -> bool:
    """
    Check if the agent has valid verification for all affected components.
    
    Args:
        agent_id: The agent's identifier
        components: List of component IDs the agent is modifying
        
    Returns:
        bool: True if verified for all components, False otherwise
    """
    if not agent_id or not components:
        return False
    
    for component in components:
        try:
            # Call the agent verification check script
            result = subprocess.run(
                [sys.executable, VERIFICATION_SCRIPT, agent_id, "--component", component, "--check"],
                capture_output=True,
                text=True,
                timeout=VERIFICATION_CHECK_TIMEOUT
            )
            
            if result.returncode != 0:
                print(f"Agent {agent_id} is not verified for component {component}.")
                print(f"Verification output: {result.stderr or result.stdout}")
                return False
        except subprocess.TimeoutExpired:
            print(f"Timeout checking verification for agent {agent_id} on component {component}.")
            return False
        except Exception as e:
            print(f"Error checking verification: {e}")
            return False
    
    return True

def main() -> int:
    """Main entry point for the pre-commit hook."""
    print("Running HMS verification pre-commit hook...")
    
    # Determine if commit is from agent or human
    is_agent, agent_id = is_agent_commit()
    
    if is_agent:
        print(f"Agent commit detected: {agent_id}")
        
        # Identify affected components
        components = get_changed_components()
        if not components:
            print("Warning: Unable to determine affected components. Using generic verification.")
            # Default to a generic component for verification
            components = ["HMS-DEV"]
        
        # Check if agent is verified for all affected components
        if is_agent_verified(agent_id, components):
            print(f"Agent {agent_id} is verified for components: {', '.join(components)}")
            return 0  # Allow commit
        else:
            print(f"Error: Agent {agent_id} failed verification for one or more components.")
            print(f"Please run verification first: python {VERIFICATION_SCRIPT} {agent_id} --component COMPONENT")
            return 1  # Block commit
    else:
        print("Human commit detected.")
        
        # Check if developer has valid verification
        if is_human_verified():
            print("Developer verification is valid.")
            return 0  # Allow commit
        else:
            print("Error: Developer verification is missing or expired.")
            print(f"Please run verification first: python {HUMAN_VERIFICATION_SCRIPT}")
            return 1  # Block commit

if __name__ == "__main__":
    sys.exit(main())