#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

-
# In[ ]:


# Find the FIFA World Cup league ID

import requests
import os

headers = {
    "x-apisports-key": os.environ["API_FOOTBALL_KEY"]
}

response = requests.get(
    "https://v3.football.api-sports.io/leagues",
    headers=headers,
    params={"search": "World Cup"},
)

response.raise_for_status()

for league in response.json()["response"]:
    print(
        league["league"]["id"],
        league["league"]["name"],
        league["country"]["name"],
    )


# In[14]:


# Find all the team ids

BASE_URL = "https://v3.football.api-sports.io"

response = requests.get(
    f"{BASE_URL}/teams",
    headers=headers,
    params={
        "league": 1,      # FIFA World Cup
        "season": 2026,
    },
    timeout=30,
)

response.raise_for_status()

data = response.json()

print(f"Found {data['results']} teams\n")

for item in sorted(data["response"], key=lambda x: x["team"]["name"]):
    team = item["team"]

    print(
        f"{team['id']:>4} | "
        f"{team['name']:<25} | "
        f"{team['country']}"
    )


# In[15]:


# Find the team ID for Argentian and Spain
team_ids = {
    team["team"]["name"]: team["team"]["id"]
    for team in data["response"]
}

print(team_ids["Argentina"])
print(team_ids["Spain"])


# In[17]:


# Get Argentina's squad

TEAM_ID = team_ids["Argentina"]  # Replace with the ID returned above


response = requests.get(
    "https://v3.football.api-sports.io/players/squads",
    headers=headers,
    params={
        "team": TEAM_ID,
    },
)

response.raise_for_status()

data = response.json()

for squad in data["response"]:
    print(f"\n{squad['team']['name']}")
    print("-" * 40)

    for player in squad["players"]:
        print(
            f"{player['id']:>5} | "
            f"{player['name']:<30} | "
            f"{player['position']}"
        )


# In[19]:


# get Lionel Messi's player statistics

MESSI_PLAYER_ID = 154 

response = requests.get(
    "https://v3.football.api-sports.io/players",
    headers=headers,
    params={
        "id": MESSI_PLAYER_ID,
        "season": 2026,
    },
)

response.raise_for_status()

data = response.json()

for player in data["response"]:
    p = player["player"]
    stats = player["statistics"][0]

    print("=" * 60)
    print(f"Name       : {p['name']}")
    print(f"Player ID  : {p['id']}")
    print(f"Nationality: {p['nationality']}")
    print(f"Age        : {p['age']}")
    print(f"Team       : {stats['team']['name']}")
    print(f"Position   : {stats['games']['position']}")
    print(f"Appearances: {stats['games']['appearences']}")
    print(f"Minutes    : {stats['games']['minutes']}")
    print(f"Rating     : {stats['games']['rating']}")
    print(f"Goals      : {stats['goals']['total']}")
    print(f"Assists    : {stats['goals']['assists']}")
    print(f"Shots      : {stats['shots']['total']}")
    print(f"Shots OT   : {stats['shots']['on']}")
    print(f"Passes     : {stats['passes']['total']}")
    print(f"Key Passes : {stats['passes']['key']}")
    print(f"Pass %     : {stats['passes']['accuracy']}")

