/**
 * --- Day 7: Camel Cards ---
 * In Camel Cards, you get a list of hands, and your goal is to order them based
 * on the strength of each hand. A hand consists of five cards labeled one of
 * A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card
 * follows this order, where A is the highest and 2 is the lowest.
 *
 * Every hand is exactly one type. From strongest to weakest, they are:
 *
 * Five of a kind, where all five cards have the same label: AAAAA
 * Four of a kind, where four cards have the same label and one card has a
 * different label: AA8AA
 * Full house, where three cards have the same label, and the remaining two
 * cards share a different label: 23332
 * Three of a kind, where three cards have the same label, and the remaining
 * two cards are each different from any other card in the hand: TTT98
 * Two pair, where two cards share one label, two other cards share a second
 * label, and the remaining card has a third label: 23432
 * One pair, where two cards share one label, and the other three cards have a
 * different label from the pair and each other: A23A4
 * High card, where all cards' labels are distinct: 23456
 *
 * Hands are primarily ordered based on type; for example, every full house is
 * stronger than any three of a kind.
 *
 * If two hands have the same type, a second ordering rule takes effect.
 * Start by comparing the first card in each hand. If these cards are different,
 * the hand with the stronger first card is considered stronger. If the first
 * card in each hand have the same label, however, then move on to considering
 * the second card in each hand. If they differ, the hand with the higher second
 * card wins; otherwise, continue with the third card in each hand, then the
 * fourth, then the fifth.
 *
 * So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger
 * because its first card is stronger. Similarly, 77888 and 77788 are both a
 * full house, but 77888 is stronger because its third card is stronger (and
 * both hands have the same first and second card).
 *
 * To play Camel Cards, you are given a list of hands and their corresponding
 * bid (your puzzle input). For example: test-input.txt
 *
 * This example shows five hands; each hand is followed by its bid amount. Each
 * hand wins an amount equal to its bid multiplied by its rank, where the
 * weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up
 * to the strongest hand. Because there are five hands in this example, the
 * strongest hand will have rank 5 and its bid will be multiplied by 5.
 *
 * So, the first step is to put the hands in order of strength:
 * 32T3K is the only one pair and the other hands are all a stronger type, so
 * it gets rank 1.
 * KK677 and KTJJT are both two pair. Their first cards both have the same
 * label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank
 * 2 and KK677 gets rank 3.
 * T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card,
 * so it gets rank 5 and T55J5 gets rank 4.
 *
 * Now, you can determine the total winnings of this set of hands by adding up
 * the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 +
 * 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.
 *
 * Find the rank of every hand in your set. What are the total winnings?
 *
 * --- Part 2 ---
 * To make things a little more interesting, the Elf introduces one additional
 * rule. Now, J cards are jokers - wildcards that can act like whatever card
 * would make the hand the strongest type possible.
 *
 * To balance this, J cards are now the weakest individual cards, weaker even
 * than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4,
 * 3, 2, J.
 *
 * J cards can pretend to be whatever card is best for the purpose of
 * determining hand type; for example, QJJQ2 is now considered four of a kind.
 * However, for the purpose of breaking ties between two hands of the same type,
 * J is always treated as J, not the card it's pretending to be: JKKK2 is weaker
 * than QQQQ2 because J is weaker than Q.
 *
 * Now, the above example goes very differently: test-input.txt
 *
 * 32T3K is still the only one pair; it doesn't contain any jokers, so its
 * strength doesn't increase.
 * KK677 is now the only two pair, making it the second-weakest hand.
 * T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA
 * gets rank 4, and KTJJT gets rank 5.
 *
 * With the new joker rule, the total winnings in this example are 5905.
 * Using the new joker rule, find the rank of every hand in your set. What are
 * the new total winnings?
 */

import { readFileIntoArray } from "../utils";

// low to high, because that's going to make math easier
const RANKED_HAND_TYPES = [
  "high-card",
  "one-pair",
  "two-pair",
  "three-of-a-kind",
  "full-house",
  "four-of-a-kind",
  "five-of-a-kind",
] as const;

const RANKED_SUITS = {
  A: 0,
  K: 1,
  Q: 2,
  J: 3,
  T: 4,
  "9": 5,
  "8": 6,
  "7": 7,
  "6": 8,
  "5": 9,
  "4": 10,
  "3": 11,
  "2": 12,
};

const RANKED_SUITS_WITH_JOKER = {
  A: 0,
  K: 1,
  Q: 2,
  T: 3,
  "9": 4,
  "8": 5,
  "7": 6,
  "6": 7,
  "5": 8,
  "4": 9,
  "3": 10,
  "2": 11,
  J: 12,
};

type Suit = keyof typeof RANKED_SUITS;
type Hand = {
  originalString: string;
  counts: Partial<Record<Suit, number>>;
  bid: number;
};
type HandType = (typeof RANKED_HAND_TYPES)[number];
type HandsByType = Partial<Record<HandType, Hand[]>>;

function countCardsInHand(handString: string): Hand["counts"] {
  const handCounts: Hand["counts"] = {};

  for (const char of handString) {
    handCounts[char] = (handCounts[char] ?? 0) + 1;
  }

  return handCounts;
}

