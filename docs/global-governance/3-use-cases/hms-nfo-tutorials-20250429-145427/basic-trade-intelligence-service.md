# Basic Usage of Trade Intelligence Service

## Overview

This tutorial provides a basic introduction to using the HMS-NFO Trade Intelligence Service. You'll learn how to initialize the component, perform basic operations, and interpret the results.

## Getting Started

First, you'll need to initialize the HMS-NFO client and access the component:

```python
from hms_nfo import NfoClient
from hms_nfo.components import tradeintelligenceservice

# Initialize the HMS-NFO client
client = NfoClient(api_key='YOUR_API_KEY')

# Access the component
component = client.get_component('trade_intelligence_service')
```

## Basic Operations

The following examples demonstrate common operations with this component:

### Generating Reports

```python
# Generate an intelligence report
report = component.generate_report({
    'topic': 'emerging_markets',
    'focus': 'opportunities_and_risks',
    'regions': ['asia', 'south_america'],
    'format': 'executive_summary'
})

# Save the report
with open('emerging_markets_report.pdf', 'wb') as f:
    f.write(report['content'])
```

## Next Steps

Now that you've learned the basics, you can explore more advanced features:

- [Advanced Trade Intelligence Service Tutorial](advanced_trade_intelligence_service.md)
- [Integrating with Agency Systems](integration_guide.md)
- [Custom Configurations](configuration_guide.md)
