# Data Access API

The Data Access API is the primary interface through which other HMS components interact with the HMS-NFO knowledge repository. It provides standardized methods for querying, retrieving, and in some cases updating the system's knowledge base.

## API Architecture

The Data Access API follows these design principles:

1. **Unified Interface**: Single consistent interface across all knowledge domains
2. **Contextual Queries**: Support for rich context-aware information retrieval
3. **Confidence Scores**: All responses include confidence metrics
4. **Security Layers**: Role-based access controls for sensitive information
5. **Performance Optimization**: Caching and query optimization for responsive results
6. **Versioning**: Support for accessing historical knowledge states

## Core Components

### NFO Data Access Service

```python
class HmsNfoDataAccess:
    """
    Primary interface for accessing HMS-NFO data.
    Provides methods for querying the knowledge base with context.
    """
    def __init__(self, config_path="config/nfo_access.json", ensure_model_exists=False):
        self.config = self._load_config(config_path)
        self.knowledge_graph = self._initialize_knowledge_graph()
        self.llm_client = self._initialize_llm()
        self.cache = QueryCache()
        
        if ensure_model_exists:
            self._ensure_model_exists()
            
    def query(self, query_text, agent_id=None, context=None):
        """
        Query the knowledge base with natural language.
        
        Args:
            query_text: Natural language query
            agent_id: Optional identifier of the querying agent
            context: Optional context dictionary to enhance query relevance
            
        Returns:
            Tuple of (response_text, confidence_score)
        """
        # Check cache first
        cache_key = self._generate_cache_key(query_text, context)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
            
        # Process the query
        structured_query = self._structure_query(query_text, context)
        raw_results = self.knowledge_graph.execute_query(structured_query)
        
        # Generate response with LLM
        response, confidence = self._generate_response(query_text, raw_results, context)
        
        # Cache the result
        self.cache.store(cache_key, (response, confidence))
        
        # Log the query for learning
        self._log_query(query_text, response, confidence, agent_id)
        
        return response, confidence
        
    def enrich_moneyball_discovery(self, discovery_input):
        """
        Enrich Moneyball discovery with additional knowledge.
        
        Args:
            discovery_input: Dictionary with discovery parameters
            
        Returns:
            Enhanced discovery data with additional metrics and insights
        """
        # Implementation details for enriching Moneyball analytics
```

### Query Processor

```python
class QueryProcessor:
    """
    Processes natural language queries into structured knowledge graph queries.
    Uses LLM-assisted query formulation for complex information needs.
    """
    def __init__(self, llm_client, query_templates_path="templates/queries.json"):
        self.llm_client = llm_client
        self.query_templates = self._load_templates(query_templates_path)
        
    def structure_query(self, query_text, context=None):
        """Convert natural language query to structured knowledge graph query"""
        
    def identify_query_type(self, query_text):
        """Identify the type of query to select appropriate templates"""
        
    def extract_query_parameters(self, query_text, query_type):
        """Extract parameters from query text for template filling"""
```

### Response Generator

```python
class ResponseGenerator:
    """
    Generates natural language responses from query results.
    Ensures responses are accurate, relevant, and properly cited.
    """
    def __init__(self, llm_client, response_templates_path="templates/responses.json"):
        self.llm_client = llm_client
        self.response_templates = self._load_templates(response_templates_path)
        
    def generate_response(self, query, results, context=None):
        """Generate natural language response from query results"""
        
    def calculate_confidence(self, results):
        """Calculate overall confidence score for the response"""
        
    def add_citations(self, response, results):
        """Add source citations to the response when appropriate"""
```

### Query Cache

```python
class QueryCache:
    """
    Caches query results for improved performance.
    Implements intelligent cache invalidation based on knowledge updates.
    """
    def __init__(self, max_size=1000, ttl=3600):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        self.access_history = {}
        
    def get(self, cache_key):
        """Get cached result if available and valid"""
        
    def store(self, cache_key, result):
        """Store result in cache"""
        
    def invalidate(self, entity_id):
        """Invalidate cache entries related to an entity"""
```

