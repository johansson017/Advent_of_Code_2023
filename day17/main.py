#!/c/ProgramData/Anaconda3/python
from collections import defaultdict
import math
from colorama import just_fix_windows_console
just_fix_windows_console()

def parser(filename: str):
    puzzle: dict[tuple[int, int], int] = {}
    with open(filename, "r") as file:
        for idx_y, line in enumerate(file):
            for idx_x, char in enumerate(line.strip()):
                puzzle[(idx_x, idx_y)] = int(char)

    puzzle_size = (idx_x, idx_y)

    return puzzle, puzzle_size

def node_valid(node: tuple[int, int], puzzle_size: tuple[int, int]) -> bool:
    if node[0] > puzzle_size[0] or node[0] < 0 or node[1] > puzzle_size[1] or node[1] < 0:
        return False
    return True


def find_new_nodes(puzzle_size: tuple[int, int, int],
                   node: tuple[tuple[int, int], tuple[int, int], list[int]],
                   ) -> list[tuple[int , int]]:
    x, y = node[0]
    directions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    streak = node[2] 
    recent = node[1]
    # Keep track of streak -> tuple[int, int] ??? (x streak, y streak)
    
    new_nodes: list[tuple[int, int]] = []
    for dir, s_d in zip(directions, [1, 1, 0, 0]):
        if s_d:
            s_d = streak[0] + 1
            x_s = streak[0] + 1
            y_s = 0
        else:
            s_d = streak[1] + 1
            x_s = 0
            y_s = streak[1] + 1

        if not dir == recent and node_valid(dir, puzzle_size) and s_d < 3:
            if s_d:
                new_nodes.append((dir, (x,y), (x_s, y_s)))

    return new_nodes

def find_priority_node(queue: list[tuple[int, int]], node_cost_map: dict[tuple[int, int], int]) -> tuple[int, int]:
    val = math.inf
    for node in queue:
        n_c = node[0]
        if node_cost_map[n_c] <= val:
            val = node_cost_map[n_c]
            best_node = node
    return best_node

def gen_grid(puzzle_size: tuple[int, int], val: int) -> dict[tuple[int, int], int]:
    return dict(((k, val) for k in [(x,y) for x in range(puzzle_size[0]+1) for y in range(puzzle_size[1]+1)]))

def cost_function(node: tuple[int, int], goal: tuple[int, int]) -> int:
    x_diff = goal[0] - node[0]
    y_diff = goal[1] - node[1]
    return (x_diff*10) * (y_diff*10)

def path_goal(neighbor_path_map: dict[tuple[int, int]], node: tuple[int, int]) -> int:
    full_path: list[tuple[int, int]] = []
    n_c = node[0]
    while n_c in neighbor_path_map:
        n_c = neighbor_path_map[n_c]
        full_path.insert(0, n_c)
    return full_path

def search_path(puzzle: dict[tuple[int, int], int], puzzle_size: tuple[int, int]) -> int:
    path_cost_map: dict[tuple[int, int], int] = gen_grid(puzzle_size, math.inf) #gscore
    node_cost_map: dict[tuple[int, int], int] = gen_grid(puzzle_size, math.inf) #fscore
    neighbor_path_map: dict[tuple[int, int], tuple[int, int]] = gen_grid(puzzle_size, ())
    start: tuple[int, int] = (0,0)
    streak: list[int] = [0, 0, 0, 0]
    goal: tuple[int, int] = (puzzle_size[0], puzzle_size[1])
    recent = None

    # node[0] = x,y    ::  node[1] == recent node  ::  node[2] == streak (x_streak, y_streak)
    node_start = (start, recent, streak)
    queue: list[tuple[int, int, tuple[int, int], list[int]]] = [node_start]
    
    path_cost_map[start] = 0
    node_cost_map[start] = cost_function(node_start[0], goal)
    #i = 0
    while queue:
        #i += 1
        #print(i)
        node = find_priority_node(queue, node_cost_map)
        
        if node[0] == goal:
            #print(path_cost_map)
            print_map(path_cost_map, puzzle_size, path_goal(neighbor_path_map, node))
            #print(neighbor_path_map[(11,12)])
            return path_goal(neighbor_path_map, node)
        
        ind = queue.index(node)
        queue.pop(ind)

        for neighbor_node in find_new_nodes(puzzle_size, node):
            if node[0] == (2,0):
                print(f"Neighbour nodes: {find_new_nodes(puzzle_size, node)}")
                print(f"new score path cost map: {path_cost_map[node[0]]+puzzle[neighbor_node[0]]}")
                print(f"old score path cost map: {path_cost_map[neighbor_node[0]]}")

            score = path_cost_map[node[0]] + puzzle[neighbor_node[0]]
            #print(f"score: {score},\tnew_node: {neighbor_node}")
            if score < path_cost_map[neighbor_node[0]]:
                neighbor_path_map[neighbor_node[0]] = node[0]
                path_cost_map[neighbor_node[0]] = score
                node_cost_map[neighbor_node[0]] = score + puzzle[neighbor_node[0]] 

                if neighbor_node not in queue:
                    queue.insert(0, neighbor_node)

    raise Exception("Could not find optimal path using A*, queue empty but goal not reached")

def print_map(puzzle, puzzle_size, path = None) -> None:
    for idx_y in range(puzzle_size[1]+1):
        for idx_x in range(puzzle_size[0]+1):
            if puzzle[idx_x, idx_y] == math.inf:
                print("-", end="\t")
            else:
                if (idx_x, idx_y) in path:
                    print(f"\033[91m{puzzle[idx_x, idx_y]:3d}\033[00m", end="    ")
                else:
                    print(f"{puzzle[idx_x, idx_y]:3d}", end="    ")
        print(end="\n")

def calculate_heat_loss(path: list[tuple[int, int]], puzzle):
    part1_sum: int = 0
    for p in path:
        if p:
            part1_sum += puzzle[p]
    return part1_sum

if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0
    # NOTE: If returning to start this node will have a cost
    filename = "input/sample.txt"
    puzzle, puzzle_size = parser(filename)
    path = search_path(puzzle, puzzle_size)
    part1_sum = calculate_heat_loss(path, puzzle)
    


    # 656 answer is too high
    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")