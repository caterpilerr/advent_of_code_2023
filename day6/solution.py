from math import sqrt, ceil, floor
from functools import reduce
import operator

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def solve(total, record):
    d = total ** 2 - 4 * record
    tmin = floor((total - sqrt(d)) / 2 + 1)
    tmax = ceil((total + sqrt(d)) / 2 - 1)
    tmin = clamp(tmin, 0, total)
    tmax = clamp(tmax, 0, total)

    return tmax - tmin + 1


def part_one():
    part_one_input = zip(*[line.strip().split(':')[1].split()
                         for line in input])
    ways_to_win = []
    for total, record in part_one_input:
        total = int(total)
        record = int(record)
        ways_to_win.append(solve(total, record))

    return reduce(operator.mul, ways_to_win, 1)


print(f'Part One: {part_one()}')


def part_two():
    part_two_input = [''.join(line.strip().split(':')[1].split())
                      for line in input]
    total = int(part_two_input[0])
    record = int(part_two_input[1])
    return solve(total, record)


print(f'Part Two: {part_two()}')
