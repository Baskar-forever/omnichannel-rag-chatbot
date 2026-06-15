from app.prompts.rag_prompt import build_rag_prompt


class RAGService:

    def __init__(self, retriever, llm_provider):

        self.retriever = retriever
        self.llm_provider = llm_provider

    def _build_context(self,chunks: list[dict]) -> str:

        context_parts = []

        for chunk in chunks:

            context_parts.append(
                chunk["text"]
            )

        return "\n\n".join(
            context_parts
        )

    def ask(self, question: str, top_k: int = 5) -> dict:

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

        prompt = (
            build_rag_prompt(
                context=context,
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
            "sources": chunks
        }

    def stream_ask(self,question: str,top_k: int = 5
    ):

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

        prompt = (
            build_rag_prompt(
                context=context,
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