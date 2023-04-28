from referee.game import Action
import random

# select the action with the highest utility value at the moment
def greedy_search(action_list: list[Action], action_dict: dict[Action, int]) -> Action:
    action_chosen = random.choice(action_list)
    max_utility = action_dict[action_chosen]
    for action in action_list:
        if action_dict[action] > max_utility:
            action_chosen = action
            max_utility = action_dict[action]
    return action_chosen