#!/usr/bin/python3
import os,sys
sys.path.append(os.getcwd())
from collections import defaultdict
import math
from functools import reduce
from util.solution import Solution
from dataclasses import dataclass
"""
any -> returns true if any element == 1
all -> returns true if all element are same (1)

if all -> send 0
else -> send 1

Data:
parse (key) -> (prev | next)
"""

@dataclass
class Module:
    name: str
    type: str
    value: int = None
    prev: list[object] = None
    next: list[object] = None

# UGLY as FUCK parser...
def parser(filename: str):
    data: dict[str, list[str]] = {}
    module_dict = {}
    with open(filename, "r") as file:
        for line in file:
            key, next = line.strip().split("->")
            data[key.strip()] = {"next": list(map(str.strip, next.split(",")))}

    unique_keys = set()
    for key in data:
        data[key]["prev"] = []
        for k2 in data:
            for val in data[k2]["next"]:
                unique_keys.add(val)
                if val == key[1:] and k2 != "broadcaster":
                    data[key]["prev"].append(k2[1:])
    
    # Creating dict holding objects
    for key in data:
        if key == "broadcaster":
            module_dict[key] = Module(name=key, type="broadcaster", value=0)
        else:
            module_dict[key[1:]] = Module(name=key[1:], type=key[0])
            unique_keys.remove(key[1:])

    # Creating modules for leftover "endpoints"
    for key in unique_keys:
        module_dict[key] = Module(name=key, type=None, value=0)
    
    for key in data:
        if key[0] == "%":
            module_dict[key[1:]].value = 0
        elif key[0] == "&":
            memory = []
            for val in data[key]["prev"]:
                memory.append(module_dict[val])
            module_dict[key[1:]].prev = memory
            module_dict[key[1:]].value = 1
            
    for key in data:
        next_keys = []
        for val in data[key]["next"]:
            next_keys.append(module_dict[val])

        if key == "broadcaster":
            module_dict[key].next = next_keys
        else:
            module_dict[key[1:]].next = next_keys
        
        if key == "broadcaster":
            t_list = []
            for k in data[key]["next"]:
                t_list.append(module_dict[k])
            module_dict[key].next = t_list

    return module_dict

def update_and_get_pulse(sender, pulse):
    if sender.type == "%":
        sender.value ^= 1
        pulse = sender.value
        return pulse
    
    if sender.type == "&":
        input_list = list_value_from_modules(sender.prev)
        if all(input_list):
            sender.value = 0
        else:
            sender.value = 1
        pulse = sender.value
        return pulse 


def list_value_from_modules(modules: list[object]):
    input_list = []
    for mod in modules:
        input_list.append(mod.value)
    return input_list

def button_loop(data, part2: bool = False, match_list=None):
    low_count = 0
    high_count = 0

    queue: list[str] = []
    next_queue = data["broadcaster"].next
    pulse = 0
    low_count += 1
    match_found = None

    for n in next_queue:
        queue.append((n, pulse))

    while queue:
        sender, pulse = queue.pop(0)
        if pulse == 0:
            low_count += 1
        else:
            high_count += 1

        if part2:
            # Pulse equals one because of one previous -> reverts to send HIGH pulse (1)
            # Needed to get QB to send low pulse (0) to rx
            if sender.name in match_list and pulse == 0:
                match_found = sender.name

        if (sender.type == "%" and pulse == 1) or sender.type == None:
            continue

        pulse = update_and_get_pulse(sender, pulse)
        next_queue = sender.next 
        for target in next_queue:
            queue.append((target, pulse))
    
    if match_found:
        return match_found
    
    return low_count, high_count

def solver(data, part2: bool = False):
    if part2:
        # Four values goes to QB -> (KV, JG, RZ, MR) -> They must all be High (1) for RX to be sent low pulse
        # Run loop to find when these are all individually high (1), this is when it receives a 0 pulse from previous
        match_list = ["kv", "jg", "rz", "mr"]*2 
        match_dict = defaultdict(int)
        i = 0
        while not len(match_list) == 0:
            i += 1
            result = button_loop(data, part2=True, match_list=match_list)
            if result in match_list:
                match_dict[result] = i - match_dict[result]
                match_list.remove(result)
        # Exits loop when found loop for each value, using math.LCM to get answer for when they coincide
        return math.lcm(*match_dict.values())
    else:
        low_count = 0
        high_count = 0

        for i in range(1000):
            low, high = button_loop(data)
            low_count += low
            high_count += high
    
    return low_count*high_count


if __name__=="__main__":
    day = "day20"
    input = f"{day}/input/input.txt"
    test1 = f"{day}/input/sample.txt"
    test2 = f"{day}/input/sample2.txt"
    test1_result = 32000000
    test2_result = 11687500
    
    solution = Solution(parser, solver, input)
    solution.test_input([test1, test2], [test1_result, test2_result])
    solution.solve(test=True, part1=True, part2=True)
    solution.display_result()