#!/c/ProgramData/Anaconda3/python
from collections import defaultdict
from typing import TypedDict, Union
from colorama import just_fix_windows_console
just_fix_windows_console()
"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""
Datatype = dict[str, Union[tuple[int, int], dict[tuple[int, int], str]]]
Puzzletype = dict[tuple[int, int], str]
Visitedtype = list[tuple[int, int]]

NORTH = ["7", "F", "|"]
SOUTH = ["L", "J", "|"]
WEST = ["F", "L", "-"]
EAST = ["7", "J", "-"]

# Map possible direction from order (west, east, south, north)
POSSIBILITIES = {"|": [[], [], ["L", "J", "|"], ["7", "F", "|"]],
 "-": [["F", "L", "-"],["J", "7", "-"],[],[]],
 "L": [[], EAST, [], NORTH],
 "J": [WEST, [], [], NORTH],
 "7": [WEST, [], SOUTH, []],
 "F": [[], EAST, SOUTH, []],
 "S": [WEST, EAST, SOUTH, NORTH]}

CROSS_PAIRS = {"F": "J", "L": "7"}

def empty_puzzle(filename: str) -> Datatype:
    with open(filename, "r") as file:
        sizes = file.readlines()
        y_size = len(sizes)
        x_size = len(sizes[0].strip())
    
    puzzle: dict = defaultdict()
    puzzle["nodes"] = {}
    for x in range(x_size+2):
        for y in range(y_size+2):
            puzzle["nodes"][x,y] = '.'
    puzzle["sizes"] = (x_size+2, y_size+2)
    return puzzle

def parser(filename: str, puzzle: Datatype) -> Datatype:
    with open(filename) as file:
        for idx_y, line in enumerate(file):
            for idx_x, char in enumerate(line.strip()):
                if char == 'S':
                    puzzle["start"] = (idx_x+1, puzzle["sizes"][1]-(idx_y+2))

                puzzle["nodes"][idx_x+1, puzzle["sizes"][1]-(idx_y+2)] = char
    
    return puzzle

def print_puzzle(puzzle: Puzzletype, visited: Visitedtype, inside_nodes: Visitedtype, colored = False) -> None:
    x_s, y_s = puzzle["sizes"]
    nodes = puzzle["nodes"]
    for y in range(y_s-1,-1,-1):
        for x in range(x_s):
            if (x, y) in visited:
                if colored:
                    print(f"\033[91m{nodes[x,y]}\033[00m", end="")
                else:
                    print(f"{nodes[x,y]}", end="")
            elif (x, y) in inside_nodes:
                if colored:
                    print(f"\033[92m{nodes[x,y]}\033[00m", end="")
                else:
                    print(f"{nodes[x,y]}", end="")
            else:
                    print(f"{nodes[x,y]}", end="")
        print()

def find_direction(puzzle: Puzzletype, node: tuple[int, int]) -> Visitedtype:
    new_nodes: Visitedtype = []
    x, y = node
    char = puzzle[node]
    directions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    
    for dir, pos_dir in zip(directions, POSSIBILITIES[char]):
        if puzzle[dir] in pos_dir:
            new_nodes.append(dir)

    return new_nodes

def depth_search_iter(puzzle: Puzzletype, visited: list, node: tuple[int, int]):
    stack: list = []
    stack.insert(0, node)
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            for edge in find_direction(puzzle, node):
                stack.insert(0, edge)
        
    return visited

def solver1(puzzle: Datatype) -> tuple[int, Visitedtype]:
    part1_sum: int = 0 
    start_x, start_y = puzzle["start"]
    visited: list = []
    
    visited = depth_search_iter(puzzle["nodes"], visited, (start_x, start_y))
    part1_sum = int(len(visited)/2)

    return part1_sum, visited

def is_pipe_crossing(puzzle: Puzzletype, node: tuple[int, int], x_max):
    x, y = node
    crossing = True
    for x_new in range(x+1, x_max):
        if puzzle[x_new, y] == "-":
            continue
        elif puzzle[x_new, y] in CROSS_PAIRS[puzzle[x, y]]:
            break
        else:
            crossing = False
            break

    return crossing, x_new

def solver2(puzzle: Puzzletype, sizes: tuple[int, int], visited: Visitedtype, unvisited: Visitedtype) -> tuple[int, Visitedtype]:
    part2_sum: int = 0
    inside_nodes: Visitedtype = []

    x_max, y_max = sizes
    for node in unvisited:
        right_count = 0
        for x in range(node[0]+1, x_max):
            if (x, node[1]) in visited:
                if puzzle[x, node[1]] == "|":
                    right_count += 1
                elif puzzle[x, node[1]] == "F" or puzzle[x, node[1]] == "L":
                    crossing, x = is_pipe_crossing(puzzle, (x, node[1]), x_max)
                    right_count += crossing
        
        if right_count % 2 != 0:
            inside_nodes.append(node)

    part2_sum = len(inside_nodes)

    return part2_sum, inside_nodes

def unvisited_nodes(puzzle: Puzzletype, visited: Visitedtype) -> Visitedtype:
    unvisited: Visitedtype = []
    for key in puzzle:
        if key not in visited:
            unvisited.append(key)

    return unvisited


if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/sample3.txt"
    puzzle = empty_puzzle(filename)
    puzzle = parser(filename, puzzle)
    
    part1_sum, visited = solver1(puzzle)
    unvisited = unvisited_nodes(puzzle["nodes"], visited)
    part2_sum, inside_nodes = solver2(puzzle["nodes"], puzzle["sizes"], visited, unvisited)
    print_puzzle(puzzle, visited, inside_nodes, colored=True)

    # 6773, 493 
    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")