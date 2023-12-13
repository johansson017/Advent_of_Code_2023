#!/usr/bin/python3
from collections import defaultdict
import itertools, functools, re

Arraytype = list[list[str]]



def transform(array: Arraytype):
    new_array: Arraytype = []
    for i in range(len(array[0])):
        temp_string = ""
        for j in range(len(array)):
            temp_string += array[j][i]
        new_array.append(temp_string)

    return new_array

def identify_mirror(array: Arraytype) -> int:
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
        
        if array[(val-cmp_amount):val] == list(reversed(array[val:(val+cmp_amount)])):
            return val

def parser(filename: str):
    part1_sum: int = 0
    
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

    for arr in array:
        if answer := identify_mirror(transform(arr)):
            part1_sum += answer
        elif answer := identify_mirror(arr):
            part1_sum += answer*100
    
    return part1_sum

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/input.txt"
    part1_sum = parser(filename)


    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")