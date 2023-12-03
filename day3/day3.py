#!/usr/bin/python3
"""
Store "maze" in dict with positions?
Swap "digits" for their whole numbers?
"""
from collections import defaultdict
import string

def number_search(puzzle: dict[(int, int), str], coords: tuple[int, int]) -> (int, list[int]):
    node_sum: int = 0
    part_numbers: list[int] = []
    xcord, ycord = coords
    xarea = range(xcord-1, xcord+2)
    yarea = range(ycord-1, ycord+2)
    visited: list[tuple[int, int]] = []
    for y in yarea:
        for x in xarea:
            if (x,y) not in visited:
                visited.append((x,y))
                if puzzle[(x,y)].isdigit():
                    number_str = puzzle[(x,y)]
                    x_back = x - 1
                    x_front = x + 1
                    visited.append((x_back, y))
                    visited.append((x_front, y))
                
                    while puzzle[(x_back, y)].isdigit():
                        number_str = puzzle[(x_back, y)] + number_str
                        x_back -= 1
                        visited.append((x_back, y))

                    while puzzle[(x_front, y)].isdigit():
                        number_str += puzzle[(x_front, y)]
                        x_front += 1
                        visited.append((x_front, y))

                    node_sum += int(number_str)
                    part_numbers.append(int(number_str))

    return node_sum, part_numbers

def parser(filename: str, puzzle: dict[(int, int), str]) -> dict[(int, int), str]:
    with open(filename, "r") as file:
        for idx, line in enumerate(file):
            line = line.strip()
            for idx_c, char in enumerate(line):
                puzzle[(idx_c, idx)] = char
    return puzzle

def create_empty_puzzle(filename) -> dict[(int, int), str]:
    puzzle: dict[(int, int), str] = defaultdict()

    with open(filename, "r") as file:
        fp = file.readlines()
        #print(f"y len = {len(fp)}")
        #print(f"x len = {len(fp[0].strip())}")
        y_len = len(fp)
        x_len = len(fp[0].strip())

        for x in range(-1,x_len+2):
            for y in range(-1, y_len+2):
                puzzle[(x,y)] = "."            
        
    return puzzle

def solver(puzzle: dict[(int, int), str]) -> int:
    total_adj: int = 0
    gear_mult: int = 0
    for key, val in puzzle.items():
        if (val != ".") and (val not in string.digits):
            #print(type(key), key)
            numbers_adj_sum, part_numbers = number_search(puzzle, key)
            total_adj += numbers_adj_sum
            if (val == "*") and (len(part_numbers) == 2):
                gear_mult += part_numbers[0] * part_numbers[1]

    return total_adj, gear_mult


if __name__=="__main__":
    filename = "input/input.txt"
    
    puzzle = create_empty_puzzle(filename)
    puzzle = parser(filename, puzzle)
    part1, part2 = solver(puzzle)
    
    #print(number_search(puzzle, (3,1)), "\t\t", puzzle[(3,1)])
    #print(puzzle)
    #solver(puzzle)
    print(f"Answer for part 1: {part1}")
    print(f"Answer for part 2: {part2}")