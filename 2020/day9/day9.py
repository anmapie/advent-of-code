# --- Day 9: Encoding Error ---
# With your neighbor happily enjoying their video game, you turn your attention to an open data port on the little screen in the seat in front of you.

# Though the port is non-standard, you manage to connect it to your computer through the clever use of several paperclips. Upon connection, the port outputs a series of numbers (your puzzle input).

# The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which, conveniently for you, is an old cypher with an important weakness.

# XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should be the sum of any two of the 25 immediately previous numbers. The two numbers will have different values, and there might be more than one such pair.

# For example, suppose your preamble consists of the numbers 1 through 25 in a random order. To be valid, the next number must be the sum of two of those numbers:

# 26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
# 49 would be a valid next number, as it is the sum of 24 and 25.
# 100 would not be valid; no two of the previous 25 numbers sum to 100.
# 50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be different.
# Suppose the 26th number is 45, and the first number (no longer an option, as it is more than 25 numbers ago) was 20. Now, for the next number to be valid, there needs to be some pair of numbers among 1-19, 21-25, or 45 that add up to it:

# 26 would still be a valid next number, as 1 and 25 are still within the previous 25 numbers.
# 65 would not be valid, as no two of the available numbers sum to it.
# 64 and 66 would both be valid, as they are the result of 19+45 and 21+45 respectively.

# The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?

# --- Part Two ---
# The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a contiguous set of at least two numbers in your list which sum to the invalid number from step 1.

# To find the encryption weakness, add together the smallest and largest number in this contiguous range.

import sys

TEST_SEQUENCE_LENGTH = 5  # used for test1.txt
PROBLEM_SEQUENCE_LENGTH = 25  # used for test2.txt


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            numbers = [int(line) for line in file_reader.readlines()]
            print(find_first_invalid_number(numbers, PROBLEM_SEQUENCE_LENGTH))
            print(break_xmas_encryption(numbers, PROBLEM_SEQUENCE_LENGTH))
    except Exception as error:
        print(error)


def break_xmas_encryption(numbers, sequence_length):
    # step 1: find the first invalid number
    # (good thing we did that in part 1, eh?)
    invalid_number = find_first_invalid_number(numbers, sequence_length)

    # step 2: find the first continuous sub-list of numbers that sum to invalid number
    continuous_numbers = find_continuous_sequence_for_target_sum(
        numbers, invalid_number
    )

    # step 3 return the sum of the min and max of the sub-list from step 2
    return min(continuous_numbers) + max(continuous_numbers)


# first invalid number == first number that is not the sum of two numbers in the
# immediately preceding sequence of sequence_length numbers
def find_first_invalid_number(numbers, sequence_length):
    # keep track of where we are in the list, so we can always grab the
    # sequence_length list of numbers immediately preceding the candidate
    offset = 0

    # the first sequence_length numbers do not need to be considered
    for candidate_number in numbers[sequence_length:]:
        sequence = numbers[offset : sequence_length + offset]
        candidate_is_valid = False

        # sum every number with ever other number (sliding up the list)
        # until we find two numbers that sum to the candidate number
        for i in range(sequence_length):
            sequence_i = sequence[i]
            if sequence_i > candidate_number:
                continue
            for j in range(i + 1, sequence_length):
                sequence_j = sequence[j]
                if sequence_i + sequence_j == candidate_number:
                    candidate_is_valid = True
                    break

        # no two numbers in the sequence could add up to the candidate?
        # we've got our invalid number; return it
        if not candidate_is_valid:
            return candidate_number

        # move on to the next candidate number
        offset += 1


# return the sub-list of continuous numbers from a larger list that
# add up to the given target_sum
def find_continuous_sequence_for_target_sum(numbers, target_sum):
    for i in range(len(numbers)):
        running_sum = 0

        # keep track of the start + end of our sub-list
        start_index = i
        end_index = i

        # sum numbers until we meet or exceed the target, or can't sum any more numbers
        while running_sum < target_sum and end_index < len(numbers[start_index:]):
            running_sum += numbers[end_index]
            end_index += 1

        if running_sum == target_sum:
            return numbers[start_index:end_index]

    return []


if __name__ == "__main__":
    main()
