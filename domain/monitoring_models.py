from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any

from domain.rag_models import GroundedRecommendation

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

@dataclass(frozen=True)
class RAGInteraction:
    interaction_id: str
    user_query:str
    answer:str
    provider:str
    model_name:str
    retrieval_strategy:str
    prompt_strategy:str
    retrieved_document_ids: tuple[Any, ...]
    citation_ids: tuple[Any, ...]
    latency_ms: float
    retrieval_latency_ms: float
    llm_latency_ms: float
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    success: bool
    error_message: str | None = None
    created_at: datetime | None = None
    metadata: dict[str, str] | None = None

    @classmethod
    def create(
        cls,
        *,
        user_query: str,
        # answer: str,
        recommendation: GroundedRecommendation,
        retrieval_strategy: str,
        prompt_strategy: str,
        # retrieved_document_ids: tuple[str, ...],
        # citation_ids: tuple[str, ...],
        latency_ms: float,
        # retrieval_latency_ms: float,
        # llm_latency_ms: float,
        # input_tokens: int = 0,
        # output_tokens: int = 0,
        cost: float = 0.0,
        success: bool = True,
        error_message: str | None = None,
        created_at: datetime | None = None,
        metadata: dict[str, str] | None = None,
    ) -> "RAGInteraction":
        return cls(
            interaction_id=str(uuid4()),
            user_query=user_query,
            answer=recommendation.summary,
            provider=recommendation.provider,
            model_name=recommendation.model_name,
            retrieval_strategy=retrieval_strategy,
            prompt_strategy=prompt_strategy,
            retrieved_document_ids=tuple(
                citation.chunk_id.rsplit(":", maxsplit=2)[0]
                for citation in recommendation.citations
            ),
            citation_ids=tuple(
                citation.citation_id
                for citation in recommendation.citations
            ),
            latency_ms=latency_ms,  
            retrieval_latency_ms=recommendation.retrieval_latency_ms,
            llm_latency_ms=recommendation.llm_latency_ms,
            input_tokens=recommendation.input_tokens,
            output_tokens=recommendation.output_tokens,
            estimated_cost_usd=cost,
            success=success,
            error_message=error_message,
            created_at=created_at or utc_now(),
            metadata=metadata or {},
        )

@dataclass(frozen=True)
class UserFeedback:
    feedback_id: str
    interaction_id: str
    rating: int
    comment: str | None
    created_at: datetime

    @classmethod
    def create(
        cls,
        *,
        interaction_id: str,
        rating: int,
        comment: str | None = None,
    ) -> "UserFeedback":
        if rating not in (-1, 1):
            raise ValueError("Feedback rating must be -1 or 1.")

        return cls(
            feedback_id=str(uuid4()),
            interaction_id=interaction_id,
            rating=rating,
            comment=comment,
            created_at=utc_now(),
        )