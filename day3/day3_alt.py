#!/usr/bin/python3
if __name__=="__main__":
    import re
    sum1: int = 0
    sum2: int = 0
    input: list[str] = open("input/input.txt").read().splitlines()
    for idx, line in enumerate(input):
        for idx_c, char in enumerate(line):
            if (char != ".") and (not char.isdigit()):
                matches: int = 0
                adj_numbers: list[int] = []
                for y in range(idx-1, idx+2):
                    for numb in re.finditer(r"(\d+)", input[y]):
                        span = range(numb.start(), numb.end())
                        if (idx_c-1 in span) or (idx_c in span) or (idx_c+1 in span):
                            matches += 1
                            adj_numbers.append(int(numb.group(0)))
                if (char == "*") and (len(adj_numbers) == 2):
                    sum2 += adj_numbers[0] * adj_numbers[1]
                    sum1 += sum(adj_numbers)
                else:
                    sum1 += sum(adj_numbers)
    print(f"Part 1 answer: {sum1}\nPart 2 answer: {sum2}")