#!/usr/bin/python3
from collections import defaultdict
import functools

"""
# == rocks
. == empty
O == balls

x,y grid with obstacles (#)

alternative 1:
store all 
"""



def parser(filename: str) -> list[str]:
    with open(filename, "r") as file:
        array = list(map(lambda x: x.strip(), file.readlines()))
        #print(array)
    return array

def parser2(filename):
    array = []
    with open(filename) as file:
        for line in file:
            array.append([x for x in line.strip()])    

    return array

def parser3(filename):
    data: dict = {}
    with open(filename, "r") as file:
        for idx_y, line in enumerate(file):
            for idx_x, char in enumerate(line.strip()):
                data[idx_x, idx_y] = char

        y_size = idx_y+1
        x_size = idx_x+1
    
    properties: dict = {"size": (x_size, y_size)}

    return data, properties

def running_count(array: list[str]):
    part1_sum: int = 0

    x_size = len(array[0])
    y_size = len(array) 

    points_array = [y_size]*x_size
    #print(points_array)
    for idx_y, string in enumerate(array):
        for idx_x, char in enumerate(string):
            if char == "O":
                part1_sum += points_array[idx_x]
                
                print(idx_x, idx_y, points_array[idx_x])
                # replacement in array
                if not array[y_size - points_array[idx_x]][idx_x] == "O":
                    array[y_size - points_array[idx_x]][idx_x] = "O"
                    array[idx_y][idx_x] = "."

                # Modifying array with points 
                points_array[idx_x] -= 1
                #print(idx_y, idx_x, points_array)
                #print(array[idx_y], idx_x)
            elif char == "#":
                points_array[idx_x] = y_size - (idx_y + 1)

    #print(points_array)
    return part1_sum, array

def new_count(array: list[list[str]]):
    part1_sum: int = 0
    
    x_size = len(array[0])
    y_size = len(array)

    return

def running_count_dict(data: dict, properties: dict):
    part1_sum: int = 0

    x_max, y_max = properties["size"]
    points_array = [y_max] * x_max

    for y in range(y_max):
        for x in range(x_max):
            if data[x, y] == "O":
                part1_sum += points_array[x]

                if not data[x, (y_max-points_array[x])] == "O":
                    data[x, (y_max - points_array[x])] = "O"
                    data[x, y] = "."
                
                points_array[x] -= 1
            
            elif data[x, y] == "#":
                points_array[x] = y_max - (y + 1)

    return part1_sum, data


def spinning_cycle(array: list[str]) -> list[str]:
    x_size = len(array[0])
    y_size = len(array)

    sum1, array = running_count(array)
    #for r in array:
        #print(r)
    #print(sum1)
    #print(sum1)
    temp_sum: int = 0
    temp_sum_arr = []
    low_sum = 0
    
    # Clockwise rotation
    for i in range(12):
        array = [list(x) for x in zip(*reversed(array))]
        sum1, array = running_count(array)
        temp_sum += sum1
        print(sum1)
        if i % 4 == 0:
            if temp_sum in temp_sum_arr:
                print(f"cycle found in array on iteration {i}, with array index {temp_sum_arr.index(temp_sum)}, and sum {sum1}")
            else:
                print(f"Cycle not found in array")
                temp_sum_arr.append(temp_sum)
            temp_sum = 0
    
    print(len(temp_sum_arr))
    print(low_sum)

    sum1, t = running_count(array)
    array = [list(x) for x in zip(*reversed(array))]
    #sum1, array = running_count(array)
    #print(sum1)
    for r in array:
        for c in r:
            print(f"{c}", end="")
        print(end="\n")
    print()
    #print(sum1)

def compare_time(array, data, properties, iterations) -> None:
    import time
    s = time.time()
    for i in range(1000000):
        part1_sum, data = running_count_dict(data, properties)
    print(part1_sum, f"\tTime taken for dict[tuple[int, int], str]: {time.time()-s}")


    s2 = time.time()
    for i in range(1000000):
        part1_sum, array = running_count(array)
    print(part1_sum, f"\tTime taken for list[list[str]]: {time.time()-s2}")

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    #test = ["str", "new"]
    #test[0] = "newi_new" 
    #print(test)

    filename = "input/sample.txt"
    #array = parser(filename)
    array = parser2(filename)
    data, properties = parser3(filename)
    spinning_cycle(array)


    facit = running_count(parser2('input/sample1.txt')) 
    print(f"1 cycle answer: {facit[0]} for array:")
    for r in facit[1]:
        for c in r:
            print(c, end="")
        print(end="\n")
    #compare_time(array, data, properties, 1000000)

    #for r in array:
    #    print(r)

    # Sample 1 -> 87
    # Sample 2 ->
    # Sample 3 -> 69

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")
