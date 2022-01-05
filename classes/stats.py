class Stats:
    def __init__(self) -> None:
        self.stats = {
            "scored_max_turn": {
                "player": "",
                "value": 0
            },
            "max_loss_turn": {
                "player": "",
                "value": 0
            },
            "longest_turn": {
                "player": "",
                "value": 0
            },
            "scoring_turn": {
                "turns": 1,
                "score": 0
            },
            "non_scoring_turn": {
                "turns": 1,
                "score": 0
            }
        }
    
    def get_stats(self) -> dict:
        return self.stats

    def update_longest_turn(self, player, value) -> None:
        self.stats["longest_turn"] = {
            "player": player.get_name(),
            "value": value
        }
    
    def update_non_scoring_turn(self, score) -> None:
        self.stats["non_scoring_turn"]["turns"] += 1
        self.stats["non_scoring_turn"]["score"] += score

    def update_max_loss_turn(self, player, score) -> None:
        self.stats["max_loss_turn"] = {
            "player": player.get_name(),
            "value": score
        }

    def update_scored_max_turn(self, player, score) -> None:
        self.stats["scored_max_turn"] = {
            "player": player.get_name(),
            "value": score
        }

    def update_scoring_turn(self, score) -> None:
        self.stats["scoring_turn"]["turns"] += 1
        self.stats["scoring_turn"]["score"] += score

    def print_endgame_stats(self) -> None:
        print("\n")
        print(f"Max turn scoring : {self.stats['scored_max_turn']['player']} with {self.stats['scored_max_turn']['value']}")
        print(f"Longest turn : {self.stats['longest_turn']['player']} with {self.stats['longest_turn']['value']}")
        print(f"Max turn loss : {self.stats['max_loss_turn']['player']} with {self.stats['max_loss_turn']['value']}")
        print("\n")
        print(f"Mean scoring turn : {round(self.stats['scoring_turn']['score'] / self.stats['scoring_turn']['turns'], 2)} ({self.stats['scoring_turn']['turns']} turns)")
        print(f"Mean non scoring turn : {round(self.stats['non_scoring_turn']['score'] / self.stats['non_scoring_turn']['turns'], 2)} ({self.stats['non_scoring_turn']['turns']} turns)")     