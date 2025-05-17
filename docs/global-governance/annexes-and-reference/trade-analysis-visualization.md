# Trade Analysis Visualization Guide

HMS-CDF provides powerful visualization capabilities for trade policy analysis. This guide demonstrates how to create comprehensive visualizations that explain the fiscal side of trade policies.

## Visualization Types

The HMS-CDF visualization system supports multiple types of economic data visualizations:

1. **Time Series Charts**: Display trends over time for metrics like GDP growth, trade volume, and employment
2. **Comparative Bar Charts**: Compare impacts across sectors, countries, or policies
3. **Heat Maps**: Show intensity of impacts across geographic regions
4. **Sankey Diagrams**: Visualize flow of goods, services, and capital
5. **Radar Charts**: Compare multi-dimensional policy impacts
6. **Economic Dashboards**: Integrated views combining multiple visualization types

## Example: Comprehensive Trade Agreement Analysis

Below is an example of visualizing the fiscal impacts of a multilateral trade agreement:

### GDP Impact Analysis

```javascript
// Create a GDP impact chart
const gdpChart = cdfClient.visualization.createTimeSeriesChart({
  title: 'GDP Growth Projections (2025-2030)',
  data: economicImpact.gdpProjections,
  scenarios: ['baseline', 'agreement_implementation', 'optimal_implementation'],
  annotations: [
    {
      type: 'line',
      value: 3.2,
      label: 'Historical Average Growth Rate',
      style: 'dashed'
    },
    {
      type: 'range',
      startValue: '2026-07',
      endValue: '2027-06',
      label: 'Implementation Period',
      style: 'highlight'
    }
  ],
  yAxisLabel: 'Annual GDP Growth (%)',
  xAxisLabel: 'Year',
  legendPosition: 'bottom'
});
```

![GDP Impact Chart](../assets/trade_analysis/gdp_impact_chart.png)

### Sectoral Impact Analysis

```javascript
// Create a sectoral impact chart
const sectoralChart = cdfClient.visualization.createBarChart({
  title: 'Sectoral Growth Impact (% Change)',
  data: economicImpact.sectoralImpacts,
  primaryDimension: 'sector',
  metrics: ['growth_change', 'export_growth', 'employment_change'],
  sortBy: 'growth_change',
  sortDirection: 'descending',
  colors: ['#4285F4', '#34A853', '#FBBC05'],
  yAxisLabel: 'Percentage Change (%)',
  xAxisLabel: 'Economic Sector',
  showValues: true,
  maxItems: 10
});
```

![Sectoral Impact Chart](../assets/trade_analysis/sectoral_impact_chart.png)

### Trade Balance Projection

```javascript
// Create a trade balance chart
const tradeBalanceChart = cdfClient.visualization.createAreaChart({
  title: 'Trade Balance Projection (2025-2030)',
  data: economicImpact.tradeBalanceProjections,
  scenarios: ['baseline', 'agreement_implementation'],
  areaStyle: 'stacked',
  yAxisLabel: 'Trade Balance (Billions USD)',
  xAxisLabel: 'Year',
  annotations: [
    {
      type: 'threshold',
      value: 0,
      label: 'Balance Point',
      style: 'solid'
    }
  ],
  includeDataTable: true
});
```

![Trade Balance Chart](../assets/trade_analysis/trade_balance_chart.png)

### Employment Impact Visualization

```javascript
// Create an employment impact chart
const employmentChart = cdfClient.visualization.createStackedBarChart({
  title: 'Job Creation by Sector (5-Year Projection)',
  data: economicImpact.employmentImpacts,
  primaryDimension: 'sector',
  stackDimension: 'job_category',
  metrics: ['job_count'],
  sortBy: 'job_count',
  sortDirection: 'descending',
  yAxisLabel: 'Jobs Created',
  xAxisLabel: 'Economic Sector',
  showTotal: true,
  maxItems: 8
});
```

![Employment Impact Chart](../assets/trade_analysis/employment_impact_chart.png)

## Creating a Comprehensive Dashboard

To create a complete fiscal policy dashboard that incorporates all visualizations:

