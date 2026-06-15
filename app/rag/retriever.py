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
        top_k: int = 5
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
                limit=top_k
            )
        )

        chunks = []

        for result in results:

            chunks.append(
                {
                    "text":
                        result.payload.get(
                            "text",
                            ""
                        ),

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

        return chunks
