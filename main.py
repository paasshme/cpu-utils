from assembler import assemble, preassemble, format_bin
from schematic import create_rom
import sys
import os.path
if __name__ == '__main__':

    asm_file = "main.as"
    if len( sys.argv ) == 2:
        asm_file = sys.argv[1]
        if not os.path.isfile(asm_file):
            print(f"File not found {asm_file}")
            exit(1)

    print(f"Assembling {asm_file}")
    assemble(asm_file, "build/output.bin")
    debug_symbols = None
    preassemble(asm_file, "build/output.asx")
    with open("build/output.asx", "r") as r:
        debug_symbols = r.readlines()
    with open("build/output.bin") as f:
        lines = f.readlines()
        create_rom(lines, debug_symbols)

    format_bin("build/output.bin", "build/output_formatted.txt")