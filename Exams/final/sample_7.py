import re
'''
Tries and find a word in a text file that represents a grid of words, all of the same length.
There is only one word per line in the file.
The letters that make up a word can possibly be separated by an arbitrary number of spaces,
and there can also be spaces at the beginning or at the end of a word,
and there can be lines consisting of nothing but spaces anywhere in the file.
Assume that the file stores data as expected.

A word can be read horizontally from left to right,
or vertically from top to bottom,
or diagonally from top left to bottom right
(this is more limited than the lab exercise).
The locations are represented as a pair (line number, column number),
starting the numbering with 1 (not 0).
'''


def find_word(filename, word):
    '''
    >>> find_word('word_search_1.txt', 'PLATINUM')
    PLATINUM was found horizontally (left to right) at position (10, 4)
    >>> find_word('word_search_1.txt', 'MANGANESE')
    MANGANESE was found horizontally (left to right) at position (11, 4)
    >>> find_word('word_search_1.txt', 'LITHIUM')
    LITHIUM was found vertically (top to bottom) at position (2, 14)
    >>> find_word('word_search_1.txt', 'SILVER')
    SILVER was found vertically (top to bottom) at position (2, 13)
    >>> find_word('word_search_1.txt', 'SODIUM')
    SODIUM was not found
    >>> find_word('word_search_1.txt', 'TITANIUM')
    TITANIUM was not found
    >>> find_word('word_search_2.txt', 'PAPAYA')
    PAPAYA was found diagonally (top left to bottom right) at position (1, 9)
    >>> find_word('word_search_2.txt', 'RASPBERRY')
    RASPBERRY was found vertically (top to bottom) at position (5, 14)
    >>> find_word('word_search_2.txt', 'BLUEBERRY')
    BLUEBERRY was found horizontally (left to right) at position (13, 5)
    >>> find_word('word_search_2.txt', 'LEMON')
    LEMON was not found
    '''
    with open(filename) as file:
        grid = None
        # Insert your code here
        grid = []
        grid1 = []
        file_content = file.read()
        for i in file_content:
            if ord(i) == 10:
                if len(grid1) != 0:
                    grid.append(grid1)
                grid1 = []
            if 65 <= ord(i) <= 90 or 97 <= ord(i) <= 122:
                grid1.append(i)
        # A one liner that sets grid to the appropriate value is enough.
        location = find_word_horizontally(grid, word)
        found = False
        if location:
            found = True
            print(word, 'was found horizontally (left to right) at position', location)
        location = find_word_vertically(grid, word)
        if location:
            found = True
            print(word, 'was found vertically (top to bottom) at position', location)
        location = find_word_diagonally(grid, word)
        if location:
            found = True
            print(word, 'was found diagonally (top left to bottom right) at position', location)
        if not found:
            print(word, 'was not found')
    
    
def find_word_horizontally(grid, word):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            k = 0
            j1 = j
            while word[k] == grid[i][j1]:
                if k == len(word) - 1:
                    return (i+1, j+1)
                k += 1
                j1 += 1
                if k >= len(word) or j1 >= len(grid[0]):
                    break
    return


def find_word_vertically(grid, word):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            k = 0
            i1 = i
            while word[k] == grid[i1][j]:
                if k == len(word) - 1:
                    return (i+1, j+1)
                k += 1
                i1 += 1
                if k >= len(word) or i1 >= len(grid):
                    break
    return


def find_word_diagonally(grid, word):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            k = 0
            i1 = i
            j1 = j
            while word[k] == grid[i1][j1]:
                if k == len(word) - 1:
                    return (i+1, j+1)
                k += 1
                i1 += 1
                j1 += 1
                if k >= len(word) or i1 >= len(grid) or j1 >= len(grid[0]):
                    break
    return


if __name__ == '__main__':
    import doctest
    doctest.testmod()   
