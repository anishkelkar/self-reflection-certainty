"""
LLM client adapters for different providers.
"""
from abc import ABC, abstractmethod
import os
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
                 **kwargs):
        """
        Initialize LiteLLM client with generic configuration.
        
        Args:
            model: Model name (e.g., 'gpt-4', 'gemini-pro', 'ollama/llama2:7b')
                  If None, uses LLM_MODEL env var or defaults to 'gpt-4'
            api_key: API key for the LLM provider
                    If None, uses LLM_API_KEY env var
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
        
        self.completion_kwargs = kwargs
    
    def generate_response(self, prompt: str) -> str:
        try:
            # For local models, don't pass API key
            if self.model.startswith('ollama/') or self.model.startswith('local/'):
                response = litellm.completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    **self.completion_kwargs
                )
            else:
                response = litellm.completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    api_key=self.api_key,
                    **self.completion_kwargs
                )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Provide helpful error messages
            if "authentication" in str(e).lower() or "unauthorized" in str(e).lower():
                raise Exception(
                    f"Authentication failed. Please check your API key for {self.model}.\n"
                    f"Error: {e}\n"
                    "Make sure LLM_API_KEY is set correctly."
                )
            elif "quota" in str(e).lower() or "rate limit" in str(e).lower():
                raise Exception(
                    f"Rate limit or quota exceeded. Error: {e}\n"
                    "Please check your API usage limits."
                )
            else:
                raise Exception(f"Error generating response: {e}")
    
    def __repr__(self):
        return f"LiteLLMClient(model='{self.model}')"
