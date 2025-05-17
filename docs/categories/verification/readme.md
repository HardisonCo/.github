# HMS Verification System

The HMS Verification System ensures that both human developers and AI agents have adequate knowledge of the HMS ecosystem and specific components before making changes to the codebase.

## Purpose

This system addresses several key needs in our agent-based development architecture:

1. **Knowledge Verification**: Ensures contributors understand the HMS ecosystem and architectural patterns before making changes
2. **Component-Specific Verification**: Tests knowledge about specific components being modified
3. **Repository Integration**: Uses repository analysis data to generate relevant questions
4. **Agent Integration**: Enables A2A and MCP agents to verify their knowledge programmatically
5. **Branch Protection**: Provides pre-commit hooks to enforce verification requirements

## System Components

The verification system includes:

1. **`setup_verification.py`**: The core verification system for human developers
2. **`repo_analysis_verifier.py`**: Integrates repository analysis data from `codex-cli/repo_analysis_logs`
3. **`agent_verification.py`**: Specialized verification for AI agents
4. **`pre-commit-hook.py`**: Git pre-commit hook to enforce verification requirements
5. **`mcp_verification_adapter.py`**: MCP adapter for A2A agent integration
6. **`trivia_questions.json`**: Core questions about the HMS ecosystem
7. **`install_verification.sh`**: Installation script to set up the verification system

## Installation

To install the verification system:

```bash
cd docs/verification
chmod +x install_verification.sh
./install_verification.sh
```

This installs the pre-commit hook, configures the MCP adapter, and sets up file permissions.

## Usage

### For Human Developers

Run the verification script to verify yourself:

```bash
python docs/verification/setup_verification.py
```

Upon successful completion, a verification token will be stored in `~/.hms_verification` that is valid for 30 days.

### For AI Agents

Agents can verify themselves programmatically:

```bash
python docs/verification/agent_verification.py [agent-id] --component [component-name]
```

Or via the MCP adapter:

```bash
python docs/verification/mcp_verification_adapter.py --agent-id [agent-id] --component [component-name] --action verify
```

### API Endpoints (MCP Integration)

The MCP adapter supports these operations:

1. **check_verification**: Check if an agent has valid verification
2. **verify_agent**: Conduct verification for an agent
3. **block_if_unverified**: Block an operation if the agent is not verified

Example JSON request to the MCP adapter:

```json
{
  "action": "verify_agent",
  "params": {
    "agent_id": "hms-a2a-agent",
    "component": "HMS-API"
  }
}
```

## Repository Analysis Integration

The verification system automatically incorporates data from repository analysis logs:

```
codex-cli/repo_analysis_logs/HMS-*_summary.json
codex-cli/repo_analysis_logs/HMS-*_last_commit.txt
```

These files provide component-specific information used to generate quiz questions about:

- Component purpose and context
- Technology stack and architectural patterns
- Integration points with other components
- Latest commit information

## Extending the System

To add new verification questions:

1. Edit `trivia_questions.json` to add general HMS knowledge questions
2. Update repository analysis logs for component-specific questions
3. For new verification types, extend the `repo_analysis_verifier.py` module

## License

This verification system is part of the HMS ecosystem and is covered by the same license as the main project.