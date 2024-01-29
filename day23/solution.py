from collections import deque

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()


def find_start(input_grid):
    for i in range(len(input_grid[0])):
        if input_grid[0][i] == '.':
            return (0, i)

    return None


def find_end(input_grid):
    for i in range(len(input_grid[-1])):
        if input_grid[-1][i] == '.':
            return (len(input_grid) - 1, i)

    return None


def find_longest_path(input, start, end, directions):
    longest_path = 0
    queue = deque([(start, set())])
    while queue:
        current, visited = queue.pop()
        while True:
            next_tiles = []
            visited.add(current)
            for i, j in directions[input[current[0]][current[1]]]:
                next_i, next_j = current[0] + i, current[1] + j
                if next_i < 0 or next_i >= len(input) or next_j < 0 or next_j >= len(input[0]):
                    continue
                if (next_i, next_j) in visited or input[next_i][next_j] == '#':
                    continue
                next_tiles.append((next_i, next_j))

            if len(next_tiles) == 1:
                current = next_tiles[0]
                continue

            if len(next_tiles) > 1:
                queue.extend((tile, set(visited))
                             for tile in next_tiles)
            else:
                if current == end:
                    longest_path = max(longest_path, len(visited))
            break

    return longest_path - 1


start = find_start(input)
end = find_end(input)


def part_one():
    directions = {
        '>': [(0, 1)],
        '<': [(0, -1)],
        '^': [(-1, 0)],
        'v': [(1, 0)],
        '.': [(0, 1), (0, -1), (-1, 0), (1, 0)]
    }

    return find_longest_path(input, start, end, directions)


print(f'Part One: {part_one()}')


class node():
    def __init__(self, id):
        self.id = id
        self.adjacent = set()

    def add_adjacent(self, adj):
        self.adjacent.add(adj)

    def __repr__(self):
        return f'{self.adjacent}'


def is_intersection(input, x, y):
    neighbors = 0
    for i, j in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
        next_i, next_j = x + i, y + j
        if next_i < 0 or next_i >= len(input) or next_j < 0 or next_j >= len(input[0]):
            continue
        if input[next_i][next_j] == '#':
            continue
        neighbors += 1

    return neighbors > 2


def build_graph(input, directions):
    pseduo_current = (start[0] + 1, start[1])
    graphs = dict([(start, node(start))])
    queue = deque([(start, pseduo_current)])
    visited = set([start])
    while queue:
        start_node_id, current = queue.popleft()
        path = 0
        while True:
            path += 1
            next_tiles = []
            visited.add(current)
            for i, j in directions[input[current[0]][current[1]]]:
                next_i, next_j = current[0] + i, current[1] + j
                if next_i < 0 or next_i >= len(input) or next_j < 0 or next_j >= len(input[0]):
                    continue
                if input[next_i][next_j] == '#':
                    continue
                next = (next_i, next_j)
                if is_intersection(input, *next) or next == end:
                    if next not in graphs:
                        graphs[next] = node(next)
                    adj = graphs[next]
                    adj.add_adjacent((start_node_id, path + 1))
                    start_node = graphs[start_node_id]
                    start_node.add_adjacent((adj.id, path + 1))
                if next in visited:
                    continue
                next_tiles.append((next_i, next_j))

            if len(next_tiles) == 1:
                current = next_tiles[0]
                continue

            if len(next_tiles) > 1:
                queue.extend((current, tile)
                             for tile in next_tiles)

            break

    return graphs


def find_longest_path_in_graph(graphs, start, end):
    def rec(node_id, visited):
        if node_id == end:
            return 0

        visited.add(node_id)
        max_path = float('-inf')
        for adj_id, weight in graphs[node_id].adjacent:
            if adj_id in visited:
                continue
            max_path = max(max_path, weight + rec(adj_id, visited))
        visited.remove(node_id)

        return max_path

    max_path = rec(start, set())

    return max_path


def part_two():
    directions = {
        '>': [(0, 1), (0, -1), (-1, 0), (1, 0)],
        '<': [(0, 1), (0, -1), (-1, 0), (1, 0)],
        '^': [(0, 1), (0, -1), (-1, 0), (1, 0)],
        'v': [(0, 1), (0, -1), (-1, 0), (1, 0)],
        '.': [(0, 1), (0, -1), (-1, 0), (1, 0)]
    }

    graphs = build_graph(input, directions)
    result = find_longest_path_in_graph(graphs, start, end)

    return result


print(f'Part Two: {part_two()}')
