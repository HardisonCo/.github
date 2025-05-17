# Basic Usage of Knowledge Integration Engine

## Overview

This tutorial provides a basic introduction to using the HMS-NFO Knowledge Integration Engine. You'll learn how to initialize the component, perform basic operations, and interpret the results.

## Getting Started

First, you'll need to initialize the HMS-NFO client and access the component:

```python
from hms_nfo import NfoClient
from hms_nfo.components import knowledgeintegrationengine

# Initialize the HMS-NFO client
client = NfoClient(api_key='YOUR_API_KEY')

# Access the component
component = client.get_component('knowledge_integration_engine')
```

## Basic Operations

The following examples demonstrate common operations with this component:

### Querying the Knowledge Base

```python
# Query the knowledge base
results = component.query({
    'topic': 'trade_agreements',
    'countries': ['USA', 'CAN', 'MEX'],
    'timeframe': 'current',
    'confidence_threshold': 0.7
})

# Process results
for item in results:
    print(f"Title: {item['title']}")
    print(f"Confidence: {item['confidence_score']}")
```

## Next Steps

Now that you've learned the basics, you can explore more advanced features:

- [Advanced Knowledge Integration Engine Tutorial](advanced_knowledge_integration_engine.md)
- [Integrating with Agency Systems](integration_guide.md)
- [Custom Configurations](configuration_guide.md)
