"""Test OpenRouter API integration."""
import sys
from pathlib import Path
import asyncio
import httpx

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import settings
from loguru import logger

async def test_openrouter_api():
    """Test OpenRouter API connection."""
    logger.info("Testing OpenRouter API connection...")
    
    if not settings.openrouter_api_key:
        logger.error("OPENROUTER_API_KEY not found in environment")
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.openrouter_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": settings.llm_model,
                    "messages": [{"role": "user", "content": "What is 2+2?"}],
                    "max_tokens": 20,
                    "temperature": 0.1
                },
                timeout=30.0
            )
        
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            logger.success(f"✓ OpenRouter API working! Response: {answer}")
            return True
        else:
            logger.error(f"✗ OpenRouter API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"✗ OpenRouter API test failed: {e}")
        return False

async def test_tavily_api():
    """Test Tavily API connection."""
    logger.info("Testing Tavily API connection...")
    
    if not settings.tavily_api_key:
        logger.error("TAVILY_API_KEY not found in environment")
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": settings.tavily_api_key,
                    "query": "mathematics",
                    "max_results": 1
                },
                timeout=30.0
            )
        
        if response.status_code == 200:
            result = response.json()
            results = result.get('results', [])
            logger.success(f"✓ Tavily API working! Found {len(results)} results")
            return True
        else:
            logger.error(f"✗ Tavily API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Tavily API test failed: {e}")
        return False

async def main():
    """Run API tests."""
    logger.info("=" * 50)
    logger.info("API CONNECTION TESTS")
    logger.info("=" * 50)
    
    openrouter_ok = await test_openrouter_api()
    tavily_ok = await test_tavily_api()
    
    logger.info("\n" + "=" * 50)
    logger.info("TEST RESULTS")
    logger.info("=" * 50)
    
    if openrouter_ok and tavily_ok:
        logger.success("🎉 All API connections working!")
        logger.info("\nYou can now run:")
        logger.info("1. python scripts/setup_knowledge_base.py")
        logger.info("2. python scripts/test_system.py")
        logger.info("3. uvicorn backend.main:app --reload")
    else:
        logger.error("❌ Some API connections failed")
        logger.info("\nPlease check your API keys in .env file")

if __name__ == "__main__":
    asyncio.run(main())