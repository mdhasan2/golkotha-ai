class FixtureService:

    def __init__(self, client):
        self.client = client

    def by_league(self, league_id, season,):
        return self.client.get("fixtures", league=league_id, season=season)["response"]
    
    def by_team(self, team_id, season):
        return self.client.get("fixtures", team=team_id, season=season,)["response"]
    