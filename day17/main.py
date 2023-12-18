#!/c/ProgramData/Anaconda3/python
from collections import defaultdict, Counter
import math, typing
import heapq
from colorama import just_fix_windows_console
just_fix_windows_console()

Puzzletype = dict[tuple[int, int], int] 


# Directions for counting streak -> curr - new = dir
DIRECTIONS = {(1,0): "left", (-1,0): "right", (0,1): "up", (0,-1): "down"}
PRINTDIR = {"left": "<", "right": ">", "up": "^", "down": "v"}


class Node:
    def __init__(self, coords, dir, streak, value=math.inf, prev=((None, None)), c_node=None):
        self.coords = coords
        self.dir: str = dir 
        self.streak = streak
        self.value = value
        self.prev: tuple[int, int] = prev
        self.chain: object = c_node

    def __lt__(self, other):
        return self.value < other.value
    
    def __iter__(self):
        yield self.coords
        yield self.dir
        yield self.streak
    
    def __repr__(self):
        return PRINTDIR[self.dir] 

def parser(filename: str):
    puzzle: Puzzletype = {}
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


def find_new_nodes(puzzle_size: tuple[int, int],
                   node: tuple[tuple[int, int], tuple[int, int], list[int]],
                   limitations: tuple[int, int]) -> list[tuple[int , int]]:
    new_nodes = []
    x, y = node.coords
    streak = node.streak
    new_coords = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    s_min, s_max = limitations

    for n_c in new_coords:
        x_dir = x - n_c[0]
        y_dir = y - n_c[1]
        if DIRECTIONS[(x_dir, y_dir)] == node.dir:
            consecutive = True
            new_streak = streak + 1
        else:
            consecutive = False
            new_streak = 1
        
        if n_c == node.prev[0] or not node_valid(n_c, puzzle_size) or new_streak > s_max or (not consecutive and streak < s_min):
            continue

        new_nodes.append(Node(n_c, DIRECTIONS[(x_dir, y_dir)], new_streak))

    return new_nodes

def search_path(puzzle: Puzzletype, puzzle_size: tuple[int, int], part2: bool) -> int:
    path_cost_map = defaultdict(lambda: math.inf)
    goal: tuple[int, int] = (puzzle_size[0], puzzle_size[1])
    limitations = (0,3)
    s1 = Node((0, 0), DIRECTIONS[(-1,0)], 1, value=0)
    s2 = Node((0, 0), DIRECTIONS[(0,-1)], 1, value=0)
    path_cost_map[(s1.coords, s1.dir, s1.streak)] = 0
    path_cost_map[(s2.coords, s2.dir, s2.streak)] = 0
    queue = [s1, s2]

    heapq.heapify(queue)
    capture_nodes = []
    seen = dict() 
    while queue:
        node = heapq.heappop(queue)
        
        if tuple(node) in seen:
            continue
            
        if not part2:
            if node.coords == goal:
                final_value = node.value
                path = []
                path.insert(0, node)
                while node.chain:
                    path.insert(0, node.chain)
                    node = node.chain
                return final_value, path
        else:
            limitations = (4,10)

        for neighbor_node in find_new_nodes(puzzle_size, node, limitations):
            score = node.value + puzzle[neighbor_node.coords]

            if score < path_cost_map[tuple(neighbor_node)]:
                neighbor_node.value = score
                neighbor_node.prev = tuple(node)
                neighbor_node.chain = node
                path_cost_map[tuple(neighbor_node)] = score

                seen[tuple(node)] = node.value 

                heapq.heappush(queue, neighbor_node)

    # Running without early termination for part2 as to be able to check streak on states
    # Did not manage to find how to do otherwise
    results = []
    for key, val in seen.items():
        (x,y), _, streak = key
        if (x,y) == goal and streak >= 4:
            results.append(val)

    return min(results)

def print_map(puzzle, puzzle_size, path: list[object]) -> None:
    list_obj = []
    for obj in path:
        list_obj.append(obj.coords)

    for idx_y in range(puzzle_size[1]+1):
        for idx_x in range(puzzle_size[0]+1):
            if puzzle[idx_x, idx_y] == math.inf:
                print("-", end="\t")
            else:
                if (idx_x, idx_y) in list_obj:
                    idx_obj = list_obj.index((idx_x, idx_y))
                    print(f"\033[91m{str(path[idx_obj])}\033[00m", end="")
                else:
                    print(f"{puzzle[idx_x, idx_y]}", end="")
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
    
    filename = "input/sample.txt"
    puzzle, puzzle_size = parser(filename)
    part1_sum, map_path = search_path(puzzle, puzzle_size, part2=False)
    print_map(puzzle, puzzle_size, map_path)
    #part2_sum = search_path(puzzle, puzzle_size, part2=True)
    
    print(f"Answer for Part 1: {part1_sum}\nAnswer for Part 2: {part2_sum}")