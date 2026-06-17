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

    questions = [

        "How many projects has ZenFuture delivered?",

        "What cloud solutions do you provide?",

        "Do you provide CRM software?",

        "What is ZenFuture's mission?",

        "What banking solutions do you offer?",

        "What products do you offer?"
    ]

    output_file = (
        "documents/rag_evaluation.txt"
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

            print("\n" + "=" * 100)
            print(
                f"QUESTION {index}"
            )
            print("=" * 100)

            print(question)

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

            chunks = (
                retriever.retrieve(
                    question=question,
                    top_k=10
                )
            )

            print("\nRETRIEVED CHUNKS")
            print("-" * 100)

            file.write(
                "RETRIEVED CHUNKS\n"
            )

            file.write(
                "-" * 100 + "\n"
            )

            for chunk_index, chunk in enumerate(
                chunks,
                start=1
            ):

                print(
                    f"\nCHUNK {chunk_index}"
                )

                print(
                    f"Score: {chunk['score']}"
                )

                print(
                    f"URL: {chunk['url']}"
                )

                print(
                    chunk["text"]
                )

                file.write(
                    f"\nCHUNK {chunk_index}\n"
                )

                file.write(
                    f"Score: {chunk['score']}\n"
                )

                file.write(
                    f"URL: {chunk['url']}\n"
                )

                file.write(
                    chunk["text"] + "\n"
                )

            print("\nANSWER")
            print("-" * 100)

            file.write(
                "\nANSWER\n"
            )

            file.write(
                "-" * 100 + "\n"
            )

            answer = ""

            for token in (
                rag_service.stream_ask(
                    question=question,
                    top_k=10
                )
            ):

                print(
                    token,
                    end="",
                    flush=True
                )

                answer += token

            print("\n")

            file.write(
                answer
            )

            file.write(
                "\n\n"
            )

    print(
        f"\nSaved: {output_file}"
    )


if __name__ == "__main__":
    main()