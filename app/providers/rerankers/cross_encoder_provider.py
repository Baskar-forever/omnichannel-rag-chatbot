from sentence_transformers import (
    CrossEncoder
)

from app.providers.rerankers.base import (
    RerankerProvider
)


class CrossEncoderProvider(
    RerankerProvider
):

    def __init__(
        self,
        model_name=
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):

        self.model = (
            CrossEncoder(
                model_name
            )
        )

    def rerank(
        self,
        question: str,
        chunks: list,
        top_k: int = 5
    ):

        pairs = [

            (
                question,
                chunk["text"]
            )

            for chunk
            in chunks
        ]

        scores = (
            self.model.predict(
                pairs
            )
        )

        ranked = []

        for chunk, score in zip(
            chunks,
            scores
        ):

            item = dict(chunk)

            item[
                "rerank_score"
            ] = float(score)

            ranked.append(
                item
            )

        ranked.sort(
            key=lambda x:
                x["rerank_score"],
            reverse=True
        )

        return ranked[:top_k]