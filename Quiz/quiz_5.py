# Prompts the user for a nonnegative integer that codes a set S as follows:
# - Bit 0 codes 0
# - Bit 1 codes -1
# - Bit 2 codes 1
# - Bit 3 codes -2
# - Bit 4 codes 2
# - Bit 5 codes -3
# - Bit 6 codes 3
# ...
# Computes a derived nonnegative number that codes the set of running sums
# of the members of S when those are listed in increasing order.
#
# Computes the ordered list of members of a coded set.
#
# Written by Gavin and Eric Martin for COMP9021


import sys

try:
    encoded_set = int(input('Input a nonnegative integer: '))
    if encoded_set < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()


def display(L):
    print('{', end='')
    print(', '.join(str(e) for e in L), end='')
    print('}')


def decode(encoded_set):
    decode_result = []
    i = 0
    while encoded_set != 0:
        if i >= 0:
            if encoded_set % 2 != 0:
                decode_result.append(i)
            i = -1 * i
            i -= 1
        else:
            if encoded_set % 2 != 0:
                decode_result.append(i)
            i = i * -1
        encoded_set = encoded_set >> 1
        # print(encoded_set)
    decode_result = sorted(decode_result)
    return decode_result


def code_derived_set(encoded_set):
    code_derived = decode(encoded_set)
    sum_code_derived = 0
    code_derived_result = []
    for i in range(0, len(code_derived)):
        sum_code_derived = sum_code_derived + code_derived[i]
        code_derived_result.append(sum_code_derived)
    code_derived_result = sorted(list(set(code_derived_result)))
    # print(f'result is {code_derived_result}')
    result = 0
    for j in range(0, len(code_derived_result)):
        if code_derived_result[j] < 0:
            number = -code_derived_result[j] * 2 - 1
            result = result | 1 << number
        if code_derived_result[j] >= 0:
            number = code_derived_result[j] * 2
            result = result | 1 << number
    return result


print('The encoded set is: ', end='')
display(decode(encoded_set))
code_of_derived_set = code_derived_set(encoded_set)
print('The derived set is encoded as:', code_of_derived_set)
print('It is: ', end='')
display(decode(code_of_derived_set))
