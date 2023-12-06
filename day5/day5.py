#!/usr/bin/python3
from dataclasses import dataclass, fields
from collections import defaultdict
import time
"""
SEEEDS
"""
def add_seed_range(seed_ranges: list[dict[str, int]], high, low) -> dict[str, int]:
    new_seed = {"high": high, "low": low}
    seed_ranges.append(new_seed)
    return seed_ranges

def parser(filename) -> tuple[list[int], list[dict[str, int]], dict[str, dict[str, list[int]]]]:
    processes: dict = defaultdict()
    seeds_part1: list[int] = []
    seed_ranges: list = []
    with open(filename) as file:
        seed_nr = file.readline()
        _, seed_nr = seed_nr.strip().split(":")
        seed_nr = list(map(int, seed_nr.strip().split(" ")))
        for idx, s in enumerate(seed_nr):
            seeds_part1.append(s)
            if idx % 2 == 0:
                high = s + seed_nr[idx + 1] - 1
                low = s
                seed_ranges = add_seed_range(seed_ranges, high, low)

        for line in file:
            if line.isspace():
                continue
            elif ":" in line:
                key = line.strip().rstrip(" map:")
                processes[key] = defaultdict()
                processes[key]["dest"]: list[int] = []
                processes[key]["low"]: list[int] = []
                processes[key]["high"]: list[int] = []
            else:
                dest, start, span = map(int, line.strip().split(" "))
                processes[key]["dest"].append(dest)
                processes[key]["low"].append(start)
                processes[key]["high"].append(start + span-1)
    
    return seeds_part1, seed_ranges, processes

def solver1(seeds_part1: list[int], processes: dict[str, dict[str, list[int]]]) -> int:
    part1: int = None
    for process in processes:
        for idx, seed in enumerate(seeds_part1):
            for (dest, high, low) in zip(processes[process]["dest"],
                                         processes[process]["high"],
                                         processes[process]["low"]):

                if (seed >= low) and (seed <= high):
                    seeds_part1[idx] += dest - low
                    break        
    
    for seed in seeds_part1:
        if part1 == None:
            part1 = seed
        elif seed < part1:
            part1 = seed

    return part1
    

def solver2(seed_ranges: list[dict[str, int]], processes: dict[str, dict[str, list[int]]]) -> int:
    part2: int = None

    for process in processes:
        for seed in seed_ranges:
            for (dest, high, low) in zip(processes[process]["dest"],
                                         processes[process]["high"],
                                         processes[process]["low"]):
                
                increase = dest - low
                # Within a range
                if  seed["low"] >= low and seed["high"] <= high:
                    seed["high"] += increase 
                    seed["low"] += increase
                    break
                
                # Sliding "above" upper limit
                elif seed["high"] > high and seed["low"] >= low and seed["low"] < high :
                    seed_ranges = add_seed_range(seed_ranges, seed["high"], high+1)
                    seed["high"] = high + increase
                    seed["low"] += increase
                    break
                
                # Sliding "below" lower limit
                elif seed["low"] < low and seed["high"] <= high and seed["high"] > low:
                    seed_ranges = add_seed_range(seed_ranges, low-1, seed["low"])
                    seed["low"] = low + increase
                    seed["high"] += increase
                    break
                
                # Encapsulating full span and extra over/under
                elif seed["low"] < low and seed["high"] > high:
                    seed_ranges = add_seed_range(seed_ranges, seed["high"], high+1)
                    seed_ranges = add_seed_range(seed_ranges, low-1, seed["low"])
                    seed["low"] = low + increase
                    seed["high"] = high + increase 
                    break
    
    for seed in seed_ranges:
        if part2 == None:
            part2 = seed["low"]
        elif seed["low"] < part2:
            part2 = seed["low"]
    
    return part2

if __name__=="__main__":
    s = time.time()
    filename = "input/input.txt"
    seeds_part1, seed_ranges, processes = parser(filename)
    part1_sum = solver1(seeds_part1, processes)
    part2_sum = solver2(seed_ranges, processes)

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")
    print(f"Time taken: {time.time()-s}")