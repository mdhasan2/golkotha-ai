
import os
import pandas as pd
import joblib

from app.container import(
    build_training_container,
    build_prediction_container,
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



load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
SEASON = 2026

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
    print(type(features))
    print(features)
    

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

    # trainer = ModelTrainer()

    training_container = build_training_container()

    return training_container.train_model.execute(X, y,)


def main() -> None:

    football_api = SportsAPI(API_KEY, Sport.FOOTBALL)
    
    # dataset = build_dataset(football_api)

    # dataset.to_csv(
    #     "data/worldcup_training.csv",
    #     index=False,
    # )

    dataset = pd.read_csv("data/worldcup_training.csv")

    model = train_model(dataset)

    print(model)

    model = joblib.load("models/new_xgboost.pkl")

    prediction_container = build_prediction_container(model)

    print(prediction_container)

    features = build_match_features(
        football_api,
        "Argentina",
        "Spain",
    )

    print(features)

    # predictor = PredictionService(model)

    # app = StreamlitService(predictor)

    app = StreamlitService(prediction_container.predict_match,)

    # print("Reached visualize")

    app.visualize(features)

if __name__ == "__main__":
    main()    