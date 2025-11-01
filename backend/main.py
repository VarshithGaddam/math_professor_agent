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
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
