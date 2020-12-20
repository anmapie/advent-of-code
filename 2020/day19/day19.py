import re
import sys


def main():
    input_file = sys.argv[1]
    try:
        with open(input_file) as file_reader:
          clean_lines = [line.rstrip() for line in file_reader.readlines() if len(line.rstrip()) > 0]
          rules, messages = parse_rules_and_messages(clean_lines)
          
    except Exception as error:
        print(error)
        raise

def parse_rules_and_messages(clean_input_lines):
  rules = {}
  messages = []
  for line in clean_input_lines:
    if re.match(r"\d+:", line):
      rule_number, rule = line.split(": ")
      rules[rule_number] = rule.strip("\"")
    else:
      messages.append(line)
  
  return (rules, messages)


      

    

if __name__ == "__main__":
    main()