# Using Learning System with United States African Development Foundation (USADF)

## Overview

This tutorial demonstrates how to use the HMS-NFO Learning System to support United States African Development Foundation (USADF)'s mission and operations. The examples focus on practical applications of data analytics to enhance decision-making and identify opportunities.

## Prerequisites

- Access to HMS-NFO system
- Authentication credentials for agency-specific data
- Basic understanding of HMS-NFO architecture
- Python 3.7+ with required libraries

## Integration Setup

```python
from hms_nfo import NfoClient
from hms_nfo.components import learningsystem

# Initialize the HMS-NFO client
client = NfoClient(api_key='YOUR_API_KEY')

# Initialize the component for this agency
component = client.get_component('learning_system', agency='adf')
```

## Example Use Cases

