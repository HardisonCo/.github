#!/bin/bash
# Script to integrate the abundance-based economic model into all agency documentation

# Header and information
echo "==================================="
echo "HMS Economic Model Integration Tool"
echo "==================================="
echo "This script integrates the abundance-based economic model into all agency documentation."
echo ""

# Make script executable
chmod +x integrate_economic_model.py

# Check if the template exists
if [ ! -f "abundance_economic_model_template.md" ]; then
  echo "Error: abundance_economic_model_template.md not found!"
  exit 1
fi

# Check if agencies.json exists in data/extracted directory
AGENCIES_FILE="data/extracted/agencies.json"
if [ ! -f "$AGENCIES_FILE" ]; then
  echo "Error: $AGENCIES_FILE not found!"
  echo "Trying to find another agencies file..."
  AGENCIES_FILE=$(find data -name "agencies*.json" | head -1)
  if [ -z "$AGENCIES_FILE" ]; then
    echo "Error: Could not find any agencies JSON file!"
    exit 1
  fi
  echo "Using $AGENCIES_FILE instead."
fi

# Find the most recent agency directory
LATEST_AGENCY_DIR=$(find docs -name "HMS-NFO-AGENCY-*" -type d | sort | tail -1)
if [ -z "$LATEST_AGENCY_DIR" ]; then
  echo "Error: No agency directory found!"
  exit 1
fi
echo "Using latest agency directory: $LATEST_AGENCY_DIR"

# Create a new enhanced integration script
cat > enhanced_economic_model.py << 'EOF'
#!/usr/bin/env python3
"""
Enhanced script to integrate the abundance-based economic model into all agency documentation.
This script adds the economic model section to agency documentation files.
"""

import os
import sys
import json
import glob
import argparse
from datetime import datetime

def load_agencies(agencies_file):
    """Load agencies from the JSON file."""
    try:
        with open(agencies_file, 'r') as f:
            agencies = json.load(f)
            # Handle different formats of agencies data
            if isinstance(agencies, dict) and "agencies" in agencies:
                return agencies["agencies"]
            return agencies
    except Exception as e:
        print(f"Error loading agencies file: {e}")
        return []

def determine_agency_role(agency):
    """Determine the economic role of an agency based on its metadata."""
    name = agency.get("name", "").lower()
    label = agency.get("label", "").lower()
    mission = agency.get("mission", "").lower()
    core_function = agency.get("core_function", "").lower()
    
    # Default roles
    roles = {
        "resource_provider": "agency data, domain expertise, and regulatory frameworks",
        "deal_facilitator": "coordinating multi-party interactions in its domain of expertise",
        "value_creator": "reducing friction in complex transactions and enabling more efficient outcomes",
        "network_participant": "connecting various stakeholders in its regulatory ecosystem"
    }
    
    # Customize based on agency type
    if any(term in name or term in mission or term in core_function for term in ["financ", "econom", "bank", "fund", "secur", "trade"]):
        roles["resource_provider"] = "financial data, market insights, and regulatory frameworks"
        roles["deal_facilitator"] = "enabling compliant financial transactions and multi-party deals"
        roles["value_creator"] = "reducing financial friction and enabling market efficiencies"
        roles["network_participant"] = "connecting financial market participants within regulatory boundaries"
    
    elif any(term in name or term in mission or term in core_function for term in ["educat", "school", "learn", "teach", "student"]):
        roles["resource_provider"] = "educational resources, learning standards, and program funding"
        roles["deal_facilitator"] = "connecting educational institutions, content providers, and learners"
        roles["value_creator"] = "enabling more effective educational outcomes through resource optimization"
        roles["network_participant"] = "coordinating the educational ecosystem to maximize learning impact"
    
    elif any(term in name or term in mission or term in core_function for term in ["health", "medic", "care", "patient", "hospital"]):
        roles["resource_provider"] = "healthcare data, medical expertise, and care coordination resources"
        roles["deal_facilitator"] = "connecting patients, providers, and healthcare resource systems"
        roles["value_creator"] = "improving health outcomes through optimized resource allocation"
        roles["network_participant"] = "integrating across the healthcare delivery ecosystem"
    
    elif any(term in name or term in mission or term in core_function for term in ["develop", "intern", "aid", "assist"]):
        roles["resource_provider"] = "development funds, technical assistance, and coordination expertise"
        roles["deal_facilitator"] = "creating international partnerships and multi-stakeholder projects"
        roles["value_creator"] = "generating sustainable development outcomes through collaborative models"
        roles["network_participant"] = "connecting international development stakeholders across sectors"
    
    elif any(term in name or term in mission or term in core_function for term in ["secur", "defens", "intellig", "protect"]):
        roles["resource_provider"] = "security frameworks, intelligence resources, and protective capabilities"
        roles["deal_facilitator"] = "coordinating multi-agency security initiatives and partnerships"
        roles["value_creator"] = "enabling secure environments that foster economic and social prosperity"
        roles["network_participant"] = "connecting security stakeholders across government and industry"
    
    return roles

