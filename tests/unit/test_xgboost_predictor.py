import pytest
import numpy as np


from domain.models import MatchFeatures
from infrastructure.ml.xgboost_predictor import XGBoostPredictor

class FakeModel:
    classes_ = np.array([0, 1])

    def predict_proba(self, features):
        return np.array([[0.35, 0.65]], dtype=np.float32)


def test_predictor_returns_native_float_probabilities() -> None:
    predictor = XGBoostPredictor(FakeModel())

    result = predictor.predict(
        MatchFeatures.from_dict(
            {
                "home_form": 4.0,
                "away_form": 3.0,
            }
        ) 
    )

    assert result.predicted_label == 1
    assert result.probability_for(0) == pytest.approx(0.35)
    assert result.probability_for(1) == pytest.approx(0.65)
    assert isinstance(result.probability_for(1), float)