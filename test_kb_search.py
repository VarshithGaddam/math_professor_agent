"""Quick test of knowledge base search."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from backend.knowledge_base import KnowledgeBase
from loguru import logger

def test_kb_search():
    """Test KB search with various questions."""
    kb = KnowledgeBase()
    
    test_questions = [
        "Perpendiculars are drawn from points on the line to the plane",
        "What is Planck's constant?",
        "Vernier callipers measurement",
        "Nitric acid yellow brown",
        "photoelectric effect",
        "cylinder diameter measurement"
    ]
    
    for question in test_questions:
        logger.info(f"\n--- Testing: {question} ---")
        docs = kb.search(question, top_k=3)
        
        if docs:
            for i, doc in enumerate(docs):
                logger.info(f"{i+1}. Score: {doc.score:.3f} | Subject: {doc.subject} | Question: {doc.question[:80]}...")
        else:
            logger.info("No results found")

if __name__ == "__main__":
    test_kb_search()