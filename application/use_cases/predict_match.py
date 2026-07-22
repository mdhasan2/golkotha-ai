
from application.interfaces import MatchPredictorPort
from domain.models import MatchFeatures, MatchPrediction

class PredictMatch:
    def __init__(self, predictor: MatchPredictorPort) -> None:
        self._predictor = predictor

    def execute(self, features: MatchFeatures,) -> MatchPrediction:
        return self._predictor.predict(features)