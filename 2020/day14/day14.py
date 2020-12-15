# --- Day 14: Docking Data ---
# As your ferry approaches the sea port, the captain asks for your help again. The computer system that runs this port isn't compatible with the docking program on the ferry, so the docking parameters aren't being correctly initialized in the docking program's memory.

# After a brief inspection, you discover that the sea port's computer system uses a strange bitmask system in its initialization program. Although you don't have the correct decoder chip handy, you can emulate it in software!

# The initialization program (your puzzle input) can either update the bitmask or write a value to memory. Values and memory addresses are both 36-bit unsigned integers. For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory address 8.

# The bitmask is always given as a string of 36 bits, written with the most significant bit (representing 2^35) on the left and the least significant bit (2^0, that is, the 1s bit) on the right. The current bitmask is applied to values immediately before they are written to memory: a 0 or 1 overwrites the corresponding bit in the value, while an X leaves the bit in the value unchanged.

# For example, consider the following program:

# mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# mem[8] = 11
# mem[7] = 101
# mem[8] = 0
# This program starts by specifying a bitmask (mask = ....). The mask it specifies will overwrite two bits in every written value: the 2s bit is overwritten with 0, and the 64s bit is overwritten with 1.

# The program then attempts to write the value 11 to memory address 8. By expanding everything out to individual bits, the mask is applied as follows:

# value:  000000000000000000000000000000001011  (decimal 11)
# mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# result: 000000000000000000000000000001001001  (decimal 73)
# So, because of the mask, the value 73 is written to memory address 8 instead. Then, the program tries to write 101 to address 7:

# value:  000000000000000000000000000001100101  (decimal 101)
# mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# result: 000000000000000000000000000001100101  (decimal 101)
# This time, the mask has no effect, as the bits it overwrote were already the values the mask tried to set. Finally, the program tries to write 0 to address 8:

# value:  000000000000000000000000000000000000  (decimal 0)
# mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# result: 000000000000000000000000000001000000  (decimal 64)
# 64 is written to address 8 instead, overwriting the value that was there previously.

# To initialize your ferry's docking program, you need the sum of all values left in memory after the initialization program completes. (The entire 36-bit address space begins initialized to the value 0 at every address.) In the above example, only two values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.

# Execute the initialization program. What is the sum of all values left in memory after it completes?

# --- Part Two ---
# For some reason, the sea port's computer system still can't communicate with your ferry's docking program. It must be using version 2 of the decoder chip!

# A version 2 decoder chip doesn't modify the values being written at all. Instead, it acts as a memory address decoder. Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding bit of the destination memory address in the following way:

# If the bitmask bit is 0, the corresponding memory address bit is unchanged.
# If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
# If the bitmask bit is X, the corresponding memory address bit is floating.
# A floating bit is not connected to anything and instead fluctuates unpredictably. In practice, this means the floating bits will take on all possible values, potentially causing many memory addresses to be written all at once!

# For example, consider the following program:

# mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1
# When this program goes to write to memory address 42, it first applies the bitmask:

# address: 000000000000000000000000000000101010  (decimal 42)
# mask:    000000000000000000000000000000X1001X
# result:  000000000000000000000000000000X1101X
# After applying the mask, four bits are overwritten, three of which are different, and two of which are floating. Floating bits take on every possible combination of values; with two floating bits, four actual memory addresses are written:

# 000000000000000000000000000000011010  (decimal 26)
# 000000000000000000000000000000011011  (decimal 27)
# 000000000000000000000000000000111010  (decimal 58)
# 000000000000000000000000000000111011  (decimal 59)
# Next, the program is about to write to memory address 26 with a different bitmask:

# address: 000000000000000000000000000000011010  (decimal 26)
# mask:    00000000000000000000000000000000X0XX
# result:  00000000000000000000000000000001X0XX
# This results in an address with three floating bits, causing writes to eight memory addresses:

# 000000000000000000000000000000010000  (decimal 16)
# 000000000000000000000000000000010001  (decimal 17)
# 000000000000000000000000000000010010  (decimal 18)
# 000000000000000000000000000000010011  (decimal 19)
# 000000000000000000000000000000011000  (decimal 24)
# 000000000000000000000000000000011001  (decimal 25)
# 000000000000000000000000000000011010  (decimal 26)
# 000000000000000000000000000000011011  (decimal 27)
# The entire 36-bit address space still begins initialized to the value 0 at every address, and you still need the sum of all values left in memory at the end of the program. In this example, the sum is 208.

# Execute the initialization program using an emulator for a version 2 decoder chip. What is the sum of all values left in memory after it completes?

import copy
import re
import sys

# we're working with 36-bit binary
BIT_OFFSET = 35


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            raw_instructions = file_reader.readlines()
            # part 1: sum all values written to memory after the instructions are processed applying bitmasks to values
            print(
                sum_values_in_memory(
                    process_instructions_masking_value(raw_instructions)
                )
            )

            # part 2: sum all values written to memory after the instructions are processed applying bitmasks to memory addresses
            print(
                sum_values_in_memory(
                    process_instructions_masking_address(raw_instructions)
                )
            )

    except Exception as error:
        print(error)
        raise


