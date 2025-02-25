from assembler import assemble
from schematic import create_rom


if __name__ == '__main__':
    assemble("main.as", "output.bin")
    debug_symbols = None
    with open("main.as", "r") as r:
        debug_symbols = r.readlines()
    with open("output.bin") as f:
        lines = f.readlines()
        create_rom(lines, debug_symbols)  