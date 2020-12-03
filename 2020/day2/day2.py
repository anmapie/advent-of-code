# --- Day 2: Password Philosophy ---
# Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here is via toboggan.

# The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our computers; we can't log in!" You ask if you can take a look.

# Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the Official Toboggan Corporate Policy that was in effect when they were chosen.

# To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted database) and the corporate policy when that password was set.

# For example, suppose you have the following list:

# 1-3 a: abcde
# 1-3 b: cdefg
# 2-9 c: ccccccccc
# Each line gives the password policy and then the password.
# The password policy indicates the lowest and highest number of times a given letter must appear for the password to be valid.
# For example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.

# In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b, but needs at least 1.
# The first and third passwords are valid: they contain one a or nine c, both within the limits of their respective policies.

# How many passwords are valid according to their policies?
import sys


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            passwords = [parse_input_line(line) for line in file_reader.readlines()]
            print(valid_char_count_password_count(passwords))
            print(valid_postion_password_count(passwords))
    except Exception as error:
        print(error)


def parse_input_line(line):
    tokens = line.split()

    # first token: int-int (part 1: min chars-max chars) OR (part 2: char position-char position)
    char_min, char_max = tuple([int(i) for i in tokens[0].split("-")])

    # second token: target char (followed by ':', which we'll ignore)
    target_char = tokens[1][0]

    # third token: actual password
    password = tokens[2]

    return (char_min, char_max, target_char, password)


def valid_char_count_password_count(password_tuples):
    valid_passwords = 0
    for password_tuple in password_tuples:
        char_min, char_max, target_char, password = password_tuple
        target_char_count = password.count(target_char)
        if target_char_count >= char_min and target_char_count <= char_max:
            valid_passwords += 1
    return valid_passwords


def valid_postion_password_count(password_tuples):
    valid_passwords = 0
    for password_tuple in password_tuples:
        if is_valid_position_password(password_tuple):
            valid_passwords += 1

    return valid_passwords


def is_valid_position_password(password_tuple):
    target_position_1, target_position_2, target_char, password = password_tuple
    # password is valid IFF:
    # the target char occurs in target position 1 or target position 2
    # and does NOT occur in both position 1 and position 2
    # any other occurrences of the char are irrelevant
    # given target positions are not zero indexed, so we need to offset by 1
    if password[target_position_1 - 1] == target_char:
        return password[target_position_2 - 1] != target_char

    return password[target_position_2 - 1] == target_char


if __name__ == "__main__":
    main()
