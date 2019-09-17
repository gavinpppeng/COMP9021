
def f(N):
    '''
    >>> f(20)
    Here are your banknotes:
    $20: 1
    >>> f(40)
    Here are your banknotes:
    $20: 2
    >>> f(42)
    Here are your banknotes:
    $2: 1
    $20: 2
    >>> f(43)
    Here are your banknotes:
    $1: 1
    $2: 1
    $20: 2
    >>> f(45)
    Here are your banknotes:
    $5: 1
    $20: 2
    >>> f(2537)
    Here are your banknotes:
    $2: 1
    $5: 1
    $10: 1
    $20: 1
    $100: 25
    '''
    banknote_values = [1, 2, 5, 10, 20, 50, 100]
    banknote_values_dict = {1: 0, 2: 0, 5: 0, 10: 0, 20: 0, 50: 0, 100: 0}
    # Insert your code here
    for i in range(len(banknote_values)-1, -1, -1):
        while N >= banknote_values[i]:
            N -= banknote_values[i]
            banknote_values_dict[banknote_values[i]] += 1
    print('Here are your banknotes:')
    for key, value in banknote_values_dict.items():
        if value != 0:
            print(f'${key}: {value}')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
