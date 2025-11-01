# Installation Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional, for Qdrant)
- Git

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd math-professor-agent
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your API keys:
# - OPENAI_API_KEY (required)
# - ANTHROPIC_API_KEY (optional, for guardrails)
# - TAVILY_API_KEY (optional, for web search)
```

### 4. Start Qdrant Vector Database

#### Option A: Using Docker (Recommended)

```bash
docker run -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

#### Option B: Using Docker Compose

```bash
docker-compose up -d qdrant
```

#### Option C: Local Installation

Download from https://qdrant.tech/documentation/quick-start/

### 5. Initialize Knowledge Base

```bash
python scripts/setup_knowledge_base.py
```

This will:
- Create Qdrant collection
- Load 515 JEE questions
- Generate embeddings
- Index all questions

Expected output:
```
Knowledge base setup complete!
Collection: math_knowledge_base
Total vectors: 515
Status: green
```

### 6. Test the System

```bash
python scripts/test_system.py
```

This runs 6 sample questions to verify:
- Knowledge base retrieval
- Web search functionality
- Guardrails
- Solution generation

### 7. Start the Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000

API documentation: http://localhost:8000/docs

### 8. Start the Frontend

```bash
cd frontend
npm install
npm start
```

Frontend will be available at: http://localhost:3000

## Verification

### Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### Test Query API

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is 2+2?\"}"
```

### Check Metrics

```bash
curl http://localhost:8000/api/metrics
```

## Docker Deployment (All-in-One)

For production deployment:

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- Qdrant: http://localhost:6333
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Troubleshooting

### Issue: Qdrant connection failed

**Solution**: Ensure Qdrant is running on port 6333
```bash
docker ps | grep qdrant
```

### Issue: OpenRouter API key error

**Solution**: Check .env file has valid OPENROUTER_API_KEY
```bash
cat .env | grep OPENROUTER_API_KEY
```

### Issue: Knowledge base empty

**Solution**: Re-run setup script
```bash
python scripts/setup_knowledge_base.py
```

### Issue: Frontend can't connect to backend

**Solution**: Check CORS settings and backend URL
- Backend should allow origin: http://localhost:3000
- Frontend should use API_BASE_URL: http://localhost:8000

### Issue: Import errors

**Solution**: Ensure virtual environment is activated
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

## Optional: MCP Setup for Web Search

If you want to use MCP server for web search:

1. Install uv (Python package manager):
```bash
pip install uv
```

2. Configure MCP in `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "tavily-search": {
      "command": "uvx",
      "args": ["mcp-server-tavily"],
      "env": {
        "TAVILY_API_KEY": "your_key_here"
      }
    }
  }
}
```

3. Test MCP connection:
```bash
uvx mcp-server-tavily
```

## Development Mode

For development with auto-reload:

### Backend
```bash
uvicorn backend.main:app --reload --log-level debug
```

### Frontend
```bash
cd frontend
npm start
```

## Production Deployment

### Environment Variables

Set these in production:
```bash
export OPENROUTER_API_KEY=your_key
export TAVILY_API_KEY=your_key
export LOG_LEVEL=INFO
export QDRANT_HOST=your_qdrant_host
```

### Run with Gunicorn

```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Build Frontend for Production

```bash
cd frontend
npm run build
# Serve build/ directory with nginx or similar
```

## Next Steps

1. Run benchmark: `python scripts/run_benchmark.py`
2. Check API docs: http://localhost:8000/docs
3. Read architecture: `docs/ARCHITECTURE.md`
4. Read proposal: `docs/PROPOSAL.md`

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review error messages
3. Verify all services are running
4. Check API keys are valid
