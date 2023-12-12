from collections import Counter
from functools import cmp_to_key

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

input = [line.strip().split() for line in input]
input = {hand: int(score) for hand, score in input}


def get_first_rule(joker):
    def get_type(hand):
        cards = Counter(hand)
        jokers = cards.pop('J', 0) if joker else 0
        duplicates = list(sorted(cards.values(), reverse=True))
        duplicates[0:1] = [duplicates[0] + jokers] if duplicates else [jokers]
        rules = {(5,): 6, (4, 1): 5, (3, 2): 4,
                 (3, 1): 3, (2, 2): 2, (2, 1): 1}
        return next((score for rule, score in rules.items() if duplicates[:len(rule)] == list(rule)), 0)

    return get_type


def get_second_rule(joker):
    def comparator(hand, other):
        ordering = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9,
                    '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,
                    '2': 2}
        if joker:
            ordering['J'] = 1
        for card, other_card in zip(hand, other):
            if card == other:
                continue
            cmp = ordering[card] - ordering[other_card]
            if cmp > 0:
                return 1
            elif cmp < 0:
                return -1

        return 0

    return comparator


def get_comparator(joker=False):
    first_rule = get_first_rule(joker)
    second_rule = get_second_rule(joker)

    def compare_hands(hand, other):
        type = first_rule(hand)
        other_type = first_rule(other)
        if type > other_type:
            return 1
        elif type < other_type:
            return -1
        else:
            return second_rule(hand, other)

    return cmp_to_key(compare_hands)


def part_one():
    sum = 0
    sorted_hands = sorted(
        input.keys(), key=get_comparator())
    for i, hand in enumerate(sorted_hands):
        sum += input[hand] * (i + 1)

    return sum


print(f'Part One: {part_one()}')


def part_two():
    sum = 0
    sorted_hands = sorted(
        input.keys(), key=get_comparator(joker=True))
    for i, hand in enumerate(sorted_hands):
        sum += input[hand] * (i + 1)

    return sum


print(f'Part Two: {part_two()}')
