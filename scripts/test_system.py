"""Script to test the Math Agent system with sample questions."""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from backend.agent import MathProfessorAgent

# Sample questions for testing
SAMPLE_QUESTIONS = {
    "kb_physics": "In a historical experiment to determine Planck's constant, a metal surface was irradiated with light of different wavelengths. The emitted photoelectron energies were measured by applying a stopping potential. Given that c=3×10^8 m/s and e=1.6×10^-19 C, calculate Planck's constant.",
    
    "kb_math": "Perpendiculars are drawn from points on the line (x+2)/2 = (y+1)/-1 = z/3 to the plane x+y+z=3. Find the line on which the feet of perpendiculars lie.",
    
    "kb_chemistry": "Concentrated nitric acid, upon long standing, turns yellow-brown. What compound is formed?",
    
    "web_search_1": "What are the latest developments in quantum computing algorithms?",
    
    "web_search_2": "Explain the Riemann Hypothesis in simple terms for a high school student.",
    
    "web_search_3": "How is machine learning used in solving differential equations?"
}

async def test_question(agent, name, question):
    """Test a single question."""
    logger.info("\n" + "=" * 80)
    logger.info(f"TEST: {name}")
    logger.info("=" * 80)
    logger.info(f"Question: {question[:100]}...")
    
    try:
        response = await agent.process_query(question)
        
        logger.info(f"\nRoute Used: {response.route_used}")
        logger.info(f"Confidence: {response.confidence_score:.2%}")
        logger.info(f"\nAnswer: {response.answer}")
        logger.info(f"\nSolution Preview:")
        logger.info(response.step_by_step_solution[:300] + "...")
        
        if response.sources:
            logger.info(f"\nSources: {len(response.sources)} found")
        
        logger.success(f"✓ Test '{name}' completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"✗ Test '{name}' failed: {e}")
        return False

async def main():
    """Run system tests."""
    logger.info("=" * 80)
    logger.info("MATH AGENT SYSTEM TEST")
    logger.info("=" * 80)
    
    # Initialize agent
    logger.info("\nInitializing Math Professor Agent...")
    agent = MathProfessorAgent()
    logger.success("✓ Agent initialized")
    
    # Run tests
    results = {}
    for name, question in SAMPLE_QUESTIONS.items():
        results[name] = await test_question(agent, name, question)
        await asyncio.sleep(1)  # Rate limiting
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("TEST SUMMARY")
    logger.info("=" * 80)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        logger.info(f"{status}: {name}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed ({passed/total:.0%})")
    
    if passed == total:
        logger.success("\n🎉 All tests passed!")
    else:
        logger.warning(f"\n⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    asyncio.run(main())
