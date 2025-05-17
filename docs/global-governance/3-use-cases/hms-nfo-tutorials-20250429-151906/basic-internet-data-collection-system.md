# Basic Usage of Internet Data Collection System

## Overview

This tutorial provides a basic introduction to using the HMS-NFO Internet Data Collection System. You'll learn how to initialize the component, perform basic operations, and interpret the results.

## Getting Started

First, you'll need to initialize the HMS-NFO client and access the component:

```python
from hms_nfo import NfoClient
from hms_nfo.components import internetdatacollectionsystem

# Initialize the HMS-NFO client
client = NfoClient(api_key='YOUR_API_KEY')

# Access the component
component = client.get_component('internet_data_collection_system')
```

## Basic Operations

The following examples demonstrate common operations with this component:

### Collecting Data

```python
# Start a basic data collection job
collection_job = component.create_collection_job(
    sources=['government_publications', 'trade_statistics'],
    regions=['north_america'],
    frequency='daily'
)

# Start the collection
job_id = collection_job.start()
print(f"Job started with ID: {job_id}")
```

## Next Steps

Now that you've learned the basics, you can explore more advanced features:

- [Advanced Internet Data Collection System Tutorial](advanced_internet_data_collection_system.md)
- [Integrating with Agency Systems](integration_guide.md)
- [Custom Configurations](configuration_guide.md)
