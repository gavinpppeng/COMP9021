
def remove_consecutive_duplicates(word):
    '''
    >>> remove_consecutive_duplicates('')
    ''
    >>> remove_consecutive_duplicates('a')
    'a'
    >>> remove_consecutive_duplicates('ab')
    'ab'
    >>> remove_consecutive_duplicates('aba')
    'aba'
    >>> remove_consecutive_duplicates('aaabbbbbaaa')
    'aba'
    >>> remove_consecutive_duplicates('abcaaabbbcccabc')
    'abcabcabc'
    >>> remove_consecutive_duplicates('aaabbbbbaaacaacdddd')
    'abacacd'
    '''
    # Insert your code here (the output is returned, not printed out)
    return_word = []
    if word is '':
        return ''
    else:
        word_already_exist = []
        for i in range(len(word)):
            if word_already_exist is []:
                word_already_exist.append(word[i])
                return_word.append(word[i])
            elif word[i] in word_already_exist:
                continue
            else:
                return_word.append(word[i])
                word_already_exist = []
                word_already_exist.append(word[i])
    return ''.join(return_word)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
