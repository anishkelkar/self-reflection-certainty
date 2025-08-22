# Self-Reflection Certainty

A Python library for evaluating LLM answer trustworthiness using self-reflection.

## Installation

```bash
pip install self-reflection-certainty
```

## Usage

```python
from self_reflection_certainty import SelfReflectionEvaluator

# Initialize evaluator
evaluator = SelfReflectionEvaluator()

# Evaluate LLM response confidence
confidence_score = evaluator.evaluate_confidence(
    question="What is the capital of France?",
    answer="Paris is the capital of France.",
    context="Geography question about European capitals"
)

print(f"Confidence Score: {confidence_score}")
```

## Testing

```bash
# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=self_reflection_certainty
```
