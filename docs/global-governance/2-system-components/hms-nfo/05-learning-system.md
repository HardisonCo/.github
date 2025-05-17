# Learning System

The Learning System is a critical component of HMS-NFO that enables continuous improvement of knowledge quality, query responses, and analytics through feedback loops and performance tracking.

## System Architecture

The learning process operates through:

1. **Query Logging**: Recording all knowledge requests and responses
2. **Performance Monitoring**: Tracking response accuracy and confidence
3. **Feedback Collection**: Gathering explicit and implicit user feedback
4. **Pattern Recognition**: Identifying areas for knowledge enhancement
5. **Model Refinement**: Continuously improving response generation
6. **Source Prioritization**: Optimizing data collection based on impact

## Core Components

### Query Logger

```python
class QueryLogger:
    """
    Records all knowledge queries and responses for learning.
    Anonymizes sensitive information while preserving learning value.
    """
    def __init__(self, log_path="logs/query_log.jsonl"):
        self.log_path = log_path
        self.current_log = []
        self.flush_threshold = 100
        
    def log_query(self, query_text, response, confidence, agent_id=None, context=None):
        """Log a query and its response"""
        entry = {
            "timestamp": self._get_timestamp(),
            "query": query_text,
            "response_summary": self._summarize_response(response),
            "confidence": confidence,
            "agent_id": agent_id,
            "context_type": self._get_context_type(context)
        }
        
        self.current_log.append(entry)
        
        if len(self.current_log) >= self.flush_threshold:
            self.flush_logs()
            
    def flush_logs(self):
        """Write current logs to storage"""
        
    def _summarize_response(self, response):
        """Create a summary of the response, removing sensitive details"""
        
    def _get_context_type(self, context):
        """Extract the type of context without specific details"""
```

### Feedback Collector

```python
class FeedbackCollector:
    """
    Gathers explicit and implicit feedback on knowledge responses.
    Correlates feedback with query patterns for learning.
    """
    def __init__(self, feedback_db_path="learning/feedback.db"):
        self.feedback_db = self._initialize_db(feedback_db_path)
        
    def record_explicit_feedback(self, query_id, rating, comments=None):
        """Record explicit user feedback on a response"""
        
    def record_implicit_feedback(self, query_id, user_actions):
        """Record implicit feedback based on user actions after response"""
        
    def calculate_feedback_score(self, query_pattern):
        """Calculate aggregated feedback score for a query pattern"""
        
    def identify_improvement_areas(self):
        """Identify areas where responses consistently receive poor feedback"""
```

### Knowledge Gap Analyzer

```python
class KnowledgeGapAnalyzer:
    """
    Analyzes query patterns to identify gaps in the knowledge base.
    Prioritizes knowledge acquisition based on user needs.
    """
    def __init__(self, query_logger, feedback_collector):
        self.query_logger = query_logger
        self.feedback_collector = feedback_collector
        self.confidence_threshold = 0.7
        
    def identify_knowledge_gaps(self):
        """Identify areas where knowledge is missing or low-confidence"""
        
    def analyze_query_patterns(self):
        """Analyze patterns in user queries to predict future needs"""
        
    def prioritize_gap_filling(self):
        """Prioritize knowledge gaps for acquisition"""
        
    def generate_learning_targets(self):
        """Generate specific learning targets for the Internet Data Collection System"""
```

### Response Quality Trainer

```python
class ResponseQualityTrainer:
    """
    Improves response generation based on feedback and performance.
    Trains LLM prompts for better knowledge extraction and presentation.
    """
    def __init__(self, llm_client, response_templates_path="templates/responses.json"):
        self.llm_client = llm_client
        self.response_templates = self._load_templates(response_templates_path)
        self.training_data = []
        
    def collect_training_examples(self, query_logger, feedback_collector):
        """Collect positive and negative examples for training"""
        
    def optimize_response_templates(self):
        """Optimize response templates based on performance"""
        
    def train_confidence_estimator(self):
        """Improve confidence estimation accuracy"""
        
    def evaluate_improvements(self, test_queries):
        """Evaluate improvements in response quality"""
```

### Continuous Learning Manager

