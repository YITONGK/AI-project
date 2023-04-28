from referee.game import Action, HexPos, HexDir


def spread(temp_state: dict, action: Action):
    curr_cell = action.cell
    direction = action.direction
    color = temp_state[curr_cell].player
    power = temp_state[curr_cell].power
    cell_to_update = []


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