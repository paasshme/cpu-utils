#include "emulator.h"

// Implementation of CPUState methods
#define EMU_DATA_DEBUG
#ifdef EMU_DATA_DEBUG

void logRegisterChange(unsigned int regIndex, unsigned int prevValue,
                       unsigned int newValue) {
  std::cout << "Register #" << regIndex << " [" << prevValue << "] -> ["
            << newValue << "]" << std::endl;
}

void logMemoryChange(unsigned int address, unsigned int prevValue,
                     unsigned int newValue) {
  std::cout << "RAM #" << address << " [" << prevValue << "] -> [" << newValue
            << "]" << std::endl;
}

#endif

CPUState::CPUState(std::array<unsigned short, 512> instructions)
    : programCounter(0), instructions(instructions), callStackTop(-1) {}

bool CPUState::isCallStackEmpty() const { return callStackTop == -1; }

bool CPUState::isCallStackFull() const { return callStackTop == 7; }

void CPUState::writeRegister(unsigned char index, unsigned char value) {
  if (index > 7 || index < 1)
    return;
#ifdef EMU_DATA_DEBUG
  logRegisterChange(index, registers[index], value);
#endif
  registers[index] = value;
}

unsigned char CPUState::readRegister(unsigned char index) {
  if (index < 7 && index > 0)
    return registers[index];
  return 0;
}

unsigned char CPUState::readMemory(unsigned char index, unsigned char offset) {
  if (index + offset < 256 && index + offset >= 0)
    return memory[index + offset];
  return 0;
}

void CPUState::writeMemory(unsigned char address, unsigned char offset,
                           unsigned char value) {
  if (address + offset < 256 && address + offset >= 0) {
#ifdef EMU_DATA_DEBUG
    logMemoryChange(address + offset, memory[address + offset], value);
#endif
    memory[address + offset] = value;
  }
}

void CPUState::push(unsigned char value) {
  callStack[(++callStackTop) % 8] = value;
}

char CPUState::pop() { return callStack[callStackTop--]; }

void CPUState::displayState() const {
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
// Implementation of the execute function
Opcode CPUState::execute() {
  unsigned short instruction = instructions[programCounter];

  Opcode opcode = static_cast<Opcode>(instruction >> 12);
  std::cout << "Executing " << instruction << " at PC " << (int)programCounter
            << std::endl;
  std::cout << "opcode=" << opcode << std::endl;
  unsigned operand_1 = (instruction >> 8) & 0xF;
  unsigned operand_2 = (instruction >> 4) & 0xF;
  unsigned operand_3 = instruction & 0xF;
  unsigned immediate = instruction & 0xFF;
  unsigned branch_flags = (instruction >> 10) & 0x3;

  char res;
  bool jump;
  // std::cout << opcode << "op " << operand_1 << ":" << operand_2 << ": "
  // << operand_3 << ": " << immediate << std::endl;
  switch (opcode) {
  case NOP:
    programCounter++;
    break;
  case ADD:
    res = readRegister(operand_1) + readRegister(operand_2);
    writeRegister(operand_3, res);
    if (res == 0)
      zeroFlag = true;
    carryFlag = readRegister(operand_1) > 255 - readRegister(operand_2);

    programCounter++;
    break;
  case SUB:
    res = readRegister(operand_1) - readRegister(operand_2);
    writeRegister(operand_3, res);
    if (res == 0)
      zeroFlag = true;
      carryFlag = readRegister(operand_2) > readRegister(operand_1);

    programCounter++;
    break;
  case XOR:
    res = readRegister(operand_1) ^ readRegister(operand_2);
    writeRegister(operand_3, res);
    programCounter++;
    break;
  case LB:
    writeRegister(operand_3, readMemory(operand_1, operand_3));
    programCounter++;
    break;
  case XNOR:
    res = !(readRegister(operand_1) ^ readRegister(operand_2));
    writeRegister(operand_3, res);
    programCounter++;
    break;
  case AND:
    res = readRegister(operand_1) & readRegister(operand_2);
    writeRegister(operand_3, res);
    programCounter++;
    break;
  case NAND:
    res = !(readRegister(operand_1) & readRegister(operand_2));
    writeRegister(operand_3, res);
    programCounter++;
    break;
  case LDI:
    writeRegister(operand_1, immediate);
    programCounter++;
    break;
  case HALT:
    std::cout << "HALT instruction executed. Program terminated." << std::endl;
    break;
  case ADI:
    res = readRegister(operand_1);
    res += immediate;
    writeRegister(operand_1, res);
    if (res == 0)
      zeroFlag = true;
    programCounter++;
    break;
  case JMP:
    programCounter = immediate;
    break;
  case BRANCH:
    std::cout << "Branch flag=" << branch_flags << std::endl;
    jump = (branch_flags == 0 && !carryFlag) ||
           (branch_flags == 1 && zeroFlag) ||
           (branch_flags == 2 && carryFlag) || (branch_flags == 3 && !zeroFlag);
    if (jump) {
      programCounter = immediate;
    } else {
      programCounter++;
    }
    break;
  case CALL:
    push(programCounter + 1);
    programCounter = immediate;
    break;
  case RET:
    programCounter = pop();
    break;
  case ST:
    res = readRegister(operand_2);
    writeMemory(operand_1, operand_3, res);
    programCounter++;
    break;
  default:
    std::cerr << "Error: Unknown opcode!" << std::endl;
    return HALT;
    break;
  }

  return opcode;
}

// Main function to test the CPUState and execute functions
#ifdef TEST
int main(int argc, char *argv[]) {
  CPUState state;

  execute(0b0111000100100011, state);
  execute(0b1000000100001111, state);
  execute(0b1000001000001111, state);
  execute(0b0001000100100111, state);
  execute(0b1011000010010111, state);

  state.displayState();

  return 0;
}
#endif