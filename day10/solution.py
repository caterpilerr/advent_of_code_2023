from collections import deque
from math import ceil

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

input = [line.strip() for line in input]

X = len(input[0])
Y = len(input)

valid_pipes = {
    (0, 1): {'|', 'L', 'J', 'S'},
    (1, 0): {'-', 'J', '7', 'S'}
}

connections = {
    '|': [(0, 1)],
    '-': [(1, 0)],
    'L': [(1, 0)],
    'J': [],
    '7': [(0, 1)],
    'F': [(1, 0), (0, 1)],
    'S': [(0, 1), (1, 0)],
    '.': []
}


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.adjacent = []

    def add_adjacent(self, node):
        self.adjacent.append(node)
        node.adjacent.append(self)


def build_graph(input):
    parsed = dict()
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if (x, y) in parsed:
                current = parsed[(x, y)]
            else:
                current = Node(x, y)
                parsed[(x, y)] = current

            for dx, dy in connections[char]:
                next_x = x + dx
                next_y = y + dy
                if not 0 <= next_x < X or not 0 <= next_y < Y or \
                        not input[next_y][next_x] in valid_pipes[(dx, dy)]:
                    continue

                if not (next_x, next_y) in parsed:
                    parsed[(next_x, next_y)] = Node(next_x, next_y)

                current.add_adjacent(parsed[(next_x, next_y)])

            if char == 'S':
                start = parsed[(x, y)]

    return start


def get_loop_points(start: Node):
    loop_set = set()
    current = start
    next = start.adjacent[0]
    while True:
        loop_set.add((current.x, current.y))
        follow = next.adjacent[0]
        if follow == current:
            follow = next.adjacent[1]
        current = next
        next = follow
        if current == start:
            break

    return loop_set


def part_one():
    start = build_graph(input)
    cycle_length = len(get_loop_points(start))
    return ceil((cycle_length - 1) / 2)


print(f'Part One: {part_one()}')


def cross_product(vector1, vector2):
    return vector1[0]*vector2[1] - vector1[1]*vector2[0]


def rotate_vector_90(vector, direction):
    x, y = vector
    if direction == 'R':
        return y, -x
    elif direction == 'L':
        return -y, x


def get_outer_points(start: Node, loop_set):
    left_points = set()
    right_points = set()
    current = start
    next = start.adjacent[0]
    prev_vector = next.x - current.x, next.y - current.y
    rotation_direction = 0
    while True:
        current_vector = next.x - current.x, next.y - current.y
        left_vector = rotate_vector_90(current_vector, 'L')
        right_vector = rotate_vector_90(current_vector, 'R')

        first_left = current.x + left_vector[0], current.y + left_vector[1]
        if 0 <= first_left[1] < Y and 0 <= first_left[0] < X and \
                not first_left in loop_set:
            left_points.add(first_left)

        second_left = next.x + left_vector[0], next.y + left_vector[1]
        if 0 <= second_left[1] < Y and 0 <= second_left[0] < X and \
                not second_left in loop_set:
            left_points.add(second_left)

        first_right = current.x + right_vector[0], current.y + right_vector[1]
        if 0 <= first_right[1] < Y and 0 <= first_right[0] < X and \
                not first_right in loop_set:
            right_points.add(first_right)

        second_right = next.x + right_vector[0], next.y + right_vector[1]
        if 0 <= second_right[1] < Y and 0 <= second_right[0] < X and \
                not second_right in loop_set:
            right_points.add(second_right)

        if current_vector != prev_vector:
            direction = cross_product(current_vector, prev_vector)
            rotation_direction += direction

        follow = next.adjacent[0]
        if follow == current:
            follow = next.adjacent[1]

        prev_vector = current_vector
        current = next
        next = follow

        if current == start:
            break

    if rotation_direction < 0:
        return right_points
    else:
        return left_points


def enclosed(x, y, outer, loop, visited):
    queue = deque()
    island = set()
    queue.append((x, y))
    free = False
    while queue:
        current = queue.popleft()
        x, y = current
        if current in visited:
            continue
        visited.add(current)
        if not 0 <= x < X or not 0 <= y < Y:
            free = True
            continue
        if current in loop:
            continue
        if current in outer:
            free = True
        island.add(current)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            queue.append((x + dx, y + dy))

    return len(island) if not free else 0


def part_two():
    start = build_graph(input)
    loop = get_loop_points(start)
    outer = get_outer_points(start, loop)
    visited = set()
    enclosed_points = 0
    for y in range(Y):
        for x in range(X):
            if (x, y) not in visited:
                enclosed_points += enclosed(x, y, outer, loop, visited)

    return enclosed_points


print(f'Part Two: {part_two()}')
