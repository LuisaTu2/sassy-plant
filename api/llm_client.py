from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Generic LLM client interface for provider-agnostic usage"""

    def __init__(self, api_key=None):
        self.api_key = api_key

    @abstractmethod
    def create_client(self):
        pass
