# HMS-RED Component Summary

*Generated at: 2025-05-01 12:24:06*

## Status Overview

**Current Status:** ⚠️ Degraded

### Runtime Status
- **Last Successful Start:** 2025-05-01 12:24:06
- **Start Success Rate:** 1/1 (100.0%)

### Test Status
- **Last Test Run:** 2025-05-01 12:24:06
- **Test Success Rate:** 0/1 (0.0%)

## Component Information

**Description:** 
<p align="center">
  <a href="https://npmjs.com/package/promptfoo"><img src="https://img.shields.io/npm/v/promptfoo" alt="npm"></a>
  <a href="https://npmjs.com/package/promptfoo"><img src="https://img.shields.io/npm/dm/promptfoo" alt="npm"></a>

**Latest Commit:** HEAD

### Technology Stack
- **Languages:** TypeScript
- **Frameworks:** Node.js, Express
- **Databases:** Drizzle
- **Key Libraries:** Jest, ESLint, Drizzle ORM

### Architecture
- **Pattern:** mvc
- **Key Directories:** src/models, src/models

### Integration Points
- HMS-ETL
- HMS-API
- HMS-DOC


## Active Issues

### Issue 1: test_failure
- **Opened:** 2025-05-01 12:24:06
- **Status:** open
- **Details:**
  - **results:** {"passed": 12, "failed": 10, "skipped": 4, "duration": 4.472416497191191, "failure_details": ["Test failure in hms-red/tests/test_core.py", "Test failure in hms-red/tests/test_core.py", "Test failure in hms-red/tests/test_core.py", "Test failure in hms-red/tests/test_core.py", "Test failure in hms-red/tests/test_models.py", "Test failure in hms-red/tests/test_models.py", "Test failure in hms-red/tests/test_integration.py", "Test failure in hms-red/tests/test_api.py", "Test failure in hms-red/tests/test_models.py", "Test failure in hms-red/tests/test_api.py"]}

## Work Items for Self-Optimization

### Work Item 1: Fix failing tests for HMS-RED
- **Type:** test_failure
- **Priority:** medium
- **Assigned To:** HMS-AGT-RED
- **Suggested Actions:**
  - Review failing tests
  - Check for recent code changes
  - Verify test environment

### Work Item 2: Add integration tests for HMS-RED with HMS-ETL, HMS-API, HMS-DOC
- **Type:** enhancement
- **Priority:** low
- **Assigned To:** HMS-AGT-RED
- **Suggested Actions:**
  - Develop integration tests for HMS-RED with its integration points
  - Set up test fixtures for integration testing
  - Add CI configuration for integration tests

