operations_dict = {
    "NOP": "0000",
    "ADD": "0001",
    "SUB": "0010",
    "XOR": "0011",
    "NOR": "0100",
    "XNOR": "0101",
    "AND": "0110",
    "NAND": "0111",
    "LDI": "1000",
    "HALT": "1001",
    "ADI": "1010",
    "JMP": "1011",
    "BRZ": "110001",
    "BRNZ": "110011",
    "BRC": "110010",
    "BRNC": "110000",
    "CALL": "1101",
    "RET": "1110",
    "WD": "1111"
}

three_operands = ["ADD", "SUB", "XOR", "NOR", "XNOR", "AND", "NAND"]
immediate =  ["LDI", "ADI", "JMP", "BRZ", "BRNZ", "BRC", "BRNC"]
function = ["CALL", "RET"]

def handle_3_operands(operation, args) -> str:
    assemble = operations_dict[operation]
    operands = []
    pretty_formatted = ""
    for operand in args:
        if operand.startswith('r'):
            operands.append(format(int(operand[1:]), '04b'))
    res = f"{assemble}{"".join(operands)}"
    pretty_formatted += (f"{assemble} {[op for op in operands]}")
    return res

def handle_immediate(operation, address) -> str:

    res = f"{operations_dict[operation]}"
    if operation in ["LDI", "ADI"]:
        reg = format(int(address[0][1:]), '04b')
        target = format(int(address[1]), '08b')
        res += f"{reg}{target}"
    elif operation == "JMP":
        target = format(int(address[0]), '04b')
        res += f"00000000{target}"
    else:
        target = format(int(address[0]), '04b')
        # 6 bits as operation include 2 opcodes bits
        res += f"000000{target}"
    return res

def handle_others(operation) -> str:
    return "0000000000000000"

def handle_functions(operation, address: None) -> str:
    if operation == "CALL":
        return f"{operations_dict[operation]}{'0'*8}{format(int(address), '04b')}"
    elif operation == "RET":
        return f"{operations_dict[operation]}{'0'*12}"

def assemble(input_file, dest):

    assembled = []
    datas = []
    with open(input_file, 'r') as f:
        datas = f.readlines()

    if len(datas) > 16:
        print("Error, too much instructions")
        return
    for data in datas:
        d = data.split()
        operation = d[0]
        if operation in three_operands:
            assembled.append(handle_3_operands(d[0], d[1:]))
        elif operation in immediate:
            assembled.append(handle_immediate(d[0], d[1:]))
        elif operation in function:
            assembled.append(handle_functions(d[0], d[1] if len(d) > 1 else None))
        elif operation == "HALT":
            assembled.append(f"{operations_dict['HALT']}{'0'*12}")
        else:
            print("unknown op ", d[0])
            assembled.append(handle_others(d[0]))

    print(assembled)

    with open(dest, 'w') as f:
        for asm in assembled:
            print(asm)
            f.write(asm + '\n')
        if len(assembled) < 16:
            f.write(f"{operations_dict['HALT']}000000000000\n")


if __name__ == '__main__':
    assemble("main.as", "output.bin")