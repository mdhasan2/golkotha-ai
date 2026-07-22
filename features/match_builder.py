class MatchBuilder:

    def build(self, home, away):

        return{
            # ------Attack--------
            "goals_diff": home["total_goals"]-away["total_goals"],
            "assists_diff": home["total_assists"]-away["total_assists"],
            # ------Creativity--------
            "key_passes_diff": home["total_key_passes"]-away["total_key_passes"],
            "pass_accuracy_diff": home["avg_pass_accuracy"]-away["avg_pass_accuracy"],
            # ------Overall--------
            "rating_diff": home["avg_rating"]-away["avg_rating"],
        }