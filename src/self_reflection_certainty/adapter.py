"""
LLM client adapters for different providers.
"""
from abc import ABC, abstractmethod
import os
import time
import litellm
from typing import Optional


class LLMClient(ABC):
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate a response to the given prompt."""
        pass


class LiteLLMClient(LLMClient):
    
    def __init__(self, 
                 model: Optional[str] = None, 
                 api_key: Optional[str] = None,
                 max_retries: int = 3,
                 retry_delay: float = 1.0,
                 **kwargs):
        """
        Initialize LiteLLM client with generic configuration.
        
        Args:
            model: Model name (e.g., 'gpt-4', 'gemini-pro', 'ollama/llama2:7b')
                  If None, uses LLM_MODEL env var or defaults to 'gpt-4'
            api_key: API key for the LLM provider
                    If None, uses LLM_API_KEY env var
            max_retries: Maximum number of retries for rate limit errors
            retry_delay: Base delay between retries (will be exponential)
            **kwargs: Additional arguments passed to litellm.completion
        """
        # Get model from env var or use default
        self.model = model or os.getenv('LLM_MODEL', 'gpt-4')
        
        # Get API key from env var
        self.api_key = api_key or os.getenv('LLM_API_KEY')
        
        # Check if this is a local model (like Ollama)
        is_local_model = self.model.startswith('ollama/') or self.model.startswith('local/')
        
        if not self.api_key and not is_local_model:
            raise ValueError(
                "API key not provided. Please set LLM_API_KEY environment variable "
                "or pass api_key parameter. Example:\n"
                "export LLM_API_KEY='your-api-key-here'\n"
                "Or in Python:\n"
                "client = LiteLLMClient(api_key='your-api-key-here')\n\n"
                "Note: Local models like 'ollama/llama2:7b' don't require API keys."
            )
        
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.completion_kwargs = kwargs
    
    def generate_response(self, prompt: str) -> str:
        """Generate response with automatic retry on rate limit errors."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                # Prepare completion arguments
                completion_args = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    **self.completion_kwargs
                }
                
                # Only add API key for non-local models
                if not (self.model.startswith('ollama/') or self.model.startswith('local/')):
                    completion_args["api_key"] = self.api_key
                
                response = litellm.completion(**completion_args)
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()
                
                # Check if this is a rate limit error
                is_rate_limit = any(phrase in error_str for phrase in [
                    "rate limit", "quota", "too many requests", "429", 
                    "rate_limit", "quota_exceeded", "throttled"
                ])
                
                # If it's a rate limit error and we haven't exceeded max retries
                if is_rate_limit and attempt < self.max_retries:
                    # Calculate exponential backoff delay
                    delay = self.retry_delay * (2 ** attempt)
                    
                    print(f"⚠️  Rate limit hit (attempt {attempt + 1}/{self.max_retries + 1}). "
                          f"Retrying in {delay:.1f}s...")
                    
                    time.sleep(delay)
                    continue
                
                # If it's not a rate limit error, or we've exhausted retries, raise the exception
                break
        
        # If we get here, all retries failed or it's a non-retryable error
        if "authentication" in str(last_exception).lower() or "unauthorized" in str(last_exception).lower():
            raise Exception(
                f"Authentication failed. Please check your API key for {self.model}.\n"
                f"Error: {last_exception}\n"
                "Make sure LLM_API_KEY is set correctly."
            )
        elif "quota" in str(last_exception).lower() or "rate limit" in str(last_exception).lower():
            raise Exception(
                f"Rate limit or quota exceeded after {self.max_retries + 1} attempts. "
                f"Error: {last_exception}\n"
                "Please check your API usage limits or increase max_retries."
            )
        else:
            raise Exception(f"Error generating response after {self.max_retries + 1} attempts: {last_exception}")
    
    def __repr__(self):
        return f"LiteLLMClient(model='{self.model}', max_retries={self.max_retries})"
