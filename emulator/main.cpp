#include <iostream>
#include <fstream>
#include <string>
#include "emulator.h"

int main() {
    const std::string& asm_file_path = "../build/output.bin";
    CPUState cpu;
    std::ifstream input(asm_file_path);

    if (!input) {
        std::cerr << "Error opening file " << asm_file_path << std::endl;
        return 1; // Exit the program if the file cannot be opened
    }
    
    std::string line;
    while (std::getline(input, line)) { // Read the file line by line
        unsigned short s = std::stoi(line, nullptr, 2);
        execute(s,cpu);
    }
    input.close(); // Close the file
    cpu.displayState();
    return 0;
}