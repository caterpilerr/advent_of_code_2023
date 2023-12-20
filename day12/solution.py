input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

data = []
for line in input:
    line = line.strip()
    pattern, broken = line.split(' ')
    pattern = pattern.strip()
    broken = list(map(int, broken.strip().split(',')))
    data.append((pattern, broken))


def rec(start_p, pattern, start_b, broken, variation, variations, cache):
    if (start_p, start_b) in cache:
        return cache[(start_p, start_b)]

    cache[(start_p, start_b)] = 0
    if start_b == len(broken):
        for i in range(start_p, len(pattern)):
            if pattern[i] == '#':
                return cache[(start_p, start_b)]

        ending = '.' * (len(pattern) - start_p)
        variations.add(''.join(variation) + ending)
        cache[(start_p, start_b)] += 1
        return cache[(start_p, start_b)]

    skippedBroken = False
    for i in range(start_p, len(pattern)):
        if pattern[i] == '.':
            continue

        if skippedBroken:
            return cache[(start_p, start_b)]

        if pattern[i] == '#':
            skippedBroken = True

        block = '.' * (i - start_p) + broken[start_b] * '#'
        current_len = i + broken[start_b]
        if current_len > len(pattern):
            continue

        is_interval_valid = True
        for j in range(i, min(len(pattern), current_len)):
            if pattern[j] == '.':
                is_interval_valid = False
                break

        if not is_interval_valid:
            continue

        free_end = i + broken[start_b]
        if free_end < len(pattern):
            if pattern[free_end] == '#':
                continue
            else:
                block += '.'

        variation.append(block)
        result = rec(current_len + 1, pattern,
                     start_b + 1, broken, variation, variations, cache)
        variation.pop()
        cache[(start_p, start_b)] += result

    return cache[(start_p, start_b)]


def part_one():
    sum = 0
    for pattern, broken in data:
        variations = set()
        variation = []
        cache = {}
        sum += rec(0, pattern, 0, broken, variation, variations, cache)
        continue
        # DEBUG variants visualization
        print(pattern, broken)
        for var in variations:
            print(var)
        print()
    return sum


print(f'Part One: {part_one()}')


def part_two():
    sum = 0
    for pattern, broken in data:
        pattern = '?'.join((pattern for _ in range(5)))
        broken = broken * 5
        variations = set()
        variation = []
        cache = {}
        sum += rec(0, pattern, 0, broken, variation, variations, cache)
        continue
        # DEBUG variants visualization
        print(pattern, broken)
        for var in variations:
            print(var)
        print()
    return sum


print(f'Part Two: {part_two()}')
