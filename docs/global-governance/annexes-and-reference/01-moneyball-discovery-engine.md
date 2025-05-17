# Moneyball Discovery Engine

## Overview

The Moneyball Discovery Engine is a core component of the HMS-MBL system that applies statistical and analytical methods to identify undervalued trade opportunities between countries. Inspired by the "Moneyball" approach used in sports analytics, this engine focuses on finding market inefficiencies and opportunities that traditional trade analysis might overlook.

## Key Components

### UndervaluedSectorFinder

The primary class that implements Moneyball-style analytics for international trade. It focuses on identifying sectors with high growth potential but low current investment or attention.

Key functionality:
- Evaluates undervalued sectors across country pairs
- Calculates opportunity scores based on multiple factors
- Assesses complementarity between countries' economic strengths
- Calculates "Trade WAR" (Wins Above Replacement) metrics

#### Finding Opportunities

```python
def find_opportunities(self, 
                      source_country: str, 
                      target_country: str,
                      min_opportunity_score: float = 1.2) -> List[Dict]:
    """
    Find undervalued sector opportunities between countries.
    """
```

The opportunity score considers factors such as:
- Historical growth rates vs. traditional focus
- Export/import complementarity
- Undervaluation metrics in either country's model

#### Trade WAR Components

The system calculates Trade WAR (Wins Above Replacement) metrics:

```python
def calculate_trade_war_components(self, country_a: str, country_b: str) -> Dict[str, float]:
    """
    Calculate Trade WAR (Wins Above Replacement) component metrics.
    """
```

Components include:
- **Volume Potential**: GDP-weighted trade capacity
- **Complementarity**: How well sectors complement each other
- **Risk-Adjusted Return**: Balance of opportunity vs. risk
- **Diplomatic Factor**: Relationship quality
- **Innovation Potential**: Combined growth in advanced sectors

### MoneyballDealDesigner

This class designs optimized trade deals using Moneyball principles, focusing on creating balanced deals that highlight undervalued opportunities.

Key functionality:
- Creates balanced trade deals between country pairs
- Generates tariff recommendations based on opportunity scores
- Provides non-tariff recommendations to maximize deal potential

#### Balanced Deal Design

```python
def design_balanced_deal(self, 
                        country_a: str, 
                        country_b: str,
                        min_sectors: int = 3,
                        max_sectors: int = 8) -> Dict:
    """
    Design a balanced trade deal focusing on undervalued sectors.
    """
```

The system attempts to balance value between countries by:
- Finding opportunities in both directions
- Calculating expected value for each direction
- Adding lower-priority opportunities to balance the deal
- Ensuring minimum sector coverage

## Integration Points

The Moneyball Discovery Engine integrates with:
- Country Trade Models (via the `CountryTradeModel` class)
- Trade visualization components
- Policy recommendation systems
- Deal negotiation frameworks

## Technical Characteristics

- **Data-Driven**: Relies on statistical analysis rather than traditional trade metrics
- **Balanced Approach**: Focuses on creating equitable value distribution
- **Undervalued Sector Focus**: Prioritizes sectors with high-growth potential that may be overlooked
- **Adaptable**: Can be customized with different metrics and scoring systems