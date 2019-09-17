# Randomly fills an array of size 10x10 True and False, displayed as 1 and 0,
# and outputs the number chess knights needed to jump from 1s to 1s
# and visit all 1s (they can jump back to locations previously visited).
#
# Written by Gavin and Eric Martin for COMP9021


from random import seed, randrange
import sys


dim = 10


def display_grid():
    for i in range(dim):
        print('     ', end = '')
        print(' '.join(grid[i][j] and '1' or '0' for j in range(dim)))
    print()


def explore_board():
    count = 0
    global grid
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j]:
                a = i
                b = j
                # print(a, b)
                explore_the_board(a, b)
                count += 1
    return count


def explore_the_board(i, j):
    global grid
    if grid[i][j]:
        # print(i, j)
        grid[i][j] = False
        if 0 <= i - 2 <= 9 and 0 <= j - 1 <= 9:
            explore_the_board(i-2, j-1)           # north
        if 0 <= i - 2 <= 9 and 0 <= j + 1 <= 9:
            explore_the_board(i-2, j+1)
        if 0 <= i + 2 <= 9 and 0 <= j - 1 <= 9:
            explore_the_board(i+2, j-1)             # south
        if 0 <= i + 2 <= 9 and 0 <= j + 1 <= 9:
            explore_the_board(i+2, j+1)
        if 0 <= i - 1 <= 9 and 0 <= j - 2 <= 9:
            explore_the_board(i-1, j-2)             # west
        if 0 <= i + 1 <= 9 and 0 <= j - 2 <= 9:
            explore_the_board(i+1, j-2)
        if 0 <= i - 1 <= 9 and 0 <= j + 2 <= 9:
            explore_the_board(i-1, j+2)             # east
        if 0 <= i + 1 <= 9 and 0 <= j + 2 <= 9:
            explore_the_board(i+1, j+2)
    else:
        return


try:
    for_seed, n = (int(i) for i in input('Enter two integers: ').split())
    if not n:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
if n > 0:
    grid = [[randrange(n) > 0 for _ in range(dim)] for _ in range(dim)]
else:
    grid = [[randrange(-n) == 0 for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
nb_of_knights = explore_board()
if not nb_of_knights:
    print('No chess knight has explored this board.')
elif nb_of_knights == 1:
    print(f'At least 1 chess knight has explored this board.')
else:
    print(f'At least {nb_of_knights} chess knights have explored this board')
