from app.rag.qdrant_client import client


class CorpusRepository:

    def __init__(
        self,
        collection_name: str
    ):

        self.collection_name = (
            collection_name
        )

    def get_all_chunks(self):

        all_chunks = []

        offset = None

        while True:

            points, offset = (
                client.scroll(
                    collection_name=
                        self.collection_name,

                    limit=100,

                    offset=offset,

                    with_payload=True,

                    with_vectors=False
                )
            )

            for point in points:

                payload = (
                    point.payload
                )

                all_chunks.append(
                    {
                        "text":
                            payload.get(
                                "text",
                                ""
                            ),

                        "url":
                            payload.get(
                                "url",
                                ""
                            ),

                        "title":
                            payload.get(
                                "title",
                                ""
                            )
                    }
                )

            if offset is None:

                break

        return all_chunks