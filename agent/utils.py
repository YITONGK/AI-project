from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action

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