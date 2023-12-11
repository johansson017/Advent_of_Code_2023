#!/usr/bin/python3
from collections import defaultdict
import functools
import math

def parser(filename) -> dict[str, str]:
    data: dict[str[dict[str, str]]] = defaultdict()

    with open(filename, "r") as file:
        instructions = file.readline().strip()
        file.readline()
        for line in file:
            source, others = line.split(" = ")
            left, right = others.strip(" ()\n ").split(",")
            data[source] = {"L": left.strip(), "R": right.strip()}
    data["instructions"] = instructions
    
    return data

def solver1(data: dict[str, str]) -> int:
    part1_sum: int = 0

    start = "AAA"    
    end = "ZZZ"
    while start != end:
        for ins in data["instructions"]: 
            part1_sum += 1

            if start == end:
                break

            start = data[start][ins]

    return part1_sum

def solver2(data: dict[dict[str, str]]) -> int:
    part2_sum: int = 0

    starts = []
    for key in data.keys():
        if key[2] == "A":
            starts.append(key)

    #starts = ['VGA', 'AAA', 'LHA', 'RHA', 'CVA', 'LDA'] 
    #ends   = ["PQZ", "ZZZ", "BKZ", "XNZ", "KJZ", "XLZ"]
    iter_to_find = []
    pairs = {"AAA": "ZZZ", "VGA": "PQZ", "LHA": "BKZ", "RHA": "XNZ", "CVA": "KJZ", "LDA": "XLZ"}
    for key, val in pairs.items():
        iterations = 0
        end = key
        while end != val:
            for ins in data["instructions"]:
                end = data[end][ins]
                iterations += 1
                if end == val:
                    print(f"Iterations for {key} to find {val} was: {iterations}")
                    iter_to_find.append(iterations)
                    break

    # All numbers share a great denominator (highest prime)
    prime_numbers = []
    for val in iter_to_find:
        prime_numbers.append(find_prime(val))

    new_iter_numbers = list(map(lambda x: int(x[0] / x[1]), zip(iter_to_find, prime_numbers)))    

    prime_numbers = set(prime_numbers+new_iter_numbers)
    part2_sum = functools.reduce(lambda a,b: a*b, prime_numbers)

    return part2_sum


def find_prime(val):
    maxPrime = 0
    while val % 2 == 0:
        maxPrime = 2
        val = val/2 

    for i in range(3, int(math.sqrt(val)) + 1, 2):
        while val % i == 0:
            maxPrime = i
            val = val / i
    
    if val > 2:
        maxPrime = val

    return int(maxPrime)
    

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/input.txt"
    data = parser(filename)
    part1_sum = solver1(data)
    part2_sum = solver2(data)

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")