from app.rag.retriever import Retriever
from app.rag.qdrant_service import QdrantService
from app.providers.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider
)


def main():

    embedding_provider = (
        SentenceTransformerProvider(
            model_name="BAAI/bge-small-en-v1.5"
        )
    )

    qdrant_service = (
        QdrantService(
            collection_name="zenfuture_knowledge"
        )
    )

    retriever = (
        Retriever(
            embedding_provider=embedding_provider,
            qdrant_service=qdrant_service
        )
    )

    results = retriever.retrieve(
        question="How many projects has ZenFuture delivered?",
        top_k=5
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print("\n")
        print("=" * 80)

        print(f"RESULT {index}")

        print("=" * 80)

        print(result)


if __name__ == "__main__":
    main()