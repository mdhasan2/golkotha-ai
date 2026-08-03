from dataclasses import dataclass

from domain.rag_models import GroundedRecommendation

@dataclass(frozen=True)
class RecommendationResult:
    recommendation: GroundedRecommendation
    interaction_id: str
    latency_ms: float