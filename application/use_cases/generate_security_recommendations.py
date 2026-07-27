from application.ports.embedding_port import EmbeddingPort
from application.ports.vector_store_port import VectorStorePort

from domain.rag_models import (
    PredictionContext,
    RetrivedChunk,
)

from infrastructure.rag.security_query_builder import (
    SecurityQueryBuilder
)

class GenerateSecurityRecommendations:

    def __init__(
        self,
        embedding_service: EmbeddingPort,
        vector_store: VectorStorePort,
        query_builder: SecurityQueryBuilder,
    ) -> None:
        self._embedding_service = embedding_service
        self._vector_store = vector_store
        self._query_builder = query_builder
    def execute(
        self,
        context: PredictionContext,
    )-> None:
        retrieved = self._retrieve(
            context=context,
        )
        # pass
        
    def _retrieve(
        self,
        context: PredictionContext,
    ) -> list[RetrivedChunk]:
        query = self._query_builder.build(context)
        # print(query)
        embedding = (
            self._embedding_service.embed_query(query)
        )

        results = self._vector_store.search(
            query_embedding=embedding,
        )

        print(results)

        