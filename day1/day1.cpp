#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <array>

/*
1. function to get line and loop through chars to find first and last digit.


*/
std::array<std::string, 9> numbers = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};


std::string findDigits(std::string line) {
    std::string foundDigits;
    for ( auto &c: line ) {
        if (std::isdigit(c)) {
            foundDigits += c;
            //std::cout << foundDigits << "\n";
        }
    }
    return foundDigits;
}

int combineNumbers(std::string foundDigits) {
    int value;
    std::string combined_string_number;

    combined_string_number += foundDigits.front();
    combined_string_number += foundDigits.back();
    value = std::stoi(combined_string_number);

    return value;
}

int part1 (std::string filename, int &part1_sum) {
    std::ifstream file(filename);
    std::string line;


    std::string foundDigits;
    if (file.is_open()) {
        while (std::getline(file, line)) {
            foundDigits = findDigits(line);
            part1_sum += combineNumbers(foundDigits);
        }
    }
    else {
        std::cerr << "File is not open for reading" << "\n";
    }

    return part1_sum;
}


int main () {

    int part1_sum{0};
    int part2_sum{0};

    std::string filename = "input/sample1.txt";
    part1_sum = part1(filename, part1_sum);

    std::cout << "Part 1 answer: " << part1_sum << "\n";
    std::cout << "Part 2 answer: " << part2_sum << "\n";


    return 0;
}