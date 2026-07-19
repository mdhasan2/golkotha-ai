class LeagueService:
    def __init__(self, client):
        self.client = client

    def search(self, name):
        return self.client.get(
            "leagues",
            search = name,
        )["response"]
        
    def world_cup(self):
         
         leagues = self.search("World Cup")
         
         return next(
            league
            for league in leagues
            if league["league"]["id"] == 1
        )
        

