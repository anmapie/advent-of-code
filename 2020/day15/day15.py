# --- Day 15: Rambunctious Recitation ---
# You catch the airport shuttle and try to book a new flight to your vacation island. Due to the storm, all direct flights have been cancelled, but a route is available to get around the storm. You take it.

# While you wait for your flight, you decide to check in with the Elves back at the North Pole. They're playing a memory game and are ever so excited to explain the rules!

# In this game, the players take turns saying numbers. They begin by taking turns reading from a list of starting numbers (your puzzle input). Then, each turn consists of considering the most recently spoken number:

# If that was the first time the number has been spoken, the current player says 0.
# Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from when it was previously spoken.
# So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the last number is new) or an age (if the last number is a repeat).

# For example, suppose the starting numbers are 0,3,6:

# Turn 1: The 1st number spoken is a starting number, 0.
# Turn 2: The 2nd number spoken is a starting number, 3.
# Turn 3: The 3rd number spoken is a starting number, 6.
# Turn 4: Now, consider the last number spoken, 6. Since that was the first time the number had been spoken, the 4th number spoken is 0.
# Turn 5: Next, again consider the last number spoken, 0. Since it had been spoken before, the next number to speak is the difference between the turn number when it was last spoken (the previous turn, 4) and the turn number of the time it was most recently spoken before then (turn 1). Thus, the 5th number spoken is 4 - 1, 3.
# Turn 6: The last number spoken, 3 had also been spoken before, most recently on turns 5 and 2. So, the 6th number spoken is 5 - 2, 3.
# Turn 7: Since 3 was just spoken twice in a row, and the last two turns are 1 turn apart, the 7th number spoken is 1.
# Turn 8: Since 1 is new, the 8th number spoken is 0.
# Turn 9: 0 was last spoken on turns 8 and 4, so the 9th number spoken is the difference between them, 4.
# Turn 10: 4 is new, so the 10th number spoken is 0.
# (The game ends when the Elves get sick of playing or dinner is ready, whichever comes first.)

# Their question for you is: what will be the 2020th number spoken? In the example above, the 2020th number spoken will be 436.

# Here are a few more examples:

# Given the starting numbers 1,3,2, the 2020th number spoken is 1.
# Given the starting numbers 2,1,3, the 2020th number spoken is 10.
# Given the starting numbers 1,2,3, the 2020th number spoken is 27.
# Given the starting numbers 2,3,1, the 2020th number spoken is 78.
# Given the starting numbers 3,2,1, the 2020th number spoken is 438.
# Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
# Given your starting numbers, what will be the 2020th number spoken?

# --- Part Two ---
# Impressed, the Elves issue you a challenge: determine the 30000000th number spoken. For example, given the same starting numbers as above:

# Given 0,3,6, the 30000000th number spoken is 175594.
# Given 1,3,2, the 30000000th number spoken is 2578.
# Given 2,1,3, the 30000000th number spoken is 3544142.
# Given 1,2,3, the 30000000th number spoken is 261214.
# Given 2,3,1, the 30000000th number spoken is 6895259.
# Given 3,2,1, the 30000000th number spoken is 18.
# Given 3,1,2, the 30000000th number spoken is 362.
# Given your starting numbers, what will be the 30000000th number spoken?

import sys


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            starting_numbers = [int(line) for line in file_reader.readline().split(",")]
            print(find_nth_number(2020, starting_numbers))
            print(find_nth_number(30_000_000, starting_numbers))
    except Exception as error:
        print(error)


# rulez of this crazy game:
# 1. take in a list of starting numbers; these will be the first numbers spoken in the game (and hopefully unique)
# 2. once the starting numbers are spoken, you speak 0 if the next number had not been previously spoken before
# 3. if a number has been spoken before, the next number spoken is the difference between the two most recent turns that number was spoken
# (e.g. the previous turn and the turn it was spoken before)
# 4. repeat ad naseum
# find the nth number spoken in such a sequence
def find_nth_number(n, starting_numbers):
    numbers_spoken_and_last_turns = {}

    # populate all starting numbers + the turn they were spoken in our dict
    # hold off the last number - we'll use it to kick off our remaining turn loop
    for index, number in enumerate(starting_numbers[:-1]):
        numbers_spoken_and_last_turns[number] = index + 1

    # next spoken -> last in starting list
    next_spoken_number = starting_numbers[-1]
    for i in range(len(starting_numbers), n):
        if next_spoken_number in numbers_spoken_and_last_turns:
            # number spoken before? next number will be the difference between this turn and the last turn it was spoken
            previous_turn_spoken = numbers_spoken_and_last_turns[next_spoken_number]
            numbers_spoken_and_last_turns[next_spoken_number] = i
            next_spoken_number = i - previous_turn_spoken
        else:
            # number never spoken before? next number will be 0
            numbers_spoken_and_last_turns[next_spoken_number] = i
            next_spoken_number = 0

    return next_spoken_number


if __name__ == "__main__":
    main()
