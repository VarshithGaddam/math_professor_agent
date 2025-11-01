"""Setup script to initialize the knowledge base."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from backend.knowledge_base import KnowledgeBase
from backend.config import settings

def main():
    """Initialize knowledge base with dataset."""
    logger.info("Starting knowledge base setup")
    
    # Initialize KB
    kb = KnowledgeBase()
    
    # Load dataset
    dataset_path = settings.data_dir / "dataset.json"
    
    if not dataset_path.exists():
        logger.error(f"Dataset not found at {dataset_path}")
        return
    
    logger.info(f"Loading dataset from {dataset_path}")
    kb.load_dataset(str(dataset_path))
    
    # Verify
    info = kb.get_collection_info()
    logger.info(f"Knowledge base setup complete!")
    logger.info(f"Collection: {info.get('name')}")
    logger.info(f"Total vectors: {info.get('vectors_count')}")
    logger.info(f"Status: {info.get('status')}")
    
    # Test search
    logger.info("\nTesting search functionality...")
    test_query = "What is Planck's constant?"
    results = kb.search(test_query, top_k=3)
    
    logger.info(f"\nTest query: {test_query}")
    logger.info(f"Found {len(results)} results:")
    for i, doc in enumerate(results, 1):
        logger.info(f"\n{i}. Score: {doc.score:.3f}")
        logger.info(f"   Subject: {doc.subject}")
        logger.info(f"   Question: {doc.question[:100]}...")

if __name__ == "__main__":
    main()
