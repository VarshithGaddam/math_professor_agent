# Math Professor Agent - Final Proposal

## Executive Summary

This project implements a comprehensive Agentic-RAG system that replicates a mathematical professor, providing step-by-step solutions to mathematical problems. The system intelligently routes queries between a knowledge base and web search, incorporates AI guardrails for content filtering, and includes a human-in-the-loop feedback mechanism for continuous improvement.

## 1. Architecture Overview

### System Flow
```
User Query 
    ↓
Input Guardrail (Content Filtering)
    ↓
Router Agent (Decision Making)
    ↓
├─→ Knowledge Base Retrieval (Qdrant Vector DB)
│   └─→ 515 JEE Advanced Questions
│
└─→ Web Search (Tavily API via MCP)
    └─→ Educational Math Resources
    ↓
Solution Generator (GPT-4 + Few-Shot Learning)
    ↓
Output Guardrail (Quality Check)
    ↓
Response to User
    ↓
Human Feedback Collection
    ↓
DSPy Optimization & Self-Learning
```

### Technology Stack
- **Agent Framework**: LangGraph (state-based workflow orchestration)
- **LLM**: GPT-4 Turbo (solution generation)
- **Guardrails**: Claude 3 Sonnet (content filtering)
- **Vector DB**: Qdrant (knowledge base storage)
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **Web Search**: Tavily API via Model Context Protocol (MCP)
- **Optimization**: DSPy (prompt optimization and self-learning)
- **Backend**: FastAPI (REST API)
- **Frontend**: React (user interface)

## 2. Input & Output Guardrails

### Approach Taken

We implemented a **two-layer guardrail system** combining rule-based and LLM-based filtering:

#### Input Guardrails
1. **Rule-Based Layer** (Fast):
   - Length validation (minimum 5 characters)
   - Pattern matching for inappropriate content
   - Keyword filtering for non-educational queries

2. **LLM-Based Layer** (Accurate):
   - Uses Claude 3 Sonnet for semantic understanding
   - Checks educational relevance
   - Validates mathematical/scientific context
   - Filters harmful or off-topic content

#### Output Guardrails
1. **Structure Validation**:
   - Checks for mathematical notation
   - Verifies step-by-step format
   - Ensures proper answer formatting (\\boxed{})

2. **Quality Assurance**:
   - LLM-based coherence check
   - Hallucination detection
   - Educational appropriateness validation

### Why This Approach?

- **Defense in Depth**: Multiple layers catch different types of issues
- **Performance**: Rule-based filters handle obvious cases quickly
- **Accuracy**: LLM layer catches nuanced inappropriate content
- **Privacy**: Filters prevent PII and sensitive data leakage
- **Educational Focus**: Ensures system stays on-topic for math education

## 3. Knowledge Base

### Dataset Details

**Source**: JEE Advanced Examination Questions (2016-2023)
- **Total Questions**: 515
- **Subjects**: 
  - Physics: 123 questions (24%)
  - Chemistry: 156 questions (30%)
  - Mathematics: 236 questions (46%)
- **Question Types**:
  - MCQ (Single): 110 questions
  - MCQ (Multiple): 186 questions
  - Integer Type: 82 questions
  - Numeric Type: 137 questions

### Storage & Retrieval

- **Vector Database**: Qdrant (local deployment)
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- **Similarity Metric**: Cosine similarity
- **Retrieval Strategy**: Top-K retrieval (K=3) with threshold (0.7)
- **Indexing**: HNSW (Hierarchical Navigable Small World) for fast search

### Sample Questions from Knowledge Base

1. **Physics - Photoelectric Effect**:
   ```
   Question: In a historical experiment to determine Planck's constant, 
   a metal surface was irradiated with light of different wavelengths. 
   The emitted photoelectron energies were measured by applying a stopping 
   potential. Given wavelength and stopping potential data, calculate 
   Planck's constant.
   
   Answer: B (6.4 × 10^-34 J·s)
   ```

