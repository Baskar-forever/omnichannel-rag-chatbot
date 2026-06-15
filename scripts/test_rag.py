from app.rag.retriever import Retriever

from app.rag.qdrant_service import QdrantService

from app.providers.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider
)

from app.providers.llm.ollama_provider import (
    OllamaProvider
)

from app.services.rag_service import (
    RAGService
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

    llm_provider = (
        OllamaProvider(
            model="llama3.2"
        )
    )

    rag_service = (
        RAGService(
            retriever=retriever,
            llm_provider=llm_provider
        )
    )

    question = (
        "How many projects has ZenFuture delivered?"
    )

    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)

    print(question)

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)

    for token in rag_service.stream_ask(
        question=question,
        top_k=5
    ):
        print(
            token,
            end="",
            flush=True
        )

    print("\n")

    print("=" * 80)
    print("DONE")
    print("=" * 80)


if __name__ == "__main__":
    main()