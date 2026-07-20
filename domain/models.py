from __future__ import annotations
from enum import IntEnum
from dataclasses import dataclass
from typing import Any, Mapping

class MatchOutcome(IntEnum):
    """
    Preserve the numericv labels already used by the model.
    """
    AWAY_WIN = 0
    HOME_WIN = 1
    DRAW = 2 # Are we using this?

@dataclass(frozen=True)
class Team:
    id: int
    name: str

@dataclass(frozen=True)
class Match:
    fixture_id: int
    home_team: Team
    away_team: Team
    home_goals: int | None = None
    away_goals: int | None = None
    status: str | None = None

@dataclass(frozen=True)
class MatchFeatures:
    """
    A domain representation of on model inptut row.

    The internal mapping preserves compatibility with existing pandas
    DataFrame and XGBoost workflow.
    """
    values: Mapping[str, float]

    def to_dict(self) -> dict[str, float]:
        return dict(self.values)

    @classmethod
    def from_dict(cls, values: Mapping[str, Any]) -> MatchFeatures:
        converted: dict[str, float] = {}

        for feature_name, value in values.items():
            if value is None:
                raise ValueError(
                    f"Feature '{feature_name}' cannot be None."
                )
            
            converted[feature_name] = float(value)

        return cls(values=converted)

@dataclass(frozen=True)
class PredictionProbability:
    label: int
    probability: float

@dataclass(frozen=True)
class MatchPrediction:
    probabilities: tuple[PredictionProbability, ...]
    predicted_label: int

    def probability_for(self, label: int) -> float:
        for prediction in self.probabilities:
            if prediction.label == label:
                return prediction.probability

        raise KeyError(f"Prediction does not contain label {label}.")



data = {
    "shots": 12,
    "possession": 58.5,
    "passes": 421.0
}

# features = MatchFeatures(data)
# features.to_dict()
# print(features)
# checked_features = features.from_dict(data)
# print(checked_features)
proba1 = PredictionProbability(1, 78)
proba2 = PredictionProbability(0, 25)

prediction = MatchPrediction(
    probabilities=(proba1, proba2),
    predicted_label=1,
)

print(prediction.probability_for(3))
