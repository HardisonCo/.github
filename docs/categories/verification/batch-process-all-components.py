#!/usr/bin/env python3
"""
HMS Batch Component Processor

This script performs batch operations on all HMS components:
1. Simulates component starts and test runs
2. Generates component summaries
3. Ensures proper tracking records exist for all components
4. Creates work tickets for any issues detected

Use this to ensure the status tracking system has data for all HMS components.
"""

import os
import sys
import json
import time
import random
import argparse
import subprocess
from typing import Dict, List, Any, Tuple

# Add verification directory to the path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

# Import required modules
try:
    from status_tracker import (
        get_available_components,
        start_component,
        run_component_tests,
        record_component_start,
        record_test_run,
        print_header,
        print_success,
        print_error,
        print_info,
        print_warning,
        Colors
    )
    
    from component_summary_generator import (
        generate_component_summary,
        save_component_summary,
        generate_markdown_summary,
        save_markdown_summary
    )
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please make sure status_tracker.py and component_summary_generator.py exist.")
    sys.exit(1)

def process_component(component: str, options: Dict[str, Any]) -> None:
    """
    Process a single component.
    
    Args:
        component: Component ID (e.g., "HMS-API")
        options: Processing options
    """
    print_header(f"Processing {component}")
    
    # Simulate component start
    if options.get("simulate", True):
        print_info(f"Simulating start for {component}...")
        success, output = start_component(component)
        record_component_start(component, success, output)
        
        # Only run tests if the component starts successfully
        if success:
            print_info(f"Simulating tests for {component}...")
            test_success, test_results = run_component_tests(component)
            record_test_run(component, test_success, test_results)
    
    # Generate component summary
    if options.get("summary", True):
        print_info(f"Generating summary for {component}...")
        try:
            summary = generate_component_summary(component)
            save_component_summary(component, summary)
            
            markdown = generate_markdown_summary(component, summary)
            save_markdown_summary(component, markdown)
            
            print_success(f"Summary for {component} completed")
        except Exception as e:
            print_error(f"Error generating summary for {component}: {e}")

def get_all_repository_components() -> List[str]:
    """
    Get a list of all components that have repository analysis data.
    
    Returns:
        List[str]: List of component IDs
    """
    try:
        return get_available_components()
    except Exception as e:
        print_error(f"Error getting component list: {e}")
        return []

def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="HMS Batch Component Processor")
    parser.add_argument("--no-simulate", action="store_true", 
                        help="Skip simulation of component starts and tests")
    parser.add_argument("--no-summary", action="store_true", 
                        help="Skip generation of component summaries")
    parser.add_argument("--component", "-c", 
                        help="Process a specific component (format: HMS-API)")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List all available components")
    parser.add_argument("--report", "-r", action="store_true",
                        help="Generate a report of all components after processing")
    args = parser.parse_args()
    
    # Set processing options
    options = {
        "simulate": not args.no_simulate,
        "summary": not args.no_summary
    }
    
    # Get all components
    components = get_all_repository_components()
    
    if args.list:
        print_header("Available HMS Components")
        for component in sorted(components):
            print(f"- {component}")
        sys.exit(0)
    
    if not components:
        print_error("No components found with repository analysis data.")
        sys.exit(1)
    
    if args.component:
        # Process a specific component
        if args.component in components:
            process_component(args.component, options)
        else:
            print_error(f"Component not found: {args.component}")
            print_info("Available components:")
            for component in sorted(components):
                print(f"- {component}")
            sys.exit(1)
    else:
        # Process all components
        print_header(f"Processing {len(components)} components")
        
        for i, component in enumerate(sorted(components), 1):
            print_info(f"Processing component {i}/{len(components)}: {component}")
            process_component(component, options)
            print("")  # Add an empty line for readability
    
    # Generate a final report if requested
    if args.report:
        print_header("Generating Health Report")
        print_info("Running system health report...")
        
        try:
            # Import the function directly to avoid cyclic imports
            from status_tracker import generate_system_health_report, display_health_report, save_health_report
            
            report = generate_system_health_report()
            display_health_report(report)
            save_health_report(report)
        except Exception as e:
            print_error(f"Error generating health report: {e}")
    
    print_header("Processing Complete")
    print_success(f"Processed {len(components)} components")
    print_info("You can view the component summaries in the summaries directory.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)