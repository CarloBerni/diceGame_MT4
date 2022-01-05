import random
from typing import Tuple
from constants import *
from classes.scoreboard import Scoreboard
from classes.turn import Turn
from classes.stats import Stats

class Game:
    def __init__(self, players) -> None:
        self.players = players
        self.scoreboard = Scoreboard(players)
        self.current_turn = Turn(0)
        self.stats = Stats()
        self.is_finished = False

    def analyse_dices_to_roll(self, nb_dices_rolled, dice_value_occurence_list) -> int:
        return nb_dices_rolled - (nb_dices_rolled - sum(dice_value_occurence_list))

    def roll_dice_set(self, nb_dice_to_roll) -> list:
        dice_value_occurrence_list = [0] * NB_DICE_SIDE
        for n in range(nb_dice_to_roll):
            dice_value = random.randint(1, NB_DICE_SIDE)
            dice_value_occurrence_list[dice_value - 1] += 1

        return dice_value_occurrence_list

    def get_formatted_winning_occurences(self, occurences) -> list:
        formatted_winning_occurences = []
        for indexOcc, occValue in enumerate(occurences):
            if occValue >= THRESHOLD_BONUS:
                formatted_winning_occurences.append([occValue, indexOcc + 1])

            elif indexOcc + 1 in SCORING_DICE_VALUE_LIST and occValue > 0:
                formatted_winning_occurences.append([occValue, indexOcc + 1])
            

        return formatted_winning_occurences 

    def analyse_bonus_score(self, dice_value_occurrence_list) -> Tuple[int, list, int]:
        score = 0
        times_bonus = 0
        for side_value_index, dice_value_occurrence in enumerate(dice_value_occurrence_list):
            nb_of_bonus = dice_value_occurrence // THRESHOLD_BONUS
            if nb_of_bonus > 0:
                if side_value_index == 0:
                    bonus_multiplier = ACE_BONUS_MULTIPLIER
                else:
                    bonus_multiplier = STD_BONUS_MULTIPLIER
                score += nb_of_bonus * bonus_multiplier * (side_value_index + 1)
                dice_value_occurrence_list[side_value_index] %= THRESHOLD_BONUS
                times_bonus += 1

        return score, dice_value_occurrence_list, times_bonus


    def analyse_standard_score(self, dice_value_occurrence_list) -> Tuple[int, list]:
        score = 0
        for scoring_value, scoring_multiplier in zip(SCORING_DICE_VALUE_LIST, SCORING_MULTIPLIER_LIST):
            score += dice_value_occurrence_list[scoring_value - 1] * scoring_multiplier
            dice_value_occurrence_list[scoring_value - 1] = 0

        return score, dice_value_occurrence_list

    def analyse_score(self, dice_value_occurrence_list) -> Tuple[int, int]:
        bonus_score, dice_value_occurrence_list, times_bonus = self.analyse_bonus_score(dice_value_occurrence_list)
        standard_score, dice_value_occurrence_list = self.analyse_standard_score(dice_value_occurrence_list)

        return bonus_score + standard_score, times_bonus
    
    def start(self) -> None:
        while not self.is_finished:
            self.current_turn.increment_turn_number()
            for player in self.players:
                current_player_scoreboard = self.scoreboard.get_player_scoreboard(player)
                current_stats = self.stats.get_stats()
                self.scoreboard.print_total_score()

                print(f"turn#{self.current_turn.get_turn_number()}-->{player.get_name()} rank #{current_player_scoreboard['rank']}, score {current_player_scoreboard['score']}")
                remaining_dices = DEFAULT_DICES_NB
                reroll = "y"
                current_roll = 0
                potential_turn_score = 0
                is_looser = False

                while remaining_dices > 0 and reroll == "y":
                    if potential_turn_score > current_player_scoreboard['max_potential_lost']:
                        current_player_scoreboard['max_potential_lost'] = potential_turn_score
                    
                    current_roll += 1
                    current_player_scoreboard['rolls'] += 1

                    dices_occurences = self.roll_dice_set(remaining_dices)
                    formatted_winning_occurences = self.get_formatted_winning_occurences(dices_occurences)
                    previous_remaining_dices = remaining_dices
                    potential_roll_score, times_bonus = self.analyse_score(dices_occurences)
                    remaining_dices = self.analyse_dices_to_roll(remaining_dices, dices_occurences)
                    potential_turn_score += potential_roll_score

                    print(f"roll #{current_roll} : {previous_remaining_dices - remaining_dices} scoring dices {str(formatted_winning_occurences)} scoring {potential_roll_score}, potential total turn score {potential_turn_score}, remaining dice to roll : {remaining_dices}")

                    if remaining_dices == 0 and potential_roll_score > 0:
                        current_player_scoreboard['full_roll'] += 1
                        remaining_dices = DEFAULT_DICES_NB

                    if current_roll > current_stats["longest_turn"]["value"]:
                        self.stats.update_longest_turn(player, current_roll)

                    current_player_scoreboard['bonus'] += times_bonus

                    if potential_roll_score == 0:
                        self.scoreboard.update_player_scoreboard(player, current_player_scoreboard)
                        is_looser = True
                        break
                    elif remaining_dices > 0:
                        reroll = input(f"Do you want to reroll {remaining_dices} dices ? [y/n]")

                if is_looser:
                    print(f"you lose this turn and a potential to score {potential_turn_score} pts\n")
                    current_player_scoreboard["lost_score"] += potential_turn_score
                    self.stats.update_non_scoring_turn(potential_turn_score)
                    if potential_turn_score > self.stats.get_stats()["max_loss_turn"]["value"]:
                        self.stats.update_max_loss_turn(player, potential_turn_score)
                else:
                    print(f"you win this turn, scoring {potential_turn_score} pts\n")
                    current_player_scoreboard["score"] += potential_turn_score
                    self.stats.update_scoring_turn(potential_turn_score)
                    if potential_turn_score > self.stats.get_stats()["scored_max_turn"]["value"]:
                        self.stats.update_scored_max_turn(player, potential_turn_score)
                
                self.scoreboard.update_player_scoreboard(player, current_player_scoreboard)
                    
                if current_player_scoreboard["score"] >= DEFAULT_TARGET_SCORE:
                    print(f"Game in {self.current_turn.get_turn_number()} turns")
                    sorted_scoreboard = self.scoreboard.get_sorted_scoreboard()
                    for player in sorted_scoreboard:
                        if sorted_scoreboard[player]['score'] >= DEFAULT_TARGET_SCORE:
                            print(f"{player} wins ! scoring {sorted_scoreboard[player]['score']} in {sorted_scoreboard[player]['rolls']} rolls with {sorted_scoreboard[player]['full_roll']} full roll, {sorted_scoreboard[player]['bonus']} bonus and {sorted_scoreboard[player]['max_potential_lost']} potential points lost")
                        
                        else:
                            print(f"{player} lose ! scoring {sorted_scoreboard[player]['score']} in {sorted_scoreboard[player]['rolls']} rolls with {sorted_scoreboard[player]['full_roll']} full roll, {sorted_scoreboard[player]['bonus']} bonus and {sorted_scoreboard[player]['max_potential_lost']} potential points lost")
                
                    self.stats.print_endgame_stats()
                    self.is_finished = True
                    break