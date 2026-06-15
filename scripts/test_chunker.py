from crawler.content_extractor import ContentExtractor

from app.rag.content_cleaner import ContentCleaner
from app.rag.chunker import Chunker


TEST_URL = "https://zenfuture.in/about.php"


def main():

    extractor = ContentExtractor()
    cleaner = ContentCleaner()
    chunker = Chunker(
        chunk_size=500,
        chunk_overlap=100
    )

    print(f"\nExtracting: {TEST_URL}\n")

    document = extractor.extract(
        TEST_URL
    )

    print("document\n",document)
    cleaned_content = cleaner.clean(document.content)
    

    chunks = chunker.chunk(
        text=cleaned_content,
        metadata={
            "url": document.url,
            "title": document.title
        }
    )

    print("=" * 80)
    print("DOCUMENT INFO")
    print("=" * 80)

    print(f"Title: {document.title}")
    print(f"URL: {document.url}")

    print("\n")
    print("=" * 80)
    print("CHUNK SUMMARY")
    print("=" * 80)



    print(f"Total Chunks: {len(chunks)}")


    
    with open(
    "documents/chunks_preview.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for index, chunk in enumerate(chunks, start=1):

            f.write("=" * 100)
            f.write("\n")

            f.write(f"Chunk {index}\n")
            f.write(f"Chunk ID: {chunk.chunk_id}\n")
            f.write(f"Length: {len(chunk.text)}\n")

            f.write("\n")

            f.write(chunk.text)

            f.write("\n\n")


if __name__ == "__main__":
    main()