import math
from functools import reduce

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

instruction = input[0].strip()
nodes = {}
for line in input[2:]:
    name, adjacent = (data.strip() for data in line.split('='))
    nodes[name] = tuple(adjacent[1:-1].split(', '))


def part_one():
    current = 'AAA'
    instruction_i = 0
    steps = 0
    while current != 'ZZZ':
        if instruction[instruction_i] == 'R':
            current = nodes[current][1]
        else:
            current = nodes[current][0]
        steps += 1
        instruction_i = (instruction_i + 1) % len(instruction)

    return steps


print(f'Part One: {part_one()}')


def next_z(node_data, cache):
    node, instruction_i = node_data
    cache_key = (node, instruction_i)
    if cache_key in cache:
        return cache[cache_key]

    current = node
    current_i = instruction_i
    steps = 0
    while True:
        if instruction[current_i] == 'R':
            current = nodes[current][1]
        else:
            current = nodes[current][0]
        steps += 1
        current_i = (current_i + 1) % len(instruction)
        if current.endswith('Z'):
            break

    cache[cache_key] = ((current, current_i), steps)

    return cache[cache_key]


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def lcm_of_list(numbers):
    return reduce(lcm, numbers)


def part_two():
    current_nodes = [(node, 0) for node in nodes if node.endswith('A')]

    cache = {}
    steps = [0] * len(current_nodes)
    cycles = [0] * len(current_nodes)
    max_steps = float('inf')

    while True:
        for i, node in enumerate(current_nodes):
            if steps[i] >= max_steps:
                continue
            next, steps_to_next = next_z(node, cache)
            if cycles[i] == 0 and next == current_nodes[i]:
                cycles[i] = steps[i]
            current_nodes[i] = next
            steps[i] += steps_to_next

        if len(set(steps)) == 1:
            return steps[0]
        elif all(cycles):
            return lcm_of_list(cycles)
        else:
            max_steps = max(steps)


print(f'Part Two: {part_two()}')
