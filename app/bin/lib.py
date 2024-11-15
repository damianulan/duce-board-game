import json
import os
from app.models.gear.Lang import Lang
import random

def lang(key):
    locale = 'pl'
    full_key = locale+'.'+key
    output = key

    try:
        result = Lang.get(key=full_key)
        if result:
            output = result.value
    except Exception as e:
        output = "{"+key+"}"
    return output

def clean_cache():
    Lang.recreate()

def binary_chances(modifiers = 0):
    chances = {
        "yes": modifiers,
        "no" : 100 - modifiers
    }
    return chances

def rand_choices(chances, k=1):
    items = list(chances.keys())
    weights = list(chances.values())

    return random.choices(items, cum_weights=weights, k=k)

def dice_probability(k, chances):
    """
    :param chances:
    :param k:
    chances = {
        "apple": 10,
        "banana": 30,
        "cherry": 60
    }
    """
    dice = roll_dice(k)

    # Extract items and weights
    index = int(dice) - 1

    # Use random.choices to select based on weights for each roll
    results = rand_choices(chances, k)
    return results[index]

def binary_probability(modifiers):
    chances = binary_chances(modifiers)
    items = list(chances.keys())
    weights = list(chances.values())
    choice = random.choices(items, cum_weights=weights, k=1)[0]
    if 'yes' == choice :
        return True
    return False

def dice_binary(modifiers, k=12):
    chances = binary_chances(modifiers)
    items = list(chances.keys())
    weights = list(chances.values())
    dice = roll_dice(k)
    index = dice - 1
    choice = random.choices(items, cum_weights=weights, k=k)[index]
    if 'yes' == choice :
        return True
    return False

def dice_highest_score(min_score, bonus, k):
    dice = roll_dice(k) + int(bonus)
    if dice >= min_score :
        return True
    return False

def roll_dice(k):
    dice = 0
    while True:
        if 0 < dice <= k:
            break
        else :
            dice = int(input("Podaj wynik rzutu kostką [k"+str(k)+"]: "))

    return dice

def increase_by_percentage(value, percentage) :
    return value * (1 + percentage / 100)

def warning(text):
    print(f"{Bcolors.WARNING}{text}{Bcolors.ENDC}")

def danger(text):
    print(f"{Bcolors.FAIL}{text}{Bcolors.ENDC}")

def success(text):
    print(f"{Bcolors.OKGREEN}{text}{Bcolors.ENDC}")

def highlight(text):
    print(f"{Bcolors.OKCYAN}{text}{Bcolors.ENDC}")

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'