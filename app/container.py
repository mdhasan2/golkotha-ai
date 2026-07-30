
from dataclasses import dataclass
from typing import Any

from application.ports.llm_port import LLMPort

from application.use_cases.generate_security_recommendations import (
    GenerateSecurityRecommendations,
)
from application.use_cases.predict_match import PredictMatch
from application.use_cases.train_model import TrainModel


from infrastructure.ml.xgboost_trainer import XGBoostTrainer
from infrastructure.ml.xgboost_predictor import XGBoostPredictor
from infrastructure.llm.llm_factory import build_llm


@dataclass(frozen=True)
class TrainingContainer:
    train_model: TrainModel

@dataclass(frozen=True)
class PredictionContainer:
    predict_match: PredictMatch

@dataclass(frozen=True)
class LLMContainer:
    llm: LLMPort

@dataclass(frozen=True)
class AdvisorContainer:
    generate_security_recommendations: (
        GenerateSecurityRecommendations
    )

def build_training_container() -> TrainingContainer:
    trainer = XGBoostTrainer()

    return TrainingContainer(
        train_model=TrainModel(trainer),
    )

def build_prediction_container(
    model: Any,
) -> PredictionContainer:
    predictor = XGBoostPredictor(model)

    return PredictionContainer(
        predict_match=PredictMatch(
            predictor=predictor
        ),
    )

def build_llm_container() -> LLMContainer:
    llm = build_llm()

    return LLMContainer(
        llm=llm
    )

def build_advisor_container() -> AdvisorContainer:
    print("You are here")
