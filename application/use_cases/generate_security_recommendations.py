from typing import Any

from application.ports.embedding_port import EmbeddingPort
from application.ports.llm_port import LLMPort
from application.ports.vector_store_port import VectorStorePort

from domain.rag_models import (
    Citation,
    GroundedRecommendation,
    PredictionContext,
    RetrivedChunk,
)

from infrastructure.rag.citation_parser import CitationParser
from infrastructure.rag.security_prompt_builder import (
    SecurityPromptBuilder,
)

from infrastructure.rag.security_query_builder import (
    SecurityQueryBuilder
)

class GenerateSecurityRecommendations:

    def __init__(
        self,
        embedding_service: EmbeddingPort,
        vector_store: VectorStorePort,
        llm: LLMPort,
        query_builder: SecurityQueryBuilder,
        prompt_builder: SecurityPromptBuilder,
        citation_parser: CitationParser,
    ) -> None:
        self._embedding_service = embedding_service
        self._vector_store = vector_store
        self._llm = llm
        self._query_builder = query_builder
        self._prompt_builder = prompt_builder
        self._citation_parser = citation_parser
    def execute(
        self,
        context: PredictionContext,
        retrieval_limit: int = 8,
        minimum_score: float = 0.20,
    )-> GroundedRecommendation:
        retrieved = self._retrieve(
            context=context,
            limit=retrieval_limit,
            minimum_score=minimum_score,
        )

        if not retrieved:
            raise RuntimeError(
                "No sufficently relevant security guidance "
                "was retrieved."
            )

        system_prompt, user_prompt= self._prompt_builder.build(
            context=context,
            retrieved=retrieved,
        )
        # print(f"System Prompt: \n{system_prompt}\n, User Prompt: \n{user_prompt}")

        raw_response = self._llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        # print(f"LLM Response: \n{raw_response}\n")

        payload, citations = self._citation_parser.parse(
            raw_response=raw_response,
            retrieved=retrieved,
        )

        return self._to_domain_result(
            payload=payload,
            citations=citations,
            raw_response=raw_response,
        )

    def _retrieve(
        self,
        context: PredictionContext,
        limit: int,
        minimum_score: float,
    ) -> list[RetrivedChunk]:
        query = self._query_builder.build(context)
        # print(query)
        embedding = (
            self._embedding_service.embed_query(query)
        )

        # print("Query:", query)
        results = self._vector_store.search(
            query_embedding=embedding,
        )
        return [
            result
            for result in results
        ]

    @staticmethod
    def _to_domain_result(
        payload: dict[str, Any],
        citations: tuple[Citation, ...],
        raw_response: str,
    ) -> GroundedRecommendation:

        findings = tuple(
            item["statement"]
            for item in payload.get("findings", [])
        )
        
        # print(f"Payload: \n{payload}")
        recommendations = tuple(
            (
                f"{item["priority"]}: {item['action']} "
                f"- {item['reason']}"
            )
            for item in payload.get("recommendations", [],)
        )
        # print(f"Recommendations: \n{recommendations}")
        

        limitations = tuple(
            item
            for item in payload.get("limitations", [])   
        )
        
        # print(f"Limitations: \n{limitations}")

        return GroundedRecommendation(
            summary=str(payload.get("summary", "")),
            risk_level=str(
                payload.get("risk_level", "unknown")
            ),
            findings=findings,
            recommendations=recommendations,
            limitations=limitations,
            citations=citations,
            raw_response=raw_response,
        )