import os.path
import sys
import re

filename = input('Please enter the name of the file you want to get data from: ')
if not os.path.exists(filename):
    print('Sorry, there is no such file.')
    sys.exit()
file = open(filename)
file_data = file.read()
file.close()

num_list = []
file_lines = file_data.splitlines()
for line in file_lines:
    line = line.strip("\n").strip(" ")
    if len(line) != 0:
        num_list.append(re.split(r' +', line))
# print(num_list)

# print(len(num_list))
if len(num_list) != 2:
    print('Sorry, input file does not store valid data.')
    sys.exit()
if len(num_list[0]) < 2 or len(num_list[1]) < 2 or len(num_list[0]) != len(num_list[1]):
    print('Sorry, input file does not store valid data.')
    sys.exit()

ceiling_list = []
floor_list = []
try:
    for i in num_list[0]:
        ceiling_list.append(int(i))
    for j in num_list[1]:
        floor_list.append(int(j))
    k = 0
    while k < len(ceiling_list):
        if ceiling_list[k] <= floor_list[k]:
            raise ValueError
        k += 1
except ValueError:
    print('Sorry, input file does not store valid data.')
    sys.exit()


def max_distance(x, y1, y2):
    x1 = x
    if x1 == 0:
        count_list = []
        for i in range(y2 - y1+1):
            obstacle = False
            height = y1 + i
            count = 1
            x1 = x+1
            if height != y2:
                while not obstacle and x1 < len(floor_list):
                    if floor_list[x1] <= height < ceiling_list[x1]:
                        obstacle = False
                        count += 1
                        x1 += 1
                    else:
                        obstacle = True
                        count_list.append(count)
            else:
                while not obstacle and x1 < len(floor_list):
                    if floor_list[x1] < height < ceiling_list[x1]:
                        obstacle = False
                        count += 1
                        x1 += 1
                    else:
                        obstacle = True
                        count_list.append(count)
        return max(count_list)
    elif x1 == len(floor_list)-1:
        count_list3 = []
        for num2 in range(y2 - y1 + 1):
            obstacle = False
            height = y1 + num2
            count = 1
            x1 = x - 1
            if height != y2:
                while not obstacle and x1 < len(floor_list):
                    if floor_list[x1] <= height < ceiling_list[x1]:
                        obstacle = False
                        count += 1
                        x1 -= 1
                    else:
                        obstacle = True
                        count_list3.append(count)
            else:
                while not obstacle and x1 < len(floor_list):
                    if floor_list[x1] < height < ceiling_list[x1]:
                        obstacle = False
                        count += 1
                        x1 -= 1
                    else:
                        obstacle = True
                        count_list3.append(count)
        return max(count_list3)
    else:
        count_list2 = []
        for num in range(y2 - y1+1):
            obstacle = False
            height = y1 + num
            count = 1
            x1 = x+1
            x2 = x-1
            if height != y2:
                while not obstacle and x1 < len(floor_list):
                    if floor_list[x1] <= height < ceiling_list[x1]:
                        obstacle = False
                        count += 1
                        x1 += 1
                    else:
                        obstacle = True
                obstacle = False
                while not obstacle and x2 >= 0:
                    if floor_list[x2] <= height < ceiling_list[x2]:
                        obstacle = False
                        count += 1
                        x2 -= 1
                    else:
                        obstacle = True
                        count_list2.append(count)
            else:
                while not obstacle and x1 < len(floor_list):
                    if floor_list[x1] < height < ceiling_list[x1]:
                        obstacle = False
                        count += 1
                        x1 += 1
                    else:
                        obstacle = True
                obstacle = False
                while not obstacle and x2 >= 0:
                    if floor_list[x2] < height < ceiling_list[x2]:
                        obstacle = False
                        count += 1
                        x2 -= 1
                    else:
                        obstacle = True
                        count_list2.append(count)
        return max(count_list2)


west_distance = max_distance(0, floor_list[0], ceiling_list[0])
inside_tunnel = []
for i in range(len(floor_list)):
    inside_tunnel.append(max_distance(i, floor_list[i], ceiling_list[i]))

print(f'From the west, one can see into the tunnel over a distance of {west_distance}.')
print(f'Inside the tunnel, one can see into the tunnel over a maximum distance of {max(inside_tunnel)}.')






