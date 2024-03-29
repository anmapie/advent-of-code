import * as fs from "fs";

/**
 * Assumes the filename is the first CL arg
 */
export function readFileIntoArray(): string[] | null {
  try {
    const filename = process.argv[2];
    const data = fs.readFileSync(`./${filename}`, "utf8");
    return data.split("\n");
  } catch (err) {
    console.log(err);
    return null;
  }
}

export function computeSumOfArray(arr: number[]): number {
  return arr.reduce((sum, currNum) => (sum += currNum), 0);
}

export function computeProductOfArray(arr: number[]): number {
  return arr.reduce((product, currNum) => (product *= currNum), 1);
}

export function stringToNumberArr(str: string): number[] {
  return str
    .split(" ")
    .map((numStr) => parseInt(numStr))
    .filter((num) => !isNaN(num));
}
