# HMS-EDU Component Summary

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
Educational content and learning management

**Latest Commit:** Unknown

### Technology Stack
- **Languages:** Ruby
- **Frameworks:** Ruby on Rails, Sinatra
- **Databases:** PostgreSQL
- **Key Libraries:** ActiveRecord, Puma, Rack

### Architecture
- **Pattern:** mvc
- **Key Directories:** views, app/models, app/models, app/controllers, app/services

### Integration Points
- HMS-DOC
- HMS-API
- HMS-LLM


## Active Issues

### Issue 1: test_failure
- **Opened:** 2025-05-01 12:24:06
- **Status:** open
- **Details:**
  - **results:** {"passed": 45, "failed": 3, "skipped": 2, "duration": 1.7827489086766661, "failure_details": ["Test failure in hms-edu/tests/test_core.py", "Test failure in hms-edu/tests/test_api.py", "Test failure in hms-edu/tests/test_integration.py"]}

## Work Items for Self-Optimization

### Work Item 1: Fix failing tests for HMS-EDU
- **Type:** test_failure
- **Priority:** medium
- **Assigned To:** HMS-AGT-EDU
- **Suggested Actions:**
  - Review failing tests
  - Check for recent code changes
  - Verify test environment

### Work Item 2: Add integration tests for HMS-EDU with HMS-DOC, HMS-API, HMS-LLM
- **Type:** enhancement
- **Priority:** low
- **Assigned To:** HMS-AGT-EDU
- **Suggested Actions:**
  - Develop integration tests for HMS-EDU with its integration points
  - Set up test fixtures for integration testing
  - Add CI configuration for integration tests

