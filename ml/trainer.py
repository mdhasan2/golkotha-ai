from xgboost import XGBClassifier
import joblib

class ModelTrainer:
    """
    """

    def train(self, X, y):

        model = XGBClassifier(
            random_state=42,
        )

        model.fit(X,y)

        joblib.dump(
            model,
            "models/xgboost.pkl"
        )

        return model

