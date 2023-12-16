#!/c/ProgramData/Anaconda3/python
from collections import defaultdict

# Creating dictionary to for each of current "directions" and mapping to new direction(s) on new "tile"
DIRECTIONS = {(-1,0): {".": [(-1,0)], "/": [(0,1)], "\\": [(0,-1)], "|": [(0,1), (0,-1)], "-": [(-1,0)]},       # Right
              (1,0): {".": [(1,0)], "/": [(0,-1)], "\\": [(0,1)], "|": [(0,1), (0,-1)], "-": [(1, 0)]},         # Left
              (0,-1): {".": [(0,-1)], "/": [(1,0)], "\\": [(-1,0)], "|": [(0,-1)], "-": [(-1,0), (1,0)]},       # Down
              (0,1): {".": [(0,1)], "/": [(-1,0)], "\\": [(1,0)], "|": [(0,1)], "-": [(-1,0), (1,0)]}           # Up
              }


def parser(filename: str):
    puzzle: dict[tuple[int, int], str] = {}
    with open(filename, "r") as file:
        for idx_y, line in enumerate(file):
            for idx_x, char in enumerate(line.strip()):
                puzzle[(idx_x, idx_y)] = char
    
    PUZZLESIZE = (idx_x+1, idx_y+1)
    
    return  puzzle, PUZZLESIZE

def print_puzzle(puzzle, uniques = None) -> None:
    for i in range(PUZZLESIZE[1]):
        for j in range(PUZZLESIZE[0]):
            if (j,i) in uniques:
                print("#", end="")
            else:
                print(".", end="")
        print(end="\n")

def new_node(node, dir):
    x = node[0] - dir[0]
    y = node[1] - dir[1]
    return x,y

def node_valid(node):
    if (node[0] > (PUZZLESIZE[0]-1)) or (node[0] < 0):
        return False
    elif (node[1] > (PUZZLESIZE[1]-1)) or (node[1] < 0):
        return False
    else:
        return True

def solver(puzzle: dict[tuple[int, int], str], start: tuple[int, int], dir: tuple[int, int]) -> int:
    visited: dict[tuple[int ,int], int] = defaultdict()

    node = start
    dir = DIRECTIONS[dir][puzzle[node]]
    queue = []
    for d in dir:
        queue.insert(0, (new_node(node, d), d))
        visited[(node, d)] = 1

    while queue:
        # curr - new = dir
        # new = curr - dir
        v_node = queue.pop()
        node, dir = v_node
        if not node_valid(node) or v_node in visited:
            if len(queue) == 0:
                break
            else:
                continue
        
        if v_node not in visited:
            visited[v_node] = 1

        node_char = puzzle[node]
        dir = DIRECTIONS[dir][node_char]
        for d in dir:
            queue.insert(0, (new_node(node, d), d))
    
    return visited

def get_best_configuration(puzzle):
    best_configuration: dict[tuple[int, int, str], int] = {}
    
    for y in range(PUZZLESIZE[1]):
        for x in [0, PUZZLESIZE[0] - 1]:
            if x == 0:
                best_configuration[(x,y,"x")] = len(count_unique_nodes(solver(puzzle, (x,y), (-1, 0))))
            else:
                best_configuration[(x,y,"x")] = len(count_unique_nodes(solver(puzzle, (x,y), (1, 0))))

    for x in range(PUZZLESIZE[0]):
        for y in [0, PUZZLESIZE[1] - 1]:
            if y == 0:
                best_configuration[(x,y,"y")] = len(count_unique_nodes(solver(puzzle, (x,y), (0, -1))))
            else:
                best_configuration[(x,y,"y")] = len(count_unique_nodes(solver(puzzle, (x,y), (0, 1))))

    return best_configuration

def count_unique_nodes(visited: dict[tuple[tuple[int, int], int]]):
    unique_nodes: dict = {}
    for val in visited:
        node, dir = val
        if node not in unique_nodes:
            unique_nodes[node] = 1
    
    return unique_nodes

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/input.txt"
    puzzle, PUZZLESIZE = parser(filename)
    visited = solver(puzzle, (0,0), (-1,0))
    uniques = count_unique_nodes(visited)
    variations = get_best_configuration(puzzle)
    
    part1_sum = len(uniques)
    part2_sum = max(variations.values())
    #print_puzzle(puzzle, uniques)
    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")