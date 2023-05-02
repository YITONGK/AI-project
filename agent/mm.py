
from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action
from referee.game.board import CellState
from referee.game.constants import *
from .minimax_search import game_over
from .spread import spread, spawn
from .utils import get_action_list

def mm(state: dict[HexPos, CellState], action_list: list[Action], curr_color: PlayerColor, original_color: PlayerColor, depth: int):
    if game_over(state, original_color) == 2:
        return float('inf')
    if game_over(state, original_color) == 1:
        return float('-inf')
    if depth == 0 and game_over(state, original_color) == 0:
        return calculate_utility_2(state, original_color)
    else:
        if curr_color == original_color:
            max_utility = float('-inf')
            best_action = None
            for action in action_list:
                new_state = apply_action(state, action, curr_color)
                new_action_list = get_action_list(new_state, curr_color.opponent)
                utility = mm(new_state, new_action_list, curr_color.opponent, original_color, depth - 1)
                if utility > max_utility:
                    max_utility = utility
                    best_action = action
            return best_action
        else:
            min_utility = float('inf')
            best_action = None
            for action in action_list:
                new_state = apply_action(state, action, curr_color)
                new_action_list = get_action_list(new_state, curr_color.opponent)
                utility = mm(new_state, new_action_list, curr_color.opponent, original_color, depth - 1)
                if utility < min_utility:
                    min_utility = utility
                    best_action = action
            return best_action




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


def get_action_list(state: dict[HexPos, CellState], color: PlayerColor) -> list[Action]:
    action_list = []
    total_power = 0
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