def create_deal_examples(agency):
    """Create customized deal examples based on agency type."""
    name = agency.get("name", "")
    label = agency.get("label", "")
    mission = agency.get("mission", "").lower()
    core_function = agency.get("core_function", "").lower()
    
    deals = []
    
    # Default example
    default_deal = {
        "name": "Multi-Stakeholder Resource Optimization",
        "diagram": """flowchart LR
    A[[{agency}]] -->|Provides expertise & coordination| B[[Service Providers]]
    B -->|Delivers optimized services| C[[Citizens/Businesses]]
    C -->|Provides feedback & data| A
    D[[Technology Partners]] -->|Provides platforms & tools| B
    A -->|Provides standards & guidelines| D""".format(agency=label or "Agency"),
        "description": "coordinates resources and stakeholders to deliver more efficient services.",
        "steps": [
            "identifies service gaps and coordination opportunities",
            "establishes standards and coordination frameworks",
            "monitors quality and outcomes from the multi-party arrangement",
            "continuously optimizes the resource flows based on feedback and data"
        ]
    }
    deals.append(default_deal)
    
    # Add specialized deals based on agency type
    if any(term in name.lower() or term in mission or term in core_function for term in ["financ", "econom", "bank", "fund", "secur", "trade"]):
        financial_deal = {
            "name": "Financial Access Expansion Network",
            "diagram": """flowchart LR
    A[[{agency}]] -->|Regulatory framework & oversight| B[[Financial Institutions]]
    B -->|Financial services| C[[Underserved Communities]]
    D[[Technology Providers]] -->|Fintech platforms| B
    A -->|Policy guidance| D
    E[[Community Organizations]] -->|Local knowledge & outreach| C
    A -->|Program funding & standards| E
    C -->|Economic activity & data| A""".format(agency=label or "Agency"),
            "description": "expands financial access by connecting institutions, technology providers, and community organizations.",
            "steps": [
                "establishes regulatory frameworks that enable innovation while ensuring consumer protection",
                "coordinates the integration of financial institutions with fintech platforms",
                "provides funding and standards for community outreach programs",
                "monitors and optimizes the deal structure based on economic impact data"
            ]
        }
        deals.append(financial_deal)
    
    elif any(term in name.lower() or term in mission or term in core_function for term in ["educat", "school", "learn", "teach", "student"]):
        education_deal = {
            "name": "Adaptive Learning Ecosystem",
            "diagram": """flowchart LR
    A[[{agency}]] -->|Standards & funding| B[[Educational Institutions]]
    B -->|Personalized learning| C[[Students]]
    D[[Content Creators]] -->|Learning materials| B
    A -->|Quality standards| D
    E[[Technology Platforms]] -->|Adaptive learning tools| B
    A -->|Technology requirements| E
    C -->|Performance data| A""".format(agency=label or "Agency"),
            "description": "creates an adaptive learning ecosystem connecting institutions, content creators, and technology platforms.",
            "steps": [
                "establishes educational standards and provides institutional funding",
                "sets quality requirements for educational content",
                "defines technology specifications for adaptive learning platforms",
                "analyzes student performance data to continuously improve the ecosystem"
            ]
        }
        deals.append(education_deal)
    
    elif any(term in name.lower() or term in mission or term in core_function for term in ["health", "medic", "care", "patient", "hospital"]):
        health_deal = {
            "name": "Integrated Care Delivery Network",
            "diagram": """flowchart LR
    A[[{agency}]] -->|Standards & coordination| B[[Healthcare Providers]]
    B -->|Integrated care| C[[Patients]]
    D[[Technology Systems]] -->|Health information exchange| B
    A -->|Interoperability requirements| D
    E[[Community Services]] -->|Social determinants support| C
    A -->|Funding & guidelines| E
    C -->|Health outcomes data| A""".format(agency=label or "Agency"),
            "description": "facilitates integrated healthcare delivery across providers, technology systems, and community services.",
            "steps": [
                "establishes care standards and coordinates provider networks",
                "sets interoperability requirements for health information systems",
                "provides funding and guidelines for community support services",
                "analyzes health outcomes data to drive continuous improvement"
            ]
        }
        deals.append(health_deal)

    return deals

