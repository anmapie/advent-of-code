import sys

FORWARD = "F"
LEFT = "L"
RIGHT = "R"
NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"
CARDINAL_DIRECTIONS = [NORTH, EAST, SOUTH, WEST]


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            directions_list = [
                format_direction(line.rstrip()) for line in file_reader.readlines()
            ]
            print(calculate_manhattan_distance_of_route(directions_list))
            print(calculate_manhattan_distance_with_waypoint(directions_list))
    except Exception as error:
        # print(error)
        raise


def format_direction(direction):
    # direction format <char><int>
    # examples: F10, R90, N3
    # return as tuple
    return (direction[0], int(direction[1:]))


# Manhattan distance: sum of the absolute values of its east/west position and its north/south position
def calculate_manhattan_distance_of_route(directions_list):
    ship_position = (0, 0, EAST)
    # direction format <char><unit>
    # examples: F10, R90, N3
    for direction, unit in directions_list:
        ship_position = move_ship(ship_position, direction, unit)

    return abs(ship_position[0]) + abs(ship_position[1])


def calculate_manhattan_distance_with_waypoint(directions_list):
    ship_position = (0, 0, EAST)
    waypoint_position = ((10, EAST), (1, NORTH))

    for direction, unit in directions_list:
        print(f"{ship_position} - {waypoint_position}")
        ship_position, waypoint_position = move_ship_and_waypoint(
            ship_position, waypoint_position, direction, unit
        )

    return abs(ship_position[0]) + abs(ship_position[1])


# position -> (west/east, north/south, facing)
def move_ship(curr_position, direction, units):
    if direction == FORWARD:
        ship_facing = curr_position[-1]
        return move_ship_in_direction(curr_position, ship_facing, units)
    if direction == RIGHT or direction == LEFT:
        return turn_ship(curr_position, direction, units)

    return move_ship_in_direction(curr_position, direction, units)


def move_ship_in_direction(curr_position, direction, units):
    horizontal, vertical, facing = curr_position

    if direction == NORTH:
        vertical += units
    elif direction == SOUTH:
        vertical -= units
    elif direction == EAST:
        horizontal += units
    elif direction == WEST:
        horizontal -= units

    return (horizontal, vertical, facing)


def move_waypoint_in_direction(curr_position, direction, units):
    waypoint_horizontal, waypoint_vertical = curr_position

    if direction == NORTH:
        new_value = waypoint_vertical[0] + units
        new_direction = waypoint_vertical[1]

        if new_direction == SOUTH and new_value >= 0:
          new_direction = NORTH
        
        return (
            waypoint_horizontal,
            (new_value, new_direction),
        )
    if direction == SOUTH:
        new_value = waypoint_vertical[0] - units
        new_direction = waypoint_vertical[1]

        if new_direction == NORTH and new_value < 0:
          new_direction = SOUTH
        
        return (
            waypoint_horizontal,
            (new_value, new_direction),
        )
    if direction == EAST:
        new_value = waypoint_horizontal[0] + units
        new_direction = waypoint_horizontal[1]

        if new_direction == WEST and new_value >= 0:
            new_direction = EAST
        
        return (
            (new_value, new_direction),
            waypoint_vertical,
        )
    if direction == WEST:
        new_value = waypoint_horizontal[0] - units
        new_direction = waypoint_horizontal[1]

        if new_direction == EAST and new_value < 0:
            new_direction = WEST
        return (
            (new_value, new_direction),
            waypoint_vertical,
        )


def turn_ship(curr_position, direction, units):
    ship_facing = curr_position[-1]
    curr_direction_index = CARDINAL_DIRECTIONS.index(ship_facing)

    # turn units are in increments of 90
    # so we can divide by 90 to get the number of different directions the ship will turn
    turn_count = units / 90

    if direction == LEFT:
        curr_direction_index = (curr_direction_index - turn_count) % len(
            CARDINAL_DIRECTIONS
        )
    else:
        curr_direction_index = (curr_direction_index + turn_count) % len(
            CARDINAL_DIRECTIONS
        )

    return (
        curr_position[0],
        curr_position[1],
        CARDINAL_DIRECTIONS[int(curr_direction_index)],
    )


def move_ship_and_waypoint(ship_position, waypoint_position, direction, units):
    if direction == FORWARD:
        # ship is going to move twice - once horizontal and once vertical
        # in relationship to the waypoint (direction unit * waypoint unit)
        waypoint_horizontal, waypoint_vertical = waypoint_position
        next_ship_position = move_ship_in_direction(
            ship_position, waypoint_horizontal[1], abs(units * waypoint_horizontal[0])
        )
        next_ship_position = move_ship_in_direction(
            next_ship_position, waypoint_vertical[1], abs(units * waypoint_vertical[0])
        )
        return (next_ship_position, waypoint_position)
    if direction == LEFT or direction == RIGHT:
        return (ship_position, rotate_waypoint(waypoint_position, direction, units))
    else:
        return (
            ship_position,
            move_waypoint_in_direction(waypoint_position, direction, units),
        )


def rotate_waypoint(waypoint_position, direction, units):
    # turn both parts of the waypoint
    waypoint_position_1 = turn_waypoint(waypoint_position[0], direction, units)
    waypoint_position_2 = turn_waypoint(waypoint_position[1], direction, units)

    # directions in this system are ordered - (horizontal, vertical)
    # ensure these directions are returned in that order
    if waypoint_position_1[1] == EAST or waypoint_position_1[1] == WEST:
        return (waypoint_position_1, waypoint_position_2)
    return (waypoint_position_2, waypoint_position_1)


def turn_waypoint(waypoint_position_segment, direction, units):
    waypoint_segment_facing = waypoint_position_segment[-1]
    curr_direction_index = CARDINAL_DIRECTIONS.index(waypoint_segment_facing)

    # turn units are in increments of 90
    # so we can divide by 90 to get the number of different directions the ship will turn
    turn_count = units / 90

    if direction == LEFT:
        curr_direction_index = (curr_direction_index - turn_count) % len(
            CARDINAL_DIRECTIONS
        )
    else:
        curr_direction_index = (curr_direction_index + turn_count) % len(
            CARDINAL_DIRECTIONS
        )
    
    direction_value = waypoint_position_segment[0]
    new_direction = CARDINAL_DIRECTIONS[int(curr_direction_index)]

    # use correct sign for the direction
    # N/E - positive
    # W/S - negative
    if new_direction == NORTH or new_direction == EAST:
      direction_value = abs(direction_value)
    elif  direction_value > 0:
      direction_value *= -1

    return (
        direction_value,
        CARDINAL_DIRECTIONS[int(curr_direction_index)],
    )


if __name__ == "__main__":
    main()
