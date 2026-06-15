from app.providers.llm.ollama_provider import (
    OllamaProvider
)


def main():

    llm = OllamaProvider()

    answer = llm.stream_generate(
        "What is Python?"
    )

    for chunk in answer:
        print(
            chunk,
            end="",
            flush=True
        )

print()


if __name__ == "__main__":
    main()