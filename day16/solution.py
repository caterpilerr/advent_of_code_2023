from enum import Enum
from collections import deque, defaultdict

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


rules = {
    (Direction.UP,    '/'):  (Direction.RIGHT,),
    (Direction.UP,    '\\'): (Direction.LEFT,),
    (Direction.DOWN,  '/'):  (Direction.LEFT,),
    (Direction.DOWN,  '\\'): (Direction.RIGHT,),
    (Direction.LEFT,  '/'):  (Direction.DOWN,),
    (Direction.LEFT,  '\\'): (Direction.UP,),
    (Direction.RIGHT, '/'):  (Direction.UP,),
    (Direction.RIGHT, '\\'): (Direction.DOWN,),
    (Direction.UP,    '-'):  (Direction.LEFT, Direction.RIGHT),
    (Direction.DOWN,  '-'):  (Direction.LEFT, Direction.RIGHT),
    (Direction.LEFT,  '|'):  (Direction.UP,   Direction.DOWN),
    (Direction.RIGHT, '|'):  (Direction.UP,   Direction.DOWN),
}


def count_energized(x, y, direction, board):
    queue = deque()
    queue.append((x, y, direction))
    cache = set()
    energized_tiles = set()
    rules_default = defaultdict(lambda: [current_direction], rules)
    while queue:
        x, y, current_direction = queue.popleft()
        if (x, y, current_direction) in cache:
            continue

        cache.add((x, y, current_direction))
        energized_tiles.add((x, y))
        next_directions = rules_default[(current_direction, board[x][y])]

        for direction in next_directions:
            next_x, next_y = (x + direction.value[0], y + direction.value[1])
            if next_x < 0 or next_x >= len(board) or \
                    next_y < 0 or next_y >= len(board[0]):
                continue

            queue.append((next_x, next_y, direction))

    return len(energized_tiles)


board = [line.strip() for line in input]


def part_one():
    energized = count_energized(0, 0, Direction.RIGHT, board)
    return energized


print(f'Part One: {part_one()}')


def part_two():
    max_energized = 0
    for x in range(len(board)):
        left_val = count_energized(x, 0, Direction.RIGHT, board)
        right_val = count_energized(
            x, len(board[0]) - 1, Direction.LEFT, board)
        max_energized = max(max_energized, left_val, right_val)
    for y in range(len(board[0])):
        top_val = count_energized(0, y, Direction.DOWN, board)
        bot_val = count_energized(len(board) - 1, y, Direction.UP, board)
        max_energized = max(max_energized, top_val, bot_val)

    return max_energized


print(f'Part Two: {part_two()}')
