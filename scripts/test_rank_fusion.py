from app.rag.retriever import (
    Retriever
)

from app.rag.bm25_retriever import (
    BM25Retriever
)

from app.rag.corpus_repository import (
    CorpusRepository
)

from app.rag.rank_fusion import (
    RankFusion
)

from app.rag.qdrant_service import (
    QdrantService
)

from app.providers.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider
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

    questions = [

        "What products do you offer?",

        "Do you provide CRM software?",

        "What cloud services do you provide?",

        "What banking solutions do you offer?"
    ]

    output_file = (
        "documents/rank_fusion_results.txt"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        for question in questions:

            file.write(
                "=" * 100 + "\n"
            )

            file.write(
                "QUESTION\n"
            )

            file.write(
                "=" * 100 + "\n"
            )

            file.write(
                question + "\n\n"
            )

            dense_results = (
                dense_retriever.retrieve(
                    question=question,
                    top_k=10
                )
            )

            bm25_results = (
                bm25_retriever.retrieve(
                    question=question,
                    top_k=10
                )
            )

            fused_results = (
                RankFusion.fuse(
                    dense_results=
                        dense_results,

                    bm25_results=
                        bm25_results,

                    top_k=10
                )
            )

            file.write(
                "DENSE RESULTS\n"
            )

            file.write(
                "-" * 100 + "\n"
            )

            for index, chunk in enumerate(
                dense_results,
                start=1
            ):

                file.write(
                    f"\nCHUNK {index}\n"
                )

                file.write(
                    f"URL: {chunk['url']}\n"
                )

                file.write(
                    chunk["text"][:500]
                )

                file.write(
                    "\n\n"
                )

            file.write(
                "\nBM25 RESULTS\n"
            )

            file.write(
                "-" * 100 + "\n"
            )

            for index, chunk in enumerate(
                bm25_results,
                start=1
            ):

                file.write(
                    f"\nCHUNK {index}\n"
                )

                file.write(
                    f"URL: {chunk['url']}\n"
                )

                file.write(
                    chunk["text"][:500]
                )

                file.write(
                    "\n\n"
                )

            file.write(
                "\nFUSED RESULTS\n"
            )

            file.write(
                "-" * 100 + "\n"
            )

            for index, chunk in enumerate(
                fused_results,
                start=1
            ):

                file.write(
                    f"\nCHUNK {index}\n"
                )

                file.write(
                    f"URL: {chunk['url']}\n"
                )

                file.write(
                    chunk["text"][:500]
                )

                file.write(
                    "\n\n"
                )

            file.write(
                "\n\n"
            )

    print(
        f"Saved results to: {output_file}"
    )


if __name__ == "__main__":
    main()