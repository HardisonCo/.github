# Git Integration

## Overview

The HMS-DEV documentation generator automatically manages git integration to ensure that all documentation is properly committed and pushed to the central repository.

## GitHub Repository

Only the docs directory is automatically pushed to:
```
git@github.com:HardisonCo/.github.git
```

This keeps the documentation repository separate from the main codebase.

## Docs-Only Push Process

After each documentation generation run, the system:

1. Creates a temporary directory for storing only the docs
2. Copies the docs directory to this temporary location
3. Initializes a new git repository in the temporary directory
4. Configures git user information for the commit
5. Adds the HardisonCo GitHub remote as origin
6. Stages all documentation files
7. Creates a commit with a timestamped commit message
8. Force pushes only the documentation to the GitHub repository
9. Cleans up the temporary directory

This approach ensures that only documentation is pushed to the target repository, keeping it separate from the main codebase.

## Force Push Policy

The system uses `git push -f` to ensure that the repository always represents the latest documentation state. This approach:

- Ensures documentation consistency
- Prevents merge conflicts
- Maintains a clean commit history for documentation updates

## Testing Git Setup

If you need to test the documentation push process without actually pushing:

```bash
/Users/arionhardison/Desktop/CodifyHQ/HMS-DOC/test_git_setup.sh
```

This script will:
- Show what steps would be taken in the push process
- Create a temporary directory for testing
- Display the commands that would be run
- Will NOT actually push any changes

## Manual Docs-Only Push

While the system handles commits automatically, you can also manually push just the docs:

```bash
# Create a temporary directory
TEMP_DIR=$(mktemp -d)

# Copy docs to temporary directory
cp -R /Users/arionhardison/Desktop/CodifyHQ/HMS-DOC/docs $TEMP_DIR/

# Initialize git repo in temporary directory
cd $TEMP_DIR
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git remote add origin git@github.com:HardisonCo/.github.git

# Add all docs files
git add --all

# Commit and push
git commit -m "Manual documentation update"
git push -f origin master

# Clean up
cd -
rm -rf $TEMP_DIR
```