#!/usr/bin/python3
import os,sys
sys.path.append(os.getcwd())
from collections import defaultdict
import math,re, copy
from functools import reduce
from util.solution import Solution
from dataclasses import dataclass

Datatype = list[object]

"""
3D grid with each coordinate pointing to resting brick
"""
@dataclass
class Brick:
    idx: int
    x_s: int
    y_s: int
    z_s: int

    x_e: int
    y_e: int
    z_e: int

    size: tuple[int, int, int]

    # Support mutable of list[object] - list for block to which they support ON
    # Holder mutable of list[object]  - list for block to whch they support

mappings = {0:"A", 1:"B", 2:"C", 3:"d", 4:"D", 5:"E", 6:"F", 7:"G"} 

def brick_occupation_coords(brick: object, z_level: int) -> tuple[int, int, int]:
    for x in range(brick.x_s, brick.x_e+1):
        for y in range(brick.y_s, brick.y_e+1):
            for z in range(z_level, z_level+brick.size[2]):
                yield x,y,z

# Scans 3D grid for x,y coords to find earliest z level for brick resting level 
def grid_space_scanner(grid: tuple[int, int, int], grid_size: tuple[int, int, int], brick) -> int:
    z_level = 0

    for x_c in range(brick.x_s, brick.x_e+1):
        for y_c in range(brick.y_s, brick.y_e+1):
            for z in range(0, grid_size[2]):
                if (x_c, y_c, z) in grid:
                    if z > z_level:
                        z_level = z
    return z_level + 1

def find_supporting_bricks(grid: tuple[int, int, int], brick):
    for x_c in range(brick.x_s, brick.x_e+1):
        for y_c in range(brick.y_s, brick.y_e+1):
            z_s = brick.z_e - 1
            z_h = brick.z_e + brick.size[2]

            if (x_c, y_c, z_s) in grid and grid[x_c, y_c, z_s] not in brick.support:
                brick.support.append(grid[x_c, y_c, z_s])
            
            if (x_c, y_c, z_h) in grid and grid[x_c, y_c, z_h] not in brick.supporting:
                brick.supporting.append(grid[x_c, y_c, z_h])

def parser(filename: str, part2=False):
    data = []
    with open(filename, "r") as file:
        for idx, line in enumerate(file):
            b_s, b_e = line.strip().split("~")
            b_s = list(map(int, b_s.split(",")))
            b_e = list(map(int, b_e.split(",")))
            brick = Brick(idx, b_s[0], b_s[1], b_s[2], b_e[0], b_e[1], b_e[2], (b_e[0]-b_s[0]+1, b_e[1]-b_s[1]+1, b_e[2]-b_s[2]+1))
            brick.support = []
            brick.supporting = []
            data.append(brick)
    
    grid_size = (max(data, key=lambda x: x.x_s).x_s, max(data, key=lambda x: x.y_s).y_s, max(data, key=lambda x: x.z_s).z_s)
    
    return data, grid_size 


def solver(data: Datatype, part2=False, extras=None):
    part1_sum = 0
    data, grid_size = data
    data.sort(key=lambda x: x.z_s)

    # Constructing 3D grid using dict (x,y,z)
    # Meant to place all falling bricks back at rest level z by occupying the previous z dimensions
    grid: dict[tuple[int, int, int], object] = defaultdict(None)
    
    # Fill grid with brick object for positions 
    for brick in data:
        z_level = grid_space_scanner(grid, grid_size, brick)
        brick.z_e = z_level
        for b_c in brick_occupation_coords(brick, z_level):
            grid[b_c] = brick

    # Creating two new properties for brick object -> supporting and support
    for brick in data:
        find_supporting_bricks(grid, brick)
    
    domino_bricks = []
    for brick in data:
        if not brick.supporting:
            continue

        for r_brick in brick.supporting:
            if len(r_brick.support) == 1:
                if r_brick.support[0] not in domino_bricks:
                    domino_bricks.append(r_brick.support[0])
    
    part1_sum = len(data)-len(domino_bricks)
    
    
    if part2:
        domino_bricks.sort(key=lambda x: x.z_e)
        part2_sum = 0
        for fall_brick in domino_bricks:
            supporters = set()
            supporters.add(fall_brick.idx)
            queue = []
            queue.append(fall_brick)
            falling = set()

            while queue:
                current = queue.pop(0)
                for brick in current.supporting:
                    have_support = [x.idx in supporters for x in brick.support]
                    if all(have_support):
                        queue.append(brick)
                        supporters.add(brick.idx)
                        falling.add(brick.idx)
            part2_sum += len(falling)

        return part2_sum, None

    return part1_sum, None


if __name__=="__main__":
    day = "day22"
    input = f"{day}/input/input.txt"
    test = f"{day}/input/sample.txt"
    test_result = 5
    test_result2 = 7


    solution = Solution(parser, solver, input)
    solution.test_input([test, test], [test_result, test_result2])
    solution.solve(test=True, part1=True, part2=True)
    solution.display_result()