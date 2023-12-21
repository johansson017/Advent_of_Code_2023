#!/usr/bin/python3
from collections import defaultdict
import re, copy
import itertools, functools
"""
Save instructions as dict with lambda?
dict[str, dict[str, callable]]
"""


# NOTE: Current fault is that there can be a list with same "char" but different function / treshold

def parser(filename: str):
    flow: dict[str, dict[str, callable | bool]] = {}
    parts: list[dict[str, int]] = [] 
    with open(filename, "r") as file:
        lines = file.readlines()
        sect_idx = lines.index("\n")
        
        flow_lines = lines[:sect_idx]
        for line in flow_lines:
            key, other = line.strip().split("{")
            flow[key] = {}
            for expr in other.strip("}").split(","):
                if ":" not in expr:
                    flow[key]["end"] = expr
                else:
                    key2, val = expr.split(":")
                    flow[key][key2] = val

        part_lines = lines[sect_idx+1:]
        for line in part_lines:
            part_nr = line.strip().strip("{}").split(",")
            p_dict = {}
            for c in part_nr:
                key, val = c.split("=")
                p_dict[key] = int(val)    
            parts.append(p_dict)
    
    return flow, parts

def string_function(f_expr: str | bool, val) -> bool:
    limit = int(re.split("<|>", f_expr)[1])
    if "<" in f_expr:
        return val < limit
    elif ">" in f_expr:
        return val > limit
    return True

def is_accepted(flow, part) -> bool:
    key1 = "in"
    while key1 != "R" and key1 != "A":
        for f_expr, key2 in flow[key1].items():
            if f_expr == "end":
                key1 = key2
                break

            p_char = f_expr[0]
            if string_function(f_expr, part[p_char]):
                key1 = key2
                break

    if key1 == "R":
        return False
    if key1 == "A":
        return True

def part1(flow, parts) -> int:
    rating = 0
    for part in parts:
        if is_accepted(flow, part):
            rating += sum(part.values())
    return rating


def part2(flow) -> int:
    combinations: int = 0
    mappings = {"x": 0, "m": 1, "a": 2, "s": 3}
    
    start = [range(1,4001), range(1,4001), range(1,4001), range(1,4001)]
    step = "in" 
    step_key = "s<1351"
    combinations = walk_through_flow(flow, step, step_key, start, mappings)
    
    #print(functools.reduce(lambda a,b: a*b, map(max, start)))
    
    return combinations

def calculate_new_range(string_f: str, values: list[range], mappings):
    char, val = re.split("<|>", string_f)
    val = int(val)
    range1 = copy.deepcopy(values)
    range2 = copy.deepcopy(values)
    if "<" in string_f:
        if min(values[mappings[char]]) < val:
            range1[mappings[char]] = range(min(values[mappings[char]]), val)
            range2[mappings[char]] = range(val, max(values[mappings[char]])+1)
        else:
            return values
    elif ">" in string_f:
        if max(values[mappings[char]]) > val:
            range1[mappings[char]] = range(val, max(values[mappings[char]])+1)
            range2[mappings[char]] = range(min(values[mappings[char]]), val)
        else:
            return values
            
        
    # Sending back range1, range2, step_key:
    # first range sent back goes to step_key
    return range1, range2



def walk_through_flow(flow, step, step_key, values: list[range], mappings):
    #if step_key == "R":
        #return 0
    #if step_key == "A":
        #return functools.reduce(lambda a,b: a*b, map(max, values)) 
    if step_key == "end":
        if flow[step][step_key] == "R":
            return 0
        elif flow[step][step_key] == "A":
            return functools.reduce(lambda a,b: a*b, map(max, values))
        step = flow[step][step_key]
        step_key = list(flow[step].keys())[0]
        return walk_through_flow(flow, step, step_key, values, mappings)
    
    ranges = calculate_new_range(step_key, values, mappings)
 
    next_step_key = copy.deepcopy(list(flow[step].keys()))
    next_step_key.pop(0)
    next_step_key = next_step_key[0]
    
    if len(ranges) == 4:
        return walk_through_flow(flow, step, next_step_key, ranges, mappings)
    else:
        range1, range2 = ranges
    
    old_step = flow[step][step_key]
    if old_step == "R":
        return walk_through_flow(flow, step, next_step_key, range2, mappings)
    elif old_step == "A":
        #print("range1: ",range1)
        return functools.reduce(lambda a,b: a*b, map(max, range1)) + walk_through_flow(flow, step, next_step_key, range2, mappings)
    else:
        old_step_key = list(flow[old_step].keys())[0]
        return walk_through_flow(flow, old_step, old_step_key, range1, mappings) + walk_through_flow(flow, step, next_step_key, range2, mappings)


# x m a s -> [0 1 2 3]
def calculate_accepted(var, letters: list[int], flow, mappings, HISTORY):
    key1 = "in"
    while key1 != "R" and key1 != "A":
        for f_expr, key2 in flow[key1].items():
            if f_expr == "end":
                key1 = key2
                break
            
            p_char = f_expr[0]
            if p_char == var:
                if string_function(f_expr, letters[mappings[p_char]]):
                    key1 = key2
                    break
            
            if letters[mappings[p_char]] == 4000:
                update_letters(f_expr, letters, mappings)
                key1 = key2
                #print(key2)
                #print(letters)
            
            if string_function(f_expr, letters[mappings[p_char]]):
                key1 = key2
                break
            
    if key1 == "R":
        return 0
    elif key1 == "A":
        str_id = "".join(map(str, letters))
        if str_id not in HISTORY:
            HISTORY[str_id] = 1
            return functools.reduce(lambda a,b: a*b, letters)
        else:
            return 0
        #print(functools.reduce(lambda a,b: a*b, letters))
        #print(letters)

def update_letters(f_expr: str, letters, mappings):
    comb = (re.split("<|>", f_expr))
    limit = int(comb[1])
    var = comb[0]
    if "<" in f_expr:
        letters[mappings[var]] = limit - 1
    elif ">" in f_expr:
        letters[mappings[var]] = 4000 - limit + 1



def string_function2(f_expr: str, val) -> bool:
    limit = int(re.split("<|>", f_expr)[1])
    if "<" in f_expr:
        return val < limit
    elif ">" in f_expr:
        return val > limit
    return True


def parser2(filename):
    limits = {"x": set(), "m": set(), "a": set(), "s": set()}
    flow = []
    with open(filename, "r") as file:
        lines = file.readlines()
        blank_idx = lines.index("\n")
        lines = lines[:blank_idx]

        for line in lines:
            key, line = line.strip().split("{")
            line = line.strip("{}").split(",")
            flow.append(line)

    return flow

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0


    filename = "input/sample.txt"
    flow, parts = parser(filename)
    #for k,v in flow.items():
        #print(k,v)
    part1_sum = part1(flow, parts)
    flow, parts = parser(filename)
    part2_sum = part2(flow)

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")