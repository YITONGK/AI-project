import copy
from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action
from referee.game.constants import *
from .utility import evaluate


# given a certain board and specified next player, return an action list containing all next possible moves
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
    # add spawn action if and only if total power on the board doesn't exceed 49
    if total_power < MAX_TOTAL_POWER:
        for r in range(BOARD_N):
            for q in range(BOARD_N):
                if state[HexPos(r, q)].player is None:
                    action_list.append(SpawnAction(HexPos(r, q)))
    return action_list


# sort the actions according to utility value to achieve prefect ordering in minimax with alpha beta pruning
# in this way, the time complexity will hugely decrease
def sort_action_list(board: Board, action_list: list[Action], color: PlayerColor) -> list[Action]:
    action_utility = []
    new_board = copy.copy(board)
    for action in action_list:
        new_board.apply_action(action)
        utility = evaluate(new_board, color)
        new_board.undo_action()
        action_utility.append((action, utility))
    # sort from large to small, so set reverse equals true
    sorted_list = sorted(action_utility, key=lambda x: x[1], reverse=True)
    # grab the first element in every tuple, combine them into a new list and return
    sorted_action_list = [t[0] for t in sorted_list]
    return sorted_action_list


# only take k actions with the largest utility value into consideration to further improve efficiency
def top_k(sorted_action_list: list[Action], k: int) -> list[Action]:
    return sorted_action_list[:k]
