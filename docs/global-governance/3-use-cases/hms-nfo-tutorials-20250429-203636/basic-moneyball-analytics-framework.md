# Basic Usage of Moneyball Analytics Framework

## Overview

This tutorial provides a basic introduction to using the HMS-NFO Moneyball Analytics Framework. You'll learn how to initialize the component, perform basic operations, and interpret the results.

## Getting Started

First, you'll need to initialize the HMS-NFO client and access the component:

```python
from hms_nfo import NfoClient
from hms_nfo.components import moneyballanalyticsframework

# Initialize the HMS-NFO client
client = NfoClient(api_key='YOUR_API_KEY')

# Access the component
component = client.get_component('moneyball_analytics_framework')
```

## Basic Operations

The following examples demonstrate common operations with this component:

### Finding Opportunities

```python
# Find undervalued opportunities
opportunities = component.find_opportunities({
    'source_country': 'USA',
    'target_countries': ['JPN', 'DEU', 'KOR'],
    'sectors': 'all',
    'min_score': 0.6
})

# Display results
for opp in opportunities:
    print(f"Country: {opp['country']}")
    print(f"Sector: {opp['sector']}")
    print(f"Score: {opp['score']}")
```

## Next Steps

Now that you've learned the basics, you can explore more advanced features:

- [Advanced Moneyball Analytics Framework Tutorial](advanced_moneyball_analytics_framework.md)
- [Integrating with Agency Systems](integration_guide.md)
- [Custom Configurations](configuration_guide.md)
