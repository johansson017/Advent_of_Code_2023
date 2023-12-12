#!/c/msys64/mingw64/bin/python3
from collections import defaultdict
import re, functools, itertools
"""

"""
Datatype = dict[int, dict[str, int]]

def parser(filename: str):

    data: Datatype = defaultdict()
    with open(filename, "r") as file:
        for idx, line in enumerate(file):
            line = line.strip()
            spring, numbers = line.split()
            #print(spring, numbers)
            data[idx] = {"spring": ((spring + "?")*5)[:-1], "order": list(map(int, ((numbers+",")*5)[:-1].split(",")))}

    return data

def fill_permutations(permutations: list[str], start, unid_index: list[int]):

    return permutations

def spring_permutations(spring: str, order: list[int]):
    permutations: list[str] = []
    total_broken = sum(order)
    place_amount = total_broken - spring.count("#")

    unid_index: list[int] = []
    for idx, char in enumerate(spring):
        if char == "?": 
            unid_index.append(idx)

    unid_permutations = list(itertools.combinations(unid_index, place_amount))

    for perm in unid_permutations:
        temp_list = list(spring)
        for val in perm:
            temp_list[val] = "#"
        temp_list = "".join(temp_list)
        permutations.append(temp_list)

    return permutations


def solver(data: Datatype):
    part1_sum: int = 0
    for key,val in data.items():
        print(key, part1_sum)
        permutations = spring_permutations(val["spring"], val["order"])
        temp_list = []
        #print(part1_sum)

        ### TODO:: FIX THIS SHIT LOOP
        for perm in permutations:
            #print(perm)
            #print(perm, val["order"])
            #print(temp_list)
            temp_list = []
            i = 0
            j = 0
            for idx in range(len(perm)):
                if perm[idx] == "#":
                    i += 1
                    if idx == (len(perm)-1):
                        temp_list.append(i)
                else:
                    if idx == (len(perm)-1):
                        if i != 0:
                            temp_list.append(i)
                        break
                    elif i == 0:
                        continue
                    elif i == val["order"][j]:
                        temp_list.append(i)
                        j += 1
                        i = 0
                    else:
                        i = 0
                        break
            #print(temp_list, idx)
            if temp_list == val["order"]:
                part1_sum += 1

    return part1_sum

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/sample.txt"
    data = parser(filename)
    part1_sum = solver(data)

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")