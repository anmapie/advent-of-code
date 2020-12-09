# --- Day 8: Handheld Halting ---
# Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting next to you.

# Their handheld game console won't turn on! They ask if you can take a look.

# You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should be able to fix it, but first you need to be able to run the code in isolation.

# The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).

# acc increases or decreases a single global value called the accumulator by the value given in the argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the instruction immediately below it is executed next.
# jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
# nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
# For example, consider the following program:

# nop +0
# acc +1
# jmp +4
# acc +3
# jmp -3
# acc -99
# acc +1
# jmp -4
# acc +6
# These instructions are visited in this order:

# nop +0  | 1
# acc +1  | 2, 8(!)
# jmp +4  | 3
# acc +3  | 6
# jmp -3  | 7
# acc -99 |
# acc +1  | 4
# jmp -4  | 5
# acc +6  |
# First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2, jmp -4 executes, setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to continue back at the first acc +1.

# This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries to run any instruction a second time, you know it will never terminate.

# Immediately before the program would run an instruction a second time, the value in the accumulator is 5.

# Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?

import copy
import sys


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            instructions = [line.rstrip() for line in file_reader.readlines()]
            print(run_instructions(instructions))
            print(find_accumulator_without_corrupt_instruction(instructions))

    except Exception as error:
        print(error)


# returns a tuple:
# wether or not the instructions result in an infinite loop (true/false), the value of the accumulator before execution halted
def run_instructions(instructions):
    accumulator = 0
    executed_instructions = []
    next_instruction_index = 0

    # execute instructions until we hit a loop (an instruction we've already executed)
    # or until or next instruction is out of range (aka we run all the instructions)
    while (
        not next_instruction_index in executed_instructions
        and next_instruction_index < len(instructions)
    ):
        executed_instructions.append(next_instruction_index)

        # action format: <3 letter action> <+/-><int>
        # sample actions:
        # nop +0, jmp -3, acc +1
        action, raw_action_value = tuple(instructions[next_instruction_index].split())

        # convert value to an int
        action_value = int(raw_action_value)

        # do action
        if action == "nop":
            # no-op - go to next instruction
            next_instruction_index += 1
        elif action == "acc":
            # add to accumulator
            accumulator += action_value
            # go to next instruction
            next_instruction_index += 1
        elif action == "jmp":
            # jump to instruction indicated by value
            next_instruction_index += action_value
        else:
            raise Exception(f"Invalid instruction value {action}")

    instruction_loop = next_instruction_index in executed_instructions
    return (instruction_loop, accumulator)


# with the given instructions, one no-op or jump instruction can be altered
# to remove the infinite loop and run the instructions completely
def find_accumulator_without_corrupt_instruction(instructions):
    for index, instruction in enumerate(instructions):
        action = instruction[0:3]

        # if the instruction is an acc, we can skip it
        if action == "acc":
            continue

        # make a new copy of the instructions each iteration, to avoid modifying the og
        instruction_copy = copy.deepcopy(instructions)

        # if the action is a no-op or jump, switch it to the other type
        # and run the instructions to see if the loop is fixed
        if action == "nop":
            instruction_copy[index] = "jmp" + instruction[3:]
        elif action == "jmp":
            instruction_copy[index] = "nop" + instruction[3:]
        else:
            raise Exception(f"Invalid instruction value {action}")

        has_loop, accumulator = run_instructions(instruction_copy)

        if not has_loop:
            return accumulator


if __name__ == "__main__":
    main()
