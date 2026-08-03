
from pathlib import Path
from typing import Any

import joblib
import os
import pandas as pd
import streamlit as st

from app.container import(
    AdvisorContainer,
    PredictionContainer,
    build_advisor_container,
    build_prediction_container,
    build_training_container,
)

from api import SportsAPI
from enums import Sport

from dotenv import load_dotenv

from features.player_forms import PlayerForms
from features.team_features import TeamFeatures
from features.match_builder import MatchBuilder
from ml.dataset_builder import DatasetBuilder
from ml.predictor import PredictionService
from ml.trainer import ModelTrainer
from presentation.streamlit_app import StreamlitService

from domain.models import MatchFeatures
from domain.rag_models import GroundedRecommendation
from domain.security_models import SecurityAssessmentRequest

from application.mapper.prediction_context_mapper import PredictionContextMapper
from application.use_cases.generate_security_recommendations import GenerateSecurityRecommendations

from infrastructure.rag.monitored_recommendation_service import (
    MonitoringRepositoryPort,
)

load_dotenv()

# API_KEY = os.getenv("API_FOOTBALL_KEY")
SEASON = 2026
MODEL_PATH = Path(
    "models/new_xgboost.pkl"
)

def load_fixture_data(api: SportsAPI):
    """
    Keep the existing API or cached-data loading logic here.
    """
    
    league = api.leagues.world_cup()
    LEAGUE_ID = league["league"]["id"]

    return api.fixtures.by_league(LEAGUE_ID, SEASON)

def build_dataset(api: SportsAPI) -> pd.DataFrame:
    
    fixtures = load_fixture_data(api)
    
    builder = DatasetBuilder(
        api=api,
        player_forms = PlayerForms(),
        team_features = TeamFeatures(),
        match_features = MatchBuilder(),
    )

    dataset = builder.build(fixtures)

    dataset.to_csv(
        "data/worldcup_training.csv",
        index=False,
    )

    return dataset

def build_match_features(
        api: SportsAPI,
        home_team: str,
        away_team: str,
    ):

    league = api.leagues.world_cup()
    league_id = league["league"]["id"]    

    player_builder = PlayerForms()
    team_builder = TeamFeatures()
    match_builder = MatchBuilder()

    def build_team(team_name):

        team = api.teams.by_name(team_name, league_id, SEASON)
        team_id = team["team"]["id"]

        # Download squad
        squad = api.players.squad(team_id)

        # Engineer player features
        player_featurs = []
    
        for player in squad:
            stats = api.players.statistics(player["id"], SEASON, league_id)
            player_featurs.append(player_builder.build(stats))

        return team_builder.build(player_featurs)
        

    home = build_team(home_team)
    away = build_team(away_team)

    features = match_builder.build(home, away)
    # print(type(features))
    # print(features)
    

    return MatchFeatures.from_dict(features)

def train_model(dataset: pd.DataFrame):
    dataset = dataset.dropna(subset=["target"])

    # Remove non-feature columns
    X = dataset.drop(
        columns=[
            "fixture_id",
            "season",
            "home_team",
            "away_team",
            "target",
        ]
    )

    y = dataset["target"].astype(int)

    training_container = build_training_container()

    return training_container.train_model.execute(X, y,)

@st.cache_resource
def load_model() -> Any:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)

@st.cache_resource
def build_cached_prediction_container (
    _model: Any,
) -> PredictionContainer:
    return build_prediction_container(_model)

@st.cache_resource
def build_cached_advisor_container(
) -> AdvisorContainer:
    return build_advisor_container()

@st.cache_resource
def build_sports_api() -> SportsAPI:
    api_key = os.getenv("API_FOOTBALL_KEY")

    if not api_key:
        raise RuntimeError(
            "API_FOOTBALL_KEY is not configured."
        )
    return SportsAPI(api_key, Sport.FOOTBALL)

def main() -> None:

    # football_api = SportsAPI(API_KEY, Sport.FOOTBALL)
    
    model = load_model()
    football_api = build_sports_api()

    prediction_container = (
        build_cached_prediction_container(model)
    )

    advisor_container = (
        build_cached_advisor_container()
    )

    # features = build_match_features(
    #     football_api,
    #     "Argentina",
    #     "Spain",
    # )

    # print(features)

    # app = StreamlitService(prediction_container.predict_match,)

    app = StreamlitService(
        football_api=football_api,
        prediction_container=prediction_container,
        advisor_container=advisor_container,
    )



    # app.visualize(features)

    # prediction = prediction_container.predict_match.execute(features)
    
    # request = SecurityAssessmentRequest(
    #         model_name="GolKotha XGBoost",
    #         model_type="XGBoostClassifier",
    #         model_version="1.0",

    #         home_team="Argentian",
    #         away_team="Spain",

    #         # predicted_label=prediction.predicted_label,
    #         # predicted_team="Argentina",
    #         # confidence=prediction.probability_for(
    #         #     prediction.predicted_label
    #         # ),
    #         # class_probabilities={
    #         #     # "Draw": prediction.probability_for(0),
    #         #     "Spain": prediction.probability_for(0),
    #         #     "Argentina": prediction.probability_for(1),
    #         #     # "Spain": prediction.probability_for(2),
    #         # },
    #         # feature_values=features.to_dict(),

    #         prediction=prediction,
    #         features=features,

    #         user_question=(
    #             "What should I implement to make this model "
    #             "more secure and trustworthy?"
    #         ),
    # )

    # recommendations = (
    #     # advisor_container.generate_security_recommendations.execute(context)
    #     advisor_container.generate_security_recommendations.execute(
    #         request=request
    #     )
    # )

    # print(recommendations)

    # app.display_security_recommendations(recommendations)

    app.run()

    # recommendations_use_case=advisor_container.generate_security_recommendations

    # monitored_recommendations = (
    #     MonitoringRepositoryPort(
    #         recommendations_use_case,
    #     )
    # )

    # recommendations = monitored_recommendations.execute(
    #     context=request
    # )

    

if __name__ == "__main__":
    main()    