```javascript
// Create a comprehensive dashboard
const dashboard = cdfClient.visualization.createDashboard({
  title: 'Comprehensive Trade Agreement Analysis',
  description: 'Fiscal and economic impacts of the proposed multilateral trade agreement',
  visualizations: [
    { visualization: gdpChart, gridPosition: { x: 0, y: 0, w: 6, h: 4 } },
    { visualization: sectoralChart, gridPosition: { x: 6, y: 0, w: 6, h: 4 } },
    { visualization: tradeBalanceChart, gridPosition: { x: 0, y: 4, w: 8, h: 4 } },
    { visualization: employmentChart, gridPosition: { x: 8, y: 4, w: 4, h: 4 } }
  ],
  summary: economicImpact.executiveSummary,
  filters: [
    { dimension: 'year', type: 'range', defaultValue: [2025, 2030] },
    { dimension: 'scenario', type: 'select', defaultValue: 'agreement_implementation' },
    { dimension: 'sector', type: 'multiSelect', defaultValue: ['all'] }
  ],
  exportFormats: ['pdf', 'png', 'csv'],
  autoRefresh: false,
  theme: 'light'
});

// Export or display the dashboard
const dashboardUrl = await cdfClient.visualization.publish(dashboard.id);
console.log(`Dashboard published at: ${dashboardUrl}`);
```

![Comprehensive Dashboard](../assets/trade_analysis/comprehensive_dashboard.png)

## Integration with Reports

These visualizations can be integrated into formal trade policy reports:

```javascript
// Create a formal trade policy report with visualizations
const report = await cdfClient.reports.create({
  title: 'Economic and Fiscal Impact Assessment',
  subtitle: 'Multilateral Digital Economy Trade Agreement',
  includeExecutiveSummary: true,
  sections: [
    {
      title: 'Macroeconomic Impacts',
      content: `The proposed agreement is projected to increase GDP growth by 0.7 percentage 
                points annually over the baseline scenario. This growth acceleration is 
                primarily driven by expanded market access and regulatory harmonization.`,
      visualizations: [gdpChart.id]
    },
    {
      title: 'Sectoral Analysis',
      content: `Impact varies significantly across sectors, with digital services, advanced 
                manufacturing, and financial services seeing the strongest positive effects. 
                Traditional sectors show modest but positive growth as well.`,
      visualizations: [sectoralChart.id]
    },
    {
      title: 'Trade Balance Effects',
      content: `The agreement is projected to improve the trade balance by $45 billion 
                annually by year 5, primarily through increased exports of digital services 
                and high-value manufactured goods.`,
      visualizations: [tradeBalanceChart.id]
    },
    {
      title: 'Employment and Labor Market Impacts',
      content: `An estimated 1.2 million new jobs are projected over five years, with 65% 
                in high-skill sectors. Regional distribution analysis shows benefits across 
                all major metropolitan areas.`,
      visualizations: [employmentChart.id]
    },
    {
      title: 'Comprehensive Assessment',
      content: `The overall fiscal impact is positive, with increased tax revenues exceeding 
                any implementation costs by year 3. The benefit-cost ratio is estimated at 4.7:1 
                over the 10-year projection period.`,
      visualizations: [dashboard.id]
    }
  ],
  appendices: [
    {
      title: 'Methodology',
      content: `This analysis employs a computable general equilibrium model calibrated with 
                current economic data. Sensitivity analysis was performed across key parameters.`
    },
    {
      title: 'Data Sources',
      content: `Economic data sourced from Bureau of Economic Analysis, Trade Representative 
                Office, and industry association reports from 2023-2025.`
    }
  ],
  format: 'pdf',
  includeTableOfContents: true,
  includeDateOnCover: true
});

console.log(`Report generated: ${report.downloadUrl}`);
```

## Data Export for Further Analysis

The visualization system allows exporting the underlying data for further analysis:

```javascript
// Export the underlying data
const exportedData = await cdfClient.visualization.exportData({
  visualizationIds: [
    gdpChart.id,
    sectoralChart.id,
    tradeBalanceChart.id,
    employmentChart.id
  ],
  format: 'csv',
  includeMetadata: true,
  dateFormat: 'ISO'
});

console.log(`Data exported to: ${exportedData.downloadUrl}`);
```

## Conclusion

HMS-CDF's visualization capabilities provide powerful tools for explaining the fiscal side of trade policies. By combining economic data, statistical analysis, and interactive visualizations, policymakers can better understand and communicate the impacts of trade agreements and other economic policies.

For more information on visualization options, see the [HMS-CDF Visualization API Reference](../api-reference/visualization-api.md).