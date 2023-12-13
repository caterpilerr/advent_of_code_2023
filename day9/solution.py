input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

input = [list(map(int, line.split())) for line in input]


def part_one():
    sum = 0
    for sequence in input:
        predict = 0
        current = sequence
        while any(current):
            predict += current[-1]
            current = [current[i + 1] - current[i]
                       for i in range(len(current) - 1)]

        sum += predict

    return sum


print(f'Part One: {part_one()}')


def part_two():
    sum = 0
    for sequence in input:
        current = sequence
        predict = 0
        sign = 1
        while any(current):
            predict += current[0] * sign
            current = [current[i + 1] - current[i]
                       for i in range(len(current) - 1)]
            sign *= -1

        sum += predict

    return sum


print(f'Part Two: {part_two()}')
