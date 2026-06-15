from app.rag.content_cleaner import (
ContentCleaner
)

from app.rag.chunker import Chunker

class IngestionService:

    def __init__(
        self,
        extractor,
        embedding_provider,
        qdrant_service
    ):

        self.extractor = extractor

        self.embedding_provider = (
            embedding_provider
        )

        self.qdrant_service = (
            qdrant_service
        )

        self.cleaner = (
            ContentCleaner()
        )

        self.chunker = (
            Chunker(
                chunk_size=500,
                chunk_overlap=85
            )
        )

    def ingest_url(
        self,
        url: str
    ):

        document = (
            self.extractor.extract(
                url
            )
        )

        cleaned_content = (
            self.cleaner.clean(
                document.content
            )
        )

        chunks = (
            self.chunker.chunk(
                text=cleaned_content,
                metadata={
                    "url":
                        document.url,

                    "title":
                        document.title,

                    "source":
                        document.source
                }
            )
        )

        embeddings = (
            self.embedding_provider
            .embed_batch(
                [
                    chunk.text
                    for chunk in chunks
                ]
            )
        )

        self.qdrant_service.upsert_chunks(
            chunks=chunks,
            embeddings=embeddings
        )

        return {
            "url": url,
            "chunks": len(chunks)
        }

    def ingest_urls(
        self,
        urls: list[str]
    ):

        total_chunks = 0

        for url in urls:

            result = (
                self.ingest_url(url)
            )

            total_chunks += (
                result["chunks"]
            )

            print(
                f"Ingested "
                f"{url} "
                f"({result['chunks']} chunks)"
            )

        return {
            "urls": len(urls),
            "chunks": total_chunks
        }
