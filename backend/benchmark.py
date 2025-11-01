"""Benchmark evaluation against JEE Bench dataset."""
import json
import time
from typing import Optional, List
from pathlib import Path
from loguru import logger
from backend.config import settings
from backend.models import BenchmarkResult, Subject

class BenchmarkRunner:
    """Run benchmark evaluation on JEE Bench dataset."""
    
    def __init__(self, agent):
        """Initialize benchmark runner."""
        self.agent = agent
        self.dataset_path = settings.data_dir / "dataset.json"
        
    def load_dataset(self) -> List[dict]:
        """Load JEE Bench dataset."""
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_answer(self, solution: str) -> str:
        """Extract answer from solution text."""
        import re
        
        # Try to find boxed answer
        boxed_match = re.search(r'\\boxed\{([^}]+)\}', solution)
        if boxed_match:
            return boxed_match.group(1).strip()
        
        # Try to find "answer is" pattern
        answer_match = re.search(r'answer is[:\s]+([A-Z0-9.]+)', solution, re.IGNORECASE)
        if answer_match:
            return answer_match.group(1).strip()
        
        return ""
    
    def compare_answers(self, predicted: str, gold: str, question_type: str) -> bool:
        """
        Compare predicted answer with gold answer.
        
        Args:
            predicted: Predicted answer
            gold: Gold standard answer
            question_type: Type of question
            
        Returns:
            True if answers match
        """
        predicted = predicted.strip().upper()
        gold = gold.strip().upper()
        
        if question_type == "MCQ":
            return predicted == gold
        elif question_type == "MCQ(multiple)":
            # For multiple choice, check if all options match
            pred_set = set(predicted.replace(" ", ""))
            gold_set = set(gold.replace(" ", ""))
            return pred_set == gold_set
        else:
            # For numeric/integer, allow small tolerance
            try:
                pred_val = float(predicted)
                gold_val = float(gold)
                return abs(pred_val - gold_val) < 0.01
            except:
                return predicted == gold

    async def run_benchmark(self, num_samples: Optional[int] = None, 
                           subjects: Optional[List[Subject]] = None) -> BenchmarkResult:
        """
        Run benchmark evaluation.
        
        Args:
            num_samples: Number of samples to evaluate (None for all)
            subjects: List of subjects to evaluate (None for all)
            
        Returns:
            Benchmark results
        """
        logger.info("Loading benchmark dataset")
        dataset = self.load_dataset()
        
        # Filter by subjects if specified
        if subjects:
            subject_values = [s.value for s in subjects]
            dataset = [q for q in dataset if q['subject'] in subject_values]
        
        # Limit samples if specified
        if num_samples:
            dataset = dataset[:num_samples]
        
        logger.info(f"Evaluating {len(dataset)} questions")
        
        # Track results
        results = {
            'total': 0,
            'correct': 0,
            'by_subject': {},
            'by_type': {},
            'routes': {},
            'times': []
        }
        
        for idx, question_data in enumerate(dataset):
            logger.info(f"Evaluating question {idx + 1}/{len(dataset)}")
            
            start_time = time.time()
            
            try:
                # Process question
                response = await self.agent.process_query(question_data['question'])
                
                # Extract and compare answer
                predicted_answer = self.extract_answer(response.step_by_step_solution)
                is_correct = self.compare_answers(
                    predicted_answer,
                    question_data['gold'],
                    question_data['type']
                )
                
                # Update results
                results['total'] += 1
                if is_correct:
                    results['correct'] += 1
                
                # Track by subject
                subject = question_data['subject']
                if subject not in results['by_subject']:
                    results['by_subject'][subject] = {'total': 0, 'correct': 0}
                results['by_subject'][subject]['total'] += 1
                if is_correct:
                    results['by_subject'][subject]['correct'] += 1
                
                # Track by type
                qtype = question_data['type']
                if qtype not in results['by_type']:
                    results['by_type'][qtype] = {'total': 0, 'correct': 0}
                results['by_type'][qtype]['total'] += 1
                if is_correct:
                    results['by_type'][qtype]['correct'] += 1
                
                # Track route
                route = response.route_used
                results['routes'][route] = results['routes'].get(route, 0) + 1
                
                # Track time
                elapsed = time.time() - start_time
                results['times'].append(elapsed)
                
                logger.info(f"Question {idx + 1}: {'✓' if is_correct else '✗'} "
                          f"(predicted: {predicted_answer}, gold: {question_data['gold']})")
                
            except Exception as e:
                logger.error(f"Error evaluating question {idx + 1}: {e}")
                results['total'] += 1
        
        # Calculate metrics
        accuracy = results['correct'] / results['total'] if results['total'] > 0 else 0
        
        subject_accuracy = {
            subj: data['correct'] / data['total'] if data['total'] > 0 else 0
            for subj, data in results['by_subject'].items()
        }
        
        type_accuracy = {
            qtype: data['correct'] / data['total'] if data['total'] > 0 else 0
            for qtype, data in results['by_type'].items()
        }
        
        avg_time = sum(results['times']) / len(results['times']) if results['times'] else 0
        
        benchmark_result = BenchmarkResult(
            total_questions=results['total'],
            correct_answers=results['correct'],
            accuracy=accuracy,
            subject_wise_accuracy=subject_accuracy,
            type_wise_accuracy=type_accuracy,
            avg_response_time=avg_time,
            route_distribution=results['routes']
        )
        
        # Save results
        self._save_results(benchmark_result)
        
        return benchmark_result
    
    def _save_results(self, result: BenchmarkResult):
        """Save benchmark results to file."""
        results_path = settings.logs_dir / "benchmark_results.json"
        
        with open(results_path, 'w') as f:
            json.dump(result.dict(), f, indent=2)
        
        logger.info(f"Benchmark results saved to {results_path}")
