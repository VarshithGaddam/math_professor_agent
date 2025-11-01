"""Script to run JEE Bench benchmark evaluation."""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from backend.agent import MathProfessorAgent
from backend.benchmark import BenchmarkRunner

async def main():
    """Run benchmark evaluation."""
    logger.info("=" * 60)
    logger.info("JEE Bench Benchmark Evaluation")
    logger.info("=" * 60)
    
    # Initialize agent and benchmark runner
    logger.info("Initializing agent...")
    agent = MathProfessorAgent()
    
    logger.info("Initializing benchmark runner...")
    runner = BenchmarkRunner(agent)
    
    # Run benchmark
    logger.info("\nStarting benchmark evaluation...")
    logger.info("This may take 10-15 minutes for full dataset (515 questions)")
    
    # You can limit samples for quick testing
    # result = await runner.run_benchmark(num_samples=10)
    
    # Full benchmark
    result = await runner.run_benchmark()
    
    # Print results
    logger.info("\n" + "=" * 60)
    logger.info("BENCHMARK RESULTS")
    logger.info("=" * 60)
    logger.info(f"\nTotal Questions: {result.total_questions}")
    logger.info(f"Correct Answers: {result.correct_answers}")
    logger.info(f"Overall Accuracy: {result.accuracy:.2%}")
    
    logger.info("\nSubject-wise Accuracy:")
    for subject, acc in result.subject_wise_accuracy.items():
        logger.info(f"  {subject}: {acc:.2%}")
    
    logger.info("\nQuestion Type Accuracy:")
    for qtype, acc in result.type_wise_accuracy.items():
        logger.info(f"  {qtype}: {acc:.2%}")
    
    logger.info("\nRoute Distribution:")
    for route, count in result.route_distribution.items():
        logger.info(f"  {route}: {count} queries")
    
    logger.info(f"\nAverage Response Time: {result.avg_response_time:.2f}s")
    
    logger.info("\n" + "=" * 60)
    logger.info("Results saved to logs/benchmark_results.json")
    logger.info("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
