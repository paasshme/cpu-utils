from assembler import assemble, preassemble
from schematic import create_rom


if __name__ == '__main__':
    assemble("main.as", "output.bin")
    debug_symbols = None
    preassemble("main.as", "output.asx")
    with open("output.asx", "r") as r:
        debug_symbols = r.readlines()
    with open("output.bin") as f:
        lines = f.readlines()
        create_rom(lines, debug_symbols)  