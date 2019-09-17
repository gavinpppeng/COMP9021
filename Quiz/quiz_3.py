# Uses Global Temperature Time Series, avalaible at
# http://data.okfn.org/data/core/global-temp, stored in the file monthly_csv.csv,
# assumed to be stored in the working directory.
# Prompts the user for the source, a year or a range of years, and a month.
# - The source is either GCAG or GISTEMP.
# - The range of years is of the form xxxx -- xxxx (with any number of spaces,
#   possibly none, around --) and both years can be the same,
#   or the first year can be anterior to the second year,
#   or the first year can be posterior to the first year.
# We assume that the input is correct and the data for the requested month
# exist for all years in the requested range.
# Then outputs:
# - The average of the values for that source, for this month, for those years.
# - The list of years (in increasing order) for which the value is larger than that average.
#
# Written by *** and Eric Martin for COMP9021


import sys
import os
import csv


filename = 'monthly_csv.csv'
if not os.path.exists(filename):
    print(f'There is no file named {filename} in the working directory, giving up...')
    sys.exit()
with open(filename) as f:
    reader = csv.reader(f)
    data = list(reader)
print(data)
source = input('Enter the source (GCAG or GISTEMP): ')
if not source == 'GCAG' and not source == 'GISTEMP':
    print('Incorrect input, giving up.')
    sys.exit()

year_or_range_of_years = input('Enter a year or a range of years in the form XXXX -- XXXX: ')
try:
    range_year = year_or_range_of_years.replace(' ', '')
    # print(len(range_year))
    if not len(range_year) == 4 and not len(range_year) == 10:    # 1968 len = 4 ,1968--1995 len=10
        raise ValueError
    if len(range_year) == 10:
        range_year = range_year.split('--')
        # print(range_year)
        first_year = int(range_year[0])
        second_year = int(range_year[1])
        if first_year == second_year:
            first_year = 0
        if first_year > second_year:
            x = second_year
            second_year = first_year
            first_year = x
    if len(range_year) == 4:
        first_year = 0
        second_year = int(range_year)
    # print(second_year)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

month_digit = 0
month = input('Enter a month: ')
try:
    month_word = month.replace(' ', '')
    if month_word == 'January':
        month_digit = 1
    elif month_word == 'February':
        month_digit = 2
    elif month_word == 'March':
        month_digit = 3
    elif month_word == 'April':
        month_digit = 4
    elif month_word == 'May':
        month_digit = 5
    elif month_word == 'June':
        month_digit = 6
    elif month_word == 'July':
        month_digit = 7
    elif month_word == 'August':
        month_digit = 8
    elif month_word == 'September':
        month_digit = 9
    elif month_word == 'October':
        month_digit = 10
    elif month_word == 'November':
        month_digit = 11
    elif month_word == 'December':
        month_digit = 12
    else:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

average = 0
y = 1
m = 1
count_1 = 0
count_2 = 0
sum_one = 0
sum_two = 0
years_scope = []
years_above_average = []

if first_year == 0:
    while y < len(data):
        date = data[y][1].split('-')
# print(int(date[0]), second_year)
        if int(date[0]) == second_year and int(date[1]) == month_digit and data[y][0] == source:
            sum_one = sum_one + float(data[y][2])
            count_1 += 1
        y += 1
    average = sum_one / count_1
else:
    while m < len(data):
        date = data[m][1].split('-')
        if first_year <= int(date[0]) <= second_year and int(date[1]) == month_digit and data[m][0] == source:
            sum_two = sum_two + float(data[m][2])
            count_2 += 1
            years_scope.append(date[0])
        m += 1
    average = sum_two / count_2
years_scope = list(set(years_scope))
# print(years_scope)

for years in years_scope:
    j = 1
    count_larger = 0
    sum_larger = 0
    average_larger = 0
    while j < len(data):
        date = data[j][1].split('-')
        if date[0] == years and data[j][0] == source and int(date[1]) == month_digit:
                sum_larger = sum_larger + float(data[j][2])
                count_larger += 1
        j += 1
    average_larger = sum_larger / count_larger
    if average_larger > average:
        years_above_average.append(years)

# years_above_average = sorted(list(map(int, years_above_average)))
years_above_average = sorted(list(map(lambda x: int(x), years_above_average)))

print(f'The average anomaly for {month} in this range of years is: {average:.2f}.')
print('The list of years when the temperature anomaly was above average is:')
print(years_above_average)
