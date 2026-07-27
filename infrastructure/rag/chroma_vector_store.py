from collections.abc import Sequence
from typing import Any

import chromadb

from domain.rag_models import DocumentChunk, RetrivedChunk

class ChromaVectorStore:

    def __init__(
        self,
        persist_directory: str = "knowledge/vector_store",
        collection_name: str = "goalkotha_ai_security",
    ) -> None:
        self._client = chromadb.PersistentClient(
            path=persist_directory
        )

        self._collection_name = collection_name

        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add(
        self,
        chunks: Sequence[DocumentChunk],
        embeddings: Sequence[Sequence[float]],
    ) -> None:

        self._collection.upsert(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            embeddings=[
                list(embedding)
                for embedding in embeddings
            ],
            metadatas=[
                self._serialize_metadata(chunk)
                for chunk in chunks
            ],
        )

    def search(
        self,
        query_embedding: Sequence[float],
    ):
        print("You are here")

    def clear(self) -> None:
        self._client.delete_collection(
            self._collection_name
        )
        self._collection = self._client.create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        
    @staticmethod
    def _serialize_metadata(
        chunk: DocumentChunk,
    ) -> dict[str, Any]:
        metadata: dict[str, Any] = {
            "document_id": chunk.document_id,
            "title": chunk.title,
            "source_name": chunk.source_name,
            "source_url": chunk.source_url,
            "chunk_index": chunk.chunk_index,
        }

        for key, value in chunk.metadata.items():
            if isinstance(value, (str, int, float, bool)):
                metadata[key] = value
            elif value is None:
                metadata[key] = ""
            else:
                metadata[key]=str(value)

        return metadata