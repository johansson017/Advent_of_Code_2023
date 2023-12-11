#!/c/msys64/mingw64/bin/python3
from collections import defaultdict


def line_difference(array: list[int]) -> list[int]:
    new_array: list[int] = []
    for idx in range(len(array)-1):
        new_array.append(array[idx+1]-array[idx])
    return new_array

def recursive_line_solver(array: list[int], pyramid_list: list[list[int]]) -> list[list[int]]:
    new_array = line_difference(array)
    if new_array.count(0) == len(new_array) and new_array != None:
        pyramid_list.append(new_array)
        return pyramid_list
    else:
        pyramid_list.append(new_array)
        return recursive_line_solver(new_array, pyramid_list)

def forming_number_series(data):
    series: dict = defaultdict()
    for idx, serie in enumerate(data):
        pyramid_list: list[list[int]] = [serie]
        series[idx] = recursive_line_solver(serie, pyramid_list)

    return series  

def solver1(series: dict):
    part1_sum: int = 0
    for key, val in series.items():
        for idx, v in enumerate(val[::-1]):
            if idx == 0:
                val[-(idx+1)].append(0)
            else:
                val[-(idx+1)].append(v[-1]+val[-(idx)][-1])
        part1_sum += val[0][-1]
    
    return part1_sum

def solver2(series: dict):
    part2_sum: int = 0
    for key, val in series.items():
        for idx, v in enumerate(val[::-1]):
            if idx == 0:
                val[-(idx+1)].insert(0, 0)
            else:
                val[-(idx+1)].insert(0, v[0]-val[-(idx)][0])
        part2_sum += val[0][0]
    
    return part2_sum


def parser(filename) -> list[list[int]]:
    data: list[list[int]] = []    
    with open(filename) as file:
       for line in file:
           data.append(list(map(int, [x for x in line.strip().split()]))) 
    
    return data

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0
    
    # NOTE: Slightly overenginered

    filename = "input/input.txt"
    data = parser(filename)
    series = forming_number_series(data)
    part1_sum = solver1(series)
    part2_sum = solver2(series) 
    
    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")