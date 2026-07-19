class PlayerForms:
    """
    """

    def build(self, statistics):

        return {
            "goals": statistics["goals"]["total"] or 0,
            "assists": statistics["goals"]["assists"] or 0,
            # "xg": statistics["expected_goals"]
            # "xa": statistics["expected_assists"],
            "shots": statistics["shots"]["total"] or 0,
            "key_passes": statistics["passes"]["key"] or 0,
            "pass_accuracy": statistics["passes"]["accuracy"] or 0,
            "rating": float(statistics["games"]["rating"] or 0),
        }