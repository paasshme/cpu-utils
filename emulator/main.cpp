#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "emulator.h"

int main() {
    const std::size_t MAX_LINES = 512;
    const std::string& asm_file_path = "../build/output.bin";
    std::ifstream input(asm_file_path);
    std::array<unsigned short, MAX_LINES> instructions;

    if (!input) {
        std::cerr << "Error opening file " << asm_file_path << std::endl;
        return 1; // Exit the program if the file cannot be opened
    }
    
    std::string line;
    std::size_t currentCount = 0;
    while (currentCount < MAX_LINES && std::getline(input, line)) { // Read the file line by line
        unsigned short s = std::stoi(line, nullptr, 2);
        instructions[currentCount] = s;
        currentCount++;
    }

    for (std::size_t i = 0; i < currentCount; ++i) {
        std::cout << "Line " << i + 1 << ": " << std::hex << instructions[i] << std::dec <<  std::endl;
    }

    input.close(); // Close the file
    CPUState cpu(instructions);
    while(cpu.execute() != HALT);

    cpu.displayState();
    return 0;
}