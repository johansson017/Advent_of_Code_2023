#!/c/ProgramData/Anaconda3/python
from collections import defaultdict
import re, functools, itertools
"""

"""
Datatype = dict[int, dict[str, int]]

def parser(filename: str, part2: bool):

    data: Datatype = defaultdict()
    with open(filename, "r") as file:
        for idx, line in enumerate(file):
            line = line.strip()
            spring, numbers = line.split()
            if part2:
                data[idx] = {"spring": ((spring + "?")*5)[:-1], "order": tuple(map(int, ((numbers+",")*5)[:-1].split(",")))}
            else:
                data[idx] = {"spring": spring, "order": tuple(map(int, numbers.split(",")))}

    return data

def memorize_springs(f: callable):
    MEMORY: dict = {}
    def wrapper(*args):
        if args in MEMORY:
            return MEMORY[args]
        else:
            MEMORY[args] = f(*args)
        return MEMORY[args]
    return wrapper

@memorize_springs
def spring_memory(spring: str, groups: tuple[int]):
    if not spring:
        if not groups:
            return 1
        else:
            return 0
    
    if spring[0] == ".":
        return spring_memory(spring[1:], groups)

    elif spring[0] == "?":
        dot_string = "." + spring[1:]
        hash_string = "#" + spring[1:]
        return spring_memory(dot_string, groups) + spring_memory(hash_string, groups)

    elif spring[0] == "#":
        if not groups:
            return 0
        
        elif len(spring) >= sum(groups): 
            for char in spring[:groups[0]]:
                if char != "#" and char != "?":
                    return 0
            if len(spring) == groups[0]:
                return 1
            elif spring[groups[0]] == "#":
                return 0
            else:
                return spring_memory(spring[groups[0]+1:], groups[1:])

        else:
            return 0


def solver(data: Datatype):
    combinations: int = 0
    permutations: int = 0
    for key, val in data.items():
        groups = val["order"]
        spring = val["spring"]

        permutations = spring_memory(spring, groups)

        combinations += permutations

    return combinations

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/input.txt"
    data_part1 = parser(filename, False)
    data_part2 = parser(filename, True)
    part1_sum = solver(data_part1)
    part2_sum = solver(data_part2)

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")