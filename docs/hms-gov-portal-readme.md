# HMS Government Agency Animation Portal

## Overview

The HMS Government Agency Animation Portal provides interactive visualizations of how HMS components integrate with various federal agencies. This system includes:

1. The animation portal interface
2. Agency documentation generator
3. Verification tools
4. Maintenance scheduler
5. Admin dashboard

## Quick Start

To launch the portal, run:

```
./launch-portal.sh
```

This will open both the animation portal and the admin dashboard in your default browser.

## System Components

### Animation Portal

The main interface for viewing interactive animations showing how HMS components integrate with government agencies.

- **File:** HMS-GOV-COMPLETE-ANIMATION-FIXED.html
- **Access:** Open directly in a browser or use the launcher script

### Admin Dashboard

A comprehensive dashboard for managing the portal system.

- **File:** HMS-GOV-ADMIN-DASHBOARD.html
- **Access:** Open directly in a browser or use the launcher script

### Documentation Generator

Generates detailed documentation for each agency.

- **File:** generate-agency-documentation.js
- **Usage:** `node generate-agency-documentation.js` or `npm run generate`

### Verification Tools

Ensures the portal is working correctly with all agencies.

- **File:** verify-animation-portal.js
- **Usage:** `node verify-animation-portal.js` or `npm run verify`

### Maintenance Scheduler

Automatically verifies and updates the portal system.

- **File:** schedule-portal-maintenance.js
- **Usage:** `node schedule-portal-maintenance.js` or `npm run start-maintenance`

## Maintenance

### Regular Tasks

1. **Verification:** Run `npm run verify` to ensure the portal is working correctly
2. **Documentation Updates:** Run `npm run generate` to update documentation when agency data changes
3. **Portal Fixes:** Run `npm run fix` if issues are detected with the portal

### Backup

The system setup process created a backup of all important files in the `backup` directory. It's recommended to create additional backups regularly.

## Troubleshooting

1. **Portal Not Displaying Properly:** Run the verification script to identify issues
2. **Missing Agency Data:** Check the agency-portal-data.js file for completeness
3. **Documentation Generation Errors:** Check the logs in the `logs` directory for specific error messages

## Contact

For support or questions, contact admin@hardisonco.example
