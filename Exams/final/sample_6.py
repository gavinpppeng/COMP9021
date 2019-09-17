'''
is_valid_prefix_expression(expression) checks whether the string expression
represents a correct infix expression (where arguments follow operators).

evaluate_prefix_expression(expression) returns the result of evaluating expression.

For expression to be syntactically correct:
- arguments have to represent integers, that is, tokens that can be converted to an integer
  thanks to int();
- operators have to be any of +, -, * and /;
- at least one space has to separate two consecutive tokens.

Assume that evaluate_prefix_expression() is only called on syntactically correct expressions,
and that / (true division) is applied to a denominator that is not 0.

You might find the reversed() function, the split() string method,
and the pop() and append() list methods useful.
'''

import re
from operator import add, sub, mul, truediv


class ListNonEmpty(Exception):
    pass


def is_valid_prefix_expression(expression):
    '''
    >>> is_valid_prefix_expression('12')
    Correct prefix expression
    >>> is_valid_prefix_expression('+ 12 4')
    Correct prefix expression
    >>> is_valid_prefix_expression('- + 12 4 10')
    Correct prefix expression
    >>> is_valid_prefix_expression('+ - + 12 4 10 * 11 4')
    Correct prefix expression
    >>> is_valid_prefix_expression('/ + - + 12 4 10 * 11 4 5')
    Correct prefix expression
    >>> is_valid_prefix_expression('+ / + - + 12 4 10 * 11 4 5 - 80 82 ')
    Correct prefix expression
    >>> is_valid_prefix_expression('twelve')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('2 3')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ + 2 3')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+1 2')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ / 1 2 *3 4')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+1 2')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ +1 2')
    Correct prefix expression
    >>> is_valid_prefix_expression('++1 2')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ +1 -2')
    Correct prefix expression
    '''
    stack = []
    try:
        ex_list = []
        ex_digit = []
        operator = ['+', '-', '*', '/']
        expression = re.split(r' +', expression)
        for i in range(len(expression)):
            if len(expression[i]) == 0:
                continue
            else:
                if expression[i] in operator:
                    ex_list.append(expression[i])
                else:
                    ex_list.append(int(expression[i]))
        ex_pre_list = list(reversed(ex_list))
        # print(ex_pre_list)
        while len(ex_pre_list) != 0:
            op_or_dig = ex_pre_list.pop(0)
            if op_or_dig not in operator:
                ex_digit.append(op_or_dig)
            elif op_or_dig in operator:
                if len(ex_digit) <= 1:
                    raise IndexError
                else:
                    a = ex_digit.pop()
                    b = ex_digit.pop()
                    if op_or_dig == '+':
                        result = add(a, b)
                    elif op_or_dig == '-':
                        result = sub(a, b)
                    elif op_or_dig == '*':
                        result = mul(a, b)
                    else:
                        result = truediv(a, b)
                    ex_digit.append(result)

        # print(ex_digit)
        if len(ex_digit) != 1:
            raise ListNonEmpty

    # - IndexError is raised in particular when trying to pop from an empty list
    # - ValueError is raised in particular when trying to convert to an int
    #   a string that cannot be converted to an int
    # - ListNonEmpty is expected to be raised when a list is found out not to be empty
    except (IndexError, ValueError, ListNonEmpty):
        print('Incorrect prefix expression')
    else:
        print('Correct prefix expression')
    
    
def evaluate_prefix_expression(expression):
    '''
    >>> evaluate_prefix_expression('12')
    12
    >>> evaluate_prefix_expression('+ 12 4')
    16
    >>> evaluate_prefix_expression('- + 12 4 10')
    6
    >>> evaluate_prefix_expression('+ - + 12 4 10 * 11 4')
    50
    >>> evaluate_prefix_expression('/ + - + 12 4 10 * 11 4 5')
    10.0
    >>> evaluate_prefix_expression('+ / + - + 12 4 10 * 11 4 5 - 80 82 ')
    8.0
    >>> evaluate_prefix_expression('+ +1 2')
    3
    >>> evaluate_prefix_expression('+ +1 -2')
    -1
    '''
    ex_list = []
    ex_digit = []
    operator = ['+', '-', '*', '/']
    expression = re.split(r' +', expression)
    for i in range(len(expression)):
        if len(expression[i]) == 0:
            continue
        else:
            if expression[i] in operator:
                ex_list.append(expression[i])
            else:
                ex_list.append(int(expression[i]))
    ex_pre_list = list(reversed(ex_list))
    while len(ex_pre_list) != 0:
        op_or_dig = ex_pre_list.pop(0)
        if op_or_dig not in operator:
            ex_digit.append(op_or_dig)
        elif op_or_dig in operator:
            if len(ex_digit) <= 1:
                raise IndexError
            else:
                a = ex_digit.pop()
                b = ex_digit.pop()
                if op_or_dig == '+':
                    result = add(a, b)
                elif op_or_dig == '-':
                    result = sub(a, b)
                elif op_or_dig == '*':
                    result = mul(a, b)
                else:
                    result = truediv(a, b)
                ex_digit.append(result)
    if len(ex_digit) != 1:
        raise ListNonEmpty
    else:
        return ex_digit[0]


if __name__ == '__main__':
    import doctest
    doctest.testmod()   
