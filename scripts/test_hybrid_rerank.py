from app.rag.retriever import (
    Retriever
)

from app.rag.bm25_retriever import (
    BM25Retriever
)

from app.rag.hybrid_retriever import (
    HybridRetriever
)

from app.rag.corpus_repository import (
    CorpusRepository
)

from app.rag.qdrant_service import (
    QdrantService
)

from app.providers.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider
)

from app.providers.rerankers.cross_encoder_provider import (
    CrossEncoderProvider
)


def main():

    embedding_provider = (
        SentenceTransformerProvider(
            model_name=
            "BAAI/bge-small-en-v1.5"
        )
    )

    qdrant_service = (
        QdrantService(
            collection_name=
            "zenfuture_knowledge"
        )
    )

    dense_retriever = (
        Retriever(
            embedding_provider=
            embedding_provider,

            qdrant_service=
            qdrant_service
        )
    )

    corpus_repository = (
        CorpusRepository(
            collection_name=
            "zenfuture_knowledge"
        )
    )

    bm25_retriever = (
        BM25Retriever(
            corpus_repository=
            corpus_repository
        )
    )

    reranker_provider = (
        CrossEncoderProvider()
    )

    hybrid_retriever = (
        HybridRetriever(
            dense_retriever=
            dense_retriever,

            bm25_retriever=
            bm25_retriever,

            reranker_provider=
            reranker_provider
        )
    )

    questions = [

        "How many projects has ZenFuture delivered?",

        "What cloud services do you provide?",

        "Do you provide CRM software?",

        "What is ZenFuture's mission?",

        "What banking solutions do you offer?",

        "What products do you offer?"
    ]

    output_file = (
        "documents/hybrid_rerank_results.txt"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        for index, question in enumerate(
            questions,
            start=1
        ):

            print(
                f"\n[{index}] {question}"
            )

            results = (
                hybrid_retriever.retrieve(
                    question=question,
                    top_k=5
                )
            )

            file.write(
                "=" * 100 + "\n"
            )

            file.write(
                f"QUESTION {index}\n"
            )

            file.write(
                "=" * 100 + "\n"
            )

            file.write(
                question + "\n\n"
            )

            file.write(
                "HYBRID + RERANK RESULTS\n"
            )

            file.write(
                "-" * 100 + "\n"
            )

            for rank, chunk in enumerate(
                results,
                start=1
            ):

                file.write(
                    f"\nRANK {rank}\n"
                )

                file.write(
                    f"RERANK SCORE: {chunk.get('rerank_score', 'N/A')}\n"
                )

                file.write(
                    f"URL: {chunk.get('url', '')}\n"
                )

                file.write(
                    f"TITLE: {chunk.get('title', '')}\n\n"
                )

                file.write(
                    chunk.get(
                        "text",
                        ""
                    )
                )

                file.write(
                    "\n\n"
                )

            file.write(
                "\n\n"
            )

    print(
        f"\nResults saved to: {output_file}"
    )


if __name__ == "__main__":
    main()