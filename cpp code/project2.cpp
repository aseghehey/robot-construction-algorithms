// Jaedon Jensen, Jimmy Rodriguez, and Emanuel Aseghehey

#include <fstream>
#include <string>
#include <utility>
#include <stdexcept>
#include <vector>
#include <sstream>

auto readInput(const std::string& filename) {
    std::ifstream input_file;
    input_file.open(filename);
    if (!input_file.is_open()) {
        throw std::runtime_error("Unable to open " + filename);
    }
    std::vector<std::vector<std::string>> robot_list;
    std::string line;
    // skip first 2 lines
    getline(input_file, line); // number of robots line
    getline(input_file, line); // blank line
    std::vector<std::string> tmp;
    while(getline(input_file, line)){
        line.erase(line.find_last_not_of(" \t\f\v\n\r") + 1); // remove trailing whitespace
        if(line.empty()) {
            robot_list.push_back(tmp);
            tmp.clear();
            continue;
        }
        tmp.push_back(line);
    }
    robot_list.push_back(tmp);
    return robot_list;
}

auto readOmnidroid(const std::vector<std::string>& lines) {
    std::vector<std::vector<unsigned int>> clean_input;
    for(const std::string& line : lines) {
        if(line == "omnidroid") { // skip line since we already know this is an omnidroid
            continue;
        }
        std::vector<unsigned int> tmp;
        std::string num;
        std::istringstream line_stream(line);
        while(getline(line_stream, num, ' ')) { // splitting the line by ' '
            tmp.push_back(std::stoi(num));
        }
        clean_input.push_back(tmp);
    }
    unsigned int n = clean_input[0][0];
    unsigned int m = clean_input[0][1];
    std::vector<unsigned int> tmp;
    std::vector<std::vector<unsigned int>> dep(n, tmp); // initialize adjacency list
    for(unsigned int i = 1; i <= m; i++) {
        unsigned int need = clean_input[i][0];
        unsigned int needfor = clean_input[i][1];
        dep[needfor].push_back(need);
    }
    std::vector<unsigned int> sprockets;
    for(unsigned int i = m+1; i < clean_input.size(); i++) {
        sprockets.push_back(clean_input[i][0]);
    }
    std::pair<std::vector<std::vector<unsigned int>>, std::vector<unsigned int>> dep_sprockets(dep, sprockets);
    return dep_sprockets;
}

auto readRobotomaton(const std::vector<std::string>& lines) {
    std::vector<unsigned int> sprocket;
    std::vector<unsigned int> previous;
    for(auto it = lines.begin() + 2; it != lines.end(); it++) {
        std::string line = *it;
        std::string num;
        std::istringstream line_stream(line);
        getline(line_stream, num, ' '); // splitting the line by ' '
        sprocket.push_back(std::stoi(num));
        getline(line_stream, num, ' '); // splitting the line by ' '
        previous.push_back(std::stoi(num));
    }
    std::pair<std::vector<unsigned int>, std::vector<unsigned int>> sprocket_previous(sprocket, previous);
    return sprocket_previous;
}

long int omnidroid(unsigned int num, std::vector<long int>& cache, const std::vector<std::vector<unsigned int>>& use, const std::vector<unsigned int>& sprockets) {
    // memoization check
    if(cache[num] != -1) {
        return cache[num];
    }
    // base case
    if(use[num].empty()) {
        return (long int) sprockets[num];
    }
    // loop through edges (part dependencies) and add their sprocket count
    long int added_use = 0;
    for(unsigned int t : use[num]) {
        added_use += omnidroid(t, cache, use, sprockets);
    }
    cache[num] = (long int) sprockets[num] + added_use;
    return cache[num];
}

auto robotomaton(const std::vector<unsigned int>& sprocket, const std::vector<unsigned int>& previous) {
    // iterative robotomaton algorithm
    unsigned long int total = sprocket[0];
    // cache[i] stores the sum of all the sprockets required to build stages 0..i
    std::vector<unsigned long int> cache(sprocket.size(), 0);
    cache[0] = sprocket[0];
    for(unsigned int i = 1; i < sprocket.size(); i++) {
        total = sprocket[i];
        // add all sprockets from previous stages
        if(previous[i] == i) {
            total += cache[i - 1];
        }
        // add all sprockets from previous stages then subtract the sum of sprockets from stages not needed
        else {
            total += cache[i - 1] - cache[i - previous[i] - 1];
        }
        cache[i] = cache[i - 1] + total;
    }
    return total;
}


int main() {
    auto robot_list = readInput("input.txt");
    std::ofstream output("output.txt");
    for(const auto& robot : robot_list) {
        if(robot[0] == "omnidroid") {
            auto dep_sprockets = readOmnidroid(robot);
            auto dep = dep_sprockets.first;
            auto sprockets = dep_sprockets.second;
            std::vector<long int> cache(sprockets.size(), -1); // map for memoization with sentinel value -1
            output << omnidroid(sprockets.size() - 1, cache, dep, sprockets) << std::endl;
        }
        else if(robot[0] == "robotomaton") {
            auto sprocket_previous = readRobotomaton(robot);
            auto sprocket = sprocket_previous.first;
            auto previous = sprocket_previous.second;
            output << robotomaton(sprocket, previous) << std::endl;
        }
    }
    output.close();
    return 0;
}