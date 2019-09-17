'''
Given a word w, a good subsequence of w is defined as a word w' such that
- all letters in w' are different;
- w' is obtained from w by deleting some letters in w.

Returns the list of all good subsequences, without duplicates, in lexicographic order
(recall that the sorted() function sorts strings in lexicographic order).

The number of good sequences grows exponentially in the number of distinct letters in w,
so the function will be tested only for cases where the latter is not too large.

'''

import itertools


def find_subset(find_list):
    list_tuple = []
    return_list = []
    for i in range(1, len(find_list) + 1):
        list3 = list(itertools.permutations(find_list, i))
        list_tuple = list_tuple + list3
    for j in range(len(list_tuple)):
        list_separate = list(itertools.chain(list_tuple[j]))
        k = 0
        list_add = ''
        while k < len(list_separate):
            list_add = list_add + list_separate[k]
            k += 1
        return_list.append(list_add)
    # print(return_list)
    return return_list


def good_subsequences(word):
    '''
    >>> good_subsequences('')
    ['']
    >>> good_subsequences('aaa')
    ['', 'a']
    >>> good_subsequences('aaabbb')
    ['', 'a', 'ab', 'b']
    >>> good_subsequences('aaabbc')
    ['', 'a', 'ab', 'abc', 'ac', 'b', 'bc', 'c']
    >>> good_subsequences('aaabbaaa')
    ['', 'a', 'ab', 'b', 'ba']
    >>> good_subsequences('abbbcaaabccc')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb']
    >>> good_subsequences('abbbcaaabcccaaa')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb', 'cba']
    >>> good_subsequences('abbbcaaabcccaaabbbbbccab')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb', 'cba']
    '''
    no_dupli_subsequences = ['']
    word_already_exit = []
    no_dupli_list = []
    alphabet = set()
    return_list =[]
    # no duplicate list!
    if word == '':
        return no_dupli_subsequences
    else:
        for i in range(len(word)):
            if word_already_exit is []:
                word_already_exit.append(word[i])
                no_dupli_list.append(word[i])
            elif word[i] in word_already_exit:
                continue
            else:
                no_dupli_list.append(word[i])
                word_already_exit = []
                word_already_exit.append(word[i])
    for i in range(len(no_dupli_list)):
        alphabet.add(no_dupli_list[i])
    alphabet_list = list(alphabet)
    # print(no_dupli_list)
    alphabet_list_arrange = find_subset(alphabet_list)
    no_dupli_subsequences = no_dupli_subsequences + alphabet_list
    # print(no_dupli_subsequences)
    for i in range(len(alphabet_list_arrange)):
        if len(alphabet_list_arrange[i]) == 1:
            continue
        else:
            j = 0
            while j < len(alphabet_list_arrange[i]):
                k = 0
                while k < len(no_dupli_list):
                    if no_dupli_list[k] == alphabet_list_arrange[i][j]:
                        j += 1
                        k += 1
                        if j == len(alphabet_list_arrange[i]):
                            no_dupli_subsequences.append(alphabet_list_arrange[i])
                            break
                    else:
                        k += 1
                if k == len(no_dupli_list):
                    break
    return sorted(no_dupli_subsequences)

# Possibly define another function
                

if __name__ == '__main__':
    import doctest
    doctest.testmod()
