
#!/usr/bin/python3
import os,sys
sys.path.append(os.getcwd())
from collections import defaultdict
import math,re
from functools import reduce
from util.solution import Solution
from dataclasses import dataclass

Datatype = []

def parser(filename: str, part2=False):
    return

def solver(data: Datatype, part2=False):
    return

if __name__=="__main__":
    day = "day22"
    input = f"{day}/input/input.txt"
    test = f"{day}/input/sample.txt"
    test_result = 32000000
    
    solution = Solution(parser, solver, input)
    solution.test_input([test], [test_result])
    solution.solve(test=True, part1=True, part2=False)
    solution.display_result()