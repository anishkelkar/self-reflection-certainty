"""
LLM client adapters for different providers.
"""
from abc import ABC, abstractmethod
import litellm


class LLMClient(ABC):
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate a response to the given prompt."""
        pass


class LiteLLMClient(LLMClient):
    
    def __init__(self, model: str, api_key: str, **kwargs):
        self.model = model
        self.api_key = api_key
        self.completion_kwargs = kwargs
    
    def generate_response(self, prompt: str) -> str:

        try:
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                api_key=self.api_key,
                **self.completion_kwargs
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating response: {e}")
