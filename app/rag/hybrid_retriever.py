from app.rag.rank_fusion import (
    RankFusion
)


class HybridRetriever:

    def __init__(
        self,
        dense_retriever,
        bm25_retriever,
        reranker_provider
    ):

        self.dense_retriever = (
            dense_retriever
        )

        self.bm25_retriever = (
            bm25_retriever
        )

        self.reranker_provider = (
            reranker_provider
        )

    def retrieve(
        self,
        question: str,
        top_k: int = 5
    ):

        dense_results = (
            self.dense_retriever.retrieve(
                question=question,
                top_k=20
            )
        )

        bm25_results = (
            self.bm25_retriever.retrieve(
                question=question,
                top_k=20
            )
        )

        fused_results = (
            RankFusion.fuse(
                dense_results=
                    dense_results,

                bm25_results=
                    bm25_results,

                top_k=20
            )
        )

        if not fused_results:

            return []

        reranked_results = (
            self.reranker_provider.rerank(
                question=question,
                chunks=fused_results,
                top_k=top_k
            )
        )

        return reranked_results