"""
Core self-reflection certainty implementation.
"""
from typing import List, Optional, Dict, Any
from .adapter import LLMClient, LiteLLMClient
from .prompts import get_evaluation_prompts
from .utils import map_response_to_score


class SelfReflectionCertainty:
    """
    Implements the self-reflection certainty algorithm from Chen & Mueller (ACL'24).
    
    This class evaluates the trustworthiness of LLM outputs by having the model
    self-evaluate its own answers using multiple evaluation prompts.
    """
    
    def __init__(self, 
                 client: Optional[LLMClient] = None, 
                 num_evaluations: int = 2):
        """
        Initialize the self-reflection certainty evaluator.
        
        Args:
            client: LLM client adapter for making API calls
                   If None, creates a LiteLLMClient using environment variables
            num_evaluations: Number of self-evaluation rounds to perform
        """
        if client is None:
            # Auto-create client using environment variables for security
            self.client = LiteLLMClient()
        else:
            self.client = client
        
        self.num_evaluations = num_evaluations
    
    def evaluate_answer(self, question: str, answer: Optional[str] = None) -> Dict[str, Any]:
        """
        Evaluate the certainty of an answer to a question.
        
        Args:
            question: The question being asked
            answer: The answer to evaluate. If None, generates one automatically.
            
        Returns:
            Dictionary containing:
            - answer: The evaluated answer
            - certainty_score: Float between 0-1 indicating confidence
            - evaluation_scores: List of individual evaluation scores
            - evaluations: List of evaluation responses
        """
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
        
        Args:
            question: The question being asked
            answer: The answer to evaluate. If None, generates one automatically.
            threshold: Minimum certainty score to consider trustworthy (default: 0.7)
            
        Returns:
            tuple: (is_trustworthy: bool, result: dict)
        """
        result = self.evaluate_answer(question, answer)
        is_trustworthy = result['certainty_score'] >= threshold
        return is_trustworthy, result
    
    @classmethod
    def from_env(cls, num_evaluations: int = 2) -> 'SelfReflectionCertainty':
        """
        Create evaluator using environment variables (recommended).
        
        Requires:
        - LLM_API_KEY: Your API key
        - LLM_MODEL: Model name (optional, defaults to 'gpt-4')
        
        Example:
            export LLM_API_KEY="your-api-key"
            export LLM_MODEL="gpt-4"
            
            evaluator = SelfReflectionCertainty.from_env()
        """
        return cls(num_evaluations=num_evaluations)