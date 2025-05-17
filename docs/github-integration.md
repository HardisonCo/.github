# GitHub Integration for HMS-DEV

This document outlines the integration between HMS-DEV and GitHub, allowing developers to work with GitHub issues using codex CLI.

## Overview

HMS-DEV provides tools for fetching GitHub issues and converting them into a format that can be used with codex. This integration allows developers to:

1. List GitHub issues from configured repositories
2. View detailed information about specific issues
3. Launch codex CLI with a GitHub issue for focused work
4. Manage multiple repositories for issue tracking
5. Use pomodoro workflow with CoRT supervisor for structured and effective work
6. Track progress and receive intelligent feedback on approach

## Setup

### Prerequisites

1. **GitHub CLI (gh)**: The integration requires the GitHub CLI to be installed and authenticated.
   ```bash
   # Install GitHub CLI
   brew install gh  # macOS
   # or
   apt install gh   # Ubuntu/Debian
   
   # Authenticate with GitHub
   gh auth login
   ```

2. **Codex CLI**: Ensure that codex CLI is in your PATH.

### Configuration

The integration automatically creates a repository configuration file at `~/.hms-github-repos`. This file contains the list of repositories to track, with one repository per line in the format `owner/repo`.

By default, it's configured with `CodifyHQ/HMS-DEV` as the primary repository.

## Using the Integration

### Command Line Tools

HMS-DEV provides two main scripts for GitHub integration:

1. **Bash Script**: `tools/github/fetch_issues.sh`
2. **Node.js Script**: `tools/github/github-issues.js`

Both scripts provide similar functionality but with different implementations. The Bash script is integrated with `flow-tools.sh` for seamless usage.

### Basic Commands

#### Flow Tools Integration

The simplest way to use the GitHub integration is through the `flow-tools.sh` script:

```bash
# Open a GitHub issue with codex
./scripts/flow-tools.sh github-issue <issue_id>
```

This command:
1. Fetches the issue from the default repository
2. Presents options for standard mode or pomodoro workflow with CoRT supervision
3. Formats it for codex
4. Launches codex with the issue content

When using pomodoro workflow mode, you'll get:
- 25-minute focused work sessions with 5-minute breaks
- Chain of Recursive Thoughts (CoRT) supervisor checking progress
- Adaptive workflow that can reset if you're stuck
- Automatic journal entries for tracking progress

#### Direct Script Usage

For more advanced usage, you can use the script directly:

```bash
# List configured repositories
./tools/github/fetch_issues.sh list-repos

# Add a repository to track
./tools/github/fetch_issues.sh add-repo owner/repo

# Remove a repository from tracking
./tools/github/fetch_issues.sh remove-repo <number>

# List issues from a repository
./tools/github/fetch_issues.sh list-issues [repo] [state] [label] [assignee]

# Get detailed information about an issue
./tools/github/fetch_issues.sh get-issue <repo> <issue_number> [format]

# Launch codex with a GitHub issue
./tools/github/fetch_issues.sh codex-issue [repo] <issue_number>
```

### Output Formats

When fetching issues, you can specify different output formats:

- **text**: Simple text format (default)
- **json**: Raw JSON data
- **markdown**: Formatted markdown for documentation

Example:
```bash
./tools/github/fetch_issues.sh get-issue CodifyHQ/HMS-DEV 42 markdown
```

## Working with GitHub Issues in Codex

When you launch codex with a GitHub issue, it creates a markdown file with the issue details and opens it in codex. This allows you to:

1. View all issue details including title, description, and metadata
2. Work on the issue directly in codex
3. Reference issue details while implementing solutions

The issue files are cached at `~/.hms-issues/` to reduce API calls to GitHub.

## Pomodoro Workflow with CoRT Supervision

HMS-DEV includes a specialized workflow for working on GitHub issues with structured pomodoro sessions and Chain of Recursive Thoughts supervision:

### Pomodoro Workflow

The pomodoro workflow provides:

- 25-minute focused work sessions
- 5-minute breaks between sessions
- Automatic progress tracking in the agent journal
- Ability to add notes during or after pomodoros
- Session continuity with multiple pomodoros for a single issue

### CoRT Supervisor

The Chain of Recursive Thoughts supervisor (`supervisor/github_issue_supervisor.py`) provides:

- Real-time analysis of your progress on the issue
- Intelligent feedback on your approach based on journal entries
- Ability to suggest adjustments or resets when you're stuck
- Continuous monitoring in the background

To manually start the supervisor in continuous mode:

```bash
# Start the supervisor in continuous mode
python3 supervisor/github_issue_supervisor.py

# Or analyze a specific issue
python3 supervisor/github_issue_supervisor.py analyze <issue_number> <repo>

# Or run a single supervision cycle
python3 supervisor/github_issue_supervisor.py run-once
```

The supervisor checks every 5 minutes and adds entries to the agent journal with its recommendations.

## Advanced Usage

### Customizing the Integration

You can customize the GitHub integration by:

1. Modifying the cache duration in the scripts (default: 1 hour)
2. Adding additional repositories to track
3. Creating custom issue formats for different workflows

### Troubleshooting

If you encounter issues with the GitHub integration:

1. Ensure GitHub CLI is installed and authenticated
2. Check that the repository configuration file exists
3. Verify that the repository you're trying to access exists and is accessible
4. Make sure codex CLI is in your PATH

## Examples

### Example 1: Working on a Bug Fix with Pomodoro Workflow

```bash
# List open bug issues
./tools/github/fetch_issues.sh list-issues CodifyHQ/HMS-DEV open bug

# Start the CoRT supervisor in the background
python3 supervisor/github_issue_supervisor.py &

# Open issue #42 with codex and choose pomodoro workflow
./scripts/flow-tools.sh github-issue 42
# Select option 2 when prompted

# Or use the pomodoro script directly
./tools/github/issue-pomodoro.sh 42 CodifyHQ/HMS-DEV
```

### Example 2: Working Across Multiple Repositories

```bash
# Add repositories to track
./tools/github/fetch_issues.sh add-repo CodifyHQ/HMS-API
./tools/github/fetch_issues.sh add-repo CodifyHQ/HMS-UI

# List repositories
./tools/github/fetch_issues.sh list-repos

# List issues from a specific repository
./tools/github/fetch_issues.sh list-issues CodifyHQ/HMS-API open feature

# Open issue with codex
./tools/github/fetch_issues.sh codex-issue CodifyHQ/HMS-API 17
```