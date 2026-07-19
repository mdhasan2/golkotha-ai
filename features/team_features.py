import numpy as np

class TeamFeatures:

    def build(self, players):

        return {
            "total_goals": int(np.sum([p["goals"]for p in players])),
            "total_assists": int(np.sum([p["assists"]for p in players])),
            "total_shots": int(np.sum([p["shots"]for p in players])),
            "total_key_passes": int(np.sum([p["key_passes"]for p in players])),
            "avg_pass_accuracy": float(np.mean([p["pass_accuracy"]for p in players])),
            "avg_rating": float(np.mean([p["rating"]for p in players])),
        }