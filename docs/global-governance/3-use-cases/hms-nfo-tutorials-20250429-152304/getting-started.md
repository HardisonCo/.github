# Getting Started with HMS-NFO

## Overview

This tutorial provides a general introduction to HMS-NFO, the System-Level Information Repository for the HMS ecosystem. You'll learn how to set up your environment, authenticate with the system, and perform basic operations.

## Prerequisites

- Python 3.7 or higher
- Agency-specific access credentials
- Basic understanding of data analytics concepts

## Installation

```bash
# Install the HMS-NFO client library
pip install hms-nfo-client

# Verify installation
python -c "import hms_nfo; print(hms_nfo.__version__)"
```

## Authentication

```python
from hms_nfo import NfoClient

# Method 1: Direct API key
client = NfoClient(api_key='YOUR_API_KEY')

# Method 2: Environment variable
# export HMS_NFO_API_KEY=YOUR_API_KEY
client = NfoClient.from_env()

# Method 3: Configuration file
client = NfoClient.from_config('~/.hms-nfo/config.yaml')

# Verify authentication
print(client.is_authenticated())  # Should return True
```

## Basic Operations

### Accessing Components

```python
# Access the Moneyball Analytics component
moneyball = client.get_component('moneyball_analytics_framework')

# Access the Data Collection component
data_collection = client.get_component('internet_data_collection_system')

# Access the Knowledge Integration component
knowledge = client.get_component('knowledge_integration_engine')
```

### Querying Data

```python
# Query economic data
results = client.query({
    'data_type': 'economic_indicators',
    'country': 'USA',
    'indicators': ['gdp', 'inflation', 'unemployment'],
    'timeframe': 'last_5_years',
    'frequency': 'quarterly'
})

# Display results
import pandas as pd

df = pd.DataFrame(results['data'])
print(df.head())
```

## Next Steps

Now that you have the basics, explore these resources to learn more:

1. [Agency-Specific Tutorials](../index.md#agency-specific-tutorials)
2. [Component Tutorials](../index.md#component-tutorials)
3. [API Reference Documentation](/api-reference)
4. [Sample Notebooks and Code](/examples)
