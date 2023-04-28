from referee.game import Action
import random

# select a possible next action randomly
def random_search(action_list: list[Action]):
    return random.choice(action_list)
