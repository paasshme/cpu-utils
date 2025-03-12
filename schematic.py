import mcschematic

save_folder = r"C:\Users\jacqu\AppData\Roaming\.minecraft\config\worldedit\schematics"
schem_name = "prog"


def get_element_with_fallback(arr, index, fallback):
    return arr[index] if index < len(arr) else fallback

def full_one(x,y,z, repeater_direction, schem):
    create_instruction([1]*16, x,y,z, repeater_direction, schem)

def create_instruction(line, x,y,z, repeater_direction, schem):
    byte1 = line[:8]
    byte2 = line[8:16]
    for i, char in enumerate(byte1):
        if char == "1":
            schem.setBlock((x, y, z),f"minecraft:repeater[facing={repeater_direction}]")
        elif char == "0":
            schem.setBlock((x, y, z),f"minecraft:purple_concrete")
        schem.setBlock((x, y-1, z),"minecraft:purple_concrete")
        y -= 2

    y -= 2
    for i, char in enumerate(byte2):
        if char == "1":
            schem.setBlock((x, y, z),f"minecraft:repeater[facing={repeater_direction}]")
        elif char == "0":
            schem.setBlock((x, y, z),f"minecraft:purple_concrete")
        schem.setBlock((x, y-1, z),"minecraft:purple_concrete")
        y -= 2


def create_rom(lines, debug_symbols = None):
    schem = mcschematic.MCSchematic()

    # 0 0 0 => first block of first instruction

    x_offset = 0
    y_offset = 0
    z = 0

    while len(lines) <= 511:
        lines.append('0000000000000000\n')


    d = {}
    # print(lines)

    for i in range(len(lines)): # for all cols
        line = lines[i]

        if len(line) != 17:
            print(f"Incorrect instruction size f{len(line)} for {line}")

        """
        determine which ROM block(32 ins each) to use (16 possibilities, 4 LSBs)
        Positions of the 16 blocks:
        ---------
        14 15
        12 13
        ...
        4 5
        2 3
        0 1
        --------

        A block is the following (right block, left blocks are symetrics)
        ------
        31 30 29... 16
        0 1 2 .. 15
        -----

        Example: Instruction line 20 should be in block 4, position 1 (in the block)
        Because:
        0b0001 0100 & 0b1111 = 4
        0b0001 0100 >> 4 = 1
        if rom block is even, offset is positive
        """
        mask = 0b1111
        block_to_use = i & mask
        position_in_block = i >> 4


        # for first block
        offset_z = 4 + 2 * (position_in_block % 16)
        offset_z = offset_z if i % 2 == 0 else -offset_z

        block_offset = (-9 * (block_to_use // 2) )
        offset_x = block_offset -1 if position_in_block > 15 else block_offset + 1
        repeater_direction = "west" if position_in_block > 15 else "east"
        create_instruction(line, offset_x, y_offset, offset_z, repeater_direction, schem)

        # full_one(offset_x, y_offset, offset_z,  , schem)
        # create_instruction(line, offset_x, y_offset, offset_z,  "west" if position_in_block > 15 else "east", schem)
        # schem.setBlock((offset_x, y_offset, offset_z), "minecraft:redstone_lamp",)
        # schem.setBlock((offset_x, y_offset+1, offset_z), f"minecraft:repeater[facing={]")
        # if debug_symbols:
        #     debug_data = get_element_with_fallback(debug_symbols,i, None)
        #     if debug_data:
        #         schem.setBlock((x_offset, y_offset+1, z-1),
        #             f"""minecraft:acacia_sign{{front_text:{{messages:['{{"text":"{i}"}}','{{"text":"{debug_data}"}}','{{"text":""}}','{{"text":""}}']}}}}"""
        #         )
        # schem.setBlock((x_offset, y_offset, z-1), "minecraft:redstone_lamp")

        
        # byte1 = line[:8]
        # byte2 = line[8:]
        # for i, char in enumerate(byte1):
        #     # print(i, char)
        #     if char == "1":
        #         schem.setBlock((x_offset, y_offset, z),"minecraft:repeater[facing=south]")
        #     schem.setBlock((x_offset, y_offset-1, z),"minecraft:purple_concrete")
        #     schem.setBlock((x_offset, y_offset, z-1), "minecraft:redstone_lamp")

        #     y_offset -= 2

        # y_offset -= 2
        # for i, char in enumerate(byte2):
        #     if char == "1":
        #         schem.setBlock((x_offset, y_offset, z), "minecraft:repeater[facing=south]")
        #     schem.setBlock((x_offset, y_offset-1, z),"minecraft:purple_concrete")
        #     schem.setBlock((x_offset, y_offset, z-1), "minecraft:redstone_lamp")

        #     y_offset -= 2

        # y_offset = 0
        # x_offset -= 2
    schem.save(save_folder, schem_name, mcschematic.Version.JE_1_20_1)
    print(f"Schema saved as {schem_name} !")
if __name__ == '__main__':
    with open("build/output.bin") as f:
        lines = f.readlines()
        create_rom(lines)