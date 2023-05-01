# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from referee.game import Board
from .greedy_search import greedy_search
from .minimax_search import assign_utility
from .random_search import random_search
from .utils import get_action_list
from .minimax_search import minimax

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
        # state[(3, 3)] = ("r", 1)
        # state[(3, 2)] = ("b", 1)
        match self._color:
            case PlayerColor.RED:
                # action = SpawnAction(HexPos(3, 3))
                curr_board = board
                red_action_list = get_action_list(curr_board, PlayerColor.RED)
                red_action_dict = assign_utility(curr_board, red_action_list, PlayerColor.RED)
                action = minimax(curr_board,red_action_list)
                #action = greedy_search(red_action_list, red_action_dict)
                # action = random_search(red_action_list)
                red_action_list.clear()
                red_action_dict.clear()
                # for i in range(len(red_action_list)):
                #     print(i, ": ", red_action_list[i], "---", action_dict[red_action_list[i]])
                # print(state, "\n\n")
                # move = translate(action)
                # update(state, move)
                # return action
            case PlayerColor.BLUE:
                # This is going to be invalid... BLUE never spawned!
                # action = SpawnAction(HexPos(3, 2))
                curr_board = board
                blue_action_list = get_action_list(curr_board, PlayerColor.BLUE)
                blue_action_dict = assign_utility(curr_board, blue_action_list, PlayerColor.BLUE)
                #action = minimax(curr_board, blue_action_list)
                action = greedy_search(blue_action_list, blue_action_dict)
                # action = random_search(blue_action_list)
                blue_action_list.clear()
                blue_action_dict.clear()
                # action = SpreadAction(HexPos(3, 3), HexDir.Up)
                # print(state, "\n\n")
                # return action
        # print_action(action)
        return action


    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        board.apply_action(action)
        curr_state = board._state

        # for key in curr_state:
        #     print(key, curr_state[key])

        # print(curr_state)
        # print_state(curr_state)

        # action_list = get_action_list(curr_board, PlayerColor.RED)
        # for i in range(len(action_list)):
        #     print(i, ": ", action_list[i])

        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass


# use to debug
def print_action(action: Action):
    if type(action) == SpawnAction:
        print(action.cell)
    if type(action) == SpreadAction:
        print(action.cell, action.direction)

# use to debug
def print_state(curr_state: dict):
    print("current board state:")
    for key in curr_state:
        if curr_state[key].player != None:
            print(key, curr_state[key])