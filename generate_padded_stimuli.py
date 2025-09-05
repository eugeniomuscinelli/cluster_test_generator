import argparse

def generate_stimuli(input_file, output_header="stimuli.h"):
    stimuli_dict = {}

    # Read the input stimuli
    with open(input_file, "r") as file:
        for line in file:
            parts = line.strip().split("_")
            if len(parts) == 2:
                address = int(parts[0], 16)
                instruction = int(parts[1], 16)
                stimuli_dict[address] = instruction

    # Sort the addresses
    sorted_addresses = sorted(stimuli_dict.keys())

    BASE_ADDRESS = sorted_addresses[0]
    stimuli_list = []

    # Fill in holes with 0s
    current_address = BASE_ADDRESS
    for addr in sorted_addresses:
        while current_address < addr:
            stimuli_list.append((current_address, 0x0))  # Fill with zeros
            current_address += 8  # Advance by 8 bytes (64 bits)
        stimuli_list.append((addr, stimuli_dict[addr]))
        current_address = addr + 8

    # Generate the header
    with open(output_header, "w") as header:
        header.write("#ifndef STIMULI_H\n#define STIMULI_H\n\n")
        header.write("#include <stdint.h>\n\n")
        header.write("typedef struct {\n")
        header.write("    uint64_t address;\n")
        header.write("    uint64_t instruction;\n")
        header.write("} Stimulus;\n\n")

        header.write("static const Stimulus stimuli[] = {\n")
        for addr, instr in stimuli_list:
            header.write(f"    {{0x{addr:08X}, 0x{instr:016X}}},\n")
        header.write("};\n\n")

        header.write("#define BASE_ADDRESS 0x{:08X}\n".format(BASE_ADDRESS))
        header.write("#define NUM_STIMULI {}\n\n".format(len(stimuli_list)))
        header.write("#endif // STIMULI_H\n")

    print(f"Generated {output_header} with {len(stimuli_list)} entries including padded zeros.")

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate stimuli.h from a JTAG stimuli file.")
    parser.add_argument("input_file", help="Path to the JTAG stimuli .txt file")
    args = parser.parse_args()
    generate_stimuli(args.input_file)