```python
class ContinuousLearningManager:
    """
    Orchestrates the overall learning process.
    Ensures systematic improvement of the knowledge system.
    """
    def __init__(
        self, 
        query_logger, 
        feedback_collector, 
        knowledge_gap_analyzer,
        response_quality_trainer
    ):
        self.query_logger = query_logger
        self.feedback_collector = feedback_collector
        self.knowledge_gap_analyzer = knowledge_gap_analyzer
        self.response_quality_trainer = response_quality_trainer
        self.learning_cycle_interval = 86400  # 24 hours
        
    def run_learning_cycle(self):
        """Execute a complete learning cycle"""
        
    def update_knowledge_priorities(self):
        """Update priorities for knowledge acquisition"""
        
    def refine_response_generation(self):
        """Refine response generation based on learning"""
        
    def measure_system_improvement(self):
        """Measure improvement in system performance"""
```

## Learning Metrics

The system tracks several key metrics for learning:

### Query Performance Metrics

- **Response Confidence**: Average confidence score of responses
- **Response Accuracy**: Percentage of responses rated positively
- **Response Latency**: Time to generate responses
- **Knowledge Coverage**: Percentage of queries with high-confidence responses
- **Novelty Rate**: Percentage of unique queries never seen before

### Feedback Metrics

- **Explicit Feedback**: User ratings and comments
- **Implicit Feedback**: User actions following responses
- **Feedback Participation**: Percentage of queries receiving feedback
- **Satisfaction Trend**: Change in feedback ratings over time
- **Dissatisfaction Clusters**: Common themes in negative feedback

### Knowledge Growth Metrics

- **Knowledge Entities Added**: Rate of new entity addition
- **Relationship Density**: Growth in connections between entities
- **Confidence Improvement**: Increase in average confidence scores
- **Source Diversity**: Range of sources contributing to knowledge
- **Refresh Rate**: How frequently knowledge is updated

## Learning Feedback Loops

The Learning System implements several feedback loops:

### 1. Query-Driven Learning Loop

```
Query → Response → Feedback → Template Optimization → Improved Response
```

When users consistently find responses lacking for certain query types, the system optimizes response templates and query understanding.

### 2. Confidence Calibration Loop

```
Response + Confidence → Feedback → Confidence Model Adjustment → Better Calibration
```

The system learns to provide more accurate confidence scores by correlating predicted confidence with actual usefulness.

### 3. Knowledge Acquisition Loop

```
Knowledge Gap → Learning Target → Data Collection → Knowledge Integration → Gap Filled
```

Identified knowledge gaps drive targeted data collection to improve coverage in high-demand areas.

### 4. Source Quality Loop

```
Source → Knowledge → Response Quality → Source Value Assessment → Source Prioritization
```

Sources that consistently contribute to high-quality responses receive higher priority in the data collection process.

## Integration Points

The Learning System integrates with:

- **Internet Data Collection System**: Directs what data to prioritize collecting
- **Knowledge Integration Engine**: Provides feedback on knowledge quality and gaps
- **Data Access API**: Monitors query patterns and response performance
- **HMS-AGX**: Shares insights about knowledge representation effectiveness
- **HMS-ACT**: Receives feedback on actionable intelligence quality

## Learning System Dashboard

The Learning System provides a dashboard for monitoring system improvement:

```
HMS-NFO Learning System Performance Dashboard
Date: 2023-12-15

Query Performance:
- Queries Processed: 15,428 (↑12% from last period)
- Average Confidence: 0.83 (↑0.05 from last period)
- High Confidence Rate: 78% (↑6% from last period)
- Response Time: 125ms (↓15ms from last period)

Knowledge Quality:
- Entity Count: 152,384 (↑3,245 from last period)
- Relationship Count: 892,561 (↑15,892 from last period)
- Source Count: 324 (↑8 from last period)
- Top Knowledge Domain: Trade Economics (32% of queries)

Learning Activities:
- Knowledge Gaps Filled: 128
- Response Templates Optimized: 15
- New Data Sources Added: 8
- Confidence Model Recalibrations: 3

Top Areas for Improvement:
1. Regional Trade Agreement Specifics
2. Emerging Market Sector Growth Rates
3. Import Certificate Implementation Details
```

Through systematic learning and improvement, HMS-NFO continuously enhances its knowledge quality, response accuracy, and analytical capabilities, ensuring the entire HMS ecosystem benefits from increasingly valuable information resources.