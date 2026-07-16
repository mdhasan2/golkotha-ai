import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

url = "https://v3.football.api-sports.io/leagues?id=1&season=2026"

payload={}
headers = {
  'x-apisports-key': API_KEY,
}

response = requests.request("GET", url, headers=headers, data=payload)

# Fixtures

#response = requests.request("GET", url, headers=headers, params= { "league":1, "season": 2026}, data=payload)

print(response.text)
