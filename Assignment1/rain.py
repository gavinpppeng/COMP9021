import sys
import os
import re

filename = input('Which data file do you want to use?')
if not os.path.exists(filename):
    print(f'There is no file named {filename} in the working directory, giving up...')
    sys.exit()
file = open(filename)
file_data = file.read()
file.close()
# print(file_data)
num_list = []
count_dict = {}
try:
    file_lines = file_data.splitlines()
    for line in file_lines:
        num_list.append(re.split(r' +', line.strip(" ")))
# print(len(num_list[0]))
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

try:
    water_pour = int(input('How many decilitres of water do you want to pour down?'))
    if water_pour < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

# print(num_list)
i = 0
j = 0
count_list = []
len_count_set = 0
while i < len(num_list):
    while j < len(num_list[i]):
        count_list.append(num_list[i][j])
        j += 1
    i += 1
    j = 0
count_set = sorted(list(set(count_list)), key=lambda x: int(x))

for len_count_set in count_set:
    count_dict.update({len_count_set: 0})

for key, value in count_dict.items():
    for i in count_list:
        if i == key:
            count_dict[key] += 1

# print(count_set)
water_volume = []
count = 1
if len(count_set) > 1:
    while count < len(count_set):
        count1 = 0
        sum_value = 0
        while count1 < count:
            count_value = 0
            diff_value = int(count_set[count]) - int(count_set[count1])
            for key, value in count_dict.items():
                if key == count_set[count1]:
                    count_value = value
            sum_value = diff_value * count_value + sum_value
            count1 += 1
        water_volume.append(sum_value)
        count += 1
#    print(water_volume)

    water_capacity = 0
    average = 0
    larger_than_largest = True
    while water_capacity < len(water_volume):
        if water_pour <= water_volume[water_capacity]:
            for key, value in count_dict.items():
                if int(key) <= int(count_set[water_capacity]):
                    average = average + value
            if water_capacity > 0:
                water_pour = water_pour - water_volume[water_capacity-1]
            water_rises = water_pour / average
# print(water_rises)
            height = float(int(count_set[water_capacity]) + water_rises)
            larger_than_largest = False
            break
        water_capacity += 1

    sum_average = 0
    if larger_than_largest:
        water_pour = water_pour - water_volume[len(water_volume)-1]
        for key, value in count_dict.items():
            sum_average = sum_average + value
        height = water_pour / sum_average + int(count_set[len(count_set)-1])
else:
    for key, value in count_dict.items():
        height = int(key) + water_pour / value
print(f'The water rises to {height:.2f} centimetres.')


