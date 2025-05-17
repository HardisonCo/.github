# Basic Usage of Learning System

## Overview

This tutorial provides a basic introduction to using the HMS-NFO Learning System. You'll learn how to initialize the component, perform basic operations, and interpret the results.

## Getting Started

First, you'll need to initialize the HMS-NFO client and access the component:

```python
from hms_nfo import NfoClient
from hms_nfo.components import learningsystem

# Initialize the HMS-NFO client
client = NfoClient(api_key='YOUR_API_KEY')

# Access the component
component = client.get_component('learning_system')
```

## Basic Operations

The following examples demonstrate common operations with this component:

### Training Models

```python
# Define training parameters
training_job = component.create_training_job({
    'model_type': 'sector_classifier',
    'training_data': 'historical_trade_data',
    'features': ['volume', 'price', 'seasonality', 'growth_rate'],
    'validation_split': 0.2
})

# Start training
job_id = training_job.start()
print(f"Training started with job ID: {job_id}")
```

## Next Steps

Now that you've learned the basics, you can explore more advanced features:

- [Advanced Learning System Tutorial](advanced_learning_system.md)
- [Integrating with Agency Systems](integration_guide.md)
- [Custom Configurations](configuration_guide.md)
