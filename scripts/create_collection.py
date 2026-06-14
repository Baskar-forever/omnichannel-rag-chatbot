from qdrant_client.models import Distance
from qdrant_client.models import VectorParams

from app.rag.qdrant_client import client

COLLECTION_NAME = "zenfuture_knowledge"

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

print("Collection created")