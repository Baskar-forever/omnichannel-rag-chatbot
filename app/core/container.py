from app.providers.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider
)

from app.providers.llm.ollama_provider import (
    OllamaProvider
)

from app.providers.rerankers.cross_encoder_provider import (
    CrossEncoderProvider
)

from app.rag.qdrant_service import (
    QdrantService
)

from app.rag.retriever import (
    Retriever
)

from app.rag.bm25_retriever import (
    BM25Retriever
)

from app.rag.hybrid_retriever import (
    HybridRetriever
)

from app.rag.corpus_repository import (
    CorpusRepository
)

from app.repositories.session_repository import (
    SessionRepository
)

from app.repositories.lead_repository import (
    LeadRepository
)

from app.repositories.message_repository import (
    MessageRepository
)

from app.services.rag_service import (
    RAGService
)

from app.services.chat_service import (
    ChatService
)


class ServiceContainer:

    def __init__(self):

        
        # Embeddings

        self.embedding_provider = (
            SentenceTransformerProvider(
                model_name=
                "BAAI/bge-small-en-v1.5"
            )
        )

        
        # Vector Store
        

        self.qdrant_service = (
            QdrantService(
                collection_name=
                "zenfuture_knowledge"
            )
        )

        
        # Dense Retriever
        

        self.dense_retriever = (
            Retriever(
                embedding_provider=
                    self.embedding_provider,

                qdrant_service=
                    self.qdrant_service
            )
        )

        
        # BM25
        

        self.corpus_repository = (
            CorpusRepository(
                collection_name=
                "zenfuture_knowledge"
            )
        )

        self.bm25_retriever = (
            BM25Retriever(
                corpus_repository=
                    self.corpus_repository
            )
        )

        
        # Reranker
        

        self.reranker_provider = (
            CrossEncoderProvider(
                model_name=
                "cross-encoder/ms-marco-MiniLM-L-6-v2"
            )
        )

        
        # Hybrid Retriever
        

        self.retriever = (
            HybridRetriever(
                dense_retriever=
                    self.dense_retriever,

                bm25_retriever=
                    self.bm25_retriever,

                reranker_provider=
                    self.reranker_provider
            )
        )

        
        # LLM
        

        self.llm_provider = (
            OllamaProvider(
                model="llama3.2"
            )
        )

        
        # RAG Service
        

        self.rag_service = (
            RAGService(
                retriever=
                    self.retriever,

                llm_provider=
                    self.llm_provider
            )
        )

        
        # Chat Service
        

        self.chat_service = (
            ChatService(
                rag_service=
                    self.rag_service,

                session_repository=
                    SessionRepository(),

                lead_repository=
                    LeadRepository(),

                message_repository=
                    MessageRepository()
            )
        )


container = ServiceContainer()