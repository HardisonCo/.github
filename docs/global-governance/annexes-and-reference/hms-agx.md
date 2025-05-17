# Peace Corps with HMS-AGX

![Peace Corps Logo](/images/gov/peacecorps.png)

> **This tutorial covers the AI-powered version of PeaceCorps using HMS-AGX, not the legacy system.**

## Overview

The HMS-AGX system enhances PeaceCorps's capabilities in agent extensions - specialized ai capabilities for specific agency domains, providing intelligent automation and advanced analytics for improved service delivery.

Agency administrators and citizens can access this system at: [agx.peacecorps.us.gov-ai.co](https://agx.peacecorps.us.gov-ai.co)

## Key Users

This component serves the following key user types:

- **Domain specialists**: Interacts with HMS-AGX to access PeaceCorps services and functions
- **Technical staff**: Interacts with HMS-AGX to access PeaceCorps services and functions
- **Program experts**: Interacts with HMS-AGX to access PeaceCorps services and functions
- **AI administrators**: Interacts with HMS-AGX to access PeaceCorps services and functions

## Agency-Specific Stakeholders

The PeaceCorps HMS-AGX system specifically serves:

- **Local governments**
- **International partners**
- **Project managers**
- **Community organizations**
- **NGOs**

## Core Capabilities

- Domain-specific AI capabilities
- Customized agency workflows
- Specialized data processing
- Advanced decision support
- Agency-specific knowledge models

## Legacy System vs. AI-Powered Approach

| Aspect | Legacy System | AI-Powered Approach |
|--------|--------------|----------------------|
| Generic, | Generic, non-specialized systems | Domain-specific AI capabilities |
| Limited | Limited domain expertise | Customized agency workflows |
| Manual | Manual specialized processing | Specialized data processing |
| Inconsistent | Inconsistent decision making | Advanced decision support |

## Real-World Use Cases

### Cross-Agency Coordination

#### Legacy Approach

Siloed development initiatives with manual coordination meetings

#### AI-Powered Approach

Integrated development platform with automated cross-agency synchronization

#### Key Benefits

- Elimination of duplicate efforts
- Comprehensive visibility across initiatives
- Automated resource sharing

### Grant Program Management

#### Legacy Approach

Annual grant cycles with manual proposal review and limited impact tracking

#### AI-Powered Approach

Continuous grant platform with intelligent proposal evaluation and outcome monitoring

#### Key Benefits

- 85% faster proposal evaluation
- Dynamic funding based on real-time outcomes
- Automated impact assessment

## Implementation Example

```python
from hms.client import HMSClient
from hms.components import hmsagx

# Initialize the HMS client with authentication
client = HMSClient(
    agency="PeaceCorps",
    api_key="YOUR_API_KEY",
    environment="production"
)

# Initialize the HMS-AGX component
agx = client.get_component('hms-agx')

# AI agent deployment example
agent_result = agx.deploy_agent(
    agent_type="service_assistant",
    name="Permit Application Assistant",
    capabilities=[
        "application_guidance",
        "requirements_clarification",
        "status_checking",
        "document_verification"
    ],
    knowledge_sources=[
        "permit_regulations",
        "application_procedures",
        "common_questions"
    ],
    deployment_channels=["web", "mobile", "chat"]
)

print(f"Agent deployed with ID: {agent_result['agent_id']}")
```

## API Reference

Key endpoints for this component:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/operations` | POST | Perform a component operation |
| `/operations/{id}` | GET | Check operation status |
| `/configuration` | GET | View component configuration |
| `/configuration` | PUT | Update component configuration |
| `/status` | GET | Check component health status |

[Back to Agency Index](index.md)
