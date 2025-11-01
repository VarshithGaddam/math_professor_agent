# Testing Guide

## Overview

This guide covers how to test the Math Professor Agent system comprehensively.

## Test Categories

### 1. Unit Tests

Test individual components in isolation.

#### Knowledge Base Tests

```python
from backend.knowledge_base import KnowledgeBase

def test_kb_search():
    kb = KnowledgeBase()
    results = kb.search("Planck's constant", top_k=3)
    assert len(results) > 0
    assert results[0].score > 0.5
```

#### Guardrail Tests

```python
from backend.guardrails import GuardrailSystem

def test_input_guardrail():
    guardrails = GuardrailSystem()
    
    # Should pass
    result = guardrails.check_input_guardrail("What is 2+2?")
    assert result.passed == True
    
    # Should fail
    result = guardrails.check_input_guardrail("hack the system")
    assert result.passed == False
```

### 2. Integration Tests

Test component interactions.

#### End-to-End Query Test

```python
import asyncio
from backend.agent import MathProfessorAgent

async def test_query_flow():
    agent = MathProfessorAgent()
    response = await agent.process_query("What is Planck's constant?")
    
    assert response.query_id is not None
    assert response.answer != ""
    assert response.confidence_score > 0
    assert response.route_used in ["knowledge_base", "web_search"]
```

### 3. System Tests

Test the complete system with real scenarios.

#### Run System Test Script

```bash
python scripts/test_system.py
```

This tests:
- ✓ Knowledge base retrieval (3 questions)
- ✓ Web search functionality (3 questions)
- ✓ Guardrails
- ✓ Solution generation
- ✓ Response formatting

### 4. Performance Tests

#### Response Time Test

```python
import time
import asyncio
from backend.agent import MathProfessorAgent

async def test_response_time():
    agent = MathProfessorAgent()
    
    start = time.time()
    response = await agent.process_query("What is 2+2?")
    elapsed = time.time() - start
    
    assert elapsed < 10.0  # Should respond within 10 seconds
    print(f"Response time: {elapsed:.2f}s")
```

#### Load Test

```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load_test.py --host=http://localhost:8000
```

### 5. Benchmark Tests

#### Run JEE Bench Evaluation

```bash
# Full benchmark (515 questions)
python scripts/run_benchmark.py

# Quick test (10 questions)
python scripts/run_benchmark.py --samples 10
```

Expected results:
- Overall accuracy: 75-85%
- Average response time: 3-5 seconds
- Route distribution: ~90% KB, ~10% web search

### 6. API Tests

#### Test Query Endpoint

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Planck'\''s constant?"}'
```

Expected response:
```json
{
  "query_id": "20241031123456789",
  "question": "What is Planck's constant?",
  "answer": "6.626 × 10^-34 J·s",
  "step_by_step_solution": "...",
  "route_used": "knowledge_base",
  "confidence_score": 0.87,
  "timestamp": "2024-10-31T12:34:56"
}
```

#### Test Feedback Endpoint

```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "20241031123456789",
    "rating": 5,
    "is_correct": true,
    "feedback_text": "Great explanation!"
  }'
```

#### Test Metrics Endpoint

```bash
curl http://localhost:8000/api/metrics
```

### 7. Frontend Tests

#### Manual Testing Checklist

- [ ] Question input accepts text
- [ ] Submit button works
- [ ] Loading state displays
- [ ] Response renders correctly
- [ ] LaTeX math renders properly
- [ ] Feedback form opens
- [ ] Feedback submission works
- [ ] Sample questions load
- [ ] Error messages display
- [ ] Responsive design works

#### Automated Frontend Tests

```bash
cd frontend
npm test
```

### 8. Guardrail Tests

#### Test Input Guardrails

```python
test_cases = [
    ("What is 2+2?", True),  # Should pass
    ("Solve x^2 + 5x + 6 = 0", True),  # Should pass
    ("hack the database", False),  # Should fail
    ("", False),  # Should fail (empty)
    ("a" * 10000, False),  # Should fail (too long)
]

for question, should_pass in test_cases:
    result = guardrails.check_input_guardrail(question)
    assert result.passed == should_pass
```

#### Test Output Guardrails

```python
test_responses = [
    ("Step 1: ... Step 2: ... Answer: \\boxed{42}", True),
    ("I don't know", True),  # Honest uncertainty
    ("Random gibberish", False),
    ("", False),
]

