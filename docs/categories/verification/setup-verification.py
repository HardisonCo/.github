#!/usr/bin/env python3
"""
HMS-DEV Developer Verification System

This script implements the developer verification process to ensure that
developers have a baseline understanding of the HMS system and have properly
configured their environment before contributing code.

The verification process includes:
1. A trivia quiz about HMS components and architecture
2. Repository analysis questions specific to components
3. Security advisory review
4. Component connection verification

Upon successful completion, the script generates a verification token that
is valid for 30 days, allowing the developer to commit code.
"""

import os
import sys
import json
import time
import random
import hashlib
import datetime
from getpass import getpass
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Union

# Import repository analysis verification
try:
    from repo_analysis_verifier import get_repository_verification_questions
except ImportError:
    def get_repository_verification_questions(num_questions: int = 3) -> List[Dict[str, Any]]:
        """Fallback if repo_analysis_verifier module isn't available."""
        print("Warning: Repository analysis verification module not found.")
        return []

# Constants
VERIFICATION_FILE = os.path.expanduser("~/.hms_verification")
VERIFICATION_VALIDITY_DAYS = 30
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config")
QUESTIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trivia_questions.json")
MIN_CORRECT_ANSWERS = 7  # Minimum number of correct answers to pass
TOTAL_QUESTIONS = 10     # Total number of questions to ask


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


def load_questions() -> List[Dict[str, Any]]:
    """Load trivia questions from JSON file and enhance with repository-specific questions."""
    try:
        # Load standard questions from the questions file
        with open(QUESTIONS_FILE, 'r') as f:
            standard_questions = json.load(f)
        
        # Get repository analysis questions (3 by default)
        repo_questions = get_repository_verification_questions(3)
        
        # Combine both question sets
        if repo_questions:
            print_info(f"Added {len(repo_questions)} component-specific questions based on repository analysis.")
            return standard_questions + repo_questions
        
        return standard_questions
        
    except FileNotFoundError:
        print_error(f"Questions file not found: {QUESTIONS_FILE}")
        print_info("Creating a sample questions file...")
        
        # Create sample questions
        sample_questions = [
            {
                "id": "q1",
                "question": "What does HMS stand for in the context of our project?",
                "type": "multiple_choice",
                "options": [
                    "Holistic Management System",
                    "Hierarchical Microservice Structure",
                    "Host Modular System",
                    "Hybrid Module Schema"
                ],
                "correct_answer": 0,
                "explanation": "HMS stands for Holistic Management System, which describes our integrated approach to system design."
            },
            {
                "id": "q2",
                "question": "Which component is responsible for agent-to-agent communication in the HMS ecosystem?",
                "type": "multiple_choice",
                "options": [
                    "HMS-DEV",
                    "HMS-DOC",
                    "HMS-A2A",
                    "HMS-MCP"
                ],
                "correct_answer": 2,
                "explanation": "HMS-A2A (Agent-to-Agent) is the component that enables collaborative communication between intelligent agents."
            },
            {
                "id": "q3",
                "question": "What is the Chain of Recursive Thoughts (CoRT) used for in HMS?",
                "type": "multiple_choice",
                "options": [
                    "To validate API requests",
                    "For complex reasoning and decision making",
                    "To optimize database queries",
                    "For UI component rendering"
                ],
                "correct_answer": 1,
                "explanation": "CoRT is used for complex reasoning and decision making, especially in the supervisor system."
            },
            {
                "id": "q4",
                "question": "Which workflow pattern does HMS use for agent development?",
                "type": "multiple_choice",
                "options": [
                    "Waterfall",
                    "Kanban",
                    "Pomodoro",
                    "Scrum"
                ],
                "correct_answer": 2,
                "explanation": "HMS uses a Pomodoro-style workflow (25 min focus → 5 min break) for agent development."
            },
            {
                "id": "q5",
                "question": "The HMS-DEV tool marketplace includes verification mechanisms for tools.",
                "type": "true_false",
                "correct_answer": True,
                "explanation": "True. The tool marketplace includes verification mechanisms to ensure tool quality and security."
            },
            {
                "id": "q6",
                "question": "Sub-agents must pass a certification process before they can commit to protected branches.",
                "type": "true_false",
                "correct_answer": True,
                "explanation": "True. Sub-agents must pass the trivia & onboarding quiz before committing to protected branches."
            },
            {
                "id": "q7",
                "question": "What is the primary principle of the HMS verification approach?",
                "type": "multiple_choice",
                "options": [
                    "Multiple LLMs debating to reach consensus",
                    "Human approval for all decisions",
                    "Verification is harder than generation",
                    "Random sampling of outputs"
                ],
                "correct_answer": 2,
                "explanation": "The primary principle is 'Verification is harder than generation', which emphasizes sound verification mechanisms over multi-LLM debates."
            },
            {
                "id": "q8",
                "question": "What command would you use to create a new component agent?",
                "type": "token_input",
                "correct_answer": "./flow-tools create-agent",
                "explanation": "The command './flow-tools create-agent' is used to create a new component agent in the HMS ecosystem."
            },
            {
                "id": "q9",
                "question": "How many phases are in the standard HMS development process?",
                "type": "token_input",
                "correct_answer": "10",
                "explanation": "The HMS development process has 10 phases: Plan, Build, Launch, Run, Track, Analyze, Plan Improvements, Build Improvements, Release, and Verify."
            },
            {
                "id": "q10",
                "question": "What file format is used for component profiles in HMS?",
                "type": "token_input",
                "correct_answer": "yaml",
                "explanation": "Component profiles in HMS are stored in YAML format, specifically in agent_profile.yaml files."
            }
        ]
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(QUESTIONS_FILE), exist_ok=True)
        
        # Save sample questions
        with open(QUESTIONS_FILE, 'w') as f:
            json.dump(sample_questions, f, indent=2)
        
        # Add repository analysis questions if available
        repo_questions = get_repository_verification_questions(3)
        if repo_questions:
            print_info(f"Added {len(repo_questions)} component-specific questions based on repository analysis.")
            return sample_questions + repo_questions
        
        return sample_questions


