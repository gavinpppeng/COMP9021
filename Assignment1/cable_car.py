import os.path
import sys
import re
from collections import defaultdict


filename = input('Please enter the name of the file you want to get data from: ')
if not os.path.exists(filename):
    print('Sorry, there is no such file.')
    sys.exit()
file = open(filename)
file_data = file.read()
file.close()
# print(file_data)
num_list = []
num_list1 = []
num = []
file_lines = file_data.splitlines()
for line in file_lines:
        line = line.strip("\n").strip(" ")         # delete \n and " ", and the length will become 0
        if len(line) != 0:
            num_list.append(re.split(r' +', line))
# print(len(file_lines))
# print(num_list)
for i in range(len(num_list)):
        num_list1 = num_list1 + num_list[i]
# print(num_list1)

num_judge = []
try:
    if len(num_list1) < 2:
        raise ValueError
    for i in range(len(num_list1)):
        if int(num_list1[i]) <= 0:
            raise ValueError
        else:
            num.append(int(num_list1[i]))
            num_judge = sorted(list(set(num)))
except ValueError:
    print('Sorry, input file does not store valid data.')
    sys.exit()
if num != num_judge:
    print('Sorry, input file does not store valid data.')
    sys.exit()
# print(num)
# print(num_judge)

max_appear = 2
num_dict = {}
dict_list = [{0: 0}]
for i in range(1, len(num)):
    for j in range(i-1, -1, -1):
        add_key = True
        diff_value = num[i] - num[j]
        for key, value in dict_list[j].items():
            if diff_value == key:
                if dict_list[j][key]+1 > max_appear:
                    max_appear = dict_list[j][key]+1
                num_dict.update({key: dict_list[j][key]+1})
                add_key = False
        if add_key:
            num_dict.update({diff_value: 2})
    dict_list.append(num_dict)
    num_dict = {}
# print(num_dict, dict_list)

len_dict_list = len(dict_list)-1
count_list = []
while len_dict_list >= 0:
    new_dict = {}
    new_list = []
    new_dict = dict_list[len_dict_list]
    for key in new_dict.keys():
        new_list.append(key)
    if len(new_list) <= 2:
        if len(new_list) == 2:
            diff_num = new_list[0]
            if diff_num != new_list[1] - new_list[0]:
                break
            else:
                count = 1
        else:
            count = 0
    else:
        count = 0
        diff_num = new_list[0]
        for i in range(len(new_list)-1):
            if diff_num != new_list[i+1] - new_list[i]:
                break
            else:
                count += 1
    count_list.append(count)
# print(new_list)
    len_dict_list -= 1

longest_ride = max(count_list)+1
perfect_ride = len(num) - max_appear
if perfect_ride == 0:
    print('The ride is perfect!')
else:
    print('The ride could be better...')
print(f'The longest good ride has a length of: {longest_ride}')
print(f'The minimal number of pillars to remove to build a perfect ride from the rest is: {perfect_ride}')



