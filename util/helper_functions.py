
def string_replace(string: str, index: int, replacement):
    return string[:index] + replacement + string[(index+1):]