#!/usr/bin/python3
from collections import defaultdict
import functools

Galaxytype = dict[int, tuple[int, int]]

def fetch_distance(array: list[int], idx: int, multiplier) -> int:
    # NOTE: Multiply with (multiplier-1) due to original index already counting one of the "replacing" row/column
    return sum(list(map(lambda x: x*(multiplier-1), [1 for x in array if idx > x]))) + idx

def parser(filename: str) -> Galaxytype:
    # Start with array of arrays to find extra row/columns
    puzzle_array: list[list[str]] = []
    with open(filename, "r") as file:
        puzzle_array = [x.strip() for x in file.readlines()]

    extra_row: list[int] = []
    extra_col: list[int] = []
    for idx, line in enumerate(puzzle_array):
        if line.count(".") == len(line):
            extra_row.append(idx)
    
    for idx in range(len(puzzle_array[0])):
        temp_arr = []
        for arr in puzzle_array:
            temp_arr.append(arr[idx])

        if temp_arr.count(".") == len(temp_arr):
            extra_col.append(idx)

    galaxy_dict1: Galaxytype = defaultdict()
    galaxy_dict2: Galaxytype = defaultdict()
    iter_galaxy: int = 0
    for idx_y, line in enumerate(puzzle_array):
        for idx_x, char in enumerate(line):
            if char == '#':
                iter_galaxy += 1
                galaxy_dict1[iter_galaxy] = (fetch_distance(extra_col, idx_x, 2), fetch_distance(extra_row, idx_y, 2))
                galaxy_dict2[iter_galaxy] = (fetch_distance(extra_col, idx_x, 1000000), fetch_distance(extra_row, idx_y, 1000000))

    return galaxy_dict1, galaxy_dict2

def solver(galaxy_dict: Galaxytype):
    answer: int = 0
    pairs: list[tuple[int, int]] = []
    nr_galaxies = max(galaxy_dict.keys())
    for i in range(1, nr_galaxies):
        for j in range(i+1, nr_galaxies+1):
            pairs.append((i,j))
    
    for pair in pairs:
        first, second = pair
        answer += abs(galaxy_dict[first][0] - galaxy_dict[second][0]) + abs(galaxy_dict[first][1] - galaxy_dict[second][1])

    return answer


if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/input.txt"
    galaxy_dict1, galaxy_dict2 = parser(filename)
    part1_sum = solver(galaxy_dict1)
    part2_sum = solver(galaxy_dict2)

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")