# HMS-DOC to HMS-NFO Integration

This integration allows components in HMS-DOC to access data from the HMS-NFO data model, including full access to trade systems and Moneyball economics information.

## Overview

The HMS-NFO data model provides a comprehensive representation of government data, trade systems, and Moneyball economics principles. This integration enables HMS-DOC components to:

1. Query the HMS-NFO data model directly
2. Enhance prompts with relevant trade system information
3. Boost Moneyball discovery with enhanced metrics
4. Access entity information and data flows

## Components

- **nfo_data_access.py**: Core utility for connecting to HMS-NFO data model
- **hms_nfo_data_model.py**: HMS-NFO data model generator and query interface
- **nodes.py**: Integration to enhance documentation generation
- **moneyball_discovery.py**: Integration for optimized trade opportunity discovery

## Usage Examples

### Querying HMS-NFO Data

```python
from utils.nfo_data_access import HmsNfoDataAccess

# Initialize the data access utility
nfo_access = HmsNfoDataAccess()

# Simple query
response, confidence = nfo_access.query("What are the main components of the trade system?")
print(f"Response (confidence: {confidence:.2f}):")
print(response)

# Query with agent ID and context
context = {"source_country": "USA", "target_country": "Ghana"}
response, confidence = nfo_access.query(
    "What trade opportunities exist?", 
    agent_id="moneyball_discovery",
    context=context
)
```

### Enhancing Prompts

```python
from utils.nfo_data_access import HmsNfoDataAccess

# Initialize the data access utility
nfo_access = HmsNfoDataAccess()

# Original prompt
prompt = "How can we apply Moneyball principles to find better government service deals?"

# Enhance with HMS-NFO data
enhanced_prompt = nfo_access.enrich_prompt(prompt)
```

### Improving Moneyball Discovery

```python
from utils.nfo_data_access import HmsNfoDataAccess

# Initialize the data access utility
nfo_access = HmsNfoDataAccess()

# Original discovery parameters
discovery_input = {
    "source_country": "USA",
    "target_country": "Ghana",
    "min_opportunity_score": 1.2
}

# Enhance with HMS-NFO data
enhanced_input = nfo_access.enrich_moneyball_discovery(discovery_input)
```

## Integration with nodes.py

The `nodes.py` file has been updated to use the HMS-NFO data access utility when gathering government examples. This ensures that documentation generation benefits from the trade system and Moneyball economics information in the HMS-NFO data model.

## Integration with moneyball_discovery.py

The `moneyball_discovery.py` file has been enhanced to:

1. Initialize the HMS-NFO data access utility
2. Enhance discovery metrics with data from HMS-NFO
3. Boost opportunity scores for sectors mentioned in HMS-NFO insights
4. Include HMS-NFO insights in discovery results

## REST API Server

You can run the HMS-NFO data model as a REST API server to allow more efficient querying:

```bash
python hms_nfo_data_model.py serve
```

This starts a server on port 5000 with these endpoints:
- `POST /api/query`: Submit a query (requires JSON with `query`, optional `agent_id` and `context`)
- `GET /api/health`: Check if the server is running

The data access utility will automatically detect and use the server if it's running.

## Testing

Use the provided test script to verify the integration:

```bash
python utils/test_nfo_access.py
```

This will run several tests to demonstrate the different features of the integration.

## Trade System and Moneyball Economics Access

The HMS-NFO data model provides FULL access to:

1. **Import Certificates (Warren Buffett model)** - Tradable certificates for balancing trade and funding development
2. **Dynamic Tariff Adjustments** - Progressive tariff structures linked to development goals
3. **Moneyball Economic Analysis** - Identification of undervalued sectors using statistical methods
4. **Development Project Financing** - Mechanisms for funding international development through trade
5. **Domestic Program Funding** - Allocation of efficiency gains to domestic education, healthcare, and infrastructure
6. **Nth Degree Deal Chains** - Multi-country transaction sequences optimized for global resource allocation
7. **Gov/Civ 'Win-Win' Framework** - Ensures balanced benefits across government and civilian sectors
8. **Trade WAR Metrics** - "Wins Above Replacement" evaluation system for measuring deal effectiveness

The finance/econ section includes comprehensive documentation of both trade system mechanics and Moneyball economics principles with detailed explanations of their applications to government contexts.