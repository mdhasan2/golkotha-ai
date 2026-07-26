
from collections.abc import Sequence
from typing import Protocol

class EmbeddingPort(Protocol):

    @property
    def dimension(self) -> int:
        ...
    
    def embed_documents(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:
        ...
    
    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        ...