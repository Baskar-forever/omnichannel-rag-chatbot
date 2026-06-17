from abc import (
    ABC,
    abstractmethod
)


class RerankerProvider(
    ABC
):

    @abstractmethod
    def rerank(
        self,
        question: str,
        chunks: list,
        top_k: int
    ):
        pass