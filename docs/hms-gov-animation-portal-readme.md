# HMS Government Agency Animation Portal

An interactive visualization system for displaying relationships between government agencies and HMS components.

## Overview

The HMS Government Agency Animation Portal provides a dynamic, step-by-step visualization of how government agencies interact with various HMS (Hardison Management System) components. The system uses interactive Mermaid diagrams to illustrate these relationships, with animation controls that guide users through the connections.

## Features

- **Interactive Agency Selection**: Choose from multiple federal agencies
- **Dynamic Visualization**: Mermaid-based diagrams showing agency-HMS relationships
- **Step-by-Step Animation**: Guided walkthrough of component interactions
- **Comprehensive Documentation**: Auto-generated docs for each agency
- **Verification System**: Ensures all agencies display correctly
- **Automated Maintenance**: Scheduled verification and updates

## Getting Started

### Installation

Run the setup script to install and configure the system:

```bash
./setup-portal-system.sh
```

This will:
- Install required dependencies
- Create necessary directories
- Run initial verification
- Generate documentation
- Set up maintenance scheduler

### Usage

1. Open `HMS-GOV-COMPLETE-ANIMATION-FIXED.html` in your web browser
2. Select an agency from the dropdown menu
3. Use the animation controls to navigate through the component relationships

## Documentation

- [User Guide](USER-GUIDE.md) - Instructions for end users
- [Developer Guide](DEVELOPER-GUIDE.md) - Technical documentation for developers

## System Components

- **Animation Portal**: `HMS-GOV-COMPLETE-ANIMATION-FIXED.html`
- **Agency Data**: `agency-data.js`
- **Documentation Generator**: `generate-agency-documentation.js`
- **Verification Tool**: `verify-animation-portal.js`
- **System Setup**: `setup-portal-system.sh`
- **Maintenance Scheduler**: Platform-specific service

## Troubleshooting

If you encounter issues:

1. Run the verification tool to check system health:
   ```
   node verify-animation-portal.js
   ```

2. Check browser console for JavaScript errors

3. Verify that all agency data is properly formatted in `agency-data.js`

## Maintenance

The system includes an automated maintenance scheduler that:
- Runs daily verification checks
- Updates documentation when agency data changes
- Logs system status

## License

© Hardison Co. All rights reserved.