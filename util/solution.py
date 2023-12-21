class Solution:
    def __init__(self, parser: callable, solver: callable, input: str = None):
        self.parser = parser
        self.solver = solver
        if input:
            self.input = self._handle_input(input)
            self.parsed_input = parser(self.input[0])

        self._test_solve_result = None
        self._result_p1 = None
        self._result_p2 = None

        self.parsed_test_data = []
        self._test_output = None

        # Extra result variable
        self._extra_test = None
        self._extra_part1 = None
        self._extra_part2 = None

    def _handle_input(self, input: list[str] | str | list[int] | int):
        formatted = []
        if len(input) == 1:
            formatted.append(input[0])
        elif type(input) == str or type(input) == int:
            formatted.append(input)
        else:
            for value in input:
                formatted.append(value)
        return formatted

    def test_input(self, input: list[str] | str, output: list[int] | int):
        input = self._handle_input(input)
        self._test_output = self._handle_input(output)

        for file in input:
            self.parsed_test_data.append(self.parser(file))

    def solve(self, test: bool = False, part1: bool = False, part2: bool = False, timer=False, extras=None):
        if self.parsed_test_data and test:
            self._test_solve_result = []
            for test_data_input in self.parsed_test_data:
                output, self._extra_test = self.solver(test_data_input, extras=extras)
                self._test_solve_result.append(output)
        if part1:
            self._result_p1, self._extra_part1 = self.solver(self.parsed_input)
        if part2:
            self._result_p2, self._extra_part2 = self.solver(self.parsed_input, part2=True)
    
    def display_result(self, windows=False):
        if windows:
            self._init_windows_config()

        if self._test_solve_result:
            print("\nHere are the results for the test data:")
            for idx, test_result, test_output in zip(range(len(self._test_solve_result)), self._test_solve_result, self._test_output):
                color, sign = self._get_sign(test_result, test_output)
                print(f"TEST NUMBER {idx+1}: {color}{test_result}\033[00m {sign} {test_output}")
        if self._result_p1:
            print(f"\nResult for PART 1: {self._result_p1}")
        else:
            print(f"\nERROR: No solution for part 1 given")
        if self._result_p2:
            print(f"Result for PART 2: {self._result_p2}")
        else:
            print(f"ERROR: No solution for part 2 given")

    def print_grid(self, symbol=None, test=False, input=False):
        if test:
            print_data, start= self.parsed_test_data[0]
            visited = self._extra_test
        if input:
            print_data, start = self.parsed_input[0]
            visited = self._extra_part1

        sizes = max(print_data)


        for y in range(sizes[1]+1):
            for x in range(sizes[0]+1): 
                if (x,y) in visited:
                    print(f"\033[91m{str(print_data[x,y]) if not symbol else symbol}\033[00m", end="")
                else:
                    print(f"{str(print_data[x,y])}", end="")
            print(end="\n")


    def _get_sign(self, result, expected):
        if result == expected:
            sign = "=="
            color = "\033[92m"
        else:
            sign = "!="
            color = "\33[91m"
        return color, sign
    
    def _init_windows_config(self):
        from colorama import just_fix_windows_console
        just_fix_windows_console()