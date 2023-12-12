input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

cards = []
for line in input:
    card = line.strip().split(':')[1].split('|')
    winning = [int(val) for val in card[0].split()]
    current = [int(val) for val in card[1].split()]
    cards.append([winning, current])

def part_one():
    sum = 0
    for card in cards:
        winning = set(card[0])
        pow = -1
        for number in card[1]: 
            if number in winning:
                pow += 1
        if (pow >= 0):
            sum += 2 ** pow

    return sum

print(f'Part One: {part_one()}')

def part_two():
    cards_numbers = [1] * len(cards)
    for i, card in enumerate(cards):
        winning = set(card[0])
        matching = 0
        for number in card[1]: 
            if number in winning:
                matching += 1
        if matching > 0:
            for next in range(i + 1, min(len(cards), i + matching + 1)):
                cards_numbers[next] += cards_numbers[i]

    return sum(cards_numbers)

print(f'Part Two: {part_two()}')
