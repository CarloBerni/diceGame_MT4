class Scoreboard:
    def init_scoreboard(self, players) -> None:
        scoreboard = {}
        for player in players:
            scoreboard[player.get_name()] = {
                "score": 0,
                "bonus": 0,
                "lost_score": 0,
                "rolls": 0,
                "full_roll": 0,
                "max_potential_lost": 0,
                "rank": 0,
            }
        return scoreboard
    
    def __init__(self, players) -> None:
        self.scoreboard = self.init_scoreboard(players)

    def get_scoreboard(self) -> dict:
        return self.scoreboard
    
    def get_sorted_scoreboard(self) -> dict:
        sorted_dict_keys = sorted(self.scoreboard, key=lambda x: (self.scoreboard[x]['score']), reverse=True)
        for player in self.scoreboard:
            self.scoreboard[player]['rank'] = sorted_dict_keys.index(player) + 1

        return {x:self.scoreboard[x] for x in sorted_dict_keys}
    
    def print_total_score(self) -> None:
        sorted_scoreboard = self.get_sorted_scoreboard()
        total_score = "Total score: "
        for player in sorted_scoreboard:
            current_player_score = sorted_scoreboard[player]['score']
            total_score += f"{player}--> {current_player_score}, "
        print(total_score + "\n")
    
    def get_player_scoreboard(self, player) -> dict:
        return self.scoreboard[player.get_name()]
    
    def update_player_scoreboard(self, player, scoreboard) -> None:
        self.scoreboard[player.get_name()] = scoreboard