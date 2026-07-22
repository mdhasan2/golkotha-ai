from typing import Any, Protocol

import pandas as pd

from domain.models import MatchFeatures, MatchPrediction

class ModelTrainerPort(Protocol):
    def train(self, features: pd.DataFrame, labels: pd.Series) -> Any:
        """
        Train and return a machine-learning model.
        """
        ...

class MatchPredictorPort(Protocol):
    def predict(self, fatures: MatchFeatures,) -> MatchPrediction:
        """
        Generate a domain prediction for one match.
        """
        ...