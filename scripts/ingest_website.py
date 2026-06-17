from crawler.website_crawler import (
    WebsiteCrawler
)

from crawler.content_extractor import (
    ContentExtractor
)

from app.services.ingestion_service import (
    IngestionService
)

from app.rag.qdrant_service import (
    QdrantService
)

from app.providers.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider
)


def main():

    crawler = WebsiteCrawler()

    urls = crawler.crawl("https://zenfuture.in")

    urls = [
        url for url in urls
        if not url.startswith("https://zenfuture.in/index.php")
    ]

    print(
        f"Found {len(urls)} URLs"
    )

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

    qdrant_service.create_collection(
        vector_size=384
    )

    ingestion_service = (
        IngestionService(
            extractor=
                ContentExtractor(),

            embedding_provider=
                embedding_provider,

            qdrant_service=
                qdrant_service
        )
    )

    result = (
        ingestion_service.ingest_urls(
            urls
        )
    )

    print(result)


if __name__ == "__main__":
    main()