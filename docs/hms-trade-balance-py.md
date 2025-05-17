# HMS Trade Balance Python API

This document describes the Python API for the HMS Trade Balance System, which implements the Win-Win Calculation Framework.

## Installation

The `hms_core` Python module contains the Trade Balance API functions as part of the HMS FFI bindings. This module is automatically built and installed when building the HMS system.

```python
import hms_core
```

## API Functions

### Entity Profile Management

#### `trade_balance_create_entity_profile_py`

Creates an entity profile for use in win-win calculations.

```python
def trade_balance_create_entity_profile_py(
    entity_id: str,
    entity_name: str,
    entity_type: str,
    dimensions_json: Optional[str],
    time_preference: Optional[float],
    risk_preference: Optional[float],
    resource_constraints_json: Optional[str],
    performance_metrics_json: Optional[str]
) -> str:
    """
    Create an entity profile for use in win-win calculations.
    
    Args:
        entity_id: Unique identifier for the entity
        entity_name: Human-readable name of the entity
        entity_type: Type of entity (government, corporate, ngo, civilian)
        dimensions_json: JSON string with dimension weights
        time_preference: Entity's time preference rate (default 0.05)
        risk_preference: Entity's risk preference rate (default 0.3)
        resource_constraints_json: JSON string with resource constraints
        performance_metrics_json: JSON string with performance metrics
        
    Returns:
        JSON string with the created entity profile
    """
    pass
```

### Value Component Management

#### `trade_balance_create_value_component_py`

Creates a value component for use in win-win calculations.

```python
def trade_balance_create_value_component_py(
    dimension: str,
    amount: float,
    timeline_json: Optional[str],
    probability: Optional[float],
    verification_method: Optional[str],
    is_quantifiable: Optional[bool],
    network_effects_json: Optional[str]
) -> str:
    """
    Create a value component for use in win-win calculations.
    
    Args:
        dimension: Value dimension (economic, social, environmental, security)
        amount: Raw value amount
        timeline_json: JSON string with timeline entries [[period, amount], ...]
        probability: Probability of value realization (default 0.8)
        verification_method: Method for verifying value (default "standard")
        is_quantifiable: Whether the value is quantifiable (default True)
        network_effects_json: JSON string with network effects
        
    Returns:
        JSON string with the created value component
    """
    pass
```

### Deal Analysis and Optimization

#### `trade_balance_analyze_win_win_py`

Analyzes a deal for win-win status.

```python
def trade_balance_analyze_win_win_py(
    entity_profiles_json: str,
    value_components_json: str
) -> Dict[str, Any]:
    """
    Analyze a deal for win-win status.
    
    Args:
        entity_profiles_json: JSON string with entity profiles
        value_components_json: JSON string with value components for each entity
        
    Returns:
        Dictionary with analysis results containing:
        - analysis_id: Unique identifier for this analysis
        - is_win_win: Boolean indicating if the deal is win-win
        - entity_values: Dictionary mapping entity IDs to value assessments
        - negative_entities: List of entity IDs with negative value
        - improvement_opportunities: List of improvement suggestions
        - value_distribution: Dictionary mapping entity IDs to value percentages
        - value_inequality_gini: Gini coefficient for value inequality
    """
    pass
```

#### `trade_balance_optimize_distribution_py`

Optimizes value distribution to ensure win-win outcome.

```python
def trade_balance_optimize_distribution_py(
    entity_profiles_json: str,
    value_components_json: str,
    constraints_json: str
) -> Dict[str, Any]:
    """
    Optimize value distribution to ensure win-win outcome.
    
    Args:
        entity_profiles_json: JSON string with entity profiles
        value_components_json: JSON string with value components for each entity
        constraints_json: JSON string with optimization constraints
        
    Returns:
        Dictionary with optimization results containing:
        - optimization_id: Unique identifier for this optimization
        - success: Boolean indicating if optimization succeeded
        - optimized_components: Dictionary with optimized value components
        - error: Error message if optimization failed
    """
    pass
```

