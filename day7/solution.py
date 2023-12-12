from functools import cmp_to_key

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

input = [line.strip().split() for line in input]
input = {hand: int(score) for hand, score in input}


def first_rule(hand):
    cards = {}
    for card in hand:
        if card in cards:
            cards[card] += 1
        else:
            cards[card] = 1

    duplicates = list(sorted(cards.values(), reverse=True))
    if duplicates == [5]:
        return 6
    elif duplicates[:2] == [4, 1]:
        return 5
    elif duplicates[:2] == [3, 2]:
        return 4
    elif duplicates[:2] == [3, 1]:
        return 3
    elif duplicates[:2] == [2, 2]:
        return 2
    elif duplicates[:2] == [2, 1]:
        return 1
    else:
        return 0


ordering = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9,
            '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,
            '2': 2, 'J': 1}


def second_rule(hand, other):
    for card, other_card in zip(hand, other):
        if card == other:
            continue
        cmp = ordering[card] - ordering[other_card]
        if cmp > 0:
            return 1
        elif cmp < 0:
            return -1

    return 0


def compare_hands(first_rule):
    def comparator(hand, other):
        type = first_rule(hand)
        other_type = first_rule(other)
        if type > other_type:
            return 1
        elif type < other_type:
            return -1
        else:
            return second_rule(hand, other)

    return comparator 


def part_one():
    sum = 0
    sorted_hands = sorted(
        input.keys(), key=cmp_to_key(compare_hands(first_rule)))
    for i, hand in enumerate(sorted_hands):
        sum += input[hand] * (i + 1)

    return sum


print(f'Part One: {part_one()}')


def joker_rule(hand):
    cards = {}
    jokers = 0
    for card in hand:
        if card == 'J':
            jokers += 1
        elif card in cards:
            cards[card] += 1
        else:
            cards[card] = 1

    duplicates = list(sorted(cards.values(), reverse=True))
    if len(duplicates):
        duplicates[0] += jokers
    else:
        duplicates.append(jokers)

    if duplicates == [5]:
        return 6
    elif duplicates[:2] == [4, 1]:
        return 5
    elif duplicates[:2] == [3, 2]:
        return 4
    elif duplicates[:2] == [3, 1]:
        return 3
    elif duplicates[:2] == [2, 2]:
        return 2
    elif duplicates[:2] == [2, 1]:
        return 1
    else:
        return 0


def part_two():
    sum = 0
    sorted_hands = sorted(
        input.keys(), key=cmp_to_key(compare_hands(joker_rule)))
    for i, hand in enumerate(sorted_hands):
        sum += input[hand] * (i + 1)

    return sum


print(f'Part Two: {part_two()}')
