#!/c/ProgramData/Anaconda3/python
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

def find_loop(array: list[list[str]], found_patterns: dict[str, bool], index: int) -> int:
    string_id = "".join([x for l in array for x in l])
    
    if string_id in found_patterns:
        return True, found_patterns, string_id 
    else:
        found_patterns["".join([x for l in array for x in l])] = index
        return False, found_patterns, string_id
    
def cycle_array(array: list[list[str]]) -> list[list[str]]:
    for i in range(4):
        array = shifting_array(array)
        array = [list(x) for x in zip(*reversed(array))]
    return array

def solver(array: list[list[str]], cycles: int = 1, part1: bool = False) -> list[str]:
    found_patterns: dict[str, bool] = defaultdict()

    if part1:
        return counting_load(shifting_array(array))

    # Clockwise rotation
    for i in range(cycles):
        found_loop, found_patterns, string_id = find_loop(array, found_patterns, i)
        if found_loop:
            start_index = found_patterns[string_id]
            cycles_left = ((cycles - start_index) % (i - start_index))

            for i in range(cycles_left):
                array = cycle_array(array)

            return counting_load(array) 

        # Cycling array 
        array = cycle_array(array)



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
    part1_sum = solver(array, part1=True)
    part2_sum = solver(array, 1000000000)

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")
