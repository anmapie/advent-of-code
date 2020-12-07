# --- Day 6: Custom Customs ---
# As your flight approaches the regional airport where you'll switch to a much larger plane, customs declaration forms are distributed to the passengers.

# The form asks a series of 26 yes-or-no questions marked a through z. All you need to do is identify the questions for which anyone in your group answers "yes". Since your group is just you, this doesn't take very long.

# However, the person sitting next to you seems to be experiencing a language barrier and asks if you can help. For each of the people in their group, you write down the questions for which they answer "yes", one per line. For example:

# abcx
# abcy
# abcz
# In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. (Duplicate answers to the same question don't count extra; each question counts at most once.)

# Another group asks for your help, then another, and eventually you've collected answers from every group on the plane (your puzzle input). Each group's answers are separated by a blank line, and within each group, each person's answers are on a single line. For example:

# abc

# a
# b
# c

# ab
# ac

# a
# a
# a
# a

# b
# This list represents answers from five groups:

# The first group contains one person who answered "yes" to 3 questions: a, b, and c.
# The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c.
# The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c.
# The fourth group contains four people; combined, they answered "yes" to only 1 question, a.
# The last group contains one person who answered "yes" to only 1 question, b.
# In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.

# For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?

# --- Part Two ---
# As you finish the last group's customs declaration, you notice that you misread one word in the instructions:

# You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to which everyone answered "yes"!

# This list represents answers from five groups:

# In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
# In the second group, there is no question to which everyone answered "yes".
# In the third group, everyone answered yes to only 1 question, a. Since some people did not answer "yes" to b or c, they don't count.
# In the fourth group, everyone answered yes to only 1 question, a.
# In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.
# In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.

# For each group, count the number of questions to which everyone answered "yes".

import sys


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            grouped_custom_forms = group_custom_forms_by_party(file_reader.readlines())

            # part 1: find the count of total unique 'yes' answers in each group
            print(sum_all_unique_yes_answers(grouped_custom_forms))

            # part 2: find the count of total questions where everyone in a group answered 'yes' to the question
            print(sum_all_unanimous_yes_answers(grouped_custom_forms))
    except Exception as error:
        print(error)


# group custom forms by travel party
# each party member records their 'yes' answers on separate lines
# different parties are separated by new lines
def group_custom_forms_by_party(raw_input):
    grouped_custom_forms = []
    custom_form_group = []
    for line in raw_input:
        clean_line = line.rstrip()
        if len(clean_line) == 0:
            grouped_custom_forms.append(custom_form_group)
            custom_form_group = []
        else:
            custom_form_group.append(clean_line)

    # append the last group (if file doesn't end in new line)
    if len(custom_form_group) > 0:
        grouped_custom_forms.append(custom_form_group)

    return grouped_custom_forms


# sum all of the unique questions that had a 'yes' answer in each group
def sum_all_unique_yes_answers(grouped_custom_forms):
    unique_yes_sum = 0
    for custom_form_group in grouped_custom_forms:
        # convert individual answer sets to single string in order to find the unique answers
        unique_yes = set("".join(custom_form_group))
        unique_yes_sum += len(unique_yes)

    return unique_yes_sum


# sum all of the questions where every member of a group answered 'yes'
def sum_all_unanimous_yes_answers(grouped_custom_forms):
    unanimous_yes_sum = 0
    for custom_form_group in grouped_custom_forms:
        party_size = len(custom_form_group)
        answer_counts = {}

        # count each party member's 'yes' answers
        # store them in a dict to accumulate answers across the party
        for answer_group in custom_form_group:
            for answer in answer_group:
                if answer in answer_counts:
                    answer_counts[answer] += 1
                else:
                    answer_counts[answer] = 1

        # any question with a unanimous 'yes' in the party
        # will have an answer count equal to the party size
        for answer in answer_counts:
            if answer_counts[answer] == party_size:
                unanimous_yes_sum += 1

    return unanimous_yes_sum


if __name__ == "__main__":
    main()
