class Solution:
    def __init__(self, parser: callable, solver: callable, input: str):
        self.parser = parser
        self.solver = solver
        self.input = self._handle_input(input)
        self.parsed_input = parser(self.input)

        self._test_solve_result = None
        self._result_p1 = None
        self._result_p2 = None

        self.parsed_test_data = []
        self._test_output = None

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

    def solve(self, test: bool = False, part1: bool = False, part2: bool = False):
        if self.parsed_test_data and test:
            self._test_solve_result = []
            for test_data_input in self.parsed_test_data:
                self._test_solve_result.append(self.solver(test_data_input))
        if part1:
            self._result_p1 = self.solver(self.parsed_input)
        if part2:
            self._result_p2 = self.solver(self.parsed_input, part2=True)
    
    def display_result(self):
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

    def _get_sign(self, result, expected):
        if result == expected:
            sign = "=="
            color = "\033[92m"
        else:
            sign = "!="
            color = "\33[91m"
        return color, sign