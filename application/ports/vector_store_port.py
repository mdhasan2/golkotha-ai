from collections.abc import Sequence
from typing import protocol

from domain.rag_models import DocumentChunk, RetrivedChunk

class VectorStorePort(protocol):

    def add(
        self,
        chunks: Sequence[DocumentChunk],
        embeddings: Sequence[Sequence[float]],
    ) -> None:
        ...

    def search(
        self,
        query_embedding: Sequence[float],
        limit: int = 8,
        filters: dict[str, str] | None = None,
    ) -> list[RetrivedChunk]:
        ...

    def count(self) -> int:
        ...

    def clear(self) -> None:
        ...
    