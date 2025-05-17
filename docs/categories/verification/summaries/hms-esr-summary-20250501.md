# HMS-ESR Component Summary

*Generated at: 2025-05-01 12:24:06*

## Status Overview

**Current Status:** ❓ Unknown

### Runtime Status
- **Last Successful Start:** Never
- **Start Success Rate:** 0/1 (0.0%)

### Test Status
- **Last Test Run:** Never
- **Test Success Rate:** 0/0 (0.0%)

## Component Information

**Description:** 
Engineering Support Request (ESR) Helper is a tool to streamline and automate the management and resolution of engineering support requests.

## Installation

**Latest Commit:** 4dde24d4dc6481c1b3a508abc1f8399a88f7202f

### Technology Stack
- **Languages:** Ruby
- **Frameworks:** Ruby on Rails
- **Databases:** PostgreSQL, Redis
- **Key Libraries:** Sidekiq, RSpec, Rails helpers

### Architecture
- **Pattern:** layered
- **Key Directories:** data

### Integration Points
- HMS-CUR
- HMS-NFO
- HMS-DOC


## Active Issues

### Issue 1: start_failure
- **Opened:** 2025-05-01 12:24:06
- **Status:** open
- **Details:**
  - **output:** ERROR: Configuration file not found: hms-esr/config/production.json

## Work Items for Self-Optimization

### Work Item 1: Fix HMS-ESR startup failure
- **Type:** start_failure
- **Priority:** high
- **Assigned To:** HMS-DEV
- **Suggested Actions:**
  - Check HMS-ESR logs for error messages
  - Verify all dependencies for HMS-ESR are available
  - Check environment variables and configuration

