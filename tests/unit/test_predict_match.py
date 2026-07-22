from domain.models import (
    MatchFeatures,
    MatchPrediction,
    PredictionProbability,
)

from application.use_cases.predict_match import PredictMatch

class FakePredictor:
    def predict(self, features: MatchFeatures,) -> MatchPrediction:
        return MatchPrediction(
            probabilities=(
                PredictionProbability(
                label=0,
                probability=0.4,
            ),
            PredictionProbability(
                label=1,
                probability=0.6,
            ),
        ),
        predicted_label=1,
    )

def test_predict_match_delegates_to_predictor() -> None:
    use_case = PredictMatch(FakePredictor())

    result = use_case.execute(
        MatchFeatures.from_dict(
            {
                "feature_a": 1.0,
            }
        )
    )

    assert result.predicted_label == 1
    assert result.probability_for(1) == 0.6