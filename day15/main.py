#!/usr/bin/python3
from collections import defaultdict
import itertools, functools


def calculate_section(section: str):
    word_sum: int = 0
    for char in section:
        word_sum += ord(char)
        word_sum *= 17
        word_sum = word_sum % 256
    return word_sum

def fill_lensbox(id, lensbox):
    splitchar = "="
    remove = False
    if "-" in id:
        splitchar = "-"
        remove = True
        chars = id.rstrip("-")
        f_length = 0
    else:
        chars, f_length = id.split(splitchar)

    box_nr = calculate_section(chars)

    find_lens(box_nr, chars, f_length, lensbox, remove)

def find_lens(box_nr, chars, f_length, lensbox, remove: bool = False) -> bool:
    found = False
    for idx, lens in enumerate(lensbox[box_nr]):
        if lens[0] == chars:
            if remove:
                lensbox[box_nr].pop(idx)
            else:
                lensbox[box_nr][idx] = (chars, f_length)
                found = True
    if not found and not remove:
        lensbox[box_nr].append((chars, f_length))

def solver(filename: str):
    lensbox: dict[int, dict[str, int]] = defaultdict(list)
    
    with open(filename, "r") as file:
        sections = file.readline().split(",")
        for id in sections:
            fill_lensbox(id, lensbox)

    part2_sum = calculate_sum(lensbox)
    return part2_sum

def calculate_sum(lensbox):
    part2_sum: int = 0

    for i in range(256):
        for idx, val in enumerate(lensbox[i]):
            part2_sum += (i+1)*(idx+1)*int(val[1])

    return part2_sum

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/input.txt"

    part1_sum = sum(list(functools.reduce(lambda a,b: ((a+ord(b))*17)%256, [0]+section) for section in [[char for char in string] for string in (splitstring.strip() for splitstring in open(filename).readline().split(","))]))
    part2_sum = solver(filename)
    
    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")