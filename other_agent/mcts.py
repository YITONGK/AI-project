import random
import math

from referee.game import Board, PlayerColor, SpreadAction, SpawnAction, HexPos, HexDir, Action
from referee.game.board import CellState
import copy
from referee.game.constants import *
from .spread import spread, spawn
from .utils import get_action_list

class Node:
    def __init__(self, board: Board, parent =None):
        self.board = board
        self.parent = parent
        self.children = []
        self.wins = 0
        self.plays = 0

    def ucb1(self, c: float = 1.0):
        if self.plays == 0:
            return math.inf
        return self.wins / self.plays + c * math.sqrt(math.log(self.parent.plays) / self.plays)

    def select_child(self):
        return max(self.children, key = lambda child: child.ucb1())
