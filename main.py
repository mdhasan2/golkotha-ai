
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
from domain.rag_models import GroundedRecommendation

from application.mapper.prediction_context_mapper import PredictionContextMapper
from application.use_cases.generate_security_recommendations import GenerateSecurityRecommendations

from infrastructure.rag.security_prompt_builder import (
    SecurityPromptBuilder
)

from infrastructure.rag.security_query_builder import (
    SecurityQueryBuilder
)
from infrastructure.rag.sentence_transformer_embeddings import (
    SentenceTransformerEmbeddingService
)
from infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore
)

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

    # print(model)

    model = joblib.load("models/new_xgboost.pkl")

    prediction_container = build_prediction_container(model)

    # print(prediction_container)

    features = build_match_features(
        football_api,
        "Argentina",
        "Spain",
    )

    # print(features)

    # predictor = PredictionService(model)

    # app = StreamlitService(predictor)

    # app = StreamlitService(prediction_container.predict_match,)

    # print("Reached visualize")

    # app.visualize(features)

    prediction = prediction_container.predict_match.execute(features)
    
    # print(prediction)

    context = PredictionContextMapper().map(
            model_name="GolKotha XGBoost",
            model_type="XGBoostClassifier",
            model_version="1.0",
            home_team="Argentian",
            away_team="Spain",
            predicted_label=prediction.predicted_label,
            predicted_team="Argentina",
            confidence=prediction.probability_for(
                prediction.predicted_label
            ),
            class_probabilities={
                # "Draw": prediction.probability_for(0),
                "Spain": prediction.probability_for(0),
                "Argentina": prediction.probability_for(1),
                # "Spain": prediction.probability_for(2),
            },
            feature_values=features.to_dict(),
            user_question=(
                "What should I implement to make this model "
                "more secure and trustworthy?"
            ),
    )
    # print(context)
    query_builder = SecurityQueryBuilder()
    embeddings = SentenceTransformerEmbeddingService()
    prompt_builder = SecurityPromptBuilder()

    
    vector_store = ChromaVectorStore(
        persist_directory="knowledge/vector_store",
        collection_name="golkotha_ai_security"
    )

    

    _generate_security_recommendations=GenerateSecurityRecommendations(
        embedding_service=embeddings,
        vector_store=vector_store,
        query_builder=query_builder,
        prompt_builder=prompt_builder,
    )
    recommendations = (
        _generate_security_recommendations.execute(context)
    )

    

if __name__ == "__main__":
    main()    