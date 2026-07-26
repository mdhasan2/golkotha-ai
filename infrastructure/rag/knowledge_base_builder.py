from collections.abc import Sequence 

from application.ports.embedding_port import EmbeddingPort
from application.ports.vector_store_port import VectorStorePort
from domain.rag_models import DocumentChunk, KnowledgeDocument
from infrastructure.rag.document_chunker import DocumentChunker

class KnowledgeBaseBuilder:
    def __init__(
        self,
        chunker: DocumentChunker,
        embedding_service: EmbeddingPort,
        vector_store: VectorStorePort,
        batch_size: int = 32,
    ) -> None:

        self._chunker = chunker
        self._embedding_srevice = embedding_service
        self._vector_store = vector_store
        self._batch_size = batch_size

    def build(
        self,
        documents: Sequence[KnowledgeDocument],
        rebuild: bool = False,
    ) -> int:
        if rebuild:
            self._vector_store.clear()

        chunks: list[DocumentChunk] = []
        for document in documents:
            chunks.extend(
                self._chunker.chunk(document)
            )

        for start in range(
            0,
            len(chunks),
            self._batch_size,
        ):
            batch = chunks[
                start : start + self._batch_size
            ]

            embeddings = (
                self._embedding_srevice.embed_documents(
                    [chunk.text for chunk in batch]
                )
            )

            self._vector_store.add(
                chunks=batch,
                embeddings=embeddings,
            )


