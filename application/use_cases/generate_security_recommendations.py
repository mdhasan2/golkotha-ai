from typing import Any
from time import perf_counter

from application.mapper.prediction_context_mapper import PredictionContextMapper
from application.ports.embedding_port import EmbeddingPort
from application.ports.llm_port import LLMPort
from application.ports.vector_store_port import VectorStorePort

from domain.rag_models import (
    Citation,
    GroundedRecommendation,
    PredictionContext,
    RetrivedChunk,
)

from domain.security_models import SecurityAssessmentRequest

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
        predict_context_mapper: PredictionContextMapper,
    ) -> None:
        self._embedding_service = embedding_service
        self._vector_store = vector_store
        self._llm = llm
        self._query_builder = query_builder
        self._prompt_builder = prompt_builder
        self._citation_parser = citation_parser
        self._prediciton_context_mapper = predict_context_mapper

    def execute(
        self,
        # context: PredictionContext,
        request: SecurityAssessmentRequest,
        retrieval_limit: int = 8,
        minimum_score: float = 0.20,
    )-> GroundedRecommendation:

        context = self._prediciton_context_mapper.map(request)

        start_time = perf_counter()

        retrieved = self._retrieve(
            context=context,
            limit=retrieval_limit,
            minimum_score=minimum_score,
        )

        retrieval_latency_ms = (
            perf_counter() - start_time
        ) * 1000

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

        start_time = perf_counter()

        response = self._llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        raw_response = response.text
        input_tokens = response.input_tokens
        output_tokens = response.output_tokens
        provider = response.provider
        model_name = response.model_name

        llm_latency_ms = (
            perf_counter() - start_time
        ) * 1000

        # print(f"LLM raw Response: \n{raw_response}\n")

        payload, citations = self._citation_parser.parse(
            raw_response=raw_response,
            retrieved=retrieved,
        )

        return self._to_domain_result(
            payload=payload,
            citations=citations,
            raw_response=raw_response,
            retrieval_latency_ms=retrieval_latency_ms,
            llm_latency_ms=llm_latency_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            provider=provider,
            model_name=model_name,
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
        retrieval_latency_ms: float,
        llm_latency_ms: float,
        input_tokens: int,
        output_tokens: int,
        provider: str,
        model_name: str,
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

        # print(citations)

        # print(type(citations))

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
            retrieval_latency_ms=retrieval_latency_ms,
            llm_latency_ms=llm_latency_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            provider=provider,
            model_name=model_name,
        )