def create_economic_model_section(agency, template_content):
    """Create the economic model section for a specific agency."""
    # Get agency info
    agency_name = agency.get("name", "Unknown Agency")
    agency_label = agency.get("label", "AGENCY")
    
    # Determine agency's economic roles
    roles = determine_agency_role(agency)
    
    # Generate deal examples
    deals = create_deal_examples(agency)
    
    # Replace placeholders with agency-specific content
    content = template_content.replace("[AGENCY_NAME]", agency_name)
    
    # Replace roles
    content = content.replace("[DESCRIBE SPECIFIC RESOURCES, DATA, OR SERVICES THE AGENCY CONTRIBUTES]", 
                             roles["resource_provider"])
    content = content.replace("[DESCRIBE HOW THE AGENCY HELPS ENABLE MULTI-PARTY DEALS]", 
                             roles["deal_facilitator"])
    content = content.replace("[DESCRIBE HOW THE AGENCY CREATES ECONOMIC VALUE IN THE ECOSYSTEM]", 
                             roles["value_creator"])
    content = content.replace("[DESCRIBE THE AGENCY'S POSITION IN THE LARGER ECONOMIC NETWORK]", 
                             roles["network_participant"])
    
    # Replace deal examples
    if deals:
        deal = deals[0]  # Use the first deal example
        content = content.replace("[DEAL_NAME]", deal["name"])
        content = content.replace("```mermaid\nflowchart LR\n    A[[AGENCY_NAME]] -->|Provides X| B[[Party B]]\n    B -->|Provides Y| C[[Party C]]\n    C -->|Provides Z| A\n```",
                                 f"```mermaid\n{deal['diagram']}\n```")
        
        description_text = f"In this example, {agency_name} {deal['description']}"
        steps_text = "\n".join([f"{i+1}. {agency_name} {step}" for i, step in enumerate(deal["steps"])])
        
        content = content.replace("In this example, [AGENCY_NAME] facilitates a three-party deal by:\n1. [DESCRIBE STEP 1]",
                                 f"{description_text}\n\n{steps_text}")
        
        # Add second deal example if available
        if len(deals) > 1:
            deal2 = deals[1]
            additional_example = f"""
### Example 2: {deal2['name']}

```mermaid
{deal2['diagram']}
```

In this example, {agency_name} {deal2['description']}

{'\n'.join([f"{i+1}. {agency_name} {step}" for i, step in enumerate(deal2['steps'])])}
"""
            content = content + additional_example
    
    return content

def integrate_economic_model(agencies, agency_dir, template_content, dry_run=False):
    """Integrate the economic model into agency documentation."""
    # Find all agency directories in the target directory
    agency_dirs = []
    
    # Check if agencies directory exists
    agencies_path = os.path.join(agency_dir, "agencies")
    if os.path.isdir(agencies_path):
        # Get all subdirectories in agencies
        agency_dirs = [os.path.join(agencies_path, d) for d in os.listdir(agencies_path) 
                      if os.path.isdir(os.path.join(agencies_path, d))]
    
    # Build a lookup dictionary for agencies
    agency_dict = {}
    for agency in agencies:
        label = agency.get("label", "").lower()
        if label:
            agency_dict[label.lower()] = agency
    
    # Process each agency directory
    processed_count = 0
    for agency_dir_path in agency_dirs:
        dir_name = os.path.basename(agency_dir_path).lower()
        
        # Find matching agency from our data
        agency = agency_dict.get(dir_name)
        
        if not agency:
            # Try to find by similarity if no exact match
            best_match = None
            for label, a in agency_dict.items():
                if label in dir_name or dir_name in label:
                    best_match = a
                    break
            
            if best_match:
                agency = best_match
            else:
                # Create a minimal agency object using the directory name
                agency = {
                    "label": dir_name.upper(),
                    "name": dir_name.upper()
                }
        
        # Create the economic model content for this agency
        economic_model_content = create_economic_model_section(agency, template_content)
        
        # Path for the new file - assume standard naming convention
        economic_model_file = os.path.join(agency_dir_path, "06_economic_model.md")
        
        # Print what would be done if in dry run mode
        if dry_run:
            print(f"Would create economic model file for {agency.get('name', dir_name)} at {economic_model_file}")
            continue
            
        # Create the file
        try:
            with open(economic_model_file, 'w') as f:
                f.write(economic_model_content)
            print(f"Created economic model file for {agency.get('name', dir_name)}")
            processed_count += 1
        except Exception as e:
            print(f"Error creating file for {agency.get('name', dir_name)}: {e}")
    
    return processed_count

