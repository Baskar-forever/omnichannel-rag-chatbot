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
        # "What cloud solutions do you provide?",
        # "Do you provide CRM software?",
        # "What is ZenFuture's mission?",
        # "What banking solutions do you offer?"
    ]

    output_file = "documents/rag_test_results.txt"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        for index, question in enumerate(
            questions,
            start=1
        ):

            print(f"\n[{index}] {question}")

            file.write("=" * 100 + "\n")
            file.write(f"QUESTION {index}\n")
            file.write("=" * 100 + "\n")
            file.write(question + "\n\n")

            answer = ""

            for token in rag_service.stream_ask(
                question=question,
                top_k=5
            ):

                print(
                    token,
                    end="",
                    flush=True
                )

                answer += token

            print("\n")

            file.write("ANSWER\n")
            file.write("-" * 100 + "\n")
            file.write(answer)
            file.write("\n\n")

    print(
        f"\nResults saved to: {output_file}"
    )


if __name__ == "__main__":
    main()