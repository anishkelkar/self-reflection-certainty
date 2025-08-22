"""
Core self-reflection certainty implementation.
"""
from typing import List, Optional
from .adapter import LLMClient
from .prompts import get_evaluation_prompts
from .utils import map_response_to_score


class SelfReflectionCertainty:
    """
    Implements the self-reflection certainty algorithm from Chen & Mueller (ACL'24).
    
    This class evaluates the trustworthiness of LLM outputs by having the model
    self-evaluate its own answers using multiple evaluation prompts.
    """
    
    def __init__(self, client: LLMClient, num_evaluations: int = 2):
        """
        Initialize the self-reflection certainty evaluator.
        
        Args:
            client: LLM client adapter for making API calls
            num_evaluations: Number of self-evaluation rounds to perform
        """
        self.client = client
        self.num_evaluations = num_evaluations
    
    def evaluate_answer(self, question: str, answer: Optional[str] = None) -> dict:
        # Step 1: Generate answer if not provided
        if answer is None:
            answer = self.client.generate_response(question)
        
        # Step 2: Get multiple self-evaluations
        evaluation_prompts = get_evaluation_prompts(question, answer, self.num_evaluations)
        evaluations = []
        scores = []
        
        for prompt in evaluation_prompts:
            evaluation = self.client.generate_response(prompt)
            evaluations.append(evaluation)
            score = map_response_to_score(evaluation)
            scores.append(score)
        
        # Step 3: Compute final certainty score (average of evaluations)
        certainty_score = sum(scores) / len(scores) if scores else 0.0
        
        return {
            'answer': answer,
            'certainty_score': certainty_score,
            'evaluation_scores': scores,
            'evaluations': evaluations
        }
    
    def is_trustworthy(self, question: str, answer: Optional[str] = None, 
                      threshold: float = 0.7) -> tuple:
        """
        Simple binary trustworthiness check.
        
        Returns:
            tuple: (is_trustworthy: bool, result: dict)
        """
        result = self.evaluate_answer(question, answer)
        is_trustworthy = result['certainty_score'] >= threshold
        return is_trustworthy, result