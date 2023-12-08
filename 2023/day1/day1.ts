import { readFileIntoArray } from "../utils";

/**
 * As they're making the final adjustments, they discover that their calibration
 * document (your puzzle input) has been amended by a very young Elf who was
 * apparently just excited to show off her art skills. Consequently, the Elves
 *  are having trouble reading the values on the document.
 *
 * The newly-improved calibration document consists of lines of text; each line
 * originally contained a specific calibration value that the Elves now need to
 * recover. On each line, the calibration value can be found by combining the
 * first digit and the last digit (in that order) to form a single two-digit
 * number.
 *
 * For example: pt1-test.txt
 *
 * In this example, the calibration values of these four lines are 12, 38, 15,
 * and 77. Adding these together produces 142.
 *
 * --- PART 2 ---
 *
 * Your calculation isn't quite right. It looks like some of the digits are
 * actually spelled out with letters: one, two, three, four, five, six, seven,
 * eight, and nine also count as valid "digits".
 *
 * Equipped with this new information, you now need to find the real first and
 * last digit on each line. For example: pt2-test.txt
 *
 * In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76.
 * Adding these together produces 281.
 */
const NUMERALS_TO_NUMBERS = {
  one: 1,
  two: 2,
  three: 3,
  four: 4,
  five: 5,
  six: 6,
  seven: 7,
  eight: 8,
  nine: 9,
};

type NumeralKey = keyof typeof NUMERALS_TO_NUMBERS;

function getFirstDigitInLine(chars: string[]): string | undefined {
  for (const char of chars) {
    if (!isNaN(parseInt(char))) {
      return char;
    }
  }

  return undefined;
}

function getFirstAndLastNumeralStrings(line: string): {
  firstNumeral?: string;
  lastNumeral?: string;
} {
  const occurrences = Object.keys(NUMERALS_TO_NUMBERS).reduce(
    (numeralOccurrences, numeralString) => [
      ...numeralOccurrences,
      {
        numeral: numeralString,
        first: line.indexOf(numeralString),
        last: line.lastIndexOf(numeralString),
      },
    ],
    [] as { numeral: NumeralKey; first: number; last: number }[]
  );

  occurrences.sort((a, b) => a.first - b.first);
  const firstNumeral = occurrences.filter(
    (occurrence) => occurrence.first >= 0
  )[0]?.numeral;

  occurrences.sort((a, b) => b.last - a.last);
  const lastNumeral = occurrences.filter(
    (occurrence) => occurrence.last >= 0
  )?.[0]?.numeral;

  return {
    firstNumeral,
    lastNumeral,
  };
}

function indexOrMax(line: string, target: string | undefined): number {
  return target != null ? line.indexOf(target) : Number.MAX_SAFE_INTEGER;
}

function getNumberFromLine(
  line: string,
  options: { includeText: boolean }
): number {
  const charArray = [...line];
  let firstDigit = getFirstDigitInLine(charArray);
  let lastDigit = getFirstDigitInLine(charArray.reverse());

  if (options.includeText) {
    const { firstNumeral, lastNumeral } = getFirstAndLastNumeralStrings(line);
    firstDigit =
      indexOrMax(line, firstNumeral) < indexOrMax(line, firstDigit)
        ? NUMERALS_TO_NUMBERS[firstNumeral] ?? 0
        : firstDigit;

    lastDigit =
      line.lastIndexOf(lastNumeral) > line.lastIndexOf(lastDigit)
        ? NUMERALS_TO_NUMBERS[lastNumeral] ?? 0
        : lastDigit;
  }

  const finalNumber = parseInt(`${firstDigit}${lastDigit}`);
  return isNaN(finalNumber) ? 0 : finalNumber;
}

const lines = readFileIntoArray();
let sum = 0;

if (lines != null) {
  lines.forEach((line) => {
    const number = getNumberFromLine(line, { includeText: true });
    sum += isNaN(number) ? 0 : number;
  });
}

console.log(sum);
