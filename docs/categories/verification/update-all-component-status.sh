#!/bin/bash
#
# HMS Component Status Update Script
#
# This script updates status tracking and summaries for all HMS components.
# It can be run as a cron job or triggered by CI/CD pipelines.
#
# Features:
# - Simulates component starts and tests
# - Generates comprehensive summaries
# - Creates work tickets for issues
# - Produces a system health report
#
# Usage: ./update_all_component_status.sh [--no-simulate] [--report-only]

set -e

# Get the base directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# ANSI color codes
RESET="\033[0m"
BOLD="\033[1m"
RED="\033[91m"
GREEN="\033[92m"
YELLOW="\033[93m"
BLUE="\033[94m"
CYAN="\033[96m"

# Print header
print_header() {
    echo -e "\n$BOLD$BLUE==========================================================================$RESET"
    echo -e "$BOLD$BLUE  $1$RESET"
    echo -e "$BOLD$BLUE==========================================================================$RESET\n"
}

# Print success message
print_success() {
    echo -e "$GREEN✓ $1$RESET"
}

# Print error message
print_error() {
    echo -e "$RED✗ $1$RESET"
}

# Print info message
print_info() {
    echo -e "$CYAN• $1$RESET"
}

# Print warning message
print_warning() {
    echo -e "$YELLOW⚠ $1$RESET"
}

# Create status directories if they don't exist
ensure_directories() {
    mkdir -p "$SCRIPT_DIR/status"
    mkdir -p "$SCRIPT_DIR/summaries"
    mkdir -p "$SCRIPT_DIR/work_tickets"
    mkdir -p "$SCRIPT_DIR/logs"
}

# Log output to a file
log_to_file() {
    local log_file="$SCRIPT_DIR/logs/update_$(date +%Y%m%d_%H%M%S).log"
    
    # Create the log file
    touch "$log_file"
    
    # Output the command being run
    echo "$ $@" > "$log_file"
    
    # Run the command and tee output to the log file
    "$@" 2>&1 | tee -a "$log_file"
    
    # Return the exit code of the command
    return ${PIPESTATUS[0]}
}

# Process all components
process_all_components() {
    local args=""
    
    # Add arguments based on options
    if [ "$NO_SIMULATE" = true ]; then
        args="$args --no-simulate"
    fi
    
    if [ "$REPORT_ONLY" = true ]; then
        args="$args --no-simulate --no-summary --report"
    else
        args="$args --report"
    fi
    
    print_header "Processing All HMS Components"
    print_info "Running batch processing with options: $args"
    
    # Run the batch processor
    log_to_file python3 "$SCRIPT_DIR/batch_process_all_components.py" $args
    
    # Check exit code
    if [ $? -eq 0 ]; then
        print_success "All components processed successfully"
    else
        print_error "Error processing components"
        exit 1
    fi
}

# Send notification to system admins
send_notification() {
    print_header "Sending Notification"
    print_info "Notifying system admins of component status update..."
    
    # In a real implementation, this would send an email, Slack message, etc.
    # For now, we'll just write to a notification log
    
    local notification_log="$SCRIPT_DIR/logs/notifications.log"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    
    echo "$timestamp - Component status update completed" >> "$notification_log"
    
    # Add information about any issues
    if [ -d "$SCRIPT_DIR/work_tickets" ]; then
        local ticket_count=$(find "$SCRIPT_DIR/work_tickets" -name "*.json" | wc -l)
        if [ $ticket_count -gt 0 ]; then
            echo "$timestamp - $ticket_count work tickets exist for issues" >> "$notification_log"
        fi
    fi
    
    print_success "Notification sent"
}

# Integrate with HMS-DEV
integrate_with_hms_dev() {
    print_header "Integrating with HMS-DEV"
    print_info "Updating HMS-DEV with latest component status..."
    
    # In a real implementation, this would call HMS-DEV APIs
    # For now, we'll just create a status file that HMS-DEV can read
    
    local hms_dev_status="$REPO_ROOT/HMS-DEV_component_status.json"
    
    echo "{" > "$hms_dev_status"
    echo "  \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"," >> "$hms_dev_status"
    echo "  \"status_update\": \"complete\"," >> "$hms_dev_status"
    echo "  \"summaries_dir\": \"$SCRIPT_DIR/summaries\"," >> "$hms_dev_status"
    echo "  \"work_tickets_dir\": \"$SCRIPT_DIR/work_tickets\"" >> "$hms_dev_status"
    echo "}" >> "$hms_dev_status"
    
    print_success "HMS-DEV integration complete"
}

# Main function
main() {
    print_header "HMS Component Status Update"
    print_info "Starting component status update process..."
    
    # Process command line arguments
    NO_SIMULATE=false
    REPORT_ONLY=false
    
    for arg in "$@"; do
        case $arg in
            --no-simulate)
                NO_SIMULATE=true
                shift
                ;;
            --report-only)
                REPORT_ONLY=true
                shift
                ;;
        esac
    done
    
    # Ensure directories exist
    ensure_directories
    
    # Process all components
    process_all_components
    
    # Integrate with HMS-DEV
    integrate_with_hms_dev
    
    # Send notification
    send_notification
    
    print_header "Status Update Complete"
    print_success "HMS component status has been updated"
    print_info "You can view the component summaries in the summaries directory:"
    print_info "  $SCRIPT_DIR/summaries"
    print_info "Work tickets for any issues are in:"
    print_info "  $SCRIPT_DIR/work_tickets"
}

# Run the main function
main "$@"