
from dataclasses import dataclass
from typing import Any

from application.use_cases.train_model import TrainModel
from application.use_cases.predict_match import PredictMatch
from infrastructure.ml.xgboost_trainer import XGBoostTrainer
from infrastructure.ml.xgboost_predictor import XGBoostPredictor

@dataclass(frozen=True)
class TrainingContainer:
    train_model: TrainModel

@dataclass(frozen=True)
class PredictionContainer:
    predict_match: PredictMatch

def build_training_container() -> TrainingContainer:
    trainer = XGBoostTrainer()

    return TrainingContainer(
        train_model=TrainModel(trainer),
    )

def build_prediction_container(model: Any,) -> PredictionContainer:
    predictor = XGBoostPredictor(model)

    return PredictionContainer(
        predict_match=PredictMatch(predictor),
    )