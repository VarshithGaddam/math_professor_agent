"""Human-in-the-loop feedback system with DSPy optimization."""
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger
try:
    import dspy
    DSPY_AVAILABLE = True
    logger.info("DSPy available for advanced optimization")
except ImportError:
    DSPY_AVAILABLE = False
    logger.info("DSPy not available, using basic feedback system")
from backend.config import settings
from backend.models import FeedbackRequest, QueryResponse

class FeedbackStore:
    """Store and manage user feedback."""
    
    def __init__(self, storage_path: str = "data/feedback.json"):
        """Initialize feedback store."""
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(exist_ok=True)
        self.feedback_data = self._load_feedback()
        
    def _load_feedback(self) -> Dict:
        """Load feedback from storage."""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {"feedback": [], "statistics": {}}
    
    def _save_feedback(self):
        """Save feedback to storage."""
        with open(self.storage_path, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
    
    def add_feedback(self, feedback: FeedbackRequest, original_response: QueryResponse):
        """Add new feedback entry."""
        entry = {
            "query_id": feedback.query_id,
            "timestamp": datetime.now().isoformat(),
            "rating": feedback.rating,
            "is_correct": feedback.is_correct,
            "feedback_text": feedback.feedback_text,
            "suggested_answer": feedback.suggested_answer,
            "original_question": original_response.question,
            "original_answer": original_response.answer,
            "route_used": original_response.route_used
        }
        
        self.feedback_data["feedback"].append(entry)
        self._update_statistics()
        self._save_feedback()
        
        logger.info(f"Added feedback for query {feedback.query_id}")

    def _update_statistics(self):
        """Update feedback statistics."""
        feedbacks = self.feedback_data["feedback"]
        
        if not feedbacks:
            return
        
        total = len(feedbacks)
        correct = sum(1 for f in feedbacks if f["is_correct"])
        avg_rating = sum(f["rating"] for f in feedbacks) / total
        
        route_stats = {}
        for f in feedbacks:
            route = f["route_used"]
            if route not in route_stats:
                route_stats[route] = {"total": 0, "correct": 0}
            route_stats[route]["total"] += 1
            if f["is_correct"]:
                route_stats[route]["correct"] += 1
        
        self.feedback_data["statistics"] = {
            "total_feedback": total,
            "accuracy": correct / total,
            "avg_rating": avg_rating,
            "route_performance": route_stats,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_statistics(self) -> Dict:
        """Get feedback statistics."""
        return self.feedback_data.get("statistics", {})
    
    def get_training_data(self) -> List[Dict]:
        """Get feedback data for DSPy training."""
        return [
            f for f in self.feedback_data["feedback"]
            if f.get("suggested_answer") is not None
        ]

class DSPyOptimizer:
    """DSPy-based optimizer for improving responses based on feedback."""
    
    def __init__(self):
        """Initialize DSPy optimizer."""
        # For now, disable DSPy to avoid initialization issues
        logger.info("DSPy optimizer disabled - using basic feedback system")
        self.lm = None

    def refine_response(self, original_question: str, original_answer: str, 
                       feedback_text: str, suggested_answer: Optional[str] = None) -> str:
        """
        Refine response based on human feedback.
        
        Args:
            original_question: The original question
            original_answer: The original answer
            feedback_text: Human feedback
            suggested_answer: Optional suggested correct answer
            
        Returns:
            Refined answer
        """
        logger.info("Refining response with DSPy")
        
        if not DSPY_AVAILABLE or not self.lm:
            logger.warning("DSPy not available, using simple refinement")
            return f"""Based on your feedback: {feedback_text}

Here's an improved approach to the original question: {original_question}

{f"Suggested answer: {suggested_answer}" if suggested_answer else ""}

Please note: Advanced optimization requires DSPy installation."""
        
        # Create refinement prompt
        refinement_context = f"""Original Question: {original_question}

Original Answer: {original_answer}

Human Feedback: {feedback_text}
"""
        
        if suggested_answer:
            refinement_context += f"\nSuggested Correct Answer: {suggested_answer}"
        
        refinement_context += """

Based on the feedback, provide an improved step-by-step solution that addresses the issues mentioned.
Ensure the solution is mathematically correct and pedagogically clear.
"""
        
        try:
            # Use DSPy to generate refined response
            class MathRefinement(dspy.Signature):
                """Refine mathematical solution based on feedback."""
                context = dspy.InputField(desc="Original question, answer, and feedback")
                refined_solution = dspy.OutputField(desc="Improved step-by-step solution")
            
            refiner = dspy.ChainOfThought(MathRefinement)
            result = refiner(context=refinement_context)
            
            return result.refined_solution
        except Exception as e:
            logger.error(f"DSPy refinement failed: {e}")
            # Fallback to simple refinement without DSPy
            return f"""Based on your feedback: {feedback_text}

Here's an improved approach to the original question: {original_question}

{f"Suggested answer: {suggested_answer}" if suggested_answer else ""}

Note: This is a simplified refinement as DSPy optimization encountered an issue."""

class FeedbackAgent:
    """Agent for handling human-in-the-loop feedback."""
    
    def __init__(self):
        """Initialize feedback agent."""
        self.store = FeedbackStore()
        self.optimizer = DSPyOptimizer()
        self.response_cache = {}  # Cache original responses
        
    def cache_response(self, response: QueryResponse):
        """Cache a response for potential feedback."""
        self.response_cache[response.query_id] = response
        
    def process_feedback(self, feedback: FeedbackRequest) -> Optional[QueryResponse]:
        """
        Process user feedback and potentially refine response.
        
        Args:
            feedback: User feedback
            
        Returns:
            Refined response if applicable
        """
        # Get original response
        original_response = self.response_cache.get(feedback.query_id)
        
        if not original_response:
            logger.warning(f"Original response not found for query {feedback.query_id}")
            return None
        
        # Store feedback
        self.store.add_feedback(feedback, original_response)
        
        # If feedback indicates incorrect answer and provides suggestion, refine
        if not feedback.is_correct and (feedback.suggested_answer or feedback.feedback_text):
            refined_solution = self.optimizer.refine_response(
                original_response.question,
                original_response.step_by_step_solution,
                feedback.feedback_text or "",
                feedback.suggested_answer
            )
            
            # Create refined response
            refined_response = QueryResponse(
                query_id=original_response.query_id + "_refined",
                question=original_response.question,
                answer=feedback.suggested_answer or original_response.answer,
                step_by_step_solution=refined_solution,
                route_used=original_response.route_used,
                retrieved_docs=original_response.retrieved_docs,
                confidence_score=min(original_response.confidence_score + 0.1, 1.0),
                sources=original_response.sources,
                timestamp=datetime.now().isoformat()
            )
            
            return refined_response
        
        return None
    
    def get_statistics(self) -> Dict:
        """Get feedback statistics."""
        return self.store.get_statistics()