#### `trade_balance_calculate_entity_value_py`

Calculates the value for a single entity.

```python
def trade_balance_calculate_entity_value_py(
    entity_profile_json: str,
    value_components_json: str
) -> str:
    """
    Calculate the value for a single entity.
    
    Args:
        entity_profile_json: JSON string with entity profile
        value_components_json: JSON string with value components
        
    Returns:
        JSON string with entity value assessment
    """
    pass
```

### Examples and Utilities

#### `trade_balance_run_example_analysis_py`

Runs an example win-win analysis with pre-defined entities and components.

```python
def trade_balance_run_example_analysis_py() -> Dict[str, Any]:
    """
    Run an example win-win analysis with pre-defined entities and components.
    
    Returns:
        Dictionary with analysis results (same format as trade_balance_analyze_win_win_py)
    """
    pass
```

## Usage Examples

### Basic Deal Analysis

```python
import hms_core
import json

# Create entity profiles
gov_profile = json.loads(hms_core.trade_balance_create_entity_profile_py(
    "gov_1",
    "Government Agency",
    "government",
    '{"budget_impact": 0.3, "mission_alignment": 0.3, "constituent_benefit": 0.3, "political_capital": 0.1}',
    0.05,
    0.3,
    None,
    None
))

corp_profile = json.loads(hms_core.trade_balance_create_entity_profile_py(
    "corp_1",
    "Technology Corporation",
    "corporate",
    '{"revenue_impact": 0.4, "cost_reduction": 0.3, "market_position": 0.2, "risk_reduction": 0.1}',
    0.1,
    0.4,
    None,
    None
))

# Create value components
gov_comp1 = json.loads(hms_core.trade_balance_create_value_component_py(
    "economic",
    100.0,
    '[[0, 20.0], [1, 30.0], [2, 50.0]]',
    0.9,
    "standard",
    True,
    None
))

corp_comp1 = json.loads(hms_core.trade_balance_create_value_component_py(
    "economic",
    200.0,
    '[[0, 50.0], [1, 75.0], [2, 75.0]]',
    0.85,
    "standard",
    True,
    None
))

# Combine into entity profiles and value components
entity_profiles = {
    "gov_1": gov_profile,
    "corp_1": corp_profile
}

value_components = {
    "gov_1": {
        "comp_1": gov_comp1
    },
    "corp_1": {
        "comp_1": corp_comp1
    }
}

# Analyze the deal
analysis_result = hms_core.trade_balance_analyze_win_win_py(
    json.dumps(entity_profiles),
    json.dumps(value_components)
)

# Check if win-win
is_win_win = analysis_result["is_win_win"]
print(f"Is win-win: {is_win_win}")
```

### Deal Optimization

```python
# If the deal is not win-win, optimize it
if not analysis_result['is_win_win']:
    # Define optimization constraints
    constraints = {
        "min_positive_value": 10.0,
        "min_positive_margin": 1.0
    }
    
    # Optimize value distribution
    optimized_result = hms_core.trade_balance_optimize_distribution_py(
        json.dumps(entity_profiles),
        json.dumps(value_components),
        json.dumps(constraints)
    )
    
    # Check if optimization succeeded
    if optimized_result['success']:
        print("Optimization successful!")
        
        # Extract optimized components
        optimized_components = {}
        for entity_id, components_dict in optimized_result['optimized_components'].items():
            optimized_components[entity_id] = {}
            for comp_id, comp_json in components_dict.items():
                optimized_components[entity_id][comp_id] = json.loads(comp_json)
        
        # Analyze the optimized deal
        optimized_analysis = hms_core.trade_balance_analyze_win_win_py(
            json.dumps(entity_profiles),
            json.dumps(optimized_components)
        )
        
        print(f"Optimized is win-win: {optimized_analysis['is_win_win']}")
```

### Running the Example Analysis

```python
# Run the built-in example analysis
example_result = hms_core.trade_balance_run_example_analysis_py()
print(f"Example is win-win: {example_result['is_win_win']}")
```