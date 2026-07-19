import time
import requests

class APISportsClient:
    #BASE_URL = "https://v3.football.api-sports.io"

    def __init__( self, api_key, base_url, timeout=30, retries=3):
        self.timeout = timeout
        self.retries = retries
        self.base_url = base_url

        self.headers = {
            "x-apisports-key": api_key
        }
    
    def get(self, endpoint: str, **params):
        url = f"{self.base_url}/{endpoint}"

        for attempt in range(self.retries):
            
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
            
            except requests.RequestException:

                if attempt == self.retries-1:
                    raise
                time.sleep(2 ** attempt) 