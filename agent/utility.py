from referee.game import Board, PlayerColor


def evaluate(board: Board, color: PlayerColor) -> float:
    if board.game_over:
        # if we will win, maximise utility value
        if board.winner_color == color:
            return float('inf')
        # if opponent is going to win, minimise utility value
        else:
            return float('-inf')
    else:
        # get the total power and total number of cells of both sides from the board
        my_power = board._color_power(color)
        oppo_power = board._color_power(color.opponent)
        num_my_cells = len(board._player_cells(color))
        num_oppo_cells = len(board._player_cells(color.opponent))
        # to avoid division by zero error
        if num_oppo_cells == 0:
            return 0
        else:
            return (my_power / oppo_power) + 3 * (num_my_cells / num_oppo_cells)
