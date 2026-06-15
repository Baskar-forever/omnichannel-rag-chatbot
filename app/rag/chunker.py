from langchain_text_splitters import (
RecursiveCharacterTextSplitter
)

from app.models.chunk import Chunk
import uuid
class Chunker:

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150
    ):

        self.text_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    " ",
                    ""
                ]
            )
        )

    def chunk(
        self,
        text: str,
        metadata: dict | None = None
    ) -> list[Chunk]:

        metadata = metadata or {}

        texts = self.text_splitter.split_text(
            text
        )

        chunks = []

        for index, chunk_text in enumerate(texts):

            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    text=chunk_text,
                    metadata=metadata.copy()
                )
            )

        return chunks

