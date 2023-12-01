#!/usr/bin/python3
"""
Part 1:
1. Loop through line to find first digit
2. Loop through reverse line to find "last" digit

Part 2 (additional):
1. Check if any sequential character match start of number-word
2. If new appending causes missmatch -> remove oldest char and try again to match all to not miss cases
- Example is "five" and "seven" backwards -> "nev" exit would cause "ev"/"evi" to be missed.
"""

def find_word_number(word: str, numbers: dict[str, int]) -> str:
    match: bool = False

    for num in numbers:
        if num.startswith(word):
            match = True
            return word
    
    if match == False:
        word = word[1:]
        return find_word_number(word, numbers)

def find_first_number(line: str, numbers: dict[str, int] = None) -> str:
    word: str = ""

    for char in line:
        word += char
        if char.isdigit():
            return char
        elif numbers != None:
            if word in numbers:
                return str(numbers[word])
            else:
                # Check if any numbers start with "word" letters, 
                # else find longest "end-sequence" in word which a number-word starts with
                word = find_word_number(word, numbers)
    return "0"

def part1(filename: str) -> int:
    sum_part1: int = 0
    with open(filename, "r") as file:
        for line in file:
            sum_string: str = ""
            sum_string += find_first_number(line)
            sum_string += find_first_number(reversed(line))
            sum_part1 += int(sum_string)
        
    return sum_part1

def part2(filename: str) -> int:
    numbers: dict[str, int] = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
    numbers_reversed: dict[str, int] = dict((x[::-1],y) for x,y in numbers.items())

    sum_part2: int = 0
    with open(filename, "r") as file:
        for line in file:
            sum_string: str = ""
            sum_string += find_first_number(line, numbers)
            sum_string += find_first_number(reversed(line), numbers_reversed)
            sum_part2 += int(sum_string)

    return sum_part2

if __name__=="__main__":
    filename = "input/input.txt"
    part1_sum = part1(filename)
    part2_sum = part2(filename)

    print(f"Part 1 answer: {part1_sum}")
    print(f"Part 2 answer: {part2_sum}")


