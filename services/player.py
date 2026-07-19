import json
class PlayerService:
    def __init__(self, client):
        self.client = client

    def squad(self, team_id):

        return self.client.get("players/squads", team=team_id,)["response"][0]["players"]
    
    def statistics(self, player_id, season, league_id):
        
        #players = self.client.get("players", id=player_id, season=season,)["response"][0]["statistics"]

        response = self.client.get("players", id=player_id, season=season, league=league_id)

        #print(json.dumps(response, indent=2))
        
        players = response["response"]

        if not players:
            print(f"No player found: id={player_id}, season={season}")
            return None
        
        statistics = players[0]["statistics"]

        if not statistics:
            print(f"No statistics: id={player_id}, season={season}")
            return None
        
        return statistics[0]