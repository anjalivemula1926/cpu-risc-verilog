# ============================================
# Simple Assembler for 8-bit RISC Processor
# Author  : Anjali
# College : MANIT Bhopal
# ============================================

# opcode table
opcodes = {
    'ADD'  : '0000',
    'SUB'  : '0001',
    'AND'  : '0010',
    'OR'   : '0011',
    'XOR'  : '0100',
    'NOT'  : '0101',
    'MOV'  : '0110',
    'LOAD' : '0111',
    'STORE': '1000',
    'JMP'  : '1001',
    'BEQ'  : '1010'
}

# register table
registers = {
    'R0': '000',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'R7': '111'
}

def assemble(input_file, output_file):

    with open(input_file, 'r') as f:
        lines = f.readlines()

    instructions = []
    errors       = []
    line_num     = 0

    for line in lines:
        line_num += 1

        # remove comments and whitespace
        line = line.split('#')[0].strip()
        if not line:
            continue

        parts = line.split()
        op    = parts[0].upper()

        if op not in opcodes:
            errors.append(f"Line {line_num}: Unknown instruction '{op}'")
            continue

        opcode = opcodes[op]
        binary = ''

        try:
            # ── MOV rd, immediate ──────────────────────
            if op == 'MOV':
                rd  = registers[parts[1].upper()]
                imm = int(parts[2])
                if imm < 0 or imm > 511:
                    errors.append(f"Line {line_num}: Immediate {imm} out of range 0-511")
                    continue
                imm_bin = format(imm, '09b')
                binary  = opcode + rd + imm_bin

            # ── JMP address ────────────────────────────
            elif op == 'JMP':
                addr    = int(parts[1])
                if addr < 0 or addr > 63:
                    errors.append(f"Line {line_num}: Address {addr} out of range 0-63")
                    continue
                addr_bin = format(addr, '06b')
                binary   = opcode + '000000' + addr_bin

            # ── BEQ rd, address ────────────────────────
            elif op == 'BEQ':
                rd       = registers[parts[1].upper()]
                addr     = int(parts[2])
                addr_bin = format(addr, '06b')
                binary   = opcode + rd + '000' + addr_bin

            # ── NOT rd, rs1 ────────────────────────────
            elif op == 'NOT':
                rd     = registers[parts[1].upper()]
                rs1    = registers[parts[2].upper()]
                binary = opcode + rd + rs1 + '000000'

            # ── LOAD rd, rs1 ───────────────────────────
            elif op == 'LOAD':
                rd     = registers[parts[1].upper()]
                rs1    = registers[parts[2].upper()]
                binary = opcode + rd + rs1 + '000000'

            # ── STORE rs1, rs2 ─────────────────────────
            elif op == 'STORE':
                rs1    = registers[parts[1].upper()]
                rs2    = registers[parts[2].upper()]
                binary = opcode + '000' + rs1 + rs2 + '000'

            # ── ADD SUB AND OR XOR rd, rs1, rs2 ────────
            else:
                rd     = registers[parts[1].upper()]
                rs1    = registers[parts[2].upper()]
                rs2    = registers[parts[3].upper()]
                binary = opcode + rd + rs1 + rs2 + '000'

        except (KeyError, IndexError, ValueError) as e:
            errors.append(f"Line {line_num}: Error in '{line}' — {e}")
            continue

        # convert binary string to hex
        hex_val = format(int(binary, 2), '04X')
        instructions.append((line_num, line, binary, hex_val))

    # ── print errors if any ────────────────────────
    if errors:
        print("─── ERRORS ──────────────────────────────")
        for err in errors:
            print(err)
        print("─────────────────────────────────────────")
        return

    # ── write output .mem file ─────────────────────
    with open(output_file, 'w') as out:
        for _, _, _, hex_val in instructions:
            out.write(hex_val + '\n')

    # ── print assembly listing ─────────────────────
    print("─── Assembly Listing ────────────────────────────────────────")
    print(f"{'Addr':<6} {'Assembly':<20} {'Binary':<18} {'Hex'}")
    print("─────────────────────────────────────────────────────────────")
    for i, (line_num, asm, binary, hex_val) in enumerate(instructions):
        print(f"{i:<6} {asm:<20} {binary:<18} {hex_val}")
    print("─────────────────────────────────────────────────────────────")
    print(f"Total instructions: {len(instructions)}")
    print(f"Output written to: {output_file}")
    print("Assembly successful!")

# ── run assembler ──────────────────────────────────
assemble('program.asm', 'program.mem')