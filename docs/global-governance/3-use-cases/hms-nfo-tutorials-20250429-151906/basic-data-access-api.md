# Basic Usage of Data Access API

## Overview

This tutorial provides a basic introduction to using the HMS-NFO Data Access API. You'll learn how to initialize the component, perform basic operations, and interpret the results.

## Getting Started

First, you'll need to initialize the HMS-NFO client and access the component:

```python
from hms_nfo import NfoClient
from hms_nfo.components import dataaccessapi

# Initialize the HMS-NFO client
client = NfoClient(api_key='YOUR_API_KEY')

# Access the component
component = client.get_component('data_access_api')
```

## Basic Operations

The following examples demonstrate common operations with this component:

### Making API Requests

```python
# Make a basic API request
response = component.request({
    'endpoint': 'economic_data',
    'parameters': {
        'indicator': 'gdp',
        'country': 'USA',
        'timeframe': 'quarterly',
        'start_date': '2020-01-01',
        'end_date': '2022-12-31'
    }
})

# Process the response
print(f"Retrieved {len(response['data'])} data points")
```

## Next Steps

Now that you've learned the basics, you can explore more advanced features:

- [Advanced Data Access API Tutorial](advanced_data_access_api.md)
- [Integrating with Agency Systems](integration_guide.md)
- [Custom Configurations](configuration_guide.md)
