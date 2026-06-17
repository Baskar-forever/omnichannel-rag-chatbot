class RankFusion:

    @staticmethod
    def fuse(
        dense_results,
        bm25_results,
        top_k=10
    ):

        scores = {}

        documents = {}

        k = 60

        for rank, doc in enumerate(
            dense_results,
            start=1
        ):

            key = (
                doc["url"]
                + "::"
                + doc["text"][:100]
            )

            documents[key] = doc

            scores[key] = (
                scores.get(
                    key,
                    0
                )
                +
                (1 / (k + rank))
            )

        for rank, doc in enumerate(
            bm25_results,
            start=1
        ):

            key = (
                doc["url"]
                + "::"
                + doc["text"][:100]
            )

            documents[key] = doc

            scores[key] = (
                scores.get(
                    key,
                    0
                )
                +
                (1 / (k + rank))
            )

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for key, _ in ranked[:top_k]:

            results.append(
                documents[key]
            )

        return results