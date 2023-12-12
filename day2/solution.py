input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

games = []
for line in input:
    game_data = line.strip().split(':')[1]
    game = []
    for turn in game_data.split(';'):
        bag = {}
        for cubes in turn.split(','):
            items = cubes.split()
            bag[items[1]] = int(items[0])
        game.append(bag)
    games.append(game)


def game_is_possible(game, expected):
    for turn in game:
        for color, count in turn.items():
            if count > expected[color]:
                return False

    return True


def part_one():
    expected = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    sum = 0
    for i, game in enumerate(games):
        if game_is_possible(game, expected):
            sum += i + 1

    return sum


print(f'Part One: {part_one()}')


def part_two():
    sum = 0
    for game in games:
        required = {
            'red': 0,
            'green': 0,
            'blue': 0
        }

        for turn in game:
            for color, count in turn.items():
                required[color] = max(count, required[color])

        sum += required['red'] * required['green'] * required['blue']

    return sum


print(f'Part Two: {part_two()}')
