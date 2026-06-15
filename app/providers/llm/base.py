from abc import ABC
from abc import abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str
    ) -> str:
        pass

    @abstractmethod
    def stream_generate(
        self,
        prompt: str
    ):
        pass