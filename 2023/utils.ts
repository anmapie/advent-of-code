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
