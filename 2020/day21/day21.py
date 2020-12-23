# --- Day 21: Allergen Assessment ---
# You reach the train's last stop and the closest you can get to your vacation island without getting wet. There aren't even any boats here, but nothing can stop you now: you build a raft. You just need a few days' worth of food for your journey.

# You don't speak the local language, so you can't read any ingredients lists. However, sometimes, allergens are listed in a language you do understand. You should be able to use this information to determine which ingredient contains which allergen and work out which foods are safe to take with you on your trip.

# You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that food's ingredients list followed by some or all of the allergens the food contains.

# Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list), the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list. However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present: maybe they forgot to label it, or maybe it was labeled in a language you don't know.

# For example, consider the following list of foods:

# mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
# trh fvjkl sbzzf mxmxvkd (contains dairy)
# sqjhc fvjkl (contains soy)
# sqjhc mxmxvkd sbzzf (contains fish)
# The first food in the list has four ingredients (written in a language you don't understand): mxmxvkd, kfcds, sqjhc, and nhms. While the food might contain other allergens, a few allergens the food definitely contains are listed afterward: dairy and fish.

# The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list. In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen. Counting the number of times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which appears twice.

# Determine which ingredients cannot possibly contain any of the allergens in your list. How many times do any of those ingredients appear?

# Your puzzle answer was 2020.

# --- Part Two ---
# Now that you've isolated the inert ingredients, you should have enough information to figure out which ingredient contains which allergen.

# In the above example:

# mxmxvkd contains dairy.
# sqjhc contains fish.
# fvjkl contains soy.
# Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your canonical dangerous ingredient list. (There should not be any spaces in your canonical dangerous ingredient list.) In the above example, this would be mxmxvkd,sqjhc,fvjkl.

# Time to stock your raft with supplies. What is your canonical dangerous ingredient list?

# Your puzzle answer was bcdgf,xhrdsl,vndrb,dhbxtb,lbnmsr,scxxn,bvcrrfbr,xcgtv.

from functools import reduce
import sys


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            food_labels = build_labels(
                [line.rstrip() for line in file_reader.readlines()]
            )
            print(count_allergy_free_ingredient_occurrences(food_labels))
            print(get_dangerous_ingredient_list(food_labels))

    except Exception as error:
        print(error)
        raise


def build_labels(raw_food_labels):
    food_labels = []
    for label in raw_food_labels:
        label_parts = label.split("(")
        ingredients = label_parts[0].strip().split()
        allergens = label_parts[1].strip("contains").strip().rstrip(")").split(", ")
        food_labels.append((ingredients, allergens))
    return food_labels


def find_allergen_ingredients(food_labels):
    ingredients_by_allergen = {}
    for label in food_labels:
        ingredients, allergens = label

        # associate each ingredient with each allergen
        # we don't know which ingredients contain the listed allergens
        for allergen in allergens:
            if allergen not in ingredients_by_allergen:
                ingredients_by_allergen[allergen] = set(ingredients)
            else:
                # if we've already recorded this allergen, we can actually narrow down associated ingredients
                # by looking at only the ingredients shared between this label and previous labels we've encountered
                ingredients_by_allergen[allergen] = ingredients_by_allergen[
                    allergen
                ].intersection(set(ingredients))

    # reduce all the possible ingredient/allergen combos so each allergen is associated with only one ingredient
    return reduce_allergen_ingredients(ingredients_by_allergen)


def reduce_allergen_ingredients(ingredients_by_allergen):
    print(ingredients_by_allergen)
    reduced_allergens = set()
    reduced_ingredients = set()
    for allergen, ingredients in ingredients_by_allergen.items():
        if len(ingredients) == 1:
            reduced_allergens.update([allergen])
            reduced_ingredients.update(ingredients)

    allergen_count = len(ingredients_by_allergen.keys())
    while len(reduced_allergens) != allergen_count:
        for allergen, ingredients in ingredients_by_allergen.items():
            ingredient_diff = ingredients - reduced_ingredients
            if len(ingredient_diff) > 0:
                ingredients_by_allergen[allergen] = ingredient_diff
            if len(ingredient_diff) == 1:
                reduced_allergens.update([allergen])
                reduced_ingredients.update(ingredients)

    return ingredients_by_allergen


def find_allergy_free_ingredients(food_labels):
    ingredients_by_allergen = find_allergen_ingredients(food_labels)
    allergen_ingredients = reduce(
        lambda setA, setB: {*setA, *setB}, ingredients_by_allergen.values()
    )
    all_ingredients = set(
        reduce(
            lambda listA, listB: [*listA, *listB], [label[0] for label in food_labels]
        )
    )

    return all_ingredients - allergen_ingredients


def count_allergy_free_ingredient_occurrences(food_labels):
    allergy_free_ingredients = find_allergy_free_ingredients(food_labels)
    ingredient_count = 0
    for label in food_labels:
        ingredients = label[0]
        for ingredient in ingredients:
            if ingredient in allergy_free_ingredients:
                ingredient_count += 1
    return ingredient_count


# alphabetical by allergen
# ingredients should be unique (only appear once in list)
def get_dangerous_ingredient_list(food_labels):
    ingredients_by_allergen = find_allergen_ingredients(food_labels)
    print(ingredients_by_allergen)
    alphabetical_allergens = list(ingredients_by_allergen.keys())
    alphabetical_allergens.sort()
    print(alphabetical_allergens)

    dangerous_ingredients_list = []
    for allergen in alphabetical_allergens:
        # iterate through all ingredients and only add if they aren't already in the list
        # we can't just add willy-nilly and convert to a set at the end, because that
        # screws up the alphabetical ordering
        for ingredient in ingredients_by_allergen[allergen]:
            if ingredient not in dangerous_ingredients_list:
                dangerous_ingredients_list.append(ingredient)

    return ",".join(dangerous_ingredients_list)


if __name__ == "__main__":
    main()
