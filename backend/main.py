"""FastAPI application for Math Professor Agent."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
from backend.config import settings
from backend.models import (
    QueryRequest, QueryResponse, FeedbackRequest, FeedbackResponse,
    BenchmarkRequest, BenchmarkResult, MetricsResponse
)
from backend.agent import MathProfessorAgent
from backend.feedback_system import FeedbackAgent
from backend.benchmark import BenchmarkRunner

# Configure logging
logger.remove()
logger.add(sys.stderr, level=settings.log_level)
logger.add(
    settings.logs_dir / "app.log",
    rotation="500 MB",
    retention="10 days",
    level=settings.log_level
)

# Initialize FastAPI app
app = FastAPI(
    title="Math Professor Agent API",
    description="Agentic RAG system for mathematical tutoring",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
agent = MathProfessorAgent()
feedback_agent = FeedbackAgent()
benchmark_runner = BenchmarkRunner(agent)

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    logger.info("Starting Math Professor Agent API")
    logger.info(f"Using LLM: {settings.llm_model}")
    logger.info(f"Knowledge base: {settings.qdrant_collection_name}")
    
    # Validate API keys
    if not settings.openrouter_api_key:
        logger.error("❌ OPENROUTER_API_KEY not set! Solution generation will fail.")
        logger.error("   Get your key from https://openrouter.ai/keys and add it to .env")
        logger.error("   Format: OPENROUTER_API_KEY=sk-or-v1-...")
    else:
        logger.info(f"✓ OpenRouter API key found ({settings.openrouter_api_key[:10]}...)")
        # Test the API key
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                test_response = await client.post(
                    f"{settings.openrouter_base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.openrouter_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": settings.llm_model,
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 5,
                    },
                    timeout=10.0
                )
                if test_response.status_code == 200:
                    logger.success("✓ OpenRouter API key is valid and working!")
                elif test_response.status_code == 401:
                    logger.error("❌ OpenRouter API key is INVALID or EXPIRED!")
                    logger.error("   Please check your API key at https://openrouter.ai/keys")
                    logger.error("   The key should start with 'sk-or-v1-'")
                else:
                    logger.warning(f"⚠️  OpenRouter API returned status {test_response.status_code}")
                    logger.warning("   Key might still work, but please verify")
        except Exception as e:
            logger.warning(f"⚠️  Could not test OpenRouter API key: {e}")
            logger.warning("   This might be a network issue, but please verify your key is correct")
    
    if not settings.tavily_api_key:
        logger.warning("⚠️  TAVILY_API_KEY not set! Web search will not work.")
        logger.warning("   Get your key from https://tavily.com and add it to .env")
    else:
        logger.info("✓ Tavily API key configured")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Math Professor Agent API",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a mathematical query.
    
    Args:
        request: Query request with question
        
    Returns:
        Query response with solution
    """
    try:
        logger.info(f"Received query: {request.question[:100]}...")
        
        # Process query through agent
        response = await agent.process_query(request.question)
        
        # Cache response for potential feedback
        feedback_agent.cache_response(response)
        
        logger.info(f"Query processed successfully: {response.query_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Submit feedback on a response.
    
    Args:
        request: Feedback request
        
    Returns:
        Feedback response with optional refined answer
    """
    try:
        logger.info(f"Received feedback for query: {request.query_id}")
        
        # Process feedback
        refined_response = feedback_agent.process_feedback(request)
        
        return FeedbackResponse(
            success=True,
            message="Feedback received and processed",
            updated_response=refined_response
        )
        
    except Exception as e:
        logger.error(f"Error processing feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics():
    """
    Get system performance metrics.
    
    Returns:
        System metrics
    """
    try:
        stats = feedback_agent.get_statistics()
        
        return MetricsResponse(
            total_queries=stats.get("total_feedback", 0),
            kb_queries=stats.get("route_performance", {}).get("knowledge_base", {}).get("total", 0),
            web_search_queries=stats.get("route_performance", {}).get("web_search", {}).get("total", 0),
            rejected_queries=stats.get("route_performance", {}).get("reject", {}).get("total", 0),
            avg_confidence=0.0,  # Calculate from cached responses
            avg_response_time=0.0,  # Track in production
            feedback_count=stats.get("total_feedback", 0),
            avg_rating=stats.get("avg_rating", 0.0)
        )
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/benchmark", response_model=BenchmarkResult)
async def run_benchmark(request: BenchmarkRequest):
    """
    Run benchmark evaluation on JEE Bench dataset.
    
    Args:
        request: Benchmark configuration
        
    Returns:
        Benchmark results
    """
    try:
        logger.info("Starting benchmark evaluation")
        
        result = await benchmark_runner.run_benchmark(
            num_samples=request.num_samples,
            subjects=request.subjects
        )
        
        logger.info(f"Benchmark complete: {result.accuracy:.2%} accuracy")
        return result
        
    except Exception as e:
        logger.error(f"Error running benchmark: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint with API key status."""
    health_status = {
        "status": "healthy",
        "api_keys": {
            "openrouter": {
                "configured": bool(settings.openrouter_api_key),
                "status": "valid" if settings.openrouter_api_key else "missing"
            },
            "tavily": {
                "configured": bool(settings.tavily_api_key),
                "status": "valid" if settings.tavily_api_key else "missing"
            }
        }
    }
    
    if not settings.openrouter_api_key:
        health_status["status"] = "degraded"
        health_status["api_keys"]["openrouter"]["error"] = "OPENROUTER_API_KEY not set - solution generation will fail"
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