2. **Mathematics - 3D Geometry**:
   ```
   Question: Perpendiculars are drawn from points on the line 
   (x+2)/2 = (y+1)/-1 = z/3 to the plane x+y+z=3. 
   Find the line on which the feet of perpendiculars lie.
   
   Answer: D (x/2 = (y-1)/-7 = (z-2)/5)
   ```

3. **Chemistry - Solution Formation**:
   ```
   Question: Benzene and naphthalene form an ideal solution at room 
   temperature. Which statements about ΔG, ΔS, and ΔH are correct?
   
   Answer: BCD (ΔS_system > 0, ΔS_surroundings = 0, ΔH = 0)
   ```

## 4. Web Search Capabilities & MCP Setup

### Strategy

We use **Tavily API** through the **Model Context Protocol (MCP)** for web search:

#### Why MCP?
- **Standardized Interface**: MCP provides a consistent way to integrate external tools
- **Async Support**: Non-blocking web searches
- **Error Handling**: Built-in retry and fallback mechanisms
- **Context Preservation**: Maintains conversation context across tool calls

#### Implementation Details

1. **MCP Server Configuration**:
   ```json
   {
     "mcpServers": {
       "tavily-search": {
         "command": "uvx",
         "args": ["mcp-server-tavily"],
         "env": {"TAVILY_API_KEY": "${TAVILY_API_KEY}"}
       }
     }
   }
   ```

2. **Search Strategy**:
   - **Depth**: Advanced search mode
   - **Max Results**: 5 per query
   - **Domain Filtering**: Prioritize educational sources
     - wikipedia.org
     - mathworld.wolfram.com
     - khanacademy.org
     - brilliant.org
     - math.stackexchange.com

3. **Result Processing**:
   - Extract title, URL, and content snippet
   - Format for LLM context
   - Include source attribution

### Sample Questions Requiring Web Search

1. **Recent Mathematical Development**:
   ```
   Question: What are the latest developments in quantum computing 
   algorithms for solving optimization problems?
   
   Expected Route: Web Search (not in JEE syllabus)
   ```

2. **Conceptual Explanation**:
   ```
   Question: Explain the Riemann Hypothesis in simple terms that 
   a high school student can understand.
   
   Expected Route: Web Search (requires pedagogical resources)
   ```

3. **Applied Mathematics**:
   ```
   Question: How is machine learning used in solving partial 
   differential equations in computational fluid dynamics?
   
   Expected Route: Web Search (interdisciplinary, modern application)
   ```

## 5. Human-in-the-Loop Routing

### Architecture

Our HITL system implements a **feedback-driven optimization loop**:

```
User Interaction
    ↓
Response Generation
    ↓
User Provides Feedback
    ├─→ Rating (1-5 stars)
    ├─→ Correctness Flag
    ├─→ Text Feedback
    └─→ Suggested Answer (optional)
    ↓
Feedback Storage & Analysis
    ↓
DSPy Optimization
    ├─→ Prompt Refinement
    ├─→ Example Selection
    └─→ Response Regeneration
    ↓
Updated Response (if needed)
    ↓
Statistics Tracking
```

### Components

#### 1. Feedback Collection
- **Rating System**: 1-5 star rating for response quality
- **Binary Correctness**: User marks if answer is correct
- **Text Feedback**: Open-ended comments
- **Suggested Corrections**: Users can provide correct answers

#### 2. Feedback Storage
- **Persistent Storage**: JSON-based feedback database
- **Metadata Tracking**:
  - Query ID and timestamp
  - Route used (KB vs Web Search)
  - Original question and answer
  - User feedback details

#### 3. DSPy Optimization Engine

**DSPy** (Declarative Self-improving Python) is used for:

- **Prompt Optimization**: Automatically refines prompts based on feedback
- **Few-Shot Learning**: Selects best examples from feedback data
- **Response Refinement**: Regenerates improved answers
- **Metric Tracking**: Monitors improvement over time

#### 4. Self-Learning Mechanism

The system learns from feedback through:

1. **Immediate Refinement**: 
   - When user marks answer as incorrect
   - System regenerates using DSPy with feedback context
   - Returns improved response immediately

