# Self-Reflection Certainty

A Python library for evaluating LLM answer trustworthiness using self-reflection.

## 1. Installation

Clone and install:

```bash
git clone https://github.com/anishkelkar/self-reflection-certainty.git
cd self-reflection-certainty
pip install -e .
```

## 2. Run Demo

```bash
export LLM_MODEL="gpt-4"
export LLM_API_KEY="your-api-key"
python3 demo.py
```


### API

```python
from self_reflection_certainty import SelfReflectionCertainty

# With debug mode - shows all prompts and responses
evaluator = SelfReflectionCertainty.from_env(debug=True)

# Evaluate a question
evaluator.evaluate_answer("What is the capital of France?")
```

### Rate Limiting & Retry

The library automatically handles rate limit errors with exponential backoff:

```python
# Configure retry behavior
evaluator = SelfReflectionCertainty.from_env(
    max_retries=5,      # Maximum retry attempts
    retry_delay=0.5     # Base delay (exponential: 0.5s, 1s, 2s, 4s, 8s)
)

# Or use defaults (3 retries, 1s base delay)
evaluator = SelfReflectionCertainty.from_env()
```

**Supported Rate Limit Patterns:**
- `rate limit`, `quota`, `too many requests`, `429`
- `rate_limit`, `quota_exceeded`, `throttled`
