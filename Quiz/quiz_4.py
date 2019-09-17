# Randomly fills an array of size 10x10 with True and False, and outputs the number of blocks
# in the largest block construction, determined by rows of True's that can be stacked
# on top of each other.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randrange
import sys

dim = 10


def display_grid():
    for i in range(dim):
        print('     ', end='')
        print(' '.join(f'{int(e)}' for e in grid[i]))
    print()


def size_of_largest_construction():
    size_construction = []
    for i in range(dim-1, -1, -1):
        j1 = 0
        while j1 < dim:
            while j1 < dim and not grid[i][j1]:
                j1 += 1
            if j1 == dim-1:
                j2 = j1
                size_construction.append(construction_size(i, j1, j2))
                j2 += 1
                # print('hello world !!!!!!!!!!!!!!!!!!!!!!!')
            elif j1 == dim:
                # print('hello world!')
                break
            else:
                j2 = j1
                while j2 < dim and grid[i][j2]:
                    j2 += 1
                # print(f'i,j1,j2:{i}, {j1}, {j2}')
                size_construction.append(construction_size(i, j1, j2-1))
                # print(size_construction)
            j1 = j2
    if len(size_construction) == 0:
        return 0
    else:
        max_size_construction = max(size_construction)
        return max_size_construction


# If j1 <= j2 and the grid has a 1 at the intersection of row i and column j
# for all j in {j1, ..., j2}, then returns the number of blocks in the construction
# built over this line of blocks.
def construction_size(i, j1, j2):
    count = 0
    # print(f'i!!!!!!j1!!!!j2!!!!{i} and {j1}and{j2}')
    for j in range(j1, j2+1):
        if grid[i][j]:
            for row in range(i, -1, -1):
                if grid[row][j]:
                    count += 1
                    # print(f'row and j :!!!!{row} and {j} and {i}')
                else:
                    break
    return count


try:
    for_seed, n = input('Enter two integers, the second one being strictly positive: ').split()
    for_seed = int(for_seed)
    n = int(n)
    if n <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[bool(randrange(n)) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
# print(grid)
size = size_of_largest_construction()
if not size:
    print(f'The largest block construction has no block.')
elif size == 1:
    print(f'The largest block construction has 1 block.')
else:
    print(f'The largest block construction has {size_of_largest_construction()} blocks.')