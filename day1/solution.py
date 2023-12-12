input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()


def part_one():
    sum = 0
    for line in input:
        digits = [int(char) for char in line if char.isdigit()]
        sum += digits[0] * 10 + digits[-1]

    return sum


print(f'Part One: {part_one()}')


def part_two():
    text_digits = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }

    sum = 0
    for line in input:
        digits = [(int(char), i)
                  for i, char in enumerate(line) if char.isdigit()]
        digits.extend([(value, line.find(str))
                      for str, value in text_digits.items() if line.find(str) != -1])
        digits.extend([(value, line.rfind(str))
                      for str, value in text_digits.items() if line.rfind(str) != -1])
        sum += min(digits, key=lambda x: x[1])[0] * 10
        sum += max(digits, key=lambda x: x[1])[0]

    return sum


print(f'Part Two: {part_two()}')
