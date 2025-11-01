# System Architecture

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  - User Interface                                            │
│  - Question Input                                            │
│  - Solution Display (with LaTeX rendering)                   │
│  - Feedback Collection                                       │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────▼────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  - API Endpoints (/query, /feedback, /benchmark)            │
│  - Request Validation                                        │
│  - Response Formatting                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Math Professor Agent                        │
│                    (LangGraph)                               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. Input Guardrail Node                             │  │
│  │     - Rule-based filtering                           │  │
│  │     - LLM-based content check (Claude)               │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │  2. Router Node                                      │  │
│  │     - Query knowledge base                           │  │
│  │     - Check similarity score                         │  │
│  │     - Decide: KB or Web Search                       │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│         ┌───────────┴───────────┐                           │
│         │                       │                           │
│  ┌──────▼──────┐         ┌─────▼──────┐                    │
│  │ 3a. KB      │         │ 3b. Web    │                    │
│  │  Retrieval  │         │  Search    │                    │
│  │  Node       │         │  Node      │                    │
│  └──────┬──────┘         └─────┬──────┘                    │
│         │                       │                           │
│         └───────────┬───────────┘                           │
│                     │                                        │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │  4. Solution Generator Node                          │  │
│  │     - Load few-shot examples                         │  │
│  │     - Build context                                  │  │
│  │     - Generate step-by-step solution (GPT-4)         │  │
│  │     - Extract final answer                           │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │  5. Output Guardrail Node                            │  │
│  │     - Structure validation                           │  │
│  │     - Quality check (Claude)                         │  │
│  │     - Hallucination detection                        │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Feedback Agent                              │
│  - Collect user feedback                                     │
│  - Store in feedback database                                │
│  - DSPy optimization                                         │
│  - Response refinement                                       │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    External Services                          │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Qdrant    │  │   OpenAI     │  │   Tavily     │       │
│  │  Vector DB  │  │   GPT-4      │  │  Web Search  │       │
│  │             │  │   Embeddings │  │   (via MCP)  │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌─────────────┐                                            │
│  │  Anthropic  │                                            │
│  │  Claude 3   │                                            │
│  │ (Guardrails)│                                            │
│  └─────────────┘                                            │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Query Processing Flow

```
User Question
    ↓
[Input Guardrail]
    ├─ PASS → Continue
    └─ FAIL → Return error message
    ↓
[Router]
    ├─ Embed question
    ├─ Search Qdrant (top-3)
    ├─ Check similarity score
    │
    ├─ Score ≥ 0.7 → [KB Retrieval]
    │   ├─ Get similar questions
    │   ├─ Get gold answers
    │   └─ Build context
    │
    └─ Score < 0.7 → [Web Search]
        ├─ Query Tavily API
        ├─ Filter educational sources
        └─ Build context
    ↓
[Solution Generator]
    ├─ Load few-shot examples
    ├─ Build prompt with context
    ├─ Call GPT-4
    ├─ Parse response
    └─ Extract answer
    ↓
[Output Guardrail]
    ├─ Validate structure
    ├─ Check quality
    └─ PASS/FAIL
    ↓
Return Response to User
```

### 2. Feedback Processing Flow

```
User Submits Feedback
    ├─ Rating (1-5)
    ├─ Correctness flag
    ├─ Text feedback
    └─ Suggested answer
    ↓
[Feedback Agent]
    ├─ Retrieve original response
    ├─ Store feedback in database
    ├─ Update statistics
    │
    └─ If incorrect + suggestion provided:
        ↓
    [DSPy Optimizer]
        ├─ Build refinement context
        ├─ Generate improved solution
        └─ Return refined response
    ↓
Update User Interface
```

## Key Design Decisions

### 1. Why LangGraph?

- **State Management**: Clean state transitions between nodes
- **Conditional Routing**: Easy to implement KB vs Web Search logic
- **Debugging**: Visual graph representation
- **Extensibility**: Easy to add new nodes (e.g., calculator, code execution)

### 2. Why Qdrant?

- **Performance**: Fast similarity search with HNSW index
- **Scalability**: Can handle millions of vectors
- **Filtering**: Supports metadata filtering (by subject, type)
- **Local Deployment**: No cloud dependency for development

### 3. Why DSPy?

- **Automated Optimization**: No manual prompt engineering
- **Metric-Driven**: Optimizes based on actual performance
- **Few-Shot Learning**: Automatically selects best examples
- **Composability**: Works well with LangChain/LangGraph

### 4. Why MCP for Web Search?

- **Standardization**: Consistent interface for external tools
- **Flexibility**: Easy to swap search providers
- **Error Handling**: Built-in retry logic
- **Context Preservation**: Maintains conversation state

## Security Considerations

1. **Input Validation**: All inputs validated before processing
2. **Guardrails**: Multi-layer content filtering
3. **Rate Limiting**: Prevent API abuse (to be implemented)
4. **API Key Management**: Environment variables, never hardcoded
5. **CORS**: Configured for specific origins in production
6. **Error Handling**: No sensitive data in error messages

## Performance Optimizations

1. **Caching**: Response caching for repeated queries
2. **Batch Processing**: Batch embeddings for efficiency
3. **Async Operations**: Non-blocking web searches
4. **Connection Pooling**: Reuse database connections
5. **Lazy Loading**: Load models only when needed

## Monitoring & Observability

1. **Logging**: Structured logging with Loguru
2. **Metrics**: Track accuracy, latency, route distribution
3. **Feedback Analytics**: User satisfaction trends
4. **Error Tracking**: Log all exceptions with context
5. **Performance Metrics**: Response time, token usage

## Scalability Considerations

### Current Architecture (Single Server)
- Handles ~100 concurrent users
- ~10 queries/second
- Local Qdrant instance

### Future Scaling Options
1. **Horizontal Scaling**: Multiple FastAPI instances behind load balancer
2. **Qdrant Cloud**: Managed vector database
3. **Caching Layer**: Redis for response caching
4. **Async Workers**: Celery for background tasks
5. **CDN**: Static frontend assets

## Technology Choices Summary

| Component | Technology | Reason |
|-----------|-----------|--------|
| Agent Framework | LangGraph | State management, conditional routing |
| LLM | GPT-4 Turbo | Best reasoning for math problems |
| Guardrails | Claude 3 Sonnet | Strong content filtering |
| Vector DB | Qdrant | Fast, scalable, local deployment |
| Embeddings | Sentence-Transformers | Open source, good quality |
| Web Search | Tavily | Educational focus, MCP support |
| Optimization | DSPy | Automated prompt improvement |
| Backend | FastAPI | Fast, async, type-safe |
| Frontend | React | Component-based, rich ecosystem |
| Math Rendering | KaTeX | Fast LaTeX rendering |
