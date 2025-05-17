# HMS-MKT Component Summary

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
## Build Setup
1) clone ```develop```
2) npm install

**Latest Commit:** Unknown

### Technology Stack
- **Languages:** JavaScript, TypeScript
- **Frameworks:** Nuxt.js
- **Databases:** None
- **Key Libraries:** Jest, ESLint, Vitest

### Architecture
- **Pattern:** layered
- **Key Directories:** components, data, store

### Integration Points
- HMS-API
- HMS-NFO
- HMS-DOC


## Active Issues

### Issue 1: test_failure
- **Opened:** 2025-05-01 12:24:06
- **Status:** open
- **Details:**
  - **results:** {"passed": 38, "failed": 2, "skipped": 4, "duration": 6.79404048567039, "failure_details": ["Test failure in hms-mkt/tests/test_core.py", "Test failure in hms-mkt/tests/test_core.py"]}

## Work Items for Self-Optimization

### Work Item 1: Fix failing tests for HMS-MKT
- **Type:** test_failure
- **Priority:** medium
- **Assigned To:** HMS-AGT-MKT
- **Suggested Actions:**
  - Review failing tests
  - Check for recent code changes
  - Verify test environment

### Work Item 2: Add integration tests for HMS-MKT with HMS-API, HMS-NFO, HMS-DOC
- **Type:** enhancement
- **Priority:** low
- **Assigned To:** HMS-AGT-MKT
- **Suggested Actions:**
  - Develop integration tests for HMS-MKT with its integration points
  - Set up test fixtures for integration testing
  - Add CI configuration for integration tests

