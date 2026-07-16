import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("SPORTMONKS_API_TOKEN")

BASE_URL = "https://api.sportmonks.com/v3/football"

session = requests.Session()
session.params = {
    "api_token": API_TOKEN
}


def get(endpoint, **params):
    response = session.get(
        f"{BASE_URL}/{endpoint}",
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

WORLD_CUP_ID = 1234

fixtures = get(
    "fixtures",
    filters=f"leagueId:{WORLD_CUP_ID}"
)

print(fixtures)