# Self-Reflection Certainty

A Python library for evaluating LLM answer trustworthiness using self-reflection.

## 1. Installation

Clone and install:

```bash
git clone https://github.com/anishkelkar/self-reflection-certainty.git
cd self-reflection-certainty
pip install -e .
```

## 2. Environment Setup

### With API Key

Set your API key and model:

```bash
export LLM_MODEL="gpt-4"
export LLM_API_KEY="your-api-key"
```

### Local Testing with Ollama

For local testing without API costs:

```bash
# On macOS with Homebrew:
brew install ollama

# Start Ollama service
brew services start ollama

# Pull a model
ollama pull llama2:7b

# Test with inline command (no environment setup needed)
LLM_MODEL="ollama/llama2:7b" python3 demo.py
```

## 3. Usage

Run the demo:
```bash
# With API key
python3 demo.py

# With local Ollama (no API key needed)
LLM_MODEL="ollama/llama2:7b" python3 demo.py
```

### API

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

### Debug Mode

Enable debug mode to see the full conversation flow:

```python
# With debug mode - shows all prompts and responses
evaluator = SelfReflectionCertainty.from_env(debug=True)
result = evaluator.evaluate_answer("What is 2+2?")
```

### Methods

- `from_env(num_evaluations=2, debug=False)` - Create evaluator using environment variables
- `evaluate_answer(question, answer=None)` - Evaluate answer certainty
- `is_trustworthy(question, answer=None, threshold=0.7)` - Binary trust check
