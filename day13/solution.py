input_file = 'input.txt'
with open(input_file, 'r') as f:
    item = f.readlines()

set = []
data = [set]
for line in item:
    line = line.strip()
    if line != '':
        set.append(line)
    else:
        set = []
        data.append(set)


def count_differences(list1, list2):
    return sum(a != b for a, b in zip(''.join(list1), ''.join(list2)))


def find_symmetry(lines, diff=0):
    len_lines = len(lines)
    for i in range(len_lines // 2):
        if count_differences(lines[:i+1], lines[i+1:2*(i+1)][::-1]) == diff:
            return i

        j = len_lines - i - 1
        if count_differences(lines[-i-1:], lines[-2*i-2:-i-1][::-1]) == diff:
            return j - 1

    return -1


def horizontal_symmetry(item, diff=0):
    rows = [''.join(line[col] for line in item) for col in range(len(item[0]))]
    return find_symmetry(rows, diff)


def vertical_symmetry(item, diff=0):
    rows = [row for row in item]
    return find_symmetry(rows, diff)


def part_one():
    sum = 0
    for item in data:
        lines_left = horizontal_symmetry(item) + 1
        lines_above = vertical_symmetry(item) + 1
        sum += lines_left + lines_above * 100

    return sum


print(f'Part One: {part_one()}')


def part_two():
    sum = 0
    for item in data:
        lines_left = horizontal_symmetry(item, 1) + 1
        lines_above = vertical_symmetry(item, 1) + 1
        sum += lines_left + lines_above * 100

    return sum


print(f'Part Two: {part_two()}')
