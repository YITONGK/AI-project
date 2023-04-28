from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action
from referee.game.board import CellState

from referee.game.constants import *


def get_action_list(curr_board: Board, color: PlayerColor) -> list[Action]:
    curr_state = curr_board._state
    action_list = []
    # add spread action
    for key in curr_state:
        if curr_state[key].player == color:
            coord = HexPos(key.q, key.r)
            for direction in HexDir:
                action_list.append(SpreadAction(coord, direction))
    # add spawn action
    for q in range(BOARD_N):
        for r in range(BOARD_N):
            if curr_state[HexPos(q, r)].player == None:
                # print(q,r)
                # print(SpawnAction(HexPos(q, r)))
                action_list.append(SpawnAction(HexPos(q, r)))
    return action_list

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

def calculate_power_difference(state: dict, color: PlayerColor):
    my_power = 0
    oppo_power = 0
    for key in state:
        cellstate = state[key]
        if cellstate.player == color:
            my_power += cellstate.power
        else:
            oppo_power += cellstate.power
    return my_power - oppo_power

def apply_action(temp_state: dict, action: Action, color: PlayerColor):
    if type(action) == SpawnAction:
        cellState = CellState(color, 1)
        temp_state[action.cell] = cellState
    if type(action) == SpreadAction:
        spread(temp_state, action)

def spread(temp_state: dict, action: Action):
    curr_cell = action.cell
    direction = action.direction
    color = temp_state[curr_cell].player
    power = temp_state[curr_cell].power
    cell_to_update = []

