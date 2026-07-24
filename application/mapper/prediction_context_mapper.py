from collections.abc import Mapping

from domain.rag_models import PredictionContext

class PredictionContextMapper:

    def map(
        self,
        *,
        model_name: str,
        model_type: str,
        model_version: str | None,
        home_team: str,
        away_team: str,
        predicted_label: int,
        predicted_team: str,
        confidence: float,
        class_probabilities: Mapping[str, float],
        feature_values: Mapping[str, float],
        user_question: str | None = None,
    ) -> PredictionContext:
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "Prediction confidence must be between 0 and 1."
            )
        
        return PredictionContext(
            model_name=model_name,
            model_type=model_type,
            model_version=model_version,
            home_team=home_team,
            away_team=away_team,
            predicted_label=predicted_label,
            predicted_team=predicted_team,
            confidence=confidence,
            class_probabilities=dict(class_probabilities),
            feature_values=dict(feature_values),
            user_question=user_question,
            metadata={
                "analysis_stage": "baseline-mdoel",
                "explainability_available": False,
                "adversarial_testing_available": False,
            },
        )