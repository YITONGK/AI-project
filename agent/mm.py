import copy
from referee.game import Board, PlayerColor
from .action_list import get_action_list, sort_action_list, top_k
from .utility import evaluate


def ab_mm(board: Board, depth: int, k: int, alpha: float, beta: float,
          curr_color: PlayerColor, original_color: PlayerColor):
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
        best_utility = float('-inf')
        for action in action_list:
            new_board.apply_action(action)
            utility, _ = ab_mm(new_board, depth - 1, k, alpha, beta, curr_color.opponent, original_color)
            new_board.undo_action()
            if utility > best_utility:
                best_utility = utility
                best_action = action
            alpha = max(alpha, best_utility)
            if alpha >= beta:
                break
        return best_utility, best_action
    else:
        best_utility = float('inf')
        for action in action_list:
            new_board.apply_action(action)
            utility, _ = ab_mm(new_board, depth - 1, k, alpha, beta, curr_color.opponent, original_color)
            new_board.undo_action()
            if utility < best_utility:
                best_utility = utility
                best_action = action
            beta = min(beta, best_utility)
            if alpha >= beta:
                break
        return best_utility, best_action
