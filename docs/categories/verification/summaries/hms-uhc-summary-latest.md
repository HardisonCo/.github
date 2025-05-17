# HMS-UHC Component Summary

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
# Enroll

Enroll App is the web-facing, transactional component of the first built-to-purpose, open source eligibility and enrollment solution for Health Benefit Exchanges. Enroll powers the [DC Health Link](https://dchealthlink.com/) site for the [DC Health Benefit Exchange](http://hbx.dc.gov/), and is developed and managed by [IdeaCrew](http://www.ideacrew.com) and HBX.

**Latest Commit:** 8834420a21613febef01c741c2772aa4087295c5

### Technology Stack
- **Languages:** Ruby, JavaScript
- **Frameworks:** Ruby on Rails
- **Databases:** Redis
- **Key Libraries:** RuboCop, Babel, Bearer

### Architecture
- **Pattern:** mvc
- **Key Directories:** components, app/models, app/models, app/controllers, app/views, app/domain

### Integration Points
- HMS-EHR
- HMS-EMR
- HMS-DOC


## Active Issues

### Issue 1: test_failure
- **Opened:** 2025-05-01 12:24:06
- **Status:** open
- **Details:**
  - **results:** {"passed": 36, "failed": 5, "skipped": 2, "duration": 4.831775325580958, "failure_details": ["Test failure in hms-uhc/tests/test_core.py", "Test failure in hms-uhc/tests/test_integration.py", "Test failure in hms-uhc/tests/test_api.py", "Test failure in hms-uhc/tests/test_core.py", "Test failure in hms-uhc/tests/test_api.py"]}

## Work Items for Self-Optimization

### Work Item 1: Fix failing tests for HMS-UHC
- **Type:** test_failure
- **Priority:** medium
- **Assigned To:** HMS-AGT-UHC
- **Suggested Actions:**
  - Review failing tests
  - Check for recent code changes
  - Verify test environment

### Work Item 2: Add integration tests for HMS-UHC with HMS-EHR, HMS-EMR, HMS-DOC
- **Type:** enhancement
- **Priority:** low
- **Assigned To:** HMS-AGT-UHC
- **Suggested Actions:**
  - Develop integration tests for HMS-UHC with its integration points
  - Set up test fixtures for integration testing
  - Add CI configuration for integration tests

