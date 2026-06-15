from ollama import chat

from app.providers.llm.base import (
    LLMProvider
)


class OllamaProvider(
    LLMProvider
):

    def __init__(
        self,
        model="llama3.2"
    ):
        self.model = model

    def generate(
        self,
        prompt: str
    ) -> str:

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    def stream_generate(
        self,
        prompt: str
    ):

        stream = chat(
            model=self.model,
            stream=True,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        for chunk in stream:

            yield chunk["message"]["content"]