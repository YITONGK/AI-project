from referee.game import Action, HexPos, HexDir
from referee.game.board import CellState


def spread(temp_state: dict[HexPos, CellState], action: Action) -> None:
    cell = action.cell
    curr_cell = cell
    direction = action.direction
    color = temp_state[cell].player
    power = temp_state[cell].power
    cell_to_update = []
    max_power = 7
    # in this function we don't make edition on original board, so make a copy
    # new_board = temp_state.copy()
    # the value of power of the current token determines how many spreads to go
    while power > 0:
        curr_cell = check_boundary(move(curr_cell, direction))
        cell_to_update.append(curr_cell)
        power -= 1
    # clear the seed token from the copied board
    #new_board.pop(cell)
    temp_state.pop(cell)
    # update the spread tokens onto our copied board
    for i in range(len(cell_to_update)):
        if cell_to_update[i] not in temp_state.keys():
            temp_state[(cell_to_update[i])] = (color, 1)
        else:
            # the current coordinate is not empty
            new_power = temp_state[(cell_to_update[i])].power + 1
            temp_state[(cell_to_update[i])] = CellState(color, new_power)
            # check whether the power exceeds 6, if so the token will disappear
            if new_power == max_power:
                temp_state.pop(cell_to_update[i])
    #     if cell_to_update[i] not in new_board.keys():
    #         new_board[(cell_to_update[i])] = (color, 1)
    #     else:
    #         # the current coordinate is not empty
    #         new_power = new_board[(cell_to_update[i])].power + 1
    #         new_board[(cell_to_update[i])] = CellState(color, new_power)
    #         # check whether the power exceeds 6, if so the token will disappear
    #         if new_power == max_power:
    #             new_board.pop(cell_to_update[i])
    # return new_board


# given a coordinate and a moving direction, get the new coordinate
def move(cell: HexPos, direction: HexDir) -> HexPos:
    match direction:
        case HexDir.Up:
            return cell.__add__(HexDir.Up)
        case HexDir.Down:
            return cell.__add__(HexDir.Down)
        case HexDir.UpLeft:
            return cell.__add__(HexDir.UpLeft)
        case HexDir.DownLeft:
            return cell.__add__(HexDir.DownLeft)
        case HexDir.UpRight:
            return cell.__add__(HexDir.UpRight)
        case HexDir.DownRight:
            return cell.__add__(HexDir.DownRight)

# this function is used to check after moving, whether the coordinate is "out of board"
# as we want our tokens have coordinates where r and q are in range [0, 6]
def check_boundary(cell: HexPos) -> HexPos:
    upper_boundary = 6
    lower_boundary = 0
    r = cell.r
    q = cell.q
    # if after moving, coordinate value is 7, then change it to 0,
    # if coordinate value is -1, then change it to 6
    if r > upper_boundary:
        r = lower_boundary
    if r < lower_boundary:
        r = upper_boundary
    if q > upper_boundary:
        q = lower_boundary
    if q < lower_boundary:
        q = upper_boundary
    return HexPos(r, q)