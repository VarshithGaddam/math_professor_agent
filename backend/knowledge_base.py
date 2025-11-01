"""Knowledge base management using Qdrant vector database."""
import json
from typing import List, Dict, Any
from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from backend.config import settings
from backend.models import RetrievedDocument

class KnowledgeBase:
    """Vector database knowledge base for math questions."""
    
    def __init__(self):
        """Initialize knowledge base with Qdrant."""
        self.client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        self.collection_name = settings.qdrant_collection_name
        self.encoder = SentenceTransformer(settings.embedding_model)
        self.embedding_dim = 384  # all-MiniLM-L6-v2 dimension
        
        logger.info(f"Initialized KnowledgeBase with collection: {self.collection_name}")
    
    def create_collection(self):
        """Create Qdrant collection if it doesn't exist."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dim,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise

    def load_dataset(self, dataset_path: str):
        """
        Load dataset into knowledge base.
        
        Args:
            dataset_path: Path to dataset JSON file
        """
        logger.info(f"Loading dataset from {dataset_path}")
        
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Loaded {len(data)} questions")
        
        # Create collection
        self.create_collection()
        
        # Prepare points for insertion
        points = []
        batch_size = 100
        
        for idx, item in enumerate(data):
            # Create embedding from question text
            question_text = item['question']
            embedding = self.encoder.encode(question_text).tolist()
            
            # Create point
            point = PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    'question': question_text,
                    'gold': item['gold'],
                    'subject': item['subject'],
                    'type': item['type'],
                    'description': item['description'],
                    'index': item['index']
                }
            )
            points.append(point)
            
            # Insert in batches
            if len(points) >= batch_size:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                logger.info(f"Inserted batch of {len(points)} points")
                points = []
        
        # Insert remaining points
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Inserted final batch of {len(points)} points")
        
        logger.info("Dataset loading complete")

    def search(self, query: str, top_k: int = 3) -> List[RetrievedDocument]:
        """
        Search knowledge base for similar questions.
        
        Args:
            query: User's question
            top_k: Number of results to return
            
        Returns:
            List of retrieved documents
        """
        logger.info(f"Searching KB for: {query[:100]}...")
        
        # Encode query
        query_vector = self.encoder.encode(query).tolist()
        
        # Search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        
        # Convert to RetrievedDocument objects
        documents = []
        for result in results:
            doc = RetrievedDocument(
                question=result.payload['question'],
                gold=result.payload['gold'],
                subject=result.payload['subject'],
                type=result.payload['type'],
                description=result.payload['description'],
                score=result.score
            )
            documents.append(doc)
            logger.info(f"Found match with score {result.score:.3f}: {result.payload['subject']}")
        
        return documents
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                'name': self.collection_name,
                'vectors_count': info.vectors_count,
                'points_count': info.points_count,
                'status': info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}