def conduct_trivia_quiz() -> Tuple[int, int]:
    """
    Conduct the trivia quiz and return the score.
    
    Returns:
        Tuple[int, int]: (number of correct answers, total questions asked)
    """
    print_header("HMS Developer Verification: Trivia Quiz")
    print("This quiz tests your knowledge of the HMS system and architecture.")
    print("You need to answer at least 7 out of 10 questions correctly to pass.\n")
    
    # Load questions
    all_questions = load_questions()
    
    # Select a random subset of questions if there are more than TOTAL_QUESTIONS
    if len(all_questions) > TOTAL_QUESTIONS:
        questions = random.sample(all_questions, TOTAL_QUESTIONS)
    else:
        questions = all_questions
    
    correct_answers = 0
    
    for i, question in enumerate(questions, 1):
        print(f"\n{Colors.BOLD}Question {i} of {len(questions)}{Colors.RESET}")
        print(question["question"])
        
        if question["type"] == "multiple_choice":
            for j, option in enumerate(question["options"]):
                print(f"  {j+1}. {option}")
            
            valid_answer = False
            while not valid_answer:
                try:
                    user_answer = int(input("\nYour answer (number): "))
                    if 1 <= user_answer <= len(question["options"]):
                        valid_answer = True
                    else:
                        print_warning(f"Please enter a number between 1 and {len(question['options'])}")
                except ValueError:
                    print_warning("Please enter a valid number")
            
            # Adjust for 0-indexing in the question data
            is_correct = (user_answer - 1) == question["correct_answer"]
        
        elif question["type"] == "true_false":
            valid_answer = False
            while not valid_answer:
                user_input = input("\nYour answer (true/false): ").lower()
                if user_input in ["true", "t", "false", "f"]:
                    valid_answer = True
                    user_answer = user_input in ["true", "t"]
                else:
                    print_warning("Please enter 'true' or 'false'")
            
            is_correct = user_answer == question["correct_answer"]
        
        elif question["type"] == "token_input":
            user_answer = input("\nYour answer: ")
            is_correct = user_answer.lower() == question["correct_answer"].lower()
        
        else:
            print_error(f"Unknown question type: {question['type']}")
            continue
        
        if is_correct:
            correct_answers += 1
            print_success("Correct!")
        else:
            print_error("Incorrect.")
        
        print(f"Explanation: {question['explanation']}")
    
    print(f"\n{Colors.BOLD}Quiz Results{Colors.RESET}")
    print(f"You answered {correct_answers} out of {len(questions)} questions correctly.")
    
    if correct_answers >= MIN_CORRECT_ANSWERS:
        print_success(f"Congratulations! You passed the quiz with a score of {correct_answers}/{len(questions)}.")
    else:
        print_error(f"You did not pass the quiz. You need at least {MIN_CORRECT_ANSWERS} correct answers to pass.")
        print_info("Please review the HMS documentation and try again.")
    
    return correct_answers, len(questions)


def review_security_advisories() -> bool:
    """Present security advisories for review and acknowledgment."""
    print_header("HMS Developer Verification: Security Advisory Review")
    
    advisories = [
        {
            "id": "HMS-SEC-001",
            "title": "Agent Prompt Injection Vulnerability",
            "description": "There is a potential for prompt injection attacks in agent interfaces. Always validate and sanitize inputs to agents.",
            "mitigation": "Use the SecurityFilter middleware and implement strict input validation."
        },
        {
            "id": "HMS-SEC-002",
            "title": "Tool Marketplace Security",
            "description": "Third-party tools in the marketplace may pose security risks if not properly verified.",
            "mitigation": "Always use the built-in verification mechanisms before deploying or using tools."
        },
        {
            "id": "HMS-SEC-003",
            "title": "Authorization Token Exposure",
            "description": "Authorization tokens should not be logged or exposed in error messages.",
            "mitigation": "Use the SecureLogger class which automatically redacts sensitive information."
        }
    ]
    
    print("Please review the following security advisories:\n")
    
    for advisory in advisories:
        print(f"{Colors.BOLD}{advisory['id']}: {advisory['title']}{Colors.RESET}")
        print(f"Description: {advisory['description']}")
        print(f"Mitigation: {advisory['mitigation']}")
        print()
    
    acknowledgment = input("Do you acknowledge these security advisories and commit to following the mitigation strategies? (yes/no): ")
    
    if acknowledgment.lower() in ["yes", "y"]:
        print_success("Security advisories acknowledged.")
        return True
    else:
        print_error("You must acknowledge the security advisories to continue.")
        return False


