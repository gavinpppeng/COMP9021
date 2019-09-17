# Randomly generates a binary search tree with values from 0 up to 9, and displays it growing up.
#
# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, choice
from binary_tree_adt import *


def print_growing_up(tree):
    pass
    # Replace pass above with your code


# Possibly write additional function(s)


try:
    seed_arg, nb_of_nodes = (int(x) for x in
                             input('Enter two integers, with the second one between 0 and 10: '
                                   ).split()
                             )
    if nb_of_nodes < 0 or nb_of_nodes > 10:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(seed_arg)
data_pool = list(range(nb_of_nodes))
print(data_pool)
tree = BinaryTree()
for _ in range(nb_of_nodes):
    datum = choice(data_pool)
    tree.insert_in_bst(datum)
    data_pool.remove(datum)
print(tree)
print_growing_up(tree)
