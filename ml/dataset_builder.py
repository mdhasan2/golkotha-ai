import json
import pandas as pd


class DatasetBuilder:
    """
    """

    def __init__(self, api, player_forms, team_features, match_features,):
        self.api = api
        self.player_forms=player_forms
        self.team_features=team_features
        self.match_features=match_features

    def build(self, fixtures):
        """
        """

        dataset = []

        for fixture in fixtures:

            status = fixture["fixture"]["status"]["short"]

            if status not in ("FT", "AET", "PEN"):
                continue

            try: 
                row = self._build_match(fixture)
                if row is not None:
                    dataset.append(row)
            
            except Exception as ex:

                print(
                    f"Skipping fixture"
                    f"{fixture["fixture"]["id"]}: {ex}"
                )
        
        return pd.DataFrame(dataset)
    
    def _build_match(self, fixture):
        """
        """
        fixture_id = fixture["fixture"]["id"]

        home_team = fixture["teams"]["home"]["id"]
        away_team = fixture["teams"]["away"]["id"]

        # print(fixture_id, home_team, away_team, season)

        # Download squad

        home_players = self.api.players.squad(home_team)
        away_players = self.api.players.squad(away_team)

        # Engineer player features

        home_player_features = self._build_player_features(home_players, fixture)
        away_player_features = self._build_player_features(away_players, fixture)
        
        # Engineer team features
        
        home_team_features = self.team_features.build(home_player_features)
        away_team_features = self.team_features.build(away_player_features)

        # Engineer match featurs

        match_features = self.match_features.build(home_team_features, away_team_features,)

        # Winner

        winner = self._winner_label(fixture)

        if winner is None:
            return None


        # Final row

        match_features["fixture_id"] = fixture_id
        match_features["home_team"] = home_team
        match_features["away_team"] = away_team
        match_features["season"] = fixture["league"]["season"]
        match_features["target"] = winner

        print(json.dumps(match_features, indent=2))

        return match_features


    def _build_player_features(self, squad, fixture):
        """
        """
        players = []

        league_id = fixture["league"]["id"]
        season = fixture["league"]["season"]

        for player in squad:

            statistics = self.api.players.statistics(player["id"], season, league_id)

            if statistics is None:
                print(f"Skipping player {player["id"]}")
                continue

            features = self.player_forms.build(statistics)

            players.append(features)
        
        return players

    def _winner_label(self, fixture):
        """
        """
        goals_home = fixture["goals"]["home"]
        goals_away = fixture["goals"]["away"]

        print(
            fixture["fixture"]["id"],
            fixture["fixture"]["status"]["short"],
            fixture["goals"]
        )

        if goals_home is None or goals_away is None:
            return None
        
        if goals_home > goals_away:
        
            return 1

        if goals_home < goals_away:
            return 0
        
        return None