## API Endpoints

When running in server mode, the following REST endpoints are exposed:

### Knowledge Query

```
POST /api/v1/query
```

Request:
```json
{
  "query": "What undervalued sectors exist between USA and Vietnam?",
  "agent_id": "moneyball_discovery",
  "context": {
    "source_country": "USA",
    "target_country": "VNM",
    "operation": "find_opportunities"
  }
}
```

Response:
```json
{
  "response": "The most undervalued sectors between USA and Vietnam include advanced manufacturing (score 2.34), renewable energy (score 2.15), and digital services (score 1.98). The USA has export strengths in advanced manufacturing and digital services that complement Vietnam's growing industrial base, while Vietnam shows potential in renewable energy component manufacturing that could benefit USA's green energy transition.",
  "confidence": 0.87,
  "sources": [
    {"name": "WTO Trade Statistics 2023", "relevance": 0.92},
    {"name": "US-Vietnam Trade Report Q2 2023", "relevance": 0.85}
  ]
}
```

### Moneyball Analytics

```
POST /api/v1/moneyball/analyze
```

Request:
```json
{
  "country_a": "USA",
  "country_b": "VNM",
  "sectors": ["technology", "manufacturing", "agriculture"],
  "analysis_type": "opportunity"
}
```

Response:
```json
{
  "opportunities": [
    {
      "sector": "advanced_manufacturing",
      "opportunity_score": 2.34,
      "growth_rate": 5.5,
      "complementarity": 0.68,
      "recommendation": "Immediate focus opportunity"
    }
  ],
  "trade_war_score": 3.75,
  "confidence": 0.85
}
```

### Entity Information

```
GET /api/v1/entity/{entity_id}
```

Response:
```json
{
  "entity_id": "country:usa",
  "type": "country",
  "names": {
    "official": "United States of America",
    "short": "USA"
  },
  "attributes": {
    "gdp": {
      "value": 25460000000000.0,
      "unit": "USD",
      "year": 2023
    }
  },
  "confidence": 0.98
}
```

## Integration Patterns

### Python SDK

```python
from utils.nfo_data_access import HmsNfoDataAccess

# Initialize the client
nfo_client = HmsNfoDataAccess(ensure_model_exists=True)

# Example query
query = "What undervalued sectors exist between USA and Vietnam?"
context = {
    "source_country": "USA",
    "target_country": "VNM",
    "operation": "find_opportunities"
}

response, confidence = nfo_client.query(query, agent_id="moneyball_discovery", context=context)

if confidence >= 0.6:
    print(f"Found insights with {confidence:.2f} confidence: {response}")
else:
    print("No high-confidence insights available")
```

### Batch Processing

```python
results = nfo_client.batch_query([
    {"query": "Trade balance between USA and China", "context": {"year": 2023}},
    {"query": "Top export sectors for Vietnam", "context": {"limit": 5}},
    {"query": "Warren Buffett import certificate impact on trade deficit", "context": {"country": "USA"}}
])

for query_result in results:
    print(f"Query: {query_result['query']}")
    print(f"Response: {query_result['response']}")
    print(f"Confidence: {query_result['confidence']}")
```

## Security Model

The Data Access API implements:

- **Authentication**: API keys and JWT-based authentication
- **Authorization**: Role-based access to different knowledge domains
- **Data Classification**: Labeling of sensitive information
- **Query Logging**: Comprehensive audit trail of all queries
- **Rate Limiting**: Protection against excessive usage
- **Data Provenance**: Tracking of information sources and lineage

## Performance Considerations

The API is optimized for:

- **Query Response Time**: < 200ms for cached queries, < 2s for complex queries
- **Throughput**: Support for 1000+ queries per minute
- **Availability**: 99.9% uptime with redundant deployment
- **Scalability**: Horizontal scaling for increased load
- **Cache Efficiency**: > 80% cache hit rate for common queries

Through this sophisticated API, the HMS-NFO knowledge repository becomes a powerful resource for all HMS components, providing accurate, context-aware information about government systems, trade relationships, and economic opportunities.