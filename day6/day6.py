#!/usr/bin/python3
from collections import defaultdict
import functools, math

def calculate_ways(time: int, distance: int) -> int:
    nr_ways: int = 0
    
    minimum = math.ceil((time - math.sqrt((-time)**2 - 4*(distance+1)))/2)
    maximum = math.floor((time + math.sqrt((-time)**2 - 4*(distance+1)))/2)
    nr_ways = maximum - minimum + 1
        
    return nr_ways

def parser(filename, part):
    data: dict[str, list[int]] = defaultdict()
    with open(filename, "r") as file:
        if part == 1:
            data["time"], data["distance"] = [list(map(int, x.split(":")[1].split())) for x in file.readlines()]
        elif part == 2:
            data["time"], data["distance"] = [[int(functools.reduce(lambda a,b: a + b, f.split(":")[1].split()))] for f in file.readlines()]
    return data

def solver(data: dict[str, list[int]]) -> int:
    answer: int = 1
    for time, distance in zip(data["time"], data["distance"]):
        answer *= calculate_ways(time, distance)
    
    return answer

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0
    
    filename = "input/input.txt"
    data1 = parser(filename, 1)
    part1_sum = solver(data1)

    data2 = parser(filename, 2)
    part2_sum = solver(data2)

    print(f"Answer for part 1: {part1_sum}\nAnswer for part 2: {part2_sum}")