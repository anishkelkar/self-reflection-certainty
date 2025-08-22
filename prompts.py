"""
Prompt templates for self-evaluation.
"""
from typing import List


def get_base_evaluation_prompt(question: str, answer: str) -> str:
    """Standard evaluation prompt."""
    return f"""You are an expert evaluator. Your task is to assess whether a given answer is correct for a specific question.

Question: {question}
Proposed Answer: {answer}

Please evaluate the correctness of this answer. Choose exactly one of the following options:
A) The answer is CORRECT (score: 1.0)
B) The answer is INCORRECT (score: 0.0)
C) I am NOT SURE about the answer (score: 0.5)

Consider the following criteria:
- Accuracy: Is the answer factually correct?
- Completeness: Does the answer fully address the question?
- Relevance: Is the answer directly related to what was asked?

Respond with ONLY the letter (A, B, or C)"""


def get_reflective_evaluation_prompt(question: str, answer: str) -> str:
    """Evaluation prompt with additional reflection encouragement."""
    return f"""You are an expert evaluator. Your task is to assess whether a given answer is correct for a specific question.

Question: {question}
Proposed Answer: {answer}

Please evaluate the correctness of this answer. Choose exactly one of the following options:
A) The answer is CORRECT (score: 1.0)
B) The answer is INCORRECT (score: 0.0)
C) I am NOT SURE about the answer (score: 0.5)

Take a moment to carefully consider: Are you really sure about your evaluation?

Respond with ONLY the letter (A, B, or C)"""


def get_evaluation_prompts(question: str, answer: str, num_evaluations: int = 2) -> List[str]:
    prompts = [
        get_base_evaluation_prompt(question, answer),
        get_reflective_evaluation_prompt(question, answer)
    ]
    
    # If more evaluations needed, cycle through available prompts
    while len(prompts) < num_evaluations:
        prompts.append(prompts[len(prompts) % 2])
    
    return prompts[:num_evaluations]