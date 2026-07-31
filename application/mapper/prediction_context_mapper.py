from collections.abc import Mapping

from domain.security_models import SecurityAssessmentRequest
from domain.rag_models import PredictionContext

class PredictionContextMapper:

    def map(
        self,
        # *,
        # model_name: str,
        # model_type: str,
        # model_version: str | None,
        # home_team: str,
        # away_team: str,
        # predicted_label: int,
        # predicted_team: str,
        # confidence: float,
        # class_probabilities: Mapping[str, float],
        # feature_values: Mapping[str, float],

        # user_question: str | None = None,

        request: SecurityAssessmentRequest 

    ) -> PredictionContext:

        prediction = request.prediction
        features = request.features

        confidence = prediction.probability_for(
            prediction.predicted_label
        )

        predicted_team = (
            request.home_team
            if prediction.predicted_label == 1
            else request.away_team
        )

        class_probabilities = {
            request.away_team: prediction.probability_for(0),
            request.home_team: prediction.probability_for(1),
        }

        feature_values = features.to_dict()

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "Prediction confidence must be between 0 and 1."
            )
        
        return PredictionContext(
            model_name=request.model_name,
            model_type=request.model_type,
            model_version=request.model_version,

            home_team=request.home_team,
            away_team=request.away_team,

            predicted_label=prediction.predicted_label,
            predicted_team=predicted_team,

            confidence=confidence,

            class_probabilities=dict(class_probabilities),

            feature_values=feature_values,

            user_question=request.user_question,
            metadata={
                "analysis_stage": "baseline-mdoel",
                "explainability_available": False,
                "adversarial_testing_available": False,
            },
        )