from app.rag.qdrant_client import client

results = client.query_points(
    collection_name="zenfuture_knowledge",
    query=[0.1] * 384,
    limit=3
)

print(results)