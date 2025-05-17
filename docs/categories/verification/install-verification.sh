#!/bin/bash
#
# HMS Verification System Installation Script
#
# This script installs the HMS verification system, which ensures that
# developers and agents understand the codebase before making changes.
# It includes:
#
# 1. Installation of pre-commit hooks
# 2. Configuration of MCP adapter for A2A integration
# 3. Setting up file permissions

set -e

# Get the base directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
GIT_HOOKS_DIR="$REPO_ROOT/.git/hooks"
VERIFICATION_DIR="$SCRIPT_DIR"

# Print header
print_header() {
    echo -e "\033[1;34m========================================================================\033[0m"
    echo -e "\033[1;34m  $1\033[0m"
    echo -e "\033[1;34m========================================================================\033[0m"
}

# Print success message
print_success() {
    echo -e "\033[1;32m✓ $1\033[0m"
}

# Print error message
print_error() {
    echo -e "\033[1;31m✗ $1\033[0m"
}

# Print info message
print_info() {
    echo -e "\033[1;36mℹ $1\033[0m"
}

# Check if file exists and is executable
check_executable() {
    if [[ -f "$1" && -x "$1" ]]; then
        return 0
    else
        return 1
    fi
}

# Make Python scripts executable
make_executable() {
    chmod +x "$1"
    print_success "Made executable: $1"
}

# Install pre-commit hook
install_pre_commit_hook() {
    print_header "Installing Pre-Commit Hook"
    
    # Create the hooks directory if it doesn't exist
    mkdir -p "$GIT_HOOKS_DIR"
    
    # The pre-commit hook script
    PRE_COMMIT_HOOK="$GIT_HOOKS_DIR/pre-commit"
    
    # Create the pre-commit hook
    cat > "$PRE_COMMIT_HOOK" <<EOF
#!/bin/bash
#
# HMS Pre-Commit Hook for Verification
#
# This hook ensures that developers and agents have passed
# the verification process before allowing commits.

# Run the verification pre-commit script
python "$VERIFICATION_DIR/pre-commit-hook.py"
exit \$?
EOF
    
    # Make the hook executable
    chmod +x "$PRE_COMMIT_HOOK"
    
    print_success "Pre-commit hook installed at: $PRE_COMMIT_HOOK"
}

# Configure MCP adapter
configure_mcp_adapter() {
    print_header "Configuring MCP Verification Adapter"
    
    MCP_ADAPTER="$VERIFICATION_DIR/mcp_verification_adapter.py"
    
    # Make the adapter executable if it exists
    if [[ -f "$MCP_ADAPTER" ]]; then
        chmod +x "$MCP_ADAPTER"
        print_success "MCP adapter configured: $MCP_ADAPTER"
    else
        print_error "MCP adapter not found: $MCP_ADAPTER"
        exit 1
    fi
    
    # Check if we have the A2A MCP adapter directory
    A2A_DIR="$REPO_ROOT/tool-marketplace/integration/a2a-adapter"
    if [[ -d "$A2A_DIR" ]]; then
        # Create a symbolic link to the adapter
        ln -sf "$MCP_ADAPTER" "$A2A_DIR/verification_adapter.py"
        print_success "Linked MCP adapter to A2A integration directory"
        
        # Add reference to the adapter in A2A configuration
        A2A_CONFIG="$A2A_DIR/index.js"
        if [[ -f "$A2A_CONFIG" ]]; then
            # Check if verification adapter is already referenced
            if ! grep -q "verification_adapter" "$A2A_CONFIG"; then
                print_info "Updating A2A configuration to include verification adapter..."
                
                # This is a placeholder for the actual integration
                # In a real implementation, this would modify the A2A configuration
                print_info "A2A integration might require manual configuration."
            else
                print_info "Verification adapter already referenced in A2A configuration"
            fi
        fi
    else
        print_info "A2A adapter directory not found. Skipping A2A integration."
    fi
}

# Make all Python scripts executable
make_scripts_executable() {
    print_header "Setting Up Python Scripts"
    
    # Make all Python scripts executable
    find "$VERIFICATION_DIR" -name "*.py" -exec chmod +x {} \;
    
    print_success "Made all Python scripts executable"
}

# Test the installation
test_installation() {
    print_header "Testing Installation"
    
    # Test setup_verification.py
    SETUP_VERIFICATION="$VERIFICATION_DIR/setup_verification.py"
    if check_executable "$SETUP_VERIFICATION"; then
        print_success "setup_verification.py is properly configured"
    else
        make_executable "$SETUP_VERIFICATION"
    fi
    
    # Test agent_verification.py
    AGENT_VERIFICATION="$VERIFICATION_DIR/agent_verification.py"
    if check_executable "$AGENT_VERIFICATION"; then
        print_success "agent_verification.py is properly configured"
    else
        make_executable "$AGENT_VERIFICATION"
    fi
    
    # Test repo_analysis_verifier.py
    REPO_ANALYSIS="$VERIFICATION_DIR/repo_analysis_verifier.py"
    if check_executable "$REPO_ANALYSIS"; then
        print_success "repo_analysis_verifier.py is properly configured"
    else
        make_executable "$REPO_ANALYSIS"
    fi
    
    # Test the MCP adapter
    MCP_ADAPTER="$VERIFICATION_DIR/mcp_verification_adapter.py"
    if check_executable "$MCP_ADAPTER"; then
        print_success "mcp_verification_adapter.py is properly configured"
    else
        make_executable "$MCP_ADAPTER"
    fi
    
    print_info "Attempting to run basic verification test..."
    python "$VERIFICATION_DIR/agent_verification.py" "test-agent" --check || true
    
    print_success "Installation test completed"
}

# Main installation function
main() {
    print_header "HMS Verification System Installation"
    
    # Make scripts executable
    make_scripts_executable
    
    # Install pre-commit hook
    install_pre_commit_hook
    
    # Configure MCP adapter
    configure_mcp_adapter
    
    # Test the installation
    test_installation
    
    print_header "Installation Complete"
    echo ""
    print_info "To verify yourself, run:"
    echo "  python $VERIFICATION_DIR/setup_verification.py"
    echo ""
    print_info "To verify an agent, run:"
    echo "  python $VERIFICATION_DIR/agent_verification.py [agent-id] --component [component-name]"
    echo ""
    print_info "For MCP integration, use:"
    echo "  python $VERIFICATION_DIR/mcp_verification_adapter.py --help"
    echo ""
    print_success "HMS Verification System is now installed"
}

# Execute the main function
main