# build a memory map given a set of instructions in the format
# mask = <string>
# mem[<int>] = <int>
# bitmasks alter the VALUE being written to memory in this version
def process_instructions_masking_value(instructions):
    bitmask = []
    memory = {}
    for line in instructions:
        line_parts = line.rstrip().split("= ")

        if line_parts[0].startswith("mask"):
            bitmask = []
            for index, char in enumerate(line_parts[1]):
                # when masking values, we ignore any "X" in the bitmask
                if char != "X":
                    bitmask.append((index, char))
        elif line_parts[0].startswith("mem"):
            memory_address, binary_value = parse_memory_address_and_value(line_parts)
            memory[memory_address] = apply_mask_to_value(bitmask, binary_value)

    return memory


# build a memory map given a set of instructions in the format
# mask = <string>
# mem[<int>] = <int>
# bitmasks alter the MEMORY ADDRESS being written to in this version
# when an address is masked, it may contain "unstable" bits, represented by "X"
# these bits can be either 1 or 0 - write values to all possible permutations of the address
def process_instructions_masking_address(instructions):
    bitmask_stable_bits = []
    bitmask_unstable_bits = []
    memory = {}
    for line in instructions:
        line_parts = line.rstrip().split("= ")

        if line_parts[0].startswith("mask"):
            bitmask_stable_bits = []
            bitmask_unstable_bits = []
            for index, char in enumerate(line_parts[1]):
                # separate our "unstable" bits; store just their 'index' in the binary string (0 is the far right)
                if char == "X":
                    bitmask_unstable_bits.append(BIT_OFFSET - index)
                # in this bit mask, 1's can flip 0's; 0's do nothing
                elif char == "1":
                    bitmask_stable_bits.append((index, char))
        elif line_parts[0].startswith("mem"):
            memory_address, binary_value = parse_memory_address_and_value(line_parts)
            possible_memory_addresses = apply_mask_to_address(
                bitmask_stable_bits, bitmask_unstable_bits, memory_address
            )
            for address in possible_memory_addresses:
                memory[address] = binary_value

    return memory


def parse_memory_address_and_value(raw_memory_instruction):
    memory_address = int(re.findall(r"\d+", raw_memory_instruction[0])[0])
    binary_value = int_to_binary_string(raw_memory_instruction[1])
    return (memory_address, binary_value)


def int_to_binary_string(int_to_convert):
    return "{0:b}".format(int(int_to_convert)).zfill(36)


def apply_mask_to_value(bitmask, binary_value):
    transformed_value = list(copy.copy(binary_value))
    for index, value in bitmask:
        transformed_value[index] = value

    return "".join(transformed_value)


def apply_mask_to_address(bitmask_stable_bits, bitmask_unstable_bits, memory_address):
    possible_addresses = []
    # convert the address to binary string
    transformed_address = int_to_binary_string(memory_address)

    # transform the address with the stable bits (convert to list so we can continue to mess w/ chars)
    transformed_address = list(
        apply_mask_to_value(bitmask_stable_bits, transformed_address)
    )

    # find all possible address permutations created by the unstable bits
    # first, switch all unstable bits to one (max possible address value)
    for unstable_bit in bitmask_unstable_bits:
        transformed_address[BIT_OFFSET - unstable_bit] = "1"

    # these are our seed addresses: all unstable bits switched to 1, max unstable bit flipped to 0
    # (convert to ints so the they work with our problem)
    max_bit_index = BIT_OFFSET - bitmask_unstable_bits[0]
    seed_address_string = "".join(transformed_address)
    seed_address_1 = int(seed_address_string, 2)
    seed_address_2 = int(
        "".join(
            seed_address_string[0:max_bit_index]
            + "0"
            + seed_address_string[max_bit_index + 1 :]
        ),
        2,
    )

    # append the seed addresses to the list - they are also possibilities
    possible_addresses += [seed_address_1, seed_address_2]

    # calculate all possible addresses that can originate from the seed addresses
    possible_addresses += calculate_possible_addresses_from_seed(
        bitmask_unstable_bits[1:], seed_address_1
    ) + calculate_possible_addresses_from_seed(
        bitmask_unstable_bits[1:], seed_address_2
    )

    print(possible_addresses)
    return possible_addresses


# recursive sliding subtraction -> continually subtract (2^m + 2^n + ...) where m and n are the locations
# in the binary string of the unstable bits in the bit mask - we'll do this for every value in in the
# unstable bitmask, reducing the size of the list by one for each iteration
def calculate_possible_addresses_from_seed(bitmask_unstable_bits, seed_address):
    possible_addresses = []
    for list_index, unstable_bit_location in enumerate(bitmask_unstable_bits):
        # subtract 2^(current unstable bit) and add to the possible addresses
        next_seed_address = seed_address - (2 ** unstable_bit_location)
        possible_addresses.append(next_seed_address)
        # subtract the rest of the 2^n from this seed
        possible_addresses += calculate_possible_addresses_from_seed(
            bitmask_unstable_bits[list_index + 1 :], next_seed_address
        )

    return possible_addresses


def sum_values_in_memory(memory):
    memory_sum = 0
    for value in memory.values():
        memory_sum += int(value, 2)
    return memory_sum


if __name__ == "__main__":
    main()
