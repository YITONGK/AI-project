import math
import random

from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action
from referee.game.board import CellState
import copy
from referee.game.constants import *
from .spread import spread, spawn
from .utils import get_action_list


def minimax(curr_board, action_list) -> Action:
    action_evaluation = []
    max_eva = -999
    chosen_actions = []
# for each move in the subtree, iterate the possible nodes
    for action in action_list:
        if (curr_board._total_power < 49) or ((curr_board._total_power >= 49) and type(action) != SpawnAction):
            new_board = copy.copy(curr_board)
            new_board.apply_action(action)
            action_list = get_action_list(new_board, new_board.turn_color)
            cur_ult = iterate_nodes(new_board, action_list, 1)
            action_evaluation.append((cur_ult, action))
            new_board.undo_action()

# find move with max evaluation value
    for move in action_evaluation:
        if move[0] > max_eva:
            max_eva = move[0]

    for move in action_evaluation:
        if move[0] == max_eva:
            chosen_actions.append(move[1])

    # if max_eva == -999:
    #     chosen_action = random.choice(action_list)
    # else:
    chosen_action = random.choice(chosen_actions)
    return chosen_action

def iterate_nodes(curr_board,action_list,level) -> int:
    if level % 2 == 0:
        eva_num = -999
    else:
        eva_num = 999
    action_evaluation = []
    if level < 2:
        for action in action_list:
            if (curr_board._total_power < 49) or ((curr_board._total_power >= 49) and type(action) != SpawnAction):
                cur_action_evaluation = []
                new_board = copy.copy(curr_board)
                new_board.apply_action(action)
                action_list = get_action_list(new_board, new_board.turn_color)
                cur_ult = iterate_nodes(new_board, action_list, level + 1)
                cur_action_evaluation.append(cur_ult)
                if level % 2 == 0:
                    action_evaluation.append(max(cur_action_evaluation))
                else:
                    action_evaluation.append(min(cur_action_evaluation))
                new_board.undo_action()
    else:
        action_dict = assign_utility(curr_board, action_list, curr_board.turn_color)
        for action in action_dict:
            if (action_dict[action] > eva_num) and (level % 2 == 0):
                eva_num = action_dict[action]
            elif (action_dict[action] < eva_num) and (level % 2 != 0):
                eva_num = action_dict[action]
        return eva_num

    if level % 2 == 0:
        return max(action_evaluation)
    else:
        return min(action_evaluation)

def ab_minimax(curr_board: Board, action_list: list[Action]) -> Action:
    max_eva = -999
    chosen_action = random.choice(action_list)
    b = -999
# for each move in the subtree, iterate the possible nodes
    for action in action_list:
        if (curr_board._total_power < 49) or ((curr_board._total_power >= 49) and type(action) != SpawnAction):
            new_board = copy.copy(curr_board)
            new_board.apply_action(action)
            action_list = get_action_list(new_board, new_board.turn_color)
            cur_ult = ab_iterate_nodes(new_board, action_list, 1, b)

            if cur_ult > b:
                b = cur_ult
                chosen_action = action
            new_board.undo_action()

    if b == 0:
        chosen_action = random.choice(action_list)
    return chosen_action

def ab_iterate_nodes(curr_board: Board, action_list: list[Action], level: int ,pre_b: int) -> int:
    a = 999
    b = -999
    if level < 3:
        for action in action_list:
            if (curr_board._total_power < 49) or ((curr_board._total_power >= 49) and type(action) != SpawnAction):
                new_board = copy.copy(curr_board)
                new_board.apply_action(action)
                action_list = get_action_list(new_board, new_board.turn_color)
                cur_ult = ab_iterate_nodes(new_board, action_list, level + 1, pre_b)
                new_board.undo_action()
                if level % 2 != 0:
                    if cur_ult < pre_b:
                        a = cur_ult
                        break
                    else:
                        if cur_ult < a:
                            a = cur_ult
                else:
                    if cur_ult < pre_b:
                        b = cur_ult
                        break
                    else:
                        if b < cur_ult:
                            b = cur_ult
        if level % 2 == 0:
            return a
        else:
            return b
    else:
        for action in action_list:
            new_board = copy.copy(curr_board)
            new_board.apply_action(action)
            cur_heuristic = heuristic(curr_board)
            new_board.undo_action()
            return cur_heuristic

