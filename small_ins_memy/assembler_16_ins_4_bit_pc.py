operations_dict = {
    "NOP": "0000",
    "ADD": "0001",
    "SUB": "0010",
    "XOR": "0011",
    "LB": "0100",
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
    "ST": "1111"
}

debug_info = False
three_operands = ["ADD", "SUB", "XOR", "XNOR", "AND", "NAND"]
immediate =  ["LDI", "ADI"]
jumps = ["CALL", "RET",  "JMP", "BRZ", "BRNZ", "BRC", "BRNC"]
memy = ["ST", "LB"]

def translate_labels(datas):
    labels = {}
    address_counter = 0
    # Collect labels and their addresses
    for data in datas:
        data = data.strip()
        if data.startswith("#") or data.startswith("//") or data == "":
            continue
        if data.startswith(".") and data.endswith(":"):
            label = data[:-1]
            labels[label] = address_counter
        else:
            address_counter += 1
    return labels


def check_instruction_limit(datas):
    instructions = [data for data in datas if not (data.strip().startswith("#") or data.strip().startswith("//") or data.strip() == "")]

    if len(instructions) > 16:
        print("Error, too much instructions")
        return False
    return True


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
    return res

def handle_others(operation) -> str:
    return "0000000000000000"

def handle_jumps(operation, address: None) -> str:
    res = f"{operations_dict[operation]}"
    if operation == "CALL":
        res = f"{res}{'0'*8}{format(int(address), '04b')}"
    elif operation == "RET":
        res= f"{res}{'0'*12}"
    elif operation == "JMP":
        target = format(int(address), '04b')
        res += f"00000000{target}"
    elif operation.startswith("BR"): 
        target = format(int(address), '04b')
        # 6 bits as operation include 2 opcodes bits
        res += f"000000{target}"
    return res

def handle_memy(operation, address_reg, data_reg, offset):
    res = f"{operations_dict[operation]}"
    if operation in ["ST", "LB"]:
        
        res += f"{format(int(address_reg[1:]), '04b')}{format(int(data_reg[1:]), '04b')}{format(int(offset), '04b')}"
    return res

def preassemble(input_file, dest):
    with open(input_file, 'r') as f:
        datas = f.readlines()
    if not check_instruction_limit(datas):
        return
    
    output = []
    labels = translate_labels(datas)
    print(labels)
    for data in datas:
        data = data.strip()
        d = data.split()
        operation = d[0]
        if operation.startswith("#") or operation.startswith("//") or operation == "":
            continue
        #ignore label with form .label:
        elif  operation.startswith(".") and operation.endswith(":"):
            continue
        elif operation in jumps and operation != "RET"  and d[1] in labels:
            address = labels[d[1]]

            output.append(f"{operation} {address}")
        else:
            output.append(data)

    with open(dest, "w") as f:
        for i,out in enumerate(output):
            f.write(f"{i} {out}\n")
        f.write("END - HALT")

def assemble(input_file, dest):
    assembled = []
    datas = []
    labels = {}
    with open(input_file, 'r') as f:
        datas = f.readlines()


    if not check_instruction_limit(datas):
        return

    # First pass: collect labels and their addresses
    labels = translate_labels(datas)
    print(labels)
    # Second pass assemble instructions
    for data in datas:
        data = data.rstrip()
        d = data.split()
        operation = d[0]
        print(operation, d)
        if operation.startswith("#") or operation.startswith("//") or operation == "":
            continue
        #ignore label with form .label:
        elif  operation.startswith(".") and operation.endswith(":"):
            continue
        elif operation in three_operands:
            assembled.append(handle_3_operands(d[0], d[1:]))
        elif operation in immediate:
            assembled.append(handle_immediate(d[0], d[1:]))
        elif operation in jumps and len(d) > 1 and d[1] in labels:
            address = labels[d[1]]
            print(address, labels)
            assembled.append(handle_jumps(d[0], address))
        elif operation in jumps:
            assembled.append(handle_jumps(d[0], d[1] if len(d) > 1 else None))
        elif operation == "HALT":
            assembled.append(f"{operations_dict['HALT']}{'0'*12}")
        elif operation in memy:
            assembled.append(handle_memy(d[0], d[1], d[2], d[3]))
        else:
            print("unknown op ", d[0])
            assembled.append(handle_others(d[0]))

    print(assembled)

    with open(dest, 'w') as f:
        for asm in assembled:
            print(asm)
            f.write(asm + '\n')
        if len(assembled) < 16:
            print("add halt")
            f.write(f"{operations_dict['HALT']}000000000000\n")


if __name__ == '__main__':
    assemble("main.as", "output.bin")
    preassemble("main.as", "output.asx")