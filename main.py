
from dotenv import load_dotenv
import os
import json
import pandas as pd
from api import SportsAPI
from enums import Sport
from features.player_forms import PlayerForms
from features.team_features import TeamFeatures
from features.match_features import MatchFeatures
from ml.dataset_builder import DatasetBuilder
from ml.predictor import PredictionService
from ml.trainer import ModelTrainer
from app.streamlit_app import StreamlitService


load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

def main(): 
    football = SportsAPI(API_KEY, Sport.FOOTBALL)
   
    player_forms = PlayerForms()
    team_features = TeamFeatures()
    match_features = MatchFeatures()
    
    
    #print(json.dumps(football.leages.world_cup(), indent=2))
    #print(json.dumps(football.teams.ids(1, 2026), indent=2))
    #print(json.dumps(football.teams.by_name('Argentina', 1, 2026), indent=2))
    #print(json.dumps(football.players.squad(ARGENTINA_ID), indent=2))
    

    league_id = football.leagues.world_cup()
    LEAGUE_ID = league_id["league"]["id"]
    SEASON = 2026

    argentina_id = football.teams.by_name('Argentina', LEAGUE_ID, SEASON)
    ARGENTINA_ID = argentina_id["team"]["id"]
    
    print(LEAGUE_ID, ARGENTINA_ID, SEASON)

    # Download squad
    players_ar = football.players.squad(ARGENTINA_ID)


    # Engineer player features
    player_forms_ar = []
  
    for player in players_ar:
        stats = football.players.statistics(player["id"], SEASON, LEAGUE_ID)
        player_forms_ar.append(player_forms.build(stats))

    # Aggregate team
    argentina = team_features.build(player_forms_ar)

    # Repeat for spain
    spain_id = football.teams.by_name('Spain', LEAGUE_ID, SEASON)
    SPAIN_ID = spain_id["team"]["id"]
    
    # Download squad
    players_sp = football.players.squad(SPAIN_ID)


    # Engineer player features
    player_forms_sp = []
  
    for player in players_sp:
        stats = football.players.statistics(player["id"], SEASON, LEAGUE_ID)
        player_forms_sp.append(player_forms.build(stats))

    # Aggregate team
    spain = team_features.build(player_forms_sp)

    # print(json.dumps(argentina , indent=2))
    # print(json.dumps(spain , indent=2))

    # Comapare teams
    match_features = match_features.build(argentina, spain)
    #print(json.dumps(match , indent=2))

    # Explore fixtures
    #fixtures_list = football.fixtures.list(LEAGUE_ID, SEASON)
    #print(json.dumps(fixtures_list, indent=2))
    #fixtures_by_name = football.fixtures.by_team(ARGENTINA_ID,SEASON)
    #print(json.dumps(fixtures_by_name, indent=2))

    # Build the dataset
    builder = DatasetBuilder(
        api=football,
        player_forms = PlayerForms(),
        team_features = TeamFeatures(),
        match_features = MatchFeatures(),
    )

    fixtures_by_league = football.fixtures.by_league(LEAGUE_ID, SEASON)

    #dataset = builder.build(fixtures_by_league)

    # dataset.to_csv(
    #     "data/worldcup_training.csv",
    #     index=False,
    # )

    dataset = pd.read_csv("data/worldcup_training.csv")

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

    trainer = ModelTrainer()

    model = trainer.train(X, y)

    # Predict
    predictor = PredictionService()

    app = StreamlitService(predictor)

    app.visualize(match_features)

    



if __name__ == "__main__":
    main()    