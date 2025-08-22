# Self-Reflection Certainty

A Python library for evaluating LLM answer trustworthiness using self-reflection.

## 1. Environment Setup

Set your API key and model:

```bash
export LLM_MODEL="gpt-4"
export LLM_API_KEY="your-api-key"
```

## 2. Installation

Clone and install:

```bash
git clone https://github.com/anishkelkar/self-reflection-certainty.git
cd self-reflection-certainty
pip install -e .
```

Run the demo:
```bash
python demo.py
```

## 3. API

```python
from self_reflection_certainty import SelfReflectionCertainty

# Create evaluator
evaluator = SelfReflectionCertainty.from_env()

# Evaluate a question
result = evaluator.evaluate_answer("What is the capital of France?")
print(f"Certainty: {result['certainty_score']:.2f}")

# Check trustworthiness
is_trustworthy, result = evaluator.is_trustworthy(
    question="What is 2 + 2?",
    answer="2 + 2 equals 4",
    threshold=0.7
)
```

### Methods

- `from_env(num_evaluations=2)` - Create evaluator using environment variables
- `evaluate_answer(question, answer=None)` - Evaluate answer certainty
- `is_trustworthy(question, answer=None, threshold=0.7)` - Binary trust check

### Results

Returns a dictionary with:
- `answer`: The evaluated answer
- `certainty_score`: Confidence score (0-1)
- `evaluation_scores`: Individual evaluation scores
- `evaluations`: Raw evaluation responses
