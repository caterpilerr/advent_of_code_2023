from collections import deque


input_file = 'input.txt'
with open(input_file, 'r') as f:
    input_grid = [line.strip() for line in f.readlines()]


def find_start(input):
    start = 'S'
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == start:
                return i, j

    return None


def solve(x, y, steps):
    rock = '#'
    i = 0
    queue = deque([(x, y)])
    reached = set()
    result = None
    while i < steps:
        epoch = len(queue)
        for _ in range(epoch):
            x, y = queue.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_x, next_y = x + dx, y + dy
                if (next_x, next_y) in reached:
                    continue
                if 0 <= next_x < len(input_grid) and 0 <= next_y < len(input_grid[0]) and \
                        input_grid[next_x][next_y] != rock:
                    queue.append((next_x, next_y))
                    reached.add((next_x, next_y))

        i += 1
        result = len(reached)
        reached = set()

    return result


start = find_start(input_grid)


def part_one():
    return solve(*start, 64)


print(f'Part One: {part_one()}')


def part_two():
    steps = 26501365
    rows = len(input_grid)
    cols = len(input_grid[0])
    assert rows == cols
    assert rows % 2 == 1
    size = rows
    blocks = steps // size

    odd = solve(*start, size * 2 + 1)
    even = solve(*start, size * 2)

    even_cout = (2 * (blocks + 1) // 2 - 1) ** 2
    odd_cout = (2 * blocks // 2 - 1) ** 2

    last_block_steps = (steps - (size // 2 + 1)) - ((blocks - 1) * size)
    top_block = solve(size - 1, size // 2, last_block_steps)
    bot_block = solve(0, size // 2, last_block_steps)
    left_block = solve(size // 2, size - 1, last_block_steps)
    right_block = solve(size // 2, 0, last_block_steps)

    small_block_steps = last_block_steps - (size // 2 + 1)
    small_block_count = (2 * (blocks + 1) // 2 - 1)
    tr_small = solve(size - 1, 0, small_block_steps)
    tl_small = solve(size - 1, size - 1, small_block_steps)
    bl_small = solve(0, size - 1, small_block_steps)
    br_small = solve(0, 0, small_block_steps)

    big_block_steps = small_block_steps + size
    big_block_count = small_block_count - 1
    tr_big = solve(size - 1, 0, big_block_steps)
    tl_big = solve(size - 1, size - 1, big_block_steps)
    bl_big = solve(0, size - 1, big_block_steps)
    br_big = solve(0, 0, big_block_steps)

    return (odd*odd_cout + even*even_cout
            + top_block + bot_block + left_block + right_block
            + small_block_count*(tl_small + tr_small + bl_small + br_small) +
            + big_block_count*(tl_big + tr_big + bl_big + br_big))


print(f'Part Two: {part_two()}')
