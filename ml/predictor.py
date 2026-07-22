import joblib
import pandas as pd

class PredictionService:
    """
    """
    def __init__(self, model):
        self._model = model

    def probability(self, features):

        X = pd.DataFrame([features])

        probability = self._model.predict_proba(X)[0]

        return probability
    