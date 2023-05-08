# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, Board
from .minimax import minimax
from .action_list import get_action_list

# initialise a board for our action decision
board = Board()
# some constants to be passed to minimax search function
depth = 5
k = 6
alpha = float('-inf')
beta = float('inf')

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        action = None
        match self._color:
            case PlayerColor.RED:
                action = minimax(board, depth, k, alpha, beta, PlayerColor.RED, PlayerColor.RED)[1]
            case PlayerColor.BLUE:
                action = minimax(board, depth, k, alpha, beta, PlayerColor.BLUE, PlayerColor.BLUE)[1]
        # this if statement is to avoid 'unknown action ACK' error
        if action is None:
            return random.choice(get_action_list(board, self._color))
        return action

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        board.apply_action(action)

        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass
