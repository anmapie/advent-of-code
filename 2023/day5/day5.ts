/**
 * --- Day 5: If You Give A Seed A Fertilizer ---
 * You take the boat and find the gardener right where you were told he would
 * be: managing a giant "garden" that looks more to you like a farm.
 *
 * "A water source? Island Island is the water source!" You point out that Snow
 * Island isn't receiving any water.
 *
 * "Oh, we had to stop the water because we ran out of sand to filter it with!
 * Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand
 * soon; we only turned off the water a few days... weeks... oh no." His face
 * sinks into a look of horrified realization.
 *
 * "I've been so busy making sure everyone here has food that I completely
 * forgot to check why we stopped getting more sand! There's a ferry leaving
 * soon that is headed over in that direction - it's much faster than your boat.
 * Could you please go check it out?"
 *
 * You barely have time to agree to this request when he brings up another.
 * "While you wait for the ferry, maybe you can help us with our food production
 * problem. The latest Island Island Almanac just arrived and we're having
 * trouble making sense of it."
 *
 * The almanac (your puzzle input) lists all of the seeds that need to be
 * planted. It also lists what type of soil to use with each kind of seed, what
 * type of fertilizer to use with each kind of soil, what type of water to use
 * with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer
 * and so on is identified with a number, but numbers are reused by each
 * category - that is, soil 123 and fertilizer 123 aren't necessarily related
 * to each other.
 *
 * For example: test-input.txt
 *
 * ...I am not going to copy the rest of this input because holy shit.
 * https://adventofcode.com/2023/day/5
 *
 * What is the lowest location number that corresponds to any of the initial
 * seed numbers?
 *
 * --- Part 2 ---
 * Everyone will starve if you only plant such a small number of seeds.
 * Re-reading the almanac, it looks like the seeds: line actually describes
 * ranges of seed numbers.
 *
 * The values on the initial seeds: line come in pairs. Within each pair,
 * the first value is the start of the range and the second value is the length
 * of the range. So, in the first line of the example above:
 *
 * seeds: 79 14 55 13
 *
 * This line describes two ranges of seed numbers to be planted in the garden.
 * The first range starts with seed number 79 and contains 14 values: 79, 80,
 * ..., 91, 92. The second range starts with seed number 55 and contains 13
 * values: 55, 56, ..., 66, 67.
 *
 * Now, rather than considering four seed numbers, you need to consider a total
 * of 27 seed numbers.
 *
 * In the above example, the lowest location number can be obtained from seed
 * number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77,
 * temperature 45, humidity 46, and location 46. So, the lowest location
 * number is 46.
 *
 * Consider all of the initial seed numbers listed in the ranges on the first
 * line of the almanac. What is the lowest location number that corresponds to
 * any of the initial seed numbers?
 */
import * as fs from "fs";
import * as readline from "readline";
import { stringToNumberArr } from "../utils";

type Range = {
  min: number;
  max: number;
};

type IdMod = Range & {
  start: number;
};

type AlmanacEntry = {
  source: string;
  destination: string;
  idMods: IdMod[];
  reverseIdMods: IdMod[];
};

type Almanac = Record<string, AlmanacEntry>;

function buildIdMod(line: string): IdMod {
  const [yStart, xStart, length] = stringToNumberArr(line);

  return {
    min: xStart,
    max: xStart + length - 1,
    start: yStart,
  };
}

function buildReverseIdMod(line: string): IdMod {
  const [yStart, xStart, length] = stringToNumberArr(line);

  return {
    min: yStart,
    max: yStart + length - 1,
    start: xStart,
  };
}

// seeds: 79 14 55 13 -> [{ min: 79, max: 92 }, { min: 55, max: 67 }]
function buildSeedRanges(line: string): { min: number; max: number }[] {
  const seedLineArr = stringToNumberArr(line.split(": ")[1]);
  const ranges: Range[] = [];
  for (let i = 0; i < seedLineArr.length; i += 2) {
    ranges.push({
      min: seedLineArr[i],
      max: seedLineArr[i] + seedLineArr[i + 1] - 1,
    });
  }

  return ranges.sort((a, b) => a.min - b.min);
}

