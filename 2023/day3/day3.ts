/**
 * --- Day 3: Gear Ratios ---
 * You and the Elf eventually reach a gondola lift station; he says the gondola
 * lift will take you up to the water source, but this is as far as he can bring
 * you. You go inside. It doesn't take long to find the gondolas, but there
 * seems to be a problem: they're not moving.
 *
 * "Aaah!"
 *
 * You turn around to see a slightly-greasy Elf with a wrench and a look of
 * surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working
 * right now; it'll still be a while before I can fix it." You offer to help.
 * The engineer explains that an engine part seems to be missing from the
 * engine, but nobody can figure out which one. If you can add up all the part
 * numbers in the engine schematic, it should be easy to work out which part is
 * missing.
 *
 * The engine schematic (your puzzle input) consists of a visual representation
 * of the engine. There are lots of numbers and symbols you don't really
 * understand, but apparently any number adjacent to a symbol, even diagonally,
 * is a "part number" and should be included in your sum.
 * (Periods (.) do not count as a symbol.)
 *
 * Here is an example engine schematic: test-input.txt
 *
 * In this schematic, two numbers are not part numbers because they are not
 * adjacent to a symbol: 114 (top right) and 58 (middle right). Every other
 * number is adjacent to a symbol and so is a part number; their sum is 4361.
 *
 * Of course, the actual engine schematic is much larger. What is the sum of all
 * of the part numbers in the engine schematic?
 *
 * --- Part 2 ---
 *
 * The engineer finds the missing part and installs it in the engine! As the
 * engine springs to life, you jump in the closest gondola, finally ready to
 * ascend to the water source.
 *
 * You don't seem to be going very fast, though. Maybe something is still wrong?
 * Fortunately, the gondola has a phone labeled "help", so you pick it up and
 * the engineer answers.
 *
 * Before you can explain the situation, she suggests that you look out the
 * window. There stands the engineer, holding a phone in one hand and waving
 * with the other. You're going so slowly that you haven't even left the
 * station. You exit the gondola.
 *
 * The missing part wasn't the only issue - one of the gears in the engine is
 *  wrong. A gear is any * symbol that is adjacent to exactly two part numbers.
 * Its gear ratio is the result of multiplying those two numbers together.
 * This time, you need to find the gear ratio of every gear and add them all up
 * so that the engineer can figure out which gear needs to be replaced.
 *
 * Consider the same engine schematic again: test-input.txt
 *
 * In this schematic, there are two gears. The first is in the top left; it has
 * part numbers 467 and 35, so its gear ratio is 16345. The second gear is in
 * the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a
 * gear because it is only adjacent to one part number.) Adding up all of the
 * gear ratios produces 467835.
 *
 * What is the sum of all of the gear ratios in your engine schematic?
 */
import { computeSumOfArray, readFileIntoArray } from "../utils";

type AdjacentCharData = {
  char: string;
  row: number;
  col: number;
};

const PLACEHOLDER_SYMBOL = ".";
const GEAR_SYMBOL = "*";
const GEAR_ADJACENCY_LIMIT = 2;

function getAllAdjacentChars(
  schematic: string[][],
  row: number,
  col: number
): AdjacentCharData[] {
  return [
    // horizontal
    { char: schematic[row]?.[col - 1], row, col: col - 1 },
    { char: schematic[row]?.[col + 1], row, col: col + 1 },
    // vertical
    { char: schematic[row - 1]?.[col], row: row - 1, col },
    { char: schematic[row + 1]?.[col], row: row + 1, col },
    // diagonal
    { char: schematic[row - 1]?.[col - 1], row: row - 1, col: col - 1 },
    { char: schematic[row - 1]?.[col + 1], row: row - 1, col: col + 1 },
    { char: schematic[row + 1]?.[col - 1], row: row + 1, col: col - 1 },
    { char: schematic[row + 1]?.[col + 1], row: row + 1, col: col + 1 },
  ].filter((data) => data.char != null);
}

function isNumberAdjacentToSymbol(
  schematic: string[][],
  row: number,
  col: number
): boolean {
  const adjacentChars = getAllAdjacentChars(schematic, row, col).map(
    (data) => data.char
  );

  return (
    adjacentChars.find(
      (char) => char !== PLACEHOLDER_SYMBOL && char.match(/\W/)
    ) != null
  );
}

