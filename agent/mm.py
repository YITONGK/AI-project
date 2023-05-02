import copy
import random

from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action
from referee.game.constants import *
from .utils import get_action_list

def mm(board: Board, depth: int, curr_color: PlayerColor, original_color: PlayerColor):
    if depth == 0 or board.game_over:
        return evaluate(board, original_color), None
    best_action = None
    action_list = get_action_list(board, curr_color)
    if curr_color == original_color:
        max_utility = float('-inf')
        for action in action_list:
            new_board = copy.copy(board)
            new_board.apply_action(action)
            utility, _ = mm(new_board, depth - 1, curr_color.opponent, original_color)
            new_board.undo_action()
            if utility > max_utility:
                max_utility = utility
                best_action = action
            elif utility == max_utility:
                best_action = random.choice([best_action, action])
        return max_utility, best_action
    else:
        min_utility = float('inf')
        for action in action_list:
            new_board = copy.copy(board)
            new_board.apply_action(action)
            utility, _ = mm(new_board, depth - 1, curr_color.opponent, original_color)
            new_board.undo_action()
            if utility < min_utility:
                min_utility = utility
                best_action = action
            elif utility == min_utility:
                best_action = random.choice([best_action, action])
        return min_utility, best_action

def ab_mm(board: Board, depth: int, alpha: float, beta: float, curr_color: PlayerColor, original_color: PlayerColor):
    if depth == 0 or board.game_over:
        return evaluate(board, original_color), None
    best_action = None
    action_list = get_action_list(board, curr_color)
    # try to use perfect ordering
    action_list = sort_action_list(board, action_list, curr_color)
    # try to use topk
    action_list = topk(action_list, 20)
    new_board = copy.copy(board)
    if curr_color == original_color:
        best_utility = float('-inf')
        for action in action_list:
            new_board.apply_action(action)
            utility, _ = ab_mm(new_board, depth - 1, alpha, beta, curr_color.opponent, original_color)
            new_board.undo_action()
            if utility > best_utility:
                best_utility = utility
                best_action = action
            alpha = max(alpha, best_utility)
            if alpha >= beta:
                break
        return best_utility, best_action
    else:
        best_utility = float('inf')
        for action in action_list:
            new_board.apply_action(action)
            utility, _ = ab_mm(new_board, depth - 1, alpha, beta, curr_color.opponent, original_color)
            new_board.undo_action()
            if utility < best_utility:
                best_utility = utility
                best_action = action
            beta = min(beta, best_utility)
            if alpha >= beta:
                break
        return best_utility, best_action

def evaluate(board: Board, color: PlayerColor):
    if board.game_over:
        if board.winner_color == color:
            return float('inf')
        else:
            return float('-inf')
    else:
        my_power = board._color_power(color)
        oppo_power = board._color_power(color.opponent)
        # to avoid division by zero error
        if oppo_power == 0:
            return 0
        else:
            return my_power / oppo_power

def get_action_list(board: Board, color: PlayerColor) -> list[Action]:
    action_list = []
    total_power = board._total_power
    state = board._state
    # add spread action
    for key, value in state.items():
        if value.player == color:
            coord = HexPos(key.r, key.q)
            for direction in HexDir:
                action_list.append(SpreadAction(coord, direction))
    # add spawn action
    if total_power < MAX_TOTAL_POWER:
        for r in range(BOARD_N):
            for q in range(BOARD_N):
                if state[HexPos(r, q)].player == None:
                    action_list.append(SpawnAction(HexPos(r, q)))
    return action_list

def sort_action_list(board: Board, action_list: list[Action], color: PlayerColor) -> list[Action]:
    action_utility = []
    new_board = copy.copy(board)
    for action in action_list:
        new_board.apply_action(action)
        utility = evaluate(new_board, color)
        new_board.undo_action()
        action_utility.append((action, utility))
    # sort the list of tuples according to utility value
    # and grab the first element in every tuple, combine them into a new list and return
    sorted_list = sorted(action_utility, key=lambda x: x[1], reverse=True)
    sorted_action_list = [t[0] for t in sorted_list]
    return sorted_action_list

def topk(action_list: list[Action], k: int):
    return action_list[:k]