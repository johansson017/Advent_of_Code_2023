#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <array>

/*
1. function to get line and loop through chars to find first and last digit.


*/
std::array<std::string, 9> numbers = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};


std::string findDigits(const std::string &line) {
    std::string foundDigits;
    for ( auto &c: line ) {
        if (std::isdigit(c)) {
            foundDigits += c;
            //std::cout << foundDigits << "\n";
        }
    }
    return foundDigits;
}

int combineNumbers(const std::string &foundDigits) {
    int value;
    std::string combined_string_number;
    
    combined_string_number += foundDigits.front();
    combined_string_number += foundDigits.back();
    value = std::stoi(combined_string_number);

    return value;
}

void solver (const std::string &filename, int &part1_sum, int &part2_sum) {
    std::ifstream file(filename);
    std::string line;

    if (file.is_open()) {
        while (std::getline(file, line)) {
            std::string foundDigits = findDigits(line);
            part1_sum += combineNumbers(foundDigits);
        }
    }
    else {
        std::cerr << "File is not open for reading" << "\n";
    }
}


int main () {
    int part1_sum{0};
    int part2_sum{0};

    std::string filename = "input/sample1.txt";
    solver(filename, part1_sum, part2_sum);

    std::cout << "Part 1 answer: " << part1_sum << "\n";
    std::cout << "Part 2 answer: " << part2_sum << "\n";


    return 0;
}