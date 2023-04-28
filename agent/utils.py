from agent.spread import spread
from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action
from referee.game.board import CellState

from referee.game.constants import *

def get_action_list(curr_board: Board, color: PlayerColor) -> list[Action]:
    curr_state = curr_board._state
    action_list = []
    # add spread action
    for key in curr_state:
        if curr_state[key].player == color:
            coord = HexPos(key.r, key.q)
            for direction in HexDir:
                action_list.append(SpreadAction(coord, direction))
    # add spawn action, if total power exceeds 49, stop
    if curr_board._total_power < MAX_TOTAL_POWER:
        for r in range(BOARD_N):
            for q in range(BOARD_N):
                if curr_state[HexPos(r, q)].player == None:
                    # print(q,r)
                    # print(SpawnAction(HexPos(q, r)))
                    action_list.append(SpawnAction(HexPos(r, q)))
    return action_list


def apply_action(temp_state: dict[HexPos, CellState], action: Action, color: PlayerColor):
    if type(action) == SpawnAction:
        cellState = CellState(color, 1)
        temp_state[action.cell] = cellState
    if type(action) == SpreadAction:
        spread(temp_state, action)
    # match type(action):
    #     case SpreadAction:
    #         spread(temp_state, action)
    #     case SpawnAction:
    #         cellState = CellState(color, 1)
    #         temp_state[action.cell] = cellState