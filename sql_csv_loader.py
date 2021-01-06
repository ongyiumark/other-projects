#!/usr/bin/python3
import sys
import csv

def is_integer(s):
    if len(s) == 0: return True
    if s[0] == '-': return s[1:].isdigit()
    return s.isdigit()

def is_float(s):
    if len(s) == 0: return True
    if is_integer(s): return True
    
    i = s.find('.')
    if i == -1: return False
    return is_integer(s[:i]) and s[i+1:].isdigit()

def is_leap(year): 
    return int(year % 4 == 0) - int(year % 100 == 0) + int(year % 400 == 0)

def is_date(s):
    if len(s) == 0: return True
    if s.count('-') != 2: return False

    a = s.find('-')
    b = s.find('-', a+1)
    
    valid_year = is_integer(s[:a])
    if not valid_year: return False

    valid_month = is_integer(s[a+1:b]) and len(s[a+1:b]) == 2 and 1 <= int(s[a+1:b]) <= 12
    if not valid_month: return False
    
    days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap(int(s[:a])): days[2] += 1

    valid_day = is_integer(s[b+1:]) and len(s[b+1:]) == 2 and 1 <= int(s[b+1:]) <= days[int(s[a+1:b])]
    if not valid_day: return False

    return True

def check(f, vals):
    valid = True
    for val in vals[1:]:
        valid &= f(val)
    return valid

def get_type(vals):
    if check(is_integer, vals): return 'INTEGER' 
    if check(is_float, vals): return 'FLOAT'
    if check(is_date, vals): return 'DATE'
    return 'TEXT'

if __name__ == '__main__':
    if len(sys.argv)-1 != 2:
        raise "Invalid number of command line arguments"

    table_name = sys.argv[1]
    file_path = sys.argv[2]

    cols = []
    output = f'CREATE TABLE {table_name} (\n'
    
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        cols = zip(*csv_reader)
    
    cols = tuple(cols)
    for i in range(len(cols)):
        output += f'  {cols[i][0]} {get_type(cols[i])}'
        if i != len(cols)-1: output += ','
        output += '\n'
    
    output += f');\n\n\\copy {table_name} FROM \'{file_path}\' DELIMITER \',\' CSV HEADER;'
    print(output)



