from dataclasses import dataclass

from domain.models import MatchFeatures, MatchPrediction

@dataclass(frozen=True)
class SecurityAssessmentRequest:
    model_name: str
    model_type: str
    model_version: str

    home_team:str
    away_team:str

    prediction: MatchPrediction
    features: MatchFeatures

    user_question: str