function determineHandType(handCounts: Hand["counts"]): HandType {
  const cardCounts = Object.values(handCounts);

  if (cardCounts.includes(5)) {
    return "five-of-a-kind";
  }

  if (cardCounts.includes(4)) {
    return "four-of-a-kind";
  }

  if (cardCounts.includes(3)) {
    if (cardCounts.includes(2)) {
      return "full-house";
    }

    return "three-of-a-kind";
  }

  if (cardCounts.filter((count) => count === 2).length === 2) {
    return "two-pair";
  }

  if (cardCounts.includes(2)) {
    return "one-pair";
  }

  return "high-card";
}

function determineHandTypeWithJoker(hand: Hand): HandType {
  const jokerCount = hand.counts["J"] ?? 0;

  if (jokerCount === 5) {
    return "five-of-a-kind";
  }

  if (jokerCount === 0) {
    return determineHandType(hand.counts);
  }

  const handTypeWithoutJoker = determineHandType({
    ...hand.counts,
    J: 0,
  });

  // four-of-a-kind => five-of-a-kind
  // two-pair => full-house
  // three-of-a-kind => 1: four-of-a-kind, 2: five-of-a-kind
  // one-pair => 1: three-of-a-kind; 2: four-of-a-kind; 3: five-of-a-kind
  // high-card => 1: one-pair; 2: three-of-a-kind; 3: four-of-a-kind 4: five-of-a-kind
  switch (handTypeWithoutJoker) {
    case "four-of-a-kind":
      return "five-of-a-kind";
    case "two-pair":
      return "full-house";
    case "three-of-a-kind":
      return jokerCount === 2 ? "five-of-a-kind" : "four-of-a-kind";
    case "one-pair":
      return jokerCount === 3
        ? "five-of-a-kind"
        : jokerCount === 2
        ? "four-of-a-kind"
        : "three-of-a-kind";
    case "high-card":
      return jokerCount === 4
        ? "five-of-a-kind"
        : jokerCount === 3
        ? "four-of-a-kind"
        : jokerCount === 2
        ? "three-of-a-kind"
        : "one-pair";
    default:
      console.log(
        `This should not be physically possible: ${handTypeWithoutJoker}`
      );
      return "high-card";
  }
}

function compareCardsAtIndex(
  hand1: Hand,
  hand2: Hand,
  index: number,
  options?: { useJoker: boolean }
) {
  const suitRanks =
    options?.useJoker === true ? RANKED_SUITS_WITH_JOKER : RANKED_SUITS;
  return (
    suitRanks[hand1.originalString.charAt(index)] -
    suitRanks[hand2.originalString.charAt(index)]
  );
}

// sort all hands within their type groups
// going to sort weakest to strongest because that will make scoring easier
function sortAllHandsLowToHigh(
  handsByType: HandsByType,
  options?: { useJoker: true }
): HandsByType {
  const sortedHandsByType: HandsByType = {};

  Object.entries(handsByType).forEach(([handType, hands]) => {
    const sortedHands = hands.sort(
      (a, b) =>
        compareCardsAtIndex(b, a, 0, options) ||
        compareCardsAtIndex(b, a, 1, options) ||
        compareCardsAtIndex(b, a, 2, options) ||
        compareCardsAtIndex(b, a, 3, options) ||
        compareCardsAtIndex(b, a, 4, options)
    );

    sortedHandsByType[handType] = sortedHands;
  });

  return sortedHandsByType;
}

function computeScore(handsByType: HandsByType): number {
  let multiplier = 0;
  return RANKED_HAND_TYPES.reduce((totalScore, handType) => {
    const handTypeScore = (handsByType[handType] ?? []).reduce(
      (typeScore, hand) => {
        multiplier++;
        return (typeScore += hand.bid * multiplier);
      },
      0
    );

    return (totalScore += handTypeScore);
  }, 0);
}

const lines = readFileIntoArray();
const handsByType: HandsByType = {};
const jokerHandsByType: HandsByType = {};

for (const line of lines) {
  const [handString, bidString] = line.split(" ");

  const hand: Hand = {
    originalString: handString,
    counts: countCardsInHand(handString),
    bid: parseInt(bidString),
  };

  const handType = determineHandType(hand.counts);
  const handTypeWithJoker = determineHandTypeWithJoker(hand);

  handsByType[handType] = [...(handsByType[handType] ?? []), hand];
  jokerHandsByType[handTypeWithJoker] = [
    ...(jokerHandsByType[handTypeWithJoker] ?? []),
    hand,
  ];
}

// now that we've sorted the hands into their types, we need
// to sort all hands in each type group against each other
const sortedHandsByType = sortAllHandsLowToHigh(handsByType);
const sortedJokerHandsByType = sortAllHandsLowToHigh(jokerHandsByType, {
  useJoker: true,
});

// and now, we do the calculating
const totalScore = computeScore(sortedHandsByType);
const totalScoreWithJoker = computeScore(sortedJokerHandsByType);

console.log(`Total hand score: ${totalScore}`);
console.log(`Total hand score with JOKER: ${totalScoreWithJoker}`);
