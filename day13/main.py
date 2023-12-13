#!/usr/bin/python3
from collections import defaultdict
import itertools, functools, re

Arraytype = list[str]
replacement = {"#": ".", ".": "#"}

def transform(array: Arraytype):
    return list(map("".join, list(zip(*array))))

def string_replace(string: str, index: int, replacement):
    return string[:index] + replacement + string[(index+1):]

def identify_mirror(array: Arraytype, old_reflection: int = None) -> int | None:
    mid_lines = []
    arr_length = len(array)
    mid_point = int(arr_length/2)
    for idx in range(len(array[:-1])):
        if array[idx] == array[idx+1]:
            mid_lines.append(idx+1)

    for val in mid_lines:
        if val > mid_point:
            cmp_amount = arr_length-val
        else:
            cmp_amount = val
        
        # Saving old index for part 1 to not calculate on that again
        if (array[(val-cmp_amount):val] == list(reversed(array[val:(val+cmp_amount)]))) and (val != old_reflection):
            return val
    
    return None

def smudge_fix(array: Arraytype) -> Arraytype:
    arr_length = len(array)
    mid_point = int(arr_length/2)
    str_length = len(array[0])
    reflect_idx = list(range(1, arr_length))

    for val in reflect_idx:
        arr_cmp = []
        cmp_amount = (arr_length - val if val > mid_point else val)
        
        # Comparing upper/lower (val-cmp_amount) amount of array to count identical chars
        for val1, val2 in zip(reversed(array[(val-cmp_amount):val]), array[val:(val+cmp_amount)]):
            arr_cmp = arr_cmp + [v1==v2 for v1, v2 in zip(val1, val2)]

        # Counting if a comparison only has one "out", meaning it is the reflection fix
        if (str_length*cmp_amount) - arr_cmp.count(True) == 1:
            x = arr_cmp.index(False) % str_length

            # With the arrays, we are saving "False" value at x str_lengths away from reflection point
            # Need to calculate how many str_lengths away, by utilizing "rounding up" division
            # NOTE: Rounding Up division utilized by rounding down and adding "1"
            y = val - (int(arr_cmp.index(False) / str_length) + 1)
            
            array[y] = string_replace(array[y], x, replacement[array[y][x]])
            return array
    
    return None 


def parser(filename: str) -> Arraytype:
    part1_sum: int = 0
    part2_sum: int = 0
    
    lines = open(filename).readlines()
    array: Arraytype = []
    t_array = []
    for line in lines:
        line = line.strip()
        if line:
            t_array.append(line)
        else:
            array.append(t_array)
            t_array = []
    array.append(t_array)

    return array


def solver(data: Arraytype) -> tuple[int, int]:
    part1_sum: int = 0
    part2_sum: int = 0

    for arr in data:

        # Part 1
        answer1 = None
        p1_t = False
        if answer1 := identify_mirror(transform(arr)):
            part1_sum += answer1
            p1_t = True
        elif answer1 := identify_mirror(arr):
            part1_sum += answer1*100

        # Part 2
        transformed = False
        new_array = smudge_fix(arr)
        if new_array == None:
            new_array = transform(arr)
            new_array = smudge_fix(new_array)
            transformed = True

        # If array is transformed, change back before calculating points
        if transformed:
            new_array = transform(new_array)

        # First try finding reflection in opposite direction of part 1
        # Then try finding in same direction as part 1 but "blacklist" same reflection
        if p1_t:
            if answer2 := identify_mirror(new_array):
                part2_sum += answer2*100
            elif answer2 := identify_mirror(transform(new_array), answer1):
                part2_sum += answer2
        else:
            if answer2 := identify_mirror(transform(new_array)):
                part2_sum += answer2
            elif answer2 := identify_mirror(new_array, answer1):
                part2_sum += answer2*100

    return part1_sum, part2_sum

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/input.txt"
    data = parser(filename)
    part1_sum, part2_sum = solver(data) 

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")