def update_index_files(agency_dir, dry_run=False):
    """Update index files to include the economic model section."""
    # Find all index.md files in agency subdirectories
    agencies_path = os.path.join(agency_dir, "agencies")
    if not os.path.isdir(agencies_path):
        return 0
        
    index_files = glob.glob(os.path.join(agencies_path, "**", "index.md"), recursive=True)
    updated_count = 0
    
    for index_file in index_files:
        try:
            with open(index_file, 'r') as f:
                content = f.read()
                
            # Check if economic model is already linked
            if "06_economic_model.md" in content or "Economic Model" in content:
                continue
                
            # Find the right spot to insert the economic model link
            # Usually after Tutorial Sections header and before Quick Links
            if "## Tutorial Sections" in content:
                # Split the content
                parts = content.split("## Tutorial Sections")
                first_part = parts[0] + "## Tutorial Sections"
                second_part = parts[1]
                
                # Find where to insert (before Advanced Topics or Quick Links)
                lines = second_part.split("\n")
                insert_idx = -1
                for i, line in enumerate(lines):
                    if "Advanced Topics" in line or "## Quick Links" in line:
                        insert_idx = i
                        break
                
                if insert_idx >= 0:
                    # Insert before Advanced Topics
                    lines.insert(insert_idx, "- [Economic Model](06_economic_model.md) - Abundance-based economic framework")
                else:
                    # Append to the section list
                    for i, line in enumerate(lines):
                        if line.strip() == "" and i > 0 and lines[i-1].startswith("-"):
                            lines.insert(i, "- [Economic Model](06_economic_model.md) - Abundance-based economic framework")
                            break
                
                # Reconstruct the content
                new_content = first_part + "\n".join(lines)
                
                if dry_run:
                    print(f"Would update index file: {index_file}")
                    continue
                    
                # Write the updated content
                with open(index_file, 'w') as f:
                    f.write(new_content)
                print(f"Updated index file: {index_file}")
                updated_count += 1
                
        except Exception as e:
            print(f"Error updating index file {index_file}: {e}")
    
    return updated_count