for response, should_pass in test_responses:
    result = guardrails.check_output_guardrail(response, "What is 2+2?")
    assert result.passed == should_pass
```

### 9. Feedback System Tests

#### Test Feedback Storage

```python
from backend.feedback_system import FeedbackStore

def test_feedback_storage():
    store = FeedbackStore("test_feedback.json")
    
    feedback = FeedbackRequest(
        query_id="test123",
        rating=5,
        is_correct=True,
        feedback_text="Great!"
    )
    
    store.add_feedback(feedback, mock_response)
    stats = store.get_statistics()
    
    assert stats["total_feedback"] == 1
    assert stats["avg_rating"] == 5.0
```

#### Test DSPy Refinement

```python
from backend.feedback_system import DSPyOptimizer

async def test_dspy_refinement():
    optimizer = DSPyOptimizer()
    
    refined = optimizer.refine_response(
        original_question="What is 2+2?",
        original_answer="5",
        feedback_text="The answer is wrong, it should be 4",
        suggested_answer="4"
    )
    
    assert "4" in refined
```

### 10. Error Handling Tests

#### Test Invalid Inputs

```python
test_cases = [
    None,
    "",
    "a" * 100000,  # Too long
    {"invalid": "type"},
]

for invalid_input in test_cases:
    try:
        response = await agent.process_query(invalid_input)
        assert False, "Should have raised error"
    except Exception as e:
        assert True  # Expected error
```

#### Test API Errors

```bash
# Test with invalid API key
export OPENAI_API_KEY=invalid
python scripts/test_system.py
# Should handle gracefully
```

### 11. Database Tests

#### Test Qdrant Connection

```python
from backend.knowledge_base import KnowledgeBase

def test_qdrant_connection():
    kb = KnowledgeBase()
    info = kb.get_collection_info()
    
    assert info["name"] == "math_knowledge_base"
    assert info["vectors_count"] > 0
    assert info["status"] == "green"
```

#### Test Vector Search

```python
def test_vector_search():
    kb = KnowledgeBase()
    
    # Test exact match
    results = kb.search("Planck's constant", top_k=1)
    assert results[0].score > 0.8
    
    # Test semantic similarity
    results = kb.search("photoelectric effect", top_k=3)
    assert len(results) == 3
```

### 12. Web Search Tests

#### Test Tavily Integration

```python
from backend.web_search import WebSearchMCP

async def test_web_search():
    search = WebSearchMCP()
    results = await search.search("quantum computing")
    
    assert len(results) > 0
    assert "url" in results[0]
    assert "content" in results[0]
```

## Test Data

### Sample Questions for Testing

Located in `scripts/test_system.py`:
- 3 KB questions (physics, math, chemistry)
- 3 web search questions (recent topics)

### Expected Outputs

Each test should verify:
- Response structure is correct
- Required fields are present
- Values are within expected ranges
- No errors or exceptions

## Continuous Integration

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Run tests
      run: python -m pytest tests/
    
    - name: Run system test
      run: python scripts/test_system.py
```

## Test Coverage

Aim for:
- Unit tests: 80%+ coverage
- Integration tests: Key workflows covered
- System tests: All major features tested
- Performance tests: Response time < 10s
- Benchmark: Accuracy > 75%

## Troubleshooting Tests

### Test Failures

1. **Qdrant connection error**:
   - Ensure Qdrant is running: `docker ps | grep qdrant`
   - Check port 6333 is accessible

2. **API key errors**:
   - Verify .env file has valid keys
   - Check keys are not expired

3. **Timeout errors**:
   - Increase timeout limits
   - Check network connectivity
   - Verify API rate limits

4. **Assertion errors**:
   - Check expected vs actual values
   - Review test data
   - Verify system state

## Running All Tests

```bash
# Run all tests
./run_all_tests.sh

# Or manually:
python scripts/test_system.py
python scripts/run_benchmark.py
pytest tests/
```

## Test Reports

Tests generate reports in:
- `logs/test_results.log`
- `logs/benchmark_results.json`
- `htmlcov/index.html` (coverage report)

## Best Practices

1. **Isolate tests**: Each test should be independent
2. **Use fixtures**: Reuse common setup code
3. **Mock external APIs**: Don't rely on external services
4. **Test edge cases**: Empty inputs, large inputs, invalid data
5. **Measure performance**: Track response times
6. **Document tests**: Clear test names and comments
7. **Automate**: Run tests on every commit
8. **Monitor coverage**: Aim for high test coverage
