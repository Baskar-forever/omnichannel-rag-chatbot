from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(
        self,
        corpus_repository
    ):

        self.corpus_repository = (
            corpus_repository
        )

        self._build_index()

    def _build_index(self):

        self.chunks = (
            self.corpus_repository
            .get_all_chunks()
        )

        tokenized = [

            chunk["text"]
            .lower()
            .split()

            for chunk
            in self.chunks
        ]

        self.bm25 = (
            BM25Okapi(
                tokenized
            )
        )

    def retrieve(
        self,
        question,
        top_k=10
    ):

        query = (
            question.lower()
            .split()
        )

        scores = (
            self.bm25.get_scores(
                query
            )
        )

        ranked = sorted(
            zip(
                self.chunks,
                scores
            ),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            item[0]
            for item
            in ranked[:top_k]
        ]