def main():
    parser = argparse.ArgumentParser(description="Integrate economic model into agency documentation")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--agencies-file", required=True, help="Path to agencies JSON file")
    parser.add_argument("--agency-dir", required=True, help="Path to agency documentation directory")
    parser.add_argument("--template", required=True, help="Path to economic model template")
    args = parser.parse_args()
    
    # Load agencies
    agencies = load_agencies(args.agencies_file)
    if not agencies:
        print("No agencies found in the provided file.")
        return 1
    
    print(f"Loaded {len(agencies)} agencies from {args.agencies_file}")
    
    # Load template
    try:
        with open(args.template, 'r') as f:
            template_content = f.read()
    except Exception as e:
        print(f"Error loading template: {e}")
        return 1
    
    # Integrate the economic model
    processed = integrate_economic_model(agencies, args.agency_dir, template_content, args.dry_run)
    
    # Update index files
    updated = update_index_files(args.agency_dir, args.dry_run)
    
    if args.dry_run:
        print(f"Would process {processed} agencies and update {updated} index files.")
    else:
        print(f"Successfully processed {processed} agencies and updated {updated} index files.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF

# Make the enhanced script executable
chmod +x enhanced_economic_model.py

# Add verbose and progress bar functions
cat >> enhanced_economic_model.py << 'EOF'

import sys
import time

class ProgressBar:
    def __init__(self, total, prefix='Progress:', suffix='Complete', length=50, fill='█', print_end='\r'):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.print_end = print_end
        self.start_time = time.time()
        self.iteration = 0
        self.update(0)
        
    def update(self, iteration):
        self.iteration = iteration
        percent = ("{0:.1f}").format(100 * (iteration / float(self.total)))
        filled_length = int(self.length * iteration // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        
        elapsed_time = time.time() - self.start_time
        if iteration > 0:
            est_total_time = elapsed_time * (self.total / iteration)
            est_remaining = est_total_time - elapsed_time
            time_info = f" | {elapsed_time:.1f}s elapsed | {est_remaining:.1f}s remaining"
        else:
            time_info = ""
            
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}{time_info}')
        sys.stdout.flush()
        
        if iteration == self.total:
            print()
            
def enable_verbose_output():
    original_print = print
    
    def timestamped_print(*args, **kwargs):
        timestamp = time.strftime('%H:%M:%S')
        original_print(f"[{timestamp}]", *args, **kwargs)
        
    sys.modules[__name__].__dict__['print'] = timestamped_print

# Modify main function to use progress bar
original_main = main

def main_with_progress():
    # Create new argument parser based on original
    parser = argparse.ArgumentParser(description="Integrate economic model into agency documentation")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--agencies-file", required=True, help="Path to agencies JSON file")
    parser.add_argument("--agency-dir", required=True, help="Path to agency documentation directory")
    parser.add_argument("--template", required=True, help="Path to economic model template")
    args = parser.parse_args()
    
    if args.verbose:
        enable_verbose_output()
        print("Verbose output enabled")
    
    # Load agencies
    print(f"Loading agencies from {args.agencies_file}")
    agencies = load_agencies(args.agencies_file)
    if not agencies:
        print("No agencies found in the provided file.")
        return 1
    
    print(f"Loaded {len(agencies)} agencies from {args.agencies_file}")
    
    # Load template
    try:
        print(f"Loading template from {args.template}")
        with open(args.template, 'r') as f:
            template_content = f.read()
        print(f"Template loaded: {len(template_content)} characters")
    except Exception as e:
        print(f"Error loading template: {e}")
        return 1
    
    # Find all agency directories
    print(f"Scanning agency directory: {args.agency_dir}")
    agency_dirs = []
    
    for item in os.listdir(args.agency_dir):
        item_path = os.path.join(args.agency_dir, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            agency_dirs.append(item_path)
    
    total_agencies = len(agency_dirs)
    print(f"Found {total_agencies} agency directories to process")
    
    # Create a lookup dictionary for agencies
    agency_dict = {}
    for agency in agencies:
        label = agency.get("label", "").lower()
        if label:
            agency_dict[label.lower()] = agency
    
    # Set up progress bar
    if not args.verbose:  # Only show progress bar in non-verbose mode
        progress = ProgressBar(total_agencies, prefix="Processing:", suffix="Complete")
    
    # Integrate the economic model
    processed_count = 0
    for i, agency_dir_path in enumerate(agency_dirs):
        dir_name = os.path.basename(agency_dir_path).lower()
        
        if args.verbose:
            print(f"Processing agency directory: {dir_name}")
        elif not args.dry_run:
            progress.update(i)
        
        # Find matching agency from our data
        agency = agency_dict.get(dir_name)
        
        if not agency:
            # Try to find by similarity if no exact match
            best_match = None
            for label, a in agency_dict.items():
                if label in dir_name or dir_name in label:
                    best_match = a
                    break
            
            if best_match:
                agency = best_match
            else:
                # Create a minimal agency object using the directory name
                agency = {
                    "label": dir_name.upper(),
                    "name": dir_name.upper()
                }
            
            if args.verbose:
                if best_match:
                    print(f"No exact match found for {dir_name}, using best match: {best_match.get('label', '')}")
                else:
                    print(f"No match found for {dir_name}, using directory name")
        
        # Create the economic model content for this agency
        if args.verbose:
            print(f"Creating economic model content for {agency.get('name', dir_name)}")
        
        economic_model_content = create_economic_model_section(agency, template_content)
        
        # Path for the new file
        economic_model_file = os.path.join(agency_dir_path, "06_economic_model.md")
        
        # Print what would be done if in dry run mode
        if args.dry_run:
            print(f"Would create economic model file for {agency.get('name', dir_name)} at {economic_model_file}")
            continue
            
        # Create the file
        try:
            with open(economic_model_file, 'w') as f:
                f.write(economic_model_content)
            
            processed_count += 1
            
            if args.verbose:
                print(f"Created economic model file for {agency.get('name', dir_name)}")
        except Exception as e:
            print(f"Error creating file for {agency.get('name', dir_name)}: {e}")
    
    # Update the final progress bar count
    if not args.verbose and not args.dry_run:
        progress.update(total_agencies)
    
    # Update index files
    print(f"\nUpdating index files...")
    updated = update_index_files(args.agency_dir, args.dry_run)
    
    if args.dry_run:
        print(f"Would process {processed_count} agencies and update {updated} index files.")
    else:
        print(f"Successfully processed {processed_count} agencies and updated {updated} index files.")
    
    return 0

# Replace main with the new one
main = main_with_progress
EOF

# Perform a dry run first to show what would be done
echo "Performing dry run to show what would be done..."
python3 enhanced_economic_model.py --dry-run --agencies-file "$AGENCIES_FILE" --agency-dir "$LATEST_AGENCY_DIR" --template "abundance_economic_model_template.md" --verbose

# Prompt for confirmation
read -p "Do you want to proceed with the integration? (y/n): " confirm

if [[ $confirm != [yY] ]]; then
  echo "Operation cancelled."
  exit 0
fi

# Run the actual integration
echo ""
echo "======================================================"
echo "Running economic model integration with progress bar..."
echo "======================================================"
python3 enhanced_economic_model.py --agencies-file "$AGENCIES_FILE" --agency-dir "$LATEST_AGENCY_DIR" --template "abundance_economic_model_template.md"

# Regenerate agency tutorials with the economic model section
echo "Regenerating agency tutorials with the economic model section..."

# Find all agency tutorial generation scripts and run them
TUTORIAL_SCRIPTS=(generate_agency_tutorials.py generate_agency_tutorials_with_sections.py)
SCRIPT_RUN=false

for script in "${TUTORIAL_SCRIPTS[@]}"; do
  if [ -f "$script" ]; then
    # Run the script to regenerate tutorials
    python3 "$script" --output-dir "$LATEST_AGENCY_DIR"
    SCRIPT_RUN=true
    break
  fi
done

if [ "$SCRIPT_RUN" = false ]; then
  echo "Warning: No tutorial generation scripts found. Skipping tutorial regeneration."
fi

# Update the README to reflect the new economic model
echo "Checking if README has been updated..."
if grep -q "Abundance-Based Economic Model" README.md; then
  echo "README already contains the economic model section."
else
  echo "Warning: README.md may need to be manually updated to include the economic model section."
fi

# Create symlinks for the latest documentation
echo "Updating symlinks to latest documentation..."
echo "Creating symlinks for all HMS component scripts..."

# Create symlinks for all component scripts
for script in run_*.sh; do
  # Skip the current script and any scripts that might cause issues
  if [[ "$script" == "run_economic_model_integration.sh" || 
        "$script" == "run_comprehensive_docs.sh" || 
        "$script" == "run_all_parallel.sh" || 
        "$script" == "run_all_hms.sh" ]]; then
    continue
  fi
  
  # Extract component name
  component=$(echo "$script" | sed 's/run_\(.*\)\.sh/\1/')
  
  # Create domain structure symlink if needed
  if [[ "$script" == "run_domain_structure.sh" ]]; then
    if [ ! -e "run_hms-domain-structure.sh" ]; then
      ln -sf "$script" "run_hms-domain-structure.sh"
      echo "Created symlink: run_hms-domain-structure.sh -> $script"
    fi
  fi
done

# Create symlinks to latest documentation directories
AGENCY_LATEST="docs/HMS-NFO-AGENCY-latest"
TUTORIALS_LATEST="docs/HMS-NFO-TUTORIALS-latest"

# Find the most recent agency and tutorial directories
LATEST_AGENCY=$(find docs -name "HMS-NFO-AGENCY-*" -type d | sort | tail -1)
LATEST_TUTORIALS=$(find docs -name "HMS-NFO-TUTORIALS-*" -type d | sort | tail -1)

if [ -n "$LATEST_AGENCY" ]; then
  if [ -L "$AGENCY_LATEST" ]; then
    rm "$AGENCY_LATEST"
  fi
  ln -s "$LATEST_AGENCY" "$AGENCY_LATEST"
  echo "Created symlink: $AGENCY_LATEST -> $LATEST_AGENCY"
fi

if [ -n "$LATEST_TUTORIALS" ]; then
  if [ -L "$TUTORIALS_LATEST" ]; then
    rm "$TUTORIALS_LATEST"
  fi
  ln -s "$LATEST_TUTORIALS" "$TUTORIALS_LATEST"
  echo "Created symlink: $TUTORIALS_LATEST -> $LATEST_TUTORIALS"
fi

echo "Symlink creation complete."
echo "You can now run: ./run_all_hms.sh or ./run_all_parallel.sh"
echo "For documentation: ./run_tutorial_progress.sh"

echo ""
echo "==================================="
echo "Integration complete!"
echo "==================================="
echo "The abundance-based economic model has been integrated into all agency documentation."
echo "Please review the changes in the docs directory."
echo ""

exit 0
