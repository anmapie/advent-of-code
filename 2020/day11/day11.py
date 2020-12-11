# --- Day 11: Seating System ---
# Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

# By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

# The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
# Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.
# Floor (.) never changes; seats don't move, and nobody sits on the floor.

# After one round of these rules, every seat in the example layout becomes occupied:

# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##
# After a second round, the seats with four or more occupied adjacent seats become empty again:

# #.LL.L#.##
# #LLLLLL.L#
# L.L.L..L..
# #LLL.LL.L#
# #.LL.LL.LL
# #.LLLL#.##
# ..L.L.....
# #LLLLLLLL#
# #.LLLLLL.L
# #.#LLLL.##
# This process continues for three more rounds:

# #.##.L#.##
# #L###LL.L#
# L.#.#..#..
# #L##.##.L#
# #.##.LL.LL
# #.###L#.##
# ..#.#.....
# #L######L#
# #.LL###L.L
# #.#L###.##
# #.#L.L#.##
# #LLL#LL.L#
# L.L.L..#..
# #LLL.##.L#
# #.LL.LL.LL
# #.LL#L#.##
# ..L.L.....
# #L#LLLL#L#
# #.LLLLLL.L
# #.#L#L#.##
# #.#L.L#.##
# #LLL#LL.L#
# L.#.L..#..
# #L##.##.L#
# #.#L.LL.LL
# #.#L#L#.##
# ..L.L.....
# #L#L##L#L#
# #.LLLLLL.L
# #.#L#L#.##
# At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

# Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?


# --- Part Two ---
# As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care about the first seat they can see in each of those eight directions!

# Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions. For example, the empty seat below would see eight occupied seats:

# .......#.
# ...#.....
# .#.......
# .........
# ..#L....#
# ....#....
# .........
# #........
# ...#.....
# The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

# .............
# .L.L.#.#.#.#.
# .............
# The empty seat below would see no occupied seats:

# .##.##.
# #.#.#.#
# ##...##
# ...L...
# ##...##
# #.#.#.#
# .##.##.

# Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.

# Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.

# Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?


import sys

ADJACENT_DIRECTION_MODS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
]

OCCUPIED_SEAT_TOLERANCE_FOR_RULE_VERSION = {
    1: 4,
    2: 5,
}


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            seat_map = [list(line.rstrip()) for line in file_reader.readlines()]
            print(count_all_occupied_seats(get_stable_seat_map(seat_map, 1)))
            print(count_all_occupied_seats(get_stable_seat_map(seat_map, 2)))
    except Exception as error:
        print(error)


# stable seat map based on some version of the seating rules
def get_stable_seat_map(seat_map, rule_version):
    # we want to keep running the rules on the map until it's stable (no seats change during a round of rule application)
    # so we'll start our loop control (change count) with a non-zero value
    change_count = 42
    next_seat_map = seat_map

    while change_count != 0:
        next_seat_map, change_count = apply_rules_to_seat_map(
            next_seat_map, rule_version
        )

    return next_seat_map


def count_all_occupied_seats(seat_map):
    occupied_count = 0
    for row in seat_map:
        for seat in row:
            if seat == "#":
                occupied_count += 1

    return occupied_count


# Part 1 Rules:
# Rule 1: if a seat is empty ('L') and all seats adjacent to it are empty (or floor), the seat becomes occupied
# Rule 2: if a seat is occupied ('#') and four or more seats adjacent to it are occupied, it becomes empty
# Rule 3: the floor never changes (good ol' floor)
# ---
# Part 2 Rules:
# Rule 0: 'line of sight' -> next seat after a set of floor spaces
# Rule 1: if a seat is empty ('L') and all seats in its line of sight in all 8 directions to it are empty, the seat becomes occupied
# Rule 2: if a seat is occupied ('#') and five or more seats in its line of sight occupied, it becomes empty
# Rule 3: the floor never changes (u never let me down floor)
def apply_rules_to_seat_map(seat_map, rule_version):
    new_seat_map = []
    change_count = 0
    for row_index, row in enumerate(seat_map):
        new_row = []
        for seat_index, seat in enumerate(row):
            if seat == ".":
                # seat is floor
                # and floor is forever floor (floor4lyfe bb)
                new_row.append(".")
            else:
                # occupied seat tolerance -> max relevant seats that can be occupied in relation to an empty seat
                occupied_seat_tolerance = OCCUPIED_SEAT_TOLERANCE_FOR_RULE_VERSION[
                    rule_version
                ]

                # count occupied seats that are relevant to this seat based on the rule version
                relevant_occupied_seats = 0

                if rule_version == 1:
                    relevant_occupied_seats = count_occupied_adjacent_seats(
                        seat_map, row_index, seat_index
                    )
                if rule_version == 2:
                    relevant_occupied_seats = count_occupied_line_of_sight_seats(
                        seat_map, row_index, seat_index
                    )

                if seat == "L":
                    # if all adjacent seats are empty, switch seat to occupied
                    if relevant_occupied_seats == 0:
                        new_row.append("#")
                        change_count += 1
                    else:
                        new_row.append("L")
                elif seat == "#":
                    # if four or more adjacent seats are occupied, switch to empty
                    if relevant_occupied_seats >= occupied_seat_tolerance:
                        new_row.append("L")
                        change_count += 1
                    else:
                        new_row.append("#")

        new_seat_map.append(new_row)

    return (new_seat_map, change_count)


def count_occupied_adjacent_seats(seat_map, row_index, seat_index):
    occupied_count = 0

    for mod in ADJACENT_DIRECTION_MODS:
        row_mod, seat_mod = mod
        if seat_is_occupied(seat_map, row_index + row_mod, seat_index + seat_mod):
            occupied_count += 1

    # that's what it's all about!
    return occupied_count


def count_occupied_line_of_sight_seats(seat_map, row_index, seat_index):
    occupied_count = 0

    for mod in ADJACENT_DIRECTION_MODS:
        if seat_in_line_of_site_is_occupied(seat_map, row_index, seat_index, mod):
            occupied_count += 1

    return occupied_count


def seat_in_line_of_site_is_occupied(seat_map, row_index, seat_index, direction_mod):
    row_mod, seat_mod = direction_mod
    next_row_index = row_index + row_mod
    next_seat_index = seat_index + seat_mod
    # walk the entire line of sight of the seat until we hit another seat or run off the map
    while not seat_is_out_of_bounds(seat_map, next_row_index, next_seat_index):
        # if it's floor, keep going baby
        if seat_map[next_row_index][next_seat_index] == ".":
            next_row_index += row_mod
            next_seat_index += seat_mod
        else:
            return seat_is_occupied(seat_map, next_row_index, next_seat_index)

    # overran the map -> no occupied adjacent seats
    return False


def seat_is_occupied(seat_map, row_index, seat_index):
    if seat_is_out_of_bounds(seat_map, row_index, seat_index):
        return False
    return seat_map[row_index][seat_index] == "#"


def seat_is_out_of_bounds(seat_map, row_index, seat_index):
    return (
        row_index < 0
        or seat_index < 0
        or row_index >= len(seat_map)
        or seat_index >= len(seat_map[0])
    )


if __name__ == "__main__":
    main()
