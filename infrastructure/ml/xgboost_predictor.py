from typing import Any

import numpy as np
import pandas as pd

from domain.models import (
    MatchFeatures,
    MatchPrediction,
    PredictionProbability,
)

class XGBoostPredictor:
    """
    """
    def __init__(self, model: Any):
        self._model = model

    def predict(self, features: MatchFeatures,) -> MatchPrediction:
        print(type(features))
        print(features)
        input_frame = pd.DataFrame([features.to_dict()])

        raw_probabilities = self._model.predict_proba(input_frame)
    
        classes = self._model.classes_
    
        probability_row = self._extract_probability_row(raw_probabilities)
    
        if len(classes) != len(probability_row):
            raise ValueError(
                "The model class count does not match "
            )
        
        probabilities = tuple(
            PredictionProbability(
                label=int(label),
                probability=float(probability)
            )
            for label, probability in zip(
                classes,
                probability_row,
                strict=True,
            )
        )

        predicted_index = int(np.argmax(probability_row))
        predicted_label = int(classes[predicted_index])

        return MatchPrediction(
            probabilities=probabilities,
            predicted_label=predicted_label,
        )

    # def probability(self, features: dict[str, float],) -> list[float]:
        
    #     """
    #     Temporary compatibiltiy method for the existing Streamlit UI.

    #     Remove after the UI has migrated to MarchPrediction.
    #     """

    #     domain_features = MatchFeatures.from_dict(features)
    #     prediction = self.predict(domain_features)

    #     return [
    #         item.probability
    #         for item in prediction.probabilities
    #     ]
    
    @staticmethod
    def _extract_probability_row(raw_probabilities: Any,) -> np.ndarray:
        probability_array = np.asarray(raw_probabilities)

        if probability_array.ndim != 2:
            raise ValueError(
                "Expected predict_proba() to return a two-dimensional array."
            )
    
        if probability_array.shape[0] != 1:
            raise ValueError(
                "Expected exactly one prediction row."
            )
        
        return probability_array[0] 