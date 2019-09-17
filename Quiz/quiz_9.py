# Randomly fills a grid of size 7 x 7 with NE, SE, SW, NW,
# meant to represent North-East, South-East, North-West, South-West,
# respectively, and starting from the cell in the middle of the grid,
# determines, for each of the 4 corners of the grid, the preferred path amongst
# the shortest paths that reach that corner, if any. At a given cell, it is possible to move
# according to any of the 3 directions indicated by the value of the cell;
# e.g., from a cell storing NE, it is possible to move North-East, East, or North.
# At any given point, one prefers to move diagonally, then horizontally,
# and vertically as a last resort.
#
# Written by Gavin and Eric Martin for COMP9021


import sys
from random import seed, choice
from queue_adt import *


def display_grid():
    for row in grid:
        print('    ', *row)


def preferred_paths_to_corners():
    path = {}
    pass_route = [[False for _ in range(dim)] for _ in range(dim)]
    reverse_path = [[(i, j) for i in range(dim)] for j in range(dim)]
    # print(pass_route)
    queue = Queue()
    queue.enqueue((3, 3))
    pass_route[3][3] = True
    while not queue.is_empty():
        (i, j) = queue.dequeue()
        if (i, j) not in corners:
                # print(i,j)
                if grid[i][j] == 'NE':
                    if i-1 >= 0 and j+1 <= (dim-1) and not pass_route[i-1][j+1]:
                        a = i - 1
                        b = j + 1
                        queue.enqueue((a, b))
                        pass_route[a][b] = True
                        reverse_path[a][b] = (i, j)
                    if j+1 <= (dim-1) and not pass_route[i][j+1]:
                        b = j + 1
                        queue.enqueue((i, b))
                        pass_route[i][b] = True
                        reverse_path[i][b] = (i, j)
                    if i-1 >= 0 and not pass_route[i-1][j]:
                        a = i - 1
                        queue.enqueue((a, j))
                        pass_route[a][j] = True
                        reverse_path[a][j] = (i, j)
                elif grid[i][j] == 'SE':
                    if i + 1 <= (dim-1) and j + 1 <= (dim - 1) and not pass_route[i+1][j+1]:
                        a = i + 1
                        b = j + 1
                        queue.enqueue((a, b))
                        pass_route[a][b] = True
                        reverse_path[a][b] = (i, j)
                    if j + 1 <= (dim - 1) and not pass_route[i][j+1]:
                        b = j + 1
                        queue.enqueue((i, b))
                        pass_route[i][b] = True
                        reverse_path[i][b] = (i, j)
                    if i + 1 <= (dim-1) and not pass_route[i+1][j]:
                        a = i + 1
                        queue.enqueue((a, j))
                        pass_route[a][j] = True
                        reverse_path[a][j] = (i, j)
                elif grid[i][j] == 'SW':
                    if i + 1 <= (dim - 1) and j - 1 >= 0 and not pass_route[i+1][j-1]:
                        a = i + 1
                        b = j - 1
                        queue.enqueue((a, b))
                        pass_route[a][b] = True
                        reverse_path[a][b] = (i, j)
                    if j - 1 >= 0 and not pass_route[i][j-1]:
                        b = j - 1
                        queue.enqueue((i, b))
                        pass_route[i][b] = True
                        reverse_path[i][b] = (i, j)
                    if i + 1 <= (dim - 1) and not pass_route[i+1][j]:
                        a = i + 1
                        queue.enqueue((a, j))
                        pass_route[a][j] = True
                        reverse_path[a][j] = (i, j)
                else:               # NW
                    if i - 1 >= 0 and j - 1 >= 0 and not pass_route[i-1][j-1]:
                        a = i - 1
                        b = j - 1
                        queue.enqueue((a, b))
                        pass_route[a][b] = True
                        reverse_path[a][b] = (i, j)
                    if j - 1 >= 0 and not pass_route[i][j-1]:
                        b = j - 1
                        queue.enqueue((i, b))
                        pass_route[i][b] = True
                        reverse_path[i][b] = (i, j)
                    if i - 1 >= 0 and not pass_route[i-1][j]:
                        a = i - 1
                        queue.enqueue((a, j))
                        pass_route[a][j] = True
                        reverse_path[a][j] = (i, j)

# for print
    for x, y in corners:
        # print(x, y)
        # print(pass_route[x][y])
        if pass_route[x][y]:
            point_x = x
            point_y = y
            path[(x, y)] = [reverse_path[point_x][point_y]]
            while reverse_path[point_x][point_y] != (3, 3):
                point_x, point_y = reverse_path[point_x][point_y]
                path[(x, y)].append(reverse_path[point_x][point_y])
            path[(x, y)].reverse()
            path[(x, y)].append((x, y))

# for reverse
    path_result = {}
    for path_key, path_list in path.items():
        # print(f'Hello {path_key[0]} and {path_key[1]}')
        path_result[(path_key[1], path_key[0])] = []
        for path_return in path_list:
            path_result[(path_key[1], path_key[0])].append((path_return[1], path_return[0]))
        # print(f'result is {path_result}')

    return path_result


try:
    seed_arg = int(input('Enter an integer: '))
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(seed_arg)
size = 3
dim = 2 * size + 1
grid = [[0] * dim for _ in range(dim)]
directions = 'NE', 'SE', 'SW', 'NW'

grid = [[choice(directions) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
# print(grid[3])
# print(directions[0][1])


corners = (0, 0), (dim - 1, 0), (dim - 1, dim - 1), (0, dim - 1)
paths = preferred_paths_to_corners()
if not paths:
    print('There is no path to any corner')
    sys.exit()
for corner in corners:
    if corner not in paths:
        print(f'There is no path to {corner}')
    else:
        print(f'The preferred path to {corner} is:')
        print('  ', paths[corner])
