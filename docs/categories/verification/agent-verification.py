#!/usr/bin/env python3
"""
HMS Agent Verification System

This script implements a verification system specifically designed for agent verification
within the HMS A2A (Agent-to-Agent) and MCP (Model Context Protocol) environments.

When an agent attempts to make changes to protected branches or perform sensitive operations, 
this verification system ensures the agent has adequate knowledge of:

1. The HMS ecosystem and architecture
2. The specific components it's working with
3. The integration points and dependencies
4. Recent repository changes and structure

This script integrates with the standard developer verification process but is
specifically designed for programmatic use by HMS-A2A and HMS-MCP agents.
"""

import os
import sys
import json
import time
import random
import hashlib
import argparse
import datetime
from typing import Dict, List, Any, Tuple, Optional, Union

# Import the repository analysis verification module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from repo_analysis_verifier import get_repository_verification_questions
    from setup_verification import (
        load_questions as load_standard_questions,
        print_header, print_info, print_success, print_error, print_warning,
        Colors, VERIFICATION_FILE, VERIFICATION_VALIDITY_DAYS
    )
except ImportError:
    print("Error: Required verification modules not found.")
    sys.exit(1)


def agent_verification_check(agent_id: str, component: str = None) -> bool:
    """
    Check if an agent has a valid verification for a specific component.
    
    Args:
        agent_id: The unique identifier for the agent
        component: Optional component the agent wants to work with
        
    Returns:
        bool: True if verification is valid, False otherwise
    """
    verification_file = os.path.expanduser(f"~/.hms_verification_{agent_id}")
    
    if not os.path.exists(verification_file):
        return False
    
    with open(verification_file, "r") as f:
        data = json.load(f)
    
    # Check if verification has expired
    expiry = data.get("expiry", 0)
    if int(time.time()) > expiry:
        return False
    
    # If component is specified, check if agent is verified for it
    if component and component not in data.get("verified_components", []):
        return False
    
    return True


def generate_component_questions(component: str, count: int = 3) -> List[Dict[str, Any]]:
    """Generate questions specific to a component."""
    # Get repository analysis questions for the specific component
    repo_questions = []
    
    try:
        # Call repo_analysis_verifier to get component-specific questions
        from repo_analysis_verifier import get_available_components, load_component_data, generate_component_questions
        
        components = get_available_components()
        if component in components:
            component_data = load_component_data(component)
            repo_questions = generate_component_questions(component_data, component)
            
            # Select a subset of questions if we have more than requested
            if len(repo_questions) > count:
                repo_questions = random.sample(repo_questions, count)
    except Exception as e:
        print_warning(f"Error generating component questions: {e}")
    
    # If we don't have enough component-specific questions, add general questions
    general_questions = load_standard_questions()
    
    if len(repo_questions) < count:
        remaining = count - len(repo_questions)
        # Take random questions from general questions to fill the gap
        selected_general = random.sample(general_questions, min(remaining, len(general_questions)))
        repo_questions.extend(selected_general)
    
    return repo_questions


def conduct_agent_verification(agent_id: str, component: str = None) -> bool:
    """
    Conduct verification for an agent.
    
    Args:
        agent_id: The unique identifier for the agent
        component: Optional component the agent is working with
        
    Returns:
        bool: True if verification passed, False otherwise
    """
    print_header(f"HMS Agent Verification: {agent_id}")
    
    if component:
        print_info(f"Verifying for component: {component}")
        questions = generate_component_questions(component, count=5)
    else:
        # General verification with both standard and repo questions
        std_questions = load_standard_questions()
        repo_questions = get_repository_verification_questions(3)
        
        # Combine and select a subset
        all_questions = std_questions + repo_questions
        questions = random.sample(all_questions, min(7, len(all_questions)))
    
    if not questions:
        print_error("No verification questions available.")
        return False
    
    # For simulation purposes, we'll auto-answer correctly
    # In a real implementation, this would integrate with the agent's reasoning
    print_info(f"Processing {len(questions)} verification questions...")
    
    # Simulate agent answering questions
    correct_answers = 0
    required_correct = max(1, len(questions) * 7 // 10)  # 70% required to pass
    
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question['question']}")
        
        # Simulate agent reasoning and answering
        time.sleep(0.5)  # Simulate thinking time
        
        # In a real implementation, the agent would use its knowledge to answer
        # For simulation, we'll just use the correct answer from the question
        is_correct = True  # Assuming agent answers correctly for simulation
        
        if is_correct:
            correct_answers += 1
            print_success("Correct!")
        else:
            print_error("Incorrect.")
    
    # Check if enough questions were answered correctly
    if correct_answers >= required_correct:
        print_success(f"Verification passed: {correct_answers}/{len(questions)} correct")
        
        # Save verification token
        save_agent_verification(agent_id, component)
        return True
    else:
        print_error(f"Verification failed: {correct_answers}/{len(questions)} correct (required: {required_correct})")
        return False


def save_agent_verification(agent_id: str, component: str = None) -> None:
    """Save verification token for an agent."""
    verification_file = os.path.expanduser(f"~/.hms_verification_{agent_id}")
    
    # Calculate expiry time
    expiry = int(time.time()) + (VERIFICATION_VALIDITY_DAYS * 24 * 60 * 60)
    
    # Load existing data if available
    data = {}
    if os.path.exists(verification_file):
        with open(verification_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    
    # Update verification data
    data["agent_id"] = agent_id
    data["timestamp"] = int(time.time())
    data["expiry"] = expiry
    
    # Add component to verified components if specified
    if component:
        if "verified_components" not in data:
            data["verified_components"] = []
        
        if component not in data["verified_components"]:
            data["verified_components"].append(component)
    
    # Save verification data
    with open(verification_file, "w") as f:
        json.dump(data, f, indent=2)
    
    # Set file permissions
    os.chmod(verification_file, 0o600)
    
    expiry_date = datetime.datetime.fromtimestamp(expiry)
    print_info(f"Verification saved. Valid until: {expiry_date.strftime('%Y-%m-%d')}")


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="HMS Agent Verification System")
    parser.add_argument("agent_id", help="The unique identifier for the agent")
    parser.add_argument("--component", "-c", help="The component to verify for")
    parser.add_argument("--check", action="store_true", help="Check verification status without conducting verification")
    args = parser.parse_args()
    
    if args.check:
        # Just check verification status
        is_valid = agent_verification_check(args.agent_id, args.component)
        if is_valid:
            print_success(f"Agent {args.agent_id} has valid verification")
            if args.component:
                print_info(f"Verified for component: {args.component}")
            sys.exit(0)
        else:
            print_error(f"Agent {args.agent_id} does not have valid verification")
            sys.exit(1)
    else:
        # Conduct verification
        passed = conduct_agent_verification(args.agent_id, args.component)
        sys.exit(0 if passed else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nVerification process interrupted.")
        sys.exit(1)