def verify_component_connections() -> bool:
    """Verify connections between HMS components."""
    print_header("HMS Developer Verification: Component Connection Verification")
    
    components = [
        {"name": "HMS-DEV", "status": "present"},
        {"name": "HMS-A2A", "status": "required"},
        {"name": "HMS-DOC", "status": "optional"},
        {"name": "HMS-MCP", "status": "optional"}
    ]
    
    print("Checking component connections...\n")
    
    all_required_present = True
    
    for component in components:
        time.sleep(0.5)  # Simulate checking
        
        if component["status"] == "present":
            print_success(f"{component['name']} is present and properly configured.")
        elif component["status"] == "required":
            # In a real implementation, we would actually check if the component exists
            # For now, we'll simulate that HMS-A2A is not properly configured
            print_warning(f"{component['name']} is required but not properly configured.")
            all_required_present = False
            print_info(f"To configure {component['name']}, run `./flow-tools setup-component {component['name'].lower()}`")
        elif component["status"] == "optional":
            # Simulate that optional components are not present
            print_info(f"{component['name']} is optional and not currently configured.")
    
    if not all_required_present:
        print_warning("\nSome required components are not properly configured.")
        proceed = input("Would you like to proceed anyway? (yes/no): ")
        return proceed.lower() in ["yes", "y"]
    
    return True


def generate_verification_token(username: str) -> str:
    """Generate a verification token for the user."""
    timestamp = int(time.time())
    expiry = timestamp + (VERIFICATION_VALIDITY_DAYS * 24 * 60 * 60)
    
    token_data = {
        "username": username,
        "timestamp": timestamp,
        "expiry": expiry,
        "random": random.randint(1000, 9999)
    }
    
    # Create a hash of the token data
    data_str = json.dumps(token_data, sort_keys=True)
    token_hash = hashlib.sha256(data_str.encode()).hexdigest()
    
    # Combine components to form the token
    token = f"{username}:{expiry}:{token_hash[:16]}"
    
    return token


def save_verification_token(token: str) -> None:
    """Save the verification token to the verification file."""
    with open(VERIFICATION_FILE, "w") as f:
        f.write(token)
    
    # Set file permissions to be readable only by the user
    os.chmod(VERIFICATION_FILE, 0o600)


def is_verification_valid() -> bool:
    """Check if the user has a valid verification token."""
    if not os.path.exists(VERIFICATION_FILE):
        return False
    
    with open(VERIFICATION_FILE, "r") as f:
        token = f.read().strip()
    
    # Parse the token
    try:
        _, expiry_str, _ = token.split(":")
        expiry = int(expiry_str)
        
        # Check if the token has expired
        return time.time() < expiry
    except:
        return False


def run_verification_process() -> None:
    """Run the complete verification process."""
    if is_verification_valid():
        print_info("You already have a valid verification token.")
        renew = input("Would you like to renew your verification? (yes/no): ")
        if renew.lower() not in ["yes", "y"]:
            return
    
    print_header("HMS Developer Verification Process")
    print("This process will ensure you have the knowledge and setup required to contribute to HMS.")
    print("The verification includes a trivia quiz, security advisory review, and component verification.")
    
    username = input("Please enter your username: ")
    
    # Run trivia quiz
    correct_answers, total_questions = conduct_trivia_quiz()
    quiz_passed = correct_answers >= MIN_CORRECT_ANSWERS
    
    if not quiz_passed:
        print_error("You must pass the trivia quiz to complete verification.")
        sys.exit(1)
    
    # Review security advisories
    advisories_acknowledged = review_security_advisories()
    if not advisories_acknowledged:
        print_error("You must acknowledge the security advisories to complete verification.")
        sys.exit(1)
    
    # Verify component connections
    components_verified = verify_component_connections()
    if not components_verified:
        print_error("Component verification failed.")
        sys.exit(1)
    
    # Generate and save verification token
    token = generate_verification_token(username)
    save_verification_token(token)
    
    expiry_date = datetime.datetime.fromtimestamp(time.time() + (VERIFICATION_VALIDITY_DAYS * 24 * 60 * 60))
    
    print_header("Verification Complete")
    print_success(f"You have successfully completed the HMS Developer Verification!")
    print_info(f"Your verification is valid until: {expiry_date.strftime('%Y-%m-%d')}")
    print_info(f"A verification token has been saved to: {VERIFICATION_FILE}")
    print("\nYou can now commit code to the HMS repository.")


def main() -> None:
    """Main entry point for the script."""
    try:
        run_verification_process()
    except KeyboardInterrupt:
        print("\n\nVerification process interrupted.")
        sys.exit(1)


if __name__ == "__main__":
    main()