import mcschematic

save_folder = r"C:\Users\jacqu\AppData\Roaming\.minecraft\config\worldedit\schematics"

def get_element_with_fallback(arr, index, fallback):
    return arr[index] if index < len(arr) else fallback


def create_rom(lines, debug_symbols = None):
    schem = mcschematic.MCSchematic()

    # 0 0 0 => first block of first instruction

    x_offset = 0
    y_offset = 0
    z = 0

    while len(lines) < 16:
        lines.append('0000000000000000')


    print(lines)

    for i in range(len(lines)): # for all cols
        line = lines[i]

        if len(line) != 16:
            print("error", line[0])

        if debug_symbols:
            debug_data = get_element_with_fallback(debug_symbols,i, None)
            if debug_data:
                schem.setBlock((x_offset, y_offset+1, z-1),
                    f"""minecraft:acacia_sign{{front_text:{{messages:['{{"text":"{i}"}}','{{"text":"{debug_data}"}}','{{"text":""}}','{{"text":""}}']}}}}"""
                )
        schem.setBlock((x_offset, y_offset, z-1), "minecraft:redstone_lamp")

        
        byte1 = line[:8]
        byte2 = line[8:]
        for i, char in enumerate(byte1):
            # print(i, char)
            if char == "1":
                schem.setBlock((x_offset, y_offset, z),"minecraft:repeater[facing=south]")
            schem.setBlock((x_offset, y_offset-1, z),"minecraft:purple_concrete")
            schem.setBlock((x_offset, y_offset, z-1), "minecraft:redstone_lamp")

            y_offset -= 2

        y_offset -= 2
        for i, char in enumerate(byte2):
            if char == "1":
                schem.setBlock((x_offset, y_offset, z), "minecraft:repeater[facing=south]")
            schem.setBlock((x_offset, y_offset-1, z),"minecraft:purple_concrete")
            schem.setBlock((x_offset, y_offset, z-1), "minecraft:redstone_lamp")

            y_offset -= 2

        y_offset = 0
        x_offset -= 2

    schem.save(save_folder, "program", mcschematic.Version.JE_1_20_1)


if __name__ == '__main__':
    with open("output.bin") as f:
        lines = f.readlines()
        create_rom(lines)