# Using Data Access API with National Mediation Board

## Overview

This tutorial demonstrates how to use the HMS-NFO Data Access API to support National Mediation Board's mission and operations. The examples focus on practical applications of data analytics to enhance decision-making and identify opportunities.

## Prerequisites

- Access to HMS-NFO system
- Authentication credentials for agency-specific data
- Basic understanding of HMS-NFO architecture
- Python 3.7+ with required libraries

## Integration Setup

```python
from hms_nfo import NfoClient
from hms_nfo.components import dataaccessapi

# Initialize the HMS-NFO client
client = NfoClient(api_key='YOUR_API_KEY')

# Initialize the component for this agency
component = client.get_component('data_access_api', agency='nmb')
```

## Example Use Cases

### 1. Accessing Agency-Specific Data

```python
# Query the API for agency-relevant data
data = component.query({
    'agency': 'nmb',
    'data_type': 'economic_indicators',
    'timeframe': 'last_12_months',
    'granularity': 'monthly',
    'format': 'json'
})

# Process and visualize the data
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(data['results'])
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['value'], marker='o')
plt.title('National Mediation Board Economic Indicator Trends')
plt.xlabel('Date')
plt.ylabel('Value')
plt.grid(True)
plt.savefig('economic_trends.png')
plt.show()
```

### 2. Using Restful Capabilities

```python
# Example code for RESTful API endpoints for querying trade data
# This is a placeholder for agency-specific implementation
from hms_nfo.utils import data_processor

# Process agency-specific data
processed_data = component.process_data(
    data_type='restful',
    source='nmb_database',
    filters={
        'relevance': 'high',
        'timeframe': 'current'
    }
)

# Display the results
print(f"Processed {len(processed_data['items'])} items")
for item in processed_data['items'][:3]:
    print(f"ID: {item['id']}")
    print(f"Title: {item['title']}")
    print(f"Relevance score: {item['relevance_score']}")
    print()
```

### 3. Using Graphql Capabilities

```python
# Example code for GraphQL interface for complex queries
# This is a placeholder for agency-specific implementation
from hms_nfo.utils import data_processor

# Process agency-specific data
processed_data = component.process_data(
    data_type='graphql',
    source='nmb_database',
    filters={
        'relevance': 'high',
        'timeframe': 'current'
    }
)

# Display the results
print(f"Processed {len(processed_data['items'])} items")
for item in processed_data['items'][:3]:
    print(f"ID: {item['id']}")
    print(f"Title: {item['title']}")
    print(f"Relevance score: {item['relevance_score']}")
    print()
```

## Best Practices

1. **Authentication**: Always securely store API keys and credentials
2. **Rate Limiting**: Be mindful of API rate limits for data collection
3. **Data Caching**: Cache responses for frequently accessed data
4. **Error Handling**: Implement robust error handling for API failures
5. **Versioning**: Pay attention to API versioning in your requests

## Additional Resources

- [HMS-NFO Data Access API Documentation](../components/data_access_api.md)
- [National Mediation Board Data Integration Guide](../agencies/nmb.md)
- [API Reference](/api-reference)
- [Example Notebooks](/notebooks)
