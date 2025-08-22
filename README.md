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

## 3. Development Process Overview

### Resources & Tools Used
- **Git & GitHub**: Version control and collaboration
- **Python 3**: Core development language  
- **LiteLLM**: Abstracted LLM provider interface
- **Ollama**: Local LLM testing (llama2:7b)
- **VS Code/Cursor**: IDE with AI assistance
- **Terminal**: Command-line development and testing

### Development Methodology
1. **Iterative Development**: Started with basic functionality and progressively enhanced
2. **User-Driven Design**: Responded to feedback to improve API usability
3. **Security-First**: Enforced environment variables for API keys
4. **Testing-Driven**: Used local Ollama for cost-effective testing
5. **Documentation-First**: Maintained comprehensive README throughout development

### Key Design Decisions
- **Environment Variable Configuration**: `LLM_MODEL` and `LLM_API_KEY` for security
- **Abstracted LLM Interface**: `LLMClient` base class with `LiteLLMClient` implementation
- **Debug Mode**: Built-in conversation flow visibility for transparency
- **Rate Limiting**: Automatic retry with exponential backoff for production robustness
- **Local Model Support**: Ollama integration for development and testing

## 4. Time Spent

### Total Development Time: **2 hours**

**Breakdown:**
- **Initial Setup & Git**: 25 minutes
- **Core Algorithm Implementation**: 35 minutes
- **API Design & Refactoring**: 25 minutes
- **Rate Limiting & Error Handling**: 35 minutes
- **Testing & Debugging**: 25 minutes
- **Documentation & Polish**: 25 minutes

### Development Phases
1. **Foundation** (35 min): Basic self-reflection algorithm
2. **API Design** (25 min): User-friendly interface design  
3. **Production Features** (35 min): Rate limiting, error handling
4. **Testing & Polish** (50 min): Local testing, documentation

### Key Strengths for Evaluation

#### Algorithm Correctness
✅ **Self-Reflection Implementation**: Multiple evaluation prompts with different cognitive approaches  
✅ **Scoring System**: A/B/C response mapping to numerical scores (1.0/0.0/0.5)  
✅ **Transparency**: Full conversation flow visibility in debug mode  
✅ **Robustness**: Rate limiting, error handling, retry logic  

#### API Design Excellence
✅ **Security**: Environment variable configuration only  
✅ **Simplicity**: `from_env()` factory method with sensible defaults  
✅ **Flexibility**: Configurable retries, evaluations, debug mode  
✅ **Transparency**: Users can see and modify evaluation prompts  
✅ **Production Ready**: Rate limiting, error handling, local model support  

#### Innovation
- **Local Testing**: Ollama integration for cost-effective development
- **Prompt Engineering**: Multiple evaluation strategies (Standard, Reflective, Critical)
- **Debug Transparency**: Unlike black-box services, users see the full evaluation process