from heapq import heappop, heappush
from collections import defaultdict


input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = [line.strip() for line in f.readlines()]


def parse_input(input):
    grid = dict()
    blocks = defaultdict(set)
    index = 1
    for line in input:
        start, end = (tuple(int(coord) for coord in point.split(','))
                      for point in line.split('~'))
        vector = tuple(1 if e != s else 0 for e, s in zip(end, start))
        while True:
            blocks[index].add(start)
            grid[start] = index
            if start == end:
                break
            start = tuple(s + v for s, v in zip(start, vector))
        index += 1

    return grid, blocks


def get_min_z(name):
    return min(p[2] for p in blocks[name])


def get_supports(grid, blocks):
    supported = defaultdict(set)
    basis = defaultdict(set)
    down_vec = (0, 0, -1)
    heap = []
    for name in blocks:
        heappush(heap, (get_min_z(name), name))
    while heap:
        name = heappop(heap)[1]
        is_falling = True
        while True:
            new_points = set()
            for point in blocks[name]:
                down_point = tuple(p + v for p, v in zip(point, down_vec))
                if down_point[2] == 0:
                    is_falling = False
                    break
                if down_point in grid and grid[down_point] != name:
                    supported[grid[down_point]].add(name)
                    basis[name].add(grid[down_point])
                    is_falling = False
                new_points.add(down_point)
            if not is_falling:
                break
            for point in blocks[name]:
                grid.pop(point)
            grid.update({point: name for point in new_points})
            blocks[name] = new_points

    return supported, basis


grid, blocks = parse_input(input)
supported, basis = get_supports(grid, blocks)


def part_one():
    disintegrated = 0
    for name in blocks:
        if name not in supported:
            disintegrated += 1
        elif all(len(basis[supported_block]) > 1 for supported_block in supported[name]):
            disintegrated += 1

    return disintegrated


print(f'Part One: {part_one()}')


def get_falling_blocks(name):
    falling = 0
    heap = []
    visited = set()
    current_basis = {k: v.copy() for k, v in basis.items()}
    for supported_block in supported[name]:
        heappush(heap, (get_min_z(supported_block), supported_block))
        current_basis[supported_block].discard(name)
    while heap:
        current = heappop(heap)[1]
        if not current_basis[current]:
            falling += 1
            for supported_block in supported[current]:
                current_basis[supported_block].discard(current)
                if supported_block not in visited:
                    heappush(heap, (get_min_z(supported_block), supported_block))
                    visited.add(supported_block)

    return falling


def part_two():
    result = sum(get_falling_blocks(name) for name in blocks)

    return result


print(f'Part Two: {part_two()}')
