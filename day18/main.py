#!/usr/bin/python3
from collections import defaultdict

DIRECTIONS = {"R": (1,0), "D": (0, 1), "L": (-1, 0), "U": (0, -1)}

"""
Parse data and create trench map (start at (0,0))
1. Keep data (input) as list of instruction including tuples with (direction tuple[int, int], steps: int, code: str)
2. Create empty map: dict[coords: tuple[int, int], code: str]
Dig down inside of trench boundary (1 m)
3. Fill-algorithm?
"""

Datatype = list[tuple[int, int], int, str]
Trenchtype = dict[tuple[int, int], str]


# Part 2 -> Store data for corners:
# list[tuple[int, int]]
def parser(filename: str, part2=False, hexa_enable=True):
    data: Datatype = []
    if part2:
        with open(filename, "r") as file:
            x_cord = 0
            y_cord = 0
            for idx, line in enumerate(file):
                if hexa_enable:
                    hexacode = hexacode.strip("()")
                    hexacode = line.strip().split()[2].strip("()")
                    length, _dir = int(hexacode[1:-1], base=16), int(hexacode[-1])
                    _dir = [*DIRECTIONS.items()][_dir][0]
                else:
                    _dir, length, hexacode = line.strip().split()
                    length = int(length)

                match _dir:
                    case "R":
                        x_cord += length+1
                    case "L":
                        x_cord -= length+1
                    case "U":
                        y_cord -= length+1
                    case "D":
                        y_cord += length+1

                data.append((x_cord, y_cord, idx))
    else:
        data = [(DIRECTIONS[_dir], int(steps), code.strip("()")) for _dir,steps,code in ((line.strip().split() for line in open(filename)))]
    return data

def dig_trench(data: Datatype) -> Trenchtype:
    trench: Trenchtype = {}
    dig_pos = (0,0)
    trench[dig_pos] = "start"

    # Instruction = [direction, steps, code] 
    for instruction in data:
        for _ in range(instruction[1]):
            dig_pos = add_tuple(dig_pos, instruction[0])
            trench[dig_pos] = instruction[2]
    
    return trench

def add_tuple(t1, t2) -> tuple[int ,int]:
    return tuple(map(sum, zip(t1, t2)))

def mult_tuple(t1, t2) -> tuple[int, int]:
    return tuple(map(lambda a,b: a*b, t1, t2))

def fill_trench(trench: Trenchtype) -> int:
    # Add new start point "diagonal" to start
    dig_pos = (1,1)

    queue = []
    queue.append(dig_pos)

    while queue:
        dig_pos = queue.pop()

        # new_dir = tuple[dir_str: str, dir_coords: tuple[int, int]]
        for new_dir in [*DIRECTIONS.items()]:
            new_fill = add_tuple(dig_pos, new_dir[1])
            if new_fill not in trench:
                trench[new_fill] = "empty"
                queue.insert(0, new_fill)
    
    return len(trench.keys())

# return tuple consisting of (steps, direction)
def trench_corners(data) -> tuple[int, str]:
    new_node = (0, 0)
    instr_list = []

    for instruction in data:
        #distance = mult_tuple(instruction[0], (instruction[1], instruction[1]))
        #new_node = add_tuple(new_node, distance)
        instr_list.append((instruction[1], instruction[2]))

    return instr_list
#def print_trench(trench: Trenchtype) -> None:

#def print_trench(instructions) -> None:
def calculate_trench(instruction) -> int:
    print(instruction)
    total_area = 0
    last_down = 0
    last_up = 0
    last_horizontal = 0

    #[(start, end, horizontal_coord)]
    total_downs = set()
    total_ups = set()

    cons_x = 0
    cons_y = 0
    
    for ins in instruction:
        if ins[1] == "D":
            dest_x = last_down + ins[0]
            source_x = last_down
            last_down = dest_x
            last_up = last_up + ins[0] 


            total_downs.add((source_x, dest_x, last_horizontal))
        elif ins[1] == "U":
            dest_y = last_up - ins[0]
            source_y = last_up
            last_up = dest_y
            last_down = last_down - ins[0] 
            
            total_ups.add((source_y, dest_y, last_horizontal))
        
        elif ins[1] == "R":
            last_horizontal += ins[0]
            
        elif ins[1] == "L":
            last_horizontal -= ins[0]

    print(f"Downs: {total_downs}")
    print(f"Ups: {total_ups}")
    #for down in total_downs:
        #print(down) 
    #for ins in instruction:
        #if ins[1] == "D":
            #delta_y = ins[0][0] - last_down
        #if ins[1] == "U":
            #delta_y = 
    print(calculate_area(total_downs, total_ups)) 

