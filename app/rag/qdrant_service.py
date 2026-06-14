from app.rag.qdrant_client import client

COLLECTION_NAME = "zenfuture_knowledge"


class QdrantService:

    def get_collections(self):
        return client.get_collections()