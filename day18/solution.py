import numpy as np

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()


commands = []
for line in input:
    command, steps, color = line.strip().split()
    steps = int(steps)
    color = color[1:-1]
    commands.append((command, steps, color))

directions = {
    'U': np.array([-1, 0]),
    'D': np.array([1, 0]),
    'L': np.array([0, -1]),
    'R': np.array([0, 1])}


def get_area(points):
    area = 0
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        width = points[j][0] - points[i][0]
        height = points[j][1]
        area += width * height

    return int(abs(area))


def get_real_vertices(points):
    left_points = []
    right_points = []
    rotation_direction = 0
    i = 0
    while True:
        next_i = (i + 1) % len(points)
        prev_i = (i - 1) % len(points)
        next_vector = points[next_i] - points[i]
        prev_vector = points[i] - points[prev_i]

        next_vector_norm = next_vector / np.linalg.norm(next_vector)
        prev_vector_norm = prev_vector / np.linalg.norm(prev_vector)
        direction = np.cross(next_vector, prev_vector)
        if direction >= 0:
            left_component = points[i] + 0.5 * \
                (next_vector_norm - prev_vector_norm)
            right_component = points[i] + 0.5 * \
                (prev_vector_norm - next_vector_norm)
        else:
            left_component = points[i] + 0.5 * \
                (prev_vector_norm - next_vector_norm)
            right_component = points[i] + 0.5 * \
                (next_vector_norm - prev_vector_norm)

        left_points.append(left_component)
        right_points.append(right_component)
        rotation_direction += direction

        i = (i + 1) % len(points)
        if np.array_equal(points[i], points[0]):
            break

    if rotation_direction >= 0:
        return right_points
    else:
        return left_points


def decode_command(code):
    code_commands = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}
    steps = int(code[1:6], base=16)
    command = code_commands[int(code[6:])]

    return command, steps


def calculate_area(commands, decode=False):
    current = np.array([0, 0], dtype=np.int64)
    vertices = [current]
    for command in commands:
        if decode:
            real_command, real_steps = decode_command(command[2])
            vector = directions[real_command]
            steps = real_steps
        else:
            vector = directions[command[0]]
            steps = command[1]
        current = current + steps * vector
        vertices.append(current)

    real_borders = get_real_vertices(vertices[:-1])

    return get_area(real_borders)


def part_one():
    return calculate_area(commands)


print(f'Part One: {part_one()}')


def part_two():
    return calculate_area(commands, decode=True)


print(f'Part Two: {part_two()}')
