#!/usr/bin/python3
from collections import defaultdict

def parser(filename: str) -> list[list[str]]:
    array = []
    with open(filename) as file:
        for line in file:
            array.append([x for x in line.strip()])    

    return array

def shifting_array(array: list[str]) -> list[list[str]]:
    x_size = len(array[0])
    y_size = len(array) 

    moving_array = [y_size]*x_size

    for idx_y, string in enumerate(array):
        for idx_x, char in enumerate(string):
            if char == "O":
                # Replacement in array
                if not array[y_size - moving_array[idx_x]][idx_x] == "O":
                    array[y_size - moving_array[idx_x]][idx_x] = "O"
                    array[idx_y][idx_x] = "."

                # Modifying array with points 
                moving_array[idx_x] -= 1

            elif char == "#":
                moving_array[idx_x] = y_size - (idx_y + 1)

    return array

def counting_load(array: list[list[str]]):
    load: int = 0
    x_size = len(array[0])
    y_size = len(array)

    for idx_y in range(y_size):
        for idx_x in range(x_size):
            if array[idx_y][idx_x] == "O":
                load += (y_size - idx_y)

    return load

def find_pattern(array: list[list[str]]) -> int:
    distance: int = 0



    return distance

def spinning_cycle(array: list[str], cycles: int = 1) -> list[str]:
    part1_sum: int = 0
    part2_sum: int = 0

    part1_sum = counting_load(shifting_array(array))

    temp_sum: int = 0
    temp_sum_arr = []

    cycles = cycles*4
    repeat_array: list[int] = []
    found_pattern: bool = False

    # 3600 -> 800 cycles between each value align
    # Anti-Clockwise rotation
    i = 1 
    while i <= cycles:
        array = shifting_array(array)
        array = [list(x) for x in zip(*reversed(array))]


        #if i > 3950000000:
            #print_array(array)
            #break
        if i % 4 == 0:
            load = counting_load(array)
            
            if load in temp_sum_arr:
                if not found_pattern:
                    if i - last_append > 10000:

                        repeat_array.append(load)
                        #if i % 4 == 0:

                        if load in repeat_array and len(repeat_array) > 1000:
                            reversed_repeat_arr = list(reversed(repeat_array))
                            rep_index = reversed_repeat_arr.index(load)
                            diff_index = reversed_repeat_arr[rep_index+1:].index(load) + 1

                            #print(load, repeat_array, rep_index, diff_index)
                            loops = 0
                            for j in range(2,10):
                                if repeat_array[rep_index:rep_index+diff_index] == repeat_array[rep_index+(j-1)*diff_index:rep_index+j*diff_index]:
                                    loops += 1
                        
                            if loops == 8:
                                #print(len(repeat_array))
                                print(f"found loop with reoccuring distance {diff_index}")
                                found_pattern = True
                                print_array(array)
                                i = cycles - (diff_index*4)
                                print((cycles-i)%diff_index)
                                print(i)

 
                        #comp_array = []
                        ##backwards_repeat_array = list(reversed(repeat_array))
                        #for rep_idx, val in enumerate(repeat_array):
                            #if val == load:
                                #print(comp_array)
                                #if val in comp_array:
                                    #index_diff = rep_idx - recent_index
                                    #if comp_array == repeat_array[recent_index:rep_idx]:
                                        #found_pattern = True
                                        #print(index_diff, found_pattern)
                                        #break
                                #else:
                                    #recent_index = rep_idx
                                    #comp_array.append(val)


                         


                #if i % len(temp_sum_arr) == 0:
                    #if load == recent_load:
                        #print(True)
                        #break
                    #else:
                        #recent_load = load
                        #print(recent_load, i)
                #else:
                    #continue
            else:
                last_append = i
                temp_sum_arr.append(load)

        i += 1

    print_array(array)
    part2_sum = counting_load(array)

    return part1_sum, part2_sum

def print_array(array: list[list[str]]) -> None:
    for r in array:
        for c in r:
            print(c, end="")
        print(end="\n")

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/input.txt"
    array = parser(filename)
    part1_sum, part2_sum = spinning_cycle(array, 1000000000)

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")