def calculate_area(data):
    total_area = 0
    data = sorted(data, key=lambda x: x[1])
    #print(data)
    
    while data:
        # construct "rows" with vertices on same y coords
        y_rows = []
        area_containers = []
   
        min_y = data.pop(0)
        y_rows.append(min_y)
        if data:
            while min_y[1] == data[0][1]:
                min_y = data.pop(0)
                y_rows.append(min_y)
                if not data:
                    break
        
        x_min_row = min(y_rows, key=lambda x: x[0])
        x_max_row = max(y_rows, key=lambda x: x[0])
        #y_rows.sort(key=lambda x: x[2])

        y_rows = [x_max_row, x_min_row]
        if data:
            next_y = data[0]
            y_diff = next_y[1] - min_y[1]
            
            next_rows = [x for x in data if x[1] == next_y[1]]
            print(f"y_row: {y_rows}, next_row: {next_rows}")
            next_rows.sort(key=lambda x: x[0])

            horz_dist = x_min_row[0]
            while len(next_rows) > 2:
                temp_rows = []
                temp_rows.append((horz_dist, min_y[1]))
                horz_dist += next_rows[1][0]
                temp_rows.append((horz_dist, min_y[1]))
                temp_rows.append((horz_dist, y_diff))
                temp_rows.append((horz_dist-next_rows[1][0], y_diff))
                area_containers.append(temp_rows)
                next_rows.pop(0)
                next_rows.pop(0)
                break
            
            #print(f"Area nodes: {y_rows}") 
            #next_rows.sort(key=lambda x: x[0])
            if len(next_rows) <= 2:
                # "reverse insert to get rectangle"
                y_rows.insert(1, (y_rows[-1][0], y_diff))
                y_rows.insert(1, (y_rows[0][0], y_diff))
                area_containers.append(y_rows)


        #if data:
            #next_y = data.pop(0)
            #y_rows.append(next_y)
            #while next_y[1] == data[0][1]:
                #next_y = data.pop(0)
                #y_rows.append(next_y)
                #if not data:
                    #break
        #y_rows.sort(key=lambda x: x[2])
        #print(y_rows)
        for a_c in area_containers:
            for idx in range(len(a_c)):
                n_idx = (idx+1) % len(a_c)
                x_mult = a_c[idx][0] + a_c[n_idx][0]
                y_mult = a_c[idx][1] - a_c[n_idx][1]
            
                total_area += x_mult * y_mult
        
    #for idx in range(len(data)):
        #n_idx = (idx+1) % len(data)
        #total_area += abs((data[idx][0] +  data[n_idx][0]) * (data[idx][1] - data[n_idx][1]))
        print(area_containers, total_area) 
    return int(abs(total_area / 2))


def calc_test(data):
    total_area = 0
    for idx in range(len(data)):
        n_idx = (idx+1) % len(data)
       
        x_mult = data[idx][0] + data[n_idx][0]
        y_mult = data[idx][1] - data[n_idx][1]
            
        total_area += x_mult * y_mult

        print(f"given points: {data[idx], data[n_idx]},\t we calculate AREA: {total_area}")

    return int(abs(total_area / 2))
# NOTE: CHECK IF NODE INSIDE AREA BY PIPE CROSSING

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/sample.txt"
    #data = parser(filename)
    #trench = dig_trench(data)
    #part1_sum = fill_trench(trench)

    data = parser(filename, part2=True, hexa_enable=False)
    
    #print(f"sum of calculate area: {calculate_area(data)}")
    print(f"sum of calculate test are: {calc_test(data)}")


    #assert calculate_area([(0,1), (1,1), (1,0), (0,0)]) == 1
    #assert calculate_area([(0,2), (1,2), (1,1), (2,1), (2,0), (0,0)]) == 3
    ##print(calculate_area([(0,4), (2,4), (2,3), (1,3), (1,2), (3,2), (3,0), (0,0)]))
    #assert calc_test([(0,4), (2,4), (2,3), (1,3), (1,1), (2,1), (2,2), (3,2), (0,0)]) == 8

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")