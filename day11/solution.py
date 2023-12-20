input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

y_filled = set()
x_filled = set()
galaxies = list()
for y, line in enumerate(input):
    for x, char in enumerate(line):
        if char == '#':
            x_filled.add(x)
            y_filled.add(y)
            galaxies.append((x, y))


def build_coordinate_map(compression_factor=2):
    x_map = dict()
    x_real = 0
    for x in range(len(input[0])):
        x_map[x] = x_real
        x_real += 1 if x in x_filled else compression_factor

    y_map = dict()
    y_real = 0
    for y in range(len(input)):
        y_map[y] = y_real
        y_real += 1 if y in y_filled else compression_factor

    return x_map, y_map


def part_one():
    x_map, y_map = build_coordinate_map()
    sum = 0
    for i, galaxy in enumerate(galaxies):
        for other_galaxy in galaxies[i+1:]:
            path = abs(x_map[galaxy[0]] - x_map[other_galaxy[0]]) + \
                abs(y_map[galaxy[1]] - y_map[other_galaxy[1]])
            sum += path

    return sum


print(f'Part One: {part_one()}')


def part_two():
    x_map, y_map = build_coordinate_map(1000000)
    sum = 0
    for i, galaxy in enumerate(galaxies):
        for other_galaxy in galaxies[i+1:]:
            path = abs(x_map[galaxy[0]] - x_map[other_galaxy[0]]) + \
                abs(y_map[galaxy[1]] - y_map[other_galaxy[1]])
            sum += path

    return sum


print(f'Part Two: {part_two()}')
