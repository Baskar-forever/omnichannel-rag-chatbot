class Retriever:

    def __init__(self,embedding_provider,qdrant_service):
        self.embedding_provider = (
            embedding_provider
        )

        self.qdrant_service = (
            qdrant_service
        )

    def retrieve(
        self,
        question: str,
        top_k: int = 10
    ):

        query_embedding = (
            self.embedding_provider
            .embed_text(
                question
            )
        )

        results = (
            self.qdrant_service.search(
                query_embedding=
                    query_embedding,
                limit=top_k * 2
            )
        )

        chunks = []

        seen_chunks = set()

        for result in results:

            text = (
                result.payload.get(
                    "text",
                    ""
                ).strip()
            )

            if text in seen_chunks:
                continue

            seen_chunks.add(
                text
            )

            chunks.append(
                {
                    "text": text,

                    "url":
                        result.payload.get(
                            "url",
                            ""
                        ),

                    "title":
                        result.payload.get(
                            "title",
                            ""
                        ),

                    "score":
                        result.score
                }
            )

            if len(chunks) >= top_k:
                break

        return chunks
