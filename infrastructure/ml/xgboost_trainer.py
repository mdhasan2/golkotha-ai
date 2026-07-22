import joblib
import pandas as pd

from xgboost import XGBClassifier




class XGBoostTrainer:
    """
    Infrastructure implementation of the model trainer interface.
    """

    def train(self, features: pd.DataFrame,labels: pd.Series,) -> XGBClassifier:
        model = XGBClassifier()
        model.fit(features, labels)

        joblib.dump(
            model,
            "models/new_xgboost.pkl"
        )

        return model

