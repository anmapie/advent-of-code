# --- Day 4: Passport Processing ---
# You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport. While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't actually valid documentation for travel in most of the world.

# It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport scanners, and the delay could upset your travel itinerary.

# Due to some questionable network security, you realize you might be able to solve both of these problems at the same time.

# The automatic passport scanners are slow because they're having trouble detecting which passports have all required fields. The expected fields are as follows:

# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)
# Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

# Here is an example batch file containing four passports:

# ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
# byr:1937 iyr:2017 cid:147 hgt:183cm

# iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
# hcl:#cfa07d byr:1929

# hcl:#ae17e1 iyr:2013
# eyr:2024
# ecl:brn pid:760753108 byr:1931
# hgt:179cm

# hcl:#cfa07d eyr:2025 pid:166559648
# iyr:2011 ecl:brn hgt:59in
# The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt (the Height field).

# The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials, not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat this "passport" as valid.

# The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so this passport is invalid.

# According to the above rules, your improved system would report 2 valid passports.

# Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?

# --- Part Two ---
# The line is moving more quickly now, but you overhear airport security talking about how passports with invalid data are getting through. Better add some data validation, quick!

# You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:

# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.
# Your job is to count the passports where all required fields are both present and valid according to the above rules.
# Count the number of valid passports - those that have all required fields and valid values. Continue to treat cid as optional. In your batch file, how many passports are valid?

import re
import sys

REQUIRED_PASSPORT_FIELDS = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
VALID_EYE_COLORS = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
            raw_passports = file_reader.readlines()
            print(count_valid_passports(raw_passports))
            print(count_valid_passports(raw_passports, True))
    except Exception as error:
        print(error)


def count_valid_passports(raw_passports, validate_field_values=False):
    valid_passport_count = 0
    curr_passport_valid_fields = set([])
    for raw_line in raw_passports:
        line = raw_line.rstrip()
        if len(line) == 0:
            # hit a new line; if all fields for current
            if has_all_required_fields(curr_passport_valid_fields):
                valid_passport_count += 1
            # reset curr_passport_fields for next passport
            curr_passport_valid_fields = set([])

        fields = line.split()
        for field in fields:
            field_parts = field.split(":")
            field_name = field_parts[0]
            field_value = field_parts[1]
            # only consider required passport fields - anything else is irrelevant
            if field_name in REQUIRED_PASSPORT_FIELDS:
                # validate the field value if asked to do so
                if not validate_field_values or is_valid_field_value(
                    field_name, field_value
                ):
                    curr_passport_valid_fields.add(field_name)

    # check the last passport (if file does not end w/ newline)
    if len(curr_passport_valid_fields) > 0 and has_all_required_fields(
        curr_passport_valid_fields
    ):
        valid_passport_count += 1

    return valid_passport_count


def is_valid_field_value(field_name, field_value):
    try:
        if field_name == "byr":
            # four digits; at least 1920 and at most 2002
            byr = int(field_value)
            return byr >= 1920 and byr <= 2002
        if field_name == "iyr":
            # four digits; at least 2010 and at most 2020
            iyr = int(field_value)
            return iyr >= 2010 and iyr <= 2020
        if field_name == "eyr":
            # four digits; at least 2020 and at most 2030
            eyr = int(field_value)
            return eyr >= 2020 and eyr <= 2030
        if field_name == "hgt":
            # a number followed by either cm or in
            height_match = re.match(r"^(\d+)(in|cm)$", field_value)

            # no match? get outta here
            if height_match == None:
                return False

            height_value, height_unit = height_match.groups()
            height_as_int = int(height_value)
            if height_unit == "in":
                # if in, the number must be at least 59 and at most 76
                return height_as_int >= 59 and height_as_int <= 76
            if height_unit == "cm":
                # if cm, the number must be at least 150 and at most 193
                return height_as_int >= 150 and height_as_int <= 193
        if field_name == "hcl":
            # a # followed by exactly six characters 0-9 or a-f
            return re.match(r"^#[\da-f]{6}$", field_value)
        if field_name == "ecl":
            # exactly one of: amb blu brn gry grn hzl oth
            return field_value in VALID_EYE_COLORS
        if field_name == "pid":
            # a nine-digit number, including leading zeroes
            return re.match(r"^\d{9}$", field_value)
    except Exception as error:
        print(error)
        return False

    return False


def has_all_required_fields(passport_fields):
    return len(passport_fields) == len(REQUIRED_PASSPORT_FIELDS)


if __name__ == "__main__":
    main()
