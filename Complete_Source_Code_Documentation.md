# Complete Source Code Documentation
## Math Professor Agent - Agentic RAG System

### Document Information
- **Project**: Math Professor Agent - Complete Source Code Analysis
- **Document Type**: Source Code Architecture Documentation
- **Version**: 1.0
- **Date**: November 1, 2024
- **Total Files**: 35+ source files analyzed
- **Lines of Code**: ~3,500+ lines

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Code Architecture Overview](#code-architecture-overview)
3. [Backend Components Analysis](#backend-components-analysis)
4. [Frontend Components Analysis](#frontend-components-analysis)
5. [Data Flow & Interactions](#data-flow--interactions)
6. [Key Design Patterns](#key-design-patterns)
7. [Component Dependencies](#component-dependencies)
8. [API Integration Points](#api-integration-points)
9. [Configuration Management](#configuration-management)
10. [Error Handling Strategy](#error-handling-strategy)

---

## Executive Summary

The Math Professor Agent is a sophisticated Agentic-RAG system built with modern software architecture principles. The codebase demonstrates production-ready practices with clear separation of concerns, comprehensive error handling, and scalable design patterns.

### Key Architecture Highlights
- **Modular Design**: 9 backend modules, each with single responsibility
- **Type Safety**: Comprehensive Pydantic models for data validation
- **Async Architecture**: Non-blocking operations throughout
- **State Management**: LangGraph for complex workflow orchestration
- **Configuration-Driven**: Environment-based configuration management
- **Comprehensive Logging**: Structured logging with Loguru
- **Error Resilience**: Graceful degradation and fallback mechanisms

---

## Code Architecture Overview

### System Architecture Layers
```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  React Frontend (Port 3000) + FastAPI Docs (Port 8000)     │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│     FastAPI Backend + LangGraph Agent Orchestration        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     BUSINESS LAYER                          │
│   Guardrails + Router + Knowledge Base + Web Search        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                             │
│      Qdrant Vector DB + External APIs + File Storage       │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure Analysis
```
math-professor-agent/
├── backend/                 # Python FastAPI Backend (9 modules)
│   ├── main.py             # FastAPI application entry point
│   ├── agent.py            # LangGraph agent orchestration
│   ├── guardrails.py       # Multi-layer content filtering
│   ├── knowledge_base.py   # Qdrant vector database integration
│   ├── web_search.py       # Tavily API web search
│   ├── feedback_system.py  # Human-in-the-loop with DSPy
│   ├── benchmark.py        # JEE Bench evaluation system
│   ├── models.py           # Pydantic data models
│   └── config.py           # Configuration management
├── frontend/               # React Frontend Application
│   ├── src/App.js          # Main React component
│   ├── src/App.css         # Styling and UI design
│   └── public/index.html   # HTML template with KaTeX
├── data/                   # Data storage and examples
│   ├── dataset.json        # 515 JEE Advanced questions
│   ├── few_shot_examples.json # Training examples
│   └── feedback.json       # User feedback storage
└── scripts/                # Utility and setup scripts
    ├── setup_knowledge_base.py
    ├── test_system.py
    └── run_benchmark.py
```
---


## Backend Components Analysis

### 1. FastAPI Application (`main.py`)
**Purpose**: Central API server and application orchestration
**Lines of Code**: ~200 lines
**Key Responsibilities**:
- HTTP request handling and routing
- CORS middleware configuration
- Component initialization and dependency injection
- API key validation and health checks
- Structured logging configuration

**Code Structure**:
```python
# Core Components Initialization
app = FastAPI(title="Math Professor Agent API", version="1.0.0")
agent = MathProfessorAgent()
feedback_agent = FeedbackAgent()
benchmark_runner = BenchmarkRunner(agent)

# API Endpoints
@app.post("/api/query")           # Main query processing
@app.post("/api/feedback")        # Feedback submission
@app.get("/api/metrics")          # System metrics
@app.post("/api/benchmark")       # Benchmark evaluation
@app.get("/health")               # Health check with API status
```

**Key Features**:
- **Startup Validation**: Validates API keys on startup with detailed error messages
- **Error Handling**: Comprehensive exception handling with HTTP status codes
- **Logging Integration**: Structured logging with file rotation
- **CORS Configuration**: Cross-origin resource sharing for frontend integration

### 2. Agent System (`agent.py`)
**Purpose**: LangGraph-based workflow orchestration
**Lines of Code**: ~350 lines
**Key Responsibilities**:
- State-based workflow management
- Intelligent routing between knowledge base and web search
- Solution generation with LLM integration
- Confidence score calculation

**LangGraph Workflow Architecture**:
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    question: str
    route_decision: str
    retrieved_docs: list
    web_results: list
    answer: str
    step_by_step_solution: str
    confidence_score: float
    sources: list
    guardrail_passed: bool
    query_id: str

# Workflow Nodes
workflow.add_node("input_guardrail", self.input_guardrail_node)
workflow.add_node("router", self.router_node)
workflow.add_node("kb_retrieval", self.kb_retrieval_node)
workflow.add_node("web_search", self.web_search_node)
workflow.add_node("solution_generator", self.solution_generator_node)
workflow.add_node("output_guardrail", self.output_guardrail_node)
```

**Routing Logic**:
```python
# Intelligent routing based on similarity scores
if docs and docs[0].score >= settings.similarity_threshold:
    state["route_decision"] = RouteDecision.KNOWLEDGE_BASE.value
else:
    state["route_decision"] = RouteDecision.WEB_SEARCH.value
```

**Key Features**:
- **Conditional Routing**: Dynamic workflow paths based on similarity scores
- **State Management**: Comprehensive state tracking through workflow
- **Error Recovery**: Graceful handling of LLM API failures
- **Confidence Calculation**: Dynamic confidence scoring based on route and content

### 3. Guardrails System (`guardrails.py`)
**Purpose**: Multi-layer content filtering and safety
**Lines of Code**: ~200 lines
**Key Responsibilities**:
- Input content validation and filtering
- Output quality assurance
- Educational content verification
- Inappropriate content detection

**Multi-Layer Architecture**:
```python
# Layer 1: Rule-based filtering (fast)
educational_keywords = [
    'formula', 'equation', 'solve', 'calculate', 'trigonometry',
    'algebra', 'geometry', 'physics', 'chemistry', 'mathematics'
]

# Layer 2: LLM-based semantic check (accurate)
prompt = """You are a content filter for an educational math tutoring system.
Analyze this question and determine if it is educational and appropriate..."""
```

**Key Features**:
- **Defense in Depth**: Multiple validation layers
- **Performance Optimization**: Fast rule-based checks before LLM calls
- **Educational Focus**: Keyword-based educational content detection
- **Graceful Degradation**: Fails open if LLM checks fail

### 4. Knowledge Base (`knowledge_base.py`)
**Purpose**: Vector database management and semantic search
**Lines of Code**: ~150 lines
**Key Responsibilities**:
- Qdrant vector database integration
- Embedding generation and storage
- Semantic similarity search
- Batch processing for large datasets

**Vector Search Implementation**:
```python
class KnowledgeBase:
    def __init__(self):
        self.client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        self.encoder = SentenceTransformer(settings.embedding_model)
        self.embedding_dim = 384  # all-MiniLM-L6-v2 dimension
    
    def search(self, query: str, top_k: int = 3) -> List[RetrievedDocument]:
        query_vector = self.encoder.encode(query).tolist()
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
```

**Key Features**:
- **Efficient Indexing**: HNSW algorithm for fast similarity search
- **Batch Processing**: Optimized bulk data insertion
- **Metadata Storage**: Rich document metadata for filtering
- **Cosine Similarity**: Optimal for semantic text matching

### 5. Web Search Integration (`web_search.py`)
**Purpose**: External knowledge retrieval via Tavily API
**Lines of Code**: ~80 lines
**Key Responsibilities**:
- Tavily API integration for web search
- Educational domain filtering
- Result formatting for LLM consumption
- Error handling for API failures

**MCP Integration**:
```python
class WebSearchMCP:
    async def search(self, query: str, max_results: int = 5):
        response = await client.post(f"{self.base_url}/search", json={
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_domains": [
                "wikipedia.org", "mathworld.wolfram.com",
                "khanacademy.org", "brilliant.org"
            ]
        })
```

**Key Features**:
- **Domain Filtering**: Focus on educational sources
- **Advanced Search**: Deep search mode for better results
- **Result Formatting**: Structured output for LLM processing
- **Async Operations**: Non-blocking API calls### 6. F
eedback System (`feedback_system.py`)
**Purpose**: Human-in-the-loop learning with DSPy optimization
**Lines of Code**: ~250 lines
**Key Responsibilities**:
- User feedback collection and storage
- Response refinement based on feedback
- Statistics tracking and analysis
- DSPy integration for automated optimization

**Feedback Architecture**:
```python
class FeedbackAgent:
    def __init__(self):
        self.store = FeedbackStore()           # JSON-based storage
        self.optimizer = DSPyOptimizer()       # Response refinement
        self.response_cache = {}               # Response caching
    
    def process_feedback(self, feedback: FeedbackRequest):
        # Store feedback and update statistics
        self.store.add_feedback(feedback, original_response)
        
        # Refine response if incorrect
        if not feedback.is_correct:
            refined_solution = self.optimizer.refine_response(...)
```

**Statistics Tracking**:
```python
def _update_statistics(self):
    total = len(feedbacks)
    correct = sum(1 for f in feedbacks if f["is_correct"])
    avg_rating = sum(f["rating"] for f in feedbacks) / total
    
    # Route performance analysis
    route_stats = {}
    for f in feedbacks:
        route = f["route_used"]
        route_stats[route] = {"total": 0, "correct": 0}
```

**Key Features**:
- **Persistent Storage**: JSON-based feedback database
- **Real-time Statistics**: Dynamic performance metrics
- **Response Refinement**: DSPy-powered improvement generation
- **Route Analysis**: Performance tracking by routing decision

### 7. Benchmark System (`benchmark.py`)
**Purpose**: JEE Bench evaluation and performance measurement
**Lines of Code**: ~180 lines
**Key Responsibilities**:
- Dataset loading and processing
- Answer extraction and comparison
- Performance metrics calculation
- Result reporting and storage

**Evaluation Pipeline**:
```python
class BenchmarkRunner:
    async def run_benchmark(self, num_samples=None, subjects=None):
        dataset = self.load_dataset()
        
        for question_data in dataset:
            # Process through agent
            response = await self.agent.process_query(question_data['question'])
            
            # Extract and compare answers
            predicted_answer = self.extract_answer(response.step_by_step_solution)
            is_correct = self.compare_answers(predicted_answer, question_data['gold'])
            
            # Update metrics
            self._update_results(is_correct, question_data)
```

**Answer Comparison Logic**:
```python
def compare_answers(self, predicted: str, gold: str, question_type: str):
    if question_type == "MCQ":
        return predicted.upper() == gold.upper()
    elif question_type == "MCQ(multiple)":
        pred_set = set(predicted.replace(" ", ""))
        gold_set = set(gold.replace(" ", ""))
        return pred_set == gold_set
    else:  # Numeric/Integer
        try:
            return abs(float(predicted) - float(gold)) < 0.01
        except:
            return predicted == gold
```

**Key Features**:
- **Flexible Evaluation**: Support for different question types
- **Comprehensive Metrics**: Subject-wise and type-wise accuracy
- **Performance Tracking**: Response time and route distribution
- **Result Persistence**: JSON-based result storage

### 8. Data Models (`models.py`)
**Purpose**: Type-safe data structures and API contracts
**Lines of Code**: ~120 lines
**Key Responsibilities**:
- Pydantic model definitions
- Request/response validation
- Enum definitions for constants
- Type safety enforcement

**Core Models**:
```python
class QueryRequest(BaseModel):
    question: str = Field(..., description="The mathematical question to solve")
    user_id: Optional[str] = Field(None, description="Optional user identifier")

class QueryResponse(BaseModel):
    query_id: str
    question: str
    answer: str
    step_by_step_solution: str
    route_used: RouteDecision
    confidence_score: float
    sources: Optional[List[str]] = None
    timestamp: str

class FeedbackRequest(BaseModel):
    query_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    is_correct: bool
    feedback_text: Optional[str] = None
```

**Key Features**:
- **Type Safety**: Comprehensive type hints and validation
- **API Documentation**: Self-documenting with field descriptions
- **Validation Rules**: Built-in data validation (e.g., rating 1-5)
- **Enum Support**: Type-safe constants for routing decisions

### 9. Configuration Management (`config.py`)
**Purpose**: Centralized configuration and environment management
**Lines of Code**: ~80 lines
**Key Responsibilities**:
- Environment variable loading
- Default value management
- Path configuration
- Settings validation

**Configuration Structure**:
```python
class Settings(BaseSettings):
    # API Keys
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    
    # Model Configuration
    llm_model: str = os.getenv("LLM_MODEL", "openai/gpt-3.5-turbo")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Application Settings
    similarity_threshold: float = 0.5
    max_tokens: int = 1024  # Cost-optimized
    temperature: float = 0.1
```

**Key Features**:
- **Environment-Based**: Flexible configuration via environment variables
- **Type Safety**: Pydantic-based settings with type validation
- **Default Values**: Sensible defaults for all configurations
- **Path Management**: Automatic directory creation and path resolution

---

## Frontend Components Analysis

### 1. Main Application (`App.js`)
**Purpose**: React-based user interface for mathematical queries
**Lines of Code**: ~150 lines
**Key Responsibilities**:
- User input handling and validation
- API communication with backend
- Response rendering with LaTeX support
- Feedback collection interface

**Component Architecture**:
```javascript
function App() {
  // State Management
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showFeedback, setShowFeedback] = useState(false);
  
  // API Integration
  const handleSubmit = async (e) => {
    const res = await axios.post(`${API_BASE_URL}/api/query`, {
      question: question
    });
    setResponse(res.data);
  };
  
  // Feedback Submission
  const handleFeedback = async () => {
    await axios.post(`${API_BASE_URL}/api/feedback`, {
      query_id: response.query_id,
      rating: rating,
      is_correct: isCorrect,
      feedback_text: feedbackText
    });
  };
}
```

**LaTeX Rendering Integration**:
```javascript
<ReactMarkdown
  remarkPlugins={[remarkMath]}
  rehypePlugins={[rehypeKatex]}
>
  {response.step_by_step_solution}
</ReactMarkdown>
```

**Key Features**:
- **Real-time Rendering**: LaTeX mathematical notation support
- **Interactive Feedback**: User rating and correction system
- **Sample Questions**: Pre-defined example questions
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during processing

### 2. Styling System (`App.css`)
**Purpose**: Professional UI design and responsive layout
**Lines of Code**: ~300 lines
**Key Responsibilities**:
- Modern gradient-based design
- Responsive layout for different screen sizes
- Interactive element styling
- Mathematical content presentation

**Design System**:
```css
/* Modern gradient background */
body {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Card-based layout */
.App-main {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* Interactive elements */
.query-section button[type="submit"]:hover:not(:disabled) {
  transform: translateY(-2px);
}
```

**Key Features**:
- **Modern Design**: Gradient backgrounds and card-based layout
- **Interactive Elements**: Hover effects and smooth transitions
- **Accessibility**: Proper contrast ratios and focus states
- **Mathematical Display**: Optimized styling for LaTeX content

### 3. HTML Template (`index.html`)
**Purpose**: Application shell and external resource loading
**Key Responsibilities**:
- KaTeX CSS integration for LaTeX rendering
- Meta tags for SEO and mobile optimization
- Content Security Policy configuration
- Progressive Web App support

**External Dependencies**:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<meta http-equiv="Content-Security-Policy" content="...">
```

**Key Features**:
- **LaTeX Support**: KaTeX CSS for mathematical notation
- **Security**: Content Security Policy for XSS protection
- **Mobile Optimization**: Responsive viewport configuration
- **SEO Optimization**: Proper meta tags and descriptions