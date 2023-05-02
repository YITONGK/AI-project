import copy
import random

from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action
from referee.game.board import CellState
from referee.game.constants import *
from .minimax_search import game_over
from .spread import spread, spawn
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




def evaluate(board: Board, color: PlayerColor):
    if board.game_over:
        if board.winner_color == color:
            return float('inf')
        else:
            return float('-inf')
    else:
        return calculate_utility_2(board._state, color)



def calculate_utility_2(state: dict[HexPos, CellState], color: PlayerColor) -> float:
    my_power = 0
    oppo_power = 0
    for key, value in state.items():
        if value.player == color:
            my_power += value.power
        else:
            oppo_power += value.power
    if oppo_power == 0:
        return 0
    else:
        return my_power / oppo_power


def apply_action(temp_state: dict[HexPos, CellState], action: Action, color: PlayerColor) -> None:
    new_state = temp_state.copy()
    match action:
        case SpawnAction():
            spawn(new_state, action, color)
        case SpreadAction():
            spread(new_state, action)
    return new_state


def get_action_list(board: Board, color: PlayerColor) -> list[Action]:
    action_list = []
    total_power = 0
    state = board._state
    for key, value in state.items():
        total_power += value.power
    # add spread action
    for key in state:
        if state[key].player == color:
            coord = HexPos(key.r, key.q)
            for direction in HexDir:
                action_list.append(SpreadAction(coord, direction))
    # add spawn action
    if total_power < MAX_TOTAL_POWER:
        for r in range(BOARD_N):
            for q in range(BOARD_N):
                if state[HexPos(r, q)].player == None:
                    # print(q,r)
                    # print(SpawnAction(HexPos(q, r)))
                    action_list.append(SpawnAction(HexPos(r, q)))
    return action_list

def game_over(board: Board) -> bool:
    """
    True iff the game is over.
    """
    if board.turn_count < 2:
        return False

    return any([
        board.turn_count >= MAX_TURNS,
        board._color_power(PlayerColor.RED) == 0,
        board._color_power(PlayerColor.BLUE) == 0
    ])