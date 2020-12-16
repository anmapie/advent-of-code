# --- Day 16: Ticket Translation ---
# As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed trip coming up is on a high-speed train. However, the train ticket you were given is in a language you don't understand. You should probably figure out what it says before you get to the train station after the next flight.

# Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and so you figure out the fields these tickets must have and the valid ranges for values in those fields.

# You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby tickets for the same train service (via the airport security cameras) together into a single document you can reference (your puzzle input).

# The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields in every ticket is named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).

# Each ticket is represented by a single line of comma-separated values. The values are the numbers on the ticket in the order they appear; every ticket has the same format. For example, consider this ticket:

# .--------------------------------------------------------.
# | ????: 101    ?????: 102   ??????????: 103     ???: 104 |
# |                                                        |
# | ??: 301  ??: 302             ???????: 303      ??????? |
# | ??: 401  ??: 402           ???? ????: 403    ????????? |
# '--------------------------------------------------------'
# Here, ? represents text in a language you don't understand. This ticket might be represented as 101,102,103,104,301,302,303,401,402,403; of course, the actual train tickets you're looking at are much more complicated. In any case, you've extracted just the numbers in such a way that the first number is always the same specific field, the second number is always a different specific field, and so on - you just don't know what each position actually means!

# Start by determining which tickets are completely invalid; these are tickets that contain values which aren't valid for any field. Ignore your ticket for now.

# For example, suppose you have the following notes:

# class: 1-3 or 5-7
# row: 6-11 or 33-44
# seat: 13-40 or 45-50

# your ticket:
# 7,1,14

# nearby tickets:
# 7,3,47
# 40,4,50
# 55,2,20
# 38,6,12
# It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

# Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?

# Your puzzle answer was 28882.

# --- Part Two ---
# Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use the remaining valid tickets to determine which field is which.

# Using the valid ranges for each field, determine what order the fields appear on the tickets. The order is consistent between all tickets: if seat is the third field, it is the third field on every ticket, including your ticket.

# For example, suppose you have the following notes:

# class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19

# your ticket:
# 11,12,13

# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9
# Based on the nearby tickets in the above example, the first position must be row, the second position must be class, and the third position must be seat; you can conclude that in your ticket, class is 12, row is 11, and seat is 13.

# Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?

# Your puzzle answer was 1429779530273.

import sys


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            fields_and_ranges, my_ticket, other_tickets = process_file(
                file_reader.readlines()
            )
            print(sum_invalid_ticket_values(other_tickets, fields_and_ranges))
            print(
                multiply_values_in_list(
                    find_departure_fields_for_my_ticket(
                        fields_and_ranges, my_ticket, other_tickets
                    )
                )
            )
    except Exception as error:
        print(error)


def process_file(raw_lines):
    fields_and_ranges = {}
    my_ticket = []
    other_tickets = []

    set_my_ticket = False
    set_other_tickets = False
    for line in raw_lines:
        if ":" in line:
            line_parts = line.split(": ")
            label = line_parts[0]

            if "your ticket" in label:
                set_my_ticket = True
            elif "nearby tickets" in label:
                set_other_tickets = True
            else:
                raw_ranges = line_parts[1].split(" or ")
                range_list = []
                for raw_range in raw_ranges:
                    range_min, range_max = tuple(raw_range.split("-"))
                    range_list.append((int(range_min), int(range_max) + 1))
                    fields_and_ranges[label] = range_list
        elif set_my_ticket:
            my_ticket = parse_ticket(line)
            set_my_ticket = False
        elif set_other_tickets:
            other_tickets.append(parse_ticket(line))

    return (fields_and_ranges, my_ticket, other_tickets)


def parse_ticket(raw_ticket):
    return [int(value) for value in raw_ticket.rstrip().split(",")]


def sum_invalid_ticket_values(tickets, fields_and_ranges):
    all_valid_values = build_valid_value_list(fields_and_ranges)
    invalid_values_sum = 0
    for ticket in tickets:
        for value in ticket:
            if not value in all_valid_values:
                invalid_values_sum += value
                break

    return invalid_values_sum


def is_ticket_invalid(valid_values, ticket):
    for value in ticket:
        if not value in valid_values:
            return True


def multiply_values_in_list(given_list):
    product = 1
    for value in given_list:
        product *= value
    return product


def find_departure_fields_for_my_ticket(fields_and_ranges, my_ticket, other_tickets):
    ordered_fields = build_field_order(fields_and_ranges, other_tickets)

    departure_field_values = []
    for index, field in enumerate(ordered_fields):
        if "departure" in field:
            departure_field_values.append(my_ticket[index])

    return departure_field_values


def build_valid_value_list(fields_and_ranges):
    valid_values = []
    for valid_ranges in fields_and_ranges.values():
        for valid_range in valid_ranges:
            for i in range(valid_range[0], valid_range[1]):
                valid_values.append(i)
    return set(valid_values)


def build_field_order(fields_and_ranges, tickets):
    possible_fields_for_positions = build_field_possibilities(
        fields_and_ranges, tickets
    )

    # reduce all the fields to a single possibility
    while not possible_fields_fully_reduced(possible_fields_for_positions):
        possible_fields_for_positions = reduce_possible_fields(
            possible_fields_for_positions
        )

    fields_in_order = []
    for i in range(0, len(possible_fields_for_positions.keys())):
        fields_in_order.append(possible_fields_for_positions[i][0])

    return fields_in_order


def build_field_possibilities(fields_and_ranges, tickets):
    all_valid_values = build_valid_value_list(fields_and_ranges)
    field_names = fields_and_ranges.keys()
    valid_fields_for_index = {}

    # pitch out all invalid tickets
    valid_tickets = [
        ticket for ticket in tickets if not is_ticket_invalid(all_valid_values, ticket)
    ]
    ticket_length = len(valid_tickets[0])

    for field in field_names:
        # print(field)
        valid_ranges = fields_and_ranges[field]
        # print(valid_ranges)
        for i in range(0, ticket_length):
            valid_for_field = True
            for ticket in valid_tickets:
                if not valid_for_field:
                    break
                value = ticket[i]
                if value_is_valid_for_field(value, valid_ranges):
                    continue
                valid_for_field = False
            if valid_for_field:
                if not i in valid_fields_for_index:
                    valid_fields_for_index[i] = []
                valid_fields_for_index[i].append(field)

    return valid_fields_for_index


def reduce_possible_fields(possible_fields_for_positions):
    field_position_count = len(possible_fields_for_positions.keys())
    for i in range(0, field_position_count):
        possible_fields_i = possible_fields_for_positions[i]
        for j in range(0, field_position_count):
            possible_fields_j = possible_fields_for_positions[j]
            list_diff = list(set(possible_fields_j) - set(possible_fields_i))
            # print(list_diff)
            if len(list_diff) > 0:
                possible_fields_for_positions[j] = list_diff

    return possible_fields_for_positions


def value_is_valid_for_field(value, valid_ranges):
    for valid_range in valid_ranges:
        if value in range(valid_range[0], valid_range[1]):
            return True

    return False


def possible_fields_fully_reduced(possible_fields_for_positions):
    for possible_fields in possible_fields_for_positions.values():
        if len(possible_fields) > 1:
            return False
    return True


if __name__ == "__main__":
    main()