def heuristic(board: Board):

    if game_over(board._state, board.turn_color.opponent) == 1:
        heuristic_num = 999
    elif game_over(board._state, board.turn_color.opponent) == -1:
        heuristic_num = -999
    else:
        if board.turn_color == PlayerColor.RED:
            heuristic_num = board._color_power(PlayerColor.BLUE) - board._color_power(PlayerColor.RED)
        else:
            heuristic_num = board._color_power(PlayerColor.RED) - board._color_power(PlayerColor.BLUE)

    return heuristic_num


# assign utility value to each action in the list and return as a dict
def assign_utility(curr_board: Board, action_list: list[Action], color: PlayerColor) -> dict[Action, int]:
    action_dict = {}
    for action in action_list:
        utility = calculate_utility(curr_board, action, color)
        action_dict[action] = utility
    return action_dict

# initially use power difference before and after an action applies to the current board as utility value
def calculate_utility(curr_board: Board, action: Action, color: PlayerColor) -> int:
    if game_over(curr_board._state, curr_board.turn_color.opponent) == 1:
        return 999
    elif game_over(curr_board._state, curr_board.turn_color.opponent) == -1:
        return -999
    else:
        initial_power_difference = calculate_power_difference(curr_board._state, color)
        temp_state = curr_board._state.copy()
        # temp_board.apply_action(action)
        apply_action(temp_state, action, color)
        final_power_difference = calculate_power_difference(temp_state, color)
        return final_power_difference - initial_power_difference

def assign_utility_2(curr_board: Board, action_list: list[Action], color: PlayerColor) -> dict[Action, int]:
    action_dict = {}
    for action in action_list:
        utility = calculate_utility_2(curr_board, action, color)
        action_dict[action] = utility
    return action_dict

def calculate_utility_2(curr_board: Board, action: Action, color: PlayerColor) -> float:
    temp_state = curr_board._state.copy()
    apply_action(temp_state, action, color)
    my_power = 0
    oppo_power = 0
    for key, value in temp_state.items():
        if value.player == color:
            my_power += value.power
        else:
            oppo_power += value.power
    if oppo_power == 0:
        return 0
    else:
        return my_power / oppo_power

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
    # new_state = temp_state.copy()
    match action:
        case SpawnAction():
            spawn(temp_state, action, color)
        case SpreadAction():
            spread(temp_state, action)
    # return new_state



def game_over(state: dict[HexPos, CellState], color: PlayerColor) -> int:
    my_token = 0
    oppo_token = 0
    for key, value in state.items():
        if value.player == color:
            my_token += 1
        if value.player == color.opponent:
            oppo_token += 1
    if my_token != 0 and oppo_token == 0:
        return 1
    if oppo_token != 0 and my_token == 0:
        return -1
    else:
        return 0


def win_or_lose(curr_board : Board, action : Action, player_color : PlayerColor) -> str:
    curr_board.apply_action(action)
    red_power = curr_board._color_power(PlayerColor.RED)
    blue_power = curr_board._color_power(PlayerColor.BLUE)
    curr_board.undo_action()
    if red_power == 0 or blue_power == 0:
        if (red_power == 0 and PlayerColor.RED == player_color) or (blue_power == 0 and player_color == PlayerColor.BLUE):
            return "lose"
        elif(red_power == 0 and PlayerColor.BLUE == player_color) or (blue_power == 0 and PlayerColor.RED == player_color):
            return "win"
    else:
        return "continue"