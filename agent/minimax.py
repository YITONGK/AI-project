from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action

from referee.game.constants import *


def get_action_list(curr_board: Board, color: PlayerColor) -> list[Action]:
    next_action = []
    # add spread action
    for key in curr_board:
        if curr_board[key].player == color:
            coord = HexPos(key.q, key.r)
            for direction in HexDir:
                next_action.append(SpreadAction(coord, direction))
    # add spawn action
    for q in range(BOARD_N):
        for r in range(BOARD_N):
            if curr_board[HexPos(q, r)].player == None:
                # print(q,r)
                # print(SpawnAction(HexPos(q, r)))
                next_action.append(SpawnAction(HexPos(q, r)))
    return next_action


