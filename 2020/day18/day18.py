# --- Day 18: Operation Order ---
# As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted by the child sitting next to you. They're curious if you could help them with their math homework.

# Unfortunately, it seems like this "math" follows different rules than you remember.

# The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*), and parentheses ((...)). Just like normal math, parentheses indicate that the expression inside must be evaluated before it can be used by the surrounding expression. Addition still finds the sum of the numbers on both sides of the operator, and multiplication still finds the product.

# However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.

# For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

# 1 + 2 * 3 + 4 * 5 + 6
#   3   * 3 + 4 * 5 + 6
#       9   + 4 * 5 + 6
#          13   * 5 + 6
#              65   + 6
#                  71
# Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

# 1 + (2 * 3) + (4 * (5 + 6))
# 1 +    6    + (4 * (5 + 6))
#      7      + (4 * (5 + 6))
#      7      + (4 *   11   )
#      7      +     44
#             51
# Here are a few more examples:

# 2 * 3 + (4 * 5) becomes 26.
# 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
# Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the homework; what is the sum of the resulting values?

# Your puzzle answer was 6811433855019.

# --- Part Two ---
# You manage to answer the child's questions and they finish part 1 of their homework, but get stuck when they reach the next section: advanced math.

# Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with. Instead, addition is evaluated before multiplication.

# For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:

# 1 + 2 * 3 + 4 * 5 + 6
#   3   * 3 + 4 * 5 + 6
#   3   *   7   * 5 + 6
#   3   *   7   *  11
#      21       *  11
#          231
# Here are the other examples from above:

# 1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
# 2 * 3 + (4 * 5) becomes 46.
# 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.
# What do you get if you add up the results of evaluating the homework problems using these new rules?

# Your puzzle answer was 129770152447927.

import re
import sys


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            clean_lines = [
                line.rstrip().replace(" ", "") for line in file_reader.readlines()
            ]
            results = [
                evaluate_ordered_precedence_expression(line) for line in clean_lines
            ]
            print(sum(results))
            results_2 = [
                evaluate_weighted_precedence_expression(line) for line in clean_lines
            ]
            print(sum(results_2))

    except Exception as error:
        print(error)
        raise


# order of operations -> (), then calculate IN ORDER
# e.g. 1 + 2 * 4 = 12, 1 + 4 * 2 = 10
def evaluate_ordered_precedence_expression(expression):
    final_expression = []
    # print(expression)

    for token in expression:
        # print(f"evaluate token: {token}")
        if token == ")":
            # we got some mathing to do
            operations = []
            numbers = []
            while token != "(":
                token = final_expression.pop()
                # print(token)
                if token == "*" or token == "+":
                    operations.append(token)
                elif re.match(r"\d+", token):
                    numbers.append(int(token))
            # evaluate all that math
            result = numbers.pop()
            while len(operations) > 0:
                operation = operations.pop()
                if operation == "+":
                    result += numbers.pop()
                elif operation == "*":
                    result *= numbers.pop()
            # put that shit back on the stack
            # (and turn it back into a string or else)
            # print(f'sub result: {result}')
            final_expression.append(str(result))
        else:
            # put that crap on the stack
            final_expression.append(token)

    # do the remaining math - IN ORDER
    # (so our stack is going to operate more like a queue for this)
    # print(final_expression)
    result = int(final_expression.pop(0))
    while len(final_expression) > 0:
        token = final_expression.pop(0)
        if token == "+":
            result += int(final_expression.pop(0))
        elif token == "*":
            result *= int(final_expression.pop(0))

    return result


# order of operations -> (), +, *
# e.g. 1 + 2 * 3 + 4 = 14
def evaluate_weighted_precedence_expression(expression):
    final_expression = []
    print(expression)

    for token in expression:
        # print(f"evaluate token: {token}")
        if token == ")":
            # get yo' math on
            numbers = []
            while token != "(":
                token = final_expression.pop()
                # addition has precedence, so do all those first, and put them back into our intermediate numbers list
                if token == "+":
                    intermediate_sum = int(numbers.pop()) + int(final_expression.pop())
                    numbers.append(str(intermediate_sum))
                elif re.match(r"\d+", token):
                    numbers.append(int(token))

            # take product of all remaining numbers (that's all we have left)
            intermediate_product = 1
            for number in numbers:
                intermediate_product *= int(number)

            final_expression.append(str(intermediate_product))
        else:
            # put ot on the stack, put it on the stack
            final_expression.append(token)

    # do the remaining math
    # this does it the same as the first round of math (calculating totals in parentheses)
    # I bet I can simplify this, but I can't find the give a damn to do it right now
    # print(final_expression)
    final_sums = []
    while len(final_expression) > 0:
        token = final_expression.pop()
        if token == "+":
            intermediate_sum = final_sums.pop() + int(final_expression.pop())
            final_sums.append(intermediate_sum)
        elif re.match(r"\d+", token):
            final_sums.append(int(token))

    result_product = 1
    for number in final_sums:
        result_product *= number

    return result_product


if __name__ == "__main__":
    main()
