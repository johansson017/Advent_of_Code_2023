#!/usr/bin/python3
from dataclasses import dataclass
from collections import defaultdict, Counter
"""
A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
"""

@dataclass
class Hand:
    content: list[int] 
    number: int
    hand_type: int

    def __lt__(self, other):
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        else:
            return self.content < other.content

hand_type_dict: dict = {"5": 6, "4": 5, "3,2": 4, "3": 3, "2,2":2, "2": 1, "1": 0}

def parser(filename):
    values = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    pairs: dict() = defaultdict()

    for idx, val in enumerate(reversed(values)):
        pairs[val] = idx+1

    data: list[list[tuple[int, int]]] = []

    with open(filename) as file:
        for line in file:
            hand, number = line.strip().split()
            extra = hand.count("J")

            hand_content = []
            for idx, val in enumerate(hand):
                hand_content.append(pairs[val])
            
            hand_replace_j = hand.replace("J","")

            number_hand = []
            for idx, val in enumerate(hand_replace_j):
                number_hand.append(pairs[val])

            ordered_hand = sorted(Counter(number_hand).items(), key=dict_sort, reverse=True)

            if len(ordered_hand) == 1 or len(ordered_hand) == 0:
                hand_type = hand_type_dict["5"]
            elif ordered_hand[1][1] != 1:
                if ordered_hand[0][1]+extra >= 4:
                    hand_type = hand_type_dict[f"{ordered_hand[0][1]+extra}"]
                else:
                    hand_type = hand_type_dict[f"{ordered_hand[0][1]+extra},{ordered_hand[1][1]}"]
            else:
                hand_type = hand_type_dict[f"{ordered_hand[0][1]+extra}"]
            
            
            data.append(Hand(hand_content, int(number), hand_type))
    
    data = sorted(data)
    return data

def dict_sort(elem):

    return elem[1], elem[0]

def solver(data):
    part1_sum: int = 0
    for idx, hand in enumerate(data):
        part1_sum += (idx+1)*hand.number
    return part1_sum


if __name__=="__main__":
    part1_sum: int = 0
    part2_sum: int = 0

    filename = "input/input.txt"
    data = parser(filename)
    part1_sum = solver(data)


    print(f"Answer for Part1: {part1_sum}\nAnswer for Part2: {part2_sum}")