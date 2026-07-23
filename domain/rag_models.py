from dataclasses import dataclass

@dataclass(frozen=True)
class GroundedRecommendation:
    summary: str
    risk_level:str 

    findings: tuple[str, ...]
    recommendations: tuple[str, ...]
    limitations: tuple[str, ...]

    citations: tuple[Citation, ...]
    raw_response: str