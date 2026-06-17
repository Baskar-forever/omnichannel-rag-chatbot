from app.rag.corpus_repository import (
    CorpusRepository
)

from app.rag.bm25_retriever import (
    BM25Retriever
)


def main():

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
        "documents/bm25_test_results.txt"
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

            results = (
                bm25_retriever.retrieve(
                    question=question,
                    top_k=10
                )
            )

            file.write(
                "TOP CHUNKS\n"
            )

            file.write(
                "-" * 100 + "\n"
            )

            for index, chunk in enumerate(
                results,
                start=1
            ):

                file.write(
                    f"\nCHUNK {index}\n"
                )

                file.write(
                    f"URL: {chunk['url']}\n"
                )

                file.write(
                    f"TITLE: {chunk['title']}\n\n"
                )

                file.write(
                    chunk["text"]
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