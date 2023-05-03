from referee.game import Board, PlayerColor


def evaluate(board: Board, color: PlayerColor) -> float:
    if board.game_over:
        if board.winner_color == color:
            return float('inf')
        else:
            return float('-inf')
    else:
        my_power = board._color_power(color)
        oppo_power = board._color_power(color.opponent)
        my_cell = len(board._player_cells(color))
        oppo_cell = len(board._player_cells(color.opponent))
        # to avoid division by zero error
        if oppo_cell == 0:
            return 0
        else:
            return 0.34 * (my_power / oppo_power) + my_cell / oppo_cell
