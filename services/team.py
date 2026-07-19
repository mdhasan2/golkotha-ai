class TeamService:

    def __init__(self, client):
        self.client = client
    
    def list(self, league_id, season):
        return self.client.get("teams", league=league_id, season=season)["response"]
        
    def ids(self, league_id, season):
        return {
            team["team"]["name"]: team["team"]["id"]
            for team in self.list(league_id, season)
        }
    
    def by_name(self, name, league_id, season):

        teams = self.list(league_id, season)
        return next(
            team_name
            for team_name in teams
            if team_name["team"]["name"] == name
        )