function getPartNumbersFromRow(
  schematic: string[][],
  row: string[],
  rowIndex: number
): number[] {
  const partNumbers: number[] = [];
  let currentNumStr = "";
  let currentNumIsValid = false;

  for (let col = 0; col < row.length; col++) {
    const char = row[col];
    if (char.match(/\d/)) {
      currentNumStr += char;

      // check for symbol adjacency so we can maybe see if this is a valid
      // number we're building; note "adjacent" includes diagonal spaces
      if (!currentNumIsValid) {
        currentNumIsValid = isNumberAdjacentToSymbol(schematic, rowIndex, col);
      }
    } else {
      if (currentNumIsValid) {
        partNumbers.push(parseInt(currentNumStr));
      }

      currentNumStr = "";
      currentNumIsValid = false;
    }
  }

  // did we get to the end of the row with a number?
  // don't forget it!
  if (currentNumStr.length > 0 && currentNumIsValid) {
    partNumbers.push(parseInt(currentNumStr));
  }

  return partNumbers;
}

function findPossibleGearData(
  schematic: string[][],
  row: number,
  col: number
): AdjacentCharData[] | null {
  const adjacentDigitData = getAllAdjacentChars(schematic, row, col)
    .filter((data) => data.char.match(/\d/))
    .sort((a, b) => a.row - b.row || a.col - b.col);

  // group by row
  const digitDataByRows = adjacentDigitData.reduce(
    (dataByRow, digitData) => ({
      ...dataByRow,
      [digitData.row]: [...(dataByRow[digitData.row] ?? []), digitData],
    }),
    {} as Record<number, AdjacentCharData[]>
  );

  // if there are more rows of digit data than adjacent digits allow for a gear,
  // this is not a valid gear config
  if (Object.keys(digitDataByRows).length > GEAR_ADJACENCY_LIMIT) {
    return null;
  }

  // get the starting digit for each adjacent numberl if digits are in the same
  // row, but not in adjacent columns, they represent different numbers
  const startingDigits: AdjacentCharData[] = [];
  Object.values(digitDataByRows).forEach((digitDataList) => {
    // since we sorted by col, we just need to check if the first 2 values in
    // the list are adjacent; if not, this is 2 separate digit groups
    if (
      digitDataList.length > 1 &&
      (digitDataList[1]?.col ?? 0) - (digitDataList[0]?.col ?? 0) > 1
    ) {
      startingDigits.push(...digitDataList);
    } else {
      startingDigits.push(digitDataList[0]);
    }
  });

  if (startingDigits.length !== GEAR_ADJACENCY_LIMIT) {
    return null;
  }

  return startingDigits;
}

function findGearRatios(
  schematic: string[][],
  row: string[],
  rowIndex: number
): number[] {
  const gearRatios: number[] = [];

  for (let col = 0; col < row.length; col++) {
    if (row[col] === GEAR_SYMBOL) {
      const gearData = findPossibleGearData(schematic, rowIndex, col);

      if (gearData != null) {
        const gearNumbers: number[] = [];

        // get dem numbers
        for (const digitData of gearData) {
          // walk the row back to the first digit, add to top of stack
          let currentDigit = schematic[digitData.row][digitData.col];
          let currentCol = digitData.col;
          const digitCols: number[] = [];
          while (currentDigit != null && currentDigit.match(/\d/) != null) {
            digitCols.push(currentCol);
            currentCol -= 1;
            currentDigit = schematic[digitData.row]?.[currentCol];
          }

          // walk forward to the last digit, add to "bottom" of stack
          currentCol = digitData.col + 1;
          currentDigit = schematic[digitData.row][currentCol];
          while (currentDigit != null && currentDigit.match(/\d/) != null) {
            digitCols.unshift(currentCol);
            currentCol += 1;
            currentDigit = schematic[digitData.row]?.[currentCol];
          }

          // unspool our stack of columns
          let numberStr = "";
          while (digitCols.length > 0) {
            const poppedCol = digitCols.pop();
            if (poppedCol != null) {
              numberStr += schematic[digitData.row]?.[poppedCol] ?? "";
            }
          }

          // weep
          gearNumbers.push(parseInt(numberStr));
        }

        const ratio = gearNumbers.reduce(
          (product, currNum) => (product *= currNum),
          1
        );
        gearRatios.push(ratio);
      }
    }
  }

  return gearRatios;
}

const lines = readFileIntoArray();
const schematic: string[][] = [];
const allPartNumbers: number[] = [];
const allGearRatios: number[] = [];

for (const line of lines) {
  schematic.push([...line]);
}

for (let row = 0; row < schematic.length; row++) {
  allPartNumbers.push(...getPartNumbersFromRow(schematic, schematic[row], row));
}

for (let row = 0; row < schematic.length; row++) {
  allGearRatios.push(...findGearRatios(schematic, schematic[row], row));
}

const allPartNumbersSum = computeSumOfArray(allPartNumbers);
const allGearRatiosSum = computeSumOfArray(allGearRatios);

console.log(`Part number sum: ${allPartNumbersSum}`);
console.log(`Gear ratio sum: ${allGearRatiosSum}`);
