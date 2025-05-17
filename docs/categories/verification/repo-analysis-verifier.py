#!/usr/bin/env python3
"""
HMS Repository Analysis Verification

This script enhances the developer verification process by incorporating
repository analysis data from codex-cli/repo_analysis_logs.

When integrated with the setup_verification.py script, it ensures that
agents and developers have a clear understanding of each component's:
- Purpose and context
- Tech stack and architecture
- Integration points
- Key features and patterns

This enables more informed contributions and prevents misaligned development.
"""

import os
import json
import glob
import random
from typing import Dict, List, Any, Optional, Tuple

# Constants
REPO_LOGS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    "../../codex-cli/repo_analysis_logs"
)

# Ensure path is absolute
REPO_LOGS_DIR = os.path.abspath(REPO_LOGS_DIR)

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
    
    # Find components with repository analysis data
    repo_components = []
    summary_files = glob.glob(os.path.join(REPO_LOGS_DIR, "*_summary.json"))
    
    for file_path in summary_files:
        # Extract component name from file path
        file_name = os.path.basename(file_path)
        component = file_name.split("_summary.json")[0]
        
        # Check if there's a corresponding last_commit file
        commit_file = os.path.join(REPO_LOGS_DIR, f"{component}_last_commit.txt")
        if os.path.exists(commit_file):
            repo_components.append(component)
    
    # Combine both lists, ensuring no duplicates
    combined_components = list(set(all_known_components + repo_components))
    
    return combined_components

def load_component_data(component: str) -> Dict[str, Any]:
    """Load analysis data for a specific component."""
    summary_file = os.path.join(REPO_LOGS_DIR, f"{component}_summary.json")
    commit_file = os.path.join(REPO_LOGS_DIR, f"{component}_last_commit.txt")
    
    if not os.path.exists(summary_file) or not os.path.exists(commit_file):
        raise FileNotFoundError(f"Missing analysis files for component {component}")
    
    with open(summary_file, 'r') as f:
        summary_data = json.load(f)
    
    with open(commit_file, 'r') as f:
        last_commit = f.read().strip()
    
    return {
        "summary": summary_data,
        "last_commit": last_commit
    }

def generate_component_questions(component_data: Dict[str, Any], component: str) -> List[Dict[str, Any]]:
    """Generate verification questions based on component analysis data."""
    summary = component_data["summary"]
    last_commit = component_data["last_commit"]
    questions = []
    
    # Only proceed if we have a valid summary body
    if not summary.get("body"):
        return questions
    
    body = summary["body"]
    context = body.get("context", {})
    structure = body.get("structure", {})
    synthesis = body.get("synthesis", {})
    
    # Component purpose question
    if context.get("description"):
        description = context["description"]
        questions.append({
            "id": f"{component}_purpose",
            "question": f"What is the primary purpose of the {component} component?",
            "type": "multiple_choice",
            "options": [
                description,
                "A testing framework for HMS components",
                "Documentation generator for HMS",
                "CI/CD pipeline for HMS deployments"
            ],
            "correct_answer": 0,
            "explanation": f"The primary purpose of {component} is: {description}"
        })
    
    # Tech stack question
    if context.get("tech_stack", {}).get("languages"):
        languages = context["tech_stack"]["languages"]
        if languages:
            primary_language = languages[0]
            questions.append({
                "id": f"{component}_primary_language",
                "question": f"What is the primary programming language used in {component}?",
                "type": "multiple_choice",
                "options": generate_language_options(primary_language),
                "correct_answer": 0,
                "explanation": f"The primary language used in {component} is {primary_language}."
            })
    
    # Integration points question
    if context.get("integration_points"):
        integration_points = context["integration_points"]
        if integration_points:
            main_integration = integration_points[0]
            questions.append({
                "id": f"{component}_integration",
                "question": f"Which HMS component is a primary integration point for {component}?",
                "type": "multiple_choice",
                "options": generate_integration_options(main_integration, integration_points),
                "correct_answer": 0,
                "explanation": f"{component} integrates primarily with {main_integration} among other components."
            })
    
    # Last commit knowledge
    if last_commit:
        questions.append({
            "id": f"{component}_last_commit",
            "question": f"What is the first 7 characters of the latest commit hash for {component}?",
            "type": "token_input",
            "correct_answer": last_commit[:7],
            "explanation": f"The latest commit hash for {component} starts with {last_commit[:7]}"
        })
    
    # Architectural pattern
    if structure.get("architecture_pattern"):
        arch_pattern = structure["architecture_pattern"]
        questions.append({
            "id": f"{component}_architecture",
            "question": f"What architectural pattern does {component} follow?",
            "type": "multiple_choice",
            "options": generate_architecture_options(arch_pattern),
            "correct_answer": 0,
            "explanation": f"{component} follows the {arch_pattern} architectural pattern."
        })
    
    return questions

def generate_language_options(correct_language: str) -> List[str]:
    """Generate a list of language options with the correct one first."""
    common_languages = ["TypeScript", "JavaScript", "Python", "Java", "Go", "Ruby", "C#", "PHP", "Swift", "Rust"]
    options = [correct_language]
    
    # Add 3 random languages that aren't the correct one
    filtered_langs = [lang for lang in common_languages if lang != correct_language]
    options.extend(random.sample(filtered_langs, min(3, len(filtered_langs))))
    
    return options

def generate_integration_options(correct_integration: str, all_integrations: List[str]) -> List[str]:
    """Generate a list of integration options with the correct one first."""
    common_integrations = ["HMS-API", "HMS-DOC", "HMS-DEV", "HMS-MFE", "HMS-A2A", "HMS-MCP", "HMS-AGT", "HMS-SYS"]
    options = [correct_integration]
    
    # Add other integrations not in all_integrations
    filtered_integrations = [i for i in common_integrations if i not in all_integrations]
    options.extend(random.sample(filtered_integrations, min(3, len(filtered_integrations))))
    
    return options

def generate_architecture_options(correct_architecture: str) -> List[str]:
    """Generate a list of architecture options with the correct one first."""
    arch_options = [
        "microservices", "monolithic", "serverless", "event-driven", 
        "layered", "component_based", "modular", "service-oriented"
    ]
    options = [correct_architecture]
    
    # Add 3 random architectures that aren't the correct one
    filtered_archs = [arch for arch in arch_options if arch != correct_architecture]
    options.extend(random.sample(filtered_archs, min(3, len(filtered_archs))))
    
    return options

def select_component_questions(num_questions: int = 3) -> List[Dict[str, Any]]:
    """Select a specified number of component-specific questions for verification."""
    components = get_available_components()
    
    if not components:
        return []
    
    # Randomly select components for questions
    selected_components = random.sample(components, min(num_questions, len(components)))
    
    all_questions = []
    for component in selected_components:
        try:
            component_data = load_component_data(component)
            questions = generate_component_questions(component_data, component)
            
            if questions:
                # Select one random question from each component
                all_questions.append(random.choice(questions))
        except Exception as e:
            print(f"Error generating questions for {component}: {e}")
    
    return all_questions

def get_repository_verification_questions(num_questions: int = 3) -> List[Dict[str, Any]]:
    """
    Public API: Get component-specific questions for the verification process.
    
    Args:
        num_questions: Number of component-specific questions to include
        
    Returns:
        List of question objects ready to be used in setup_verification.py
    """
    try:
        return select_component_questions(num_questions)
    except Exception as e:
        print(f"Error generating repository verification questions: {e}")
        return []

if __name__ == "__main__":
    # Test the question generation
    questions = get_repository_verification_questions(3)
    print(json.dumps(questions, indent=2))