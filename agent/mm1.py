
from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action
from referee.game.board import CellState
from referee.game.constants import *
from .minimax_search import game_over
from .spread import spread, spawn
from .utils import get_action_list


def mm1(board: Board, depth: int, alpha, beta, color: PlayerColor):
    if depth == 0 or board.game_over():
        return evaluate(board)




    return


def evaluate(board: Board):
    return