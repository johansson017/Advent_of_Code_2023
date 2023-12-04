#include <iostream>
#include <algorithm>
#include <string>
#include <array>
#include <tuple>
#include <fstream>
#include <map>
#include <cmath>
#include <chrono>
/*std::vector<std::map<std::string, std::vector<int>>> parser(const std::string &filename) {
    std::ifstream file(filename);
    std::string line;
    std::vector<int> winners;
    std::vector<int> draws;
    std::map<std::string, std::vector<int>> number;
    std::vector<std::map<std::string, std::vector<int>>> games;

    std::string delimiter;
    if (file.is_open()) {
        while(std::getline(file, line)) {
            std::string game = line.substr(1, line.find(delimiter));
        }
    }
    else {
        std::cout << "File not open for reading" << std::endl;
    }
    return 0;
}*/
std::pair<int, int> solver(std::map<std::string, std::vector<std::vector<int>>>& input) {
    int sum_part1 = 0;
    int sum_part2 = 0;
    //std::cout << input["DRAWS"].size() << std::endl;
    
    // Initialize vector holding amount to repeat each card win
    std::vector<int> repeats;
    unsigned int games = input["DRAWS"].size();
    for ( unsigned int game = 0; game < games; game++ ) {
        repeats.push_back(1);
    }

    for ( unsigned int game = 0; game < input["DRAWS"].size(); game++ ) {
        // Loop through each game and check if player number in winning numbers
        // Add "wins" as number exist
        int wins = 0;
        sum_part2 += 1;
        for ( unsigned int num = 0; num < input["DRAWS"][game].size(); num++ ) {
            if (std::find(input["WINNERS"][game].begin(), input["WINNERS"][game].end(), input["DRAWS"][game][num]) != input["WINNERS"][game].end()) {
                //std::cout << input["DRAWS"][game][num] << std::endl;
                wins += 1;
            }
        }
        if ( wins >= 1 ) {
            sum_part1 += pow(2,(wins-1));
            unsigned int lower = std::min(games-1, game+1);
            unsigned int higher = std::min(games, game+wins+1);
            for ( unsigned int inc = lower; inc < higher; inc++ ) {
                repeats[inc] += repeats[game];
                sum_part2 += repeats[game];
            }
        }
    }
    return std::make_pair(sum_part1, sum_part2);
}

std::vector<int> parseStringNumbers(const std::string &w) {
    std::vector<int> numVector;
    std::string s;
    //std::cout << "LAST CHAR: " << w.back() << std::endl;
    for (const auto &c: w) {
        if ( c != ' ' && c != '\0' ) {
            s += c;
            //std::cout << s;
        }
        else {
            //std::cout << " " << typeid(s).name() << "\n";
            if ( s != "" ) {
                int n = std::stoi(s);
                //std::cout << n << "\n";
                numVector.push_back(n);
            } 
            s = "";
        }
    }
    return numVector;
}

void printMapVector(std::vector<std::vector<int>>& vector) {
    for ( int i = 0; i < vector.size(); i++ ) {
        std::cout << "\nGame: " << i << " -> ";
        for ( int j = 0; j < vector[i].size(); j++ ) {
            std::cout << vector[i][j] << " ";
        }
    }
    std::cout << "\n";
}

int main() {
    auto start = std::chrono::high_resolution_clock::now();
    int part1_sum = 0;
    int part2_sum = 0;
    std::string filename = "input/input.txt";
    
    std::ifstream file(filename);
    std::string line;
    std::map<std::string, std::vector<std::vector<int>>> numbers;
    std::vector<std::vector<int>> gameWinners;
    std::vector<std::vector<int>> gameDraws;

    std::string delimiter = ":";
    if (file.is_open()) {
        while ( std::getline(file, line) ) {
            std::string game = line.substr(line.find(delimiter)+1);
            //std::cout << game << ":\t";
            std::string w = game.substr(0, game.find("|")) + '\0';
            std::string d = game.substr(game.find("|")+1) + '\0';
            //std::cout << "winners: " << w << "\t\t" << "draws: " << d << "\n";
            auto winners = parseStringNumbers(w);
            auto draws = parseStringNumbers(d);

            //for ( int i = 0; i < winners.size(); i++ ) {
            //    std::cout << winners[i] << std::endl;
            //}
            
            gameWinners.push_back(winners);
            gameDraws.push_back(draws);
            //for ( int i = 0; numbers["WINNERS"].size(); i++ ) {
                //std::cout << numbers["WINNERS"][i] << std::endl;
            //}
        }
    }
    else {
        std::cout << "File not open for reading" << std::endl;
    }
    //for ( int i = 0; i < gameWinners.size(); i++ ) {
        //std::cout << gameWinners[i].size() << std::endl;
        //for ( int j = 0; j < gameWinners.size(); j++ ) {
            //std::cout << gameWinners[i][j] << std::endl;
        //}
    //}
    numbers["WINNERS"] = gameWinners;
    numbers["DRAWS"] = gameDraws;

    //printMapVector(numbers["DRAWS"]);
    auto solution = solver(numbers);
    std::cout << "PART 1 : " << solution.first << std::endl;
    std::cout << "PART 2 : " << solution.second << std::endl;
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop-start);
    std::cout << "EXECUTION TIME : " << duration.count() << "us" << std::endl;
    
    //for ( int i = 0; i < numbers["WINNERS"].size(); i++ ) {
        //for ( int j = 0; j < numbers["WINNERS"][i].size(); j++ ) {
            //std::cout << numbers["WINNERS"][i][j] << std::endl;
        //}
    //}
    //printVector(games);
    return 0;
}