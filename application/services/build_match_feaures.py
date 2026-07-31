

from api import SportsAPI
from domain.models import MatchFeatures
from features.player_forms import PlayerForms
from features.team_features import TeamFeatures
from features.match_builder import MatchBuilder

SEASON = 2026

def build_match_features(
        api: SportsAPI,
        home_team: str,
        away_team: str,
    ) -> MatchFeatures:
    """
    Download player statistics and build match-level features
    for the selected home and away teams.
    """

    league = api.leagues.world_cup()
    league_id = league["league"]["id"]    

    player_builder = PlayerForms()
    team_builder = TeamFeatures()
    match_builder = MatchBuilder()

    def build_team(team_name: str):

        team = api.teams.by_name(
            team_name,
            league_id,
            SEASON,
        )
        
        team_id = team["team"]["id"]

        # Download squad
        squad = api.players.squad(team_id)

        # Engineer player features
        player_features = []
    
        for player in squad:
            player_id = player["id"] 
            statistics = api.players.statistics(
                player_id,
                SEASON,
                league_id,
            )

            player_features.append(
                player_builder.build(statistics))

        return team_builder.build(player_features)
        

    home_features = build_team(home_team)
    away_features = build_team(away_team)

    feature_values = match_builder.build(
        home_features,
        away_features,
    )

    return MatchFeatures.from_dict(feature_values)

