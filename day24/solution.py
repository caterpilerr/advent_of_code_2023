import sympy

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = [line.strip() for line in f.readlines()]


points_data = [[tuple(int(item) for item in data.split(','))
                for data in line.split('@')] for line in input]


def get_linear_coef(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    if x1 == x2:
        return None, x1
    else:
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        return a, b


for i in range(len(points_data)):
    point, velocity = points_data[i]
    next_point = (point[0] + velocity[0], point[1] +
                  velocity[1], point[2] + velocity[2])
    a, b = get_linear_coef(point[:-1], next_point[:-1])
    points_data[i].extend([a, b])


def count_path_intersections(points_data, least, most, debug=False):
    intersections = 0
    for i in range(len(points_data)):
        for j in range(i + 1, len(points_data)):
            point1, velocity1, a1, b1 = points_data[i]
            point2, velocity2, a2, b2 = points_data[j]

            if a1 == a2:
                if debug:
                    print(f'{i} and {j} are parallel')
                continue

            x = (b2 - b1) / (a1 - a2)
            y = a1 * x + b1
            time1 = (x - point1[0]) / velocity1[0]
            time2 = (x - point2[0]) / velocity2[0]

            if time1 <= 0 or time2 <= 0:
                if debug:
                    print(f'{i} and {j} do not intersect')
                continue

            if x < least or x > most or y < least or y > most:
                if debug:
                    print(
                        f'{i} and {j} intersect at ({x}, {y}) but not in range')
                continue

            intersections += 1
            if debug:
                print(f'{i} and {j} intersect at ({x}, {y})')

    return intersections


def part_one():
    least = 200000000000000
    most = 400000000000000
    result = count_path_intersections(points_data, least, most)

    return result


print(f'Part One: {part_one()}')


def part_two():
    # xr0 + vxr * t = xi0 + vxi * t
    # t = (xr0 - xi0) / (vxi - vxr) = (yr0 - yi0) / (vyi - vyr) = (zr0 - zi0) / (vzi - vzr)
    # (xr0 - xi0) / (vxi - vxr) = (yr0 - yi0) / (vyi - vyr)
    # (xr0 - xi0) / (vxi - vxr) = (zr0 - zi0) / (vzi - vzr)
    # (xr0 - xi0) * (vzi - vzr) - (zr0 - zi0) * (vxi - vxr) = 0
    # (xr0 - xi0) * (vyi - vyr) - (yr0 - yi0) * (vxi - vxr) = 0
    xr0, yr0, zr0, vxr, vyr, vzr = sympy.symbols('xr0 yr0 zr0 vxr vyr vzr')
    equations = []
    for data in points_data[:4]:
        point, velocity = data[:2]
        xi0, yi0, zi0 = point
        vxi, vyi, vzi = velocity
        equations.append((xr0 - xi0) * (vzi - vzr) - (zr0 - zi0) * (vxi - vxr))
        equations.append((xr0 - xi0) * (vyi - vyr) - (yr0 - yi0) * (vxi - vxr))

    solution = sympy.solve(equations)
    assert len(solution) == 1
    solution = solution[0]

    return solution[xr0] + solution[yr0] + solution[zr0]


print(f'Part Two: {part_two()}')
