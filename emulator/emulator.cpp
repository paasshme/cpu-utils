#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <stack>
#include <array>    

enum Opcode {
  NOP,
  ADD,
  SUB,
  XOR,
  LB,
  XNOR,
  AND,
  NAND,
  LDI,
  HALT,
  ADI,
  JMP,
  BRANCH,
  CALL,
  RET,
  ST,
};

class CPUState {
private:
  std::array<char, 512> instructions;
  std::array<char, 8> registers{0};
  std::array<char, 8> callStack;
  int callStackTop;

  bool isCallStackEmpty() const { return callStackTop == -1; }

  bool isCallStackFull() const { return callStackTop == 7; }

public:
  std::array<unsigned char, 256> memory;
  unsigned char programCounter;
  bool carryFlag = false;
  bool zeroFlag = false;

  CPUState() : programCounter(0), callStackTop(-1) {}
  CPUState(std::array<char, 512> instructions)
      : programCounter(0), instructions(instructions), callStackTop(-1) {}

  void writeRegister(char index, char value) {
    if (index > 7 || index < 1)
      return;
    registers[index] = value;
  }

  char readRegister(char index) {
    if (index < 7 && index > 0)
      return registers[index];
    return -1;
  }

  void push(char value) { callStack[(++callStackTop) % 8] = value; }

  char pop() { return callStack[callStackTop--]; }

  void displayState() const {
    std::cout << "--- CPU State ---" << std::endl;
    std::cout << "Program Counter: " << static_cast<int>(programCounter)
              << std::endl;
    std::cout << "Carry Flag: " << (carryFlag ? "1" : "0") << std::endl;
    std::cout << "Zero Flag: " << (zeroFlag ? "1" : "0") << std::endl;

    std::cout << "Registers:" << std::endl;
    for (int i = 0; i < 8; ++i) {
      std::cout << "R" << i << ": " << static_cast<int>(registers[i])
                << std::endl;
    }

    std::cout << "Call Stack (Top: " << callStackTop << "):" << std::endl;
    std::cout << "[";
    for (int i = 0; i < 8; ++i) {
      if (i <= callStackTop) {
        std::cout << static_cast<int>(callStack[i]);
      } else {
        std::cout << " ";
      }
      if (i < 7)
        std::cout << ", ";
    }
    std::cout << "]" << std::endl;

    std::cout << "Memory (First 16):" << std::endl;
    std::cout << "[";
    for (int i = 0; i < 16; ++i) {
      std::cout << static_cast<int>(memory[i]);
      if (i < 15)
        std::cout << ", ";
    }
    std::cout << "]" << std::endl;

    std::cout << "Instructions (First 16):" << std::endl;
    std::cout << "[";
    for (int i = 0; i < 16; ++i) {
      std::cout << static_cast<int>(instructions[i]);
      if (i < 15)
        std::cout << ", ";
    }
    std::cout << "]" << std::endl;
  }
};

void execute(unsigned short instruction, CPUState &cpu) {
  unsigned opcode = static_cast<Opcode>(instruction >> 12);
  unsigned operand_1 = (instruction >> 8) & 0xF;
  unsigned operand_2 = (instruction >> 4) & 0xF;
  unsigned operand_3 = instruction & 0xF;
  unsigned immediate = instruction & 0xFF;
  unsigned branch_flags = (instruction >> 8) & 0x3;

  char res;
  bool jump;
  std::cout << opcode << "op " << operand_1 << ":" << operand_2 << ": "
            << operand_3 << ": " << immediate << std::endl;
  switch (opcode) {
  case NOP:
    // No operation
    cpu.programCounter++;
    break;
  case ADD:
    res = cpu.readRegister(operand_1) + cpu.readRegister(operand_2);
    cpu.writeRegister(operand_3, res);
    // TODO: set carry flag!
    if (res == 0)
      cpu.zeroFlag = true;

    cpu.programCounter++;
    break;
  case SUB:
    res = cpu.readRegister(operand_1) - cpu.readRegister(operand_2);
    cpu.writeRegister(operand_3, res);
    if (res == 0)
      cpu.zeroFlag = true;

    cpu.programCounter++;
    break;
  case XOR:
    res = cpu.readRegister(operand_1) ^ cpu.readRegister(operand_2);
    cpu.writeRegister(operand_3, res);

    cpu.programCounter++;
    break;
  case LB:
    cpu.writeRegister(operand_3, cpu.memory[operand_1 + operand_3]);
    cpu.programCounter++;
    break;
  case XNOR:
    res = !(cpu.readRegister(operand_1) ^ cpu.readRegister(operand_2));
    cpu.writeRegister(operand_3, res);
    cpu.programCounter++;
    break;
  case AND:
    res = cpu.readRegister(operand_1) & cpu.readRegister(operand_2);
    cpu.writeRegister(operand_3, res);
    cpu.programCounter++;
    break;
  case NAND:
    res = !(cpu.readRegister(operand_1) & cpu.readRegister(operand_2));
    cpu.writeRegister(operand_3, res);
    cpu.programCounter++;
    break;
  case LDI:
    cpu.writeRegister(operand_1, immediate);
    cpu.programCounter++;
    break;
  case HALT:
    std::cout << "HALT instruction executed. Program terminated." << std::endl;
    cpu.programCounter = -1; // Indicate program termination
    break;
  case ADI:
    res = cpu.readRegister(operand_1);
    res += immediate;
    cpu.writeRegister(operand_1, res);
    if (res == 0)
      cpu.zeroFlag = true;

    cpu.programCounter++;
    break;
  case JMP:
    cpu.programCounter = immediate;
    break;
  case BRANCH:

    jump = (branch_flags == 0 && !cpu.carryFlag) ||
           (branch_flags == 1 && cpu.zeroFlag) ||
           (branch_flags == 2 && cpu.carryFlag) ||
           (branch_flags == 3 && !cpu.zeroFlag);

    if (jump) {
      cpu.programCounter = immediate;
    } else {
      cpu.programCounter++;
    }

    break;
  case CALL:
    cpu.push(cpu.programCounter + 1);
    cpu.programCounter = immediate;
    break;
  case RET:
    cpu.programCounter = cpu.pop(); // return address from register 15
    break;
  case ST:
    res = cpu.readRegister(operand_3);
    cpu.memory[operand_1 + operand_3] = res;
    cpu.programCounter++;
    break;
  default:
    std::cerr << "Error: Unknown opcode!" << std::endl;
    cpu.programCounter = -1; // Indicate error
    break;
  }
}

int main(int argc, char *argv[]) {
  CPUState state;

  execute(0b0111000100100011, state);
  execute(0b1000000100001111, state);
  execute(0b1000001000001111, state);
  execute(0b0001000100100111, state);
  execute(0b1011000010010111, state);

  state.displayState();
}