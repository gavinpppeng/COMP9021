import sys
import math

heroes_power = []
solution1 = []
solution2 = []
judge_solution2 = []
try:
    L = input("Please input the heroes' powers: ")
    L2 = L.split(' ')
    for i in L2:
        if not int(i):
            raise ValueError
    for n in L2:
        heroes_power.append(int(n))
except ValueError:
    print('Sorry, these are not valid power values.')
    sys.exit()

try:
    power_flips = int(input('Please input the number of power flips:'))
    if power_flips < 0 or power_flips > len(L2):
        raise ValueError
except ValueError:
    print('Sorry, this is not a valid number of power flips.')
    sys.exit()


many_time_flipping = heroes_power.copy()
consecutive_time = heroes_power.copy()
power_flips2 = power_flips
power_flips3 = power_flips
while len(many_time_flipping) > 0:
    max_abs = 0
    k = 0
    for j in many_time_flipping:
        abs_j = abs(j)
        if abs_j > max_abs:
            max_abs = abs_j
    while k < len(many_time_flipping):
        if abs(many_time_flipping[k]) == max_abs:
            if power_flips2 > 0 and many_time_flipping[k] < 0:
                many_time_flipping[k] = -many_time_flipping[k]
                num = many_time_flipping.pop(k)
                solution1.append(num)
                solution2.append(num)
                judge_solution2.append(1)
                power_flips2 -= 1
                print(power_flips2)
            else:
                num = many_time_flipping.pop(k)
                solution1.append(num)
                solution2.append(num)
                judge_solution2.append(0)
        k += 1

count = -1
if not power_flips2 == 0:
    if not power_flips2 % 2 == 0:
        solution1[-1] = -solution1[-1]

while abs(count) < len(solution2) and not power_flips2 == 0:
        if judge_solution2[count] == 0:
            solution2[count] = -solution2[count]
        count -= 1
        power_flips2 -= 1

sum1 = sum(solution1)
sum2 = sum(solution2)

sum_con = []
sum_max_4 = []
if power_flips == 0:
    sum3 = sum(heroes_power)
else:
    i = 0
    while i <= len(heroes_power):
        for m in range(len(heroes_power) - i + 1):
            consecutive_time = heroes_power.copy()
            for a in range(i):
                consecutive_time[m + a] = -consecutive_time[m + a]
            sum_con.append(sum(consecutive_time))
            sum_max_4.append(max(sum_con))

        if i == power_flips3:
            sum3 = max(sum_con)
        sum_con = []
        i += 1

sum4 = max(sum_max_4)


print(f'Possibly flipping the power of the same hero many times, the greatest achievable power is {sum1}.')
print(f'Flipping the power of the same hero at most once, the greatest achievable power is {sum2}.')
print(f'Flipping the power of nb_of_flips many consecutive heroes, the greatest achievable power is {sum3}.')
print(f'Flipping the power of arbitrarily many consecutive heroes, the greatest achievable power is {sum4}.')

