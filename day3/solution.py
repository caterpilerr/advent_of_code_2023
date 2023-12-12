input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

input = [list(line.strip()) for line in input]


def left(row, col, visited):
    if col >= 0 and input[row][col].isdigit():
        visited.add((row, col))
        return left(row, col - 1, visited) + input[row][col]
    return ''


def right(row, col, visited):
    if col < len(input[row]) and input[row][col].isdigit():
        visited.add((row, col))
        return input[row][col] + right(row, col + 1, visited)
    return ''


def get_number(row, col, visited):
    if row < 0 or row >= len(input) or \
            col < 0 or col >= len(input[row]):
        return ''

    if input[row][col].isdigit():
        if (row, col) in visited:
            return ''

        visited.add((row, col))
        return left(row, col - 1, visited) + \
            input[row][col] + \
            right(row, col + 1, visited)

    return ''


def part_one():
    digits = []
    visited = set()
    for row in range(len(input)):
        for col in range(len(input[row])):
            if input[row][col].isdigit() or input[row][col] == '.':
                continue
            for i, j in ((i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]):
                number = get_number(row + i, col + j, visited)
                if number:
                    digits.append(int(number))

    return sum(digits)


print(f'Part One: {part_one()}')


def part_two():
    sum = 0
    visited = set()
    for row in range(len(input)):
        for col in range(len(input[row])):
            if input[row][col] != '*':
                continue
            adjacent = []
            for i, j in ((i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]):
                number = get_number(row + i, col + j, visited)
                if number:
                    adjacent.append(int(number))
            if len(adjacent) == 2:
                sum += adjacent[0] * adjacent[1]

    return sum


print(f'Part Two: {part_two()}')
