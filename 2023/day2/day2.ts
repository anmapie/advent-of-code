/**
 * --- Day 2: Cube Conundrum ---
 * You're launched high into the atmosphere! The apex of your trajectory just
 * barely reaches the surface of a large island floating in the sky. You gently
 * land in a fluffy pile of leaves. It's quite cold, but you don't see much
 * snow. An Elf runs over to greet you.
 *
 * The Elf explains that you've arrived at Snow Island and apologizes for the
 * lack of snow. He'll be happy to explain the situation, but it's a bit of a
 * walk, so you have some time. They don't get many visitors up here; would you
 * like to play a game in the meantime?
 *
 * As you walk, the Elf shows you a small bag and some cubes which are either
 * red, green, or blue. Each time you play this game, he will hide a secret
 * number of cubes of each color in the bag, and your goal is to figure out
 * information about the number of cubes.
 *
 * To get information, once a bag has been loaded with cubes, the Elf will reach
 * into the bag, grab a handful of random cubes, show them to you, and then put
 * them back in the bag. He'll do this a few times per game.
 *
 * You play several games and record the information from each game (your puzzle
 * input). Each game is listed with its ID number (like the 11 in Game 11: ...)
 * followed by a semicolon-separated list of subsets of cubes that were revealed
 * from the bag (like 3 red, 5 green, 4 blue).
 *
 * For example, the record of a few games might look like this: test-input.txt
 *
 * In game 1, three sets of cubes are revealed from the bag (and then put back
 * again). The first set is 3 blue cubes and 4 red cubes; the second set is 1
 * red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green
 * cubes.
 *
 * The Elf would first like to know which games would have been possible if the
 * bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?
 *
 * In the example above, games 1, 2, and 5 would have been possible if the bag
 *  had been loaded with that configuration. However, game 3 would have been
 * impossible because at one point the Elf showed you 20 red cubes at once;
 * similarly, game 4 would also have been impossible because the Elf showed you
 * 15 blue cubes at once. If you add up the IDs of the games that would have
 * been possible, you get 8.
 *
 * Determine which games would have been possible if the bag had been loaded
 * with only 12 red cubes, 13 green cubes, and 14 blue cubes.
 * What is the sum of the IDs of those games?
 *
 * --- Part 2 ---
 *
 * The Elf says they've stopped producing snow because they aren't getting any
 * water! He isn't sure why the water stopped; however, he can show you how to
 * get to the water source to check it out for yourself. It's just up ahead!
 *
 * As you continue your walk, the Elf poses a second question: in each game you
 * played, what is the fewest number of cubes of each color that could have been
 * in the bag to make the game possible?
 *
 * Again consider the example games from earlier: test-input.txt
 *
 * In game 1, the game could have been played with as few as 4 red, 2 green, and
 * 6 blue cubes. If any color had even one fewer cube, the game would have been
 * impossible.
 * Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue
 * cubes.
 * Game 3 must have been played with at least 20 red, 13 green, and 6 blue
 * cubes.
 * Game 4 required at least 14 red, 3 green, and 15 blue cubes.
 * Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
 *
 * The power of a set of cubes is equal to the numbers of red, green, and blue
 * cubes multiplied together. The power of the minimum set of cubes in game 1 is
 * 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these
 * five powers produces the sum 2286.
 *
 * For each game, find the minimum set of cubes that must have been present.
 * What is the sum of the power of these sets?
 */

import { readFileIntoArray } from "../utils";

const ABSOLUTE_RED_MAX = 12;
const ABSOLUTE_GREEN_MAX = 13;
const ABSOLUTE_BLUE_MAX = 14;

type GameData = {
  cubeMaxes: {
    blue: number;
    green: number;
    red: number;
  };
  id: number;
};

/**
 * Game data format
 * Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
 */
function buildGameDataFromLine(line: string): GameData {
  const labelAndGames = line.split(":");

  // pull of the id from the label
  const id = parseInt(labelAndGames[0].split(" ")[1]);

  // split up all the individual games
  const games = labelAndGames[1].split(";");

  let blueMax = 0;
  let greenMax = 0;
  let redMax = 0;

  // for each game, inspect the number of each color cube pulled and
  // determine if it's the max value for the game
  for (const game of games) {
    const cubeCounts = game.split(",");

    for (const cube of cubeCounts) {
      const countAndColor = cube.trim().split(" ");
      const count = parseInt(countAndColor[0]);
      switch (countAndColor[1]) {
        case "blue":
          if (count > blueMax) {
            blueMax = count;
          }
          break;
        case "green":
          if (count > greenMax) {
            greenMax = count;
          }
          break;
        case "red":
          if (count > redMax) {
            redMax = count;
          }
          break;
        default:
          console.error("wtf");
      }
    }
  }

  return {
    id,
    cubeMaxes: {
      blue: blueMax,
      green: greenMax,
      red: redMax,
    },
  };
}

// game is possible if none of the local max cube counts exceed
// the absolute max cube counts
function isGamePossible(gameData: GameData): boolean {
  const { blue, green, red } = gameData.cubeMaxes;
  return (
    blue <= ABSOLUTE_BLUE_MAX &&
    green <= ABSOLUTE_GREEN_MAX &&
    red <= ABSOLUTE_RED_MAX
  );
}

// the power of a set of cubes is equal to the numbers of red, green, and blue
// cubes multiplied together; the power for a game is the power of the
// minium required cube set
function getGamePower(gameData: GameData): number {
  const { blue, green, red } = gameData.cubeMaxes;
  return blue * green * red;
}

const lines = readFileIntoArray();
let possibleGameSum = 0;
let gamePowerSum = 0;

for (const line of lines) {
  const gameData = buildGameDataFromLine(line);
  if (isGamePossible(gameData)) {
    possibleGameSum += gameData.id;
  }
  gamePowerSum += getGamePower(gameData);
}

console.log(`Possible game sum: ${possibleGameSum}`);
console.log(`Game power sum: ${gamePowerSum}`);
