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

    