// this whole problem is a bunch of X:Y (e.g. seed:soil) id maps
// to find the location for a seed, we need to start with a seed:something map
// and traverse through as many maps as it takes to get to the
// something:location map
// ids map X:X unless they are modded
// mods encompass a range of X id values (min/max)
// they start at Y id value (start) and increment by 1 along the range
// we can compute the Y id value of any X id in the range as follows:
// (xId - min) + start = yId
function getNextId(startId: number, idMods: IdMod[]): number {
  for (const mod of idMods) {
    const { min, max, start } = mod;

    if (startId < min) {
      return startId;
    }

    if (startId >= min && startId <= max) {
      return startId - min + start;
    }
  }

  return startId;
}

function sourceIdToDestId(
  startSource: string,
  endDest: string,
  startId: number,
  almanac: Almanac
): number {
  let currSource = startSource;
  let currId = startId;

  while (currSource !== endDest && currSource != null) {
    const currEntry = almanac[currSource];
    currId = getNextId(currId, currEntry.idMods);
    currSource = currEntry.destination;
  }

  return currId;
}

// (xId - min) + start = yId
// xId = yId - start + min
function destIdToSourceId(
  startDest: string,
  endSource: string,
  startId: number,
  almanac: Almanac
): number {
  let currDest = startDest;
  let currId = startId;

  while (currDest !== endSource) {
    const currEntry = Object.values(almanac).find(
      (entry) => entry.destination === currDest
    );
    currId = getNextId(currId, currEntry.reverseIdMods);
    currDest = currEntry.source;
  }

  return currId;
}

async function buildAlmanacFromFile(): Promise<{
  seedIds: number[];
  seedRanges: Range[];
  almanac: Almanac;
}> {
  const filename = process.argv[2];
  const fileStream = fs.createReadStream(`./${filename}`);

  // gotta read this in line by line
  // https://nodejs.org/api/readline.html#readline_example_read_file_stream_line_by_line
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });

  let seedIds: number[] = [];
  let seedRanges: Range[] = [];
  let currentMods: IdMod[] = [];
  let currentReverseMods: IdMod[] = [];
  let currentSource: string;
  let currentDest: string;
  const almanac: Almanac = {};

  for await (const line of rl) {
    if (line.length === 0 && currentSource != null) {
      // finished with whatever unholy map this is
      almanac[currentSource] = {
        source: currentSource,
        destination: currentDest,
        idMods: currentMods.sort((a, b) => a.min - b.min),
        reverseIdMods: currentReverseMods.sort((a, b) => a.min - b.min),
      };
      currentMods = [];
      currentReverseMods = [];
    } else if (line.startsWith("seeds:")) {
      // file has a one line of just seed ids, e.g. "seeds: 79 14 55 13"
      seedIds = stringToNumberArr(line.split(": ")[1]);
      seedRanges = buildSeedRanges(line);
    } else if (line.match(/^\d/) != null) {
      // lines that start with numbers represent an X:Y id mod
      // mods are three numbers: Y start, X start, length
      currentMods.push(buildIdMod(line));
      currentReverseMods.push(buildReverseIdMod(line));
    } else {
      // this line tells us the source (X) + destination (Y) of the map
      // eg. seed-to-soil
      const [source, destination] = line.split(" ")[0].split("-to-");
      currentSource = source;
      currentDest = destination;
    }
  }

  // final entry
  if (currentSource != null) {
    almanac[currentSource] = {
      source: currentSource,
      destination: currentDest,
      idMods: currentMods.sort((a, b) => a.min - b.min),
      reverseIdMods: currentReverseMods.sort((a, b) => a.min - b.min),
    };
  }

  return { seedIds, seedRanges, almanac };
}

buildAlmanacFromFile().then(({ seedIds, seedRanges, almanac }) => {
  // find the SMALLEST seed location from ids
  const minLocationFromIds = seedIds.reduce((minValue, seedId) => {
    const location = sourceIdToDestId("seed", "location", seedId, almanac);
    if (location < minValue) {
      return location;
    }

    return minValue;
  }, Number.MAX_SAFE_INTEGER);

  console.log(`Min location (ids): ${minLocationFromIds}`);

  // find the smallest from the RANGES
  // to do this one, we're going to go BACKWARDS
  // starting at 0, we'll look at every location until we find the smallest
  // possible location that matches with an available seed
  let minLocationFromRange = 0;
  let seedFound = false;

  while (!seedFound) {
    const seedId = destIdToSourceId(
      "location",
      "seed",
      minLocationFromRange,
      almanac
    );

    for (const range of seedRanges) {
      if (seedId >= range.min && seedId <= range.max) {
        seedFound = true;
        break;
      }
    }

    if (!seedFound) {
      minLocationFromRange++;
    }
  }

  console.log(`Min location (range): ${minLocationFromRange}`);
});
