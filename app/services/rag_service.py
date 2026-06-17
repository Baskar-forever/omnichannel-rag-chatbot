from app.prompts.rag_prompt import (
    build_rag_prompt
)


class RAGService:

    def __init__(
        self,
        retriever,
        llm_provider
    ):

        self.retriever = retriever

        self.llm_provider = (
            llm_provider
        )

    def _build_context(
        self,
        chunks: list[dict]
    ) -> str:

        context_parts = []

        for chunk in chunks:

            context_parts.append(
                chunk["text"]
            )

        return "\n\n".join(
            context_parts
        )

    def retrieve_context(
        self,
        question: str,
        top_k: int = 10
    ) -> dict:

        chunks = (
            self.retriever.retrieve(
                question=question,
                top_k=top_k
            )
        )

        context = (
            self._build_context(
                chunks
            )
        )

        return {
            "context": context,
            "sources": chunks
        }

    def ask(
        self,
        question: str,
        top_k: int = 10
    ) -> dict:

        retrieval = (
            self.retrieve_context(
                question=question,
                top_k=top_k
            )
        )

        prompt = (
            build_rag_prompt(
                context=retrieval["context"],
                question=question
            )
        )

        answer = (
            self.llm_provider.generate(
                prompt
            )
        )

        return {
            "answer": answer,
            "sources":
                retrieval["sources"]
        }

    def stream_ask(
        self,
        question: str,
        top_k: int = 10
    ):

        retrieval = (
            self.retrieve_context(
                question=question,
                top_k=top_k
            )
        )

        prompt = (
            build_rag_prompt(
                context=retrieval["context"],
                question=question
            )
        )

        for token in (
            self.llm_provider
            .stream_generate(
                prompt
            )
        ):
            yield token