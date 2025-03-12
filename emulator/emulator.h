#pragma once

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
  std::array<unsigned char, 512> instructions;
  std::array<unsigned char, 8> registers{0};
  std::array<unsigned char, 8> callStack;
  std::array<unsigned char, 256> memory;
  int callStackTop;

  bool isCallStackEmpty() const;
  bool isCallStackFull() const;

public:
  unsigned char programCounter;
  bool carryFlag;
  bool zeroFlag;

  CPUState();
  CPUState(std::array<unsigned char, 512> instructions);

  void writeRegister(unsigned char index, unsigned char value);
  unsigned char readRegister(unsigned char index);

  void writeMemory(unsigned char address, unsigned char offset, unsigned char value);
  unsigned char readMemory(unsigned char index, unsigned char offset);
  void push(unsigned char value);
  char pop();
  void displayState() const;
};

void execute(unsigned short instruction, CPUState &cpu);
