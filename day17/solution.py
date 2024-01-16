from collections import deque

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

board = [line.strip() for line in input]


class Vector:
    __slots__ = ('x', 'y')

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def right(self):
        return Vector(self.y, -self.x)

    def left(self):
        return Vector(-self.y, self.x)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False


def min_route(data, inrow_limit=3, min_to_spin=1):
    result = float('inf')
    cache = {(0, 1, Vector(0, 1), 1): 0, (1, 0, Vector(1, 0), 1): 0}
    queue = deque()
    queue.append((0, 1, Vector(0, 1), 1, 0))
    queue.append((1, 0, Vector(1, 0), 1, 0))
    end = (len(data) - 1, len(data[0]) - 1)
    while queue:
        x, y, direction, inrow, total = queue.popleft()
        if inrow > inrow_limit:
            continue

        new_total = total + int(data[x][y])
        if (x, y) == end:
            result = min(result, new_total)
            continue

        cache[(x, y, direction, inrow)] = new_total
        directions = [direction]
        if inrow >= min_to_spin:
            directions.extend([direction.right(), direction.left()])

        for next_direction in directions:
            next_x, next_y = x + next_direction.x, y + next_direction.y
            if not (0 <= next_x < len(data) and 0 <= next_y < len(data[0])):
                continue

            new_inrow = inrow + 1 if direction == next_direction else 1
            state = (next_x, next_y, next_direction, new_inrow)
            if state not in cache or new_total < cache[state]:
                cache[state] = new_total
                queue.append((*state, new_total))

    return result


def part_one():
    result = min_route(board)

    return result


print(f'Part One: {part_one()}')


def part_two():
    result = min_route(board, 10, 4)

    return result


print(f'Part Two: {part_two()}')
