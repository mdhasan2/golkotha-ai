import joblib
import pandas as pd

class PredictionService:
    """
    """
    def __init__(self):
        self.model = joblib.load("models/xgboost.pkl")

    def probability(self, features):

        X = pd.DataFrame([features])

        probability = self.model.predict_proba(X)[0]

        print(probability)
        print(self.model.classes_)

        return probability
    