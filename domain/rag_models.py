from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True)
class KnowledgeDocument:
    """
    One normalized source document before chunking.
    """

    document_id: str
    title: str
    text: str
    source_name: str
    source_url: str
    version: str | None = None
    published_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class PredictionContext:
    """
    Information currently available from the base ML workflow.

    Later phaes can extend this context with SHAP summaries and adversarial-attack results.
    """

    model_name: str
    model_type: str
    model_version: str | None
    
    home_team: str
    away_team: str

    predicted_label: int
    predicted_team: str
    confidence: float

    class_probabilities: Mapping[str, float]

    feature_values: Mapping[str, float]

    user_question: str | None = None

    metadata: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    document_id: str

    text: str
    title: str

    source_name: str
    source_url: str
    
    chunk_index: int

    metadata: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class RetrivedChunk:
    chunk: DocumentChunk
    score: float

@dataclass(frozen=True)
class Citation:
    citation_id: str
    title: str
    source_name: str
    source_url: str
    chunk_id: str

@dataclass(frozen=True)
class GroundedRecommendation:
    summary: str
    risk_level:str 

    findings: tuple[str, ...]
    recommendations: tuple[str, ...]
    limitations: tuple[str, ...]

    citations: tuple[Citation, ...]
    raw_response: str