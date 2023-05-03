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
        # to avoid division by zero error
        if oppo_power == 0:
            return 0
        else:
            return my_power / oppo_power
