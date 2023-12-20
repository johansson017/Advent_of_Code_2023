#!/usr/bin/python3
import os,sys
sys.path.append(os.getcwd())
from collections import defaultdict
from util.solution import Solution



def parser(filename):
    return 

def solver(data, part2: bool = False):
    return 

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    input = "input/sample.txt"
    test1 = "input/sample.txt"
    test1_result = 0
    #test2 = "input/sample2.txt"

    solution = Solution(parser, solver, input)
    solution.test_input([test1], [test1_result])
    solution.solve(test=True, part1=True, part2=True)
    solution.display_result()