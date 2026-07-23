from typing import Any
from application.ports.interfaces import ModelTrainerPort

import pandas as pd

class TrainModel:
    def __init__(self, trainer: ModelTrainerPort) -> None:
        self._trainer = trainer
    
    def execute(self, features: pd.DataFrame, labels: pd.Series,) -> Any:
        return self._trainer.train(features, labels)