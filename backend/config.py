"""Configuration management for the Math Agent system."""
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    
    # Qdrant Configuration
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "math_knowledge_base")
    
    # Model Configuration
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    llm_model: str = os.getenv("LLM_MODEL", "openai/gpt-3.5-turbo")
    guardrail_model: str = os.getenv(
        "GUARDRAIL_MODEL",
        "anthropic/claude-3-sonnet-20240229"
    )
    
    # Application Settings
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1024"))  # Reduced for cost efficiency
    temperature: float = float(os.getenv("TEMPERATURE", "0.1"))
    
    # OpenRouter Configuration
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent
    data_dir: Path = base_dir / "data"
    logs_dir: Path = base_dir / "logs"
    
    # Retrieval Settings
    top_k_retrieval: int = 3
    similarity_threshold: float = 0.5  # Lowered to make KB more accessible
    
    # Guardrail Settings
    guardrail_enabled: bool = os.getenv("GUARDRAIL_ENABLED", "true").lower() != "false"
    allowed_subjects: list = ["mathematics", "physics", "chemistry", "math", "science"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Create necessary directories
settings.logs_dir.mkdir(exist_ok=True)
