import random

from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action
from referee.game.board import CellState
import copy

from referee.game.constants import *
from .spread import spread
from .utils import get_action_list


def minimax(curr_board, action_list) -> Action:
    action_evaluation = []
    max_eva = -999
    chosen_action = random.choice(action_list)
# for each move in the subtree, iterate the possible nodes
    for action in action_list:
        new_board = copy.copy(curr_board)
        action_list = get_action_list(new_board,new_board.turn_color)
        cur_ult = iterate_nodes(new_board,action_list,1)
        action_evaluation.append((cur_ult,action))

# find move with max evaluation value
    for move in action_evaluation:
        if move[0] > max_eva:
            max_eva = move[0]
            chosen_action = move[1]

    return chosen_action

def iterate_nodes(curr_board,action_list,level) -> int:
    max_eva = -999
    action_evaluation = []
    if level < 2:
        for action in action_list:
            new_board = copy.copy(curr_board)
            action_list = get_action_list(new_board, new_board.turn_color)
            cur_ult = iterate_nodes(new_board, action_list, level + 1)
            action_evaluation.append((cur_ult, action))

    else:
        action_dict = assign_utility(curr_board, action_list, curr_board._turn_color)
        for action in action_dict:
            if action_dict[action] > max_eva:
                max_eva = action_dict[action];
        return max_eva
    return 0



# assign utility value to each action in the list and return as a dict
def assign_utility(curr_board: Board, action_list: list[Action], color: PlayerColor) -> dict[Action, int]:
    action_dict = {}
    for action in action_list:
        utility = calculate_utility(curr_board, action, color)
        action_dict[action] = utility
    return action_dict

# initially use power difference before and after an action applies to the current board as utility value
def calculate_utility(curr_board: Board, action: Action, color: PlayerColor) -> int:
    initial_power_difference = calculate_power_difference(curr_board._state, color)
    temp_state = curr_board._state.copy()
    # temp_board.apply_action(action)
    apply_action(temp_state, action, color)
    final_power_difference = calculate_power_difference(temp_state, color)
    return final_power_difference - initial_power_difference

def calculate_power_difference(state: dict[HexPos, CellState], color: PlayerColor) -> int:
    my_power = 0
    oppo_power = 0
    for key in state:
        cellstate = state[key]
        if cellstate.player == color:
            my_power += cellstate.power
        else:
            oppo_power += cellstate.power
    return my_power - oppo_power

def apply_action(temp_state: dict[HexPos, CellState], action: Action, color: PlayerColor) -> None:
    if type(action) == SpawnAction:
        cellState = CellState(color, 1)
        temp_state[action.cell] = cellState
    if type(action) == SpreadAction:
        spread(temp_state, action)
    # match type(action):
    #     case SpawnAction:
    #         cellState = CellState(color, 1)
    #         temp_state[action.cell] = cellState
    #     case SpreadAction:
    #         spread(temp_state, action)

