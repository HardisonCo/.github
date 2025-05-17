# Trade Opportunity Analysis with HMS-NFO

## Overview

This tutorial demonstrates how to use HMS-NFO to identify and analyze trade opportunities using the Moneyball Analytics Framework. You'll learn how to find undervalued sectors, analyze potential partnerships, and create optimized trade strategies.

## Prerequisites

- HMS-NFO API access
- Python 3.7+
- pandas, matplotlib, and numpy libraries
- Basic understanding of trade economics

## Finding Undervalued Opportunities

```python
from hms_nfo import NfoClient
from hms_nfo.components import moneyballanalyticsframework as mbaf
import pandas as pd
import matplotlib.pyplot as plt

# Initialize client
client = NfoClient(api_key='YOUR_API_KEY')
moneyball = client.get_component('moneyball_analytics_framework')

# Set up opportunity search parameters
search_params = {
    'source_country': 'USA',
    'target_regions': ['ASIA', 'SOUTH_AMERICA'],
    'sectors': 'all',
    'min_score': 0.7,
    'risk_tolerance': 'moderate',
    'time_horizon': 'medium'  # 1-3 years
}

# Run the search
opportunities = moneyball.find_opportunities(search_params)

# Convert to DataFrame for easier analysis
opp_df = pd.DataFrame(opportunities)

# Display top opportunities by score
top_opps = opp_df.sort_values('opportunity_score', ascending=False).head(10)
print(top_opps[['country', 'sector', 'opportunity_score', 'estimated_value']])

# Visualize opportunities by region and sector
plt.figure(figsize=(12, 8))
for region in opp_df['region'].unique():
    region_data = opp_df[opp_df['region'] == region]
    plt.scatter(
        region_data['risk_factor'], 
        region_data['opportunity_score'],
        s=region_data['estimated_value'] / 1e6,  # Size by value in millions
        alpha=0.7,
        label=region
    )

plt.xlabel('Risk Factor')
plt.ylabel('Opportunity Score')
plt.title('Trade Opportunities by Region, Risk, and Value')
plt.grid(True)
plt.legend()
plt.savefig('trade_opportunities.png')
plt.show()
```

## Analyzing Specific Country Pairs

```python
# Analyze USA-Brazil trade relationship
country_pair_analysis = moneyball.analyze_country_pair('USA', 'BRA')

# Display complementary sectors
print("Complementary Sectors:")
for sector in country_pair_analysis['complementary_sectors']:
    print(f"- {sector['name']}: Score {sector['score']}")
    print(f"  USA Strength: {sector['usa_strength']}")
    print(f"  Brazil Strength: {sector['brazil_strength']}")
    print(f"  Opportunity Value: ${sector['opportunity_value']:,.2f}")

# Get tariff optimization recommendations
tariff_recs = moneyball.optimize_tariffs('USA', 'BRA')
print("\nTariff Optimization Recommendations:")
for rec in tariff_recs:
    print(f"- Sector: {rec['sector']}")
    print(f"  Current Rate: {rec['current_rate']}%")
    print(f"  Recommended Rate: {rec['recommended_rate']}%")
    print(f"  Estimated Impact: ${rec['estimated_impact']:,.2f}")
```

## Creating an Optimized Portfolio

```python
# Define portfolio parameters
portfolio_params = {
    'base_country': 'USA',
    'target_countries': ['JPN', 'BRA', 'IND', 'KOR', 'DEU'],
    'max_risk_exposure': 0.4,  # Maximum risk tolerance (0-1)
    'sectors': ['technology', 'agriculture', 'manufacturing', 'pharmaceuticals'],
    'optimization_goal': 'balanced'  # Options: value, risk, balanced
}

# Generate optimized portfolio
portfolio = moneyball.create_optimized_portfolio(portfolio_params)

print(f"Portfolio WAR Score: {portfolio['war_score']}")
print(f"Portfolio Risk Level: {portfolio['risk_level']}")
print(f"Expected Annual Value: ${portfolio['expected_annual_value']:,.2f}")

# Display country allocations
print("\nCountry Allocations:")
for country in portfolio['countries']:
    print(f"- {country['name']}: {country['allocation']}%")
    print(f"  Key Sectors: {', '.join(country['key_sectors'])}")
    print(f"  Expected Value: ${country['expected_value']:,.2f}")
```

## Best Practices

1. **Validate with Real Data**: Always cross-reference Moneyball insights with real-world data
2. **Consider Non-Quantitative Factors**: Political relationships and cultural factors matter
3. **Regular Rebalancing**: Update your analysis quarterly as conditions change
4. **Risk Management**: Diversify across regions and sectors to minimize exposure
5. **Incremental Implementation**: Start with small, focused initiatives to validate the approach

## Additional Resources

- [Moneyball Analytics Documentation](../components/moneyball_analytics_framework.md)
- [Country Trade Models Reference](../api-reference/country-models.md)
- [HMS-NFO Data Sources](../references/data-sources.md)
- [Case Studies: Successful Implementations](../case-studies/index.md)
