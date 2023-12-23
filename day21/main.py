#!/usr/bin/python3
import os,sys
sys.path.append(os.getcwd())
from collections import defaultdict
import math,re
from functools import reduce
from util.solution import Solution
from dataclasses import dataclass

Gridtype = dict[tuple[int, int], str]

def find_valid_neighbour(grid: Gridtype, node: tuple[int, int], steps, sizes):
    x, y = node
    directions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    x_max, y_max = sizes
    neighbours = []
    for direction in directions:
        nx, ny = direction
        if nx >= 0 and nx <= x_max and ny >= 0 and ny <= y_max:
            neighbours.append(((nx, ny), steps+1))
    
    return neighbours



def parser(filename: str, part2=False):
    grid: Gridtype = {}
    with open(filename, "r") as file:
        for idx_y, line in enumerate(file):
            for idx_x, char in enumerate(line.strip()):
                if char == "S":
                    start = (idx_x, idx_y)
                grid[idx_x, idx_y] = char
    return grid, start

def solver(grid: Gridtype, part2=False, extras=None):
    grid, start = grid
    sizes = max(grid.keys())
    visited = []
    queue = []
    # Add amount of steps to node property
    start_node = (start, 0)
    queue.append(start_node)

    while queue:
        node, steps = queue.pop(0)
        if node in visited:
            continue
        elif steps % 2 == 0:
            visited.append(node)

        if extras is not None:
            limit = extras["test"]
        else: limit = 64

        if steps == limit:
            continue
        
        for friend in find_valid_neighbour(grid, node, steps, sizes):
            node, steps = friend
            nx, ny = node
            if grid[nx, ny] == ".":
                queue.append(friend)

    return len(visited), visited

if __name__=="__main__":
    day = "day21"
    input = f"{day}/input/input.txt"
    test = f"{day}/input/sample.txt"
    test_result = 16
    
    solution = Solution(parser, solver, input)
    solution.test_input([test], [test_result])
    #print(solution.parsed_test_data)
    # Solver should return PRINTVALUE, EXTRA (NONE)
    solution.solve(test=True, part1=False, part2=False, extras={"test":14})
    solution.display_result(windows=True)
    solution.print_grid("0", test=True)