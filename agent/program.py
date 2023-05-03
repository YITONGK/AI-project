# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, Board
from .mm import ab_mm
from .action_list import get_action_list

# This is the entry point for your game playing agent. Currently, the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

board = Board()


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
        curr_board = board
        action = None
        match self._color:
            case PlayerColor.RED:
                action = ab_mm(curr_board, 5, 7, float('-inf'), float('inf'), PlayerColor.RED, PlayerColor.RED)[1]
            case PlayerColor.BLUE:
                action = ab_mm(curr_board, 5, 7, float('-inf'), float('inf'), PlayerColor.BLUE, PlayerColor.BLUE)[1]
        print(*referee)
        print(referee["time_remaining"], "      ", referee["space_remaining"], "        ", referee["space_limit"])
        if action is None:
            return random.choice(get_action_list(curr_board, self._color))
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
