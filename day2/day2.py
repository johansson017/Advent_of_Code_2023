#!/usr/bin/python3

"""
Bag contains: 12 red, 13 green, 14 blue

Which games are possible? -> One display of cubes must exceed one limit

Store information:
1. Save game number
2. Save highest value for each color
3. ?

Check sum:
1. If game allowed -> return game ID (connect to line parse?) (idx + 1)
"""
MAX_CUBES: dict[str, int] = {"red": 12, "green": 13, "blue": 14}

# Parse line to get most amount of red/green/blue cubes shown at once
# and return as a dict in format {color: amount}
def parse_games(line) -> dict[str, int]:
    cube_dict: dict[str, int] = {"red": 0, "green": 0, "blue": 0}

    cube_displays: list[str] = line.split(":")[1].strip().split(";")
    for display in cube_displays:
        display = display.split(",")
        for cubes in display:
            cubes = cubes.strip()
            amount, color = cubes.split(" ")
            if int(amount) > cube_dict[color]:
                cube_dict[color] = int(amount)
    
    return cube_dict

def is_game_valid(cube_dict: dict[str, int]) -> bool:
    for key, val in cube_dict.items():
        if val > MAX_CUBES[key]:
            return False
    return True

def solver(filename) -> (int, int):
    part1_sum: int = 0
    part2_sum: int = 0
    with open(filename, "r") as file:
        for idx, line in enumerate(file):
            cube_dict = parse_games(line)
            if is_game_valid(cube_dict):
                part1_sum += (idx + 1)
            part2_sum += power_of_cubes(cube_dict)

    return part1_sum, part2_sum

def power_of_cubes(cube_dict: dict[str, int]) -> int:
    game_sum: int = 1
    for value in cube_dict.values():
        game_sum *= value
    return game_sum

if __name__=="__main__":

    filename = "input/input.txt"
    part1_answer, part2_answer = solver(filename)

    print(f"Answer for part 1: {part1_answer}")
    print(f"Answer for part 2: {part2_answer}")