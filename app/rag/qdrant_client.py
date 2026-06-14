from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams

client = QdrantClient(
    host="localhost",
    port=6333
)
