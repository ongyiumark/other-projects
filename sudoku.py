#!/usr/bin/python3
import sys

if len(sys.argv)-1 != 3:
    raise "Invalid number of command line arguments"

n = int(sys.argv[1])
r = int(sys.argv[2])
c = int(sys.argv[3])

if r*c != n:
    raise "Invalid box dimensions"


cols = [[False for j in range(n+1)] for i in range(n)]
rows = [[False for j in range(n+1)] for i in range(n)]
boxes = [[False for j in range(n+1)] for i in range(n)]

grid = []
flag = [[False for j in range(n)] for i in range(n)]

for _ in range(n):
    grid.append(list(map(int, input().split())))

def get_box_number(i, j):
    return i//r*r + j//c

# Loads cols, rows, and boxes with the initial values.
def init():
    for i in range(n):
        for j in range(n):
            if grid[i][j] != 0:
                rows[i][grid[i][j]] = True
                cols[j][grid[i][j]] = True
                boxes[get_box_number(i,j)][grid[i][j]] = True
                flag[i][j] = True

def solve(i = 0, j = 0):
    if (i == n):
        for i in range(n):
            print(*grid[i])
        return

    # don't change if its one of thge initial values
    if flag[i][j]:
        if (j+1 >= n): solve(i+1, 0)
        else: solve(i, j+1)

    for val in range(1,n+1):
        if rows[i][val] or cols[j][val] or boxes[get_box_number(i,j)][val]:
            continue
        # storing in grid
        prev_val = grid[i][j]
        grid[i][j] = val
        
        # loading in rows, cols, and boxes
        rows[i][val] = cols[j][val] = boxes[get_box_number(i,j)][val] = True
        
        if (j+1 >= n): solve(i+1, 0)
        else: solve(i, j+1)

        # backtracking
        grid[i][j] = prev_val
        rows[i][val] = cols[j][val] = boxes[get_box_number(i,j)][val] = False
        
init()
solve()

