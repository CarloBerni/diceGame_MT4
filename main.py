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


def analyse_standard_score(dice_value_occurrence_list):
    score = 0
    for scoring_value, scoring_multiplier in zip(SCORING_DICE_VALUE_LIST, SCORING_MULTIPLIER_LIST):
        score += dice_value_occurrence_list[scoring_value - 1] * scoring_multiplier
        dice_value_occurrence_list[scoring_value - 1] = 0

    return score, dice_value_occurrence_list


def analyse_score(dice_value_occurrence_list):
    bonus_score, dice_value_occurrence_list, times_bonus = analyse_bonus_score(dice_value_occurrence_list)
    standard_score, dice_value_occurrence_list = analyse_standard_score(dice_value_occurrence_list)

    return bonus_score + standard_score, times_bonus

def init_scoreboard():
    scoreboard = {}
    for player in PLAYERS:
        scoreboard[player] = {
            "score": 0,
            "bonus": 0,
            "lost_score": 0,
            "rolls": 0,
            "full_roll": 0,
            "max_potential_lost": 0,
            "rank": 0,
        }
    return scoreboard


def get_sorted_scoreboard(scoreboard):
    sorted_dict_keys = sorted(scoreboard, key=lambda x: (scoreboard[x]['score']), reverse=True)
    for player in scoreboard:
        scoreboard[player]['rank'] = sorted_dict_keys.index(player) + 1

    return {x:scoreboard[x] for x in sorted_dict_keys}

def print_total_score(scoreboard):
    sorted_scoreboard = get_sorted_scoreboard(scoreboard)
    total_score = "Total score: "
    for player in sorted_scoreboard:
        current_player_score = sorted_scoreboard[player]['score']
        total_score += f"{player}--> {current_player_score}, "
    print(total_score + "\n")


def game():
    is_finished = False
    current_turn = 0
    scoreboard = init_scoreboard()
    scored_max_turn = ['', 0]
    max_loss_turn = ['', 0]
    longest_turn = ['', 0]
    scoring_turn = [0, 0]
    non_scoring_turn = [0, 0]
    while not is_finished:
        current_turn += 1
        for player in PLAYERS:

            print_total_score(scoreboard)

            print(f"turn#{current_turn}-->{player} rank #{scoreboard[player]['rank']}, score {scoreboard[player]['score']}")
            
            current_roll = 0
            potential_turn_score = 0
            is_looser = False
            reroll = "y"
            remaining_dices = DEFAULT_DICES_NB

            while remaining_dices > 0 and reroll == "y":

                if potential_turn_score > scoreboard[player]['max_potential_lost']:
                    scoreboard[player]['max_potential_lost'] = potential_turn_score

                current_roll += 1
                scoreboard[player]['rolls'] += 1
                dices_occurences = roll_dice_set(remaining_dices)
                previous_remaining_dices = remaining_dices
                potential_roll_score, times_bonus = analyse_score(dices_occurences)
                remaining_dices = analyse_dices_to_roll(remaining_dices, dices_occurences)
                potential_turn_score += potential_roll_score
                
                print(f"roll #{current_roll} : {previous_remaining_dices - remaining_dices} scoring dices scoring {potential_roll_score}, potential total turn score {potential_turn_score}, remaining dice to roll : {remaining_dices}")
                

                # Stats
                if remaining_dices == 0 and potential_roll_score > 0:
                    scoreboard[player]['full_roll'] += 1
                    remaining_dices = DEFAULT_DICES_NB

                if current_roll > longest_turn[1]:
                    longest_turn[0] = player
                    longest_turn[1] = current_roll

                scoreboard[player]['bonus'] += times_bonus

                if potential_roll_score == 0:
                    is_looser = True
                    break
                elif remaining_dices > 0:
                    reroll = input(f"Do you want to reroll {remaining_dices} dices ? [y/n]")


            if is_looser:
                print(f"you lose this turn and a potential to score {potential_turn_score} pts\n")
                scoreboard[player]["lost_score"] += potential_turn_score
                non_scoring_turn[0] += 1
                non_scoring_turn[1] += potential_turn_score

                if potential_turn_score > max_loss_turn[1]:
                    max_loss_turn[0] = player
                    max_loss_turn[1] = potential_turn_score

            else:
                print(f"you win this turn, scoring {potential_turn_score} pts\n")
                scoreboard[player]["score"] += potential_turn_score
                scoring_turn[0] += 1
                scoring_turn[1] += potential_turn_score

                if potential_turn_score > scored_max_turn[1]:
                    scored_max_turn[0] = player
                    scored_max_turn[1] = potential_turn_score

            
            #ENDGAME
            if scoreboard[player]["score"] >= DEFAULT_TARGET_SCORE:
                print(f"Game in {current_turn} turns")
                sorted_scoreboard = get_sorted_scoreboard(scoreboard)
                for player in sorted_scoreboard:
                    if sorted_scoreboard[player]['score'] >= DEFAULT_TARGET_SCORE:
                        print(f"{player} wins ! scoring {sorted_scoreboard[player]['score']} in {sorted_scoreboard[player]['rolls']} rolls with {sorted_scoreboard[player]['full_roll']} full roll, {sorted_scoreboard[player]['bonus']} bonus and {sorted_scoreboard[player]['max_potential_lost']} potential points lost")
                    
                    else:
                        print(f"{player} lose ! scoring {sorted_scoreboard[player]['score']} in {sorted_scoreboard[player]['rolls']} rolls with {sorted_scoreboard[player]['full_roll']} full roll, {sorted_scoreboard[player]['bonus']} bonus and {sorted_scoreboard[player]['max_potential_lost']} potential points lost")
                    
                    
                print("\n")
                print(f"Max turn scoring : {scored_max_turn[0]} with {scored_max_turn[1]}")
                print(f"Longest turn : {longest_turn[0]} with {longest_turn[1]}")
                print(f"Max turn loss : {max_loss_turn[0]} with {max_loss_turn[1]}")

                print("\n")
                print(f"Mean scoring turn : {round(scoring_turn[1] / scoring_turn[0]} ({scoring_turn[0]} turns)")
                print(f"Mean non scoring turn : {round(non_scoring_turn[1] / non_scoring_turn[0]} ({non_scoring_turn[0]} turns)")
                is_finished = True
                break
        


  
game()