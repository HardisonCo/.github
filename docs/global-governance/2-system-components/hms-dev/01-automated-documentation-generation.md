# Automated Documentation Generation

## Overview

The HMS-DEV component includes a powerful automated documentation generation system that processes source code and generates comprehensive documentation. The system is designed to run efficiently across 25 parallel threads to handle large codebases quickly.

## Command: generate:docs

The `generate:docs` command is configured to run automatically once every 24 hours, ensuring that documentation stays current with the latest code changes.

### Implementation Details

- **Execution Script**: `/Users/arionhardison/Desktop/CodifyHQ/HMS-DOC/generate_tutorials.sh`
- **Scheduler**: System cron job running every 24 hours
- **Parallelism**: Processes up to 25 directories simultaneously
- **Log Files**: Output logged to `/Users/arionhardison/Desktop/CodifyHQ/HMS-DOC/logs/`

### Automated Git Integration

The documentation system automatically:
- Commits all documentation changes to git
- Generates descriptive commit messages with timestamps
- Force pushes to GitHub repository: `git@github.com:HardisonCo/.github.git`

### Configuration

The documentation generator supports the following file types:
- Python (`.py`)
- JavaScript (`.js`)
- TypeScript (`.ts`) 
- Ruby (`.rb`)
- Go (`.go`)
- Rust (`.rs`)
- PHP (`.php`)
- Java (`.java`)
- Markdown (`.md`)

### Exclusions

To maintain efficiency, the following patterns are excluded from documentation:
- `node_modules/*`
- `vendor/*`
- `tests/*`
- `*.min.js`

## Manual Execution

While the system runs automatically every 24 hours, you can also trigger the documentation generation manually:

```bash
bash /Users/arionhardison/Desktop/CodifyHQ/HMS-DOC/run_hms_dev_docs_schedule.sh
```

## Output Location

Generated documentation is stored in the following location:
```
/Users/arionhardison/Desktop/CodifyHQ/HMS-DOC/output/<component-name>/
```

## Git Workflow

After documentation generation completes:

1. Documentation changes are automatically detected
2. A commit is created with message: "Auto-generated documentation update - YYYY-MM-DD"
3. Changes are force pushed to the GitHub repository
4. The entire process is logged to provide audit trail of documentation updates