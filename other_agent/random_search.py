from referee.game import Action
import random

def random_search(action_list: list[Action]) -> Action:
    return random.choice(action_list)
