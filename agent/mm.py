import copy
import random

from referee.game import Board, PlayerColor
from .action_list import get_action_list, sort_action_list, top_k
from .utility import evaluate


def ab_mm(board: Board, depth: int, k: int, alpha: float, beta: float,
          curr_color: PlayerColor, original_color: PlayerColor):
    # check whether the search should stop
    if depth == 0 or board.game_over:
        return evaluate(board, original_color), None
    best_action = None
    action_list = get_action_list(board, curr_color)
    # try to use perfect ordering
    action_list = sort_action_list(board, action_list, curr_color)
    # try to use top_k
    action_list = top_k(action_list, k)
    new_board = copy.copy(board)
    if curr_color == original_color:
        # If the current color is the caller of this minimax search, initialize the value to negative infinity
        best_utility = float('-inf')
        for action in action_list:
            new_board.apply_action(action)
            # Recursively call minimax with next level and opponent
            utility, _ = ab_mm(new_board, depth - 1, k, alpha, beta, curr_color.opponent, original_color)
            new_board.undo_action()
            # If the new board has a higher evaluation than the current best, update best_utility and the best action
            if utility > best_utility:
                best_utility = utility
                best_action = action
            # If the new board has the same evaluation as the current best, randomly pick among action and best action
            elif utility == best_utility:
                best_action = random.choice([best_action, action])
            # Update alpha
            alpha = max(alpha, best_utility)
            # If alpha is greater than or equal to beta, pruning occurs, loop stops
            if alpha >= beta:
                break
        return best_utility, best_action
    else:
        # If the current color is the opponent of initial caller, initialize the value to negative infinity
        best_utility = float('inf')
        for action in action_list:
            new_board.apply_action(action)
            # Recursively call minimax with next level and opponent
            utility, _ = ab_mm(new_board, depth - 1, k, alpha, beta, curr_color.opponent, original_color)
            new_board.undo_action()
            # If the new board has a lower evaluation than the current best, update best_utility and the best action
            if utility < best_utility:
                best_utility = utility
                best_action = action
            # If the new board has the same evaluation as the current best, randomly pick among action and best action
            elif utility == best_utility:
                best_action = random.choice([best_action, action])
            # Update beta
            beta = min(beta, best_utility)
            # If alpha is greater than or equal to beta, pruning occurs, loop stops
            if alpha >= beta:
                break
        return best_utility, best_action
