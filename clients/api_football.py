import requests

class APIFootballClient:
    BASE_URL = "https://v3.football.api-sports.io"

    def __init__(
        self,
        api_key,
        timeout=30,
        retries=3,      
    ):
        self.timeout = timeout
        self.retries = retries

        self.headers = {
            "x-apisports-key": api_key
        }
    
    def get():
        url = f"{self.BASE_URL}/{endpoint}"

        for attempt in range(self.retries):
            
            response = requests.get(
                url,
                headers=self.headers
            )