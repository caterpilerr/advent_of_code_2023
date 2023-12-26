input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

input = [list(line.strip()) for line in input]


def tilt_north(board):
    for j in range(len(board[0])):
        free_space = 0
        for i in range(len(board)):
            if board[i][j] == 'O':
                while free_space < len(board) and board[free_space][j] != '.':
                    free_space += 1
                if free_space < i:
                    board[free_space][j] = 'O'
                    board[i][j] = '.'
            elif board[i][j] == '#':
                free_space = i + 1


def tilt_south(board):
    for j in range(len(board[0])):
        free_space = len(board) - 1
        for i in range(len(board) - 1, -1, -1):
            if board[i][j] == 'O':
                while free_space >= 0 and board[free_space][j] != '.':
                    free_space -= 1
                if free_space > i:
                    board[free_space][j] = 'O'
                    board[i][j] = '.'
            elif board[i][j] == '#':
                free_space = i - 1


def tilt_west(board):
    for i in range(len(board)):
        free_space = 0
        for j in range(len(board[0])):
            if board[i][j] == 'O':
                while free_space < len(board[0]) and board[i][free_space] != '.':
                    free_space += 1
                if free_space < j:
                    board[i][free_space] = 'O'
                    board[i][j] = '.'
            elif board[i][j] == '#':
                free_space = j + 1


def tilt_east(board):
    for i in range(len(board)):
        free_space = len(board[0]) - 1
        for j in range(len(board[0]) - 1, -1, -1):
            if board[i][j] == 'O':
                while free_space >= 0 and board[i][free_space] != '.':
                    free_space -= 1
                if free_space > j:
                    board[i][free_space] = 'O'
                    board[i][j] = '.'
            elif board[i][j] == '#':
                free_space = j - 1


def total_load(board):
    load = 0
    for i, line in enumerate(board):
        stones = sum(1 for char in line if char == 'O')
        load += stones * (len(board) - i)

    return load


def spin(board):
    tilt_north(board)
    tilt_west(board)
    tilt_south(board)
    tilt_east(board)


def part_one():
    board = [line.copy() for line in input]
    tilt_north(board)

    return total_load(board)


print(f'Part One: {part_one()}')


def part_two():
    cache = dict()
    spins = 10**9
    board = [line.copy() for line in input]
    for i in range(spins):
        spin(board)
        board_key = ''.join(''.join(line) for line in board)
        if board_key in cache:
            cycle = i - cache[board_key]
            offset = (spins - (i + 1)) % cycle
            for _ in range(offset):
                spin(board)
            break
        else:
            cache[board_key] = i

    return total_load(board)


print(f'Part Two: {part_two()}')
