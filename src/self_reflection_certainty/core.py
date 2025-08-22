"""
Core self-reflection certainty implementation.
"""
import time
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
                 num_evaluations: int = 2,
                 debug: bool = False):
        """
        Initialize the self-reflection certainty evaluator.
        
        Args:
            client: LLM client adapter for making API calls
                   If None, creates a LiteLLMClient using environment variables
            num_evaluations: Number of self-evaluation rounds to perform
            debug: If True, prints detailed conversation flow
        """
        if client is None:
            # Auto-create client using environment variables for security
            self.client = LiteLLMClient()
        else:
            self.client = client
        
        self.num_evaluations = num_evaluations
        self.debug = debug
    
    def _print_debug_info(self, question: str, answer: str, evaluation_prompts: List[str], 
                          evaluations: List[str], scores: List[float], final_score: float,
                          timings: Dict[str, float]):
        """Print debug information showing the full conversation flow."""
        if not self.debug:
            return
            
        print("\n" + "="*50)
        print("🔍 DEBUG: Conversation Flow")
        print("="*50)
        
        print(f"Q: {question}")
        print(f"A: {answer}")
        print()
        
        # Show self-reflection differences and results
        for i, (prompt, evaluation, score, timing) in enumerate(zip(evaluation_prompts, evaluations, scores, timings['evaluations']), 1):
            # Extract key difference in prompt
            if "Take a moment to carefully consider" in prompt:
                prompt_type = "Reflective"
            else:
                prompt_type = "Standard"
            
            print(f"Eval {i} ({prompt_type}): {evaluation} → {score:.3f} ({timing:.2f}s)")
        
        print()
        print(f"Final: {final_score:.3f} | Total: {timings['total']:.2f}s")
        print("="*50)
        print()
    
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
            - timings: Dictionary with timing information
        """
        start_time = time.time()
        timings = {}
        
        # Step 1: Generate answer if not provided
        if answer is None:
            answer_start = time.time()
            answer = self.client.generate_response(question)
            timings['answer_generation'] = time.time() - answer_start
        else:
            timings['answer_generation'] = 0.0
        
        # Step 2: Get multiple self-evaluations
        evaluation_prompts = get_evaluation_prompts(question, answer, self.num_evaluations)
        evaluations = []
        scores = []
        evaluation_timings = []
        
        for prompt in evaluation_prompts:
            eval_start = time.time()
            evaluation = self.client.generate_response(prompt)
            eval_time = time.time() - eval_start
            
            evaluations.append(evaluation)
            evaluation_timings.append(eval_time)
            score = map_response_to_score(evaluation)
            scores.append(score)
        
        timings['evaluations'] = evaluation_timings
        
        # Step 3: Compute final certainty score (average of evaluations)
        certainty_score = sum(scores) / len(scores) if scores else 0.0
        
        # Calculate total time
        timings['total'] = time.time() - start_time
        
        # Print debug info if enabled
        self._print_debug_info(question, answer, evaluation_prompts, evaluations, scores, certainty_score, timings)
        
        return {
            'answer': answer,
            'certainty_score': certainty_score,
            'evaluation_scores': scores,
            'evaluations': evaluations,
            'timings': timings
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
    def from_env(cls, num_evaluations: int = 2, debug: bool = False) -> 'SelfReflectionCertainty':
        """
        Create evaluator using environment variables (recommended).
        
        Args:
            num_evaluations: Number of evaluation rounds
            debug: If True, prints detailed conversation flow
            
        Requires:
        - LLM_API_KEY: Your API key
        - LLM_MODEL: Model name (optional, defaults to 'gpt-4')
        
        Example:
            export LLM_API_KEY="your-api-key"
            export LLM_MODEL="gpt-4"
            
            evaluator = SelfReflectionCertainty.from_env(debug=True)
        """
        return cls(num_evaluations=num_evaluations, debug=debug)