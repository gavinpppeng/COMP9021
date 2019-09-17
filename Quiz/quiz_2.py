# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, randint
from math import gcd, sqrt


def prime(n):                 # build and return a prime list such as :2,3,5,7,11,13...
    prime_sieve = [True] * (n+1)
    prime_num = []
    for num in range(2, round(sqrt(n))+1):
        if prime_sieve[num]:
            for i in range(num*num, n+1, num):
                prime_sieve[i] = False
    for j in range(2, n+1):
        if prime_sieve[j]:
            prime_num.append(j)
    return prime_num


def prime_factor(n):                 # build a factor list, e.g 196 = 2*2*7*7, factor = [2,2,7,7]
    prime_num = prime(n)             # 用迭代的方法输出，相当于找质因数的时候，196 = 2 * prime_factor(98)
    for judge_if_prime in prime_num:    # 最后这里判断是否是质数，如果是质数就说明分解质因数完毕，函数返回，结束迭代
        if n == judge_if_prime:
            factor.append(n)
            return

    need_to_continue = True
    for k in range(round(sqrt(n))+1):
        if n % prime_num[k] == 0:            # 判断能否整除从质数列表里面取出来的质数，如果能就分离出这个质数，进行下一步迭代
            factor.append(prime_num[k])      # 如果n需要分解成两个因数（不一定都是质因数）相乘的话，只需要寻找2到sqrt(n)
            n_factor = n // prime_num[k]     # 以内的数能否被整除
            prime_factor(n_factor)
            need_to_continue = False
        if not need_to_continue:
            break


try:
    arg_for_seed, length, max_value = input('Enter three strictly positive integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, length, max_value = int(arg_for_seed), int(length), int(max_value)
    if arg_for_seed < 1 or length < 1 or max_value < 1:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randint(1, max_value) for _ in range(length)]
print('Here is L:')
print(L)
print()

size_of_simplest_fraction = 2
simplest_fractions = []
size_of_most_complex_fraction = 2
most_complex_fractions = []
multiplicity_of_largest_prime_factor = 0
largest_prime_factors = []


def nb_of_digits(num):
    count = 0
    while num != 0:
        num = num // 10             # units digit, tens digit, hundreds digit...count digits，确定一个数字有多少位
        count += 1
    return count


L_sort = sorted(list(set(L)))
for i in range(len(L_sort)):
    j = i + 1
    while j < len(L_sort):
        GCD = gcd(L_sort[i], L_sort[j])
        numerator = L_sort[i]//GCD         # 分子分母除以最大公约数就可以得到最简分数
        denominator = L_sort[j]//GCD
        sum_digits = nb_of_digits(numerator)+nb_of_digits(denominator)
        if sum_digits > size_of_most_complex_fraction:
            most_complex_fractions.clear()         # sum_digits代表分子和分母两个数字的数字的位数之和，这里如果不是最大的
            most_complex_fractions.append((numerator, denominator))      # 就把之前存放最大的分子分母的列表most_complex_fractions清空
            size_of_most_complex_fraction = sum_digits                 # 并且重新放进一个most_complex_fractions.
        elif sum_digits == size_of_most_complex_fraction and sum_digits != 2:
            most_complex_fractions.append((numerator, denominator))
        elif sum_digits == 2:              # 最小的一定有1/1, 所以分子分母最小的位数和应该为2，如果不等于2就说明不是最小/简的分数
            simplest_fractions.append((numerator, denominator))
        j += 1
simplest_fractions.append((1, 1))
if len(most_complex_fractions) == 0:
    most_complex_fractions = most_complex_fractions.copy(simplest_fractions)


simplest_fractions = sorted(list(set(simplest_fractions)), key=lambda x: x[0]/x[1])       # 输出按分数大小排序
most_complex_fractions = sorted(list(set(most_complex_fractions)), key=lambda x: x[1]/x[0])       # 输出按分数大小排序

denominator_list = []
factor = []
max_appear_time = 1
digit_time_dict = {}
for (x, y) in most_complex_fractions:
    denominator_list.append(y)


def max_digits(number, max_appear):       # 输入到这个函数里面，返回一个包含最大次数max_appear_time和包含最大出现次数的数字的数组
    global largest_prime_factors, factor
    prime_factor(number)
    modified_max = False
    for key in factor:
        digit_time_dict[key] = 0          # {factor:0}, no repeat
    for u in factor:
        for key2 in digit_time_dict.keys():   # {factor:0} 找字典中，匹配factor的质因数，找到就加一
            if u == key2:
                digit_time_dict[key2] += 1

    for dict_value in digit_time_dict.values():  # 以196为例，{2：2，5：2},然后最大出现次数为2，把这个存起来
        if dict_value > max_appear:              # 往后面的分母寻找，如果有比这个2更大的，就把存有最大出现次数的分母的质因数的
            max_appear = dict_value              # 数组清空，重新存入最大的质因数的数组，以200为例子，{2：3，5：2}，出现最多的
            modified_max = True                  # 质因数为2，次数为3，那么就把max_appear的值从2改为3，并且把
#                                                 largest_prime_factors列表中[2,5]清空，并重新赋值[2]
    if modified_max:
        largest_prime_factors = []
        for key3, value3 in digit_time_dict.items():
            if max_appear == value3:
                largest_prime_factors.append(key3)
    else:
        for key3, value3 in digit_time_dict.items():
            if max_appear == value3:
                largest_prime_factors.append(key3)
    factor = []
    return max_appear


for num in denominator_list:
    if len(denominator_list) == 1 and denominator_list[0] == 1:
        largest_prime_factors = []
        multiplicity_of_largest_prime_factor = 1
    else:
        max_appear_time = max_digits(num, max_appear_time)
        largest_prime_factors = sorted(list(set(largest_prime_factors)))
        multiplicity_of_largest_prime_factor = max_appear_time

print('The size of the simplest fraction <= 1 built from members of L is:',
      size_of_simplest_fraction
      )
print('From smallest to largest, those simplest fractions are:')
print('\n'.join(f'    {x}/{y}' for (x, y) in simplest_fractions))
print('The size of the most complex fraction <= 1 built from members of L is:',
      size_of_most_complex_fraction
      )
print('From largest to smallest, those most complex fractions are:')
print('\n'.join(f'    {x}/{y}' for (x, y) in most_complex_fractions))
print("The highest multiplicity of prime factors of the latter's denominators is:",
      multiplicity_of_largest_prime_factor
      )
print('These prime factors of highest multiplicity are, from smallest to largest:')
print('   ', largest_prime_factors)