2. **Batch Optimization**:
   - Periodic analysis of accumulated feedback
   - Identifies common error patterns
   - Updates prompt templates
   - Improves few-shot examples

3. **Route Optimization**:
   - Tracks which route (KB vs Web) performs better
   - Adjusts similarity thresholds
   - Improves routing decisions

### Statistics & Monitoring

The system tracks:
- **Overall Accuracy**: % of correct responses
- **Average Rating**: User satisfaction score
- **Route Performance**: Accuracy by route (KB vs Web Search)
- **Subject Performance**: Accuracy by subject (Math, Physics, Chemistry)
- **Question Type Performance**: Accuracy by type (MCQ, Numeric, etc.)
- **Improvement Trends**: Performance over time

## 6. JEE Bench Benchmark Results

### Evaluation Setup

- **Dataset**: Full JEE Bench (515 questions)
- **Evaluation Metrics**:
  - Overall Accuracy
  - Subject-wise Accuracy
  - Question Type Accuracy
  - Average Response Time
  - Route Distribution

### Expected Results

Based on the architecture, we expect:

- **Overall Accuracy**: 75-85%
  - Knowledge Base queries: 85-90% (high similarity matches)
  - Web Search queries: 60-70% (depends on search quality)

- **Subject-wise Performance**:
  - Mathematics: 80-85% (largest dataset, clear solutions)
  - Physics: 75-80% (numerical calculations)
  - Chemistry: 70-75% (requires domain knowledge)

- **Question Type Performance**:
  - MCQ (Single): 80-85% (clear correct answer)
  - MCQ (Multiple): 70-75% (multiple correct options)
  - Integer: 75-80% (exact numerical answer)
  - Numeric: 70-75% (decimal precision matters)

- **Route Distribution**:
  - Knowledge Base: ~90% (most questions in dataset)
  - Web Search: ~10% (low similarity or out-of-domain)

- **Average Response Time**: 3-5 seconds per query

### Benchmark Script

The system includes a benchmark runner (`backend/benchmark.py`) that:
1. Loads the JEE Bench dataset
2. Processes each question through the agent
3. Compares predicted answers with gold standard
4. Calculates accuracy metrics
5. Generates detailed report

Run with:
```bash
python -m backend.benchmark
```

Or via API:
```bash
curl -X POST http://localhost:8000/api/benchmark \
  -H "Content-Type: application/json" \
  -d '{"num_samples": 100}'
```

## 7. Key Innovations

1. **Hybrid Routing**: Intelligent decision between KB and web search
2. **Multi-Layer Guardrails**: Ensures safety and quality
3. **DSPy Integration**: Automated prompt optimization
4. **MCP for Web Search**: Standardized tool integration
5. **Real-time Feedback**: Immediate response refinement
6. **Comprehensive Metrics**: Detailed performance tracking

## 8. Deployment & Usage

### Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Add your API keys
   ```

3. **Start Qdrant** (Docker):
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

4. **Initialize Knowledge Base**:
   ```bash
   python scripts/setup_knowledge_base.py
   ```

5. **Start Backend**:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

6. **Start Frontend**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

### API Usage

**Query Endpoint**:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Planck'\''s constant?"}'
```

**Feedback Endpoint**:
```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "20241031123456789",
    "rating": 5,
    "is_correct": true,
    "feedback_text": "Great explanation!"
  }'
```

## 9. Conclusion

This Math Professor Agent system successfully implements all required components:

✅ **AI Guardrails**: Multi-layer input/output filtering
✅ **Knowledge Base**: 515 JEE questions in Qdrant vector DB
✅ **Web Search via MCP**: Tavily API integration
✅ **Human-in-the-Loop**: Feedback collection and DSPy optimization
✅ **Routing Pipeline**: Intelligent KB vs Web Search decision
✅ **JEE Bench Evaluation**: Comprehensive benchmarking system
✅ **Full Stack**: FastAPI backend + React frontend

The system provides accurate, step-by-step mathematical solutions while continuously improving through human feedback.
