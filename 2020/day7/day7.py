# --- Day 7: Handy Haversacks ---
# You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

# Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

# For example, consider the following rules:

# light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.
# These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

# You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

# In the above rules, the following options would be available to you:

# A bright white bag, which can hold your shiny gold bag directly.
# A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
# A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

# How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)

# --- Part Two ---
# It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

# Consider again your shiny gold bag and the rules from the above example:

# faded blue bags contain 0 other bags.
# dotted black bags contain 0 other bags.
# vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
# dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
# So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

# Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

# Here's another example:

# shiny gold bags contain 2 dark red bags.
# dark red bags contain 2 dark orange bags.
# dark orange bags contain 2 dark yellow bags.
# dark yellow bags contain 2 dark green bags.
# dark green bags contain 2 dark blue bags.
# dark blue bags contain 2 dark violet bags.
# dark violet bags contain no other bags.
# In this example, a single shiny gold bag must contain 126 other bags.

import re
import sys


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            all_bag_rules = build_bag_rules(file_reader.readlines())

            # part 1: count all bags that can contain at least 1 of the target color bag (shiny gold)
            print(count_bags_that_can_contain_target(all_bag_rules, "shiny gold"))

            # part 2: count all bags that a target bag MUST contain
            print(count_required_bag_contents(all_bag_rules, "shiny gold"))

    except Exception as error:
        print(error)


def build_bag_rules(raw_bag_rules):
    # bag dict format:
    # { <bag color>: { bag rules } }
    bags_with_rules = {}

    for raw_rule in raw_bag_rules:
        # rule format:
        # <color word> <color word> bags contain <number> <color word> <color word> bag, <...> .

        # bag color -> first two words
        bag_color = re.match(r"^([a-z]+ [a-z]+) bags contain", raw_rule)[1]

        # contents rules -> everything from the fifth word on
        bags_with_rules[bag_color] = build_content_rules(raw_rule)

    return bags_with_rules


def build_content_rules(raw_bag_rule_line):
    # contents rule format:
    # <number> <color word> <color word> bag(s)
    # we only care about the number and the color words
    raw_content_rules = re.finditer(r"((\d+) ([a-z]+ [a-z]+)) (?:bags?)", raw_bag_rule_line)

    # build a rules object in the form: { "color word": bag count }
    content_rules = {}
    for rule in raw_content_rules:
        match_groups = rule.groups()
        bag_count = int(match_groups[1])
        color = match_groups[2]
        content_rules[color] = bag_count

    return content_rules


# given a set of color-coordinated bag rules and a target color, count how many
# bags can contain at least one bag of that color
def count_bags_that_can_contain_target(all_bag_rules, target_color):
    bag_total = 0
    for bag_color in all_bag_rules:
        bag_total += evaluate_bag_and_child_bags(target_color, all_bag_rules, bag_color)

    return bag_total


# determine if the target color bag can be contained in any given bag or any one of its children
def evaluate_bag_and_child_bags(target_color, all_bag_rules, curr_color):
    curr_bag_rules = all_bag_rules[curr_color]
    if not curr_bag_rules:
        return 0

    if target_color in curr_bag_rules:
        return 1

    for color in curr_bag_rules:
        # in this case, we only care about ANY child bag being able to hold a target color bag
        # so we can return as soon as we find that case
        if evaluate_bag_and_child_bags(target_color, all_bag_rules, color) > 0:
            return 1

    return 0

# given a set of color-coordinated bag rules and a target color, count how many
# bags the target bag must contain (hint: it has lots of nested child bags)
def count_required_bag_contents(all_bag_rules, target_color):
    total_contained_bags = 0
    target_bag_rules = all_bag_rules[target_color]

    for child_bag_color in target_bag_rules:
        child_bag_count = target_bag_rules[child_bag_color]
        total_contained_bags += child_bag_count + (
            child_bag_count
            * count_bag_and_child_bags(target_color, all_bag_rules, child_bag_color)
        )

    return total_contained_bags


# some counting recursion for fun
# do I need it? who knows!
def count_bag_and_child_bags(target_color, all_bag_rules, curr_color):
    curr_bag_rules = all_bag_rules[curr_color]
    if not curr_bag_rules:
        return 0

    contained_bag_count = 0
    for color in curr_bag_rules:
        child_bag_count = curr_bag_rules[color]
        contained_bag_count += child_bag_count + (
            child_bag_count
            * count_bag_and_child_bags(target_color, all_bag_rules, color)
        )

    return contained_bag_count


if __name__ == "__main__":
    main()
