input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

test_input = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''.splitlines()

# input = test_input

seeds = [int(i) for i in input[0].split(':')[1].split()]

stages = [[] for _ in range(7)]
i = 0
for line in input[2:]:
    line = line.strip()
    if line == '':
        i += 1
    elif not line[0].isdigit():
        continue
    else:
        stages[i].append(list(map(int, line.split())))

for stage in stages:
    stage.sort(key=lambda x: x[1])


def binary_search(value, stage):
    l = 0
    r = len(stage) - 1
    while l <= r:
        mid = (l + r) // 2
        rule = stage[mid]
        if rule[1] <= value:
            l = mid + 1
        else:
            r = mid - 1

    if r >= 0:
        rule = stage[r]
        offset = value - rule[1]
        if offset < rule[2]:
            return rule[0] + offset

    return value


def part_one():
    current = seeds.copy()
    for i in range(len(current)):
        for stage in stages:
            current[i] = binary_search(current[i], stage)

    return min(current)


print(f'Part One: {part_one()}')


def get_next(input):
    for pair in input:
        current = pair[0]
        while current < pair[0] + pair[1]:
            yield current
            current += 1


def part_two():
    current = list(zip(*[iter(seeds)] * 2))
    min_loc = float('inf')
    for value in get_next(current):
        for stage in stages:
            value = binary_search(value, stage)
        min_loc = min(min_loc, value)

    return min_loc


print(f'Part Two: {part_two()}')
