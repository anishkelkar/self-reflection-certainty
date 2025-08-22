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
