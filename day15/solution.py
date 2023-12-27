input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

commands = []
for line in input:
    commands.extend(line.strip().split(','))


def hash(string):
    current = 0
    for char in string:
        current += ord(char)
        current *= 17
        current %= 256

    return current


def part_one():
    sum = 0
    for line in commands:
        sum += hash(line.strip())

    return sum


print(f'Part One: {part_one()}')


def part_two():
    boxes = [[] for _ in range(256)]
    for line in commands:
        line = line.strip()
        if '=' in line:
            label, focal = line.split('=')
        else:
            label, focal = line.split('-')

        box = boxes[hash(label)]
        # add command
        if focal:
            for i, item in enumerate(box):
                if item[0] == label:
                    box[i][1] = int(focal)
                    break
            else:
                box.append([label, int(focal)])
        # remove command
        else:
            for i, item in enumerate(box):
                if item[0] == label:
                    box.pop(i)
                    break

    focusing_power = 0
    for i, box in enumerate(boxes):
        for j, item in enumerate(box):
            focusing_power += (i + 1) * (j + 1) * (item[1])

    return focusing_power


print(f'Part Two: {part_two()}')
