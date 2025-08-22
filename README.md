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

## 3. Development Process Overview & Time Spent

### Total Development Time: **~2+ hours**

### Resources & Tools Used
- **Git & GitHub**: Version control and collaboration
- **Python 3**: Core development language  
- **LiteLLM**: Abstracted LLM provider interface
- **Ollama**: Local LLM testing (llama2:7b)
- **Cursor**: IDE with AI assistance

### Development Phases & Time Breakdown
1. **Paper Walkthrough & Git** (~15 min): Initial setup and repository creation
2. **Core Algorithm Implementation + Api** (~1 hr): Basic self-reflection algorithm
3. **Rate Limiting & Error Handling/Debugging** (45 min): Production features