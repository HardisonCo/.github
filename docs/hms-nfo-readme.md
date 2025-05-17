# HMS-NFO Data Model Generator

This tool crawls the HMS-NFO directory structure and uses LLM to create a concise government data model that can be accessed when needed. It includes integration with HMS-A2A specialized agents and HMS-AGX knowledge graph for enhanced capabilities, with FULL access to trade systems and Moneyball economics.

## Features

- Fast directory crawling with pattern filtering
- Parallel processing of data using thread pools
- LLM-powered extraction of government data entities and relationships
- Queryable data model for accessing government data on demand
- Automatic merging and refinement of extracted information
- Confidence scoring with learning trigger for low-confidence responses
- HMS-A2A agent integration for specialized agent queries
- HMS-AGX knowledge graph integration for supplementary information
- REST API server mode for programmatic access
- **FULL access to all trade system aspects**
- **Comprehensive Moneyball economics documentation**

## Requirements

- Python 3.7+
- OpenAI API key set in environment variable `OPENAI_API_KEY`
- Google Gemini API key (optional fallback) set in environment variable `GEMINI_API_KEY`
- Flask (optional, for API server mode): `pip install flask`
- Requests: `pip install requests`

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your API keys:
   ```
   export OPENAI_API_KEY="your-openai-api-key"
   export GEMINI_API_KEY="your-gemini-api-key"  # Optional
   ```

## Usage

### Generate Data Model

To generate a data model from the HMS-NFO directory:

```bash
python hms_nfo_data_model.py --dir /Users/arionhardison/Desktop/CodifyHQ/HMS-NFO --output hms_nfo_data_model.json
```

The script will:
1. Crawl the directory structure
2. Process files in parallel using LLM
3. Merge and refine the extracted information
4. Save the result to the specified output file

### Query Data Model

Once you've generated the data model, you can query it with natural language:

```bash
python hms_nfo_data_model.py --query "What are the main funding entities and their relationships?"
```

The response will include a confidence score. If the confidence is below the threshold (default 0.7), you'll be prompted to trigger the learning process.

### Agent Queries

Specialized agents can query the data model directly:

```bash
python hms_nfo_data_model.py --query "What funding programs are available for healthcare initiatives?" --agent healthcare
```

When an agent query has low confidence, the learning process is triggered automatically.

### Run API Server

You can run the script as an API server to allow programmatic access:

```bash
python hms_nfo_data_model.py serve
```

This starts a Flask server on port 5000 with these endpoints:
- `POST /api/query`: Submit a query (requires JSON with `query`, optional `agent_id` and `context`)
- `GET /api/health`: Check if the server is running

### Customize Confidence Threshold

You can adjust the confidence threshold for triggering learning:

```bash
python hms_nfo_data_model.py --query "Your query" --threshold 0.5
```

## Integration with HMS Systems

### HMS-A2A Integration

The tool integrates with HMS-A2A specialized agents located at `/Users/arionhardison/Desktop/CodifyHQ/HMS-A2A/specialized_agents`. Agents can query the data model and receive responses with confidence scores. When confidence is low, the system automatically triggers learning to improve future responses.

### HMS-AGX Knowledge Graph

The tool uses HMS-AGX as a supplementary knowledge source. It first attempts to connect to a running HMS-AGX API server, and if unavailable, falls back to LLM-based knowledge extraction. For trade and finance queries, the knowledge graph specifically includes trade system components and Moneyball economic principles.

### HMS-NFO Learning

When confidence is below the threshold, the system triggers a learning process that:
1. Identifies knowledge gaps in the current model
2. Suggests missing entities and relationships
3. Recommends model updates
4. Provides an improved response
5. Logs the learning event for future reference

### Trade System & Moneyball Economics

The system provides FULL access to all aspects of the trade system including:
1. **Import Certificates (Warren Buffett model)** - Tradable certificates for balancing trade and funding development
2. **Dynamic Tariff Adjustments** - Progressive tariff structures linked to development goals
3. **Moneyball Economic Analysis** - Identification of undervalued sectors using statistical methods
4. **Development Project Financing** - Mechanisms for funding international development through trade
5. **Domestic Program Funding** - Allocation of efficiency gains to domestic education, healthcare, and infrastructure
6. **Nth Degree Deal Chains** - Multi-country transaction sequences optimized for global resource allocation
7. **Gov/Civ 'Win-Win' Framework** - Ensures balanced benefits across government and civilian sectors
8. **Trade WAR Metrics** - "Wins Above Replacement" evaluation system for measuring deal effectiveness

The finance/econ section includes comprehensive documentation of both trade system mechanics and Moneyball economics principles with detailed explanations of their applications to government contexts.

## Data Model Structure

The generated data model follows this enhanced structure:

```json
{
  "entities": [
    {
      "name": "entity_name",
      "description": "concise description",
      "attributes": ["attr1", "attr2"],
      "relationships": [
        { "related_to": "other_entity", "relationship_type": "type", "description": "short description" }
      ]
    }
  ],
  "data_flows": [
    { "source": "entity1", "destination": "entity2", "data_type": "type", "description": "description" }
  ],
  "governance": [
    { "entity": "governing_body", "scope": "what_it_governs", "authorities": ["authority1", "authority2"] }
  ],
  "access_patterns": [
    { "use_case": "scenario", "data_needed": ["entity1.attr1", "entity2.attr2"], "access_level": "level" }
  ],
  "trade_systems": [
    {
      "name": "system_name",
      "description": "detailed description",
      "components": ["component1", "component2"],
      "financial_mechanisms": [
        { "name": "mechanism_name", "purpose": "detailed purpose", "operation": "detailed operation description" }
      ]
    }
  ],
  "moneyball_economics": [
    {
      "principle": "principle_name",
      "description": "detailed description",
      "application": "government application details",
      "metrics": ["metric1", "metric2"]
    }
  ]
}
```

## Performance Notes

- The script uses chunking to process large directories efficiently
- Threading allows parallel LLM API calls
- Caching reduces duplicate LLM calls for repeated content
- Set `MAX_PARALLEL_TASKS` and `CHUNK_SIZE` constants to adjust performance based on your system and API limits

## Troubleshooting

If you encounter issues:

1. Check API key environment variables are set correctly
2. Verify the HMS-NFO directory path is correct
3. Check the logs directory for detailed LLM call logs
4. For large directories, consider adjusting the chunking parameters
5. If HMS-AGX integration fails, ensure the service is running or increase the socket timeout
6. If agent queries fail, ensure the HMS-A2A directory structure is valid