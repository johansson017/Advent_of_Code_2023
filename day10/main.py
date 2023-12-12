#!/usr/bin/python3
from collections import defaultdict

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
Puzzletype = dict[tuple[int, int], str]
Visitedtype = list[tuple[int, int]]

NORTH = ["7", "F", "|"]
SOUTH = ["L", "J", "|"]
WEST = ["F", "L", "-"]
EAST = ["7", "J", "-"]

# Map possible direction from order (west, east, south, north)
possibilities = {"|": [[], [], ["L", "J", "|"], ["7", "F", "|"]],
 "-": [["F", "L", "-"],["J", "7", "-"],[],[]],
 "L": [[], EAST, [], NORTH],
 "J": [WEST, [], [], NORTH],
 "7": [WEST, [], SOUTH, []],
 "F": [[], EAST, SOUTH, []],
 "S": [WEST, EAST, SOUTH, NORTH]}

#print("\u231C")
#print("\u231D")
#print("\u231E")
#print("\u231F")
replacers = {"7": "\u231D", "L": "\u231E", "J": "\u231F", "F": "\u231C", "S": "S", "-": "-", "|": "|"}

# Nonblockers in west,east,south,north
#nonblockers = {["7", "J"],
               #["L", "F", "-", "J"],
               #["7", "F", "L"]}


def empty_puzzle(filename: str) -> Puzzletype:
    with open(filename, "r") as file:
        sizes = file.readlines()
        y_size = len(sizes)
        x_size = len(sizes[0].strip())
    
    puzzle: dict = defaultdict()
    for x in range(x_size+2):
        for y in range(y_size+2):
            puzzle[x,y] = '.'
    puzzle["sizes"] = (x_size+2, y_size+2)

    return puzzle

def parser(filename: str, puzzle: Puzzletype) -> Puzzletype:
    with open(filename) as file:
        for idx_y, line in enumerate(file):
            for idx_x, char in enumerate(line.strip()):
                if char == 'S':
                    puzzle["start"] = (idx_x+1, puzzle["sizes"][1]-(idx_y+2))
                    #print(puzzle["start"], puzzle["sizes"])

                puzzle[idx_x+1, puzzle["sizes"][1]-(idx_y+2)] = char
    
    #print(puzzle)
    return puzzle

def print_puzzle(puzzle: Puzzletype, visited: Visitedtype, unvisited: Visitedtype) -> None:
    x_s, y_s = puzzle["sizes"]
    for y in range(y_s-1,-1,-1):
        for x in range(x_s):
            if (x, y) in visited:
                print(f"\033[91m{replacers[puzzle[x,y]]}\033[00m", end="")
            elif (x, y)  in unvisited:
                print(f"{puzzle[x,y]}", end="")
            else:
                print(f"\033[92m{puzzle[x,y]}\033[00m", end="")
        print()

def find_direction(puzzle: Puzzletype, node: tuple[int, int]) -> Visitedtype:
    new_nodes: Visitedtype = []
    x, y = node
    char = puzzle[node]
    #print(char)
    directions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    
    for dir, pos_dir in zip(directions, possibilities[char]):
        if puzzle[dir] in pos_dir:
            #print(char, node, dir, pos_dir, True)
            new_nodes.append(dir)

    #print(char, new_nodes) 
    return new_nodes

def find_unvisited_direction(puzzle, visited: Visitedtype, node: tuple[int, int]) -> Visitedtype:
    x, y = node
    directions = [(max(x-1,0), y), (min(puzzle["sizes"][0], x+1), y), (x, max(0, y-1)), (x, min(puzzle["sizes"][1], y+1))]
    unvisited: Visitedtype = []

    for idx, dir in enumerate(directions):
        if dir not in visited:
           unvisited.append(dir)
        


    return unvisited

def find_nested_enclosure(puzzle: Puzzletype, node, direction):
    return

def depth_search(puzzle: Puzzletype, visited: list, node: tuple[int, int]):
    visited.append(node)
    for direction in find_direction(puzzle, node):
        if direction not in visited:
            depth_search(puzzle, visited, direction)
    return visited

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

def breadth_search(puzzle: Puzzletype, visited: Visitedtype, unvisited: Visitedtype, node: tuple[int, int]) -> Visitedtype:
    queue: Visitedtype = []
    unvisited.append(node)
    queue.insert(0, node)
    while queue:
        node = queue.pop()
        for edge in find_direction(puzzle, node):
            break
            
    return

def solver(puzzle: Puzzletype) -> tuple[int, Visitedtype]:
    part1_sum: int = 0 
    start_x, start_y = puzzle["start"]
    visited: list = []

    visited = depth_search_iter(puzzle, visited, (start_x, start_y))
    part1_sum = int(len(visited)/2)

    return part1_sum, visited

def solver2(puzzle: Puzzletype, visited: Visitedtype):
    start = (0, 0)
    unvisited: Visitedtype = []
    queue: Visitedtype = []
    queue.append(start)

    while queue:
        node = queue.pop()
        if node not in unvisited:
            unvisited.append(node)
            
            for edge in find_unvisited_direction(puzzle, visited, node):
                queue.insert(0, edge)

    return unvisited

def unvisited_nodes(puzzle: Puzzletype, visited: Visitedtype) -> Visitedtype:
    unvisited: Visitedtype = []
    for key in puzzle:
        if key not in visited:
            unvisited.append(key)

    return unvisited


if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/sample4.txt"
    puzzle = empty_puzzle(filename)
    puzzle = parser(filename, puzzle)
    #print_puzzle(puzzle)
    part1_sum, visited = solver(puzzle)
    #unvisited = unvisited_nodes(puzzle, visited)
    unvisited = solver2(puzzle, visited)
    print_puzzle(puzzle, visited, unvisited)

    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")