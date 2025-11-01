"""Pydantic models for API requests and responses."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class QuestionType(str, Enum):
    """Question type enumeration."""
    MCQ = "MCQ"
    MCQ_MULTIPLE = "MCQ(multiple)"
    INTEGER = "Integer"
    NUMERIC = "Numeric"

class Subject(str, Enum):
    """Subject enumeration."""
    PHYSICS = "phy"
    CHEMISTRY = "chem"
    MATHEMATICS = "math"

class RouteDecision(str, Enum):
    """Routing decision enumeration."""
    KNOWLEDGE_BASE = "knowledge_base"
    WEB_SEARCH = "web_search"
    REJECT = "reject"

class QueryRequest(BaseModel):
    """Request model for math queries."""
    question: str = Field(..., description="The mathematical question to solve")
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    session_id: Optional[str] = Field(None, description="Optional session identifier")

class RetrievedDocument(BaseModel):
    """Model for retrieved documents from knowledge base."""
    question: str
    gold: str
    subject: str
    type: str
    description: str
    score: float

class QueryResponse(BaseModel):
    """Response model for math queries."""
    query_id: str
    question: str
    answer: str
    step_by_step_solution: str
    route_used: RouteDecision
    retrieved_docs: Optional[List[RetrievedDocument]] = None
    confidence_score: float
    sources: Optional[List[str]] = None
    timestamp: str

class FeedbackRequest(BaseModel):
    """Request model for feedback submission."""
    query_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    feedback_text: Optional[str] = None
    is_correct: bool
    suggested_answer: Optional[str] = None

class FeedbackResponse(BaseModel):
    """Response model for feedback submission."""
    success: bool
    message: str
    updated_response: Optional[QueryResponse] = None

class GuardrailResult(BaseModel):
    """Result from guardrail check."""
    passed: bool
    reason: Optional[str] = None
    filtered_content: Optional[str] = None

class BenchmarkRequest(BaseModel):
    """Request model for benchmark evaluation."""
    num_samples: Optional[int] = Field(None, description="Number of samples to evaluate")
    subjects: Optional[List[Subject]] = Field(None, description="Subjects to evaluate")

class BenchmarkResult(BaseModel):
    """Result model for benchmark evaluation."""
    total_questions: int
    correct_answers: int
    accuracy: float
    subject_wise_accuracy: Dict[str, float]
    type_wise_accuracy: Dict[str, float]
    avg_response_time: float
    route_distribution: Dict[str, int]

class MetricsResponse(BaseModel):
    """Response model for system metrics."""
    total_queries: int
    kb_queries: int
    web_search_queries: int
    rejected_queries: int
    avg_confidence: float
    avg_response_time: float
    feedback_count: int
    avg_rating: float
