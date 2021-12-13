from random import randint

# Target total score to win by default
DEFAULT_TARGET_SCORE = 2000

# Number of dices by default in the set
DEFAULT_DICES_NB = 5
# Number of side of the dices used in the game
NB_DICE_SIDE = 6

# List of dice value scoring
LIST_SCORING_DICE_VALUE = [1, 5]
# List of associated score for scoring dice values
LIST_SCORING_MULTIPLIER = [100, 50]

# Trigger for multiple bonus
TRIGGER_OCCURRENCE_FOR_BONUS = 3
# Special bonus multiplier for multiple ace bonus
BONUS_VALUE_FOR_ACE_BONUS = 1000
# Standard multiplier for multiple dices value bonus
BONUS_VALUE_FOR_NORMAL_BONUS = 100


def roll_dice_set(nb_dice_to_roll):
    occurences = [0] * NB_DICE_SIDE
    for i in range(nb_dice_to_roll):
        random_number = randint(1, NB_DICE_SIDE)
        occurences[random_number - 1] += 1

    return occurences


def bonus_point(occArray):
    bonus = 0
    for index, occ in enumerate(occArray):
        if index != 0 and occ >= TRIGGER_OCCURRENCE_FOR_BONUS:
            bonus += (index + 1) * BONUS_VALUE_FOR_NORMAL_BONUS
            occArray[index] -= TRIGGER_OCCURRENCE_FOR_BONUS
        elif index == 0 and occ >= TRIGGER_OCCURRENCE_FOR_BONUS:
            bonus += BONUS_VALUE_FOR_ACE_BONUS
            occArray[index] -= TRIGGER_OCCURRENCE_FOR_BONUS

    return occArray, bonus


def total_score(nb_roll):
    array_occ = roll_dice_set(nb_roll)
    new_array, score = bonus_point(array_occ)
    for index, occ in enumerate(new_array):
        if index + 1 in LIST_SCORING_DICE_VALUE:
            score += occ * LIST_SCORING_MULTIPLIER[LIST_SCORING_DICE_VALUE.index(index + 1)]

    return score


print(total_score(8))