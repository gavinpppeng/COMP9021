# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, randrange

try:
    arg_for_seed = int(input('Enter an integer: '))
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
x = randrange(10 ** 10)
sum_of_digits_in_x = 0

# sum_x
sum_of_digits_in_x = sum(int(i) for i in str(x))

L = [randrange(10 ** 8) for _ in range(10)]

first_digit_greater_than_last = 0
same_first_and_last_digits = 0
last_digit_greater_than_first = 0

# first_last_comparing  第一个数字和最后一个数字的比较，数组分别是第一个比最后一个大，第一个和最后一个相等，第一个比最后一个小
for i in L:
    M = str(i)
    if M[0] > M[len(M) - 1]:
        first_digit_greater_than_last += 1
    elif M[0] == M[len(M) - 1]:
        same_first_and_last_digits += 1
    else:
        last_digit_greater_than_first += 1

# distinct_digits   求L中每个数分别出现了多少个不同的数字，先统计0-9分别出现了多少次，然后只要不是出现0次的，不同数字就增加1
distinct_digits = [0] * 9
for i in L:
    M = str(i)
    u = 0
    arr = [0] * 10

    while u < len(M):
        if int(M[u]) == 0:
            arr[0] += 1
        elif int(M[u]) == 1:
            arr[1] += 1
        elif int(M[u]) == 2:
            arr[2] += 1
        elif int(M[u]) == 3:
            arr[3] += 1
        elif int(M[u]) == 4:
            arr[4] += 1
        elif int(M[u]) == 5:
            arr[5] += 1
        elif int(M[u]) == 6:
            arr[6] += 1
        elif int(M[u]) == 7:
            arr[7] += 1
        elif int(M[u]) == 8:
            arr[8] += 1
        else:
            arr[9] += 1
        u += 1

    v = 0
    for k in arr:                       # 不同数字加1
        if k > 0:
            v += 1
    distinct_digits[v] += 1            # L中的这个数中有多少个不同数字已经计算出来，这个数有v个不同数字

# min_gap and max_gap  求第一个数字和最后一个数字的绝对值差值的最大最小值
min_gap = 10
max_gap = -1
for i in L:
    M = str(i)
    abs_value = abs(int(M[0]) - int(M[len(M) - 1]))
    if abs_value < min_gap:
        min_gap = abs_value
    if abs_value > max_gap:
        max_gap = abs_value

# first and last
# dictionary               构建字典的方法 dic[key]=value,其中key和value都是变量，如果key = ‘age’,value = 30，那么这个dic
#                          就会是 dic = {'age':30}
# first and last digits
# dictionary 计算第一个数字和最后一个数字出现的组合最多是多少次，这些组合分别是什么
seq = []
dictionary = {}
max_value = 0
first_and_last = set()
for i in L:
    M = str(i)
    seq.append(
        M[0] + M[len(M) - 1])  # build a list, put the first and last digits in it, and then using it in dictionary

for k in range(len(L)):  # update can add some new dictionary elements in old dictionary. In addition, as a key
    dictionary2 = {seq[k]: 0}  # in dictionary, it can't be repeated so we don't need to worry about the repeated keys
    dictionary.update(dictionary2)
# 即是直接用字典建立{{‘2’‘6’：0}，{‘1’‘3’：0}}，其中‘2’和‘1’分别为两个数的首数字，‘6’和‘3’分别为末尾数字
for j in seq:
    for key, value in dictionary.items():  # record the max value in the dictionary which are the maximal
        if j == key:                       # pairs' occurrence计算这些‘2’‘6’和‘1’‘3’出现多少次，
                                # 因为字典会自动过滤key一样的元素，所以在字典建立的时候并不用担心
            dictionary[key] += 1
            if max_value <= dictionary[key]:
                max_value = dictionary[key]

for key, val in dictionary.items():  # Through the maximal value to find the keys and then output
    if val == max_value:
        key2 = int(key)
        first_and_last.add((key2 // 10, key2 % 10))

# REPLACE THIS COMMENT WITH YOUR CODE

print()
print('x is:', x)
print('L is:', L)
print()
print(f'The sum of all digits in x is equal to {sum_of_digits_in_x}.')
print()
print(f'There are {first_digit_greater_than_last}, {same_first_and_last_digits} '
      f'and {last_digit_greater_than_first} elements in L with a first digit that is\n'
      '  greater than the last digit, equal to the last digit,\n'
      '  and smaller than the last digit, respectively.'
      )
print()
for i in range(1, 9):
    if distinct_digits[i]:
        print(f'The number of members of L with {i} distinct digits is {distinct_digits[i]}.')
print()
print('The minimal gap (in absolute value) between first and last digits\n'
      f'  of a member of L is {min_gap}.'
      )
print('The maximal gap (in absolute value) between first and last digits\n'
      f'  of a member of L is {max_gap}.')
print()
print('The number of pairs (f, l) such that f and l are the first and last digits\n'
      f'of members of L is maximal for (f, l) one of {sorted(first_and_last)}.'
      )
