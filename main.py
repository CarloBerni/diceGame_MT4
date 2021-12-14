import random

DEFAULT_TARGET_SCORE = 2000 # Target total score to win by default

NB_DICE_SIDE = 6  # Nb of side of the Dices
DEFAULT_DICES_NB = 5 # Nb of dices to roll
SCORING_DICE_VALUE_LIST = [1, 5]  # List of the side values of the dice who trigger a standard score
SCORING_MULTIPLIER_LIST = [100, 50]  # List of multiplier for standard score

THRESHOLD_BONUS = 3  # Threshold of the triggering for bonus in term of occurrence of the same slide value
STD_BONUS_MULTIPLIER = 100  # Standard multiplier for bonus
ACE_BONUS_MULTIPLIER = 1000  # Special multiplier for aces bonus
PLAYERS = ["Stéphane", "François", "Romain", "Laurent", "Christophe", "Isabelle", "Sylvie"] # List of players


# return a list of dices value occurrence for a roll of nb_dice_to_roll dices
def roll_dice_set(nb_dice_to_roll):
    dice_value_occurrence_list = [0] * NB_DICE_SIDE
    for n in range(nb_dice_to_roll):
        dice_value = random.randint(1, NB_DICE_SIDE)
        dice_value_occurrence_list[dice_value - 1] += 1

    return dice_value_occurrence_list

# returns the numbers of dices to roll
def analyse_dices_to_roll(nb_dices_rolled, dice_value_occurence_list):
    return nb_dices_rolled - (nb_dices_rolled - sum(dice_value_occurence_list))


def analyse_bonus_score(dice_value_occurrence_list):
    score = 0
    for side_value_index, dice_value_occurrence in enumerate(dice_value_occurrence_list):
        nb_of_bonus = dice_value_occurrence // THRESHOLD_BONUS
        if nb_of_bonus > 0:
            if side_value_index == 0:
                bonus_multiplier = ACE_BONUS_MULTIPLIER
            else:
                bonus_multiplier = STD_BONUS_MULTIPLIER
            score += nb_of_bonus * bonus_multiplier * (side_value_index + 1)
            dice_value_occurrence_list[side_value_index] %= THRESHOLD_BONUS

    return score, dice_value_occurrence_list


def analyse_standard_score(dice_value_occurrence_list):
    score = 0
    for scoring_value, scoring_multiplier in zip(SCORING_DICE_VALUE_LIST, SCORING_MULTIPLIER_LIST):
        score += dice_value_occurrence_list[scoring_value - 1] * scoring_multiplier
        dice_value_occurrence_list[scoring_value - 1] = 0

    return score, dice_value_occurrence_list


def analyse_score(dice_value_occurrence_list):
    bonus_score, dice_value_occurrence_list = analyse_bonus_score(dice_value_occurrence_list)
    standard_score, dice_value_occurrence_list = analyse_standard_score(dice_value_occurrence_list)

    return bonus_score + standard_score

def init_scoreboard():
    scoreboard = {}
    for player in PLAYERS:
        scoreboard[player] = {
            "score": 0,
            "lost_score": 0,
            "rolls": 0
        }
    return scoreboard


def print_total_score(scoreboard):
    total_score = "Total score: "
    for player in scoreboard:
        current_player_score = scoreboard[player]['score']
        total_score += f"{player}--> {current_player_score}, "
    print(total_score + "\n")


def game():
    is_finished = False
    current_turn = 0
    scoreboard = init_scoreboard()
    while not is_finished:
        current_turn += 1
        for player in PLAYERS:
            
            print(f"turn#{current_turn}-->{player} rank #1, score {scoreboard[player]['score']}")
            
            current_roll = 0
            potential_turn_score = 0
            is_looser = False
            reroll = "y"
            remaining_dices = DEFAULT_DICES_NB

            while remaining_dices > 0 and reroll == "y":
                current_roll += 1
                dices_occurences = roll_dice_set(remaining_dices)
                previous_remaining_dices = remaining_dices
                potential_roll_score = analyse_score(dices_occurences)
                remaining_dices = analyse_dices_to_roll(remaining_dices, dices_occurences)
                potential_turn_score += potential_roll_score
                print(f"roll #{current_roll} : {previous_remaining_dices - remaining_dices} scoring dices scoring {potential_roll_score}, potential total turn score {potential_turn_score}, remaining dice to roll : {remaining_dices}")
                if potential_roll_score == 0:
                    is_looser = True
                    break
                elif remaining_dices > 0:
                    reroll = input(f"Do you want to reroll {remaining_dices} dices ? [y/n]")
            
            
            if is_looser:
                print(f"you lose this turn and a potential to score {potential_turn_score} pts\n")
                scoreboard[player]["lost_score"] += potential_turn_score
            else:
                print(f"you win this turn, scoring {potential_turn_score} pts\n")
                scoreboard[player]["score"] += potential_turn_score
            print_total_score(scoreboard)
            
            if scoreboard[player]["score"] >= DEFAULT_TARGET_SCORE:
                is_finished = True
                break
        
    print(f"Game in {current_turn} turns")
        
        
            
        
game()
