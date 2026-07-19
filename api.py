from clients.api_sports import APISportsClient
from services.league import LeagueService
from services.team  import TeamService
from services.player import PlayerService
from services.fixture import FixtureService
from enums import Sport

class SportsAPI:
    """
    """
    
    def __init__(self, api_key, sport: Sport):
        client = APISportsClient(api_key=api_key, base_url=sport.value)

        self.leagues = LeagueService(client)
        self.teams = TeamService(client)
        self.players = PlayerService(client)
        self.fixtures = FixtureService(client)
        

        