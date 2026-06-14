from qdrant_client.models import PointStruct

from app.rag.qdrant_client import client

client.upsert(
    collection_name="zenfuture_knowledge",
    points=[
        PointStruct(
            id=1,
            vector=[0.1] * 384,
            payload={
                "source": "website",
                "text": "ZenFuture provides cloud services."
            }
        )
    ]
)

print("Inserted")