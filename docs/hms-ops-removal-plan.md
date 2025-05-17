# HMS-OPS Removal Plan

## Overview

This document outlines the plan for safely removing HMS-OPS from the HMS ecosystem after migrating its functionality to HMS-SYS. The removal will be conducted in phases to ensure minimal disruption to the system.

## Prerequisites

Before removing HMS-OPS, the following prerequisites must be met:

1. **Complete Migration**: All HMS-OPS functionality must be successfully migrated to HMS-SYS
2. **Update Dependencies**: All references to HMS-OPS in other components must be updated to point to HMS-SYS
3. **Test Migration**: Comprehensive testing must be performed to ensure all functionality works as expected
4. **Notification Period**: All users and systems must be notified about the upcoming removal

## Removal Phases

### Phase 1: Deprecation (2 Weeks)

1. **Mark as Deprecated**
   - Add deprecation notices to all HMS-OPS documentation
   - Add deprecation warnings to the HMS-OPS command-line interface
   - Send deprecation notifications to all users

2. **Monitor Usage**
   - Set up monitoring to track HMS-OPS usage
   - Identify any systems or users still relying on HMS-OPS
   - Provide assistance to migrate to HMS-SYS

3. **Compatibility Mode**
   - Ensure the HMS-OPS compatibility wrapper is in place for all systems
   - Verify that it correctly redirects all commands to HMS-SYS

### Phase 2: Limited Functionality (2 Weeks)

1. **Disable Write Operations**
   - Modify HMS-OPS to disable all write operations (deployments, updates, etc.)
   - All write operations should return a deprecation message and exit with a non-zero status
   - Read operations (status checks, monitoring data retrieval) should still function

2. **Final Notice**
   - Send a final notice to all users about the upcoming full removal
   - Provide clear instructions for migrating to HMS-SYS
   - Offer direct assistance for critical systems

3. **Extended Monitoring**
   - Continue monitoring HMS-OPS usage
   - Contact users or systems still using HMS-OPS directly

### Phase 3: Archive Mode (1 Week)

1. **Replace Binary with Archive Script**
   - Replace the HMS-OPS binary with a script that:
     - Returns a message indicating HMS-OPS has been replaced by HMS-SYS
     - Provides instructions for using HMS-SYS
     - Exits with a non-zero status

2. **Document Archive**
   - Archive all HMS-OPS documentation
   - Ensure documentation clearly indicates that HMS-OPS is obsolete and HMS-SYS should be used

3. **Final Checks**
   - Verify that no critical systems are dependent on HMS-OPS
   - Confirm all monitoring shows zero usage for at least 5 consecutive days

### Phase 4: Full Removal

1. **Component Removal**
   - Remove the HMS-OPS directory from the HMS ecosystem
   - Remove all HMS-OPS configuration files

2. **Cleanup**
   - Remove HMS-OPS from build and deployment scripts
   - Remove HMS-OPS from documentation indexes

3. **Verification**
   - Run system tests to ensure all functionality continues to work with HMS-SYS
   - Verify that removal of HMS-OPS doesn't cause any system failures

## Implementation Details

### Deprecation Notice Script

Replace the HMS-OPS binary with a script that returns a deprecation notice:

```bash
#!/bin/bash

echo "ERROR: HMS-OPS has been deprecated and removed from the system."
echo "Please use HMS-SYS instead:"
echo "  hms-sys <command> [arguments]"
echo ""
echo "For migration assistance, contact your system administrator."

exit 1
```

### Documentation Update

Update documentation to reflect the removal:

1. Add a prominent notice to the main documentation index
2. Create a migration guide explaining how to use HMS-SYS instead of HMS-OPS
3. Update system architecture diagrams to remove HMS-OPS and show HMS-SYS

### Monitoring Plan

1. Log all HMS-OPS usage to a central location
2. Set up daily reports on HMS-OPS usage
3. Create alerts for any usage after the removal date

## Rollback Plan

In case of critical issues, a rollback plan should be prepared:

1. **Immediate Restore**
   - Keep a backup of HMS-OPS ready for immediate restoration
   - Prepare scripts to quickly restore HMS-OPS if needed

2. **Partial Rollback**
   - Ability to restore specific functionality if issues are limited to certain operations

3. **Communication Plan**
   - Prepare communication templates for notifying users of a rollback
   - Establish clear criteria for when a rollback should be initiated

## Timeline

| Phase | Duration | Start Date | End Date |
|-------|----------|------------|----------|
| Preparation | 1 week | TBD | TBD |
| Deprecation | 2 weeks | TBD | TBD |
| Limited Functionality | 2 weeks | TBD | TBD |
| Archive Mode | 1 week | TBD | TBD |
| Full Removal | 1 day | TBD | TBD |
| Post-Removal Monitoring | 2 weeks | TBD | TBD |

## Approval Process

Before proceeding with each phase, the following approvals must be obtained:

1. System Architecture Team
2. Operations Team
3. Development Team
4. Product Management

## Conclusion

This removal plan provides a structured approach to safely removing HMS-OPS from the HMS ecosystem. By following this plan, we can ensure a smooth transition to HMS-SYS with minimal disruption to the system and users.