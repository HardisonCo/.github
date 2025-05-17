# Federal Deposit Insurance Corporation with HMS-MKT

![Federal Deposit Insurance Corporation Logo](/images/gov/fdic.svg)

> **This tutorial covers the AI-powered version of FDIC using HMS-MKT, not the legacy system.**

## Overview

The HMS-MKT system enhances FDIC's capabilities in marketplace for citizen services and program creation, providing intelligent automation and advanced analytics for improved service delivery.

Agency administrators and citizens can access this system at: [fdic.us.ai-gov.co](https://fdic.us.ai-gov.co)

## Key Users

This component serves the following key user types:

- **Program managers**: Interacts with HMS-MKT to access FDIC services and functions
- **Citizens**: Interacts with HMS-MKT to access FDIC services and functions
- **Service providers**: Interacts with HMS-MKT to access FDIC services and functions
- **Small businesses**: Interacts with HMS-MKT to access FDIC services and functions

## Agency-Specific Stakeholders

The FDIC HMS-MKT system specifically serves:

- **Small businesses**
- **Financial institutions**
- **Financial regulators**
- **Financial consumers**
- **Economic analysts**

## Core Capabilities

- Self-service program creation
- Service discovery and recommendation
- Automated eligibility determination
- Personalized service delivery
- Integrated feedback and improvement

## Legacy System vs. AI-Powered Approach

| Aspect | Legacy System | AI-Powered Approach |
|--------|--------------|----------------------|
| Complex | Complex application processes | Self-service program creation |
| Difficulty | Difficulty discovering relevant services | Service discovery and recommendation |
| Manual | Manual eligibility screening | Automated eligibility determination |
| One-size-fits-all | One-size-fits-all service delivery | Personalized service delivery |

## Real-World Use Cases

### Economic Indicator Analysis

#### Legacy Approach

Monthly manual reports with delayed insights and limited correlation analysis

#### AI-Powered Approach

Real-time economic dashboard with predictive indicators and impact assessment

#### Key Benefits

- Near real-time economic insights
- 90% more accurate forecasting
- Automated policy recommendation generation

### Small Business Loan Processing

#### Legacy Approach

Paper-based application requiring weeks of manual processing

#### AI-Powered Approach

Intelligent loan application platform with automated risk assessment

#### Key Benefits

- Loan approval time reduced from weeks to hours
- 50% increase in approval accuracy
- Personalized terms based on business profile

## Implementation Example

```python
from hms.client import HMSClient
from hms.components import hmsmkt

# Initialize the HMS client with authentication
client = HMSClient(
    agency="FDIC",
    api_key="YOUR_API_KEY",
    environment="production"
)

# Initialize the HMS-MKT component
mkt = client.get_component('hms-mkt')

# Service marketplace example
new_service = mkt.create_service(
    name="Expedited Processing Service",
    service_type="processing",
    description="Faster processing of standard applications",
    eligibility_criteria=[
        "complete_application",
        "previous_approval_history",
        "no_risk_factors"
    ],
    processing_time="2_business_days"
)

print(f"Service created with ID: {new_service['service_id']}")
```

## API Reference

Key endpoints for this component:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/services` | GET | List all available services |
| `/services` | POST | Create a new service |
| `/services/{id}` | GET | View a specific service |
| `/applications` | POST | Submit a service application |
| `/applications/{id}/status` | GET | Check application status |

[Back to Agency Index](index.md)
