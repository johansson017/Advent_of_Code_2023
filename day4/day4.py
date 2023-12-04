#!/usr/bin/python3

def calculate_games(data: tuple[list[int], list[int]]) -> tuple[int, int]:
    win, player = data
    scratch_cards: int = 0
    games: int = len(win)
    card_points: int = 0
    repeats: list[int] = [1 for x in range(games)]
    
    for idx, (w, p) in enumerate(zip(win, player)):
        scratch_cards += 1
        w_num: int = 0
        for val in p:
            if val in w:
                w_num += 1
        if w_num >= 1:
            card_points += 2**(w_num-1)
            for inc in range(min(games-1, idx+1), min(games, idx+w_num+1)):
                repeats[inc] += 1*repeats[idx]
                scratch_cards += 1*repeats[idx]

    return card_points, scratch_cards

def parser(filename) -> (list[int], list[int]):
    win_numbers: list[int] = []
    player_numbers: list[int] = []
    with open(filename, "r") as file:
        for line in file:
            win, player = line.strip().split(":")[1].split("|")
            win_numbers.append([int(x) for x in win.strip().split(" ") if x != ""])
            player_numbers.append([int(x) for x in player.strip().split(" ") if x != ""])
    return win_numbers, player_numbers


if __name__=="__main__":
    part1: int = 0
    part2: int = 0

    filename = "input/input.txt"
    data = parser(filename)
    part1, part2 = calculate_games(data)
    
    print(f"Answer for Part 1: {part1}\nAnswer for Part 2: {part2}")