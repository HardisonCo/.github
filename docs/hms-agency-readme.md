# HMS-NFO Federal Agency Documentation

This documentation organizes the HMS-NFO (System-Level Information Repository) components and capabilities by federal agency, providing a clear view of how HMS-NFO integrates with and supports different parts of the U.S. government.

## Overview

HMS-NFO serves as the central information authority for the HMS ecosystem, providing critical trade system knowledge, economic data, and government entity relationships. The agency-based documentation structure demonstrates how HMS-NFO capabilities are tailored to meet the specific needs of each federal agency.

## Documentation Structure

The agency-based documentation is organized as follows:

1. **Federal Departments**: Documentation for each cabinet-level department
2. **Independent Agencies**: Documentation for independent federal agencies
3. **Agency Categories**: Groups of agencies with similar missions (e.g., Trade Agencies, Healthcare Agencies)
4. **Components**: Mapping of HMS-NFO components to specific agencies
5. **Source Files**: Original HMS-NFO documentation for reference

## Key Features

- **Agency-Specific Capabilities**: Detailed documentation of how HMS-NFO serves each agency
- **Cross-Agency Coordination**: Information on how HMS-NFO facilitates inter-agency collaboration
- **Component Integration**: Mapping of HMS-NFO components to federal agencies
- **Specialized Functionality**: Description of domain-specific features for each agency

## Core Agency Integrations

HMS-NFO has particularly deep integration with the following agencies:

- **USTDA** (United States Trade and Development Agency): Moneyball opportunity analysis, development financing
- **DOC** (Department of Commerce): Economic data collection, trade flow monitoring
- **USITC** (United States International Trade Commission): Trade dispute analysis, tariff recommendations
- **EXIM** (Export-Import Bank): Export financing optimization, risk assessment
- **USDT** (Department of the Treasury): Financial system analysis, trade balance monitoring
- **DOS** (Department of State): Diplomatic relationship assessment, trade agreement intelligence

## Using This Documentation

To use this documentation:

1. Start with the main index to understand the overall structure
2. Navigate to specific agency pages for agency-tailored capabilities
3. Explore agency categories to understand domain-specific features
4. Reference component pages to see which agencies use specific HMS-NFO features

## Integration Architecture

The agency documentation includes detailed diagrams showing how HMS-NFO components integrate with different agency categories, and how cross-agency data flows are managed.

## Generating Updated Documentation

To regenerate the agency-based documentation:

```bash
./run_agency_docs.sh
```

This script creates a new timestamped version of the documentation and updates the "latest" symbolic link.

## Prerequisites

The agency documentation generator requires:

1. Existing HMS-NFO component documentation
2. Python 3.7+ with required dependencies
3. Appropriate file permissions

## Additional Resources

For more information on HMS-NFO:

- See the [HMS-NFO README](HMS_NFO_README.md) for details on the core system
- Refer to the original component-based documentation in the `docs/HMS-NFO` directory
- Check the [HMS System Context](hms_system_context.md) for broader ecosystem integration